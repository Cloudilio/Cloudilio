import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Cloudilio runs `npm run build` on each publish and serves the dist folder it makes
export default defineConfig({
  plugins: [react()],
});
