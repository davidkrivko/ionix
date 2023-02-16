import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  build: {
    outDir: '../../apps/owner/',
    watch: {},
    rollupOptions: {
      output: {
        entryFileNames: "[name].js",
        assetFileNames: '[name][extname]',
        chunkFileNames: '[name].js',
      }
    }
  }
})
