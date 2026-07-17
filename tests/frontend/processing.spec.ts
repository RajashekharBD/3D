import { test, expect } from "@playwright/test";

test.describe("Processing Page", () => {
  test("loads processing page with job ID", async ({ page }) => {
    await page.goto("/processing/test-job-123");
    await expect(page).toHaveURL(/\/processing\/test-job-123/);
  });

  test("displays progress tracker component", async ({ page }) => {
    await page.goto("/processing/test-job-123");
    const progressTracker = page.locator("[class*='progress'], [class*='Progress'], [role='progressbar']").first();
    await expect(progressTracker).toBeVisible({ timeout: 10000 });
  });
});
