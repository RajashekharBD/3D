import { test, expect } from "@playwright/test";

test.describe("Upload Page", () => {
  test("loads upload page", async ({ page }) => {
    await page.goto("/upload");
    await expect(page).toHaveURL(/\/upload/);
  });

  test("displays upload area", async ({ page }) => {
    await page.goto("/upload");
    const uploadArea = page.locator("input[type='file'], [class*='upload'], [class*='drop']").first();
    await expect(uploadArea).toBeVisible({ timeout: 10000 });
  });

  test("file input accepts images", async ({ page }) => {
    await page.goto("/upload");
    const fileInput = page.locator("input[type='file']").first();
    await expect(fileInput).toHaveAttribute("accept", /image/);
  });
});
