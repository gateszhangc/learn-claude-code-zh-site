const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  timeout: 30000,
  use: {
    baseURL: "http://127.0.0.1:4174",
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "desktop-chromium",
      use: {
        ...devices["Desktop Chrome"],
      },
    },
    {
      name: "mobile-chromium",
      use: {
        ...devices["Pixel 7"],
      },
    },
  ],
  webServer: {
    command: "python3 -m http.server 4174 -d /Users/a1-6/Desktop/code/book/situationalawareness",
    url: "http://127.0.0.1:4174/index.html",
    reuseExistingServer: true,
    timeout: 30000,
  },
});
