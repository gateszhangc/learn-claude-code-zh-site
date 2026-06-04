const { test, expect } = require("@playwright/test");

async function expectNoHorizontalOverflow(page) {
  const hasOverflow = await page.evaluate(() => {
    return document.documentElement.scrollWidth > window.innerWidth + 1;
  });
  expect(hasOverflow).toBeFalsy();
}

test("首页是中文 Learn Claude Code 阅读站并指向章节页", async ({ page }) => {
  await page.goto("/index.html");

  await expect(page.locator(".hero-copy h1")).toHaveText("Learn Claude Code：真正的 Agent Harness 工程");
  await expect(page.getByText("中文阅读站")).toBeVisible();
  await expect(page.getByRole("link", { name: "从 s01 开始" })).toHaveAttribute("href", "/s01_agent_loop/");
  await expect(page.getByRole("link", { name: "下载 EPUB" })).toHaveAttribute(
    "href",
    "/ebooks/learn-claude-code-zh.epub",
  );
  await expect(page.getByRole("link", { name: "电子书" })).toHaveAttribute(
    "href",
    "/ebooks/learn-claude-code-zh.epub",
  );
  await expect(page.getByRole("link", { name: /s20 Comprehensive/ })).toHaveAttribute("href", "/s20_comprehensive/");
});

test("章节页不是首页 fallback，保留正文、目录、代码和图示", async ({ page }) => {
  await page.goto("/s01_agent_loop/");

  await expect(page.locator(".chapter-masthead h1")).toHaveText("s01: Agent Loop — 一个循环就够了");
  await expect(page.locator(".course-links a.is-current")).toContainText("s01");
  await expect(page.locator(".chapter-toc")).toContainText("问题");
  await expect(page.locator(".media-figure img")).toHaveAttribute(
    "src",
    "https://raw.githubusercontent.com/shareAI-lab/learn-claude-code/main/s01_agent_loop/images/agent-loop.svg",
  );
  await expect(page.locator(".code-block").first()).toContainText("messages =");
  await expect(page.locator(".chapter-masthead").getByRole("link", { name: /下一章/ })).toHaveAttribute("href", "/s02_tool_use/");
  await expect(page.getByRole("link", { name: "电子书" })).toHaveAttribute(
    "href",
    "/ebooks/learn-claude-code-zh.epub",
  );
});

test("EPUB 电子书文件可下载", async ({ request }) => {
  const response = await request.get("/ebooks/learn-claude-code-zh.epub");
  expect(response.ok()).toBeTruthy();
  const body = await response.body();
  expect(body.length).toBeGreaterThan(100000);
  expect(body.subarray(0, 2).toString("utf8")).toBe("PK");
});

test("章节阅读界面在桌面和移动端都没有横向溢出", async ({ page, isMobile }) => {
  await page.goto("/s01_agent_loop/");

  await expectNoHorizontalOverflow(page);
  await expect(page.locator(".chapter-article")).toBeVisible();

  if (isMobile) {
    await expect(page.locator(".course-links")).toBeVisible();
    await expect(page.locator(".chapter-toc")).toBeHidden();
  } else {
    await expect(page.locator(".chapter-toc")).toBeVisible();
    await expect(page.locator(".course-rail")).toBeVisible();
  }
});

test("末章提供向前导航并显示完整 harness 内容", async ({ page }) => {
  await page.goto("/s20_comprehensive/");

  await expect(page.locator(".chapter-masthead h1")).toContainText("s20");
  await expect(page.locator(".course-links a.is-current")).toContainText("s20");
  await expect(page.locator(".chapter-masthead").getByRole("link", { name: /上一章/ })).toHaveAttribute("href", "/s19_mcp_plugin/");
  await expect(page.locator(".chapter-article")).toContainText("机制很多");
});
