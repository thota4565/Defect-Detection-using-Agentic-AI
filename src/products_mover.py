# import os
# import random
# from PIL import Image

# # ========================================================
# # CONFIG
# # ========================================================
# DEFECT_PATH = r"C:\Defect detection using agentic ai\data\casting_data\test\def_front"
# OK_PATH     = r"C:\Defect detection using agentic ai\data\casting_data\test\ok_front"

# N_DEFECT = 5
# N_OK = 5

# PRODUCT_WIDTH = 120
# PRODUCT_HEIGHT = 120

# PRODUCT_Y = 100      # adjust based on belt center
# MOVE_STEPS = 30      # MUCH LOWER so memory OK


# # ========================================================
# # Load images
# # ========================================================
# def load_sample_images():
#     defect_files = random.sample(
#         [os.path.join(DEFECT_PATH, f) for f in os.listdir(DEFECT_PATH)],
#         N_DEFECT
#     )

#     ok_files = random.sample(
#         [os.path.join(OK_PATH, f) for f in os.listdir(OK_PATH)],
#         N_OK
#     )

#     products = (
#         [{"path": p, "label": "defective"} for p in defect_files] +
#         [{"path": p, "label": "ok"} for p in ok_files]
#     )

#     random.shuffle(products)
#     return products


# # ========================================================
# # Move product left → right across ONE belt frame
# # ========================================================
# def move_product(belt_frame, product_img):
#     frames = []

#     # Resize product
#     product_img = product_img.resize((PRODUCT_WIDTH, PRODUCT_HEIGHT)).convert("RGBA")

#     start_x = -PRODUCT_WIDTH
#     end_x = belt_frame.width

#     step_x = (end_x - start_x) / MOVE_STEPS

#     for i in range(MOVE_STEPS):
#         frame = belt_frame.copy()
#         x = int(start_x + i * step_x)
#         frame.paste(product_img, (x, PRODUCT_Y), product_img)
#         frames.append(frame)

#     return frames


# # ========================================================
# # MAIN ENTRY for main.py
# # ========================================================
# def generate_product_frames(belt_frames):
#     # Use ONLY the first belt frame → avoids 40× duplication
#     base_belt = belt_frames[0]

#     products = load_sample_images()
#     output_frames = []

#     for product in products:
#         img = Image.open(product["path"]).convert("RGBA")
#         frames = move_product(base_belt, img)

#         for f in frames:
#             output_frames.append({"frame": f, "label": product["label"]})

#     return output_frames


# # Test
# if __name__ == "__main__":
#     print("products_mover ready")

# import os
# import random
# from PIL import Image

# # ========================================================(Final)
# # CONFIG
# # ========================================================
# DEFECT_PATH = r"C:\Defect detection using agentic ai\data\casting_data\test\def_front"
# OK_PATH     = r"C:\Defect detection using agentic ai\data\casting_data\test\ok_front"

# N_DEFECT = 5
# N_OK = 5

# PRODUCT_WIDTH = 120
# PRODUCT_HEIGHT = 120

# PRODUCT_Y = 100          # height on belt
# MOVE_STEPS = 150         # total frames of movement
# SPACING = 180            # distance between products on the belt


# # ========================================================
# # Load images
# # ========================================================
# def load_sample_images():
#     defect_files = random.sample(
#         [os.path.join(DEFECT_PATH, f) for f in os.listdir(DEFECT_PATH)],
#         N_DEFECT
#     )

#     ok_files = random.sample(
#         [os.path.join(OK_PATH, f) for f in os.listdir(OK_PATH)],
#         N_OK
#     )

#     products = (
#         [{"path": p, "label": "defective"} for p in defect_files] +
#         [{"path": p, "label": "ok"} for p in ok_files]
#     )

#     random.shuffle(products)
#     return products


# # ========================================================
# # All products move TOGETHER on the SAME belt
# # ========================================================
# def generate_product_frames(belt_frames):

#     base_belt = belt_frames  # ← use moving belt, not static
#     num_frames = len(base_belt)   # usually 40 frames repeating

#     products = load_sample_images()

#     # Load and resize all product images
#     product_imgs = []
#     for p in products:
#         img = Image.open(p["path"]).convert("RGBA")
#         img = img.resize((PRODUCT_WIDTH, PRODUCT_HEIGHT))
#         product_imgs.append({"img": img, "label": p["label"]})

#     # Assign initial X positions for spacing
#     for i, prod in enumerate(product_imgs):
#         prod["x"] = -PRODUCT_WIDTH - (i * SPACING)  # staggered

#     # Total frames for output
#     output_frames = []

#     # Movement logic
#     for step in range(MOVE_STEPS):
#         # Get cycling belt frame
#         belt = base_belt[step % num_frames].copy()

#         # Move each product
#         for prod in product_imgs:
#             prod["x"] += 4   # move speed (increase for faster)

#             # Draw product on belt
#             belt.paste(prod["img"], (prod["x"], PRODUCT_Y), prod["img"])

#         output_frames.append({"frame": belt, "label": None})

#     return output_frames


# # Test
# if __name__ == "__main__":
#     print("products_mover ready")


import os
import random
from PIL import Image

# ========================================================
# CONFIG
# ========================================================
DEFECT_PATH = r"C:\Defect detection using agentic ai\data\casting_data\test\def_front"
OK_PATH     = r"C:\Defect detection using agentic ai\data\casting_data\test\ok_front"

N_DEFECT = 5
N_OK = 5

PRODUCT_WIDTH  = 90
PRODUCT_HEIGHT = 90
PRODUCT_Y = 115

MOVE_STEPS = 180
SPACING = 220
SPEED = 3   # pixels per frame


def load_sample_images():
    defect_files = random.sample(
        [os.path.join(DEFECT_PATH, f) for f in os.listdir(DEFECT_PATH)],
        N_DEFECT
    )
    ok_files = random.sample(
        [os.path.join(OK_PATH, f) for f in os.listdir(OK_PATH)],
        N_OK
    )

    products = (
        [{"path": p, "label": "defective"} for p in defect_files] +
        [{"path": p, "label": "ok"} for p in ok_files]
    )

    random.shuffle(products)
    return products


def generate_product_frames(belt_frames):

    belt_count = len(belt_frames)
    products = load_sample_images()

    product_imgs = []
    for p in products:
        img = Image.open(p["path"]).convert("RGBA")
        img = img.resize((PRODUCT_WIDTH, PRODUCT_HEIGHT))
        product_imgs.append({"img": img, "label": p["label"]})

    for i, p in enumerate(product_imgs):
        p["x"] = -PRODUCT_WIDTH - (i * SPACING)

    output_frames = []

    for step in range(MOVE_STEPS):

        belt = belt_frames[step % belt_count].copy()

        for p in product_imgs:
            p["x"] += SPEED
            belt.paste(p["img"], (p["x"], PRODUCT_Y), p["img"])

        output_frames.append({"frame": belt})

    return output_frames


if __name__ == "__main__":
    print("products_mover ready")



