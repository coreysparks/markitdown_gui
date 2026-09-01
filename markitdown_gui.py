"""
MarkItDown GUI
A small desktop app for the markitdown conversion tool.

This app lets you pick an input file, choose an output path,
and convert the file to Markdown. It uses tkinter, which is
part of the standard Python library, so no extra install is
needed for the interface itself. The markitdown package must
already be installed.

Run it with:
    python markitdown_gui.py
"""

import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from markitdown import MarkItDown


class MarkItDownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkItDown Converter")
        self.root.geometry("560x420")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        self._build_layout()

    def _build_layout(self):
        pad = {"padx": 10, "pady": 6}

        # Input file row
        tk.Label(self.root, text="Input file").grid(row=0, column=0, sticky="w", **pad)
        tk.Entry(self.root, textvariable=self.input_path, width=52).grid(
            row=1, column=0, columnspan=2, sticky="w", padx=10
        )
        tk.Button(self.root, text="Browse", command=self.choose_input).grid(
            row=1, column=2, padx=10
        )

        # Output file row
        tk.Label(self.root, text="Output Markdown file").grid(row=2, column=0, sticky="w", **pad)
        tk.Entry(self.root, textvariable=self.output_path, width=52).grid(
            row=3, column=0, columnspan=2, sticky="w", padx=10
        )
        tk.Button(self.root, text="Save as", command=self.choose_output).grid(
            row=3, column=2, padx=10
        )

        # Convert button
        self.convert_btn = tk.Button(
            self.root, text="Convert", command=self.start_conversion, width=20
        )
        self.convert_btn.grid(row=4, column=0, columnspan=3, pady=14)

        # Status log
        tk.Label(self.root, text="Status").grid(row=5, column=0, sticky="w", padx=10)
        self.log = scrolledtext.ScrolledText(self.root, width=68, height=14, state="disabled")
        self.log.grid(row=6, column=0, columnspan=3, padx=10, pady=6)

    def choose_input(self):
        path = filedialog.askopenfilename(
            title="Choose a file to convert",
            filetypes=[
                ("Supported files", "*.pdf *.docx *.pptx *.xlsx *.html *.htm *.csv *.json *.xml *.txt *.zip"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.input_path.set(path)
            # Suggest an output path next to the input file
            if not self.output_path.get():
                suggested = str(Path(path).with_suffix(".md"))
                self.output_path.set(suggested)

    def choose_output(self):
        path = filedialog.asksaveasfilename(
            title="Choose where to save the Markdown file",
            defaultextension=".md",
            filetypes=[("Markdown file", "*.md"), ("All files", "*.*")],
        )
        if path:
            self.output_path.set(path)

    def write_log(self, text):
        self.log.configure(state="normal")
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.configure(state="disabled")

    def start_conversion(self):
        in_path = self.input_path.get().strip()
        out_path = self.output_path.get().strip()

        if not in_path:
            messagebox.showwarning("Missing file", "Choose an input file first.")
            return
        if not out_path:
            messagebox.showwarning("Missing output", "Choose where to save the result.")
            return
        if not Path(in_path).exists():
            messagebox.showerror("File not found", "The input file does not exist.")
            return

        self.convert_btn.configure(state="disabled")
        self.write_log(f"Converting: {in_path}")

        # Run the conversion in a background thread so the window does not freeze
        thread = threading.Thread(target=self._convert, args=(in_path, out_path), daemon=True)
        thread.start()

    def _convert(self, in_path, out_path):
        try:
            converter = MarkItDown()
            result = converter.convert(in_path)
            Path(out_path).write_text(result.text_content, encoding="utf-8")
            self.root.after(0, self._on_success, out_path)
        except Exception as exc:
            error_text = "".join(traceback.format_exception_only(type(exc), exc)).strip()
            self.root.after(0, self._on_failure, error_text)

    def _on_success(self, out_path):
        self.write_log(f"Done. Markdown saved to: {out_path}")
        self.convert_btn.configure(state="normal")
        messagebox.showinfo("Conversion complete", f"Markdown file saved to:\n{out_path}")

    def _on_failure(self, error_text):
        self.write_log(f"Error: {error_text}")
        self.convert_btn.configure(state="normal")
        messagebox.showerror("Conversion failed", error_text)


def main():
    root = tk.Tk()
    app = MarkItDownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
