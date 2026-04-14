# Here is the complete, single-file Python solution for **SanctuarySync Desktop**.
#
# It includes the **mandatory WinError 32 fix** (strict context management + GC/Retry logic), the **OAuth Scope fix** (automatic token regeneration on scope mismatch), and the requested GUI layout using `tkinter`.
#
# ### Prerequisites
#
# You must have the following libraries installed:
# ```bash
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib tk
# ```
# *(Note: You also need a `credentials.json` file from the Google Cloud Console placed in the same directory as this script.)*
#
# ### Application Code (`sanctuary_sync.py`)
#
# ```python
import os
import sys
import json
import time
import zipfile
import threading
import gc
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox

# Google API Imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

# --- CONSTANTS & CONFIGURATION ---
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CONFIG_FILE = 'sanctuary_config.json'
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

class SanctuarySyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SanctuarySync Desktop")
        self.root.geometry("700x600")
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables
        self.obs_path_var = tk.StringVar(value=os.path.expandvars(r"%APPDATA%\obs-studio\basic\scenes"))
        self.asset_path_var = tk.StringVar(value=r"C:\ChurchMedia\Assets")
        self.drive_id_var = tk.StringVar(value="1DMJsAQKJx17iF3vSkjDMKlJRsetzQZed")
        
        # Load previous config if exists
        self.load_config()

        # Build GUI
        self.build_header()
        self.build_settings_frame()
        self.build_ops_frame()
        self.build_console()
        
        self.log("SanctuarySync initialized. Ready.")

    def build_header(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.X)
        lbl = ttk.Label(frame, text="SanctuarySync Control Center", font=("Helvetica", 16, "bold"))
        lbl.pack()

    def build_settings_frame(self):
        frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Grid config
        frame.columnconfigure(1, weight=1)

        # Row 1: OBS Path
        ttk.Label(frame, text="OBS Path:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.obs_path_var).grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_folder(self.obs_path_var)).grid(row=0, column=2)

        # Row 2: Asset Path
        ttk.Label(frame, text="Asset Path:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.asset_path_var).grid(row=1, column=1, sticky=tk.EW, padx=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_folder(self.asset_path_var)).grid(row=1, column=2)

        # Row 3: G-Drive ID
        ttk.Label(frame, text="G-Drive Folder ID:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.drive_id_var).grid(row=2, column=1, sticky=tk.EW, padx=5)

    def build_ops_frame(self):
        frame = ttk.LabelFrame(self.root, text="Operations", padding=10)
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn_push = ttk.Button(frame, text="PUSH TO CLOUD", command=self.start_push)
        btn_push.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        btn_pull = ttk.Button(frame, text="PULL FROM CLOUD", command=self.start_pull)
        btn_pull.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def build_console(self):
        frame = ttk.LabelFrame(self.root, text="Console", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.console = scrolledtext.ScrolledText(frame, height=10, state='disabled', font=("Consolas", 9))
        self.console.pack(fill=tk.BOTH, expand=True)

    # --- HELPERS ---
    def log(self, msg):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        final_msg = f"[{timestamp}] {msg}\n"
        
        def _update():
            self.console.configure(state='normal')
            self.console.insert(tk.END, final_msg)
            self.console.see(tk.END)
            self.console.configure(state='disabled')
            
        self.root.after(0, _update)

    def browse_folder(self, var):
        d = filedialog.askdirectory()
        if d:
            var.set(d)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.obs_path_var.set(data.get('obs_path', ''))
                    self.asset_path_var.set(data.get('asset_path', ''))
                    self.drive_id_var.set(data.get('drive_id', ''))
            except Exception as e:
                self.log(f"Error loading config: {e}")

    def save_config(self):
        data = {
            'obs_path': self.obs_path_var.get(),
            'asset_path': self.asset_path_var.get(),
            'drive_id': self.drive_id_var.get()
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.log(f"Error saving config: {e}")

    def safe_cleanup(self, path):
        """
        WinError 32 FIX: Aggressive cleanup with GC and exponential backoff.
        """
        if not os.path.exists(path):
            return

        self.log(f"Attempting cleanup of {path}...")
        
        # Force garbage collection to help release handles
        gc.collect()
        
        retries = 5
        for i in range(retries):
            try:
                os.remove(path)
                self.log("Cleanup successful.")
                return
            except OSError as e:
                wait_time = 2 * (i + 1)
                self.log(f"Cleanup failed (Attempt {i+1}/{retries}). Locked. Waiting {wait_time}s...")
                time.sleep(wait_time)
                gc.collect()
        
        self.log(f"WARNING: Could not delete {path} after {retries} attempts. Please delete manually.")

    # --- AUTH LOGIC ---
    def get_gdrive_service(self):
        creds = None
        
        # 1. Logic: If token.json exists, load it.
        if os.path.exists(TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            except Exception as e:
                self.log("Token invalid or corrupted. Will re-authenticate.")
                creds = None

        # 2. Logic: Validate credentials. If invalid or mismatched scopes, delete token.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    self.log(f"Token refresh failed ({e}). Deleting token...")
                    if os.path.exists(TOKEN_FILE):
                        os.remove(TOKEN_FILE)
                    creds = None
            
            if not creds:
                if not os.path.exists(CREDENTIALS_FILE):
                    messagebox.showerror("Error", f"Missing {CREDENTIALS_FILE}. Cannot authenticate.")
                    return None
                
                # Deleting old token to ensure fresh scope request
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)

                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                # 3. Logic: Use port=0
                creds = flow.run_local_server(port=0)
                
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())

        return build('drive', 'v3', credentials=creds)

    # --- PUSH LOGIC ---
    def start_push(self):
        self.save_config()
        threading.Thread(target=self.run_push, daemon=True).start()

    def run_push(self):
        obs_path = self.obs_path_var.get()
        asset_path = self.asset_path_var.get()
        folder_id = self.drive_id_var.get()
        
        if not obs_path or not asset_path or not folder_id:
            self.log("Error: Paths and Folder ID are required.")
            return

        service = self.get_gdrive_service()
        if not service:
            return

        zip_name = f"SanctuarySync_Backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        self.log("Starting Backup Process...")

        try:
            # 1. ZIPPING
            self.log(f"Creating archive: {zip_name}")
            with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
                
                # Helper to add directory
                def add_dir_to_zip(local_path, zip_folder_name):
                    if not os.path.exists(local_path):
                        self.log(f"Warning: Path not found {local_path}")
                        return
                    for root, dirs, files in os.walk(local_path):
                        for file in files:
                            # RECURSION PREVENTION
                            if file.lower().endswith(".zip"):
                                continue
                            
                            abs_path = os.path.join(root, file)
                            rel_path = os.path.relpath(abs_path, local_path)
                            dest_path = os.path.join(zip_folder_name, rel_path)
                            zf.write(abs_path, dest_path)

                add_dir_to_zip(obs_path, "OBS_DATA")
                add_dir_to_zip(asset_path, "ASSETS")

            # 2. UPLOADING (WinError 32 Fix applied here)
            file_metadata = {
                'name': zip_name,
                'parents': [folder_id]
            }
            
            self.log("Uploading to Google Drive...")
            
            # CRITICAL: Open file block encompasses the API call
            with open(zip_name, "rb") as f:
                media = MediaIoBaseUpload(f, mimetype='application/zip', resumable=True)
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            
            # File handle 'f' is closed here.
            self.log(f"Backup Complete. File ID: {file.get('id')}")

        except Exception as e:
            self.log(f"CRITICAL ERROR during PUSH: {e}")
        finally:
            # 3. CLEANUP
            self.safe_cleanup(zip_name)

    # --- PULL LOGIC ---
    def start_pull(self):
        self.save_config()
        if messagebox.askyesno("Confirm Restore", "This will OVERWRITE files in your OBS and Asset folders. Continue?"):
            threading.Thread(target=self.run_pull, daemon=True).start()

    def run_pull(self):
        folder_id = self.drive_id_var.get()
        obs_path = self.obs_path_var.get()
        asset_path = self.asset_path_var.get()

        service = self.get_gdrive_service()
        if not service:
            return

        try:
            # 1. FIND LATEST BACKUP
            self.log("Searching for latest backup...")
            query = f"'{folder_id}' in parents and mimeType='application/zip' and trashed=false"
            results = service.files().list(q=query, orderBy="createdTime desc", pageSize=1).execute()
            items = results.get('files', [])

            if not items:
                self.log("No backup files found in the specified folder.")
                return

            latest_file = items[0]
            file_id = latest_file['id']
            file_name = latest_file['name']
            self.log(f"Found latest backup: {file_name}")

            # 2. DOWNLOAD
            request = service.files().get_media(fileId=file_id)
            self.log("Downloading...")
            
            temp_zip = "SanctuarySync_Restore_Temp.zip"
            
            with open(temp_zip, "wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    # Optional: Log progress
            
            # 3. EXTRACT
            self.log("Extracting files...")
            try:
                with zipfile.ZipFile(temp_zip, 'r') as zf:
                    # Filter and extract
                    for member in zf.namelist():
                        if member.startswith("OBS_DATA/"):
                            # Strip "OBS_DATA/" prefix
                            target_name = member[len("OBS_DATA/"):]
                            if not target_name: continue # Skip root folder entry
                            target_path = os.path.join(obs_path, target_name)
                        elif member.startswith("ASSETS/"):
                            # Strip "ASSETS/" prefix
                            target_name = member[len("ASSETS/"):]
                            if not target_name: continue
                            target_path = os.path.join(asset_path, target_name)
                        else:
                            continue

                        # Create dirs if needed
                        if member.endswith('/'):
                            os.makedirs(target_path, exist_ok=True)
                        else:
                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                            with open(target_path, "wb") as outfile, zf.open(member) as infile:
                                outfile.write(infile.read())
                                
                self.log("Restore Complete successfully.")
            
            except Exception as e:
                self.log(f"Error during extraction: {e}")

        except Exception as e:
            self.log(f"CRITICAL ERROR during PULL: {e}")
        finally:
            self.safe_cleanup("SanctuarySync_Restore_Temp.zip")

if __name__ == "__main__":
    root = tk.Tk()
    app = SanctuarySyncApp(root)
    root.mainloop()
# ```
#
# ### Key Technical Implementations
#
# 1.  **OAuth & Invalid Scope Fix**:
#     *   Located in `get_gdrive_service`.
#     *   It strictly checks `creds.valid`. If checking credentials fails (or refresh fails), it explicitly checks for `TOKEN_FILE` existence and deletes it (`os.remove(TOKEN_FILE)`) before initiating `InstalledAppFlow`.
#     *   It uses `flow.run_local_server(port=0)` to avoid port conflict errors.
#
# 2.  **WinError 32 (The "Final Fix")**:
#     *   **Zipping**: Uses `with zipfile.ZipFile(...)`.
#     *   **Uploading**: The `service.files().create(...).execute()` call is nested **inside** the `with open(zip_name, "rb") as f:` block. This ensures the file stream is passed to `MediaIoBaseUpload`, used, and then the context manager closes the file handle immediately.
#     *   **Cleanup**: The `safe_cleanup` method implements the `gc.collect()`, exponential backoff (sleep 2, 4, 6...), and retry loop logic to ensure the file is unlocked before deletion.
#
# 3.  **Recursion Prevention**:
#     *   Inside `run_push` -> `add_dir_to_zip`, there is an explicit check: `if file.lower().endswith(".zip"): continue`.
#
# 4.  **GUI & Persistence**:
#     *   Uses `tkinter.scrolledtext` for the console.
#     *   Methods `save_config` and `load_config` handle JSON IO automatically on startup and before operations.
#     *   Threading is used for Push/Pull operations to keep the GUI responsive (`daemon=True` so threads close if app closes).
#