# AI-Video Architecture

> Version: Architecture 2.0

---

# 1. Design Philosophy

AI-Video is designed as a modular, extensible, and maintainable video privacy framework.

The project follows several core principles:

- Single Responsibility Principle
- Layered Architecture
- Factory Pattern
- Plugin Architecture
- Low Coupling
- High Cohesion

Every subsystem has a clear responsibility and communicates through well-defined interfaces.

---

# 2. Overall Architecture

```
                GUI
                 │
                 ▼
          VideoProcessor
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
 Detector     Tracker    Renderer
     │           │           │
 Detector    Tracking   Renderer
 Factory      Engine     Factory
     │
     ▼
  AI Models

                 │
                 ▼
        Video Reader / Writer
```

The VideoProcessor coordinates the complete pipeline while individual modules remain independent.

---

# 3. Package Structure

```
ai_video/

├── detector/
├── tracker/
├── tracking/
├── renderer/
├── video/
├── gui/
├── config/
├── models/
│
├── processor.py
├── model_manager.py
├── config_manager.py
├── privacy_region.py
├── processing_stats.py
├── logger.py
├── face.py
└── version.py
```

The root package contains only shared services and domain objects.

Subsystem implementations are placed in dedicated packages.

---

# 4. Processing Pipeline

```
VideoReader
      │
      ▼
Face Detector
      │
      ▼
Face Tracker
      │
      ▼
Privacy Region
      │
      ▼
Renderer
      │
      ▼
VideoWriter
```

Each stage performs a single responsibility.

---

# 5. Plugin Architecture

Detector

```
DetectorFactory

      │

 ┌────┴─────┐
 │          │
SCRFD     YOLO
```

Tracker

```
TrackerFactory

      │

 ByteTrack
```

Renderer

```
RendererFactory

      │

 ┌────┴────────┐
 │             │
Blur      Pixelate
```

New implementations can be added by registering them in the corresponding Factory.

---

# 6. Data Flow

```
Frame

↓

Detector

↓

List[Face]

↓

Tracker

↓

Tracked Face

↓

PrivacyRegion

↓

Renderer

↓

Frame

↓

VideoWriter
```

The Face object is the shared domain model across the pipeline.

---

# 7. Package Responsibilities

## detector/

Responsible for AI-based face detection.

## tracker/

Responsible for high-level tracking components.

## tracking/

Contains internal tracking algorithms:

- Kalman Filter
- Matching
- Cost Matrix
- Assignment
- Geometry
- Track Manager

## renderer/

Responsible for privacy rendering.

## video/

Responsible for video I/O and FFmpeg integration.

## gui/

Desktop application.

## models/

AI model management.

---

# 8. Design Principles

AI-Video follows the following software engineering principles.

## Layered Architecture

Each layer only communicates with adjacent layers.

## Factory Pattern

Subsystem implementations are created through Factory classes.

## Plugin Pattern

New detectors, trackers, and renderers can be added without modifying the processing pipeline.

## Single Responsibility Principle

Every class has one primary responsibility.

## Dependency Isolation

The processor coordinates modules without depending on implementation details.

---

# 9. Future Extensions

Planned detector plugins

- RetinaFace
- YOLOv11 Face

Planned tracker plugins

- StrongSORT
- DeepSORT

Planned renderer plugins

- Solid Color
- Mosaic
- Emoji
- AI Replacement

The architecture is intentionally designed so that these extensions require minimal changes to existing code.