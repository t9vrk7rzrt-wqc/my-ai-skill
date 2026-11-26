const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true, args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'], timeout:90000});
  const out = {};
  for (const [tag,w,queries] of [
    ['pc',1920,[['1800',4900,9999,0],['Balkonhalterung',5000,6200,16],['Haken',5000,6200,0]]],
    ['m',390,[['Balkonhalterung',6700,7600,16]]],
  ]) {
    const page = await browser.newPage();
    await page.setViewport({width:w,height:900});
    await page.goto('https://solastyle.de/de/products/solar-panel-mounting-kits',{waitUntil:'domcontentloaded',timeout:120000});
    await new Promise(r=>setTimeout(r,2500));
    await page.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,100));} window.scrollTo(0,0);});
    await new Promise(r=>setTimeout(r,1000));
    for (const [s,y0,y1,minFs] of queries) {
      const r = await page.evaluate((s,y0,y1,minFs)=>{
        const els=[...document.querySelectorAll('body *')].filter(e=>{
          const t=(e.innerText||'').replace(/\s+/g,' ').trim();
          if(!t.includes(s)) return false;
          if([...e.children].some(c=>((c.innerText||'')).replace(/\s+/g,' ').includes(s))) return false;
          const rc=e.getBoundingClientRect(); const yy=rc.y+scrollY;
          return yy>=y0 && yy<=y1 && rc.width>2 && parseFloat(getComputedStyle(e).fontSize)>=minFs;
        });
        return els.slice(0,3).map(e=>{const rc=e.getBoundingClientRect();const cs=getComputedStyle(e);return {txt:e.innerText.slice(0,30),x:rc.x,y:rc.y+scrollY,w:rc.width,h:rc.height,fs:cs.fontSize,fw:cs.fontWeight,color:cs.color};});
      }, s,y0,y1,minFs);
      out[`${tag}:${s}`]=r;
    }
    await page.close();
  }
  console.log(JSON.stringify(out,null,1));
  await browser.close();
})().catch(e=>{console.error('ERR',e.message);process.exit(1);});
