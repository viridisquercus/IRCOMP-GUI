/*************************************************************************
 * Name: Lukas (Viridis) Dubsik
 * Login: xdubsil00
 * Project: IRCOMP
 * School-Project: ITU-1
 *************************************************************************/
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
});
