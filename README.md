# CloudBase ERP Desktop App

This is a lightweight Python desktop wrapper for your `Mangment 2.html` file. It loads the HTML file from your Desktop with integrated Master Security Authentication.

## Setup

1. Make sure `Mangment 2.html` is located on your Desktop.
2. Open a terminal in `c:\Users\Muham\Desktop\Mangment2-DesktopApp`.
3. Run:
   ```powershell
   py -3 -m pip install -r requirements.txt
   py -3 app.py
   ```

## Security & Access

The ERP features an encrypted Master Security Gate. On initial launch, set your private administrator credentials. Only authorized administrators with the master password can access or mutate institutional records.

## Notes

- The app loads the existing `Mangment 2.html` from your Desktop.
- If you move or rename the HTML file, update the path in `app.py` or move the file back.

## Building a single-file Windows executable

To create a portable `.exe` that runs on machines without Python:

1. Ensure `Mangment 2.html` is present in this project folder (next to `app.py`).
2. Install build dependencies and PyInstaller:

```powershell
py -3 -m pip install -r requirements.txt
```

3. Run the included build script:

```powershell
.\build.bat
```

The produced executable will be at `dist\MTECH_ERP.exe`. Note that some target machines may require the Microsoft WebView2 runtime for the embedded browser to work; if the web view fails, install WebView2 from Microsoft.
