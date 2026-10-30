#!/usr/bin/env python3
"""Read-only image integrity and exact same-canvas protected-region checks.

Requires Pillow. Writes JSON only; does not alter images or certify visual quality.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def box_arg(value):
    try:
        coords = tuple(int(part) for part in value.split(','))
        if len(coords) != 4 or min(coords) < 0 or coords[0] >= coords[2] or coords[1] >= coords[3]:
            raise ValueError()
        return coords
    except ValueError:
        raise argparse.ArgumentTypeError('Use x0,y0,x1,y1 with nonnegative, nonempty bounds')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--result', required=True)
    parser.add_argument('--allowed-mask')
    parser.add_argument('--protected-box', action='append', default=[], type=box_arg)
    parser.add_argument('--require-alpha', action='store_true')
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    report_path = Path(args.report).expanduser().resolve()
    inputs = [Path(v).expanduser().resolve() for v in (args.source, args.result, args.allowed_mask) if v]
    if report_path in inputs:
        parser.error('Report path must not overwrite an input image')
    try:
        from PIL import Image, ImageChops

        def read(path):
            original_hash = sha256(path)
            with Image.open(path) as im:
                im.load()
                icc = im.info.get('icc_profile')
                meta = dict(path=str(Path(path).resolve()), sha256=original_hash,
                            width=im.width, height=im.height, format=im.format,
                            mode=im.mode, frames=getattr(im, 'n_frames', 1),
                            exif_orientation=im.getexif().get(274),
                            icc_sha256=hashlib.sha256(icc).hexdigest() if icc else None,
                            has_alpha_channel=('A' in im.getbands() or 'transparency' in im.info))
                rgba = im.convert('RGBA')
            if original_hash != sha256(path):
                raise ValueError('Input changed while reading: ' + str(path))
            meta['alpha_extrema'] = list(rgba.getchannel('A').getextrema())
            meta['has_transparent_pixels'] = meta['alpha_extrema'][0] < 255
            return rgba, meta

        before, bm = read(args.source)
        after, am = read(args.result)
        failures = []
        report = {'schema_version': 1, 'source': bm, 'result': am,
                  'scope': 'requested technical checks only; no visual or user acceptance',
                  'comparison': 'normalized decoded 8-bit RGBA, exact channel equality; no resizing or ICC transform',
                  'failures': failures, 'warnings': []}
        for label, meta in (('source', bm), ('result', am)):
            if meta['frames'] != 1:
                failures.append(label + ': multi-frame input requires an explicit frame policy')
            if meta['exif_orientation'] not in (None, 1):
                failures.append(label + ': non-default EXIF orientation requires coordinate review')
            if meta['mode'] not in ('RGB', 'RGBA', 'L', 'LA', 'P', '1'):
                failures.append(label + ': exact native-channel validation unsupported for mode ' + meta['mode'])
        if bm['icc_sha256'] != am['icc_sha256']:
            failures.append('ICC profiles differ; display interpretation may change')
        if args.require_alpha and not (am['has_alpha_channel'] and am['has_transparent_pixels']):
            failures.append('Result does not contain actual transparent pixels')
        if bm['has_transparent_pixels'] and not am['has_transparent_pixels']:
            report['warnings'].append('Source transparency was lost; verify task authorization')
        if before.size != after.size:
            failures.append('Canvas dimensions differ; same-coordinate comparison refused')
            report['same_canvas'] = False
        else:
            report['same_canvas'] = True

            def union(bands):
                out = bands[0]
                for band in bands[1:]:
                    out = ImageChops.lighter(out, band)
                return out.point(lambda x: 255 if x else 0)

            def count(mask):
                return mask.histogram()[255]

            diff = ImageChops.difference(before, after)
            bands = diff.split()
            rgb = union(bands[:3])
            alpha = union(bands[3:])
            rgba = union(bands)
            visible = ImageChops.multiply(rgba, union([before.getchannel('A'), after.getchannel('A')]))
            report['diff'] = dict(changed_rgb_pixels=count(rgb), changed_alpha_pixels=count(alpha),
                                  changed_rgba_pixels=count(rgba), changed_visible_pixels=count(visible),
                                  changed_bbox=rgba.getbbox())
            if args.allowed_mask:
                mh = sha256(args.allowed_mask)
                with Image.open(args.allowed_mask) as raw:
                    raw.load()
                    if raw.format != 'PNG' or raw.mode != 'L' or raw.size != before.size:
                        raise ValueError('Allowed mask must be a same-size, single-channel L-mode PNG')
                    allowed = raw.point(lambda x: 255 if x else 0)
                if mh != sha256(args.allowed_mask):
                    raise ValueError('Allowed mask changed while reading')
                outside = ImageChops.multiply(rgba, ImageChops.invert(allowed))
                report['mask'] = dict(path=str(Path(args.allowed_mask).resolve()), sha256=mh,
                                      allowed_pixels=count(allowed), outside_changed_pixels=count(outside),
                                      outside_changed_bbox=outside.getbbox())
                if count(allowed) == before.width * before.height:
                    report['warnings'].append('Mask allows the whole canvas; no protected outside area exists')
                if count(outside):
                    failures.append('Changes exist outside the allowed mask')
            else:
                report['warnings'].append('No allowed mask: outside-region preservation was not assessed')
            report['protected_boxes'] = []
            for box in args.protected_box:
                if box[2] > before.width or box[3] > before.height:
                    raise ValueError('Protected box exceeds image bounds: ' + str(box))
                changes = count(rgba.crop(box))
                report['protected_boxes'].append(dict(box=box, changed_pixels=changes))
                if changes:
                    failures.append('Protected box changed: ' + str(box))
        # Recheck hashes after all calculations: an active other task may rewrite a source.
        for meta in (bm, am):
            if sha256(meta['path']) != meta['sha256']:
                failures.append('Input changed during verification: ' + meta['path'])
        report['passed_requested_checks'] = not failures
        status = 0 if not failures else 2
    except Exception as exc:
        report = {'schema_version': 1, 'passed_requested_checks': False,
                  'error': type(exc).__name__ + ': ' + str(exc)}
        status = 1
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'report': str(report_path), 'passed_requested_checks': report['passed_requested_checks'],
                      'exit_code': status}, ensure_ascii=False))
    return status


if __name__ == '__main__':
    sys.exit(main())
