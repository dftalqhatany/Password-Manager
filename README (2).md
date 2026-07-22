# 🔐 Password Manager

A simple desktop password manager built with Python, using `tkinter` for the GUI and `SQLite` for storage. Passwords are encrypted before being saved to the database.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- 🔑 Generate strong random passwords (letters + numbers + symbols)
- 💾 Save credentials for any website (Website / Email / Password)
- 🔍 Search for previously saved credentials
- 🗑️ Delete saved credentials
- 🔒 Passwords are encrypted at rest using `cryptography` (Fernet)
- ⚠️ Warns before overwriting an existing website's entry
- 👁️ Show/hide password toggle
- 📋 Auto-copies generated passwords to the clipboard (if `pyperclip` is installed)
- ⌨️ Search by pressing Enter

## Project Structure

```
password_manager/
├── main.py             # Entry point of the app — run this file to start
├── frontend.py          # Tkinter GUI (PasswordManagerGUI class)
├── backend.py           # Business logic: database, encryption, password generation (PasswordManagerBE class)
├── requirements.txt     # Required Python packages
├── logo.png              # App logo (optional)
└── README.md
```

`main.py` is intentionally kept minimal — it just wires the two main classes together:

```python
import frontend, backend

frontend.main()
```

- **`PasswordManagerGUI`** (in `frontend.py`) — builds and runs the tkinter window.
- **`PasswordManagerBE`** (in `backend.py`) — handles the database, encryption, and password generation.

On first run, two files are created automatically in the project folder:
- `password_data.db` — SQLite database storing your credentials
- `secret.key` — encryption key used to protect the stored passwords

## Requirements

- Python 3.8+
- Packages listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/password-manager.git
   cd password-manager
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Add a `logo.png` file to the project folder to display it as the app logo. If missing, a 🔐 emoji is shown instead.

## Usage

```bash
python main.py
```

| Action | How to do it |
|---|---|
| Generate a password | Click **Generate** — it's auto-copied to your clipboard |
| Save new credentials | Fill in the three fields, then click **Add** |
| Search for a website | Type the website name and click **Search**, or press Enter |
| Delete credentials | Type the website name, click **Delete**, then confirm |
| Show/hide password | Click the 👁 button |

## ⚠️ Security Notes

- `secret.key` is the encryption key — **never share it or commit it to version control**. Anyone who has both `secret.key` and `password_data.db` can decrypt every stored password.
- Add the following to your `.gitignore`:
  ```
  secret.key
  password_data.db
  venv/
  __pycache__/
  ```
- This project is intended for learning purposes. For real-world use, consider a mature, audited password manager (e.g. Bitwarden, 1Password) that offers encrypted cloud sync, a master-password unlock flow, and independent security audits.

## Roadmap

- [ ] Master password required to unlock the app
- [ ] Browsable list of all saved websites
- [ ] Export/import credentials (backup)
- [ ] Password strength meter for manually entered passwords

## License

This project is licensed under the MIT License — feel free to use and modify it.
