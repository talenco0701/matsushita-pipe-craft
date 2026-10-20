"""OGP画像（1200x630）と apple-touch-icon（180x180）を public/ に生成する。

使い方: python tools/make_ogp.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
FONT_BOLD = "C:/Windows/Fonts/YuGothB.ttc"

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
    d = ImageDraw.Draw(img)

    # 背景の配管ライン（段階的に細くなる＝ゲームの「段階口径設計」）
    draw_pipe(d, [(-20, 580), (260, 580), (260, 505), (560, 505)], 46, (12, 74, 110), (14, 116, 144))
    draw_pipe(d, [(560, 505), (860, 505), (860, 565), (1220, 565)], 30, (12, 74, 110), (14, 116, 144))
    d.line([(-20, 580), (260, 580)], fill=SKY, width=10)
    d.line([(260, 505), (560, 505)], fill=CYAN, width=8)
    d.line([(860, 565), (1220, 565)], fill=CYAN, width=6)

    # 上部バッジ
    badge_font = font(30)
    badge = "松下工業 × 採用ミニゲーム"
    bw = d.textlength(badge, font=badge_font)
    d.rounded_rectangle([72, 64, 72 + bw + 48, 64 + 56], radius=28, fill=SKY)
    d.text((72 + 24, 64 + 9), badge, font=badge_font, fill=BG_TOP)

    # タイトル
    d.text((68, 150), "快感！", font=font(84), fill=AMBER)
    d.text((68, 238), "配管クラフト", font=font(132), fill=WHITE)

    # サブコピー
    d.text((74, 398), "水が来る前に、管をつなげ！", font=font(44), fill=CYAN)

    # 右上の CTA
    cta_font = font(30)
    cta = "スマホでプレイ ▶"
    cw = d.textlength(cta, font=cta_font)
    d.rounded_rectangle([w - 72 - cw - 48, 64, w - 72, 120], radius=28, outline=AMBER, width=3)
    d.text((w - 72 - cw - 24, 64 + 9), cta, font=cta_font, fill=AMBER)

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
