/* End-to-end checks against a running web and API with the local v2 data.
 * Run from web: npm run test:browsers (defaults to http://127.0.0.1:5185).
 */
const { chromium, firefox, webkit } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.FLOODRISK_WEB_URL || 'http://127.0.0.1:5185';
const out = path.resolve(__dirname, '../../docs/evidence/mobile');
const rows = [];

async function noOverflow(page, context) {
  const bounds = await page.evaluate(() => ({ width: innerWidth, scroll: document.documentElement.scrollWidth }));
  assert(bounds.scroll <= bounds.width + 1, `${context}: page overflow ${JSON.stringify(bounds)}`);
}

(async () => {
  fs.mkdirSync(out, { recursive: true });
  for (const [name, engine] of Object.entries({ chromium, firefox, webkit })) {
    const browser = await engine.launch({ headless: true });
    try {
      for (const width of [320, 390, 768, 1440]) {
        const context = await browser.newContext({ viewport: { width, height: 844 }, reducedMotion: 'reduce' });
        const page = await context.newPage();
        const errors = [];
        page.on('pageerror', error => errors.push(error.stack || error.message));
        await page.goto(base);
        await page.locator('.metric').first().waitFor();
        await page.locator('.national-map path.leaflet-interactive').first().waitFor();
        assert.equal(await page.locator('select').count(), 3);
        for (const control of await page.locator('select, nav button').all()) {
          assert((await control.boundingBox()).height >= 44);
        }
        await noOverflow(page, `${name}/${width}/national`);
        await page.locator('path[aria-label="Texas · TX · Ver condados"]').click({ force: true });
        await page.getByRole('heading', { name: 'Explora los condados · TX' }).waitFor();
        await page.getByRole('button', { name: 'Acercar selección' }).waitFor({ state: 'visible' });
        await page.getByRole('button', { name: 'Acercar selección' }).click();
        await page.getByRole('button', { name: 'Ver estado', exact: true }).click();
        await page.getByLabel('Condado', { exact: true }).selectOption('48453');
        await page.locator('.metric').filter({ hasText: 'Travis County' }).waitFor();
        await page.getByLabel('Condado', { exact: true }).selectOption('48047');
        await page.getByRole('alert').waitFor();
        assert.equal(await page.locator('.metric').count(), 0, 'Missing result must not appear as zero');
        await noOverflow(page, `${name}/${width}/missing`);
        await page.getByLabel('Estado', { exact: true }).selectOption('FL');
        await page.getByLabel('Condado', { exact: true }).selectOption('12086');
        await page.locator('.metric').filter({ hasText: 'Miami-Dade County' }).waitFor();
        await page.getByLabel('Condado', { exact: true }).selectOption('12095');
        await page.locator('.metric').filter({ hasText: 'Orange County' }).waitFor();
        const chart = page.getByRole('list', { name: 'Eventos reportados por año' });
        await chart.waitFor();
        await chart.evaluate(el => { el.scrollLeft = el.scrollWidth; });
        await page.getByRole('button', { name: 'Volver al país' }).click();
        await page.getByRole('heading', { name: 'Estados Unidos · Explora por estado' }).waitFor();
        await page.getByRole('button', { name: 'Metodología', exact: true }).click();
        await page.getByRole('heading', { name: 'Metodología experimental' }).waitFor();
        await noOverflow(page, `${name}/${width}/methodology`);
        await page.getByRole('button', { name: 'Resumen general', exact: true }).click();
        await page.locator('.metric').first().waitFor();
        await page.getByLabel('Estado', { exact: true }).selectOption('TX');
        await page.getByLabel('Condado', { exact: true }).selectOption('48201');
        await page.locator('.metric').filter({ hasText: 'Harris County' }).waitFor();
        await page.waitForFunction(() => [...document.querySelectorAll('.map-actions button')]
          .some(button => button.textContent === 'Acercar selección' && !button.disabled));
        await page.locator('.county-map path.leaflet-interactive').first().waitFor();
        await noOverflow(page, `${name}/${width}/result`);
        if ((name === 'chromium' && width === 1440) || (name === 'webkit' && width === 390)) {
          await page.screenshot({ path: path.join(out, `${name}-${width}.png`), fullPage: true });
        }
        if (width === 390) {
          await page.setViewportSize({ width: 844, height: 390 });
          await noOverflow(page, `${name}/landscape`);
          await page.setViewportSize({ width, height: 844 });
        }
        // A failed API request remains an error, never a silent demo fallback.
        await page.route('**/api/**', route => route.abort());
        await page.reload();
        await page.getByRole('alert').waitFor();
        assert.equal(await page.locator('.metric').count(), 0);
        assert.deepEqual(errors, [], name + '/' + width + ': No uncaught browser exceptions');
        rows.push({ engine: name, version: browser.version(), width, status: 'passed' });
        console.log(name + '/' + width + ' passed');
        await context.close();
      }
    } finally { await browser.close(); }
  }
  fs.writeFileSync(path.join(out, 'results.json'), JSON.stringify({ timestamp: new Date().toISOString(), base, mode: 'live-local-v2-api', results: rows }, null, 2));
  console.log(JSON.stringify(rows, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
