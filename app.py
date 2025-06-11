import tkinter as tk
from tkinter import filedialog, messagebox
from encryptor import encryptPDF  # Ensure encryptor.py has encryptPDF
from decryptor import main as decrypt_file_main  # We will call main() logic here in wrapper

import os

def run_decryption_gui_wrapper(drm_path):
    try:
        import decryptor
        decryptor.main_entrypoint(drm_path)
    except Exception as e:
        messagebox.showerror("Decryption Error", str(e))

class DRMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure DRM PDF Application")
        self.geometry("480x400")
        self.configure(bg="#f2f2f2")
        self.resizable(True, True)

        self.mode = tk.StringVar(value="Sender")
        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(self, text="DRM PDF Tool", font=("Helvetica", 18, "bold"), bg="#f2f2f2")
        header.pack(pady=10)

        mode_frame = tk.Frame(self, bg="#f2f2f2")
        mode_frame.pack()

        tk.Label(mode_frame, text="Select Mode:", font=("Helvetica", 12), bg="#f2f2f2").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(mode_frame, text="Sender", variable=self.mode, value="Sender", command=self.switch_mode, bg="#f2f2f2").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="Receiver", variable=self.mode, value="Receiver", command=self.switch_mode, bg="#f2f2f2").pack(side=tk.LEFT)

        self.form_frame = tk.Frame(self, bg="#f2f2f2")
        self.form_frame.pack(pady=20)

        self.switch_mode()

    def switch_mode(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        if self.mode.get() == "Sender":
            self.build_sender_ui()
        else:
            self.build_receiver_ui()

    def build_sender_ui(self):
        tk.Label(self.form_frame, text="Select PDF to Protect", font=("Helvetica", 10), bg="#f2f2f2").pack()
        self.pdf_path_var = tk.StringVar()
        tk.Entry(self.form_frame, textvariable=self.pdf_path_var, width=50).pack(pady=5)
        tk.Button(self.form_frame, text="Browse", command=self.browse_pdf).pack(pady=5)

        tk.Label(self.form_frame, text="Expiration Date (YYYY-MM-DD HH:MM:SS)", font=("Helvetica", 10), bg="#f2f2f2").pack(pady=(10, 0))
        self.expiry_var = tk.StringVar()
        tk.Entry(self.form_frame, textvariable=self.expiry_var, width=30).pack(pady=5)

        tk.Label(self.form_frame, text="Allowed IP Address (Optional)", font=("Helvetica", 10), bg="#f2f2f2").pack()
        self.allowed_ip_var = tk.StringVar()
        tk.Entry(self.form_frame, textvariable=self.allowed_ip_var, width=30).pack(pady=5)

        tk.Label(self.form_frame, text="Your Email (First open only)", font=("Helvetica", 10), bg="#f2f2f2").pack()
        self.email_var = tk.StringVar()
        tk.Entry(self.form_frame, textvariable=self.email_var, width=30).pack(pady=5)

        tk.Button(self.form_frame, text="Protect PDF", command=self.encrypt_file, bg="#4CAF50", fg="white", width=20).pack(pady=15)

    def browse_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_path_var.set(path)

    def encrypt_file(self):
        pdf_path = self.pdf_path_var.get()
        expiry = self.expiry_var.get()
        allowed_ip = self.allowed_ip_var.get()
        email = self.email_var.get()

        if not pdf_path or not expiry or not email:
            messagebox.showerror("Missing Info", "PDF path, Expiration date and Email are required.")
            return

        try:
            encryptPDF(pdf_path, expiry, allowed_ip, email)  # Adjusted encryptor to accept 4 args
            messagebox.showinfo("Success", "PDF Protected Successfully!")
        except Exception as e:
            messagebox.showerror("Encryption Error", f"{e}")

    def build_receiver_ui(self):
        tk.Label(self.form_frame, text="Select DRM File", font=("Helvetica", 10), bg="#f2f2f2").pack()
        self.drm_path_var = tk.StringVar()
        tk.Entry(self.form_frame, textvariable=self.drm_path_var, width=50).pack(pady=5)
        tk.Button(self.form_frame, text="Browse", command=self.browse_drm).pack(pady=5)

        tk.Button(self.form_frame, text="Open Secure Viewer", command=self.decrypt_and_view, bg="#2196F3", fg="white", width=20).pack(pady=15)

    def browse_drm(self):
        path = filedialog.askopenfilename(filetypes=[("DRM files", "*.drm")])
        if path:
            self.drm_path_var.set(path)

    def decrypt_and_view(self):
        path = self.drm_path_var.get()
        if not path:
            messagebox.showerror("Missing Info", "Select a .drm file to open.")
            return
        run_decryption_gui_wrapper(path)

if __name__ == "__main__":
    app = DRMApp()
    app.mainloop()
