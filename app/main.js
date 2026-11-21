// قلمي: the app's page and recordings are served from inside the program, so it works without internet.
const { app, BrowserWindow, protocol, net, Menu, shell } = require('electron');
const path = require('path');
const { pathToFileURL } = require('url');

protocol.registerSchemesAsPrivileged([{ scheme: 'qalami', privileges: { standard: true, secure: true, supportFetchAPI: true } }]);
if (!app.requestSingleInstanceLock()) app.quit();

let win;
function open() {
  win = new BrowserWindow({
    width: 1100, height: 820, minWidth: 380, minHeight: 600, title: 'قلمي', backgroundColor: '#DDEFF7',
    icon: path.join(__dirname, 'icon.ico'), autoHideMenuBar: true,
    webPreferences: { contextIsolation: true, sandbox: true, autoplayPolicy: 'no-user-gesture-required', spellcheck: false }
  });
  win.loadURL('qalami://app/index.html');
  // links to other sites open in the normal browser, never inside the app
  win.webContents.setWindowOpenHandler(({ url }) => { shell.openExternal(url); return { action: 'deny' }; });
  win.webContents.on('will-navigate', (e, url) => { if (!url.startsWith('qalami://')) { e.preventDefault(); shell.openExternal(url); } });
}

app.whenReady().then(() => {
  const root = path.join(__dirname, 'www');
  protocol.handle('qalami', req => {
    const p = path.normalize(path.join(root, decodeURIComponent(new URL(req.url).pathname)));
    if (!p.startsWith(root)) return new Response('', { status: 403 });
    const type = { '.html': 'text/html; charset=utf-8', '.json': 'application/json; charset=utf-8', '.css': 'text/css; charset=utf-8', '.woff2': 'font/woff2' }[path.extname(p)];
    return net.fetch(pathToFileURL(p).toString()).then(r => type ? new Response(r.body, { status: r.status, headers: { 'content-type': type } }) : r);
  });
  Menu.setApplicationMenu(null);
  open();
});
app.on('second-instance', () => { if (win) { if (win.isMinimized()) win.restore(); win.focus(); } });
app.on('window-all-closed', () => app.quit());
