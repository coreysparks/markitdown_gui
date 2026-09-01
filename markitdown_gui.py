"""
MarkItDown GUI
A small desktop app for the markitdown conversion tool.

This app lets you pick any number of input files, choose an output
folder, and convert them all to Markdown. It uses tkinter, which is
part of the standard Python library, so no extra install is needed
for the interface itself. The markitdown package must already be
installed.

Run it with:
    python markitdown_gui.py
"""

import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from markitdown import MarkItDown


FILE_TYPES = [
    ("Supported files", "*.pdf *.docx *.pptx *.xlsx *.html *.htm *.csv *.json *.xml *.txt *.zip"),
    ("All files", "*.*"),
]


class MarkItDownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkItDown Converter")
        self.root.geometry("660x580")
        self.root.resizable(False, False)

        # Input files, in the order they were added. The listbox mirrors this.
        self.input_files = []
        self.output_dir = tk.StringVar()
        self.overwrite = tk.BooleanVar(value=True)

        self._build_layout()

    def _build_layout(self):
        pad = {"padx": 10, "pady": 6}

        # Input file list
        tk.Label(self.root, text="Input files").grid(row=0, column=0, sticky="w", **pad)

        list_frame = tk.Frame(self.root)
        list_frame.grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.file_list = tk.Listbox(
            list_frame,
            width=72,
            height=8,
            selectmode="extended",
            yscrollcommand=scrollbar.set,
        )
        scrollbar.configure(command=self.file_list.yview)
        self.file_list.pack(side="left")
        scrollbar.pack(side="left", fill="y")

        button_col = tk.Frame(self.root)
        button_col.grid(row=1, column=2, sticky="n", padx=10)
        tk.Button(button_col, text="Add files", width=12, command=self.choose_inputs).pack(pady=2)
        tk.Button(button_col, text="Remove", width=12, command=self.remove_selected).pack(pady=2)
        tk.Button(button_col, text="Clear", width=12, command=self.clear_inputs).pack(pady=2)

        # Output folder row
        tk.Label(self.root, text="Output folder").grid(row=2, column=0, sticky="w", **pad)
        tk.Entry(self.root, textvariable=self.output_dir, width=62).grid(
            row=3, column=0, columnspan=2, sticky="w", padx=10
        )
        tk.Button(self.root, text="Browse", command=self.choose_output_dir).grid(
            row=3, column=2, padx=10
        )

        tk.Checkbutton(
            self.root,
            text="Overwrite existing Markdown files",
            variable=self.overwrite,
        ).grid(row=4, column=0, columnspan=2, sticky="w", padx=10)

        # Convert button and progress bar
        self.convert_btn = tk.Button(
            self.root, text="Convert", command=self.start_conversion, width=20
        )
        self.convert_btn.grid(row=5, column=0, columnspan=3, pady=10)

        self.progress = ttk.Progressbar(self.root, length=620, mode="determinate")
        self.progress.grid(row=6, column=0, columnspan=3, padx=10)

        # Status log
        tk.Label(self.root, text="Status").grid(row=7, column=0, sticky="w", padx=10, pady=(8, 0))
        self.log = scrolledtext.ScrolledText(self.root, width=80, height=12, state="disabled")
        self.log.grid(row=8, column=0, columnspan=3, padx=10, pady=6)

    # ----- input list handling -----

    def choose_inputs(self):
        paths = filedialog.askopenfilenames(
            title="Choose files to convert",
            filetypes=FILE_TYPES,
        )
        added = 0
        for path in paths:
            path = str(Path(path))
            if path in self.input_files:
                continue
            self.input_files.append(path)
            self.file_list.insert(tk.END, path)
            added += 1
        if added:
            self.write_log(f"Added {added} file(s).")
        # Suggest the first file's folder as the output folder
        if self.input_files and not self.output_dir.get():
            self.output_dir.set(str(Path(self.input_files[0]).parent))

    def remove_selected(self):
        for index in sorted(self.file_list.curselection(), reverse=True):
            self.file_list.delete(index)
            del self.input_files[index]

    def clear_inputs(self):
        self.file_list.delete(0, tk.END)
        self.input_files.clear()

    def choose_output_dir(self):
        path = filedialog.askdirectory(
            title="Choose the folder for the Markdown files",
            initialdir=self.output_dir.get() or None,
            mustexist=False,
        )
        if path:
            self.output_dir.set(str(Path(path)))

    def write_log(self, text):
        self.log.configure(state="normal")
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.configure(state="disabled")

    # ----- conversion -----

    def start_conversion(self):
        files = list(self.input_files)
        out_dir = self.output_dir.get().strip()

        if not files:
            messagebox.showwarning("No files", "Add at least one input file first.")
            return
        if not out_dir:
            messagebox.showwarning("Missing output folder", "Choose an output folder first.")
            return

        missing = [f for f in files if not Path(f).exists()]
        if missing:
            messagebox.showerror(
                "Files not found",
                "These files no longer exist:\n\n" + "\n".join(missing),
            )
            return

        try:
            Path(out_dir).mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            messagebox.showerror("Output folder", f"Could not use that folder:\n{exc}")
            return

        self.convert_btn.configure(state="disabled")
        self.progress.configure(maximum=len(files), value=0)
        self.write_log(f"Converting {len(files)} file(s) into: {out_dir}")

        # Run the conversions in a background thread so the window does not freeze
        thread = threading.Thread(
            target=self._convert_all,
            args=(files, Path(out_dir), self.overwrite.get()),
            daemon=True,
        )
        thread.start()

    def _output_path_for(self, in_path, out_dir, used):
        """Pick a destination name, avoiding clashes between same-named inputs."""
        stem = Path(in_path).stem
        target = out_dir / f"{stem}.md"
        counter = 2
        while target in used:
            target = out_dir / f"{stem}_{counter}.md"
            counter += 1
        used.add(target)
        return target

    def _convert_all(self, files, out_dir, overwrite):
        converter = MarkItDown()
        used = set()
        succeeded = skipped = failed = 0
        total = len(files)

        for index, in_path in enumerate(files, start=1):
            out_path = self._output_path_for(in_path, out_dir, used)
            name = Path(in_path).name

            if out_path.exists() and not overwrite:
                skipped += 1
                self._post(f"[{index}/{total}] Skipped (already exists): {out_path.name}")
                self._post_progress(index)
                continue

            try:
                result = converter.convert(in_path)
                out_path.write_text(result.text_content, encoding="utf-8")
                succeeded += 1
                self._post(f"[{index}/{total}] {name} -> {out_path.name}")
            except Exception as exc:
                failed += 1
                error_text = "".join(traceback.format_exception_only(type(exc), exc)).strip()
                self._post(f"[{index}/{total}] Failed: {name}: {error_text}")
            self._post_progress(index)

        self.root.after(0, self._on_finished, succeeded, skipped, failed, out_dir)

    def _post(self, text):
        self.root.after(0, self.write_log, text)

    def _post_progress(self, value):
        self.root.after(0, self.progress.configure, {"value": value})

    def _on_finished(self, succeeded, skipped, failed, out_dir):
        summary = f"Done. {succeeded} converted, {skipped} skipped, {failed} failed."
        self.write_log(summary)
        self.convert_btn.configure(state="normal")
        if failed:
            messagebox.showwarning(
                "Conversion finished", f"{summary}\n\nSee the status log for details."
            )
        else:
            messagebox.showinfo(
                "Conversion complete", f"{summary}\n\nMarkdown files are in:\n{out_dir}"
            )


def main():
    root = tk.Tk()
    app = MarkItDownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
