const puppeteer=require('puppeteer-core');const fs=require('fs');
const OUT='/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/auto/';
const grab=()=>{const out=[];for(const e of document.querySelectorAll('img')){const r=e.getBoundingClientRect();if(r.width<40||r.height<40)continue;const c=getComputedStyle(e);if(c.display==='none'||c.visibility==='hidden')continue;
 out.push({src:(e.currentSrc||e.src).slice(-80),x:Math.round(r.x+scrollX),y:Math.round(r.y+scrollY),w:Math.round(r.width),h:Math.round(r.height),nw:e.naturalWidth,nh:e.naturalHeight,alt:(e.alt||'').slice(0,30),fit:c.objectFit,cls:(e.className||'').toString().slice(0,30)});}
 for(const e of document.querySelectorAll('div,section,span')){const c=getComputedStyle(e);if(c.backgroundImage&&c.backgroundImage.startsWith('url')){const r=e.getBoundingClientRect();if(r.width<100)continue;out.push({bg:c.backgroundImage.slice(5,90),x:Math.round(r.x+scrollX),y:Math.round(r.y+scrollY),w:Math.round(r.width),h:Math.round(r.height),cls:(e.className||'').toString().slice(0,30)});}}
 return out;};
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
for(const [tag,w,dpr] of [['pc',1920,1],['m',390,3]]){
 const p=await b.newPage();await p.setViewport({width:w,height:1000,deviceScaleFactor:dpr});
 await p.goto('https://solastyle.de/de/products/solar-panel-mounting-kits',{waitUntil:'domcontentloaded',timeout:120000});await new Promise(r=>setTimeout(r,4000));
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);for(let y=0;y<H;y+=500){await p.evaluate(y=>scrollTo(0,y),y);await new Promise(r=>setTimeout(r,200));}
 await new Promise(r=>setTimeout(r,1500));
 // tabs
 const all=await p.evaluate(grab);fs.writeFileSync(OUT+`imgs-${tag}-default.json`,JSON.stringify(all));
 for(const [i,n] of ['Technische Daten','Versand & Lieferung','Garantie & Rückgabe'].entries()){
  await p.evaluate(n=>{const el=[...document.querySelectorAll('button,a,[role=tab],li,span,div')].filter(e=>(e.innerText||'').replace(/\s+/g,' ').trim().startsWith(n)&&e.getBoundingClientRect().height<120).sort((a,b)=>a.innerText.length-b.innerText.length)[0];if(el){el.scrollIntoView({block:'center'});el.click();}},n);
  await new Promise(r=>setTimeout(r,1500));
  fs.writeFileSync(OUT+`imgs-${tag}-tab${i+1}.json`,JSON.stringify(await p.evaluate(grab)));}
 await p.close();}
await b.close();console.log('done');})();
