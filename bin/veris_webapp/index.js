const electron = require('electron');
const app = (process.type === 'renderer') ? electron.remote.app : electron.app;
const BrowserWindow = (process.type === 'renderer') ? electron.remote.BrowserWindow : electron.BrowserWindow;
const path = require('path');
const url = require('url');

const isDev = (process.mainModule.filename.indexOf('app.asar') === -1);

let win;

function createWindow() {
  win = new BrowserWindow({show: false});
  win.maximize();
  win.show();

  if (isDev) {
    win.openDevTools()
  }

  win.loadURL(url.format({
    pathname: path.join(__dirname, 'build', 'index.html'),
    protocol: 'file',
    slashes: true
  }));

  win.on('closed', () => {
    win = null;
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platformat !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (win === null) {
    createWindow();
  }
});