import basicSsl from "@vitejs/plugin-basic-ssl";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [basicSsl()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    proxy: {
      "/token": "http://127.0.0.1:8787"
    }
  },
  test: {
    environment: "jsdom"
  }
});
