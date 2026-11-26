import json,re,difflib,sys,statistics
from figflat import flat
from textcmp import rgb,norm
def run(tag,fig,states,lo=None):
    live=[]
    for st in states:
        d=json.load(open(f'{tag}-{st}.json'))
        for t in d['texts']: t['st']=st; live.append(t)
    ft=[a for a in flat(fig) if a['k']=='text' and a['t'] and (a['fs'] or 0)>=8]
    by={}
    for l in live: by.setdefault(norm(l['t']),[]).append(l)
    offs=[by[a['t']][0]['y']-a['y'] for a in ft if a['t'] in by and len(by[a['t']])==1]
    med=statistics.median(offs) if offs else 0
    res=[]
    for a in ft:
        ms=by.get(a['t'])
        if ms:
            l=min(ms,key=lambda l:abs(l['y']-a['y']-med))
            diffs=[]
            if a['fs'] and abs(float(l['fs'][:-2])-a['fs'])>=1: diffs.append(f"字号 线上{l['fs'][:-2]}px 设计{a['fs']:g}px")
            if a['fw'] and abs(int(l['fw'])-a['fw'])>=100: diffs.append(f"字重 线上{l['fw']} 设计{a['fw']:g}")
            if a['col'] and rgb(l['col']).split('@')[0]!=a['col'].split('@')[0]: diffs.append(f"颜色 线上{rgb(l['col'])} 设计{a['col']}")
            if a['td']=='UNDERLINE' and 'underline' not in l['td']: diffs.append('设计有下划线线上没有')
            if a['td'] in ('NONE','') and 'underline' in l['td']: diffs.append('线上有下划线设计没有')
            if diffs: res.append(('STYLE',a['frame'][:12],a['t'][:34],'; '.join(diffs),(round(l['x']),round(l['y']),round(l['w']),round(l['h'])),round(a['y'])))
        else:
            cand=difflib.get_close_matches(a['t'],list(by.keys()),n=1,cutoff=.55)
            res.append(('TEXT',a['frame'][:12],a['t'][:70],cand[0][:70] if cand else None,'',round(a['y'])))
    return res,med
if __name__=='__main__':
    tag,fig=sys.argv[1],sys.argv[2]; states=sys.argv[3:]
    r,med=run(tag,fig,states); print('offset',med,len(r))
    for x in r: print(x)
