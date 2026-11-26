import json,re,difflib,sys
from figflat import flat
def rgb(s):
    m=re.findall(r'[\d.]+',s); r,g,b=[int(float(x)) for x in m[:3]]; a=float(m[3]) if len(m)>3 else 1
    return '#%02X%02X%02X'%(r,g,b)+('' if a>=.99 else '@%.2f'%a)
def norm(t): return re.sub(r'\s+',' ',t).strip()
def run(tag,figs):
    live=[]
    for st in ['default','tab1','tab2','tab3']:
        try: d=json.load(open(f'{tag}-{st}.json'))
        except: continue
        for t in d['texts']: t['st']=st; live.append(t)
    ft=[a for f in figs for a in flat(f) if a['k']=='text' and a['t']]
    res=[]
    for a in ft:
        ms=[l for l in live if norm(l['t'])==a['t']]
        if ms:
            l=ms[0]
            diffs=[]
            if a['fs'] and abs(float(l['fs'][:-2])-a['fs'])>=1: diffs.append(f"字号 线上{l['fs']} 设计{a['fs']:g}px")
            if a['fw'] and abs(int(l['fw'])-a['fw'])>=100: diffs.append(f"字重 线上{l['fw']} 设计{a['fw']:g}")
            if a['col'] and rgb(l['col']).split('@')[0]!=a['col'].split('@')[0]: diffs.append(f"颜色 线上{rgb(l['col'])} 设计{a['col']}")
            if (a['td'] or 'NONE')!='NONE' and 'underline' not in l['td'] : diffs.append('设计有下划线')
            if a['td']=='NONE' and 'underline' in l['td']: diffs.append('线上有下划线设计没有')
            if diffs: res.append(('STYLE',a['frame'],a['t'][:40],l['st'],'; '.join(diffs),round(a['y']),round(l['y'])))
        else:
            cand=difflib.get_close_matches(a['t'],[norm(l['t']) for l in live],n=1,cutoff=.5)
            res.append(('TEXT',a['frame'],a['t'][:60],cand[0][:60] if cand else None,'',round(a['y']),0))
    return res
if __name__=='__main__':
    tag=sys.argv[1]; figs=sys.argv[2:]
    for r in run(tag,figs): print(r)
