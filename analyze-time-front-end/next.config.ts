import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable static export for Electron compatibility
  output: 'export',
  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },
  // Set trailing slash for consistency
  trailingSlash: true,
  // Configure base path if needed for Electron
  // basePath: './',
};

export default nextConfig;
