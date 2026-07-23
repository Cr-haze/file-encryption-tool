# 🔒 File Encryption & Decryption Tool

A simple desktop tool that lets you encrypt and decrypt any file using a secret key — built with **Python**, the **`cryptography`** library (Fernet/AES), and a **Tkinter** GUI.

## Features

- 🔐 Encrypt any file into a secure `.enc` file
- 🔓 Decrypt an encrypted file back to its original form
- 🔑 User-defined secret key (no key files to manage)
- 🛡️ AES-based encryption via `cryptography.fernet`
- 🖥️ Simple, user-friendly desktop UI (Tkinter)
- ⚠️ Wrong-key protection — decryption fails safely if the key doesn't match

## How it works

1. User selects a file and enters a secret key.
2. The key is stretched into a proper 256-bit encryption key using **PBKDF2-HMAC-SHA256**, so any password (short or long) is used safely.
3. The file is encrypted using **Fernet** (AES-128 in CBC mode with HMAC authentication) and saved as `filename.enc`.
4. The same secret key can later decrypt the `.enc` file back to its original content.

## Tech stack

- Python 3
- `cryptography` (Fernet / AES / PBKDF2)
- Tkinter (built into Python's standard library)

## Getting started

```bash
git clone https://github.com/Cr-haze/file-encryption-tool.git
cd file-encryption-tool
pip install -r requirements.txt
python file_encryptor.py
```

1. Click **Browse…** to select a file.
2. Enter a secret key.
3. Click **Encrypt File** to create a `.enc` version, or **Decrypt File** to restore an existing `.enc` file (using the same key you encrypted it with).

## Use cases

- Secure personal documents
- Protect sensitive data before backing it up or sharing it
- Learn the basics of applied cryptography in Python

## What I learned

- File handling in Python
- Symmetric encryption/decryption with the `cryptography` library
- Key derivation (PBKDF2) for turning passwords into secure keys
- Building a simple GUI with Tkinter

## Next steps / ideas

- Add drag-and-drop file support
- Support encrypting entire folders
- Add a password strength check on the secret key itself
- Store a random salt per file instead of a fixed one, for stronger security

## Security note

This tool is meant as a learning project and for personal file protection. If you lose your secret key, the encrypted file **cannot** be recovered — there is no backdoor or key recovery.

## License

MIT — free to use, modify, and share.
