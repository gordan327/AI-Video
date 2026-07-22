# AI-Video

> **Privacy-first AI Video Framework for Face Detection, Tracking and Anonymization**

AI-Video is an open-source, plugin-based framework for privacy-preserving video processing.

Originally developed to protect the privacy of children during educational activities, AI-Video has evolved into a reusable framework for building AI-powered video anonymization applications.

Unlike traditional face-blurring tools, AI-Video is designed with software engineering principles that emphasize long-term maintainability, extensibility, and reliability.

---

## Why AI-Video?

Most video anonymization software focuses on producing blurred faces.

AI-Video focuses on building a **privacy framework**.

Its architecture allows developers to replace or extend every major component—including face detectors, trackers, renderers, and future AI modules—without modifying the processing pipeline.

Core design principles:

- 🔒 Privacy First
- 🔌 Plugin Architecture
- 🧩 Extensible Design
- 🏗 Maintainable Codebase
- ✅ Well Tested
- 📚 Well Documented
- ❤️ Open Source

---

## Features

Current Version provides:

- 🎯 SCRFD Face Detection
- 🎯 ByteTrack Face Tracking
- 🎯 Smart Privacy Region
- 🎯 Temporal Region Cache
- 🎯 Prediction Freeze
- 🎯 Gaussian Blur Renderer
- 🎯 Pixelate Renderer
- 🎯 Solid Color Renderer
- 🎯 Desktop GUI
- 🎯 Command Line Interface (CLI)
- 🎯 Plugin-based Architecture
- 🎯 Factory Pattern
- 🎯 YAML Configuration
- 🎯 Automatic Audio Preservation (FFmpeg)
- 🎯 109 Automated Tests
- 🎯 GitHub Actions Continuous Integration

---

# Quick Start

Clone the repository.

```bash
git clone https://github.com/gordan327/AI-Video.git
cd AI-Video
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

macOS / Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install AI-Video.

```bash
pip install -e .
```

Launch the desktop application.

```bash
ai-video-gui
```

Or use the command line interface.

```bash
ai-video --help
```

---

# Requirements

- Python 3.11 or newer
- FFmpeg
- macOS
- Linux (experimental)
- Windows support planned for Version 1.x

---

# Example Workflow

Desktop GUI

1. Select an input video.
2. Choose an output location.
3. Select the desired anonymization renderer.
4. Click **Start**.

AI-Video automatically:

- detects faces,
- tracks identities across frames,
- preserves the original frame rate,
- preserves the original resolution,
- preserves the original audio,
- exports the processed video.

---

# Command Line

Example configuration:

```bash
ai-video --config config/config.yaml
```

---

# Project Architecture

```
src/
└── ai_video/
    ├── config/
    ├── detector/
    ├── gui/
    ├── renderer/
    ├── tracker/
    ├── tracking/
    ├── utils/
    ├── video/
    └── ...
```

Architectural principles:

- Layered Architecture
- Factory Pattern
- Plugin Architecture
- Package Modularization

The framework is intentionally designed so new AI components can be added with minimal changes to the existing codebase.

---

# Documentation

Project documentation can be found in the `docs/` directory.

Recommended reading order:

1. Vision
2. Architecture
3. Plugin Guide
4. Roadmap
5. Release Plan
6. Project Status

Main documents:

- `docs/vision.md`
- `docs/architecture.md`
- `docs/plugin.md`
- `docs/roadmap.md`
- `docs/release_plan_1.0.md`
- `docs/project_status.md`

---

# Development

Run all automated tests.

```bash
make test
```

Current project status:

- ✅ 109 automated tests
- ✅ Editable installation
- ✅ GUI application
- ✅ CLI application
- ✅ Plugin architecture
- ✅ Continuous Integration

---

# Roadmap

Version 1.0 focuses on building a stable, maintainable, and extensible privacy framework.

Future releases may include:

- GPU acceleration
- Additional detector plugins
- Additional tracker plugins
- Batch processing
- Automatic update checking
- Performance optimization
- More renderer plugins

---

# Contributing

Contributions are welcome.

Please read:

```
CONTRIBUTING.md
```

before submitting pull requests.

---

# License

This project is released under the MIT License.

See:

```
LICENSE
```

for details.

---

# Author

**KuoChing Hsieh**

Founder of AI-Video

---

# Philosophy

AI-Video is more than a face-blurring application.

It is a reusable privacy framework for AI-powered video processing.

Every feature should be:

- Reliable
- Maintainable
- Well Tested
- Well Documented

Documentation is considered part of the software.

A feature is not complete until:

- the implementation is finished;
- automated tests pass;
- documentation is updated.

---

## Acknowledgements

AI-Video stands on the shoulders of many outstanding open-source projects, including OpenCV, InsightFace, ByteTrack, FFmpeg, PySide6, and the broader Python open-source community.

Their work has made this project possible.