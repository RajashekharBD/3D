import { test, expect } from "@playwright/test";

test.describe("Navigation", () => {
  test("navbar links work", async ({ page }) => {
    await page.goto("/");
    
    const uploadLink = page.locator('a[href="/upload"]').first();
    if (await uploadLink.isVisible()) {
      await uploadLink.click();
      await expect(page).toHaveURL(/\/upload/);
    }
  });

  test("home link returns to landing", async ({ page }) => {
    await page.goto("/upload");
    const homeLink = page.locator('a[href="/"]').first();
    if (await homeLink.isVisible()) {
      await homeLink.click();
      await expect(page).toHaveURL("/");
    }
  });
});

test.describe("Viewer Redirect Page", () => {
  test("viewer page loads or redirects", async ({ page }) => {
    await page.goto("/viewer");
    const url = page.url();
    expect(url).toMatch(/\/(viewer|upload)/);
  });
});

test.describe("Download Redirect Page", () => {
  test("download page loads or redirects", async ({ page }) => {
    await page.goto("/download");
    const url = page.url();
    expect(url).toMatch(/\/(download|upload)/);
  });
});

test.describe("Responsive Design", () => {
  test("landing page works on mobile viewport", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");
    const hero = page.locator("h1").first();
    await expect(hero).toBeVisible();
  });

  test("upload page works on mobile viewport", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/upload");
    await expect(page).toHaveURL(/\/upload/);
  });
});
