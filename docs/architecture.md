# AI-Video Architecture

> Version: Architecture 2.1

---

# 1. Design Philosophy

AI-Video is designed as a modular, extensible, and maintainable privacy-first video processing framework.

The project follows several core software engineering principles:

- Single Responsibility Principle
- Layered Architecture
- Factory Pattern
- Plugin Architecture
- Low Coupling
- High Cohesion

Each subsystem has a clearly defined responsibility and communicates through well-defined interfaces.

---

# 2. Overall Architecture

```
                     GUI
                      │
                      ▼
               VideoProcessor
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Detector         Tracker         Renderer
      │               │               │
      ▼               ▼               ▼
DetectorFactory  Tracking Engine  RendererFactory
      │
      ▼
  AI Models

                      │
                      ▼
          Video Reader / Writer
```

The `VideoProcessor` coordinates the entire processing pipeline while keeping all subsystems independent and interchangeable.

---

# 3. Package Structure

```
ai_video/

├── config/
├── detector/
├── gui/
├── models/
├── renderer/
├── tracker/
├── tracking/
├── video/
│
├── config_manager.py
├── face.py
├── logger.py
├── model_manager.py
├── privacy_region.py
├── processing_stats.py
├── processor.py
```

The root package contains only shared services and domain objects.

Subsystem implementations are organized into dedicated packages.

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

Each processing stage performs a single responsibility.

The `VideoProcessor` coordinates the pipeline but does not implement detection, tracking, or rendering itself.

---

# 5. Plugin Architecture

## Detector

```
DetectorFactory

      │

 ┌────┴─────┐
 │          │
SCRFD     YOLO
```

---

## Tracker

```
TrackerFactory

      │

 ByteTrack
```

---

## Renderer

```
RendererFactory

      │

 ┌──────────────┬──────────────┬──────────────┐
 │              │              │
Blur        Pixelate      Solid Color
```

New implementations can be added by registering them in the corresponding Factory.

---

# 6. Data Flow

```
Frame
   │
   ▼
Detector
   │
   ▼
List[Face]
   │
   ▼
Tracker
   │
   ▼
Tracked Face
   │
   ▼
PrivacyRegion
   │
   ▼
Renderer
   │
   ▼
Frame
   │
   ▼
VideoWriter
```

The `Face` object is the shared domain model across the entire processing pipeline.

---

# 7. Package Responsibilities

## detector/

Responsible for AI-based face detection.

---

## tracker/

Responsible for high-level tracking components.

---

## tracking/

Contains internal tracking algorithms, including:

- Kalman Filter
- Matching
- Cost Matrix
- Assignment
- Geometry
- Track Manager

These modules are internal implementation details rather than public APIs.

---

## renderer/

Responsible for privacy rendering.

---

## video/

Responsible for video input/output and FFmpeg integration.

---

## gui/

Provides the desktop graphical user interface.

---

## models/

Responsible for AI model management.

---

## config/

Stores configuration resources used by the application.

---

# 8. Design Principles

## Layered Architecture

Each layer communicates only with adjacent layers.

---

## Factory Pattern

Concrete implementations are created through Factory classes rather than directly instantiated by the processor.

---

## Plugin Architecture

New Detectors, Trackers, and Renderers can be integrated without modifying the processing pipeline.

---

## Single Responsibility Principle

Every class has one primary responsibility.

---

## Dependency Isolation

The `VideoProcessor` coordinates the pipeline without depending on implementation details.

---

# 9. Future Extensions

Planned detector plugins

- RetinaFace
- YOLO Face

---

Planned tracker plugins

- StrongSORT
- DeepSORT

---

Planned renderer plugins

- Emoji
- AI Replacement

The architecture is intentionally designed so these extensions can be integrated with minimal changes to the existing codebase.