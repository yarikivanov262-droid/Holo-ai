"""Offline prerecorded-video analysis entry point."""
from __future__ import annotations

import argparse
from pathlib import Path

import config
from core.vision import Vision
from logic.video_analysis import VideoAnalyzer


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze a prerecorded video and save object observations as CSV."
    )
    parser.add_argument("video", type=Path, help="Path to a local prerecorded video")
    parser.add_argument(
        "--output", type=Path,
        help="CSV output path (default: data/reports/<video-name>.csv)",
    )
    args = parser.parse_args()
    output = args.output or config.OUTPUT_DIR / f"{args.video.stem}.csv"

    analyzer = VideoAnalyzer(Vision())
    count = analyzer.analyze(args.video, output)
    print(f"Offline analysis complete: {count} observations saved to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
