// 全量文字+容器样式采集：node _textcap.js  -> careful/auto/<tag>-<state>.json
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const OUT='/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/auto';
fs.mkdirSync(OUT,{recursive:true});
const L=(process.argv[2]||'de');
const cfgs=[
 {tag:`pc-${L}`,w:1920},
 {tag:`m-${L}`,w:390},
].filter(c=>!process.argv[3]||c.tag.startsWith(process.argv[3]));
const TABS={de:['Technische Daten','Versand & Lieferung','Garantie & Rückgabe'],en:['Technical','Shipping','Warranty']};
const grab = () => {
  const R = e => {const r=e.getBoundingClientRect(); return {x:+(r.x+scrollX).toFixed(1),y:+(r.y+scrollY).toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)}};
  const vis = e => {const c=getComputedStyle(e); if(c.display==='none'||c.visibility==='hidden'||+c.opacity===0) return false; const r=e.getBoundingClientRect(); return r.width>1&&r.height>1;};
  const texts=[], boxes=[];
  for(const e of document.querySelectorAll('body *')){
    if(['SCRIPT','STYLE','NOSCRIPT','SVG','PATH'].includes(e.tagName.toUpperCase())) continue;
    if(!vis(e)) continue;
    const c=getComputedStyle(e);
    const own=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').replace(/\s+/g,' ').trim();
    if(own){
      texts.push({t:own,...R(e),fs:c.fontSize,fw:c.fontWeight,col:c.color,td:c.textDecorationLine,ff:c.fontFamily.split(',')[0].replace(/"/g,''),lh:c.lineHeight,ls:c.letterSpacing,tag:e.tagName,cls:(e.className||'').toString().slice(0,40)});
    }
    const bw=parseFloat(c.borderTopWidth)||0;
    const hasBorder=bw>0&&c.borderTopStyle!=='none';
    const bg=c.backgroundColor!=='rgba(0, 0, 0, 0)';
    const rad=c.borderRadius!=='0px';
    const sh=c.boxShadow!=='none';
    const r=e.getBoundingClientRect();
    if((hasBorder||sh||(bg&&rad)||(bg&&r.width<900))&&r.width>=16&&r.height>=16&&r.width<1700){
      boxes.push({...R(e),bd:hasBorder?`${bw}px ${c.borderTopColor}`:'',bdb:`${c.borderBottomWidth} ${c.borderBottomColor}`,rad:c.borderRadius,sh:c.boxShadow==='none'?'':c.boxShadow,bg:bg?c.backgroundColor:'',tag:e.tagName,cls:(e.className||'').toString().slice(0,40)});
    }
  }
  return {texts,boxes,H:document.documentElement.scrollHeight};
};
(async()=>{
  const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'],timeout:90000});
  for(const c of cfgs){
    const p=await b.newPage(); await p.setViewport({width:c.w,height:1000,deviceScaleFactor:1});
    await p.goto(`https://solastyle.de/${L}/products/solar-panel-mounting-kits`,{waitUntil:'domcontentloaded',timeout:120000});
    await new Promise(r=>setTimeout(r,3500));
    // lazy load
    const H=await p.evaluate(()=>document.documentElement.scrollHeight);
    for(let y=0;y<H;y+=600){await p.evaluate(y=>scrollTo(0,y),y);await new Promise(r=>setTimeout(r,120));}
    await p.evaluate(()=>scrollTo(0,0)); await new Promise(r=>setTimeout(r,800));
    fs.writeFileSync(`${OUT}/${c.tag}-default.json`,JSON.stringify(await p.evaluate(grab))); await p.evaluate(()=>scrollTo(0,0)); await p.screenshot({path:`${OUT}/${c.tag}-default.png`,fullPage:true});
    for(let i=0;i<TABS[L].length;i++){
      const name=TABS[L][i];
      const ok=await p.evaluate(n=>{const el=[...document.querySelectorAll('button,a,[role=tab],summary,li,span,div')].filter(e=>(e.innerText||'').replace(/\s+/g,' ').trim().toLowerCase().startsWith(n.toLowerCase())&&e.getBoundingClientRect().width>20&&e.getBoundingClientRect().height<120).sort((a,b)=>(a.innerText.length-b.innerText.length))[0]; if(!el) return false; el.scrollIntoView({block:'center'}); el.click(); return true;},name);
      await new Promise(r=>setTimeout(r,1200));
      if(ok){ fs.writeFileSync(`${OUT}/${c.tag}-tab${i+1}.json`,JSON.stringify(await p.evaluate(grab))); await p.screenshot({path:`${OUT}/${c.tag}-tab${i+1}.png`,fullPage:true}); }
      console.log(c.tag,name,ok);
    }
    await p.close();
  }
  await b.close(); console.log('done');
})();
