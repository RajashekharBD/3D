import { test, expect } from "@playwright/test";

test.describe("Landing Page", () => {
  test("loads successfully", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(/SingleImage3D|3D/i);
  });

  test("displays hero section", async ({ page }) => {
    await page.goto("/");
    const hero = page.locator("h1").first();
    await expect(hero).toBeVisible();
  });

  test("has upload navigation link", async ({ page }) => {
    await page.goto("/");
    const uploadLink = page.locator('a[href="/upload"]').first();
    await expect(uploadLink).toBeVisible();
  });

  test("has feature cards", async ({ page }) => {
    await page.goto("/");
    const cards = page.locator("[class*='card'], [class*='Card']");
    const count = await cards.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });
});
