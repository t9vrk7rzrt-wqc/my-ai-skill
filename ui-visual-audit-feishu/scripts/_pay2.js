const puppeteer=require('puppeteer-core');const fs=require('fs');
const OUT='/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/auto/pay/';
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
for(const [tag,w] of [['pc',1920],['m',390]]){
 const p=await b.newPage();await p.setViewport({width:w,height:1000,deviceScaleFactor:1});
 let ok=false;
 for(let i=0;i<6&&!ok;i++){
  await p.goto('https://solastyle.de/en/products/solar-panel-mounting-kits',{waitUntil:'domcontentloaded',timeout:120000});
  await new Promise(r=>setTimeout(r,4000));
  ok=await p.evaluate(()=>!!document.querySelector('.product-form__submit'));console.log(tag,'try',i,ok);
 }
 for(const lab of ['t3','reload']){
  if(lab==='reload'){await p.reload({waitUntil:'domcontentloaded'});await new Promise(r=>setTimeout(r,8000));}
  const y=await p.evaluate(()=>{const e=document.querySelector('.product-form__submit');return e?e.getBoundingClientRect().y+scrollY:1100;});
  await p.evaluate(y=>scrollTo(0,y-200),y);await new Promise(r=>setTimeout(r,800));
  await p.screenshot({path:`${OUT}${tag}-en2-${lab}.png`});
 }
 await p.close();}
await b.close();})();
