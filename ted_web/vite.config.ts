import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'
import VueSetupExtension from 'vite-plugin-vue-setup-extend'
import mkcert from 'vite-plugin-mkcert'
import electron from 'vite-plugin-electron';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),
    VueDevTools(),
    VueSetupExtension(),
    //mkcert()
    /*electron({
      main: {
        entry: 'electron/main.js', // 指向Electron的主进程入口文件
      },
      preload: {
        input: 'electron/preload.js', // 指向预加载脚本
      },
      // 其他Electron相关配置
    }),*/
  ],
  server: {
    port:10000,
    host:true,
  }
})
