import json,re
from PIL import Image, ImageDraw, ImageFont
A='/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/auto/'
OUT=A+'img/'
import os; os.makedirs(OUT,exist_ok=True)
_cache={}
def load(tag,st='default'):
    k=(tag,st)
    if k not in _cache: _cache[k]=json.load(open(f'{A}{tag}-{st}.json'))
    return _cache[k]
def T(tag,st,prefix,ymin=0,ymax=1e9,xmin=0,xmax=1e9,nth=0):
    """文字元素矩形 (x,y,w,h)"""
    ms=[t for t in load(tag,st)['texts'] if t['t'].startswith(prefix) and ymin<=t['y']<=ymax and xmin<=t['x']<=xmax]
    if not ms: raise Exception(f'NOT FOUND {tag} {st} {prefix} {ymin}-{ymax}')
    t=ms[nth]; return (t['x'],t['y'],t['w'],t['h'])
def Bx(tag,st,cls,ymin=0,ymax=1e9,xmin=0,xmax=1e9,nth=0):
    ms=[b for b in load(tag,st)['boxes'] if cls in b['cls'] and ymin<=b['y']<=ymax and xmin<=b['x']<=xmax]
    b=ms[nth]; return (b['x'],b['y'],b['w'],b['h'])
def U(*rs):
    x0=min(r[0] for r in rs);y0=min(r[1] for r in rs);x1=max(r[0]+r[2] for r in rs);y1=max(r[1]+r[3] for r in rs)
    return (x0,y0,x1-x0,y1-y0)
def font(sz):
    for p in ('/System/Library/Fonts/Supplemental/Arial Unicode.ttf','/Library/Fonts/Arial Unicode.ttf'):
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
def mk(tag,st,items,out,pad=36,minw=0,maxh=1500,grow=4):
    """items: [(n,(x,y,w,h)), ...] 同一编号可出现多次；返回输出路径"""
    img=Image.open(f'{A}{tag}-{st}.png').convert('RGB'); W,H=img.size
    rs=[r for n,r in items]
    x0=min(r[0] for r in rs)-pad; y0=min(r[1] for r in rs)-pad
    x1=max(r[0]+r[2] for r in rs)+pad; y1=max(r[1]+r[3] for r in rs)+pad
    if x1-x0<minw: c=(x0+x1)/2; x0=c-minw/2; x1=c+minw/2
    x0,y0,x1,y1=int(max(0,x0)),int(max(0,y0)),int(min(W,x1)),int(min(H,y1))
    if y1-y0>maxh: print('WARN tall',out,y1-y0)
    crop=img.crop((x0,y0,x1,y1)); d=ImageDraw.Draw(crop); f=font(22 if W>800 else 18)
    seen=set()
    for n,r in items:
        bx=(r[0]-x0-grow,r[1]-y0-grow,r[0]-x0+r[2]+grow,r[1]-y0+r[3]+grow)
        d.rectangle(bx,outline=(230,0,0),width=3)
        if n not in seen:
            seen.add(n); s=str(n); tw=d.textlength(s,font=f)
            cx,cy=bx[0],max(0,bx[1]-26)
            d.rectangle((cx,cy,cx+tw+12,cy+26),fill=(230,0,0)); d.text((cx+6,cy+1),s,fill='white',font=f)
    crop.save(OUT+out); return OUT+out
