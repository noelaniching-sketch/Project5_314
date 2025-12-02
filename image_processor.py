from pathlib import Path
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow is not installed. Install with: python3 -m pip install pillow")
    sys.exit(1)


def load_image(path):
    return Image.open(path)


def resize_image(img, width=None, height=None):
    if width is None and height is None:
        return img
    w, h = img.size
    if width is None:
        # preserve aspect ratio using height
        ratio = height / h
        width = int(w * ratio)
    elif height is None:
        ratio = width / w
        height = int(h * ratio)
    return img.resize((width, height), Image.LANCZOS)


def to_grayscale(img):
    return img.convert("L")


def save_image(img, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return out_path


def make_default_outpath(input_path):
    p = Path(input_path)
    return p.with_name(p.stem + "_processed" + p.suffix)


def main(argv):
    import argparse

    parser = argparse.ArgumentParser(description="Simple image processor (resize / grayscale / save).")
    parser.add_argument("input", help="input image file path")
    parser.add_argument("-o", "--output", help="output file path (optional)")
    parser.add_argument("--width", type=int, help="resize width in pixels")
    parser.add_argument("--height", type=int, help="resize height in pixels")
    parser.add_argument("--grayscale", action="store_true", help="convert to grayscale")
    args = parser.parse_args(argv)

    inp = Path(args.input)
    if not inp.exists():
        print(f"ERROR: input file not found: {inp}")
        return 2

    try:
        img = load_image(inp)
    except Exception as e:
        print("ERROR loading image:", e)
        return 3

    img = resize_image(img, width=args.width, height=args.height)
    if args.grayscale:
        img = to_grayscale(img)

    out_path = args.output or make_default_outpath(inp)
    try:
        saved = save_image(img, out_path)
    except Exception as e:
        print("ERROR saving image:", e)
        return 4

    print(f"Saved processed image to: {saved}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))