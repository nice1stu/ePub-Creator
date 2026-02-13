# main_gui.py - Version 2.7.3
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
import os
import threading
import json  # Added for saving settings
from converter_logic import eBookConverterLogic

class ReviewDialog(simpledialog.Dialog):
    def __init__(self, parent, filename, t, a):
        self.filename = filename
        self.t, self.a = t, a
        super().__init__(parent, "Confirm Metadata")

    def body(self, master):
        tk.Label(master, text=f"Processing: {self.filename}", fg="#2980b9", font=("Segoe UI", 9, "bold"), wraplength=350).pack(pady=10)
        tk.Label(master, text="Title:").pack(anchor="w", padx=20)
        self.e1 = tk.Entry(master, width=55, font=("Segoe UI", 10))
        self.e1.insert(0, self.t); self.e1.pack(padx=20, pady=5)
        tk.Label(master, text="Author:").pack(anchor="w", padx=20)
        self.e2 = tk.Entry(master, width=55, font=("Segoe UI", 10))
        self.e2.insert(0, self.a); self.e2.pack(padx=20, pady=5)
        tk.Button(master, text="🔄 Swap Title/Author", command=self.swap, bg="#ecf0f1").pack(pady=10)
        return self.e1

    def swap(self):
        t, a = self.e1.get(), self.e2.get()
        self.e1.delete(0, tk.END); self.e1.insert(0, a)
        self.e2.delete(0, tk.END); self.e2.insert(0, t)

    def apply(self):
        self.result = (self.e1.get(), self.e2.get())

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini eBook Studio v2.7.3")
        self.root.geometry("600x550")
        self.logic = eBookConverterLogic()
        self.stop_event = threading.Event()
        self.config_file = "config.json"
        
        self.setup_ui()
        self.load_config() # Load paths on startup

    def setup_ui(self):
        f_frame = tk.LabelFrame(self.root, text=" Path Configuration ", padx=10, pady=10)
        f_frame.pack(fill="x", padx=15, pady=10)

        self.in_path = tk.StringVar(value="Not selected...")
        tk.Button(f_frame, text="📁 Source Folder", width=15, command=self.select_in).grid(row=0, column=0, pady=2)
        tk.Label(f_frame, textvariable=self.in_path, fg="#555").grid(row=0, column=1, sticky="w", padx=10)

        self.out_path = tk.StringVar(value="Not selected...")
        tk.Button(f_frame, text="📂 Output Folder", width=15, command=self.select_out).grid(row=1, column=0, pady=2)
        tk.Label(f_frame, textvariable=self.out_path, fg="#555").grid(row=1, column=1, sticky="w", padx=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.run_btn = tk.Button(btn_frame, text="▶ Start Batch", bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), width=15, command=self.start_thread)
        self.run_btn.pack(side="left", padx=5)

        self.stop_btn = tk.Button(btn_frame, text="⏹ Stop Process", bg="#c0392b", fg="white", font=("Segoe UI", 10, "bold"), width=15, command=self.request_stop, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        tk.Label(self.root, text="Activity Log:").pack(anchor="w", padx=15)
        self.log = scrolledtext.ScrolledText(self.root, height=12, font=("Consolas", 9))
        self.log.pack(fill="both", padx=15, pady=5, expand=True)

    # --- Config Management ---
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    if os.path.isdir(data.get("in_path", "")): self.in_path.set(data["in_path"])
                    if os.path.isdir(data.get("out_path", "")): self.out_path.set(data["out_path"])
            except: pass

    def save_config(self):
        data = {"in_path": self.in_path.get(), "out_path": self.out_path.get()}
        with open(self.config_file, "w") as f:
            json.dump(data, f)

    def select_in(self):
        path = filedialog.askdirectory()
        if path: 
            self.in_path.set(path)
            self.save_config()

    def select_out(self):
        path = filedialog.askdirectory()
        if path: 
            self.out_path.set(path)
            self.save_config()

    # --- Processing Logic ---
    def write_log(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def request_stop(self):
        self.stop_event.set()
        self.write_log(">> Stop requested... waiting for current task.")

    def start_thread(self):
        src, dst = self.in_path.get(), self.out_path.get()
        if not os.path.isdir(src) or not os.path.isdir(dst):
            messagebox.showerror("Error", "Select valid folders first.")
            return
        
        self.stop_event.clear()
        self.run_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        threading.Thread(target=self.process_loop, args=(src, dst), daemon=True).start()

    def process_loop(self, src, dst):
        files = [f for f in os.listdir(src) if f.lower().endswith(self.logic.allowed_formats)]
        self.root.after(0, lambda: self.write_log(f"--- Starting Batch: {len(files)} files ---"))

        for filename in files:
            if self.stop_event.is_set(): break
            
            full_path = os.path.join(src, filename)
            p_t, p_a = self.logic.parse_filename(full_path)
            data = self.logic.fetch_metadata_online(p_t, p_a)
            
            d_t = data['title'] if data else p_t
            d_a = data['author'] if data else p_a
            
            result_container = []
            def show_dialog():
                d = ReviewDialog(self.root, filename, d_t, d_a)
                result_container.append(d.result)

            self.root.after(0, show_dialog)
            
            while not result_container and not self.stop_event.is_set():
                self.root.update()
                self.root.after(100)

            if self.stop_event.is_set(): break
            
            if result_container and result_container[0]:
                f_t, f_a = result_container[0]
                self.root.after(0, lambda: self.write_log(f"Processing: {f_t}..."))
                
                if data and (f_t != data['title']):
                    data = self.logic.fetch_metadata_online(f_t, f_a)
                
                cover = self.logic.download_cover(data['cover_url']) if data else None
                success, _ = self.logic.convert_to_epub(full_path, dst, f_t, f_a, cover)
                
                msg = "  [SUCCESS]" if success else "  [FAILED]"
                self.root.after(0, lambda m=msg: self.write_log(m))
            else:
                self.root.after(0, lambda f=filename: self.write_log(f"Skipped: {f}"))

        self.root.after(0, self.finish_up)

    def finish_up(self):
        status = "stopped" if self.stop_event.is_set() else "finished"
        self.write_log(f"--- Batch Process {status} ---")
        self.run_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        messagebox.showinfo("Status", f"Processing {status}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()