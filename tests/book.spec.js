const { test, expect } = require("@playwright/test");

test("首页展示中文导读和官方来源入口", async ({ page }) => {
  await page.goto("/index.html");
  await expect(page.getByRole("heading", { name: "埃隆之书" })).toBeVisible();
  await expect(page.getByText("中文阅读地图")).toBeVisible();
  await expect(page.getByRole("link", { name: "免费 PDF", exact: true })).toHaveAttribute(
    "href",
    "https://www.elonmuskbook.org/free-book-of-elon-musk",
  );
  await expect(page.getByRole("link", { name: "官方在线版" })).toBeVisible();
});

test("目录覆盖六个阅读部分并能跳转", async ({ page }) => {
  await page.goto("/index.html");
  await expect(page.locator(".toc-links a")).toHaveCount(6);
  await page.getByRole("link", { name: /第三部分：创建公司/ }).click();
  await expect(page.locator("#part-4")).toBeInViewport();
});

test("章节阅读节点完整呈现", async ({ page }) => {
  await page.goto("/index.html");
  await expect(page.locator(".chapter-card")).toHaveCount(22);
  await expect(page.getByRole("heading", { name: "像物理学家一样思考" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "建造 SpaceX" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "69 条 Musk 核心方法" })).toBeVisible();
});

test("当前视口无横向溢出", async ({ page }) => {
  await page.goto("/index.html");
  const hasOverflow = await page.evaluate(() => {
    return document.documentElement.scrollWidth > window.innerWidth + 1;
  });
  expect(hasOverflow).toBeFalsy();
});
