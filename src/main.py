from conveyor_belt import generate_belt_frames
from products_mover import generate_product_frames
from PIL import Image

def main():
    print("Generating belt frames...")
    belt_frames = generate_belt_frames()

    print("Generating product movement frames...")
    product_frames = generate_product_frames(belt_frames)

    print("Preparing frames for GIF...")
    frames = []

    for pf in product_frames:
        if isinstance(pf, dict) and "frame" in pf:
            frm = pf["frame"]
            if isinstance(frm, Image.Image):
                frames.append(frm)
        elif isinstance(pf, Image.Image):
            frames.append(pf)

    if not frames:
        print("ERROR: No frames generated. Check products_mover output.")
        return

    print("Converting frames safely...")
    safe_frames = []
    for f in frames:
        try:
            safe_frames.append(f.convert("RGB"))
        except Exception as e:
            print("Frame conversion error:", e)

    if not safe_frames:
        print("ERROR: Frames could not be converted.")
        return

    print("Saving preview animation...")
    safe_frames[0].save(
        "preview_conveyor.gif",
        save_all=True,
        append_images=safe_frames[1:],
        duration=80,   # smoother movement (80 ms between frames)
        loop=0
    )

    print("Saved: preview_conveyor.gif")

if __name__ == "__main__":
    main()



