import argparse
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

DEFAULT_ITERATIONS = 1000
DEFAULT_BLUR_SIZES = [15, 31, 51, 71]


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark AI-Video renderers.",
    )

    parser.add_argument(
        "--loops",
        type=int,
        default=DEFAULT_ITERATIONS,
        help=(
            "Number of benchmark iterations "
            f"(default: {DEFAULT_ITERATIONS})."
        ),
    )

    parser.add_argument(
        "--blur-sizes",
        type=int,
        nargs="+",
        default=DEFAULT_BLUR_SIZES,
        help=(
            "Blur strengths to benchmark "
            "(default: 15 31 51 71)."
        ),
    )

    return parser


def validate_arguments(
    parser: argparse.ArgumentParser,
    loops: int,
    blur_sizes: list[int],
) -> None:
    if loops <= 0:
        parser.error("--loops must be greater than zero.")

    for blur_size in blur_sizes:
        if blur_size <= 0:
            parser.error(
                "--blur-sizes values must be greater than zero."
            )

        if blur_size % 2 == 0:
            parser.error(
                "--blur-sizes values must be odd numbers."
            )


def benchmark(
    renderer,
    name: str,
    frame: np.ndarray,
    iterations: int,
) -> None:
    start = perf_counter()

    for _ in range(iterations):
        working_frame = frame.copy()

        renderer.render(
            working_frame,
            BOX,
        )

    elapsed = perf_counter() - start

    fps = iterations / elapsed
    milliseconds_per_frame = (
        elapsed * 1000 / iterations
    )

    print(
        f"{name:<12}"
        f"{fps:9.2f} FPS"
        f"{milliseconds_per_frame:10.2f} ms/frame"
    )


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    validate_arguments(
        parser,
        args.loops,
        args.blur_sizes,
    )

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

    benchmarks = []

    for blur_size in args.blur_sizes:
        benchmarks.append(
            (
                f"Blur-{blur_size}",
                "blur",
                blur_size,
                12,
            )
        )

    benchmarks.extend(
        [
            (
                "Pixelate",
                "pixelate",
                51,
                12,
            ),
            (
                "Solid",
                "solid",
                51,
                12,
            ),
        ]
    )

    print()
    print("=" * 54)
    print("AI-Video Renderer Benchmark")
    print("=" * 54)
    print(
        f"Frame : {FRAME_WIDTH} x {FRAME_HEIGHT}"
    )
    print(
        f"ROI   : {BOX}"
    )
    print(
        f"Loops : {args.loops}"
    )
    print("-" * 54)

    for (
        name,
        renderer_type,
        blur_strength,
        pixel_size,
    ) in benchmarks:
        renderer = RendererFactory.create(
            renderer_type=renderer_type,
            blur_strength=blur_strength,
            pixel_size=pixel_size,
        )

        benchmark(
            renderer=renderer,
            name=name,
            frame=frame,
            iterations=args.loops,
        )

    print("=" * 54)


if __name__ == "__main__":
    main()