"""Figure for the note on cooling an AI hall in the Gulf: the two loops a liquid-cooled hall has, the three ways
the heat can leave, and which of them still work at the summer peak. Editorial plate, stone theme."""
from svglib import SVG, both

DW = 824
CONTENT = 316
W = 1400
H = round((CONTENT + 106) * W / DW)

REJECTION = [
    ("Dry cooler", ("Limited by the dry-bulb: water", "cannot leave cooler than the air."), "Spends fan power", "Out at the peak", True),
    ("Evaporative tower", ("Nears the wet-bulb, never reaches", "it. About 1,500 L/h per MW."), "Spends water", "Carries the peak", False),
    ("Chiller", ("Compressors sized for the hottest", "hour, and the power behind them."), "Spends power", "Carries the peak", False),
]


def build(theme="stone"):
    s = SVG(W, H, theme, name="two-loops", display_w=DW)
    L0, y0, R0, y1 = s.editorial_plate("01", "Two loops, three ways out", "A liquid-cooled hall in the Gulf")
    X = lambda v: L0 + s.px(v)
    P = lambda v: y0 + s.px(v)

    def card_text(x, y, w, title, lines, size=12.5, lsize=10.5, top=19):
        s.assert_fits(title, size, s.px(w - 24), f"card {title}", role="display", weight=700)
        s.display(x + s.px(12), y + s.px(top), title, size=size, weight=700)
        for j, ln in enumerate(lines):
            s.assert_fits(ln, lsize, s.px(w - 24), f"line {ln}", role="body")
            s.body(x + s.px(12), y + s.px(top + 15 + 13 * j), ln, size=lsize, fill=s.muted)

    # ---- the hall: cold plates and the air-cooled share
    s.group("hall", 300)
    s.eyebrow(X(0), P(12), "The hall", size=10)
    hx, hw = 0, 196
    s.card(X(hx), P(24), s.px(hw), s.px(78))
    card_text(X(hx), P(24), hw, "Cold plates", ("Processors and accelerators,", "warm coolant, little mass."))
    s.card(X(hx), P(126), s.px(hw), s.px(78), ghost=True)
    card_text(X(hx), P(126), hw, "Air-cooled share", ("Memory, drives, power supplies,", "switches, storage, network."))
    s.end()

    # ---- the two loops
    s.group("loops", 800)
    s.eyebrow(X(226), P(12), "Two loops", size=10)
    lx, lw = 240, 160
    s.card(X(lx), P(24), s.px(lw), s.px(78))
    card_text(X(lx), P(24), lw, "CDU, warm loop", ("Warm facility water;", "more free-cooling hours."))
    s.card(X(lx), P(126), s.px(lw), s.px(78))
    card_text(X(lx), P(126), lw, "CRAH, chilled loop", ("Coil water below the air", "it makes: compressors."))
    # pipes from the hall to the loops
    for yy in (63, 165):
        s.line(X(hx + hw), P(yy), X(lx) - s.px(5), P(yy), wd=s.W1)
        s.arrow_head(X(lx) - s.px(5), P(yy), s.px(4.5), "right", fill=s.stroke)
    s.end()

    # ---- the ways out
    s.group("rejection", 1400)
    s.eyebrow(X(434), P(12), "Three ways out", size=10)
    rx, rw, rh = 434, 286, 62
    bus = X(416)
    s.line(bus, P(63), bus, P(24 + 2 * (rh + 14) + rh / 2), wd=s.W1)          # the rejection bus
    s.line(X(lx + lw), P(63), bus, P(63), wd=s.W1)                               # warm loop to the bus
    s.line(X(lx + lw), P(165), X(lx + lw + 10), P(165), wd=s.W1)                 # chilled loop to the chiller
    s.line(X(lx + lw + 10), P(165), X(lx + lw + 10), P(24 + 2 * (rh + 14) + rh / 2), wd=s.W1)
    s.line(X(lx + lw + 10), P(24 + 2 * (rh + 14) + rh / 2), X(rx) - s.px(5), P(24 + 2 * (rh + 14) + rh / 2), wd=s.W1)
    for i, (title, lines, spends, peak, out) in enumerate(REJECTION):
        y = 24 + i * (rh + 14)
        cy = y + rh / 2
        if i < 2:
            s.line(bus, P(cy), X(rx) - s.px(5), P(cy), wd=s.W1)
        s.arrow_head(X(rx) - s.px(5), P(cy), s.px(4.5), "right", fill=s.stroke)
        s.card(X(rx), P(y), s.px(rw), s.px(rh), ghost=out)
        card_text(X(rx), P(y), rw, title, lines, top=18)
        s.assert_fits(spends, 9.5, s.px(120), "spends", role="mono", spacing=0.08)
        s.mono(X(rx + rw) - s.px(12), P(y + 18), spends, size=9.5, fill=s.eyebrow_c, anchor="end", spacing=0.08, upper=True)
        if out:
            s.hatch_rect(X(rx + 2), P(y + 2), s.px(rw - 4), s.px(rh - 4), spacing=7)
    s.end()

    # ---- the summer peak, read down the right-hand column
    s.group("peak", 2000)
    py = 24 + 3 * (rh + 14) + 4
    s.hair(X(rx), P(py), X(rx + rw), P(py))
    s.eyebrow(X(rx), P(py + 16), "Gulf summer peak", size=10)
    for j, line in enumerate(("Dry-bulb above 45 °C, wet-bulb above 30 °C.", "The dry cooler is out. The tower spends", "water, the chiller spends power.")):
        s.assert_fits(line, 10.5, s.px(rw), "peak", role="body")
        s.body(X(rx), P(py + 32 + 13 * j), line, size=10.5, fill=s.muted)
    s.end()

    # ---- the note under the hall
    s.group("note", 2400)
    ny = 24 + 2 * 102 + 6
    for j, line in enumerate(("Free-cooling hours rise with the water temperature the IT", "vendor allows, and fall to zero while the dry-bulb sits above", "the loop. The chilled loop runs on compressors all summer.")):
        s.assert_fits(line, 10.5, s.px(376), "note", role="body")
        s.body(X(0), P(ny + 14 + 13.5 * j), line, size=10.5, fill=s.muted)
    s.end()
    s.write("two-loops", "A liquid-cooled hall's two loops and the three ways its heat can leave: dry cooler, evaporative tower and chiller, with what each spends and which carries the Gulf summer peak",
            "Drawing by Abdelilah Sidqui for sidqui.com; typical arrangement, no project.")


if __name__ == "__main__":
    both(build)
