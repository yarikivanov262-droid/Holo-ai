"""Analyze a prerecorded video and write detection observations to CSV.

This module deliberately has no emulator connection, input injection, aiming,
movement, or gameplay-control functions.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import cv2

from core.vision import Vision


class VideoAnalyzer:
    def __init__(self, vision: Vision) -> None:
        self.vision = vision

    def analyze(self, video_path: str | Path, csv_path: str | Path) -> int:
        source = Path(video_path)
        if not source.is_file():
            raise FileNotFoundError(f"Video not found: {source}")
        capture = cv2.VideoCapture(str(source))
        if not capture.isOpened():
            raise RuntimeError(f"Could not open video: {source}")

        destination = Path(csv_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        frame_index = 0
        count = 0
        try:
            with destination.open("w", newline="", encoding="utf-8") as report:
                writer = csv.DictWriter(
                    report,
                    fieldnames=["frame", "time_seconds", "class", "confidence", "x1", "y1", "x2", "y2"],
                )
                writer.writeheader()
                fps = capture.get(cv2.CAP_PROP_FPS) or 0.0
                while True:
                    ok, frame = capture.read()
                    if not ok:
                        break
                    for item in self.vision.detect(frame):
                        x1, y1, x2, y2 = item["bbox"]
                        writer.writerow({
                            "frame": frame_index,
                            "time_seconds": round(frame_index / fps, 3) if fps > 0 else "",
                            "class": item["class"],
                            "confidence": item["conf"],
                            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                        })
                        count += 1
                    frame_index += 1
        finally:
            capture.release()
        return count
