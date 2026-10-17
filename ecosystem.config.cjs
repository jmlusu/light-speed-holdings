module.exports = {
  apps: [
    {
      name: "vite-dev",
      script: "C:\\Users\\jmlus\\light-speed-holdings\\node_modules\\.bin\\vite.exe",
      args: "dev",
      cwd: ".",
      port: 1441,
      env: {
        VITE: "true",
      },
      env_production: {
        VITE: "true",
      },
    },
    {
      name: "vite-preview",
      script: "C:\\Users\\jmlus\\light-speed-holdings\\node_modules\\.bin\\vite.exe",
      args: "preview",
      cwd: ".",
      port: 1440,
      env: {
        VITE: "true",
      },
      env_production: {
        VITE: "true",
      },
    },
  ],
};
