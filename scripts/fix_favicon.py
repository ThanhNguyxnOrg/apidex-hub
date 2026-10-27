#!/usr/bin/env python3
"""Remove a dark matte from APIDex Hub's legacy favicon and write real ICO/PNG assets.

The old site/public/favicon.ico is actually a PNG file. This script keeps the
existing minimal network-mark design, removes only the dark background region
connected to the canvas edge, and exports a transparent PNG plus a real ICO.

Once favicon.png exists, it is treated as the transparent source on later runs.
Delete it only when intentionally reprocessing a newly replaced legacy source.
"""

from collections import deque
from pathlib import Path
from statistics import median

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "site" / "public"
ICO_PATH = PUBLIC / "favicon.ico"
PNG_PATH = PUBLIC / "favicon.png"
MAX_BACKGROUND_DISTANCE = 150
BACKGROUND_NOISE_FLOOR = 5


def rgb_distance(pixel, background):
    return max(abs(pixel[i] - background[i]) for i in range(3))


def estimate_background(image):
    """Estimate the matte from dark, opaque pixels around the canvas edge."""
    width, height = image.size
    edge = []

    for x in range(width):
        edge.extend((image.getpixel((x, 0)), image.getpixel((x, height - 1))))
    for y in range(1, height - 1):
        edge.extend((image.getpixel((0, y)), image.getpixel((width - 1, y))))

    samples = [
        pixel[:3]
        for pixel in edge
        if pixel[3] > 128 and max(pixel[:3]) < 100
    ]

    if not samples:
        samples = [
            pixel[:3]
            for pixel in image.getdata()
            if pixel[3] > 200 and max(pixel[:3]) < 100
        ]

    if not samples:
        return (0, 0, 0)

    return tuple(int(median(channel)) for channel in zip(*samples))


def remove_edge_background(image):
    """Build an alpha matte only for dark pixels connected to the image edge."""
    image = image.convert("RGBA")
    width, height = image.size
    pixels = list(image.getdata())
    background = estimate_background(image)
    max_contrast = max(max(255 - channel, channel) for channel in background)
    visited = bytearray(width * height)
    queue = deque()

    def eligible(index):
        pixel = pixels[index]
        return rgb_distance(pixel, background) <= MAX_BACKGROUND_DISTANCE

    def seed(index):
        if not visited[index] and eligible(index):
            visited[index] = 1
            queue.append(index)

    for x in range(width):
        seed(x)
        seed((height - 1) * width + x)
    for y in range(height):
        seed(y * width)
        seed(y * width + width - 1)

    while queue:
        index = queue.popleft()
        x = index % width
        y = index // width

        if x > 0:
            seed(index - 1)
        if x + 1 < width:
            seed(index + 1)
        if y > 0:
            seed(index - width)
        if y + 1 < height:
            seed(index + width)

    cleaned = []
    for index, pixel in enumerate(pixels):
        if not visited[index]:
            cleaned.append(pixel)
            continue

        delta = rgb_distance(pixel, background)
        if delta <= BACKGROUND_NOISE_FLOOR or pixel[3] == 0:
            cleaned.append((0, 0, 0, 0))
            continue

        # Un-matte the color so the edge keeps its intended hue when displayed
        # on a non-black page, while preserving its appearance on the old matte.
        matte_alpha = min(1.0, delta / max_contrast)
        if matte_alpha <= 0:
            cleaned.append((0, 0, 0, 0))
            continue

        foreground = tuple(
            max(0, min(255, round(background[channel] +
                                  (pixel[channel] - background[channel]) / matte_alpha)))
            for channel in range(3)
        )
        alpha = max(0, min(255, round(pixel[3] * matte_alpha)))
        cleaned.append((*foreground, alpha) if alpha else (0, 0, 0, 0))

    result = Image.new("RGBA", image.size)
    result.putdata(cleaned)
    return result, background, sum(1 for hit in visited if hit)


def main():
    PUBLIC.mkdir(parents=True, exist_ok=True)

    # First run reads the legacy PNG disguised as .ico. Future runs use the
    # transparent PNG that this script produced, making the operation stable.
    if PNG_PATH.exists():
        with Image.open(PNG_PATH) as existing:
            icon = existing.convert("RGBA")
        background = None
        processed_pixels = 0
    else:
        with Image.open(ICO_PATH) as legacy:
            icon = legacy.convert("RGBA")
        icon, background, processed_pixels = remove_edge_background(icon)

    if icon.width != icon.height:
        raise ValueError(f"Favicon must be square, got {icon.size}")

    icon.save(PNG_PATH, format="PNG", optimize=True)
    icon.save(ICO_PATH, format="ICO", sizes=[(16, 16), (32, 32)])

    with Image.open(PNG_PATH) as check:
        check.load()
        if check.mode != "RGBA":
            raise RuntimeError(f"Expected RGBA favicon, got {check.mode}")
        corner_alpha = [check.getpixel(point)[3] for point in
                        ((0, 0), (check.width - 1, 0),
                         (0, check.height - 1), (check.width - 1, check.height - 1))]
        print(
            f"Created transparent PNG {check.size}; corner alpha={corner_alpha}; "
            f"source matte={background}; processed pixels={processed_pixels}"
        )

    with Image.open(ICO_PATH) as check:
        if check.format != "ICO":
            raise RuntimeError(f"Expected real ICO format, got {check.format}")
        print(f"Created valid ICO with frames: {check.ico.sizes()}")


if __name__ == "__main__":
    main()
