"""Figure for the note on converted mining sites: from the grid number to the IT number. A 100 MW connection feeds
the cooling plant and the losses first, then the redundant distribution, and reaches the racks as about 65 MW of IT.
Editorial plate, stone theme."""
from svglib import SVG, both

DW = 824
CONTENT = 296
W = 1400
H = round((CONTENT + 106) * W / DW)

BARS = [  # label, MW of 100, value label, two lines of explanation
    ("At the fence", 100, "100 MW",
     ("The grid connection: the number", "in the announcement and the price")),
    ("After the cooling plant and losses", 80, "about 80 MW",
     ("Chillers, pumps, fans, dry coolers and", "the losses in distribution take a share")),
    ("After redundancy", 65, "about 65 MW of IT",
     ("The lines carry each other’s load,", "so a share of their rating is held back")),
]


def build(theme="stone"):
    s = SVG(W, H, theme, name="grid-number", display_w=DW)
    L0, y0, R0, y1 = s.editorial_plate("04", "The grid number and the IT number", "A converted mining site, typical")
    X = lambda v: L0 + s.px(v)
    P = lambda v: y0 + s.px(v)
    BX0, BX1, BH = 324, 720, 26
    scale = (BX1 - BX0) / 100
    for i, (label, mw, value, lines) in enumerate(BARS):
        y = 20 + i * 84
        s.group(f"bar-{i + 1}", 300 + 500 * i)
        s.eyebrow(X(0), P(y + 8), f"0{i + 1}", size=10)
        s.assert_fits(label, 12.5, s.px(300), f"label {label}", role="display", weight=700)
        s.display(X(26), P(y + 8), label, size=12.5)
        for j, ln in enumerate(lines):
            s.assert_fits(ln, 10.5, s.px(304), f"line {ln}", role="body")
            s.body(X(26), P(y + 27 + 13 * j), ln, size=10.5, fill=s.muted)
        if mw < 100:
            s.hatch_rect(X(BX0 + mw * scale), P(y + 10), s.px((100 - mw) * scale), s.px(BH), spacing=6)
        s.fill_rect(X(BX0), P(y + 10), s.px(mw * scale), s.px(BH), fill=s.accent if i == 2 else s.t["card_ghost"])
        s.rect(X(BX0), P(y + 10), s.px(100 * scale), s.px(BH), wd=s.W0 * 2, stroke=s.line_c)
        s.assert_fits(value, 11, s.px(mw * scale - 16), f"value {value}", role="display", weight=700)
        s.display(X(BX0 + mw * scale) - s.px(8), P(y + 10 + BH / 2 + 4), value, size=11, anchor="end", fill=s.bg if i == 2 else s.ink)
        s.end()

    s.group("note", 1900)
    ny = P(20 + 3 * 84 - 10)
    s.hair(X(0), ny, X(720), ny)
    note = "Galaxy’s first phase at Helios, Texas, July 2026: 133 MW of IT delivered from about 200 MW of gross site power."
    s.assert_fits(note, 10.5, s.px(720), "note", role="body")
    s.body(X(0), ny + s.px(20), note, size=10.5, fill=s.muted)
    s.end()
    s.write("grid-number", "From the grid number to the IT number on a converted mining site: 100 MW at the fence, about 80 MW after the cooling plant and the losses, about 65 MW of IT after redundancy",
            "Drawing by Abdelilah Sidqui for sidqui.com; typical arrangement, no project.")


if __name__ == "__main__":
    both(build)
