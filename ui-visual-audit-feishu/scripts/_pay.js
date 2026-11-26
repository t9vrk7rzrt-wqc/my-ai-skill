const puppeteer=require('puppeteer-core');const fs=require('fs');
const OUT='/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/auto/pay/';fs.mkdirSync(OUT,{recursive:true});
const probe=()=>{const out=[];for(const e of document.querySelectorAll('button,a,[role=button],iframe,shopify-accelerated-checkout,paypal-button,[class*=paypal],[class*=checkout],[class*=dynamic]')){const r=e.getBoundingClientRect();if(r.width<100||r.height<30||r.y+scrollY<900||r.y+scrollY>2200)continue;const c=getComputedStyle(e);out.push({tag:e.tagName,cls:(e.className||'').toString().slice(0,50),x:Math.round(r.x),y:Math.round(r.y+scrollY),w:Math.round(r.width),h:Math.round(r.height),bg:c.backgroundColor,txt:(e.innerText||'').replace(/\s+/g,' ').slice(0,40),rad:c.borderRadius});}return out;};
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
for(const [tag,w] of [['pc',1920],['m',390]]){
 const p=await b.newPage();await p.setViewport({width:w,height:1000,deviceScaleFactor:1});
 for(const lang of ['de','en']){
  const url=`https://solastyle.de/${lang}/products/solar-panel-mounting-kits`;
  await p.goto(url,{waitUntil:'domcontentloaded',timeout:120000});
  for(const [lab,ms] of [['t3',3000],['t12',9000]]){
    await new Promise(r=>setTimeout(r,ms));
    const y=await p.evaluate(()=>{const e=document.querySelector('.product-form__submit');return e?e.getBoundingClientRect().y+scrollY:1100;});
    await p.evaluate(y=>scrollTo(0,y-200),y);await new Promise(r=>setTimeout(r,800));
    await p.screenshot({path:`${OUT}${tag}-${lang}-load-${lab}.png`});
    fs.writeFileSync(`${OUT}${tag}-${lang}-load-${lab}.json`,JSON.stringify(await p.evaluate(probe)));
  }
  await p.reload({waitUntil:'domcontentloaded'});await new Promise(r=>setTimeout(r,8000));
  const y=await p.evaluate(()=>{const e=document.querySelector('.product-form__submit');return e?e.getBoundingClientRect().y+scrollY:1100;});
  await p.evaluate(y=>scrollTo(0,y-200),y);await new Promise(r=>setTimeout(r,800));
  await p.screenshot({path:`${OUT}${tag}-${lang}-reload.png`});
  fs.writeFileSync(`${OUT}${tag}-${lang}-reload.json`,JSON.stringify(await p.evaluate(probe)));
  console.log(tag,lang,'ok');
 }
 await p.close();}
await b.close();})();
