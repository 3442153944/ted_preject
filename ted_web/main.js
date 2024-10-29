const { app, BrowserWindow, Menu } = require('electron');  // 引入 Menu
const path = require('path');

require('electron-reload')(path.join(__dirname, 'dist'), {
    electron: path.join(__dirname, 'node_modules', '.bin', 'electron')
});

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),  // 使用 path.join
            contextIsolation: false,
            nodeIntegration: true,
        },
    });

    // 在开发环境中加载 Vite 开发服务器地址
    if (process.env.NODE_ENV === 'development') {
        win.loadURL('http://localhost:10000');
    } else {
        // 在生产环境中加载打包好的文件
        win.loadURL('http://localhost:10000'); // 这里可以改为实际的打包路径
    }

    // 设置自定义菜单
    const menu = Menu.buildFromTemplate([  // 正确使用 Menu
        {
            label: '文件',
            submenu: [
                {
                    label: '打开',
                    accelerator: 'CmdOrCtrl+O',
                    click: () => {
                        console.log('打开文件');
                        // 在这里可以加入打开文件的逻辑
                    },
                },
                {
                    label: '退出',
                    accelerator: 'CmdOrCtrl+Q',
                    click: () => {
                        app.quit();
                    },
                },
            ],
        },
        {
            label: '编辑',
            submenu: [
                { role: 'undo', label: '撤销' },
                { role: 'redo', label: '重做' },
                { type: 'separator' },
                { role: 'cut', label: '剪切' },
                { role: 'copy', label: '复制' },
                { role: 'paste', label: '粘贴' },
            ],
        },
        {
            label: '帮助',
            submenu: [
                {
                    label: '关于',
                    click: () => {
                        console.log('打开关于窗口');
                        // 这里可以实现显示“关于”对话框的逻辑
                    },
                },
            ],
        },
        {
            label:'窗口',
            submenu:[
                {
                    label:'最小化',
                    click:()=>{
                        win.minimize();
                    }
                },
                {
                    label:'最大化',
                    click:()=>{
                        win.maximize();
                    }
                },
                {
                    label:'关闭',
                    click:()=>{
                        win.close();
                    }
                }
            ]
        },{
            label:'页面',
            submenu:[
                {
                    label:'刷新',
                    click:()=>{
                        win.reload();
                    }
                }
            ]
        },
        {
            label:'返回',
            click:()=> {
                if (win.webContents.canGoBack()) {
                    win.webContents.goBack();
                }
            }
        },
        {
            label:'前进',
            click:()=> {
                if (win.webContents.canGoForward()) {
                    win.webContents.goForward();
                }
            }
        },
    ]);

    // 将自定义菜单应用到当前窗口
    Menu.setApplicationMenu(menu);  // 正确设置菜单
}

app.whenReady().then(createWindow).catch(err => console.error('Failed to create window:', err));

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
