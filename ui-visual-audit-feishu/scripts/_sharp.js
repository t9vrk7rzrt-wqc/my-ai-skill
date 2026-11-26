const puppeteer=require('puppeteer-core');
const OUT='/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/auto/pay/';
(async()=>{const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage']});
for(const [tag,w,dpr,clip] of [['m',390,3,{x:0,y:110,width:390,height:390}],['pc',1920,2,{x:364,y:234,width:720,height:720}]]){
 const p=await b.newPage();await p.setViewport({width:w,height:1000,deviceScaleFactor:dpr});
 await p.goto('https://solastyle.de/de/products/solar-panel-mounting-kits',{waitUntil:'domcontentloaded',timeout:120000});await new Promise(r=>setTimeout(r,7000));
 await p.screenshot({path:OUT+`sharp-${tag}.png`,clip});
 console.log(tag,await p.evaluate(()=>[...document.querySelectorAll('img')].filter(i=>i.getBoundingClientRect().width>300).slice(0,3).map(i=>[i.naturalWidth,i.complete,(i.currentSrc||'').slice(-40)])));
 await p.close();}
await b.close();})();
