// Render every *.svg under the given paths to PNG at its intrinsic size (headless Chromium).
// usage: NODE_PATH=$(npm root -g) node render.cjs <dir-or-file> [...]
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

const files = [];
const walk = (p) => fs.statSync(p).isDirectory()
  ? fs.readdirSync(p).forEach((f) => walk(path.join(p, f)))
  : p.endsWith('.svg') && files.push(path.resolve(p));
process.argv.slice(2).forEach(walk);

(async () => {
  const browser = await chromium.launch();
  for (const f of files) {
    const svg = fs.readFileSync(f, 'utf8');
    const w = +svg.match(/width="(\d+)"/)[1];
    const h = +svg.match(/height="(\d+)"/)[1];
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await page.setContent(`<html><body style="margin:0;background:#000">${svg}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: f.replace(/\.svg$/, '.png'), clip: { x: 0, y: 0, width: w, height: h } });
    await page.close();
    console.log('rendered', path.relative(process.cwd(), f.replace(/\.svg$/, '.png')));
  }
  await browser.close();
})();
