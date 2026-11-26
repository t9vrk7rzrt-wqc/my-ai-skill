#!/usr/bin/env python3
"""按模块生成“设计稿 / 线上”同倍率合并标注图（红框 + 编号 + 图例）。

硬规则：
- 中文标签必须用可渲染 CJK 的字体（禁止 load_default，禁止先试会失败的 PingFang）
- 标注图要够清晰：默认更高输出宽度；图例与标题禁止出现方框乱码
"""
import sys
from PIL import Image, ImageDraw, ImageFont

RED, BLUE = (230, 0, 0), (30, 110, 220)

_FONT_CANDIDATES = (
    '/Library/Fonts/Arial Unicode.ttf',
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
)


def font(sz):
    for p in _FONT_CANDIDATES:
        try:
            if p.endswith('.ttc'):
                return ImageFont.truetype(p, sz, index=0)
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    raise RuntimeError('无可用中文字体，拒绝生成会乱码的标注图')


def union(boxes, pad, W, H):
    x0 = min(b[0] for b in boxes) - pad
    y0 = min(b[1] for b in boxes) - pad
    x1 = max(b[0] + b[2] for b in boxes) + pad
    y1 = max(b[1] + b[3] for b in boxes) + pad
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    return int(x0), int(y0), int(x1 - x0), int(y1 - y0)


def tag(d, x, y, n, r=12):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    d.text((x, y), str(n), fill='white', font=font(15), anchor='mm')


def module_image(fig_png, live_png, fig_y, live_y, fig_h, live_h, items, out,
                 maxw=1600, pad=40, minw=640, labels=('Figma 设计稿', '线上实现')):
    fig, live = Image.open(fig_png).convert('RGB'), Image.open(live_png).convert('RGB')
    W = fig.width
    fb = union([b for it in items for b in it['fm']] + [(x, y, 60, 20) for it in items for x, y, _ in it.get('ftxt', [])], pad, W, fig_h)
    lb = union([b for it in items for b in it['lm']] + [(x, y, 60, 20) for it in items for x, y, _ in it.get('ltxt', [])], pad, live.width, live_h)
    sc = min(2.2 if W < 600 else 2.0, maxw / max(fb[2], lb[2], minw))
    crops = []
    for im, box, oy, key, tk in ((fig, fb, fig_y, 'fm', 'ftxt'), (live, lb, live_y, 'lm', 'ltxt')):
        c = im.crop((box[0], oy + box[1], box[0] + box[2], oy + box[1] + box[3]))
        c = c.resize((int(box[2] * sc), int(box[3] * sc)), Image.LANCZOS)
        d = ImageDraw.Draw(c)
        for it in items:
            for x, y, t in it.get(tk, []):
                d.text(((x - box[0]) * sc, (y - box[1]) * sc), t, fill=RED, font=font(max(16, int(16 * sc))))
            for i, (x, y, w, h) in enumerate(it[key]):
                x0, y0 = (x - box[0]) * sc, (y - box[1]) * sc
                d.rectangle([x0 - 3, y0 - 3, x0 + w * sc + 3, y0 + h * sc + 3], outline=RED, width=3)
                if i == 0 or len(it[key]) <= 3:
                    tag(d, max(12, x0 - 3), max(12, y0 - 3), it['n'])
        crops.append(c)
    Wd = max(crops[0].width, crops[1].width, 640)
    lf, probe, lines = font(20), ImageDraw.Draw(Image.new('RGB', (10, 10))), []
    for it in items:
        cur = ''
        for ch in f"{it['n']}  {it['legend']}":
            if probe.textlength(cur + ch, font=lf) > Wd - 24:
                lines.append(cur); cur = '    '
            cur += ch
        lines.append(cur)
    lab_h, gap = 34, 12
    H = lab_h + crops[0].height + gap + lab_h + crops[1].height + 24 + 32 * len(lines) + 12
    canvas = Image.new('RGB', (Wd, H), 'white')
    d = ImageDraw.Draw(canvas)
    y = 0
    for c, lb_, col in ((crops[0], labels[0], RED), (crops[1], labels[1], BLUE)):
        d.text((10, y + 4), lb_, fill=col, font=font(22)); y += lab_h
        canvas.paste(c, (0, y)); y += c.height + gap
    y += 8
    for ln in lines:
        d.text((10, y), ln, fill=(40, 40, 40), font=lf); y += 32
    # PNG 无损，避免 JPEG 再压糊
    if out.lower().endswith(('.jpg', '.jpeg')):
        out = out.rsplit('.', 1)[0] + '.png'
    canvas.save(out, optimize=True)
    return out


def blur_pair(fig_png, live_png, fy, fx, fw, fh, ly, lx, lw, lh, out, zoom=2.8,
              legend='线上配图和设计稿相比同位置过于模糊，需替换高清图'):
    """上设计稿清晰 / 下线上发糊 — 局部放大对比；中文必须可读。"""
    fig, live = Image.open(fig_png).convert('RGB'), Image.open(live_png).convert('RGB')
    fc = fig.crop((fx, fy, fx + fw, fy + fh)).resize((int(fw * zoom), int(fh * zoom)), Image.LANCZOS)
    lc = live.crop((lx, ly, lx + lw, ly + lh)).resize((int(lw * zoom), int(lh * zoom)), Image.LANCZOS)
    W = max(fc.width, lc.width, 720)
    gap, lab = 10, 32
    H = lab + fc.height + gap + lab + lc.height + 72
    canvas = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(canvas)
    y = 0
    for c, labt, col in ((fc, 'Figma 设计稿（清晰）', RED), (lc, '线上实现（发糊）', BLUE)):
        d.text((10, y + 4), labt, fill=col, font=font(20)); y += lab
        canvas.paste(c, (0, y)); y += c.height + gap
    d.ellipse([10, y + 6, 32, y + 28], fill=RED)
    d.text((21, y + 17), '1', fill='white', font=font(14), anchor='mm')
    d.text((40, y + 6), legend, fill=(40, 40, 40), font=font(18))
    if out.lower().endswith(('.jpg', '.jpeg')):
        out = out.rsplit('.', 1)[0] + '.png'
    canvas.save(out, optimize=True)
    return out


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        a = Image.new('RGB', (800, 600), (240, 240, 240)); b = Image.new('RGB', (800, 600), (250, 250, 250))
        for im in (a, b):
            ImageDraw.Draw(im).rectangle([100, 100, 300, 200], fill=(180, 180, 180))
        a.save('/tmp/_fig.png'); b.save('/tmp/_live.png')
        module_image('/tmp/_fig.png', '/tmp/_live.png', 0, 0, 600, 600,
                     [dict(n=1, fm=[(100, 100, 200, 100)], lm=[(100, 100, 200, 100)], legend='中文图例测试：设计稿清晰')],
                     '/tmp/_ann_selftest.png')
        print('wrote /tmp/_ann_selftest.png')
