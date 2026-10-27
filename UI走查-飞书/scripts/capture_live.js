#!/usr/bin/env node
/**
 * 采集线上页面：整页截图 + 叶子元素的 rect 与计算样式（含祖先累乘 opacity）。
 *
 * 依赖: npm i puppeteer-core   （使用本机 Chrome）
 * 用法: node capture_live.js <url> <width> <outDir> [height=1000] [--lang de]
 *   例: node capture_live.js https://example.com/page 1920 out/pc
 *       node capture_live.js https://example.com/de/page 390 out/mobile_de 844
 * 环境变量: CHROME_PATH 默认 macOS Google Chrome
 * 输出: <outDir>/page.png, <outDir>/dom.json  (按顶层 section 分组)
 */
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer-core');

const [url, widthArg, outDir, heightArg] = process.argv.slice(2).filter(a => !a.startsWith('--'));
if (!url || !widthArg || !outDir) {
  console.error('usage: node capture_live.js <url> <width> <outDir> [height] [--lang xx]');
  process.exit(1);
}
const lang = (process.argv.includes('--lang') && process.argv[process.argv.indexOf('--lang') + 1]) || null;
const width = parseInt(widthArg, 10);
const height = parseInt(heightArg || '1000', 10);
const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await puppeteer.launch({ executablePath: chrome, headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1, isMobile: width < 600 });
  if (lang) await page.setExtraHTTPHeaders({ 'Accept-Language': lang });
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 90000 });

  // 懒加载：强制 eager + 滚动到底再回顶
  await page.evaluate(async () => {
    document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
    await new Promise(res => {
      let y = 0;
      const t = setInterval(() => {
        window.scrollBy(0, 600); y += 600;
        if (y >= document.documentElement.scrollHeight) { clearInterval(t); res(); }
      }, 120);
    });
    window.scrollTo(0, 0);
    await document.fonts.ready;
  });
  await new Promise(r => setTimeout(r, 1500));

  await page.screenshot({ path: path.join(outDir, 'page.png'), fullPage: true });

  const data = await page.evaluate(() => {
    const effOpacity = el => { let o = 1; for (let e = el; e; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity); return o; };
    const pick = sel => [...document.querySelectorAll(sel)].filter(s => s.getBoundingClientRect().height > 20);
    let sections = pick('main > *, body > .shopify-section, body > section');
    if (!sections.length) sections = pick('body > *:not(script):not(style):not(noscript)'); // 兜底：非常规结构
    return sections.map((s, idx) => {
      const sr = s.getBoundingClientRect();
      const items = [];
      [s, ...s.querySelectorAll('*')].forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width < 1 || r.height < 1) return;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none') return;
        const ownText = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ').trim();
        const isLeaf = ['IMG', 'SVG', 'svg', 'VIDEO', 'BUTTON', 'INPUT'].includes(el.tagName) || ownText || cs.backgroundImage !== 'none' || cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.borderTopWidth !== '0px';
        if (!isLeaf) return;
        items.push({
          tag: el.tagName.toLowerCase(), cls: (el.getAttribute('class') || '').slice(0, 60), text: ownText.slice(0, 120),
          x: Math.round(r.x), y: Math.round(r.y + scrollY), w: +r.width.toFixed(1), h: +r.height.toFixed(1),
          fs: cs.fontSize, fw: cs.fontWeight, lh: cs.lineHeight, ls: cs.letterSpacing, color: cs.color, op: effOpacity(el).toFixed(2),
          ff: cs.fontFamily.slice(0, 40), ta: cs.textAlign, bg: cs.backgroundColor, bgi: cs.backgroundImage.slice(0, 80),
          bd: cs.border.slice(0, 60), radius: cs.borderRadius, shadow: cs.boxShadow.slice(0, 80),
          src: el.currentSrc || el.getAttribute('src') || '', nat: el.naturalWidth ? `${el.naturalWidth}x${el.naturalHeight}` : '',
        });
      });
      return { idx, id: s.id, cls: (s.getAttribute('class') || '').slice(0, 60), y: Math.round(sr.y + scrollY), h: Math.round(sr.height), w: Math.round(sr.width), text: (s.innerText || s.textContent || '').slice(0, 80).replace(/\s+/g, ' '), items };
    });
  });
  fs.writeFileSync(path.join(outDir, 'dom.json'), JSON.stringify(data, null, 1));
  console.log(`ok: ${data.length} sections -> ${outDir}`);
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
