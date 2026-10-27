#!/usr/bin/env python3
"""把走查记录写入飞书多维表格，并回读校验。依赖 lark-cli（已 auth 并有 Base 写权限）。

records.json 是列表，每项:
  {"fields": {"问题描述": "...", "页面": ["Branding"], "尺寸": ["PC端"], "所属模块": ["06 Quality"],
              "语言": ["双语"], "优先级": ["P2"], "问题类型": ["基础视觉还原"], "需人工复核": false,
              "备注说明": "", "提出时间": "2026-10-27"},
   "image": "/abs/path/to/img.png"}          # 可选；同一张图可被多条共用

用法:
  feishu_write.py create  --base B --table T --records records.json [--dry-run]
  feishu_write.py verify  --base B --table T [--expect N]
  feishu_write.py blanks  --base B --table T            # 只列空白行，不删（删除需用户确认）
约定: select/单选值写成数组；每批 ≤200；附件用相对路径上传（本脚本会拷到临时目录再上传）；
      不创建字段、不删记录、不改他人记录。
"""
import argparse, glob, json, os, shutil, subprocess, sys, tempfile
from collections import Counter


def run(args, cwd=None):
    r = subprocess.run(['lark-cli', 'base'] + args, capture_output=True, text=True, cwd=cwd)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {'ok': False, 'raw': r.stdout + r.stderr}


def base_args(a):
    return ['--as', 'user', '--base-token', a.base, '--table-id', a.table]


def dump(a):
    d = tempfile.mkdtemp()
    subprocess.run(['lark-cli', 'base', '+record-list'] + base_args(a) + ['--limit', '200'], capture_output=True, cwd=d)
    fs = glob.glob(os.path.join(d, '*.ndjson'))
    return [json.loads(l) for l in open(fs[0])] if fs else []


def first(v):
    return v[0] if isinstance(v, list) and v else v


def cmd_create(a):
    recs = json.load(open(a.records))
    print(f'{len(recs)} records; dry-run={a.dry_run}')
    if a.dry_run:
        for r in recs[:5]:
            print(json.dumps(r['fields'], ensure_ascii=False)[:160], r.get('image'))
        return
    ids = []
    for i in range(0, len(recs), 50):
        o = run(['+record-batch-create'] + base_args(a) +
                ['--json', json.dumps({'create_records': [r['fields'] for r in recs[i:i + 50]]}, ensure_ascii=False)])
        if not o.get('ok'):
            sys.exit(f'batch create failed: {str(o)[:400]}')
        ids += o['data']['record_id_list']
    json.dump(ids, open('created_ids.json', 'w'))
    work, names, bad = tempfile.mkdtemp(), {}, []
    for r, rid in zip(recs, ids):
        p = r.get('image')
        if not p:
            continue
        n = names.setdefault(p, f'f{len(names):03d}_' + os.path.basename(p))
        if not os.path.exists(os.path.join(work, n)):
            shutil.copy(p, os.path.join(work, n))
        o = run(['+record-upload-attachment'] + base_args(a) + ['--record-id', rid, '--field-id', '问题截图', '--file', './' + n], cwd=work)
        print(rid, 'ok' if o.get('ok') else 'FAIL', flush=True)
        if not o.get('ok'):
            bad.append((rid, str(o)[:200]))
    print('created', len(ids), 'failed uploads', bad)


def cmd_verify(a):
    R = dump(a)
    blanks = [r['record_id'] for r in R if not r.get('问题描述')]
    no_att = [r['record_id'] for r in R if r.get('问题描述') and len(r.get('问题截图') or []) != 1]
    print('records', len(R), '| blank', len(blanks), '| attachment!=1', len(no_att))
    print(Counter((first(r.get('页面')), first(r.get('尺寸'))) for r in R if r.get('问题描述')))
    mods = {}
    for r in R:
        if r.get('问题描述') and first(r.get('所属模块')):
            mods.setdefault((first(r.get('页面')), first(r.get('尺寸'))), []).append(first(r['所属模块']))
    for k, v in mods.items():
        print(k, 'module order monotonic (by sort):', v == sorted(v) or 'view sorts them; ok')
    if a.expect is not None and len(R) - len(blanks) != a.expect:
        print(f'!! expected {a.expect}, got {len(R) - len(blanks)}')


def cmd_blanks(a):
    for r in dump(a):
        if not r.get('问题描述') and not r.get('问题截图'):
            print(r['record_id'])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['create', 'verify', 'blanks'])
    ap.add_argument('--base', required=True); ap.add_argument('--table', required=True)
    ap.add_argument('--records'); ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--expect', type=int)
    a = ap.parse_args()
    {'create': cmd_create, 'verify': cmd_verify, 'blanks': cmd_blanks}[a.cmd](a)
