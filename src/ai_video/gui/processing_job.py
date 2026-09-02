from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProcessingJob:
    """描述一次影片處理工作所需的資料。"""

    input_path: Path
    output_path: Path
    temp_output_path: Path
    detector: str
    tracker: str
    renderer: str