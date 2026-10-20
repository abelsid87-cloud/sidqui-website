"""Figure for the note on Tier III certificates: the three Uptime Institute certifications placed on the life of a
facility, what each proves, and the two gaps in which the certified topology is lost. Editorial plate, stone."""
from svglib import SVG, both

DW = 824
CONTENT = 296
W = 1400
H = round((CONTENT + 106) * W / DW)

# Operation is the long stage; the certificates sit where they are issued, each above its card.
STAGES = [("Design", 107), ("Construction", 150), ("Commissioning", 103), ("Operation", 360)]
CERTS = [
    (107, "Design Documents", ("Proves the drawings would meet", "Tier III if built as drawn."), ("Not what was built, nor", "how the controls behave.")),
    (360, "Constructed Facility", ("Demonstrations on site: paths out,", "elements failed, load supported."), ("One installation, one phase;", "the next phase is not covered.")),
    (613, "Operational Sustainability", ("Management, staffing, maintenance", "and operating practice."), ("Not an uptime percentage;", "no certificate is."))
]
GAPS = [(107, 360, "Value engineering, substitutions"), (360, 720, "Changes, load growth, bypasses")]
ASK = [("The certificate: type,", "date, phase, capacity"), ("Changes since, checked", "against the drawings"), ("The integrated systems", "test report"), ("Load carried against the", "certified capacity")]


def build(theme="stone"):
    s = SVG(W, H, theme, name="three-certificates", display_w=DW)
    L0, y0, R0, y1 = s.editorial_plate("02", "Three certificates, three objects", "What each one proves")
    X = lambda v: L0 + s.px(v)
    P = lambda v: y0 + s.px(v)

    # ---- the gaps above the line, where the topology is lost
    s.group("gaps", 300)
    s.eyebrow(X(0), P(12), "Where the topology is lost", size=10)
    for x0, x1, label in GAPS:
        s.hatch_rect(X(x0 + 8), P(22), s.px(x1 - x0 - 16), s.px(22), spacing=7)
        s.assert_fits(label, 10, s.px(x1 - x0 - 24), "gap label", role="body")
        s.body(X(x0 + 14), P(36), label, size=10, fill=s.ink, halo=True)
    s.end()

    # ---- the life of the facility
    s.group("stages", 800)
    ty = 70
    s.line(X(0), P(ty), X(720), P(ty), wd=s.W1)
    s.arrow_head(X(720), P(ty), s.px(5), "right", fill=s.stroke)
    x = 0
    for name, w in STAGES:
        s.line(X(x), P(ty - 6), X(x), P(ty + 6), wd=s.W2)
        s.assert_fits(name.upper(), 9.5, s.px(w - 10), "stage", spacing=0.14)
        s.eyebrow(X(x + 8), P(ty - 12), name, size=9.5)
        x += w
    s.end()

    # ---- the three certificates, hung from the line
    s.group("certificates", 1400)
    cw, ch = 214, 110
    for i, (cx, title, proves, limits) in enumerate(CERTS):
        x = cx - cw / 2
        y = ty + 26
        s.fill_circle(X(cx), P(ty), s.px(6), fill=s.accent)
        s.line(X(cx), P(ty + 6), X(cx), P(y), wd=s.W2, stroke=s.accent)
        s.card(X(x), P(y), s.px(cw), s.px(ch))
        s.mono(X(x + 12), P(y + 18), f"TIER CERTIFICATION 0{i + 1}", size=9, fill=s.eyebrow_c, spacing=0.1)
        s.assert_fits(title, 12, s.px(cw - 24), "cert title", role="display", weight=700)
        s.display(X(x + 12), P(y + 36), title, size=12, weight=700)
        for j, ln in enumerate(proves):
            s.assert_fits(ln, 10, s.px(cw - 24), "proves", role="body")
            s.body(X(x + 12), P(y + 54 + 13 * j), ln, size=10)
        for j, ln in enumerate(limits):
            s.assert_fits(ln, 10, s.px(cw - 24), "limits", role="body")
            s.body(X(x + 12), P(y + 84 + 13 * j), ln, size=10, fill=s.muted)
    s.end()

    # ---- what to ask for
    s.group("ask", 2000)
    ay = ty + 26 + ch + 22
    s.hair(X(0), P(ay), X(720), P(ay))
    s.eyebrow(X(0), P(ay + 18), "Before relying on a Tier III claim, ask for", size=10)
    colw = (720 - 3 * 16) / 4
    for i, item in enumerate(ASK):
        cx = X(i * (colw + 16))
        s.mono(cx, P(ay + 38), f"0{i + 1}", size=9.5, fill=s.eyebrow_c, weight=500)
        for j, ln in enumerate(item):
            s.assert_fits(ln, 10.5, s.px(colw - 26), "ask", role="body")
            s.body(cx + s.px(22), P(ay + 38 + 13 * j), ln, size=10.5)
    s.end()
    s.write("three-certificates", "Uptime Institute's three Tier certifications on the life of a facility, what each proves and does not, the gaps where the certified topology is lost, and four things to ask for before relying on a claim",
            "Drawing by Abdelilah Sidqui for sidqui.com.")


if __name__ == "__main__":
    both(build)
