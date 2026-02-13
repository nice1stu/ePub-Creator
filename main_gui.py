# main_gui.py - Version 2.1.0
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from converter_logic import eBookConverterLogic

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("eBook Routing Converter v2.1.0")
        self.root.geometry("550x550")
        self.logic = eBookConverterLogic()
        
        # Default Folders
        self.source_dir = os.path.join(os.getcwd(), "To_Be_Processed")
        self.output_dir = os.path.join(os.getcwd(), "Processed")
        self.cover_path = None

        # Ensure folders exist on startup
        for folder in [self.source_dir, self.output_dir]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.setup_ui()

    def setup_ui(self):
        # --- Folder Selection ---
        tk.Label(self.root, text="Step 1: Folder Configuration", font=("Arial", 10, "bold")).pack(pady=10)
        
        # Source Folder
        f1 = tk.Frame(self.root)
        f1.pack(fill="x", padx=20)
        self.lbl_source = tk.Label(f1, text=f"Source: ...{self.source_dir[-30:]}", fg="blue")
        self.lbl_source.pack(side="left")
        tk.Button(f1, text="Browse", command=self.browse_source).pack(side="right")

        # Output Folder
        f2 = tk.Frame(self.root)
        f2.pack(fill="x", padx=20, pady=5)
        self.lbl_output = tk.Label(f2, text=f"Output: ...{self.output_dir[-30:]}", fg="blue")
        self.lbl_output.pack(side="left")
        tk.Button(f2, text="Browse", command=self.browse_output).pack(side="right")

        tk.Frame(self.root, height=2, bd=1, relief="sunken").pack(fill="x", padx=20, pady=15)

        # --- Metadata ---
        tk.Label(self.root, text="Step 2: Metadata", font=("Arial", 10, "bold")).pack()
        tk.Label(self.root, text="Book Title:").pack()
        self.ent_title = tk.Entry(self.root, width=45)
        self.ent_title.pack(pady=5)

        tk.Label(self.root, text="Author Name:").pack()
        self.ent_author = tk.Entry(self.root, width=45)
        self.ent_author.pack(pady=5)

        # --- Cover ---
        self.lbl_cover = tk.Label(self.root, text="No cover selected", fg="gray")
        self.lbl_cover.pack(pady=(10,0))
        tk.Button(self.root, text="Select Cover Image", command=self.browse_cover).pack()

        tk.Frame(self.root, height=2, bd=1, relief="sunken").pack(fill="x", padx=20, pady=15)

        # --- Convert ---
        self.btn_convert = tk.Button(
            self.root, text="Select File From Source & Convert", 
            command=self.run_conversion, 
            bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), height=2
        )
        self.btn_convert.pack(pady=10)

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w").pack(side="bottom", fill="x")

    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_dir = path
            self.lbl_source.config(text=f"Source: ...{path[-30:]}")

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir = path
            self.lbl_output.config(text=f"Output: ...{path[-30:]}")

    def browse_cover(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if path:
            self.cover_path = path
            self.lbl_cover.config(text=f"Cover: {os.path.basename(path)}", fg="green")

    def run_conversion(self):
        title = self.ent_title.get().strip() or "Untitled"
        author = self.ent_author.get().strip() or "Unknown Author"

        # Force file selection to start in the source folder
        file_path = filedialog.askopenfilename(
            initialdir=self.source_dir,
            title="Select file from source folder",
            filetypes=[("All Supported", "*.rtf *.txt *.pdf *.docx")]
        )

        if file_path:
            self.status_var.set("Processing...")
            self.root.update_idletasks()
            
            success, result = self.logic.convert_to_epub(
                file_path, self.output_dir, title, author, self.cover_path
            )
            
            if success:
                self.status_var.set("Success!")
                messagebox.showinfo("Done", f"File saved to:\n{result}")
            else:
                self.status_var.set("Error")
                messagebox.showerror("Error", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()