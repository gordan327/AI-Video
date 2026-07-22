from time import perf_counter

import numpy as np

from ai_video.renderer.renderer_factory import RendererFactory


FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

BOX = (
    400,
    150,
    880,
    650,
)

ITERATIONS = 1000


def benchmark(renderer, name: str):
    frame = np.random.randint(
        0,
        255,
        (
            FRAME_HEIGHT,
            FRAME_WIDTH,
            3,
        ),
        dtype=np.uint8,
    )

    start = perf_counter()

    for _ in range(ITERATIONS):
        working = frame.copy()
        renderer.render(
            working,
            BOX,
    )

    elapsed = perf_counter() - start

    fps = ITERATIONS / elapsed
    ms = elapsed * 1000 / ITERATIONS

    print(
        f"{name:<10}"
        f"{fps:8.2f} FPS"
        f"   {ms:7.2f} ms/frame"
    )


def main():
    print()
    print("=" * 50)
    print("AI-Video Renderer Benchmark")
    print("=" * 50)
    print(
        f"Frame : {FRAME_WIDTH} x {FRAME_HEIGHT}"
    )
    print(
        f"ROI   : {BOX}"
    )
    print(
        f"Loops : {ITERATIONS}"
    )
    
    print("-" * 50)

    benchmarks = [
        ("Blur-15", "blur", 15, 12),
        ("Blur-31", "blur", 31, 12),
        ("Blur-51", "blur", 51, 12),
        ("Blur-71", "blur", 71, 12),
        ("Pixelate", "pixelate", 51, 12),
        ("Solid", "solid", 51, 12),
    ]

    for name, renderer_type, blur_strength, pixel_size in benchmarks:
        renderer = RendererFactory.create(
            renderer_type=renderer_type,
            blur_strength=blur_strength,
            pixel_size=pixel_size,
        )

        benchmark(renderer, name)

    print("=" * 50)


if __name__ == "__main__":
    main()