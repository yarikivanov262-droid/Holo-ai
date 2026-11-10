# Holo AI — offline video analysis prototype

This repository includes a responsive project dashboard and a small Python scaffold for **passive analysis of prerecorded video files**. It does not connect to an emulator or control a game.

## Python setup

```bash
python -m pip install -r requirements.txt
```

Place an ONNX model that you are authorized to use at `models/holo_yolo.onnx`. Check that the model's class order matches `CLASS_NAMES` in `config.py` and that the exported output layout is compatible with the decoder. Model exports vary, so validate against the model's own documentation before relying on the results.

Run analysis on a local video file:

```bash
python main.py path/to/prerecorded-video.mp4
```

By default, the CSV report is saved under `data/reports/`. To choose another destination:

```bash
python main.py path/to/prerecorded-video.mp4 --output data/reports/session.csv
```

## Scope

The Python workflow reads a supplied video file, runs ONNX inference on its frames, and writes detections to CSV. It does not capture live gameplay, connect to ADB, send touch events, aim, navigate, or start/stop gameplay. No credentials or external game API calls are required.

See `PROGRESS.md` for the completed and remaining work.
