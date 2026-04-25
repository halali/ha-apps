import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://tauri.app/v1/api/config
const host = process.env.TAURI_DEV_HOST;

export default defineConfig(async () => ({
  plugins: [react()],

  // Tauri expects a fixed port and bails if it can't claim it.
  clearScreen: false,
  server: {
    port: 1420,
    strictPort: true,
    host: host || false,
    hmr: host
      ? { protocol: "ws", host, port: 1421 }
      : undefined,
    watch: {
      // Don't watch the Rust side from the JS dev server.
      ignored: ["**/src-tauri/**"],
    },
  },
}));
