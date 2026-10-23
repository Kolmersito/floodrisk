import { defineConfig } from 'vite';

export default defineConfig({
  // Explicit baseline for the existing Vite 7 app, not a Safari guarantee.
  build: { target: ['chrome107', 'edge107', 'firefox104', 'safari16'] },
  server: { proxy: { '/api': 'http://127.0.0.1:8000' } },
  preview: { proxy: { '/api': 'http://127.0.0.1:8000' } },
});
