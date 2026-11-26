const puppeteer = require('puppeteer-core');
const fs = require('fs');
const OUT = '/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/font-annot';
const URL = 'https://solastyle.de/de/products/solar-panel-mounting-kits';

const PC = {
  width: 1920, tag: 'pc',
  groups: {
    A_scene: [
      {k:'scene_title', s:'Premium Black. Leistung', label:'场景主标题'},
      {k:'scene_metric', s:'23,5', label:'指标数字', minFs:30},
      {k:'scene_metric_t', s:'Modulwirkungsgrad unter', label:'指标标题'},
    ],
    B_tech: [
      {k:'tech_title', s:'Was macht LONGi', label:'技术标题'},
      {k:'tech_card_t', s:'HPBC-2.0-Rückkontaktzellen', label:'卡片标题'},
      {k:'tech_card_b', s:'Rückseitige Zellkontakte', label:'卡片正文'},
    ],
    C_home: [
      {k:'home_title', s:'Solarenergie – ganz', label:'居家主标题'},
      {k:'home_dim', s:'1800 × 1134', label:'尺寸数字', minFs:30},
    ],
    D_set: [{k:'set_title', s:'Zwei Module. Deine', label:'套装主标题'}],
    E_mount: [{k:'mount_title', s:'Deine Halterung – Teil', label:'支架主标题'}],
    F_install: [
      {k:'step_num', s:'01', label:'步骤序号', minFs:40, exact:true},
      {k:'step_title', s:'Platz prüfen', label:'步骤标题'},
    ],
  }
};
const MOB = {
  width: 390, tag: 'm',
  groups: {
    A_scene: [
      {k:'scene_title', s:'Premium Black. Leistung', label:'场景主标题'},
    ],
    B_tech: [
      {k:'tech_title', s:'Was macht LONGi', label:'技术标题'},
      {k:'tech_card_t', s:'HPBC-2.0-Rückkontaktzellen', label:'卡片标题'},
    ],
    C_home: [{k:'home_title', s:'Solarenergie – ganz', label:'居家主标题'}],
    D_set: [{k:'set_title', s:'Zwei Module. Deine', label:'套装主标题'}],
    E_mount: [{k:'mount_title', s:'Deine Halterung – Teil', label:'支架主标题'}],
    F_feature: [{k:'feature', s:'HPBC 2.0 Rückkontakttechnologie', label:'卖点文字'}],
    G_install: [{k:'step_title', s:'Platz prüfen', label:'步骤标题'}],
  }
};

async function measure(page, s, minFs, exact) {
  return page.evaluate((s, minFs, exact) => {
    const all = [...document.querySelectorAll('body *')];
    let best = null;
    for (const el of all) {
      const txt = (el.innerText || el.textContent || '').replace(/\s+/g,' ').trim();
      if (!txt) continue;
      const ok = exact ? txt === s : txt.includes(s);
      if (!ok) continue;
      // deepest: no child with same match
      const kids = [...el.children].filter(c => (c.innerText||c.textContent||'').replace(/\s+/g,' ').trim().includes(s));
      if (kids.length) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) continue;
      const cs = getComputedStyle(el);
      const fs = parseFloat(cs.fontSize);
      if (minFs && fs < minFs) continue;
      best = { x: r.x + window.scrollX, y: r.y + window.scrollY, w: r.width, h: r.height,
               fs: cs.fontSize, fw: cs.fontWeight, color: cs.color, ff: cs.fontFamily.split(',')[0],
               lh: cs.lineHeight, txt: txt.slice(0,40), tag: el.tagName };
      break;
    }
    return best;
  }, s, minFs || 0, !!exact);
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true, args: ['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'], timeout: 90000
  });
  const results = {};
  for (const cfg of [PC, MOB]) {
    const page = await browser.newPage();
    await page.setViewport({ width: cfg.width, height: 900 });
    await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 120000 });
    await new Promise(r => setTimeout(r, 3000));
    // auto scroll to load lazy
    await page.evaluate(async () => { for (let y=0;y<document.body.scrollHeight;y+=600){ window.scrollTo(0,y); await new Promise(r=>setTimeout(r,120)); } window.scrollTo(0,0); });
    await new Promise(r => setTimeout(r, 1500));
    for (const [gname, items] of Object.entries(cfg.groups)) {
      const gres = [];
      for (const it of items) {
        const m = await measure(page, it.s, it.minFs, it.exact);
        gres.push({ ...it, m });
      }
      results[`${cfg.tag}_${gname}`] = gres;
      // screenshot clip
      const rects = gres.filter(g => g.m).map(g => g.m);
      if (!rects.length) continue;
      const pad = 60;
      const x0 = Math.max(0, Math.min(...rects.map(r=>r.x)) - pad);
      const y0 = Math.max(0, Math.min(...rects.map(r=>r.y)) - pad);
      const x1 = Math.min(cfg.width, Math.max(...rects.map(r=>r.x+r.w)) + pad);
      const y1 = Math.max(...rects.map(r=>r.y+r.h)) + pad;
      await page.evaluate(y => window.scrollTo(0, y), Math.max(0, y0 - 100));
      await new Promise(r=>setTimeout(r,500));
      await page.screenshot({ path: `${OUT}/${cfg.tag}_${gname}.png`, clip: { x: x0, y: y0, width: x1-x0, height: y1-y0 }, captureBeyondViewport: true });
      results[`${cfg.tag}_${gname}_clip`] = { x0, y0, x1, y1 };
    }
    await page.close();
  }
  fs.writeFileSync(`${OUT}/measure.json`, JSON.stringify(results, null, 2));
  await browser.close();
  console.log('DONE');
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
