# AI-Video

> Privacy-first AI Video Framework for Face Detection, Tracking and Anonymization

AI-Video is an open-source, plugin-based video privacy framework designed to automatically detect, track, and anonymize faces in videos while preserving the original video quality and audio.

Originally created for educational activities, AI-Video emphasizes **privacy protection**, **maintainability**, and **extensibility**.

---

# Features

AI-Video currently provides:

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
- 🎯 Plugin Architecture
- 🎯 Factory Pattern
- 🎯 YAML Configuration
- 🎯 Automatic Audio Preservation (FFmpeg)
- 🎯 109 Automated Tests
- 🎯 GitHub Actions Continuous Integration

---

# Why AI-Video?

Most video anonymization tools focus only on blurring faces.

AI-Video is designed as a reusable **privacy framework**, making it easy to build new detectors, trackers, renderers, and future AI plugins without changing the core architecture.

Core design principles:

- Privacy First
- Plugin-based
- Extensible
- Maintainable
- Testable
- Open Source

---

# Requirements

- Python 3.11 or newer
- FFmpeg
- macOS
- Windows (planned for Version 1.x)
- Linux (experimental)

---

# Installation

Clone the repository:

```bash
git clone https://github.com/gordan327/AI-Video.git
cd AI-Video
```

Create a virtual environment:

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

Install AI-Video:

```bash
pip install -e .
```

---

# Quick Start

## Desktop GUI

```bash
ai-video-gui
```

Select

1. Input Video
2. Output Location
3. Click **Start**

The processed video will preserve:

- original audio
- original frame rate
- original resolution

---

## Command Line

```bash
ai-video --help
```

Example:

```bash
ai-video \
    --config config/config.yaml
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

Major design patterns:

- Layered Architecture
- Factory Pattern
- Plugin Architecture
- Package Modularization

---

# Documentation

Complete documentation is available in:

```
docs/
```

Recommended reading order:

1. vision.md
2. architecture.md
3. plugin.md
4. roadmap.md
5. release_plan_1.0.md
6. project_status.md

---

# Development

Run all tests:

```bash
make test
```

Current test status:

```
109 passed
```

---

# Roadmap

AI-Video Version 1.0 focuses on:

- Stability
- Documentation
- Maintainability
- Reliable Processing

Future development includes:

- GPU acceleration
- More detector plugins
- More tracker plugins
- Batch processing
- Automatic update checking

For detailed plans, see:

```
docs/roadmap.md
```

---

# License

MIT License

---

# Author

KuoChing Hsieh

Founder of AI-Video

---

# Philosophy

AI-Video is more than a face blurring tool.

It is a privacy-first AI framework.

Every feature should be:

- Reliable
- Maintainable
- Well tested
- Well documented

Documentation is considered part of the software.

A feature is not complete until:

- implementation is finished;
- tests pass;
- documentation is updated.