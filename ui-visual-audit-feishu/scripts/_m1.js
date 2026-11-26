const puppeteer = require('puppeteer-core');
const fs = require('fs');
const OUT='/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/m1';
fs.mkdirSync(OUT,{recursive:true});
const cfgs=[
 {tag:'pc-de',url:'https://solastyle.de/de/products/solar-panel-mounting-kits',w:1920},
 {tag:'pc-en',url:'https://solastyle.de/en/products/solar-panel-mounting-kits',w:1920},
 {tag:'m-de',url:'https://solastyle.de/de/products/solar-panel-mounting-kits',w:390},
 {tag:'m-en',url:'https://solastyle.de/en/products/solar-panel-mounting-kits',w:390},
];
const probe = () => {
  const cs = e => getComputedStyle(e);
  const R = e => {const r=e.getBoundingClientRect(); return {x:+(r.x+scrollX).toFixed(1),y:+(r.y+scrollY).toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)}};
  const style = e => {const c=cs(e); return {bd:`${c.borderTopWidth} ${c.borderTopStyle} ${c.borderTopColor}`, bdR:`${c.borderRightWidth} ${c.borderRightColor}`, rad:c.borderRadius, sh:c.boxShadow, ol:`${c.outlineWidth} ${c.outlineStyle} ${c.outlineColor} off${c.outlineOffset}`, bg:c.backgroundColor, bgi:c.backgroundImage.slice(0,60), pad:c.padding, fs:c.fontSize, fw:c.fontWeight, col:c.color, td:c.textDecorationLine+' '+c.textDecorationColor, ff:c.fontFamily.split(',')[0]}};
  const deep = (s)=>[...document.querySelectorAll('body *')].filter(e=>{const t=(e.innerText||'').replace(/\s+/g,' ').trim(); return t===s || (t.includes(s)&&![...e.children].some(c=>(c.innerText||'').replace(/\s+/g,' ').includes(s)))&&e.getBoundingClientRect().width>2;});
  const out={};
  // option cards: climb from option names
  const climb=(txt)=>{
    const el=deep(txt)[0]; if(!el) return null;
    const chain=[]; let e=el;
    for(let i=0;i<8&&e&&e!==document.body;i++){chain.push({tag:e.tagName,cls:(e.className||'').toString().slice(0,50),...R(e),...style(e)}); e=e.parentElement;}
    return chain;
  };
  out.card_sel_panel = climb('EcoLife Premium Black');
  out.card_un_panel = climb('Hi-MO X10');
  out.card_sel_mount = climb('Balkonhalterung');
  out.card_un_mount = climb('Universalhalterung');
  // labels
  const lbl={}; for(const s of ['Wähle deine Solarmodule','Solarmodule','Wähle deine Halterung','Halterung','Menge','Anzahl','Choose your','Quantity']){const e=deep(s)[0]; if(e) lbl[s]={...R(e),...style(e),txt:e.innerText.slice(0,30)};} out.labels=lbl;
  // buttons
  const btns={}; for(const s of ['In den Warenkorb','Add to cart','Add to Cart','Mit PayPal','Pay with','PayPal','Versandinformationen','Shipping information','Jetzt','Checkout']){const e=deep(s)[0]; if(e) btns[s]={...R(e),...style(e),txt:e.innerText.slice(0,40),tag:e.tagName};} out.btns=btns;
  // gallery buttons: all buttons in top 1100px
  out.gal=[...document.querySelectorAll('button,a,[role=button]')].filter(e=>{const r=e.getBoundingClientRect(); return r.y+scrollY>150&&r.y+scrollY<1300&&r.width>20&&r.width<130&&r.height>20&&r.height<130;}).slice(0,40).map(e=>({tag:e.tagName,aria:(e.getAttribute('aria-label')||'').slice(0,30),cls:(e.className||'').toString().slice(0,40),...R(e),...style(e),svg:(e.querySelector('svg')?R(e.querySelector('svg')):null), svgstroke:e.querySelector('svg')?[...e.querySelectorAll('svg *')].slice(0,3).map(p=>cs(p).stroke+' '+cs(p).strokeWidth):null}));
  return out;
};
(async()=>{
  const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'],timeout:90000});
  for(const c of cfgs){
    const p=await b.newPage(); await p.setViewport({width:c.w,height:1000,deviceScaleFactor:2});
    await p.goto(c.url,{waitUntil:'domcontentloaded',timeout:120000}); await new Promise(r=>setTimeout(r,3500));
    const data=await p.evaluate(probe);
    fs.writeFileSync(`${OUT}/${c.tag}.json`,JSON.stringify(data,null,1));
    // screenshots of top area
    await p.evaluate(()=>window.scrollTo(0,0)); await new Promise(r=>setTimeout(r,500));
    await p.screenshot({path:`${OUT}/${c.tag}-top.png`,clip:{x:0,y:0,width:c.w,height:c.w===1920?1100:2000},captureBeyondViewport:true});
    await p.close(); console.log('done',c.tag);
  }
  await b.close();
})().catch(e=>{console.error('ERR',e.message);process.exit(1)});
