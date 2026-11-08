const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');

function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 940,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false
    }
  });

  const desktopPath = app.getPath('desktop');
  const htmlFilePath = path.join(desktopPath, 'Mangment 2.html');

  if (!fs.existsSync(htmlFilePath)) {
    const fallbackHTML = `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>File Not Found</title></head><body style="font-family:sans-serif; padding:24px;"><h1>Missing HTML file</h1><p>Please ensure <strong>Mangment 2.html</strong> exists on your Desktop.</p></body></html>`;
    win.loadURL(`data:text/html;charset=UTF-8,${encodeURIComponent(fallbackHTML)}`);
    return;
  }

  win.loadFile(htmlFilePath);
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
