#!/usr/bin/env python3
"""按模块生成“设计稿 / 线上”同倍率合并标注图（红框 + 编号 + 图例）。

作为库使用:
    from annotate import module_image
    module_image(
        fig_png='figma_pc.png', live_png='live_pc.png',
        fig_y=2695, live_y=2599,                 # 该模块在各自整页图里的起始 y
        fig_h=468, live_h=364,                   # 模块高度（裁切上限）
        items=[dict(n=1,
                    fm=[(x,y,w,h)], lm=[(x,y,w,h)],            # 相对模块左上角的框；第一个框带编号
                    ftxt=[(x,y,'16')], ltxt=[(x,y,'24')],      # 可选：在图上写的数值
                    legend='副标题颜色：设计稿 …；线上 …')],
        out='img/pc-certified.png')

约定：框的坐标是“模块相对坐标”；设计稿与线上用同一个缩放比例；多框的同一问题只在第一个框上放编号。
命令行自测: python3 annotate.py --selftest
"""
import sys
from PIL import Image, ImageDraw, ImageFont

RED, BLUE = (230, 0, 0), (30, 110, 220)


def font(sz):
    for p in ('/System/Library/Fonts/PingFang.ttc', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
              '/Library/Fonts/Arial Unicode.ttf'):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def union(boxes, pad, W, H):
    x0 = min(b[0] for b in boxes) - pad
    y0 = min(b[1] for b in boxes) - pad
    x1 = max(b[0] + b[2] for b in boxes) + pad
    y1 = max(b[1] + b[3] for b in boxes) + pad
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    return int(x0), int(y0), int(x1 - x0), int(y1 - y0)


def tag(d, x, y, n, r=11):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    d.text((x, y), str(n), fill='white', font=font(14), anchor='mm')


def module_image(fig_png, live_png, fig_y, live_y, fig_h, live_h, items, out,
                 maxw=1200, pad=36, minw=520, labels=('Figma 设计稿', '线上实现')):
    fig, live = Image.open(fig_png).convert('RGB'), Image.open(live_png).convert('RGB')
    W = fig.width
    fb = union([b for it in items for b in it['fm']] + [(x, y, 60, 20) for it in items for x, y, _ in it.get('ftxt', [])], pad, W, fig_h)
    lb = union([b for it in items for b in it['lm']] + [(x, y, 60, 20) for it in items for x, y, _ in it.get('ltxt', [])], pad, live.width, live_h)
    sc = min(2.0 if W < 600 else 1.8, maxw / max(fb[2], lb[2], minw))
    crops = []
    for im, box, oy, key, tk in ((fig, fb, fig_y, 'fm', 'ftxt'), (live, lb, live_y, 'lm', 'ltxt')):
        c = im.crop((box[0], oy + box[1], box[0] + box[2], oy + box[1] + box[3]))
        c = c.resize((int(box[2] * sc), int(box[3] * sc)), Image.LANCZOS)
        d = ImageDraw.Draw(c)
        for it in items:
            for x, y, t in it.get(tk, []):
                d.text(((x - box[0]) * sc, (y - box[1]) * sc), t, fill=RED, font=font(max(14, int(15 * sc))))
            for i, (x, y, w, h) in enumerate(it[key]):
                x0, y0 = (x - box[0]) * sc, (y - box[1]) * sc
                d.rectangle([x0 - 3, y0 - 3, x0 + w * sc + 3, y0 + h * sc + 3], outline=RED, width=3)
                if i == 0 or len(it[key]) <= 3:
                    tag(d, max(11, x0 - 3), max(11, y0 - 3), it['n'])
        crops.append(c)
    # 图例自动换行
    Wd = max(crops[0].width, crops[1].width, 560)
    lf, probe, lines = font(18), ImageDraw.Draw(Image.new('RGB', (10, 10))), []
    for it in items:
        cur = ''
        for ch in f"{it['n']}  {it['legend']}":
            if probe.textlength(cur + ch, font=lf) > Wd - 20:
                lines.append(cur); cur = '    '
            cur += ch
        lines.append(cur)
    lab_h, gap = 30, 10
    H = lab_h + crops[0].height + gap + lab_h + crops[1].height + 20 + 28 * len(lines) + 10
    canvas = Image.new('RGB', (Wd, H), 'white')
    d = ImageDraw.Draw(canvas)
    y = 0
    for c, lb_, col in ((crops[0], labels[0], RED), (crops[1], labels[1], BLUE)):
        d.text((8, y + 2), lb_, fill=col, font=font(20)); y += lab_h
        canvas.paste(c, (0, y)); y += c.height + gap
    y += 10
    for ln in lines:
        d.text((8, y), ln, fill=(40, 40, 40), font=lf); y += 28
    canvas.save(out)
    return out


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        a = Image.new('RGB', (800, 600), (240, 240, 240)); b = Image.new('RGB', (800, 600), (250, 250, 250))
        for im in (a, b):
            ImageDraw.Draw(im).rectangle([100, 100, 300, 200], fill=(180, 180, 180))
        a.save('/tmp/_fig.png'); b.save('/tmp/_live.png')
        module_image('/tmp/_fig.png', '/tmp/_live.png', 0, 0, 600, 600,
                     [dict(n=1, fm=[(100, 100, 200, 100)], lm=[(100, 100, 200, 100)], ftxt=[(180, 76, '16')], ltxt=[(180, 76, '24')],
                           legend='示例：卡片间距 设计稿 16px，线上 24px')], '/tmp/_ann.png')
        print('selftest ok -> /tmp/_ann.png')
