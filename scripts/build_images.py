"""Generate the site's images from the portrait and the static fonts: the social card (1200x630), a card for each
published note, the icons, and the headshot downloads. Run: python -I scripts/build_images.py"""
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "public"
FONTS = ROOT / "scripts/fonts"
GROUND, INK, MUTED, ACCENT, LINE = (242, 239, 233), (23, 22, 20), (107, 101, 92), (158, 69, 34), (217, 211, 200)
NAME = "Abdelilah Sidqui"
EYEBROW = "DUBAI · DATA CENTER INFRASTRUCTURE"
DEFINITION = ["Electrical engineer, Managing Partner of the data center", "engineering consultancy UBIK, and Board Director of", "African Digital Infrastructure Investments."]


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def social_card() -> None:
    im = Image.new("RGB", (1200, 630), GROUND)
    d = ImageDraw.Draw(im)
    portrait = Image.open(PUB / "people/abdelilah-sidqui.jpg").convert("RGB")
    portrait = portrait.resize((272, 340), Image.LANCZOS)
    im.paste(portrait, (1200 - 72 - 272, 72))
    d.text((72, 84), EYEBROW, font=font("JetBrainsMono-Regular.ttf", 17), fill=ACCENT)
    d.text((66, 128), NAME.split()[0], font=font("SchibstedGrotesk-Bold.ttf", 118), fill=INK)
    d.text((66, 240), NAME.split()[1], font=font("SchibstedGrotesk-Bold.ttf", 118), fill=INK)
    y = 404
    for line in DEFINITION:
        d.text((72, y), line, font=font("Inter-Regular.ttf", 25), fill=INK)
        y += 36
    d.line([(72, 548), (1128, 548)], fill=(217, 211, 200), width=1)
    d.text((72, 566), "SIDQUI.COM", font=font("JetBrainsMono-Regular.ttf", 15), fill=MUTED)
    im.save(PUB / "og.jpg", "JPEG", quality=88, optimize=True)


def published_notes():
    """(slug, title) of each note in content/notes that is not a draft, read from the front matter."""
    for file in sorted((ROOT / "content/notes").glob("*.mdx")):
        head = re.match(r"---\n(.*?)\n---", file.read_text(encoding="utf-8"), re.S)
        fields = dict(re.findall(r"^(\w+):\s*(.*)$", head.group(1), re.M)) if head else {}
        if fields.get("draft", "").strip() == "true" or not fields.get("title"):
            continue
        yield file.stem, fields["title"].strip().strip('"')


def wrap(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if d.textlength(trial, font=f) <= width:
            current = trial
        else:
            lines.append(current); current = word
    if current:
        lines.append(current)
    return lines


def note_cards() -> None:
    """A card per note for LinkedIn and the other previews: the title large on the ground, the name at the foot."""
    out = PUB / "og"; out.mkdir(exist_ok=True)
    for slug, title in published_notes():
        im = Image.new("RGB", (1200, 630), GROUND)
        d = ImageDraw.Draw(im)
        d.text((72, 84), "NOTES · SIDQUI.COM", font=font("JetBrainsMono-Regular.ttf", 17), fill=ACCENT)
        size = 76
        while True:
            f = font("SchibstedGrotesk-Bold.ttf", size)
            lines = wrap(d, title, f, 1056)
            if len(lines) <= 3 or size <= 56:
                break
            size -= 4
        y = 146
        for line in lines:
            d.text((66, y), line, font=f, fill=INK)
            y += round(size * 1.06)
        d.line([(72, 548), (1128, 548)], fill=LINE, width=1)
        d.text((72, 564), NAME, font=font("Inter-Regular.ttf", 22), fill=INK)
        tag = font("JetBrainsMono-Regular.ttf", 15)
        d.text((1128 - d.textlength(EYEBROW, font=tag), 570), EYEBROW, font=tag, fill=MUTED)
        im.save(out / f"{slug}.jpg", "JPEG", quality=88, optimize=True)


def icons() -> None:
    """A stone square with the initials in the display face; the favicon is read at 16 and 32 px, so one letter."""
    for size, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-icon.png")):
        im = Image.new("RGB", (size, size), GROUND)
        d = ImageDraw.Draw(im)
        f = font("SchibstedGrotesk-Bold.ttf", round(size * 0.62))
        box = d.textbbox((0, 0), "S", font=f)
        d.text(((size - (box[2] - box[0])) / 2 - box[0], (size - (box[3] - box[1])) / 2 - box[1]), "S", font=f, fill=INK)
        im.save(PUB / name, "PNG", optimize=True)
    base = Image.open(PUB / "icon-512.png")
    base.save(PUB / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


def headshots() -> None:
    src = Image.open(PUB / "people/abdelilah-sidqui.jpg").convert("RGB")
    out = PUB / "downloads"; out.mkdir(exist_ok=True)
    small = src.copy(); small.thumbnail((800, 1000), Image.LANCZOS)
    small.save(out / "abdelilah-sidqui-headshot-800.jpg", "JPEG", quality=90, optimize=True)
    src.save(out / "abdelilah-sidqui-headshot-full.jpg", "JPEG", quality=94, optimize=True)


if __name__ == "__main__":
    social_card(); note_cards(); icons(); headshots()
    print("wrote og.jpg, the note cards, icons, favicon and the headshot downloads")
