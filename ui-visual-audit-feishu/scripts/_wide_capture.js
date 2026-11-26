const puppeteer = require('puppeteer-core');
const fs = require('fs');
const OUT = '/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/font-annot';
const URL = 'https://solastyle.de/de/products/solar-panel-mounting-kits';
const jobs = [
 {name:'pc_set_wide', w:1920, anchor:'Zwei Module. Deine', up:60, down:620},
 {name:'pc_mount_wide', w:1920, anchor:'Deine Halterung – Teil', up:60, down:720},
 {name:'pc_scene_wide', w:1920, anchor:'Premium Black. Leistung', up:120, down:520},
 {name:'pc_home_wide', w:1920, anchor:'Solarenergie – ganz', up:60, down:620},
 {name:'m_set_wide', w:390, anchor:'Zwei Module. Deine', up:40, down:520},
 {name:'m_mount_wide', w:390, anchor:'Deine Halterung – Teil', up:40, down:520},
 {name:'m_scene_wide', w:390, anchor:'Premium Black. Leistung', up:60, down:320},
 {name:'m_tech_wide', w:390, anchor:'Was macht LONGi', up:40, down:620},
];
(async () => {
  const browser = await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true, args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'], timeout:90000});
  const info = {};
  for (const w of [1920, 390]) {
    const page = await browser.newPage();
    await page.setViewport({width: w, height: 900});
    await page.goto(URL, {waitUntil:'domcontentloaded', timeout:120000});
    await new Promise(r=>setTimeout(r,2500));
    await page.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,100));} window.scrollTo(0,0);});
    await new Promise(r=>setTimeout(r,1200));
    for (const j of jobs.filter(j=>j.w===w)) {
      const r = await page.evaluate((s)=>{
        const el=[...document.querySelectorAll('body *')].filter(e=>{const t=(e.innerText||'').replace(/\s+/g,' ').trim(); return t.includes(s) && ![...e.children].some(c=>((c.innerText||'')).replace(/\s+/g,' ').includes(s));})[0];
        if(!el) return null; const rc=el.getBoundingClientRect(); return {x:rc.x+scrollX,y:rc.y+scrollY,w:rc.width};
      }, j.anchor);
      if(!r){ info[j.name]='miss'; continue; }
      const cx = w===1920 ? 0 : 0;
      const clip={x:0, y:Math.max(0,r.y-j.up), width:w, height:j.up+j.down};
      await page.screenshot({path:`${OUT}/${j.name}.png`, clip, captureBeyondViewport:true});
      info[j.name]={clipY:clip.y, clipH:clip.height, titleY:r.y, titleX:r.x};
    }
    await page.close();
  }
  fs.writeFileSync(`${OUT}/wide_info.json`, JSON.stringify(info,null,1));
  await browser.close(); console.log('DONE', JSON.stringify(info));
})().catch(e=>{console.error('ERR',e.message);process.exit(1);});
