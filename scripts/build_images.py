"""Generate the site's images from the portrait and the static fonts: the social card (1200x630), the icons, and
the headshot downloads. Run: python -I scripts/build_images.py"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "public"
FONTS = ROOT / "scripts/fonts"
GROUND, INK, MUTED, ACCENT = (242, 239, 233), (23, 22, 20), (107, 101, 92), (158, 69, 34)
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
    social_card(); icons(); headshots()
    print("wrote og.jpg, icons, favicon and the headshot downloads")
