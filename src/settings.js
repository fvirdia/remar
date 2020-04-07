function showSettings(message) {
    ipcRenderer.send('open-settings', message);
}
