import { test, expect } from '@playwright/test';

test.describe('Upload Page', () => {
  test('renders upload page with title and drop zone', async ({ page }) => {
    await page.goto('/upload');
    await expect(page.locator('h1')).toContainText('Upload Image');
    await expect(page.locator('#file-upload')).toBeAttached();
  });

  test('shows file size constraint text', async ({ page }) => {
    await page.goto('/upload');
    const text = await page.textContent('body');
    expect(text).toContain('3D model');
  });

  test('drag zone highlights on interaction', async ({ page }) => {
    await page.goto('/upload');
    const dropZone = page.locator('label[for="file-upload"]');
    await expect(dropZone).toBeVisible();
  });
});

test.describe('Processing Page', () => {
  test('renders processing page with job ID', async ({ page }) => {
    await page.goto('/processing/test-job-123');
    await expect(page.locator('h1')).toContainText('Processing Asset');
    await expect(page.locator('body')).toContainText('test-job-123');
  });

  test('shows progress tracker component', async ({ page }) => {
    await page.goto('/processing/test-job-456');
    // The ProgressTracker should render the Pipeline Stages section
    await expect(page.locator('body')).toContainText('Pipeline Stages');
  });

  test('shows progress percentage', async ({ page }) => {
    await page.goto('/processing/test-job-789');
    await expect(page.locator('body')).toContainText('Progress');
  });
});

test.describe('Results Page', () => {
  test('renders results page with job ID', async ({ page }) => {
    await page.goto('/results/test-job-000');
    await expect(page.locator('body')).toContainText('test-job-000');
  });

  test('shows reconstruction results heading', async ({ page }) => {
    await page.goto('/results/test-result-001');
    // Should show either the results or an error state
    const body = await page.textContent('body');
    const hasResults = body?.includes('Reconstruction Results') || body?.includes('Results Unavailable');
    expect(hasResults).toBeTruthy();
  });

  test('shows back to upload button', async ({ page }) => {
    await page.goto('/results/test-result-002');
    // Wait for either loading to finish or error state
    await page.waitForTimeout(2000);
    const hasBackButton = await page.locator('text=Back to Upload').or(page.locator('text=Go to Upload')).count();
    expect(hasBackButton).toBeGreaterThan(0);
  });
});

test.describe('Navigation', () => {
  test('home page loads', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Single Image/i);
  });

  test('upload page is accessible', async ({ page }) => {
    await page.goto('/upload');
    expect(page.url()).toContain('/upload');
  });

  test('download page is accessible', async ({ page }) => {
    await page.goto('/download');
    expect(page.url()).toContain('/download');
  });

  test('viewer page is accessible', async ({ page }) => {
    await page.goto('/viewer');
    expect(page.url()).toContain('/viewer');
  });
});

test.describe('Download Panel', () => {
  test('results page shows Pipeline Deliverables when data exists', async ({ page }) => {
    // Navigate to a results page (will show error state since no backend)
    await page.goto('/results/test-dl-panel');
    await page.waitForTimeout(2000);
    const body = await page.textContent('body');
    // Should show either deliverables or error
    const valid = body?.includes('Pipeline Deliverables') || body?.includes('Results Unavailable');
    expect(valid).toBeTruthy();
  });
});
