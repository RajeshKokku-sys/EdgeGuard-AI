# EdgeGuard AI

Intelligent Edge AI Security Surveillance Platform.

This repository is organized around production-style modules instead of a single script. The current milestone adds a multi-camera architecture with separate camera and detection abstractions.

## Current Milestone

- Camera abstraction through `camera.CameraManager`
- Multi-camera orchestration through `camera.MultiCameraManager`
- Person detection abstraction through `detection.PersonDetector`
- Central settings in `config.settings`
- Simple runnable entrypoint in `app.main`

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
python -m app.main
```

By default, the sample config uses local webcam source `0`. Update `config/settings.py` to add RTSP streams, USB cameras, or video files.
