"""OGP画像（1200x630）と apple-touch-icon（180x180）を public/ に生成する。

使い方: python tools/make_ogp.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
FONT_BOLD = "C:/Windows/Fonts/YuGothB.ttc"
SCENE = ROOT / "tools" / "ogp_scene.jpg"  # ゲーム画面のキャプチャ（縦長）

BG_TOP = (9, 13, 22)        # #090d16
BG_BOTTOM = (15, 23, 42)    # slate-900
SKY = (56, 189, 248)        # sky-400
CYAN = (103, 232, 249)      # cyan-300
AMBER = (251, 191, 36)      # amber-400
WHITE = (255, 255, 255)
SLATE = (148, 163, 184)     # slate-400


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def vertical_gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        d.line([(0, y), (w, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return img


def draw_pipe(d, points, width, color, joint_color):
    d.line(points, fill=color, width=width, joint="curve")
    for x, y in points[1:-1]:
        r = width // 2 + 6
        d.ellipse([x - r, y - r, x + r, y + r], fill=joint_color)


def make_ogp():
    w, h = 1200, 630
    img = vertical_gradient(w, h, BG_TOP, BG_BOTTOM)

    # 右側にゲーム画面（3D の現場を撮ったもの）を敷く
    if SCENE.exists():
        shot = Image.open(SCENE).convert("RGB")
        sw, sh = shot.size
        crop = shot.crop((0, int(sh * 0.2), sw, int(sh * 0.72)))
        scale = h / crop.height
        crop = crop.resize((int(crop.width * scale), h), Image.LANCZOS)
        x0 = w - crop.width
        img.paste(crop, (x0, 0))
        # 左の文字エリアへなじませるグラデーション
        fade = Image.new("L", (240, h))
        for x in range(240):
            ImageDraw.Draw(fade).line([(x, 0), (x, h)], fill=int(255 * (1 - x / 240)))
        img.paste(Image.new("RGB", (240, h), BG_BOTTOM), (x0, 0), fade)
    d = ImageDraw.Draw(img)

    # 上部バッジ
    badge_font = font(28)
    badge = "松下工業 × 採用ミニゲーム"
    bw = d.textlength(badge, font=badge_font)
    d.rounded_rectangle([64, 64, 64 + bw + 44, 64 + 52], radius=26, fill=SKY)
    d.text((64 + 22, 64 + 8), badge, font=badge_font, fill=BG_TOP)

    # タイトル
    d.text((60, 150), "快感！", font=font(80), fill=AMBER)
    d.text((60, 236), "配管", font=font(128), fill=WHITE)
    d.text((60, 372), "クラフト", font=font(96), fill=WHITE)

    # サブコピー
    d.text((66, 500), "安く・うまく・漏らさずつなげ！", font=font(36), fill=CYAN)
    d.text((66, 554), "スマホで遊べる3D配管パズル ▶", font=font(26), fill=AMBER)

    img.save(PUBLIC / "ogp.png", optimize=True)


def make_touch_icon():
    s = 180
    img = Image.new("RGB", (s, s), BG_TOP)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([10, 10, s - 10, s - 10], radius=36, fill=(12, 74, 110))
    d.line([(10, 128), (90, 128), (90, 70), (170, 70)], fill=SKY, width=16, joint="curve")
    f = font(46)
    tw = d.textlength("配管", font=f)
    d.text(((s - tw) / 2, 18), "配管", font=f, fill=WHITE)
    img.save(PUBLIC / "apple-touch-icon.png", optimize=True)


if __name__ == "__main__":
    PUBLIC.mkdir(exist_ok=True)
    make_ogp()
    make_touch_icon()
    print("wrote", PUBLIC / "ogp.png", PUBLIC / "apple-touch-icon.png")
