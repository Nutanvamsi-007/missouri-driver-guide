#!/usr/bin/env python3
"""
Generate brand assets, favicons, PWA icons, and OpenGraph preview images
for the Missouri Driver Guide public web deployment.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ASSETS_DIR = "/Users/nutanvamsigunti/workspace/missouri-driver-guide/assets"
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
os.makedirs(ICONS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Colors
MO_NAVY = (11, 37, 69)      # #0b2545
MO_SKY = (2, 132, 199)      # #0284c7
MO_GOLD = (245, 158, 11)    # #f59e0b
DARK_BG = (11, 17, 32)      # #0b1120
CARD_BG = (15, 23, 42)      # #0f172a
WHITE = (255, 255, 255)
LIGHT_BLUE = (224, 242, 254)
ACCENT_CYAN = (56, 189, 248) # #38bdf8

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"

def create_svg_favicon():
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="moGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b2545" />
      <stop offset="100%" stop-color="#0284c7" />
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f59e0b" />
      <stop offset="100%" stop-color="#fbbf24" />
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.45" />
    </filter>
  </defs>
  <!-- Background Rounded Shield -->
  <rect x="16" y="16" width="480" height="480" rx="108" fill="url(#moGrad)" stroke="#f59e0b" stroke-width="12" filter="url(#shadow)" />
  
  <!-- Outer Highway Shield Outline -->
  <path d="M 120,95 L 392,95 C 410,180 435,270 380,360 C 335,420 256,450 256,450 C 256,450 177,420 132,360 C 77,270 102,180 120,95 Z" 
        fill="rgba(15,23,42,0.6)" stroke="url(#goldGrad)" stroke-width="14" stroke-linejoin="round" />
  
  <!-- MO State Text -->
  <text x="256" y="175" font-family="-apple-system, 'Inter', 'Segoe UI', Arial, sans-serif" font-size="72" font-weight="900" fill="#f8fafc" text-anchor="middle" letter-spacing="6">MISSOURI</text>
  
  <!-- Inner Highway Badge with Steering Wheel / Car Silhouette -->
  <!-- Road lines -->
  <polygon points="210,380 302,380 270,250 242,250" fill="#38bdf8" opacity="0.4" />
  <!-- Center dashed line -->
  <line x1="256" y1="260" x2="256" y2="370" stroke="#f59e0b" stroke-width="6" stroke-dasharray="16 10" stroke-linecap="round" />
  
  <!-- Car Silhouette -->
  <g transform="translate(196, 215) scale(0.24)">
    <path d="M100 280 C60 280 40 250 50 220 L80 140 C95 100 130 80 180 80 L320 80 C370 80 405 100 420 140 L450 220 C460 250 440 280 400 280 L380 280 C380 310 355 330 325 330 C295 330 275 310 275 280 L225 280 C225 310 205 330 175 330 C145 330 120 310 120 280 Z" fill="#ffffff" />
    <path d="M105 150 L395 150 L370 105 C360 95 340 90 320 90 L180 90 C160 90 140 95 130 105 Z" fill="#0b2545" />
    <!-- Headlights -->
    <circle cx="95" cy="220" r="22" fill="#fbbf24" />
    <circle cx="405" cy="220" r="22" fill="#fbbf24" />
  </g>
  
  <!-- Bottom Pill: 2026 -->
  <rect x="186" y="396" width="140" height="34" rx="17" fill="#f59e0b" />
  <text x="256" y="420" font-family="-apple-system, 'Inter', Arial, sans-serif" font-size="20" font-weight="900" fill="#0b2545" text-anchor="middle" letter-spacing="2">DOR 2026</text>
</svg>'''
    svg_path = os.path.join(ICONS_DIR, "favicon.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {svg_path}")
    
    # Also save to root favicon.svg
    root_svg = "/Users/nutanvamsigunti/workspace/missouri-driver-guide/favicon.svg"
    with open(root_svg, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated {root_svg}")

def generate_png_icon(size):
    """Generate high-res raster icon of specified dimensions"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background rounded rect
    margin = int(size * 0.04)
    radius = int(size * 0.22)
    x0, y0 = margin, margin
    x1, y1 = size - margin, size - margin
    
    # Gradient simulation using concentric fills or navy base with border
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=MO_NAVY, outline=MO_GOLD, width=max(2, int(size * 0.03)))
    
    # Inner badge
    badge_pad = int(size * 0.16)
    badge_x0, badge_y0 = badge_pad, int(size * 0.15)
    badge_x1, badge_y1 = size - badge_pad, int(size * 0.85)
    draw.rounded_rectangle([badge_x0, badge_y0, badge_x1, badge_y1], radius=int(radius * 0.6), fill=(15, 23, 42, 220), outline=MO_SKY, width=max(1, int(size * 0.02)))
    
    # Text "MO"
    font_size = int(size * 0.28)
    try:
        font = ImageFont.truetype(FONT_BOLD, font_size)
    except Exception:
        font = ImageFont.load_default()
        
    text = "MO"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) // 2
    ty = int(size * 0.23)
    draw.text((tx, ty), text, font=font, fill=WHITE)
    
    # Subtext "DRIVER"
    sub_size = max(10, int(size * 0.10))
    try:
        sub_font = ImageFont.truetype(FONT_BOLD, sub_size)
    except Exception:
        sub_font = ImageFont.load_default()
    sub_text = "DRIVER"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    sub_tw = sub_bbox[2] - sub_bbox[0]
    draw.text(((size - sub_tw) // 2, int(size * 0.53)), sub_text, font=sub_font, fill=ACCENT_CYAN)

    # Pill "2026"
    pill_w = int(size * 0.44)
    pill_h = int(size * 0.14)
    px0 = (size - pill_w) // 2
    py0 = int(size * 0.68)
    draw.rounded_rectangle([px0, py0, px0 + pill_w, py0 + pill_h], radius=pill_h // 2, fill=MO_GOLD)
    
    year_size = max(9, int(size * 0.08))
    try:
        year_font = ImageFont.truetype(FONT_BOLD, year_size)
    except Exception:
        year_font = ImageFont.load_default()
    year_text = "2026 DOR"
    yb = draw.textbbox((0, 0), year_text, font=year_font)
    ytw = yb[2] - yb[0]
    yth = yb[3] - yb[1]
    draw.text(((size - ytw) // 2, py0 + (pill_h - yth) // 2 - 1), year_text, font=year_font, fill=MO_NAVY)

    return img

def generate_all_icons():
    create_svg_favicon()
    
    sizes = {
        "icon-512.png": 512,
        "icon-192.png": 192,
        "apple-touch-icon.png": 180,
        "favicon-32x32.png": 32,
        "favicon-16x16.png": 16,
    }
    
    generated_images = {}
    for filename, s in sizes.items():
        im = generate_png_icon(s)
        path = os.path.join(ICONS_DIR, filename)
        im.save(path, "PNG")
        generated_images[s] = im
        print(f"Generated {path} ({s}x{s})")
        
    # Also save apple-touch-icon.png to root for default safari crawls
    root_apple = "/Users/nutanvamsigunti/workspace/missouri-driver-guide/apple-touch-icon.png"
    generated_images[180].save(root_apple, "PNG")
    
    # Save multi-size favicon.ico in root and icons dir
    ico_path = "/Users/nutanvamsigunti/workspace/missouri-driver-guide/favicon.ico"
    generated_images[32].save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"Generated {ico_path}")

def generate_og_image():
    """Generate high-impact 1200x630 OpenGraph social preview banner"""
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), DARK_BG)
    draw = ImageDraw.Draw(img)
    
    # Decorative subtle gradient background grid / glow
    for y in range(H):
        ratio = y / H
        r = int(DARK_BG[0] * (1 - ratio) + 15 * ratio)
        g = int(DARK_BG[1] * (1 - ratio) + 23 * ratio)
        b = int(DARK_BG[2] * (1 - ratio) + 42 * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    # Cyan / Blue subtle radial glow at top-left
    glow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    glow_draw.ellipse([-100, -100, 500, 500], fill=(2, 132, 199, 45))
    glow_draw.ellipse([800, 100, 1400, 700], fill=(11, 37, 69, 70))
    img = Image.alpha_composite(img.convert("RGBA"), glow_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Border frame
    draw.rectangle([12, 12, W - 12, H - 12], outline=(255, 255, 255, 30), width=1)
    
    # Badge Pill (Top Left)
    pill_x, pill_y = 60, 50
    pill_w, pill_h = 440, 42
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=21, fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    
    # Pulse dot in pill
    draw.ellipse([pill_x + 16, pill_y + 14, pill_x + 28, pill_y + 26], fill=(16, 185, 129))
    
    try:
        pill_font = ImageFont.truetype(FONT_BOLD, 16)
        title_font = ImageFont.truetype(FONT_BOLD, 52)
        sub_font = ImageFont.truetype(FONT_BOLD, 26)
        desc_font = ImageFont.truetype(FONT_REGULAR, 20)
        card_title_font = ImageFont.truetype(FONT_BOLD, 18)
        card_desc_font = ImageFont.truetype(FONT_REGULAR, 15)
        stat_num_font = ImageFont.truetype(FONT_BOLD, 36)
        stat_lbl_font = ImageFont.truetype(FONT_BOLD, 14)
    except Exception:
        pill_font = title_font = sub_font = desc_font = card_title_font = card_desc_font = stat_num_font = stat_lbl_font = ImageFont.load_default()
        
    draw.text((pill_x + 38, pill_y + 11), "OFFICIAL 2026 MISSOURI DOR EDITION", font=pill_font, fill=(241, 245, 249))
    
    # Main Headline
    draw.text((60, 115), "Missouri Driver Guide", font=title_font, fill=(255, 255, 255))
    draw.text((60, 180), "Interactive Study System & Permit Exam Simulator", font=sub_font, fill=ACCENT_CYAN)
    
    # Sub-description
    draw.text((60, 226), "Free, comprehensive preparation portal for the Missouri Department of Revenue", font=desc_font, fill=(203, 213, 225))
    draw.text((60, 255), "Class F Driver License Exam. 100% Client-Side with Zero Latency.", font=desc_font, fill=(148, 163, 184))

    # Feature Grid Badges (Left Column)
    features = [
        ("🚗 25-Question Exam Simulator", "Timed & Practice modes with official 80% passing threshold (20/25)"),
        ("📖 Full 16-Chapter Handbook", "Complete 102 pages with high-res original PDF inspector & audio"),
        ("🛑 80+ Traffic Signs Lab", "Interactive 3D flashcards covering shapes, regulatory, and warning signs"),
        ("⚡ Real-Time Physics Simulators", "Stopping distance braking physics & Missouri point violation tracking")
    ]
    
    card_y = 310
    for title, desc in features:
        card_w = 640
        card_h = 64
        draw.rounded_rectangle([60, card_y, 60 + card_w, card_y + card_h], radius=10, fill=(15, 23, 42, 230), outline=(51, 65, 85), width=1)
        draw.text((78, card_y + 12), title, font=card_title_font, fill=(248, 250, 252))
        draw.text((78, card_y + 36), desc, font=card_desc_font, fill=(148, 163, 184))
        card_y += 74

    # Right Column: Visual Signs Showcase Card
    right_x = 740
    right_y = 110
    right_w = 400
    right_h = 470
    draw.rounded_rectangle([right_x, right_y, right_x + right_w, right_y + right_h], radius=18, fill=(15, 23, 42), outline=MO_GOLD, width=2)
    
    # Right Header
    draw.rectangle([right_x, right_y, right_x + right_w, right_y + 60], fill=(30, 41, 59))
    draw.text((right_x + 24, right_y + 18), "OFFICIAL STATE TEST ASSETS", font=card_title_font, fill=MO_GOLD)

    # Composite Actual Traffic Sign Images from assets/images/signs/
    sample_signs = [
        ("stop_sign.png", 60),
        ("speed_limit_70.png", 60),
        ("interstate_shield.png", 60),
        ("shape_diamond.png", 60),
        ("yield_sign.png", 60),
        ("pedestrian_crossing.png", 60),
    ]
    
    grid_coords = [
        (right_x + 40, right_y + 85),
        (right_x + 160, right_y + 85),
        (right_x + 280, right_y + 85),
        (right_x + 40, right_y + 205),
        (right_x + 160, right_y + 205),
        (right_x + 280, right_y + 205),
    ]
    
    for (filename, target_size), (gx, gy) in zip(sample_signs, grid_coords):
        sign_path = os.path.join(ASSETS_DIR, "images", "signs", filename)
        # White tile backing
        draw.rounded_rectangle([gx - 8, gy - 8, gx + target_size + 8, gy + target_size + 8], radius=8, fill=(255, 255, 255))
        if os.path.exists(sign_path):
            try:
                sign_im = Image.open(sign_path).convert("RGBA")
                sign_im.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
                # Center within tile
                offset_x = gx + (target_size - sign_im.width) // 2
                offset_y = gy + (target_size - sign_im.height) // 2
                img.paste(sign_im, (offset_x, offset_y), sign_im)
            except Exception as e:
                print(f"Could not load {filename}: {e}")
                
    # Bottom Stats Bar on Right Card
    stats_y = right_y + 340
    draw.line([(right_x + 20, stats_y), (right_x + right_w - 20, stats_y)], fill=(51, 65, 85), width=1)
    
    stat_items = [
        ("102", "PAGES"),
        ("25", "QUESTIONS"),
        ("81", "SIGNS"),
    ]
    
    col_w = right_w // 3
    for i, (num, lbl) in enumerate(stat_items):
        cx = right_x + (i * col_w) + (col_w // 2)
        nb = draw.textbbox((0, 0), num, font=stat_num_font)
        nw = nb[2] - nb[0]
        draw.text((cx - nw // 2, stats_y + 18), num, font=stat_num_font, fill=(248, 250, 252))
        
        lb = draw.textbbox((0, 0), lbl, font=stat_lbl_font)
        lw = lb[2] - lb[0]
        draw.text((cx - lw // 2, stats_y + 64), lbl, font=stat_lbl_font, fill=ACCENT_CYAN)

    og_out = os.path.join(IMAGES_DIR, "og-image.png")
    img.save(og_out, "PNG", quality=95)
    print(f"Generated OpenGraph preview image: {og_out}")

if __name__ == "__main__":
    generate_all_icons()
    generate_og_image()
    print("All branding assets generated successfully!")
