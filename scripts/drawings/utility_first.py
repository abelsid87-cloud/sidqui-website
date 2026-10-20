"""Figure for the note on starting an African data center brief with the utility: what the utility file sets,
in two chains. The documents set the capacity and the dates the phases follow; the outage record sets the
generator duty, the autonomy and the fuel on site. Editorial plate, stone theme."""
from svglib import SVG, both

DW = 824
CONTENT = 292
W = 1400
H = round((CONTENT + 106) * W / DW)

ROW1 = [
    (("Capacity", "letter"), ("Capacity may be", "available. Reserves", "nothing.")),
    (("Connection", "offer"), ("Point, voltage, cost,", "programme. Reserved", "once accepted.")),
    (("Connection", "agreement"), ("Capacity committed", "by dates. Not", "continuity of supply.")),
    (("Energisation", "certificate"), ("Supply at the", "boundary, sometimes", "below contract.")),
    (("Supply", "contract"), ("Tariff and contracted", "demand. No promise", "of continuity.")),
]
ROW2 = [
    (("Outage", "record"), ("Frequency, duration,", "the longest outage", "on the feeder.")),
    (("Generator", "duty"), ("Regular running under", "load is prime duty,", "not standby.")),
    (("Autonomy",), ("Longest credible", "outage plus the time", "to the next delivery.")),
    (("Fuel", "on site"), ("About 6,500 litres", "per MW-day, as a", "rule of thumb.")),
    (("Tanks",), ("Space, tanker access,", "distance from the", "public edge.")),
]


def build(theme="stone"):
    s = SVG(W, H, theme, name="utility-first", display_w=DW)
    L0, y0, R0, y1 = s.editorial_plate("03", "What the utility file sets", "Two chains, before the first drawing")
    X = lambda v: L0 + s.px(v)
    P = lambda v: y0 + s.px(v)
    n = 5
    CW, CH, gap = 128, 92, (720 - 5 * 128) / 4

    def chain(rows, top, eyebrow, result):
        s.eyebrow(X(0), P(top), eyebrow, size=10)
        y = top + 12
        for i, (title, lines) in enumerate(rows):
            x = X(i * (CW + gap))
            s.card(x, P(y), s.px(CW), s.px(CH))
            s.mono(x + s.px(12), P(y + 17), f"0{i + 1}", size=9, fill=s.eyebrow_c, spacing=0.1)
            ty = y + 33
            for j, ln in enumerate(title):
                s.assert_fits(ln, 12, s.px(CW - 24), f"title {ln}", role="display", weight=700)
                s.display(x + s.px(12), P(ty + 14 * j), ln, size=12, weight=700)
            ly = ty + 14 * len(title) + 4
            for j, ln in enumerate(lines):
                s.assert_fits(ln, 9.5, s.px(CW - 22), f"line {ln}", role="body")
                s.body(x + s.px(12), P(ly + 12 * j), ln, size=9.5, fill=s.muted)
            if i < n - 1:
                x1, x2 = x + s.px(CW), X((i + 1) * (CW + gap))
                s.line(x1, P(y + CH / 2), x2 - s.px(5), P(y + CH / 2), wd=s.px(1.4))
                s.arrow_head(x2 - s.px(5), P(y + CH / 2), s.px(4.5), "right", fill=s.stroke)
        s.assert_fits(result, 10.5, s.px(720), "result", role="body")
        s.body(X(0), P(y + CH + 16), result, size=10.5, fill=s.ink)
        return y + CH + 26

    s.group("capacity", 300)
    end1 = chain(ROW1, 12, "The documents set the capacity and the dates", "Phase 1 is drawn to the capacity committed in writing, by its date; later phases follow the later dates and the reinforcement.")
    s.end()

    s.group("fuel", 1400)
    s.hair(X(0), P(end1), X(720), P(end1))
    chain(ROW2, end1 + 14, "The outage record sets the generators and the fuel", "Storage covers the longest credible outage plus the road to the next delivery; a weak grid changes fuel, not the Tier objective.")
    s.end()
    s.write("utility-first", "What a utility's file sets in a data center brief: the five documents and the capacity and dates they commit, and the outage record that sets generator duty, autonomy and fuel storage",
            "Drawing by Abdelilah Sidqui for sidqui.com; typical sequence, no project.")


if __name__ == "__main__":
    both(build)
