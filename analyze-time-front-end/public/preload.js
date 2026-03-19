const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Example methods for future use
  // getVersion: () => process.version,
  // platform: process.platform,
  
  // Clipboard access (if needed in future)
  // readClipboard: () => ipcRenderer.invoke('read-clipboard'),
  // writeClipboard: (text) => ipcRenderer.invoke('write-clipboard', text),
  
  // File system access (if needed in future)
  // readFile: (filePath) => ipcRenderer.invoke('read-file', filePath),
  // writeFile: (filePath, data) => ipcRenderer.invoke('write-file', filePath, data),
  
  // App info
  getInfo: () => ({
    platform: process.platform,
    arch: process.arch,
    nodeVersion: process.versions.node,
    electronVersion: process.versions.electron,
    chromeVersion: process.versions.chrome,
  }),
});

// Remove all listeners when the window is closed
window.addEventListener('beforeunload', () => {
  ipcRenderer.removeAllListeners();
});

// Security: Prevent node integration in renderer
window.nodeRequire = undefined;
delete window.process;
delete window.Buffer;
delete window.global;
