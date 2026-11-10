# Holo AI — status and checklist

Last update: offline video-analysis scaffold.

## Completed

- [x] Created the `core`, `logic`, `telegram_bot`, `models`, and `data` project directories (empty asset/output directories are represented by this checklist until files are added).
- [x] Added Python dependency list for OpenCV, NumPy, and ONNX Runtime.
- [x] Added configuration with model path, class labels, input size, and confidence threshold; no secrets are embedded.
- [x] Added ONNX inference for supplied image frames.
- [x] Added a prerecorded-video analyzer that writes detections to CSV.
- [x] Added a command-line entry point for offline analysis.

## Remaining

- [ ] Add an authorized ONNX model to `models/holo_yolo.onnx` and verify its output tensor layout and class order.
- [ ] Install requirements and run a test against a video file that you are authorized to analyze.
- [ ] Add unit tests for model output decoding and CSV reporting.
- [ ] Decide whether a permitted, non-gameplay reporting integration is needed.

## Intentionally not included

- Emulator/ADB connection, screenshots from a live game, touch/swipe injection, aiming or gameplay automation.
- Gameplay FSM, remote start/stop controls for a live game, external game-account API access, or anti-cheat evasion.

The implemented workflow only reads a local prerecorded video and writes observations. It does not issue game inputs.
