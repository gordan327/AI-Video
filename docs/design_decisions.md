# AI-Video Design Decisions

> Architectural Decision Records (ADR)

This document records important architectural decisions made during the development of AI-Video.

Its purpose is to explain **why** the project is designed this way, rather than only describing **what** the architecture looks like.

---

# DD-001 Factory Pattern

## Decision

Use Factory classes to create Detector, Tracker and Renderer implementations.

Examples

- DetectorFactory
- TrackerFactory
- RendererFactory

## Why

Avoid hard-coded implementation classes inside the processing pipeline.

Instead of

```
processor
    ↓
SCRFDFaceDetector()
```

the processor depends only on the factory.

```
processor
    ↓
DetectorFactory
    ↓
SCRFDFaceDetector
```

## Benefits

- Easy to add plugins
- Lower coupling
- Easier testing
- Cleaner processor

---

# DD-002 Separate Tracker and Tracking

## Decision

Split the tracking subsystem into two packages.

```
tracker/
tracking/
```

## Why

The tracker package contains public tracking components.

The tracking package contains internal tracking algorithms.

Examples

tracker/

- FaceTracker
- ByteTrackFaceTracker
- TrackerFactory

tracking/

- Kalman Filter
- Matching
- Assignment
- Cost Matrix
- Track
- Track Manager

## Benefits

- Clear responsibility
- Better package organization
- Easier maintenance

---

# DD-003 Shared Domain Model

## Decision

The Face class remains in the root package.

## Why

Face objects are shared by

- Detector
- Tracker
- Renderer

It is not owned by any specific subsystem.

---

# DD-004 Processor as Coordinator

## Decision

Processor remains in the root package.

## Why

Processor coordinates every subsystem.

It does not belong to

- detector
- tracker
- renderer
- video

Keeping it in the root package clearly expresses its orchestration role.

---

# DD-005 Package Modularization

## Decision

Large subsystems are organized into dedicated packages.

Current packages

- detector
- tracker
- tracking
- renderer
- video
- gui

## Why

Improve readability.

Reduce file clutter.

Support future growth.

---

# DD-006 Plugin Architecture

## Decision

Every extensible subsystem should support plugins.

Current plugin systems

- Detector
- Tracker
- Renderer

Future plugins

Detector

- RetinaFace
- YOLO

Tracker

- StrongSORT
- DeepSORT

Renderer

- Blur
- Pixelate
- Emoji
- AI Replace

---

# DD-007 Configuration Driven Design

## Decision

Subsystem selection is controlled by configuration.

Examples

```
detector.type
tracker.type
renderer.type
```

## Why

Avoid hard-coded implementation selection.

Allow GUI and CLI to use the same configuration mechanism.

---

# DD-008 Small Increment Refactoring

## Decision

Large refactoring is performed through many small commits.

Typical workflow

1. Create package
2. Move a few files
3. Fix imports
4. Run pytest
5. Commit

## Why

Reduce risk.

Keep every commit runnable.

Make debugging easier.

---

# DD-009 Documentation First

## Decision

Architecture documentation is updated whenever the architecture changes.

Important documents

- README
- Architecture
- Vision
- Roadmap
- Plugin Guide
- Design Decisions

## Why

Documentation is treated as part of the software.

Good documentation reduces future maintenance costs.

---

# Future Decisions

Future architectural decisions should be added here instead of modifying previous records.

Examples

DD-010

Introduce asynchronous processing.

DD-011

Cloud inference support.

DD-012

Distributed video processing.

Each decision should explain:

- What changed
- Why it changed
- Expected benefits