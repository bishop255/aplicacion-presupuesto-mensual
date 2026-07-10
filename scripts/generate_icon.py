from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
PNG_PATH = ASSETS / "app_icon.png"
ICO_PATH = ASSETS / "app_icon.ico"


def build_icon(size=1024):
    scale = size / 256
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    def s(value):
        return int(round(value * scale))

    draw.rounded_rectangle((0, 0, size, size), radius=s(56), fill="#2563eb")
    draw.rounded_rectangle((s(48), s(54), s(208), s(202)), radius=s(22), fill="#ffffff")
    draw.rounded_rectangle((s(64), s(78), s(192), s(94)), radius=s(8), fill="#dbeafe")
    draw.rounded_rectangle((s(64), s(112), s(126), s(126)), radius=s(7), fill="#22c55e")
    draw.rounded_rectangle((s(64), s(142), s(160), s(156)), radius=s(7), fill="#0891b2")
    draw.rounded_rectangle((s(64), s(172), s(138), s(186)), radius=s(7), fill="#f59e0b")
    draw.ellipse((s(144), s(132), s(212), s(200)), fill="#7c3aed")
    draw.line((s(178), s(145), s(178), s(187)), fill="#ffffff", width=s(10))
    draw.arc((s(158), s(142), s(202), s(174)), start=198, end=340, fill="#ffffff", width=s(8))
    draw.arc((s(154), s(158), s(198), s(190)), start=18, end=160, fill="#ffffff", width=s(8))
    return image


def main():
    ASSETS.mkdir(exist_ok=True)
    image = build_icon()
    image.save(PNG_PATH)
    image.save(
        ICO_PATH,
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"Icono generado: {ICO_PATH}")


if __name__ == "__main__":
    main()
