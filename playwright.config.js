const { defineConfig, devices } = require("@playwright/test");

const siteRoot = __dirname;

module.exports = defineConfig({
  testDir: "./tests",
  timeout: 30000,
  use: {
    baseURL: "http://127.0.0.1:4176",
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
    command: `python3 -m http.server 4176 -d ${JSON.stringify(siteRoot)}`,
    url: "http://127.0.0.1:4176/index.html",
    reuseExistingServer: true,
    timeout: 30000,
  },
});
