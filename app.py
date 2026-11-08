import os
import sys
import json
import hashlib
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

import webview

APP_SALT = 'MTECH_APP_SEC_SALT_2026'
AUTH_FILE = Path(os.path.expanduser('~')) / '.mtech_auth_vault.json'


def hash_password(pwd: str) -> str:
    return hashlib.sha256((pwd + APP_SALT).encode('utf-8')).hexdigest()


def load_vault() -> dict:
    if AUTH_FILE.exists():
        try:
            with open(AUTH_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_vault(username: str, password_hash: str):
    data = {'username': username, 'password_hash': password_hash}
    try:
        with open(AUTH_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving auth vault: {e}")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('CloudBase ERP - Master Security Gateway')
        self.root.geometry('520x580')
        self.root.resizable(False, False)

        # Look for the ERP HTML on Desktop first, or adjacent to script
        self.desktop_html = Path(os.path.expanduser('~')) / 'Desktop' / 'Mangment 2.html'
        local_html = Path(__file__).resolve().parent / 'Mangment 2.html'
        if not self.desktop_html.exists() and local_html.exists():
            self.desktop_html = local_html

        if getattr(sys, 'frozen', False):
            try:
                base = Path(sys._MEIPASS)
                bundled = base / 'Mangment 2.html'
                if bundled.exists():
                    self.desktop_html = bundled
            except Exception:
                pass

        self.logged_in = False
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self.login_frame = ttk.Frame(self.root, padding=24)
        self.main_frame = ttk.Frame(self.root, padding=24)

        self.build_frames()

    def build_frames(self):
        vault = load_vault()
        if not vault:
            self.build_setup_frame()
        else:
            self.build_login_frame()
        self.build_main_frame()

    def build_setup_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        title = ttk.Label(self.login_frame, text='Master Security Setup', font=('Segoe UI', 18, 'bold'))
        title.pack(pady=(0, 6))

        subtitle = ttk.Label(
            self.login_frame,
            text='Create your private master credentials.\nOnly you will have access to this ERP system.',
            font=('Segoe UI', 9),
            justify='center'
        )
        subtitle.pack(pady=(0, 18))

        ttk.Label(self.login_frame, text='Administrator Username:', font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        user_entry = ttk.Entry(self.login_frame, textvariable=self.username_var)
        user_entry.pack(fill='x', pady=(2, 10))

        ttk.Label(self.login_frame, text='Create Master Password:', font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        pass_entry = ttk.Entry(self.login_frame, textvariable=self.password_var, show='*')
        pass_entry.pack(fill='x', pady=(2, 10))

        ttk.Label(self.login_frame, text='Confirm Master Password:', font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        confirm_entry = ttk.Entry(self.login_frame, textvariable=self.confirm_var, show='*')
        confirm_entry.pack(fill='x', pady=(2, 16))

        setup_btn = ttk.Button(self.login_frame, text='Save Master Credentials & Login', command=self.on_setup)
        setup_btn.pack(fill='x')

        status_label = ttk.Label(self.login_frame, textvariable=self.status_var, font=('Segoe UI', 9), foreground='#dc2626')
        status_label.pack(pady=(12, 0))

        self.login_frame.pack(expand=True, fill='both')

    def build_login_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

        title = ttk.Label(self.login_frame, text='CloudBase ERP Login', font=('Segoe UI', 20, 'bold'))
        title.pack(pady=(0, 6))

        subtitle = ttk.Label(self.login_frame, text='Enter your private master credentials to access the ERP.', font=('Segoe UI', 9))
        subtitle.pack(pady=(0, 20))

        ttk.Label(self.login_frame, text='Username:', font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        user_entry = ttk.Entry(self.login_frame, textvariable=self.username_var)
        user_entry.pack(fill='x', pady=(2, 12))

        ttk.Label(self.login_frame, text='Master Password:', font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        pass_entry = ttk.Entry(self.login_frame, textvariable=self.password_var, show='*')
        pass_entry.pack(fill='x', pady=(2, 18))

        login_button = ttk.Button(self.login_frame, text='Unlock ERP System', command=self.on_login)
        login_button.pack(fill='x')

        status_label = ttk.Label(self.login_frame, textvariable=self.status_var, font=('Segoe UI', 9), foreground='#dc2626')
        status_label.pack(pady=(12, 0))

        reset_btn = ttk.Button(self.login_frame, text='Reset Master Credentials', command=self.on_reset_credentials)
        reset_btn.pack(pady=(16, 0))

        self.login_frame.pack(expand=True, fill='both')

    def build_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ttk.Label(self.main_frame, text='CloudBase ERP Active', font=('Segoe UI', 20, 'bold'))
        title.pack(pady=(0, 10))

        desc = ttk.Label(
            self.main_frame,
            text='Session Authenticated.\nReady for Google Cloud Sync & Local Storage.',
            font=('Segoe UI', 9),
            justify='center',
            foreground='#16a34a'
        )
        desc.pack(pady=(0, 18))

        browser_btn = ttk.Button(self.main_frame, text='Open ERP (Google Sync Ready - localhost:8000)', command=self.open_erp_browser)
        browser_btn.pack(fill='x', pady=(0, 8))

        app_button = ttk.Button(self.main_frame, text='Open ERP in App Window', command=self.open_erp_html)
        app_button.pack(fill='x', pady=(0, 12))

        logout_button = ttk.Button(self.main_frame, text='Lock Session / Logout', command=self.on_logout)
        logout_button.pack(fill='x', pady=(15, 0))

        self.main_status_label = ttk.Label(self.main_frame, textvariable=self.status_var, font=('Segoe UI', 9), foreground='#16a34a')
        self.main_status_label.pack(pady=(16, 0))

    def open_erp_browser(self):
        import webbrowser
        webbrowser.open('http://localhost:8000/Mangment%202.html')
        self.set_status('Opened in browser on http://localhost:8000 (Google OAuth compatible).')

    def on_setup(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        confirm = self.confirm_var.get()

        if not username:
            self.status_var.set('Username cannot be empty.')
            return

        if len(password) < 4:
            self.status_var.set('Password must be at least 4 characters long.')
            return

        if password != confirm:
            self.status_var.set('Passwords do not match. Please re-enter.')
            return

        pwd_hash = hash_password(password)
        save_vault(username, pwd_hash)

        self.logged_in = True
        self.status_var.set('Master account created successfully!')
        self.show_main_frame()

    def on_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        vault = load_vault()

        if not vault:
            self.build_setup_frame()
            return

        expected_user = vault.get('username', '')
        expected_hash = vault.get('password_hash', '')

        if username.lower() == expected_user.lower() and hash_password(password) == expected_hash:
            self.logged_in = True
            self.status_var.set('Authentication successful. Session unlocked.')
            self.show_main_frame()
        else:
            self.logged_in = False
            self.status_var.set('Invalid username or master password. Access denied.')

    def on_reset_credentials(self):
        vault = load_vault()
        if vault:
            confirm = messagebox.askyesno(
                'Reset Master Credentials',
                'Are you sure you want to reset your master credentials?\nYou will be prompted to create new credentials.'
            )
            if not confirm:
                return

        if AUTH_FILE.exists():
            AUTH_FILE.unlink(missing_ok=True)

        self.username_var.set('')
        self.password_var.set('')
        self.confirm_var.set('')
        self.status_var.set('Credentials reset. Please create new master credentials.')
        self.build_setup_frame()

    def on_logout(self):
        self.logged_in = False
        self.password_var.set('')
        self.confirm_var.set('')
        self.status_var.set('Session locked.')
        self.show_login_frame()

    def set_status(self, message, success=True):
        self.status_var.set(message)
        if hasattr(self, 'main_status_label'):
            self.main_status_label.configure(foreground='#16a34a' if success else '#dc2626')

    def open_erp_html(self):
        if not self.logged_in:
            self.set_status('Login required before opening the ERP window.', success=False)
            return

        if not self.desktop_html.exists():
            self.set_status('Mangment 2.html not found.', success=False)
            return

        try:
            self.launch_erp_viewer(self.desktop_html)
            self.set_status('ERP page opened in a secure window.')
        except Exception as exc:
            self.set_status(f'Could not open ERP page: {exc}', success=False)

    def launch_erp_viewer(self, html_path: Path):
        if getattr(sys, 'frozen', False):
            webview.create_window('CloudBase ERP Page', html_path.absolute().as_uri(), width=1200, height=800, resizable=True)
            webview.start()
        else:
            helper_script = Path(__file__).resolve().parent / 'erp_viewer.py'
            if not helper_script.exists():
                raise FileNotFoundError('ERP viewer helper is missing: erp_viewer.py')

            subprocess.Popen(
                [sys.executable, str(helper_script), str(html_path)],
                cwd=str(helper_script.parent),
                close_fds=False,
            )

    def show_main_frame(self):
        self.login_frame.pack_forget()
        self.main_frame.pack(expand=True, fill='both')
        self.root.title('CloudBase ERP - Unlocked')

    def show_login_frame(self):
        self.main_frame.pack_forget()
        self.build_login_frame()
        self.root.title('CloudBase ERP Login')


def run_background_server():
    import http.server
    import socketserver
    directory = str(Path(__file__).resolve().parent)
    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(*args, directory=directory, **kwargs)
    try:
        with socketserver.TCPServer(("127.0.0.1", 8000), handler) as httpd:
            httpd.serve_forever()
    except Exception:
        pass


def main():
    import threading
    srv_thread = threading.Thread(target=run_background_server, daemon=True)
    srv_thread.start()

    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
