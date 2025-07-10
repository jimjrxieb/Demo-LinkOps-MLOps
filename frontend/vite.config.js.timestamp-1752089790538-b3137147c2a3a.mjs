// vite.config.js
import { defineConfig } from 'file:///home/jimjrxieb/shadow-link-industries/LinkOps-MLOps/frontend/node_modules/vite/dist/node/index.js';
import vue from 'file:///home/jimjrxieb/shadow-link-industries/LinkOps-MLOps/frontend/node_modules/@vitejs/plugin-vue/dist/index.mjs';
import { resolve } from 'path';
var __vite_injected_original_dirname =
  '/home/jimjrxieb/shadow-link-industries/LinkOps-MLOps/frontend';
var vite_config_default = defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__vite_injected_original_dirname, './'),
      '~': resolve(__vite_injected_original_dirname, './'),
    },
  },
  server: {
    port: 3e3,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router'],
          utils: ['axios'],
        },
      },
    },
  },
  css: {
    postcss: './postcss.config.js',
  },
});
export { vite_config_default as default };
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvaG9tZS9qaW1qcnhpZWIvc2hhZG93LWxpbmstaW5kdXN0cmllcy9MaW5rT3BzLU1MT3BzL2Zyb250ZW5kXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvaG9tZS9qaW1qcnhpZWIvc2hhZG93LWxpbmstaW5kdXN0cmllcy9MaW5rT3BzLU1MT3BzL2Zyb250ZW5kL3ZpdGUuY29uZmlnLmpzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9ob21lL2ppbWpyeGllYi9zaGFkb3ctbGluay1pbmR1c3RyaWVzL0xpbmtPcHMtTUxPcHMvZnJvbnRlbmQvdml0ZS5jb25maWcuanNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJ1xuaW1wb3J0IHZ1ZSBmcm9tICdAdml0ZWpzL3BsdWdpbi12dWUnXG5pbXBvcnQgeyByZXNvbHZlIH0gZnJvbSAncGF0aCdcblxuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKHtcbiAgcGx1Z2luczogW3Z1ZSgpXSxcbiAgcmVzb2x2ZToge1xuICAgIGFsaWFzOiB7XG4gICAgICAnQCc6IHJlc29sdmUoX19kaXJuYW1lLCAnLi8nKSxcbiAgICAgICd+JzogcmVzb2x2ZShfX2Rpcm5hbWUsICcuLycpXG4gICAgfVxuICB9LFxuICBzZXJ2ZXI6IHtcbiAgICBwb3J0OiAzMDAwLFxuICAgIGhvc3Q6IHRydWUsXG4gICAgcHJveHk6IHtcbiAgICAgICcvYXBpJzoge1xuICAgICAgICB0YXJnZXQ6ICdodHRwOi8vbG9jYWxob3N0OjgwMDAnLFxuICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgICAgIHJld3JpdGU6IChwYXRoKSA9PiBwYXRoLnJlcGxhY2UoL15cXC9hcGkvLCAnJylcbiAgICAgIH1cbiAgICB9XG4gIH0sXG4gIGJ1aWxkOiB7XG4gICAgb3V0RGlyOiAnZGlzdCcsXG4gICAgc291cmNlbWFwOiB0cnVlLFxuICAgIHJvbGx1cE9wdGlvbnM6IHtcbiAgICAgIG91dHB1dDoge1xuICAgICAgICBtYW51YWxDaHVua3M6IHtcbiAgICAgICAgICB2ZW5kb3I6IFsndnVlJywgJ3Z1ZS1yb3V0ZXInXSxcbiAgICAgICAgICB1dGlsczogWydheGlvcyddfVxuICAgICAgfVxuICAgIH1cbiAgfSxcbiAgY3NzOiB7XG4gICAgcG9zdGNzczogJy4vcG9zdGNzcy5jb25maWcuanMnXG4gIH1cbn0pOyJdLAogICJtYXBwaW5ncyI6ICI7QUFBeVcsU0FBUyxvQkFBb0I7QUFDdFksT0FBTyxTQUFTO0FBQ2hCLFNBQVMsZUFBZTtBQUZ4QixJQUFNLG1DQUFtQztBQUl6QyxJQUFPLHNCQUFRLGFBQWE7QUFBQSxFQUMxQixTQUFTLENBQUMsSUFBSSxDQUFDO0FBQUEsRUFDZixTQUFTO0FBQUEsSUFDUCxPQUFPO0FBQUEsTUFDTCxLQUFLLFFBQVEsa0NBQVcsSUFBSTtBQUFBLE1BQzVCLEtBQUssUUFBUSxrQ0FBVyxJQUFJO0FBQUEsSUFDOUI7QUFBQSxFQUNGO0FBQUEsRUFDQSxRQUFRO0FBQUEsSUFDTixNQUFNO0FBQUEsSUFDTixNQUFNO0FBQUEsSUFDTixPQUFPO0FBQUEsTUFDTCxRQUFRO0FBQUEsUUFDTixRQUFRO0FBQUEsUUFDUixjQUFjO0FBQUEsUUFDZCxTQUFTLENBQUMsU0FBUyxLQUFLLFFBQVEsVUFBVSxFQUFFO0FBQUEsTUFDOUM7QUFBQSxJQUNGO0FBQUEsRUFDRjtBQUFBLEVBQ0EsT0FBTztBQUFBLElBQ0wsUUFBUTtBQUFBLElBQ1IsV0FBVztBQUFBLElBQ1gsZUFBZTtBQUFBLE1BQ2IsUUFBUTtBQUFBLFFBQ04sY0FBYztBQUFBLFVBQ1osUUFBUSxDQUFDLE9BQU8sWUFBWTtBQUFBLFVBQzVCLE9BQU8sQ0FBQyxPQUFPO0FBQUEsUUFBQztBQUFBLE1BQ3BCO0FBQUEsSUFDRjtBQUFBLEVBQ0Y7QUFBQSxFQUNBLEtBQUs7QUFBQSxJQUNILFNBQVM7QUFBQSxFQUNYO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
