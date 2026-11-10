"""YOLO ONNX inference for prerecorded video frames; does not control a game."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np
import onnxruntime as ort

import config


class Vision:
    def __init__(self, model_path: str | Path = config.MODEL_PATH) -> None:
        model_path = Path(model_path)
        if not model_path.is_file():
            raise FileNotFoundError(
                f"ONNX model not found: {model_path}. Add a model you are authorized to use."
            )
        self.session = ort.InferenceSession(
            str(model_path), providers=["CPUExecutionProvider"]
        )
        self.input_name = self.session.get_inputs()[0].name

    def detect(self, frame: np.ndarray) -> list[dict[str, Any]]:
        """Return detections for one supplied, prerecorded frame."""
        if frame is None or frame.ndim != 3:
            raise ValueError("frame must be a non-empty OpenCV color image")
        height, width = frame.shape[:2]
        resized = cv2.resize(frame, (config.INPUT_SIZE, config.INPUT_SIZE))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        tensor = np.ascontiguousarray(rgb.transpose(2, 0, 1)[None], dtype=np.float32) / 255.0
        outputs = self.session.run(None, {self.input_name: tensor})
        if not outputs:
            return []

        predictions = np.asarray(outputs[0])
        if predictions.ndim == 3:
            predictions = predictions[0]
        # YOLOv8 ONNX exports commonly use [4 + classes, candidates].
        if predictions.ndim != 2:
            raise ValueError(f"Unsupported model output shape: {predictions.shape}")
        if predictions.shape[0] < predictions.shape[1]:
            predictions = predictions.T
        class_count = len(config.CLASS_NAMES)
        if predictions.shape[1] < 4 + class_count:
            raise ValueError(
                "Model output does not match configured classes; check model metadata and CLASS_NAMES."
            )

        boxes_xywh = predictions[:, :4]
        scores = predictions[:, 4 : 4 + class_count]
        class_ids = scores.argmax(axis=1)
        confidences = scores[np.arange(len(scores)), class_ids]
        selected = np.flatnonzero(confidences >= config.CONFIDENCE_THRESHOLD)
        if not len(selected):
            return []

        # Convert normalized-to-model pixel coordinates from center xywh to frame xyxy.
        scale_x, scale_y = width / config.INPUT_SIZE, height / config.INPUT_SIZE
        boxes: list[list[int]] = []
        kept_scores: list[float] = []
        kept_ids: list[int] = []
        for idx in selected:
            cx, cy, bw, bh = boxes_xywh[idx]
            x1 = max(0, min(width, round((cx - bw / 2) * scale_x)))
            y1 = max(0, min(height, round((cy - bh / 2) * scale_y)))
            x2 = max(0, min(width, round((cx + bw / 2) * scale_x)))
            y2 = max(0, min(height, round((cy + bh / 2) * scale_y)))
            boxes.append([x1, y1, max(0, x2 - x1), max(0, y2 - y1)])
            kept_scores.append(float(confidences[idx]))
            kept_ids.append(int(class_ids[idx]))

        # NMS removes duplicate boxes. It is for reporting only; no actions are issued.
        keep = cv2.dnn.NMSBoxes(
            boxes, kept_scores, config.CONFIDENCE_THRESHOLD, 0.45
        )
        if len(keep) == 0:
            return []
        detections = []
        for raw_index in np.asarray(keep).reshape(-1):
            x, y, w, h = boxes[int(raw_index)]
            class_id = kept_ids[int(raw_index)]
            detections.append({
                "class": config.CLASS_NAMES[class_id],
                "bbox": [x, y, x + w, y + h],
                "conf": round(kept_scores[int(raw_index)], 4),
            })
        return detections
