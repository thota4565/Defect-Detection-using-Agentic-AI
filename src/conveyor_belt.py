# from PIL import Image, ImageDraw

# # ==========================
# # CONFIG
# # ==========================
# WIDTH, HEIGHT = 800, 300          # Size of the full image
# BELT_HEIGHT = 80                  # Thickness of the belt
# BELT_Y_CENTER = HEIGHT // 2       # Vertical center of belt
# FRAMES = 40                       # Number of frames in GIF
# STEP = 8                          # How many pixels the belt moves per frame
# PATTERN_WIDTH = 40                # Distance between belt slats
# DURATION_MS = 80                  # Delay between frames (controls speed)

# # Colors (R, G, B)
# BG_COLOR = (15, 15, 25)           # Dark background
# BELT_COLOR = (60, 60, 70)         # Belt main color
# BELT_EDGE_COLOR = (30, 30, 35)    # Slightly darker edges
# SLAT_COLOR = (100, 100, 110)      # Moving slats
# RAIL_COLOR = (160, 160, 170)      # Side rails color

# def draw_frame(offset):
#     """
#     Draw a single frame of the horizontal conveyor belt.
#     offset: how much the slat pattern is shifted horizontally.
#     """
#     img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
#     draw = ImageDraw.Draw(img)

#     # --------------------------
#     # Belt position
#     # --------------------------
#     belt_top = BELT_Y_CENTER - BELT_HEIGHT // 2
#     belt_bottom = BELT_Y_CENTER + BELT_HEIGHT // 2

#     # Main belt rectangle
#     draw.rectangle(
#         [0, belt_top, WIDTH, belt_bottom],
#         fill=BELT_COLOR
#     )

#     # Slight darker edges on top & bottom of belt (for 3D-ish look)
#     edge_thickness = 6
#     draw.rectangle(
#         [0, belt_top, WIDTH, belt_top + edge_thickness],
#         fill=BELT_EDGE_COLOR
#     )
#     draw.rectangle(
#         [0, belt_bottom - edge_thickness, WIDTH, belt_bottom],
#         fill=BELT_EDGE_COLOR
#     )

#     # --------------------------
#     # Moving belt slats (horizontal motion)
#     # --------------------------
#     # We draw vertical strips that repeat every PATTERN_WIDTH pixels,
#     # shifted by 'offset' so they animate.
#     for x in range(-PATTERN_WIDTH * 2, WIDTH + PATTERN_WIDTH * 2, PATTERN_WIDTH):
#         x_pos = x + offset
#         draw.rectangle(
#             [x_pos, belt_top + 5, x_pos + 10, belt_bottom - 5],
#             fill=SLAT_COLOR
#         )

#     # --------------------------
#     # Side rails (thick rails along top and bottom of belt)
#     # --------------------------
#     rail_thickness = 20

#     # Top rail above the belt
#     rail_top_top = belt_top - rail_thickness - 5
#     rail_top_bottom = belt_top - 5
#     draw.rectangle(
#         [0, rail_top_top, WIDTH, rail_top_bottom],
#         fill=RAIL_COLOR
#     )

#     # Bottom rail below the belt
#     rail_bottom_top = belt_bottom + 5
#     rail_bottom_bottom = belt_bottom + rail_thickness + 5
#     draw.rectangle(
#         [0, rail_bottom_top, WIDTH, rail_bottom_bottom],
#         fill=RAIL_COLOR
#     )

#     return img


# def main():
#     frames = []

#     # Generate frames with increasing offset to simulate motion
#     for i in range(FRAMES):
#         # Move to the left: negative offset (or positive for right)
#         offset = -(i * STEP) % PATTERN_WIDTH
#         frame = draw_frame(offset)
#         frames.append(frame)

#     # Save as animated GIF
#     output_path = "horizontal_conveyor.gif"
#     frames[0].save(
#         output_path,
#         save_all=True,
#         append_images=frames[1:],
#         duration=DURATION_MS,
#         loop=0,
#         optimize=True,
#     )

#     print(f"Saved animated conveyor belt GIF as: {output_path}")


# if __name__ == "__main__":
#     main()



# from PIL import Image, ImageDraw

# # ==========================
# # CONFIG
# # ==========================
# WIDTH, HEIGHT = 900, 320
# BELT_HEIGHT = 90
# BELT_Y_CENTER = HEIGHT // 2
# FRAMES = 40
# STEP = 8
# PATTERN_WIDTH = 50
# DURATION_MS = 70

# # Industrial colors
# BG_COLOR = (20, 22, 30)
# BELT_TOP_COLOR = (90, 90, 95)       # Light top reflection
# BELT_MID_COLOR = (45, 45, 50)       # Dark rubber center
# BELT_BOTTOM_COLOR = (80, 80, 85)    # Bottom reflection
# SLAT_COLOR = (120, 120, 125)
# RAIL_LIGHT = (200, 200, 210)
# RAIL_DARK = (120, 120, 130)
# ROLLER_OUTER = (100, 100, 105)
# ROLLER_INNER = (60, 60, 65)
# ROLLER_CENTER = (30, 30, 35)

# def draw_gradient(draw, x1, y1, x2, y2, start_color, end_color):
#     """Vertical gradient fill."""
#     height = y2 - y1
#     for i in range(height):
#         ratio = i / height
#         r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
#         g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
#         b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
#         draw.line([(x1, y1 + i), (x2, y1 + i)], fill=(r, g, b))


# def draw_roller(draw, cx, cy, radius):
#     """Draws a metallic roller with 3-level shading."""
#     # Outer ring
#     draw.ellipse(
#         [cx - radius, cy - radius, cx + radius, cy + radius],
#         fill=ROLLER_OUTER
#     )
#     # Mid ring
#     draw.ellipse(
#         [cx - radius*0.7, cy - radius*0.7, cx + radius*0.7, cy + radius*0.7],
#         fill=ROLLER_INNER
#     )
#     # Dark center cap
#     draw.ellipse(
#         [cx - radius*0.35, cy - radius*0.35, cx + radius*0.35, cy + radius*0.35],
#         fill=ROLLER_CENTER
#     )


# def draw_frame(offset):
#     img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
#     draw = ImageDraw.Draw(img)

#     # --------------------------
#     # Belt position
#     # --------------------------
#     belt_top = BELT_Y_CENTER - BELT_HEIGHT // 2
#     belt_bottom = BELT_Y_CENTER + BELT_HEIGHT // 2

#     # 3D belt shading: gradient top → mid → bottom
#     belt_mid = (belt_top + belt_bottom) // 2
#     draw_gradient(draw, 0, belt_top, WIDTH, belt_mid, BELT_TOP_COLOR, BELT_MID_COLOR)
#     draw_gradient(draw, 0, belt_mid, WIDTH, belt_bottom, BELT_MID_COLOR, BELT_BOTTOM_COLOR)

#     # --------------------------
#     # Motion slats
#     # --------------------------
#     for x in range(-PATTERN_WIDTH * 2, WIDTH + PATTERN_WIDTH * 2, PATTERN_WIDTH):
#         x_pos = x + offset
#         draw.rectangle(
#             [x_pos, belt_top + 8, x_pos + 14, belt_bottom - 8],
#             fill=SLAT_COLOR
#         )

#     # --------------------------
#     # Top & Bottom Metallic Rails
#     # --------------------------
#     rail_thickness = 28

#     # Top rail (gradient)
#     rail_top_top = belt_top - rail_thickness - 8
#     rail_top_bottom = belt_top - 8
#     draw_gradient(draw, 0, rail_top_top, WIDTH, rail_top_bottom, RAIL_LIGHT, RAIL_DARK)

#     # Bottom rail
#     rail_bottom_top = belt_bottom + 8
#     rail_bottom_bottom = belt_bottom + rail_thickness + 8
#     draw_gradient(draw, 0, rail_bottom_top, WIDTH, rail_bottom_bottom, RAIL_LIGHT, RAIL_DARK)

#     # Shadow under rails
#     shadow_color = (10, 10, 15)
#     draw.rectangle([0, rail_top_bottom, WIDTH, rail_top_bottom + 3], fill=shadow_color)
#     draw.rectangle([0, rail_bottom_top - 3, WIDTH, rail_bottom_top], fill=shadow_color)

#     # --------------------------
#     # Support rollers (under rails)
#     # --------------------------
#     roller_radius = 18
#     spacing = 150

#     for x in range(0, WIDTH, spacing):
#         # bottom rollers
#         draw_roller(draw, x + spacing // 2, rail_bottom_bottom + 5, roller_radius)
#         # top rollers
#         draw_roller(draw, x + spacing // 2, rail_top_top - 5, roller_radius)

#     # --------------------------
#     # Subtle shadow below entire belt
#     # --------------------------
#     draw.rectangle([0, belt_bottom, WIDTH, belt_bottom + 6], fill=(10, 10, 15))

#     return img


# def main():
#     frames = []

#     for i in range(FRAMES):
#         offset = -(i * STEP) % PATTERN_WIDTH
#         frames.append(draw_frame(offset))

#     frames[0].save(
#         "horizontal_conveyor.gif",
#         save_all=True,
#         append_images=frames[1:],
#         duration=DURATION_MS,
#         loop=0,
#         optimize=True,
#     )

#     print("Saved animated conveyor belt GIF as: horizontal_conveyor.gif")


# if __name__ == "__main__":
#     main()


# from PIL import Image, ImageDraw

# # ==========================
# # CONFIG
# # ==========================
# WIDTH, HEIGHT = 900, 320
# BELT_HEIGHT = 90
# BELT_Y_CENTER = HEIGHT // 2
# FRAMES = 40
# STEP = 8
# PATTERN_WIDTH = 55
# DURATION_MS = 70

# # Colors (Image-2 style clean industrial)
# BG_COLOR = (20, 22, 30)

# # Belt shading (smooth clean gradient)
# BELT_TOP = (65, 70, 80)
# BELT_MID = (40, 42, 48)
# BELT_BOTTOM = (55, 60, 68)

# # Slats
# SLAT_COLOR = (160, 160, 165)

# # Rails (smooth single strip, no rollers)
# RAIL_LIGHT = (200, 200, 205)
# RAIL_DARK = (140, 140, 145)

# def draw_gradient(draw, x1, y1, x2, y2, c1, c2):
#     """Vertical gradient fill."""
#     height = y2 - y1
#     for i in range(height):
#         ratio = i / height
#         r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
#         g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
#         b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
#         draw.line([(x1, y1 + i), (x2, y1 + i)], fill=(r, g, b))


# def draw_frame(offset):
#     img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
#     draw = ImageDraw.Draw(img)

#     # --------------------------
#     # Belt area
#     # --------------------------
#     belt_top = BELT_Y_CENTER - BELT_HEIGHT // 2
#     belt_bottom = BELT_Y_CENTER + BELT_HEIGHT // 2
#     belt_mid = (belt_top + belt_bottom) // 2

#     # Smooth 3-level gradient like image-2
#     draw_gradient(draw, 0, belt_top, WIDTH, belt_mid, BELT_TOP, BELT_MID)
#     draw_gradient(draw, 0, belt_mid, WIDTH, belt_bottom, BELT_MID, BELT_BOTTOM)

#     # --------------------------
#     # Belt motion slats (clean and thin)
#     # --------------------------
#     SLAT_WIDTH = 8
#     SLAT_GAP = PATTERN_WIDTH

#     for x in range(-200, WIDTH + 200, SLAT_GAP):
#         x_pos = x + offset
#         draw.rectangle(
#             [x_pos, belt_top + 10, x_pos + SLAT_WIDTH, belt_bottom - 10],
#             fill=SLAT_COLOR
#         )

#     # --------------------------
#     # Modern smooth side rails (no circles)
#     # --------------------------
#     rail_height = 25

#     # Top rail
#     rail_top_y1 = belt_top - rail_height - 10
#     rail_top_y2 = belt_top - 10
#     draw_gradient(draw, 0, rail_top_y1, WIDTH, rail_top_y2, RAIL_LIGHT, RAIL_DARK)

#     # Bottom rail
#     rail_bottom_y1 = belt_bottom + 10
#     rail_bottom_y2 = belt_bottom + rail_height + 10
#     draw_gradient(draw, 0, rail_bottom_y1, WIDTH, rail_bottom_y2, RAIL_LIGHT, RAIL_DARK)

#     # --------------------------
#     # Glossy highlight (industrial shine)
#     # --------------------------
#     highlight_y = belt_top + 8
#     draw.rectangle([0, highlight_y, WIDTH, highlight_y + 2], fill=(220, 220, 230))

#     return img


# def main():
#     frames = []
#     for i in range(FRAMES):
#         offset = -(i * STEP) % PATTERN_WIDTH
#         frames.append(draw_frame(offset))

#     frames[0].save(
#         "horizontal_conveyor.gif",
#         save_all=True,
#         append_images=frames[1:],
#         duration=70,
#         loop=0,
#     )
#     print("Saved: horizontal_conveyor.gif")


# if __name__ == "__main__":
#     main()


# from PIL import Image, ImageDraw
# import random

# # ==========================
# # CONFIG
# # ==========================
# WIDTH, HEIGHT = 900, 320
# BELT_HEIGHT = 90
# BELT_Y_CENTER = HEIGHT // 2
# FRAMES = 40
# STEP = 8
# PATTERN_WIDTH = 55
# DURATION_MS = 70

# # Colors
# BG_COLOR = (18, 20, 28)

# # Belt shading (smooth gradient)
# BELT_TOP = (75, 80, 90)
# BELT_MID = (40, 42, 48)
# BELT_BOTTOM = (60, 65, 72)

# # Slats
# SLAT_COLOR = (165, 165, 170)

# # Rails (premium metallic)
# RAIL_LIGHT = (215, 215, 220)
# RAIL_DARK = (140, 140, 145)

# # Scanner tunnel (transparent)
# SCANNER_COLOR = (0, 150, 255, 70)  # RGBA
# SCANNER_OUTLINE = (150, 200, 255)


# # --------------------------
# # Gradient helper
# # --------------------------
# def draw_gradient(draw, x1, y1, x2, y2, c1, c2):
#     height = y2 - y1
#     for i in range(height):
#         ratio = i / height
#         r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
#         g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
#         b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
#         draw.line([(x1, y1 + i), (x2, y1 + i)], fill=(r, g, b))


# # --------------------------
# # Add subtle rubber texture
# # --------------------------
# def add_texture(img, belt_top, belt_bottom):
#     draw = ImageDraw.Draw(img)
#     for _ in range(4500):  # soft sprinkle
#         x = random.randint(0, WIDTH-1)
#         y = random.randint(belt_top, belt_bottom)
#         shade = random.randint(35, 55)
#         draw.point((x, y), fill=(shade, shade, shade))


# # --------------------------
# # Draw scanner tunnel
# # --------------------------
# def draw_scanner(img, belt_top, belt_bottom):
#     draw = ImageDraw.Draw(img, "RGBA")

#     tunnel_width = 220
#     tunnel_height = BELT_HEIGHT + 40

#     x1 = WIDTH//2 - tunnel_width//2
#     x2 = WIDTH//2 + tunnel_width//2

#     y1 = belt_top - 30
#     y2 = belt_bottom + 30

#     # Transparent glass
#     draw.rectangle([x1, y1, x2, y2], fill=SCANNER_COLOR, outline=SCANNER_OUTLINE)

#     # Top sensor light indicator
#     light_x1 = (x1 + x2) // 2 - 15
#     light_x2 = (x1 + x2) // 2 + 15
#     light_y1 = y1 - 25
#     light_y2 = y1 - 5
#     draw.rectangle([light_x1, light_y1, light_x2, light_y2], fill=(255, 255, 255))


# # --------------------------
# # Build each frame
# # --------------------------
# def draw_frame(offset):
#     img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
#     draw = ImageDraw.Draw(img)

#     belt_top = BELT_Y_CENTER - BELT_HEIGHT // 2
#     belt_bottom = BELT_Y_CENTER + BELT_HEIGHT // 2
#     belt_mid = (belt_top + belt_bottom) // 2

#     # --- Belt shading (3 gradient layers) ---
#     draw_gradient(draw, 0, belt_top, WIDTH, belt_mid, BELT_TOP, BELT_MID)
#     draw_gradient(draw, 0, belt_mid, WIDTH, belt_bottom, BELT_MID, BELT_BOTTOM)

#     # --- Add rubber texture ---
#     add_texture(img, belt_top, belt_bottom)

#     # --- Slats (moving) ---
#     SLAT_WIDTH = 8
#     for x in range(-200, WIDTH + 200, PATTERN_WIDTH):
#         x_pos = x + offset
#         draw.rectangle(
#             [x_pos, belt_top + 12, x_pos + SLAT_WIDTH, belt_bottom - 12],
#             fill=SLAT_COLOR
#         )

#     # --- Rails (metallic gradient) ---
#     rail_height = 25

#     # Top rail
#     top_y1 = belt_top - rail_height - 10
#     top_y2 = belt_top - 10
#     draw_gradient(draw, 0, top_y1, WIDTH, top_y2, RAIL_LIGHT, RAIL_DARK)

#     # Bottom rail
#     bot_y1 = belt_bottom + 10
#     bot_y2 = belt_bottom + rail_height + 10
#     draw_gradient(draw, 0, bot_y1, WIDTH, bot_y2, RAIL_LIGHT, RAIL_DARK)

#     # --- Shadow under rails ---
#     draw.rectangle([0, top_y2, WIDTH, top_y2 + 4], fill=(10, 10, 15))
#     draw.rectangle([0, bot_y1 - 4, WIDTH, bot_y1], fill=(10, 10, 15))

#     # --- Overhead light reflection ---
#     highlight_y = belt_top + 10
#     highlight_height = 6
#     draw.rectangle([0, highlight_y, WIDTH, highlight_y + highlight_height],
#                    fill=(230, 230, 240))

#     # --- Shadow under belt ---
#     draw.rectangle([0, belt_bottom, WIDTH, belt_bottom + 8], fill=(8, 8, 12))

#     # --- Scanner tunnel (glass effect) ---
#     draw_scanner(img, belt_top, belt_bottom)

#     return img


# # --------------------------
# # MAIN
# # --------------------------
# def main():
#     frames = []
#     for i in range(FRAMES):
#         offset = -(i * STEP) % PATTERN_WIDTH
#         frames.append(draw_frame(offset))

#     frames[0].save(
#         "horizontal_conveyor.gif",
#         save_all=True,
#         append_images=frames[1:],
#         duration=DURATION_MS,
#         loop=0,
#     )
#     print("Saved: horizontal_conveyor.gif")


# if __name__ == "__main__":
#     main()


# from PIL import Image, ImageDraw
# import random

# # ==========================(tunnel)
# # CONFIG
# # ==========================
# WIDTH, HEIGHT = 900, 320
# BELT_HEIGHT = 90
# BELT_Y_CENTER = HEIGHT // 2
# FRAMES = 40
# STEP = 8
# PATTERN_WIDTH = 55
# DURATION_MS = 70

# # Colors
# BG_COLOR = (18, 20, 28)

# BELT_TOP = (75, 80, 90)
# BELT_MID = (40, 42, 48)
# BELT_BOTTOM = (60, 65, 72)

# SLAT_COLOR = (165, 165, 170)

# RAIL_LIGHT = (215, 215, 220)
# RAIL_DARK = (140, 140, 145)

# SCANNER_COLOR = (0, 150, 255, 70)  # transparent blue
# SCANNER_OUTLINE = (150, 200, 255)


# # -----------------------------
# # Gradient function
# # -----------------------------
# def draw_gradient(draw, x1, y1, x2, y2, c1, c2):
#     height = y2 - y1
#     for i in range(height):
#         t = i / height
#         r = int(c1[0] * (1 - t) + c2[0] * t)
#         g = int(c1[1] * (1 - t) + c2[1] * t)
#         b = int(c1[2] * (1 - t) + c2[2] * t)
#         draw.line([(x1, y1 + i), (x2, y1 + i)], fill=(r, g, b))


# # -----------------------------
# # Rubber texture on belt
# # -----------------------------
# def add_texture(img, top, bottom):
#     draw = ImageDraw.Draw(img)
#     for _ in range(4500):
#         x = random.randint(0, WIDTH - 1)
#         y = random.randint(top, bottom)
#         shade = random.randint(35, 55)
#         draw.point((x, y), fill=(shade, shade, shade))


# # -----------------------------
# # Draw scanner tunnel
# # -----------------------------
# def draw_scanner(img, belt_top, belt_bottom):
#     draw = ImageDraw.Draw(img, "RGBA")

#     tw = 220
#     x1 = WIDTH // 2 - tw // 2
#     x2 = WIDTH // 2 + tw // 2

#     y1 = belt_top - 30
#     y2 = belt_bottom + 30

#     draw.rectangle([x1, y1, x2, y2], fill=SCANNER_COLOR, outline=SCANNER_OUTLINE)

#     # white sensor light
#     lx1 = (x1 + x2) // 2 - 15
#     lx2 = (x1 + x2) // 2 + 15
#     ly1 = y1 - 25
#     ly2 = y1 - 5

#     draw.rectangle([lx1, ly1, lx2, ly2], fill=(255, 255, 255))


# # -----------------------------
# # Draw one belt frame
# # -----------------------------
# def draw_frame(offset):
#     img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
#     draw = ImageDraw.Draw(img)

#     belt_top = BELT_Y_CENTER - BELT_HEIGHT // 2
#     belt_bottom = BELT_Y_CENTER + BELT_HEIGHT // 2
#     belt_mid = (belt_top + belt_bottom) // 2

#     # Belt shading
#     draw_gradient(draw, 0, belt_top, WIDTH, belt_mid, BELT_TOP, BELT_MID)
#     draw_gradient(draw, 0, belt_mid, WIDTH, belt_bottom, BELT_MID, BELT_BOTTOM)

#     add_texture(img, belt_top, belt_bottom)

#     SLAT_WIDTH = 8
#     for x in range(-200, WIDTH + 200, PATTERN_WIDTH):
#         xx = x + offset
#         draw.rectangle([xx, belt_top + 12, xx + SLAT_WIDTH, belt_bottom - 12], fill=SLAT_COLOR)

#     # Rails
#     rail_h = 25
#     ty1 = belt_top - rail_h - 10
#     ty2 = belt_top - 10
#     draw_gradient(draw, 0, ty1, WIDTH, ty2, RAIL_LIGHT, RAIL_DARK)

#     by1 = belt_bottom + 10
#     by2 = belt_bottom + rail_h + 10
#     draw_gradient(draw, 0, by1, WIDTH, by2, RAIL_LIGHT, RAIL_DARK)

#     draw.rectangle([0, ty2, WIDTH, ty2 + 4], fill=(10, 10, 15))
#     draw.rectangle([0, by1 - 4, WIDTH, by1], fill=(10, 10, 15))

#     draw.rectangle([0, belt_top + 10, WIDTH, belt_top + 16], fill=(230, 230, 240))
#     draw.rectangle([0, belt_bottom, WIDTH, belt_bottom + 8], fill=(8, 8, 12))

#     draw_scanner(img, belt_top, belt_bottom)

#     return img


# # -----------------------------
# # ⭐ REQUIRED FUNCTION
# # -----------------------------
# def generate_belt_frames():
#     frames = []
#     for i in range(FRAMES):
#         offset = -(i * STEP) % PATTERN_WIDTH
#         frames.append(draw_frame(offset))
#     return frames


# # -----------------------------
# # Standalone GIF test
# # -----------------------------
# if __name__ == "__main__":
#     frames = generate_belt_frames()
#     frames[0].save(
#         "horizontal_conveyor.gif",
#         save_all=True,
#         append_images=frames[1:],
#         duration=DURATION_MS,
#         loop=0
#     )
#     print("Saved horizontal_conveyor.gif")


# from PIL import Image, ImageDraw
# import random

# # ==========================(Final)
# # CONFIG
# # ==========================
# WIDTH, HEIGHT = 900, 320
# BELT_HEIGHT = 90
# BELT_Y_CENTER = HEIGHT // 2
# FRAMES = 40
# STEP = 8
# PATTERN_WIDTH = 55
# DURATION_MS = 70

# # Colors
# BG_COLOR = (18, 20, 28)

# BELT_TOP = (75, 80, 90)
# BELT_MID = (40, 42, 48)
# BELT_BOTTOM = (60, 65, 72)

# SLAT_COLOR = (165, 165, 170)

# RAIL_LIGHT = (215, 215, 220)
# RAIL_DARK = (140, 140, 145)


# # -----------------------------
# # Gradient function
# # -----------------------------
# def draw_gradient(draw, x1, y1, x2, y2, c1, c2):
#     height = y2 - y1
#     for i in range(height):
#         t = i / height
#         r = int(c1[0] * (1 - t) + c2[0] * t)
#         g = int(c1[1] * (1 - t) + c2[1] * t)
#         b = int(c1[2] * (1 - t) + c2[2] * t)
#         draw.line([(x1, y1 + i), (x2, y1 + i)], fill=(r, g, b))


# # -----------------------------
# # Rubber texture on belt
# # -----------------------------
# def add_texture(img, top, bottom):
#     draw = ImageDraw.Draw(img)
#     for _ in range(4500):
#         x = random.randint(0, WIDTH - 1)
#         y = random.randint(top, bottom)
#         shade = random.randint(35, 55)
#         draw.point((x, y), fill=(shade, shade, shade))


# # -----------------------------
# # Draw one belt frame
# # -----------------------------
# def draw_frame(offset):
#     img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
#     draw = ImageDraw.Draw(img)

#     belt_top = BELT_Y_CENTER - BELT_HEIGHT // 2
#     belt_bottom = BELT_Y_CENTER + BELT_HEIGHT // 2
#     belt_mid = (belt_top + belt_bottom) // 2

#     # Belt shading
#     draw_gradient(draw, 0, belt_top, WIDTH, belt_mid, BELT_TOP, BELT_MID)
#     draw_gradient(draw, 0, belt_mid, WIDTH, belt_bottom, BELT_MID, BELT_BOTTOM)

#     add_texture(img, belt_top, belt_bottom)

#     SLAT_WIDTH = 8
#     for x in range(-200, WIDTH + 200, PATTERN_WIDTH):
#         xx = x + offset
#         draw.rectangle([xx, belt_top + 12, xx + SLAT_WIDTH, belt_bottom - 12], fill=SLAT_COLOR)

#     # Rails
#     rail_h = 25
#     ty1 = belt_top - rail_h - 10
#     ty2 = belt_top - 10
#     draw_gradient(draw, 0, ty1, WIDTH, ty2, RAIL_LIGHT, RAIL_DARK)

#     by1 = belt_bottom + 10
#     by2 = belt_bottom + rail_h + 10
#     draw_gradient(draw, 0, by1, WIDTH, by2, RAIL_LIGHT, RAIL_DARK)

#     draw.rectangle([0, ty2, WIDTH, ty2 + 4], fill=(10, 10, 15))
#     draw.rectangle([0, by1 - 4, WIDTH, by1], fill=(10, 10, 15))

#     draw.rectangle([0, belt_top + 10, WIDTH, belt_top + 16], fill=(230, 230, 240))
#     draw.rectangle([0, belt_bottom, WIDTH, belt_bottom + 8], fill=(8, 8, 12))

#     return img


# # ==========================
# # Generate Frames (required)
# # ==========================
# def generate_belt_frames():
#     frames = []
#     for i in range(FRAMES):
#         offset = -(i * STEP) % PATTERN_WIDTH
#         frames.append(draw_frame(offset))
#     return frames


# # Standalone test
# if __name__ == "__main__":
#     frames = generate_belt_frames()
#     frames[0].save(
#         "horizontal_conveyor.gif",
#         save_all=True,
#         append_images=frames[1:],
#         duration=DURATION_MS,
#         loop=0
#     )
#     print("Saved horizontal_conveyor.gif")



from PIL import Image, ImageDraw
import random

# ==========================
# CONFIG
# ==========================
WIDTH, HEIGHT = 900, 320
BELT_HEIGHT = 90
BELT_Y_CENTER = HEIGHT // 2
FRAMES = 40
STEP = 8
PATTERN_WIDTH = 55
DURATION_MS = 70

# Colors
BG_COLOR = (18, 20, 28)

BELT_TOP = (75, 80, 90)
BELT_MID = (40, 42, 48)
BELT_BOTTOM = (60, 65, 72)

SLAT_COLOR = (165, 165, 170)

RAIL_LIGHT = (215, 215, 220)
RAIL_DARK = (140, 140, 145)


def draw_gradient(draw, x1, y1, x2, y2, c1, c2):
    height = y2 - y1
    for i in range(height):
        t = i / height
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.line([(x1, y1 + i), (x2, y1 + i)], fill=(r, g, b))


def add_texture(img, top, bottom):
    draw = ImageDraw.Draw(img)
    for _ in range(4500):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(top, bottom)
        shade = random.randint(35, 55)
        draw.point((x, y), fill=(shade, shade, shade))


def draw_frame(offset):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    belt_top = BELT_Y_CENTER - BELT_HEIGHT // 2
    belt_bottom = BELT_Y_CENTER + BELT_HEIGHT // 2
    belt_mid = (belt_top + belt_bottom) // 2

    draw_gradient(draw, 0, belt_top, WIDTH, belt_mid, BELT_TOP, BELT_MID)
    draw_gradient(draw, 0, belt_mid, WIDTH, belt_bottom, BELT_MID, BELT_BOTTOM)

    add_texture(img, belt_top, belt_bottom)

    SLAT_WIDTH = 8
    for x in range(-200, WIDTH + 200, PATTERN_WIDTH):
        xx = x + offset
        draw.rectangle([xx, belt_top + 12, xx + SLAT_WIDTH, belt_bottom - 12], fill=SLAT_COLOR)

    rail_h = 25
    ty1 = belt_top - rail_h - 10
    ty2 = belt_top - 10
    draw_gradient(draw, 0, ty1, WIDTH, ty2, RAIL_LIGHT, RAIL_DARK)

    by1 = belt_bottom + 10
    by2 = belt_bottom + rail_h + 10
    draw_gradient(draw, 0, by1, WIDTH, by2, RAIL_LIGHT, RAIL_DARK)

    draw.rectangle([0, ty2, WIDTH, ty2 + 4], fill=(10, 10, 15))
    draw.rectangle([0, by1 - 4, WIDTH, by1], fill=(10, 10, 15))

    draw.rectangle([0, belt_top + 10, WIDTH, belt_top + 16], fill=(230, 230, 240))
    draw.rectangle([0, belt_bottom, WIDTH, belt_bottom + 8], fill=(8, 8, 12))

    return img


def generate_belt_frames():
    frames = []
    for i in range(FRAMES):
        offset = -(i * STEP) % PATTERN_WIDTH
        frames.append(draw_frame(offset))
    return frames


if __name__ == "__main__":
    frames = generate_belt_frames()
    frames[0].save(
        "horizontal_conveyor.gif",
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0
    )
    print("Saved horizontal_conveyor.gif")


