import json, sys, re
B='/Users/yeahmobi/Desktop/SolaStyle_详情页第一轮走查_20261116/全量重走_20261117/careful/'
def hexc(c,op=1):
    if not c: return ''
    return '#%02X%02X%02X'%tuple(round(c[k]*255) for k in 'rgb')+('' if op>=0.99 else '@%.2f'%op)
def flat(path):
    d=json.load(open(B+'figma/'+path)); out=[]
    for nid,v in d['nodes'].items():
        doc=v['document']; ox=doc['absoluteBoundingBox']['x']; oy=doc['absoluteBoundingBox']['y']
        def walk(n,path,vis):
            if n.get('visible') is False: return
            ab=n.get('absoluteBoundingBox')
            rec=None
            if ab:
                x,y,w,h=ab['x']-ox,ab['y']-oy,ab['width'],ab['height']
                if n['type']=='TEXT':
                    st=n.get('style',{}); fills=[f for f in n.get('fills',[]) if f.get('visible',True)]
                    col=hexc(fills[0]['color'],fills[0].get('opacity',1)*fills[0]['color'].get('a',1)) if fills else ''
                    out.append(dict(k='text',frame=doc['name'],t=re.sub(r'\s+',' ',n.get('characters','')).strip(),x=x,y=y,w=w,h=h,fs=st.get('fontSize'),fw=st.get('fontWeight'),col=col,ff=st.get('fontFamily'),td=st.get('textDecoration',''),path=path))
                else:
                    strokes=[s for s in n.get('strokes',[]) if s.get('visible',True)]
                    fills=[f for f in n.get('fills',[]) if f.get('visible',True) and f['type']=='SOLID']
                    eff=[e for e in n.get('effects',[]) if e.get('visible',True)]
                    r=n.get('cornerRadius',0) or max(n.get('rectangleCornerRadii',[0]) or [0])
                    if (strokes or r or eff or fills) and w>=16 and h>=16 and n['type'] not in ('VECTOR','BOOLEAN_OPERATION','LINE','ELLIPSE') :
                        out.append(dict(k='box',frame=doc['name'],name=n['name'],x=x,y=y,w=w,h=h,rad=r,stroke=(hexc(strokes[0]['color'],strokes[0].get('opacity',1))+' %spx'%n.get('strokeWeight') if strokes else ''),fill=(hexc(fills[0]['color'],fills[0].get('opacity',1)) if fills else ''),eff=[e['type'] for e in eff],path=path))
            for c in n.get('children',[]): walk(c,path+'/'+n['name'][:14],vis)
        walk(doc,'',True)
    return out
if __name__=='__main__':
    for f in ['pc-intro.json','pc-story-modules.json','pc-warranty.json','m-detail.json']:
        o=flat(f); print(f,len(o),sum(1 for a in o if a['k']=='text'))
