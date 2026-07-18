import { test, expect } from "@playwright/test";

test.describe("Results Page", () => {
  test("loads results page with job ID", async ({ page }) => {
    await page.goto("/results/test-job-123");
    await expect(page).toHaveURL(/\/results\/test-job-123/);
  });

  test("displays 3D viewer area", async ({ page }) => {
    await page.goto("/results/test-job-123");
    const canvas = page.locator("canvas").first();
    await expect(canvas).toBeVisible({ timeout: 15000 });
  });

  test("displays download panel", async ({ page }) => {
    await page.goto("/results/test-job-123");
    const downloadSection = page.locator("[class*='download'], [class*='Download']").first();
    await expect(downloadSection).toBeVisible({ timeout: 10000 });
  });
});
