import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8529,
    proxy: {
      '/api': {
        target: 'http://localhost:9529',
        changeOrigin: true
      }
    }
  }
})