class PerformanceReporter:
    """產生並輸出影片處理效能報告。"""

    @staticmethod
    def print_report(
        *,
        frame_count: int,
        processing_time: float,
        detector_time: float,
        tracker_time: float,
        renderer_time: float,
        writer_time: float,
    ) -> None:
        """輸出各處理模組的效能統計。"""

        if frame_count == 0:
            print("沒有可供統計的影格。")
            return

        measured_time = (
            detector_time
            + tracker_time
            + renderer_time
            + writer_time
        )

        other_time = max(
            0.0,
            processing_time - measured_time,
        )

        def average_ms(
            total_time: float,
        ) -> float:
            return (
                total_time
                / frame_count
                * 1000
            )

        def percentage(
            total_time: float,
        ) -> float:
            if processing_time <= 0:
                return 0.0

            return (
                total_time
                / processing_time
                * 100
            )

        processing_fps = (
            frame_count / processing_time
            if processing_time > 0
            else 0.0
        )

        print()
        print("=" * 58)
        print("AI-Video Module Performance")
        print("=" * 58)
        print(
            f"Frames          : "
            f"{frame_count}"
        )
        print(
            f"Processing Time : "
            f"{processing_time:.2f} sec"
        )
        print(
            f"Processing FPS  : "
            f"{processing_fps:.2f}"
        )
        print("-" * 58)

        print(
            f"Detection       : "
            f"{detector_time:8.2f} sec | "
            f"{average_ms(detector_time):7.2f} "
            f"ms/frame | "
            f"{percentage(detector_time):6.2f}%"
        )

        print(
            f"Tracking        : "
            f"{tracker_time:8.2f} sec | "
            f"{average_ms(tracker_time):7.2f} "
            f"ms/frame | "
            f"{percentage(tracker_time):6.2f}%"
        )

        print(
            f"Rendering       : "
            f"{renderer_time:8.2f} sec | "
            f"{average_ms(renderer_time):7.2f} "
            f"ms/frame | "
            f"{percentage(renderer_time):6.2f}%"
        )

        print(
            f"Video Writing   : "
            f"{writer_time:8.2f} sec | "
            f"{average_ms(writer_time):7.2f} "
            f"ms/frame | "
            f"{percentage(writer_time):6.2f}%"
        )

        print(
            f"Other / Reading : "
            f"{other_time:8.2f} sec | "
            f"{average_ms(other_time):7.2f} "
            f"ms/frame | "
            f"{percentage(other_time):6.2f}%"
        )

        print("=" * 58)
