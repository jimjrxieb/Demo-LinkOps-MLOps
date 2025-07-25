import { test, expect } from '@playwright/test';
import jwt from 'jsonwebtoken';

// Helper to create an expired token for testing
const createExpiredToken = (role: string) => {
  const now = Math.floor(Date.now() / 1000);
  return jwt.sign(
    {
      sub: 'test-user',
      role,
      exp: now - 60, // Expired 1 minute ago
    },
    process.env.JWT_SECRET_KEY || 'test-secret'
  );
};

test.describe('Session Management', () => {
  test('should handle slim vs full user access correctly', async ({ page }) => {
    // Test slim user login
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'demo-slim');
    await page.fill('input[placeholder="Password"]', 'demo');
    await page.click('button:has-text("Login")');
    
    // Verify slim user restrictions
    await expect(page).toHaveURL('/');
    await page.goto('/ml-builder');
    await expect(page).toHaveURL('/'); // Should redirect back to home
    
    // Test full user login
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'demo-full');
    await page.fill('input[placeholder="Password"]', 'arise!');
    await page.click('button:has-text("Login")');
    
    // Verify full user access
    await expect(page).toHaveURL('/');
    await page.goto('/ml-builder');
    await expect(page).toHaveURL('/ml-builder'); // Should have access
  });

  test('should show session warning and handle refresh', async ({ page }) => {
    // Mock time functions
    await page.addInitScript(() => {
      const now = Date.now();
      window.originalDateNow = Date.now;
      window.Date.now = () => now + 25 * 60 * 1000; // 25 minutes elapsed
    });

    // Login
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'demo-slim');
    await page.fill('input[placeholder="Password"]', 'demo');
    await page.click('button:has-text("Login")');

    // Verify warning appears
    const warning = page.locator('.session-warning');
    await expect(warning).toBeVisible();
    
    // Test session extension
    await page.click('button:has-text("Extend Session")');
    await expect(warning).not.toBeVisible();
    
    // Verify timer reset
    const timer = page.locator('.session-timer');
    const timerText = await timer.textContent();
    expect(timerText).toContain('30:00');
  });

  test('should handle session expiry gracefully', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'demo-slim');
    await page.fill('input[placeholder="Password"]', 'demo');
    await page.click('button:has-text("Login")');

    // Mock expired token
    await page.evaluate(() => {
      localStorage.setItem('demo-linkops-auth', JSON.stringify({
        token: 'expired-token',
        role: 'slim'
      }));
    });

    // Try to access protected route
    await page.goto('/pipeline');
    
    // Should redirect to login
    await expect(page).toHaveURL('/login');
    
    // Should show error message
    const error = page.locator('.error-message');
    await expect(error).toBeVisible();
    await expect(error).toContainText('Session expired');
  });

  test('should maintain session with activity', async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'demo-slim');
    await page.fill('input[placeholder="Password"]', 'demo');
    await page.click('button:has-text("Login")');

    // Simulate user activity
    for (let i = 0; i < 5; i++) {
      await page.goto('/pipeline');
      await page.goto('/rag');
      await page.waitForTimeout(1000); // 1 second between actions
    }

    // Verify session is still active
    const timer = page.locator('.session-timer');
    await expect(timer).toBeVisible();
    await expect(page).not.toHaveURL('/login');
  });
});

test.describe('Session Security', () => {
  test('should not accept tampered tokens', async ({ page }) => {
    // Login normally
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'demo-slim');
    await page.fill('input[placeholder="Password"]', 'demo');
    await page.click('button:has-text("Login")');

    // Try to tamper with token
    await page.evaluate(() => {
      const auth = JSON.parse(localStorage.getItem('demo-linkops-auth') || '{}');
      auth.role = 'full'; // Try to escalate privileges
      localStorage.setItem('demo-linkops-auth', JSON.stringify(auth));
    });

    // Try to access restricted route
    await page.goto('/ml-builder');
    
    // Should be redirected
    await expect(page).toHaveURL('/');
  });

  test('should handle refresh token rotation', async ({ page, request }) => {
    // Login
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'demo-slim');
    await page.fill('input[placeholder="Password"]', 'demo');
    await page.click('button:has-text("Login")');

    // Store original refresh token
    const cookies = await page.context().cookies();
    const originalRefreshToken = cookies.find(c => c.name === 'refresh_token')?.value;

    // Trigger a refresh
    await page.click('button:has-text("Extend Session")');

    // Get new refresh token
    const newCookies = await page.context().cookies();
    const newRefreshToken = newCookies.find(c => c.name === 'refresh_token')?.value;

    // Verify token rotation
    expect(newRefreshToken).toBeDefined();
    expect(newRefreshToken).not.toEqual(originalRefreshToken);

    // Try to use old refresh token
    const response = await request.post('/auth/refresh', {
      headers: {
        Cookie: `refresh_token=${originalRefreshToken}`
      }
    });
    expect(response.status()).toBe(401);
  });
}); 