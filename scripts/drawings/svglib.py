"""Minimal SVG builder for sidqui.com's drawings, taken from UBIK's drawing library with a Stone theme and the site's own plate. No dependencies.

Every stroked element gets pathLength="1" and data-draw so the site can animate stroke-dashoffset from 1 to 0.
Groups carry data-system and --d (delay) so systems draw in sequence. Fills, hatches and text are not animated.

Themes: "paper" (ink type, blue strokes, for plates on the page surface) and "navy" (white type, light-blue
strokes, for page headers). A generator builds the same drawing in both and `write()` names the files
`<name>.svg` (paper) and `<name>.navy.svg` (navy); the site picks the navy file when it draws inverse.

Type: three roles from the site's own system. `display` (Schibsted Grotesk: titles, stage names, sheet titles,
figures), `body` (Inter: notes, deliverables, legends, subtitles) and `mono` (JetBrains Mono: eyebrows in
uppercase with 0.14em tracking, numbers, tags, axis figures, ratings). The SVGs are inlined into the page, where
next/font exposes the faces through CSS variables, so every text carries both a font-family attribute and the
variable in its style.

Sizes. Coordinates are viewBox units. Stroke widths and font sizes are DISPLAY pixels: the builder multiplies
them by k = viewBox width / display width (`display_w`). Weight hierarchy: W1 primary systems, W2 secondary,
W3 annotation and leaders, W0 construction (drawn in the line colour), WB bus bars.

Plates. `editorial_plate()` for process diagrams and charts: a top hairline with the eyebrow and a strapline,
the wordmark on a bottom hairline. `drawing_plate()` for true drawings: a reduced title block strip at the
bottom. Navy header drawings are built frameless. Both assert that their strings fit: nothing is truncated.

Dashes. The site's draw-in sets stroke-dasharray on every data-draw element, so a dashed stroke that must
animate is drawn as short segments (`dashed`); a dashed stroke that need not animate carries a fractional
dasharray on pathLength="1" and no data-draw (`dash=` on the primitives).
"""
from __future__ import annotations
import json
import math
import sys
import zlib
from pathlib import Path
from typing import Callable

NAVY = "#071F35"; BLUE = "#248EC8"; BLUE2 = "#63BCEB"; BLUE_INK = "#1B6E9C"; PAPER = "#F6F7F5"
INK = "#0E1B26"; MUTED = "#5B6B76"; LINE = "#D5DEE4"; SIGNAL = "#D7A85B"; WHITE = "#FFFFFF"
FACES = {
    "display": ("'Schibsted Grotesk', sans-serif", "var(--font-display,'Schibsted Grotesk'),sans-serif", 0.56),
    "body": ("'Inter', sans-serif", "var(--font-body,'Inter'),sans-serif", 0.52),
    "mono": ("'JetBrains Mono', monospace", "var(--font-mono,'JetBrains Mono'),monospace", 0.6),
}
MONO = FACES["mono"][0]
STONE_INK = "#171614"; STONE_MUTED = "#6B655C"; STONE_LINE = "#D9D3C8"; STONE_ACCENT = "#9E4522"; STONE_PLATE = "#FAF8F4"; STONE_GROUND = "#F2EFE9"
THEMES = {
    "stone": dict(stroke=STONE_INK, accent=STONE_ACCENT, ink=STONE_INK, muted=STONE_MUTED, faint="#B5AEA3", line=STONE_LINE, grid="rgba(23,22,20,0.05)",
                  fill="rgba(158,69,34,0.10)", fill2="rgba(158,69,34,0.16)", fill_ink="rgba(23,22,20,0.045)",
                  hatch="rgba(107,101,92,0.45)", bg=STONE_PLATE, card="#FFFFFF", card_ghost=STONE_GROUND, edge=STONE_ACCENT, eyebrow=STONE_ACCENT, signal=SIGNAL),
    "paper": dict(stroke=BLUE_INK, accent=BLUE, ink=INK, muted=MUTED, faint="#AFBEC8", line=LINE, grid="rgba(7,31,53,0.06)",
                  fill="rgba(36,142,200,0.10)", fill2="rgba(36,142,200,0.14)", fill_ink="rgba(7,31,53,0.045)",
                  hatch="rgba(27,110,156,0.45)", bg=PAPER, card="#fff", card_ghost=PAPER, edge=BLUE, eyebrow=BLUE_INK, signal=SIGNAL),  # "#fff": the site's test tells paper from navy by the absence of "#FFFFFF"
    "navy":  dict(stroke=BLUE2, accent=WHITE, ink=WHITE, muted="rgba(255,255,255,0.62)", faint="rgba(255,255,255,0.34)", line="rgba(255,255,255,0.14)",
                  grid="rgba(255,255,255,0.06)", fill="rgba(99,188,235,0.12)", fill2="rgba(99,188,235,0.18)", fill_ink="rgba(255,255,255,0.05)",
                  hatch="rgba(99,188,235,0.45)", bg=NAVY, card="rgba(255,255,255,0.06)", card_ghost="rgba(255,255,255,0.025)", edge=BLUE2, eyebrow=BLUE2, signal=SIGNAL),
}
OUT_DIR = Path(__file__).resolve().parents[2] / "public" / "drawings"
SIGNATURE = "Abdelilah Sidqui"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, w: int, h: int, theme: str = "paper", name: str = "drawing", display_w: float | None = None,
                 stroke_w: float | None = None, text_scale: float | None = None):
        """display_w: the width the drawing is shown at, in CSS px; sets k so px sizes hold on the page."""
        self.w, self.h, self.theme, self.t, self.name = w, h, theme, THEMES[theme], name
        self.k = (w / display_w) if display_w else (text_scale or 1.0)
        k = self.k
        self.W0, self.W3, self.W2, self.W1, self.WB = round(0.5 * k, 2), round(0.8 * k, 2), round(1.3 * k, 2), round(2.2 * k, 2), round(4.2 * k, 2)
        self.sw = round((stroke_w or 1.3) * k, 2)
        self.uid = f"d{zlib.crc32((name + theme).encode()):08x}"
        self.parts: list[str] = []
        self._defs: dict[str, str] = {}

    # ---- theme shortcuts
    @property
    def muted(self): return self.t["muted"]
    @property
    def faint(self): return self.t["faint"]
    @property
    def line_c(self): return self.t["line"]
    @property
    def ink(self): return self.t["ink"]
    @property
    def stroke(self): return self.t["stroke"]
    @property
    def accent(self): return self.t["accent"]
    @property
    def bg(self): return self.t["bg"]
    @property
    def eyebrow_c(self): return self.t["eyebrow"]
    @property
    def paper(self): return self.theme == "paper"

    def px(self, n: float) -> float:
        """Display px to viewBox units."""
        return round(n * self.k, 2)

    # ---- defs: patterns with ids unique to this drawing and theme (several drawings share a page)
    def hatch(self, spacing_px: float = 6, angle: int = 45, colour: str | None = None, key: str = "h") -> str:
        hid = f"{self.uid}-{key}"
        if hid not in self._defs:
            sp = self.px(spacing_px)
            self._defs[hid] = (f'<pattern id="{hid}" patternUnits="userSpaceOnUse" width="{sp}" height="{sp}" patternTransform="rotate({angle})">'
                               f'<line x1="0" y1="0" x2="0" y2="{sp}" stroke="{colour or self.t["hatch"]}" stroke-width="{self.W0}"/></pattern>')
        return f"url(#{hid})"

    def dots(self, step_px: float = 16, key: str = "g") -> str:
        hid = f"{self.uid}-{key}"
        if hid not in self._defs:
            sp = self.px(step_px); r = self.px(0.7)
            self._defs[hid] = (f'<pattern id="{hid}" patternUnits="userSpaceOnUse" width="{sp}" height="{sp}">'
                               f'<circle cx="{sp / 2}" cy="{sp / 2}" r="{r}" fill="{self.ink}" fill-opacity="0.03"/></pattern>')
        return f"url(#{hid})"

    # ---- structure
    def group(self, system: str, delay_ms: int):
        self.parts.append(f'<g data-system="{system}" style="--d:{delay_ms}ms">')
        return self

    def end(self):
        self.parts.append("</g>")

    def raw(self, s: str):
        self.parts.append(s)

    # ---- stroked primitives (animated unless dashed)
    def _attrs(self, stroke=None, wd=None, dash=None, length=None, opacity=None):
        s = stroke or self.t["stroke"]; w = wd if wd is not None else self.sw
        op = f' opacity="{opacity}"' if opacity is not None else ""
        if dash and length:
            d, g = dash
            da = f"{self.px(d) / length:.5f} {self.px(g) / length:.5f}"
            return f'stroke="{s}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="{da}"{op}'
        return f'stroke="{s}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" data-draw="1"{op}'

    def line(self, x1, y1, x2, y2, stroke=None, wd=None, dash=None, opacity=None):
        L = math.hypot(x2 - x1, y2 - y1) if dash else None
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {self._attrs(stroke, wd, dash, L, opacity)}/>')

    def hair(self, x1, y1, x2, y2):
        """A construction line in the line colour."""
        self.line(x1, y1, x2, y2, stroke=self.line_c, wd=self.W0)

    def polyline(self, pts, stroke=None, wd=None, dash=None, close=False, opacity=None):
        p = " ".join(f"{x},{y}" for x, y in pts)
        L = None
        if dash:
            q = list(pts) + ([pts[0]] if close else [])
            L = sum(math.hypot(q[i + 1][0] - q[i][0], q[i + 1][1] - q[i][1]) for i in range(len(q) - 1))
        tag = "polygon" if close else "polyline"
        self.parts.append(f'<{tag} points="{p}" {self._attrs(stroke, wd, dash, L, opacity)}/>')

    def path(self, d, stroke=None, wd=None, dash=None, length=None, opacity=None):
        """length: approximate path length in units, needed only with dash."""
        self.parts.append(f'<path d="{d}" {self._attrs(stroke, wd, dash, length, opacity)}/>')

    def rect(self, x, y, w, h, stroke=None, wd=None, dash=None, opacity=None):
        L = 2 * (w + h) if dash else None
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {self._attrs(stroke, wd, dash, L, opacity)}/>')

    def circle(self, cx, cy, r, stroke=None, wd=None, dash=None, opacity=None):
        L = 2 * math.pi * r if dash else None
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" {self._attrs(stroke, wd, dash, L, opacity)}/>')

    def dashed(self, x1, y1, x2, y2, d=5, g=4, stroke=None, wd=None):
        """An animated dashed line: short segments, each drawn in."""
        L = math.hypot(x2 - x1, y2 - y1)
        if L == 0: return
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        dd, gg = self.px(d), self.px(g)
        pos = 0.0
        while pos < L:
            e = min(L, pos + dd)
            self.line(round(x1 + ux * pos, 1), round(y1 + uy * pos, 1), round(x1 + ux * e, 1), round(y1 + uy * e, 1), stroke, wd)
            pos += dd + gg

    # ---- fills (not animated)
    def dot(self, cx, cy, r=3, fill=None):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill or self.t["stroke"]}"/>')

    def fill_rect(self, x, y, w, h, fill=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill or self.t["fill"]}"/>')

    def fill_poly(self, pts, fill=None):
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.parts.append(f'<polygon points="{p}" fill="{fill or self.t["fill"]}"/>')

    def fill_path(self, d, fill=None):
        self.parts.append(f'<path d="{d}" fill="{fill or self.t["fill"]}"/>')

    def fill_circle(self, cx, cy, r, fill=None):
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill or self.t["fill"]}"/>')

    def hatch_rect(self, x, y, w, h, spacing=6, angle=45):
        self.fill_rect(x, y, w, h, fill=self.hatch(spacing, angle))

    def hatch_poly(self, pts, spacing=6, angle=45):
        self.fill_poly(pts, fill=self.hatch(spacing, angle))

    # ---- type: three roles
    def text_w(self, s: str, size: float = 11, spacing: float = 0, role: str = "mono", weight: int = 400) -> float:
        """Approximate advance of a label in units. spacing in units per character."""
        em = FACES[role][2] * (1.06 if weight >= 600 and role != "mono" else 1.0)
        return len(s) * (em * self.px(size) + spacing)

    def text(self, x, y, s, size=11, fill=None, anchor="start", weight=400, upper=False, halo=False, spacing=0.0, role="mono", opacity=None):
        """size in display px; spacing in em. halo draws the theme background behind the label so it reads over strokes."""
        s = s.upper() if upper else s
        fs = self.px(size); sp = round(spacing * fs, 2)
        if isinstance(weight, str): weight = {"normal": 400, "bold": 700}.get(weight, int(weight) if weight.isdigit() else 400)
        if halo:
            w = self.text_w(s, size, sp, role, weight) + self.px(6); hh = fs * 1.25
            lx = x - self.px(3) if anchor == "start" else x - w / 2 if anchor == "middle" else x - w + self.px(3)
            self.parts.append(f'<rect x="{lx:.1f}" y="{y - fs:.1f}" width="{w:.1f}" height="{hh:.1f}" fill="{self.bg}" fill-opacity="0.92"/>')
        attr, var, _ = FACES[role]
        op = f' opacity="{opacity}"' if opacity is not None else ""
        ls = f' letter-spacing="{sp}"' if sp else ""
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{attr}" style="font-family:{var}" font-size="{fs}" font-weight="{weight}" fill="{fill or self.ink}" text-anchor="{anchor}"{ls}{op}>{esc(s)}</text>')

    def eyebrow(self, x, y, s, fill=None, anchor="start", size=11.5, halo=False):
        """Mono, uppercase, 0.14em tracking: the site's section eyebrow."""
        self.text(x, y, s, size=size, fill=fill or self.muted, anchor=anchor, weight=400, upper=True, spacing=0.14, role="mono", halo=halo)

    def mono(self, x, y, s, size=11, fill=None, anchor="start", weight=400, spacing=0.06, halo=False, upper=False):
        self.text(x, y, s, size=size, fill=fill, anchor=anchor, weight=weight, spacing=spacing, role="mono", halo=halo, upper=upper)

    def body(self, x, y, s, size=12.5, fill=None, anchor="start", weight=400, halo=False):
        self.text(x, y, s, size=size, fill=fill, anchor=anchor, weight=weight, role="body", halo=halo)

    def display(self, x, y, s, size=15, fill=None, anchor="start", weight=700, spacing=0.0, halo=False):
        self.text(x, y, s, size=size, fill=fill, anchor=anchor, weight=weight, spacing=spacing, role="display", halo=halo)

    def wordmark(self, x, y, anchor="start", with_mark=False):
        """The author's name where UBIK's drawings carry the wordmark: a 13 px display label."""
        self.display(x, y, SIGNATURE, size=13, weight=700, anchor=anchor)

    def assert_fits(self, s: str, size: float, width: float, where: str, role: str = "mono", spacing: float = 0.0, weight: int = 400):
        """Build-time check: a label that would overflow its cell fails the build instead of being truncated."""
        sp = spacing * self.px(size)
        need = self.text_w(s, size, sp, role, weight)
        if need > width:
            per = need / max(1, len(s))
            raise ValueError(f"{self.name} ({self.theme}): {where} does not fit: {s!r} is {len(s)} characters, "
                             f"the cell takes about {int(width / per)} at {size} px {role}. Shorten the string; do not shrink the type.")

    # ---- plates
    def editorial_plate(self, sheet: str, title: str, strapline: str = "", margin_px: float = 52, delay: int = 0, note: str = "sidqui.com · drawing"):
        """Process diagrams and charts: top hairline with the eyebrow 'Sheet NN / Title' left and a strapline right;
        the wordmark on a bottom hairline. Returns the content box (x0, y0, x1, y1) between the rules."""
        m = self.px(margin_px)
        L, R = m, self.w - m
        ey = self.px(26); ry = self.px(37)
        head = f"Figure {sheet} / {title}"
        sp = 0.14 * self.px(11.5)
        used = self.text_w(strapline.upper(), 11.5, sp) + self.px(32) if strapline else 0
        self.assert_fits(head.upper(), 11.5, (R - L) - used, "plate eyebrow (with the strapline on the same rule)", spacing=0.14)
        self.group("plate", delay)
        self.eyebrow(L, ey, head, fill=self.eyebrow_c)
        if strapline: self.eyebrow(R, ey, strapline, anchor="end")
        self.hair(L, ry, R, ry)
        by = self.h - self.px(39)
        self.hair(L, by, R, by)
        self.wordmark(L, by + self.px(21))
        if note: self.eyebrow(R, by + self.px(21), note, anchor="end")
        self.end()
        self._box = (L, ry + self.px(16), R, by - self.px(14))
        return self._box

    def drawing_plate(self, sheet: str, title: str, subtitle: str, scale: str = "none", scale_label: str = "Scale", margin_px: float = 52, delay: int = 2600, grid: bool = False):
        """True drawings on paper: the reduced title block strip at the bottom. Returns the content box above it."""
        m = self.px(margin_px)
        L, R = m, self.w - m
        ty = self.h - self.px(62)        # the rule above the strip
        tx = L + self.px(110)
        # the sheet cell is right-anchored at R - 150 px; the title and subtitle may run up to its left edge
        sheet_w = max(self.text_w(sheet, 12, 0.12 * self.px(12)), self.text_w("SHEET", 11.5, 0.14 * self.px(11.5)))
        avail = R - self.px(150) - sheet_w - self.px(16) - tx
        self.assert_fits(title, 15, avail, "title block title", role="display", weight=700)
        self.assert_fits(subtitle, 12, avail, "title block subtitle", role="body")
        self.group("title-block", delay)
        self.line(L, ty, R, ty, stroke=self.ink, wd=self.px(1.2))
        self.wordmark(L, ty + self.px(34), with_mark=True)
        self.display(tx, ty + self.px(28), title, size=15, weight=700)
        self.body(tx, ty + self.px(46), subtitle, size=12, fill=self.muted)
        self.mono(R - self.px(150), ty + self.px(28), sheet, size=12, weight=500, spacing=0.12, anchor="end")
        self.eyebrow(R - self.px(150), ty + self.px(46), "Sheet", anchor="end")
        self.mono(R, ty + self.px(28), scale, size=12, weight=500, spacing=0.12, anchor="end")
        self.eyebrow(R, ty + self.px(46), scale_label, anchor="end")
        self.end()
        self._box = (L, self.px(20), R, ty - self.px(16))
        if grid:
            self.parts.insert(0, f'<rect x="{L}" y="{self._box[1]}" width="{R - L}" height="{self._box[3] - self._box[1]}" fill="{self.dots()}"/>')
        return self._box

    def header_box(self, margin_px: float = 12):
        """Navy header drawings: frameless, the whole viewBox less a small margin."""
        m = self.px(margin_px)
        self._box = (m, m, self.w - m, self.h - m)
        return self._box

    # ---- cards and marks
    def card(self, x, y, w, h, ghost=False, edge=True):
        """The site's card: fill, hairline border in the line colour, a 2.5-unit blue left edge."""
        self.fill_rect(x, y, w, h, fill=self.t["card_ghost"] if ghost else self.t["card"])
        self.rect(x, y, w, h, wd=self.W0 * 2, stroke=self.line_c)
        if edge: self.fill_rect(x, y, self.px(2.2), h, fill=self.line_c if ghost else self.t["edge"])

    def legend(self, x, y, items, size=12, gap_px=22, swatch_px=22, cols=1, col_w=None, delay=None, title=None):
        """items: (kind, label[, extra]) with kind 'fill' (extra: fill or pattern), 'line' (extra: dict wd/dash/stroke),
        'sym' (extra: callable(s, cx, cy)). Body text; optional eyebrow title."""
        if delay is not None: self.group("legend", delay)
        sw, g = self.px(swatch_px), self.px(gap_px)
        if title:
            self.eyebrow(x, y, title); y += g
        rows = math.ceil(len(items) / cols)
        cw = col_w or (self.w / cols)
        for i, it in enumerate(items):
            kind, label = it[0], it[1]; extra = it[2] if len(it) > 2 else None
            c, r = divmod(i, rows)
            ix, iy = x + c * cw, y + r * g
            if kind == "fill":
                self.fill_rect(ix, iy - sw * 0.3, sw, sw * 0.55, fill=extra)
                self.rect(ix, iy - sw * 0.3, sw, sw * 0.55, wd=self.W0 * 2, stroke=self.line_c if self.paper else self.faint)
            elif kind == "line":
                e = extra or {}
                if e.get("dash"):
                    self.line(ix, iy, ix + sw, iy, wd=e.get("wd", self.W2), stroke=e.get("stroke"), dash=e["dash"])
                else:
                    self.line(ix, iy, ix + sw, iy, wd=e.get("wd", self.W2), stroke=e.get("stroke"))
            elif kind == "sym":
                extra(self, ix + sw / 2, iy)
            self.body(ix + sw + self.px(10), iy + self.px(4), label, size=size)
        if delay is not None: self.end()

    def dim_h(self, x1, x2, y, label, size=10.5, above=True, stroke=None):
        """Horizontal dimension string with oblique ticks; figure in mono."""
        st = stroke or self.muted; t = self.px(4)
        self.line(x1, y, x2, y, wd=self.W3, stroke=st)
        for x in (x1, x2):
            self.line(x - t, y + t, x + t, y - t, wd=self.W3, stroke=st)
        self.mono((x1 + x2) / 2, y - self.px(5) if above else y + self.px(size) + self.px(4), label, size=size, anchor="middle", fill=self.ink)

    def north_arrow(self, x, y, r_px=18):
        r = self.px(r_px)
        self.circle(x, y, r, wd=self.W3, stroke=self.faint)
        self.fill_poly([(x, y - r * 0.8), (x + r * 0.32, y + r * 0.45), (x, y + r * 0.2)], fill=self.ink)
        self.polyline([(x, y - r * 0.8), (x - r * 0.32, y + r * 0.45), (x, y + r * 0.2)], close=True, wd=self.W3, stroke=self.ink)
        self.mono(x, y + r + self.px(13), "N", size=10.5, anchor="middle", weight=500)

    def scale_bar(self, x, y, unit, segments=4, seg_value=25, unit_label="m", size=10):
        h = self.px(5)
        for i in range(segments):
            x0 = x + i * unit * seg_value
            if i % 2 == 0: self.fill_rect(x0, y - h / 2, unit * seg_value, h, fill=self.ink)
            self.rect(x0, y - h / 2, unit * seg_value, h, wd=self.W0, stroke=self.ink)
            self.mono(x0, y - self.px(8), f"{i * seg_value}", size=size, anchor="middle", fill=self.muted)
        xe = x + segments * unit * seg_value
        self.mono(xe, y - self.px(8), f"{segments * seg_value}", size=size, anchor="middle", fill=self.muted)
        self.mono(xe + self.px(10), y + self.px(4), unit_label, size=size, fill=self.muted)

    def diamond(self, x, y, s, filled=False, stroke=None, wd=None):
        pts = [(x, y - s), (x + s, y), (x, y + s), (x - s, y)]
        self.fill_poly(pts, fill=self.t["fill2"] if filled else self.bg)
        self.polyline(pts, close=True, wd=wd or self.W2, stroke=stroke)

    def circled(self, x, y, label, r_px=10, filled=False, size=10):
        r = self.px(r_px)
        self.fill_circle(x, y, r, fill=self.t["fill2"] if filled else self.bg)
        self.circle(x, y, r, wd=self.W2)
        self.mono(x, y + self.px(size * 0.36), str(label), size=size, anchor="middle", weight=700, spacing=0)

    # ---- IEC-style symbol library: sizes are viewBox units, weights follow the hierarchy
    def breaker(self, x, y, s=12, wd=None, vertical=True):
        w = wd or self.W2
        self.rect(x - s / 2, y - s / 2, s, s, wd=w)
        if vertical: self.line(x - s / 2 + s * 0.2, y + s / 2 - s * 0.2, x + s / 2 - s * 0.2, y - s / 2 + s * 0.2, wd=w)
        else: self.line(x - s / 2 + s * 0.2, y - s / 2 + s * 0.2, x + s / 2 - s * 0.2, y + s / 2 - s * 0.2, wd=w)

    def switch(self, x, y, s=12, wd=None):
        w = wd or self.W2
        self.line(x, y - s, x, y - s * 0.4, wd=w); self.line(x, y + s * 0.4, x, y + s, wd=w)
        self.line(x, y + s * 0.4, x + s * 0.55, y - s * 0.45, wd=w)
        self.dot(x, y + s * 0.4, w * 0.9)

    def transformer(self, cx, cy, r=11, wd=None):
        w = wd or self.W1
        self.circle(cx, cy - r * 0.55, r, wd=w); self.circle(cx, cy + r * 0.55, r, wd=w)

    def genset(self, cx, cy, r=13, wd=None):
        w = wd or self.W1
        self.circle(cx, cy, r, wd=w)
        self.mono(cx, cy + r * 0.3, "G", size=r * 1.05 / self.k, anchor="middle", weight=700, spacing=0)
        self.path(f"M{cx - r * 0.42},{cy + r * 0.62} q{r * 0.21},-{r * 0.3} {r * 0.42},0 q{r * 0.21},{r * 0.3} {r * 0.42},0", wd=self.W3)

    def utility(self, cx, cy, r=13, wd=None):
        w = wd or self.W1
        self.circle(cx, cy, r, wd=w)
        self.path(f"M{cx - r * 0.55},{cy} q{r * 0.27},-{r * 0.55} {r * 0.55},0 q{r * 0.27},{r * 0.55} {r * 0.55},0", wd=w)

    def ups(self, cx, cy, w=56, h=40, wd=None, battery=True):
        ww = wd or self.W1; x0, y0 = cx - w / 2, cy - h / 2
        self.rect(x0, y0, w, h, wd=ww)
        self.line(x0 + w, y0, x0, y0 + h, wd=self.W3)
        a = min(w, h) * 0.16
        self.path(f"M{x0 + w * 0.12},{y0 + h * 0.33} q{a * 0.6},-{a} {a * 1.2},0 q{a * 0.6},{a} {a * 1.2},0", wd=self.W3)
        self.line(x0 + w * 0.56, y0 + h * 0.72, x0 + w * 0.88, y0 + h * 0.72, wd=self.W3)
        self.line(x0 + w * 0.56, y0 + h * 0.82, x0 + w * 0.88, y0 + h * 0.82, wd=self.W3)
        if battery:
            bx = x0 + w + self.px(5)
            self.line(x0 + w, cy, bx + self.px(2), cy, wd=self.W3)
            self.line(bx + self.px(2), cy - self.px(5), bx + self.px(2), cy + self.px(5), wd=self.W2)
            self.line(bx + self.px(5), cy - self.px(2.5), bx + self.px(5), cy + self.px(2.5), wd=self.W2)

    def ats(self, cx, cy, w=48, h=26, wd=None):
        ww = wd or self.W1; x0, y0 = cx - w / 2, cy - h / 2
        self.rect(x0, y0, w, h, wd=ww)
        self.line(cx - w * 0.25, y0 + h * 0.25, cx, y0 + h * 0.72, wd=self.W2)
        self.dot(cx - w * 0.25, y0 + h * 0.25, self.W2 * 0.9); self.dot(cx + w * 0.25, y0 + h * 0.25, self.W2 * 0.9)
        self.line(cx, y0 + h * 0.72, cx, y0 + h, wd=self.W2)

    def chiller(self, x, y, w=44, h=26, wd=None):
        ww = wd or self.W1
        self.rect(x, y, w, h, wd=ww)
        self.circle(x + w * 0.3, y + h / 2, h * 0.28, wd=self.W3)
        self.line(x + w * 0.58, y + h * 0.3, x + w * 0.85, y + h * 0.3, wd=self.W3)
        self.line(x + w * 0.58, y + h * 0.7, x + w * 0.85, y + h * 0.7, wd=self.W3)

    def pump(self, cx, cy, r=9, wd=None, angle=0):
        ww = wd or self.W1
        self.circle(cx, cy, r, wd=ww)
        a = math.radians(angle)
        pts = [(cx + r * 0.85 * math.cos(a), cy + r * 0.85 * math.sin(a)),
               (cx + r * 0.75 * math.cos(a + 2.4), cy + r * 0.75 * math.sin(a + 2.4)),
               (cx + r * 0.75 * math.cos(a - 2.4), cy + r * 0.75 * math.sin(a - 2.4))]
        self.polyline(pts, close=True, wd=self.W3)

    def valve(self, cx, cy, s=7, wd=None, vertical=False, motor=False):
        ww = wd or self.W2
        if vertical: self.polyline([(cx - s, cy - s), (cx + s, cy - s), (cx - s, cy + s), (cx + s, cy + s)], close=True, wd=ww)
        else: self.polyline([(cx - s, cy - s), (cx - s, cy + s), (cx + s, cy - s), (cx + s, cy + s)], close=True, wd=ww)
        if motor:
            self.line(cx, cy, cx, cy - s * 1.6, wd=self.W3)
            self.rect(cx - s * 0.6, cy - s * 2.6, s * 1.2, s, wd=self.W3)
            self.mono(cx, cy - s * 1.85, "M", size=s * 0.9 / self.k, anchor="middle", spacing=0)

    def crah(self, x, y, w=36, h=22, wd=None):
        ww = wd or self.W1
        self.rect(x, y, w, h, wd=ww)
        self.circle(x + w * 0.7, y + h / 2, h * 0.3, wd=self.W3)
        for i in range(3):
            self.line(x + w * 0.12 + i * w * 0.1, y + h * 0.2, x + w * 0.12 + i * w * 0.1, y + h * 0.8, wd=self.W3)

    def rack(self, x, y, w=36, h=56, units=4, wd=None):
        ww = wd or self.W1
        self.rect(x, y, w, h, wd=ww)
        for i in range(1, units + 1):
            self.line(x + w * 0.16, y + i * h / (units + 1), x + w * 0.84, y + i * h / (units + 1), stroke=self.faint, wd=self.W3)

    def battery(self, cx, cy, s=6, wd=None, vertical=False):
        ww = wd or self.W2
        for i, long in enumerate((True, False, True, False)):
            o = -s * 1.5 + i * s; L = s if long else s * 0.5
            if vertical: self.line(cx - L, cy + o, cx + L, cy + o, wd=ww)
            else: self.line(cx + o, cy - L, cx + o, cy + L, wd=ww)

    def earth(self, cx, cy, s=6, wd=None):
        ww = wd or self.W2
        self.line(cx, cy - s, cx, cy, wd=ww)
        for i, f in enumerate((1.0, 0.65, 0.3)):
            self.line(cx - s * f, cy + i * s * 0.45, cx + s * f, cy + i * s * 0.45, wd=ww)

    def busbar(self, x1, x2, y, wd=None, stroke=None):
        self.line(x1, y, x2, y, wd=wd or self.WB, stroke=stroke)

    bus = busbar

    def arrow_head(self, x, y, size=6, dir="right", fill=None):
        """Filled arrow head (not animated), for leaders and axes."""
        s = size
        pts = {"right": [(x, y), (x - s * 1.6, y - s * 0.7), (x - s * 1.6, y + s * 0.7)],
               "left": [(x, y), (x + s * 1.6, y - s * 0.7), (x + s * 1.6, y + s * 0.7)],
               "down": [(x, y), (x - s * 0.7, y - s * 1.6), (x + s * 0.7, y - s * 1.6)],
               "up": [(x, y), (x - s * 0.7, y + s * 1.6), (x + s * 0.7, y + s * 1.6)]}[dir]
        self.fill_poly(pts, fill=fill or self.t["stroke"])

    def open_arrow(self, x, y, size=5, dir="right", stroke=None, wd=None):
        """Open arrow head (animated), as on the mock's path."""
        s = size
        d = {"right": f"M{x - s * 1.6},{y - s} L{x},{y} L{x - s * 1.6},{y + s}", "down": f"M{x - s},{y - s * 1.6} L{x},{y} L{x + s},{y - s * 1.6}",
             "up": f"M{x - s},{y + s * 1.6} L{x},{y} L{x + s},{y + s * 1.6}", "left": f"M{x + s * 1.6},{y - s} L{x},{y} L{x + s * 1.6},{y + s}"}[dir]
        self.path(d, stroke=stroke, wd=wd or self.W2)

    # ---- output
    def write(self, name: str, title: str, provenance: str):
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        tid = f"d{zlib.crc32(name.encode()):08x}"  # stable, unique per drawing, carries no name
        defs = f"<defs>{''.join(self._defs.values())}</defs>" if self._defs else ""
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="{tid}">'
               f'<title id="{tid}">{esc(title)}</title>{defs}' + "".join(self.parts) + "</svg>")
        if "…" in svg:
            raise ValueError(f"{name} ({self.theme}): an ellipsis reached the output; no label may be truncated")
        file = f"{name}.svg"
        for attempt in range(3):
            try:
                (OUT_DIR / file).write_text(svg, encoding="utf-8")
                (OUT_DIR / f"{name}.json").write_text(json.dumps({"title": title, "provenance": provenance}, indent=2), encoding="utf-8")
                break
            except OSError:
                if attempt == 2: raise
        print(f"wrote {file} ({len(svg)} bytes)")


def both(build: Callable[[str], None]):
    """Build a drawing in the site's one theme."""
    build("stone")
