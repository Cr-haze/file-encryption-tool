"""
File Encryption & Decryption Tool
----------------------------------
A simple, secure desktop tool to encrypt and decrypt any file using a
user-provided secret key. Built with Python, the `cryptography` library
(Fernet / AES), and Tkinter for the GUI.

How it works:
1. User selects a file and enters a secret key (password).
2. The key is stretched into a proper encryption key using PBKDF2 (so any
   password, short or long, works safely).
3. The file is encrypted with Fernet (AES-128 under the hood) and saved
   as a new file with a `.enc` extension.
4. The same secret key can later decrypt the `.enc` file back to its
   original form.

Run:
    pip install cryptography
    python file_encryptor.py
"""

import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# A fixed salt keeps this simple/portable. For stronger per-file security,
# you could generate a random salt and store it alongside the .enc file.
SALT = b"file-encryptor-tool-salt"


def derive_key(secret_key: str) -> bytes:
    """Turn a user-provided password into a valid 32-byte Fernet key."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=390_000,
    )
    key = kdf.derive(secret_key.encode("utf-8"))
    return base64.urlsafe_b64encode(key)


def encrypt_file(filepath: str, secret_key: str) -> str:
    fernet = Fernet(derive_key(secret_key))
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    out_path = filepath + ".enc"
    with open(out_path, "wb") as f:
        f.write(encrypted)
    return out_path


def decrypt_file(filepath: str, secret_key: str) -> str:
    fernet = Fernet(derive_key(secret_key))
    with open(filepath, "rb") as f:
        data = f.read()
    decrypted = fernet.decrypt(data)  # raises InvalidToken if key is wrong
    if filepath.endswith(".enc"):
        out_path = filepath[:-4]
    else:
        out_path = filepath + ".dec"
    with open(out_path, "wb") as f:
        f.write(decrypted)
    return out_path


class FileEncryptorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("File Encryption & Decryption Tool")
        self.root.geometry("460x260")
        self.root.resizable(False, False)

        self.filepath = tk.StringVar()

        tk.Label(root, text="🔒 File Encryption & Decryption Tool",
                 font=("Segoe UI", 14, "bold")).pack(pady=(16, 4))
        tk.Label(root, text="Encrypt or decrypt any file with a secret key.",
                 font=("Segoe UI", 9), fg="gray").pack(pady=(0, 16))

        # File selector row
        file_frame = tk.Frame(root)
        file_frame.pack(fill="x", padx=20)
        tk.Entry(file_frame, textvariable=self.filepath, state="readonly",
                 width=38).pack(side="left", fill="x", expand=True)
        tk.Button(file_frame, text="Browse…", command=self.browse_file).pack(
            side="left", padx=(8, 0))

        # Secret key row
        key_frame = tk.Frame(root)
        key_frame.pack(fill="x", padx=20, pady=16)
        tk.Label(key_frame, text="Secret key:").pack(side="left")
        self.key_entry = tk.Entry(key_frame, show="•")
        self.key_entry.pack(side="left", fill="x", expand=True, padx=(8, 0))

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Encrypt File", width=16, bg="#2e7d32",
                  fg="white", command=self.handle_encrypt).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Decrypt File", width=16, bg="#1565c0",
                  fg="white", command=self.handle_decrypt).grid(row=0, column=1, padx=6)

        self.status = tk.Label(root, text="", font=("Segoe UI", 9), fg="gray")
        self.status.pack(pady=(10, 0))

    def browse_file(self):
        path = filedialog.askopenfilename(title="Select a file")
        if path:
            self.filepath.set(path)

    def _validate(self):
        if not self.filepath.get():
            messagebox.showwarning("Missing file", "Please select a file first.")
            return False
        if not self.key_entry.get():
            messagebox.showwarning("Missing key", "Please enter a secret key.")
            return False
        return True

    def handle_encrypt(self):
        if not self._validate():
            return
        try:
            out_path = encrypt_file(self.filepath.get(), self.key_entry.get())
            self.status.config(text=f"✅ Encrypted → {os.path.basename(out_path)}", fg="green")
            messagebox.showinfo("Success", f"File encrypted:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Encryption failed", str(e))

    def handle_decrypt(self):
        if not self._validate():
            return
        try:
            out_path = decrypt_file(self.filepath.get(), self.key_entry.get())
            self.status.config(text=f"✅ Decrypted → {os.path.basename(out_path)}", fg="green")
            messagebox.showinfo("Success", f"File decrypted:\n{out_path}")
        except InvalidToken:
            messagebox.showerror("Decryption failed", "Wrong secret key or corrupted file.")
        except Exception as e:
            messagebox.showerror("Decryption failed", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorApp(root)
    root.mainloop()
