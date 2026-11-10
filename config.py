"""Configuration for offline video analysis only."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
MODEL_PATH = ROOT_DIR / "models" / "holo_yolo.onnx"
OUTPUT_DIR = ROOT_DIR / "data" / "reports"
CLASS_NAMES = ["target", "obstacle", "item", "player"]
CONFIDENCE_THRESHOLD = 0.5
INPUT_SIZE = 640
