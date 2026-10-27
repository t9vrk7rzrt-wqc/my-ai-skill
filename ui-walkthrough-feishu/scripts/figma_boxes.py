#!/usr/bin/env python3
"""读取 Figma REST /nodes JSON，输出相对根画板的文字与容器框（自动跳过不可见祖先）。

用法:
  figma_boxes.py nodes.json --y 2695 3163                # 只看 y 区间（相对根画板）
  figma_boxes.py nodes.json --y 2695 3163 --types TEXT   # 只要文字
  figma_boxes.py nodes.json --name 卡片                   # 按名称包含过滤
  figma_boxes.py nodes.json --text "^LONGi products"      # 按文字内容正则过滤
  figma_boxes.py nodes.json --y 0 99999 --include-hidden # 连隐藏节点一起看（会标 hidden）

输出每行: 类型 | 名称/文字 | x y w h (相对根，y 同时给相对区间起点) | 字号/字重/字距/行高/颜色 或 圆角
"""
import argparse, json, re, sys


def hexcolor(c, op=None):
    h = '#%02X%02X%02X' % tuple(round(c[k] * 255) for k in 'rgb')
    a = c.get('a', 1)
    if op is not None:
        a *= op
    return h if a >= 0.999 else f'{h}@{a:.2f}'


def load_root(path):
    d = json.load(open(path))
    if 'nodes' in d:
        return list(d['nodes'].values())[0]['document']
    return d.get('document', d)


def walk(n, vis, out, include_hidden):
    v = vis and n.get('visible', True)
    if v or include_hidden:
        out.append((n, v))
    for c in n.get('children') or []:
        walk(c, v, out, include_hidden)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--y', nargs=2, type=float, default=[-1e9, 1e9])
    ap.add_argument('--types', default='TEXT,FRAME,RECTANGLE,INSTANCE,COMPONENT,GROUP')
    ap.add_argument('--name')
    ap.add_argument('--text')
    ap.add_argument('--max-w', type=float, default=1e9)
    ap.add_argument('--include-hidden', action='store_true')
    a = ap.parse_args()

    root = load_root(a.file)
    rb = root['absoluteBoundingBox']
    ox, oy = rb['x'], rb['y']
    nodes = []
    walk(root, True, nodes, a.include_hidden)
    types = set(a.types.split(','))
    y0 = a.y[0]
    for n, vis in nodes:
        bb = n.get('absoluteBoundingBox')
        if not bb or n['type'] not in types:
            continue
        x, y, w, h = bb['x'] - ox, bb['y'] - oy, bb['width'], bb['height']
        if not (a.y[0] <= y <= a.y[1]) or w > a.max_w:
            continue
        if a.name and a.name not in n['name']:
            continue
        if a.text and not (n['type'] == 'TEXT' and re.search(a.text, n.get('characters', ''))):
            continue
        tag = '' if vis else ' [hidden]'
        if n['type'] == 'TEXT':
            s = n.get('style', {})
            fills = [f for f in n.get('fills', []) if f.get('visible', True) and f.get('type') == 'SOLID']
            col = hexcolor(fills[0]['color'], fills[0].get('opacity')) if fills else '-'
            if n.get('opacity') is not None:
                col += f' node-opacity={n["opacity"]:.2f}'
            info = (f'{s.get("fontSize")}px/{s.get("fontWeight")} ls={s.get("letterSpacing", 0):.2f} '
                    f'lh={s.get("lineHeightPx", 0):.1f} {col} {s.get("fontFamily")}')
            label = n.get('characters', '')[:48].replace('\n', ' ')
        else:
            info = f'r={n.get("cornerRadius")}' if n.get('cornerRadius') else ''
            label = n['name'][:40]
        print(f'{n["type"][:5]:5} | {label} | x={x:.1f} y={y:.1f} (+{y - y0:.1f}) w={w:.1f} h={h:.1f} | {info}{tag}')


if __name__ == '__main__':
    sys.exit(main())
