import json,subprocess,shutil,os,tempfile
BASE='UVq0bjt7FaN0IysckYyckrnrnFh'; TBL='tblHOe0vEjMHsX52'
def run(args,cwd=None):
    r=subprocess.run(['lark-cli','base']+args+['--as','user','--base-token',BASE,'--table-id',TBL],capture_output=True,text=True,cwd=cwd)
    try: return json.loads(r.stdout)
    except: return {'ok':False,'raw':r.stdout+r.stderr}
def full(sfx):
    for l in open('/tmp/pdp-r3.ndjson'):
        r=json.loads(l)
        if r['record_id'].endswith(sfx): return r['record_id']
def cur(rid):
    o=run(['+record-get','--record-id',rid]); return o
def upd(rid,fields):
    p='/tmp/_upd.json'; json.dump({'update_records':{rid:fields}},open(p,'w'),ensure_ascii=False)
    return run(['+record-batch-update','--json','@'+p]) if False else run(['+record-batch-update','--json',open(p).read()])
def up(rid,path,name):
    d='/tmp/up'; os.makedirs(d,exist_ok=True); n=name; shutil.copy(path,f'{d}/{n}')
    return run(['+record-upload-attachment','--record-id',rid,'--field-id','问题截图','--file','./'+n],cwd=d)
def rm_all(rid,tokens):
    if not tokens: return
    args=['+record-remove-attachment','--record-id',rid,'--field-id','问题截图','--yes']
    for t in tokens: args+=['--file-token',t]
    return run(args)
def create(fields):
    p=json.dumps({'create_records':[fields]},ensure_ascii=False)
    o=run(['+record-batch-create','--json',p]); return o
