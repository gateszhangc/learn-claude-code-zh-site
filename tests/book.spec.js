const { test, expect } = require("@playwright/test");

test("首页是中文 Learn Claude Code 阅读站", async ({ page }) => {
  await page.goto("/index.html");

  await expect(page.locator(".hero-copy h1")).toHaveText("Learn Claude Code：真正的 Agent Harness 工程");
  await expect(page.getByText("中文阅读站")).toBeVisible();
  await expect(page.getByText("把 shareAI-lab 的中文 README 整理成适合连续阅读的静态网页")).toBeVisible();
  await expect(page.getByRole("link", { name: "GitHub 原文" })).toHaveAttribute(
    "href",
    "https://github.com/shareAI-lab/learn-claude-code/blob/main/README-zh.md",
  );
});

test("目录覆盖 README 的主要中文章节", async ({ page }) => {
  await page.goto("/index.html");

  const tocLinks = page.locator(".toc-links a");
  await expect(tocLinks).toHaveCount(12);
  await expect(page.getByRole("link", { name: /Agency 来自模型/ })).toBeVisible();
  await expect(page.getByRole("link", { name: /全部章节/ })).toBeVisible();

  await page.getByRole("link", { name: /全部章节/ }).click();
  await expect(page.locator("#全部章节")).toBeInViewport();
});

test("正文保留代码块、表格和核心中文内容", async ({ page }) => {
  await page.goto("/index.html");

  await expect(page.getByText("Agency -- 感知、推理、行动的能力 -- 来自模型训练")).toBeVisible();
  await expect(page.locator(".code-block").first()).toContainText("Harness = Tools + Knowledge");
  await expect(page.locator("table").first()).toContainText("旧 12 章版本");
  await expect(page.locator("table").last()).toContainText("s20");
});

test("当前视口无横向溢出且目录可浏览", async ({ page }) => {
  await page.goto("/index.html");

  const hasOverflow = await page.evaluate(() => {
    return document.documentElement.scrollWidth > window.innerWidth + 1;
  });
  expect(hasOverflow).toBeFalsy();

  const toc = page.locator(".toc-links");
  await expect(toc).toBeVisible();
  const scrollWidth = await toc.evaluate((node) => node.scrollWidth);
  const clientWidth = await toc.evaluate((node) => node.clientWidth);
  expect(scrollWidth).toBeGreaterThanOrEqual(clientWidth);
});
