# AI-Video 1.0 Release Plan

> Target: First stable public release

AI-Video 1.0 will be the first stable release of the privacy-first video processing framework.

The goal of version 1.0 is not to include every possible feature. The priority is to deliver a reliable, understandable, installable, and extensible foundation.

---

## 1. Release Objectives

AI-Video 1.0 should provide:

- Reliable face privacy protection
- Stable Detector, Tracker, and Renderer interfaces
- A usable desktop GUI
- A functional command-line entry point
- Clear installation instructions
- Complete developer documentation
- Automated test coverage for critical components
- A repeatable release process

---

## 2. Must Have

These items are required before version 1.0 can be released.

### Core Processing

- [x] Video reading and writing
- [x] FFmpeg audio merge
- [x] SCRFD face detection
- [x] ByteTrack-based face tracking
- [x] Smart head privacy region
- [x] Kalman prediction
- [x] Freeze and expansion strategy
- [x] Temporal privacy hold
- [x] Blur renderer
- [x] Pixelate renderer
- [x] Processing cancellation
- [x] Progress reporting
- [x] Processing statistics

### Plugin Framework

- [x] Detector interface
- [x] DetectorFactory
- [x] Tracker interface
- [x] TrackerFactory
- [x] Renderer interface
- [x] RendererFactory
- [x] Modular package structure
- [ ] Stable public plugin API declaration
- [ ] Plugin compatibility documentation

### Desktop GUI

- [x] Input video selection
- [x] Output video selection
- [x] Detector selection
- [x] Tracker selection
- [x] Renderer selection
- [x] Progress bar
- [x] Live processing statistics
- [x] Runtime log view
- [x] Stop processing
- [x] Preferences dialog
- [x] Drag and drop
- [ ] About dialog
- [ ] Clear and consistent version display
- [ ] Friendly error messages for missing models and FFmpeg

### Command Line

- [x] `ai-video`
- [x] `ai-video-gui`
- [ ] `ai-video --help`
- [ ] `ai-video --version`
- [ ] Optional configuration path
- [ ] Clear exit codes for success, cancellation, and failure

### Configuration

- [x] YAML configuration
- [x] Dot-notation access
- [x] Runtime configuration updates
- [x] Detector configuration
- [x] Tracker configuration
- [x] Renderer configuration
- [ ] Configuration validation
- [ ] Helpful messages for invalid values
- [ ] Documented default configuration

### Testing

- [x] Tracking algorithm tests
- [x] Privacy region tests
- [x] Blur renderer tests
- [x] Pixelate renderer tests
- [x] FaceRenderer tests
- [x] DetectorFactory tests
- [x] TrackerFactory tests
- [x] RendererFactory tests
- [ ] ConfigManager tests
- [ ] CLI tests
- [ ] VideoReader tests
- [ ] VideoWriter tests
- [ ] Processor integration test
- [ ] Release smoke test

### Documentation

- [x] README
- [x] CHANGELOG
- [x] CONTRIBUTING
- [x] Architecture
- [x] API Reference
- [x] Design Decisions
- [x] Plugin Guide
- [x] Vision
- [x] Roadmap
- [x] Release Plan
- [ ] Installation troubleshooting
- [ ] Plugin compatibility policy
- [ ] Release notes for version 1.0

### Packaging and Distribution

- [x] Installable Python package
- [x] Editable installation support
- [x] Console entry points
- [ ] Correct project URLs
- [ ] Verified package metadata
- [ ] Clean source distribution build
- [ ] Clean wheel build
- [ ] Installation test in a fresh virtual environment
- [ ] Version tag
- [ ] GitHub Release
- [ ] Optional PyPI release decision

---

## 3. Nice to Have

These features are valuable but are not required for version 1.0.

### Additional Detectors

- [ ] YOLO face detector production support
- [ ] RetinaFace detector
- [ ] Detector benchmark comparison

### Additional Trackers

- [ ] StrongSORT
- [ ] DeepSORT
- [ ] Tracker benchmark comparison

### Additional Renderers

- [ ] Solid color renderer
- [ ] Black box renderer
- [ ] Emoji renderer
- [ ] Image overlay renderer

### GUI Improvements

- [ ] Recent files
- [ ] Theme selection
- [ ] Language selection
- [ ] Before-and-after preview
- [ ] Batch processing
- [ ] Output folder shortcut

### Performance

- [ ] GPU benchmark
- [ ] CPU benchmark
- [ ] Memory measurement
- [ ] Pipeline timing report
- [ ] Large video stress test

---

## 4. Out of Scope for 1.0

The following items are explicitly excluded from version 1.0:

- Cloud processing service
- Web application
- Distributed processing
- Mobile application
- Real-time streaming server
- Automatic third-party plugin discovery
- AI face replacement
- License plate privacy protection
- Full multilingual interface
- Enterprise user management
- Remote processing API

These items may be considered for later releases.

---

## 5. Public API Candidate

The following interfaces are candidates for stability in version 1.0:

```text
Face
FaceDetector.detect()
FaceTracker.track()
BaseRenderer.render()
DetectorFactory.create()
TrackerFactory.create()
RendererFactory.create()
PrivacyRegion.create()
ConfigManager.get()
ConfigManager.set()
VideoProcessor.run()
```

Before release, each candidate must be reviewed for:

- Naming
- Parameters
- Return values
- Error behavior
- Type hints
- Documentation
- Backward compatibility expectations

Internal tracking modules are not part of the stable public API.

```text
tracking.assignment
tracking.cost_matrix
tracking.geometry
tracking.kalman_filter
tracking.matching
tracking.track_manager
```

---

## 6. Quality Gates

Version 1.0 cannot be released until all mandatory quality gates pass.

### Gate 1: Automated Tests

```bash
PYTHONPATH=src pytest -q
```

Requirements:

- All tests pass
- No unexpected warnings
- No skipped critical tests

### Gate 2: CLI Smoke Test

```bash
ai-video --version
ai-video --help
```

Requirements:

- Commands exit normally
- Version matches package metadata
- Help text is understandable

### Gate 3: GUI Smoke Test

```bash
ai-video-gui
```

Requirements:

- Application opens
- Video can be selected
- Blur processing succeeds
- Pixelate processing succeeds
- Stop button works
- No crash during normal use

### Gate 4: Fresh Installation

In a new virtual environment:

```bash
python -m venv .venv-test
source .venv-test/bin/activate
pip install .
ai-video-gui
```

Requirements:

- Installation succeeds
- Entry points are created
- Required modules are present
- GUI starts successfully

### Gate 5: Documentation Verification

A new user should be able to:

1. Install the project using README instructions
2. Start the GUI
3. Process a short video
4. Run the tests
5. Understand how to add a Renderer plugin

### Gate 6: Privacy Review

Use the fixed benchmark video set and verify:

- No obvious unprotected face frames
- Masked and partially occluded faces remain protected
- Temporary detector failures are covered
- Fast movement does not cause unacceptable leakage
- Blur and Pixelate both protect the full privacy region

---

## 7. Release Checklist

### Version and Metadata

- [ ] Update `pyproject.toml`
- [ ] Update `src/ai_video/version.py`
- [ ] Update README version references
- [ ] Update CHANGELOG
- [ ] Verify project URLs
- [ ] Verify license metadata

### Code Quality

- [ ] Run full test suite
- [ ] Run syntax checks
- [ ] Remove unused files
- [ ] Remove debugging output
- [ ] Confirm `.gitignore`
- [ ] Confirm no generated files are tracked
- [ ] Review public API

### Functional Verification

- [ ] Test Blur
- [ ] Test Pixelate
- [ ] Test cancellation
- [ ] Test audio merge
- [ ] Test Preferences
- [ ] Test drag and drop
- [ ] Test CLI
- [ ] Test GUI

### Documentation

- [ ] README complete
- [ ] API Reference current
- [ ] Architecture current
- [ ] Plugin Guide current
- [ ] Release notes written
- [ ] Installation troubleshooting written

### Distribution

- [ ] Build source package
- [ ] Build wheel
- [ ] Install built wheel in clean environment
- [ ] Create Git commit
- [ ] Create version tag
- [ ] Create GitHub Release

---

## 8. Proposed Release Sequence

### 0.8.0

Focus:

- CLI help and version support
- Configuration validation
- ConfigManager tests
- Video I/O tests

### 0.9.0

Focus:

- Processor integration test
- Installation troubleshooting
- Public API review
- Packaging verification
- Release candidate preparation

### 1.0.0-rc1

Focus:

- Feature freeze
- Bug fixes only
- Fresh installation test
- Privacy benchmark review
- Documentation verification

### 1.0.0

Focus:

- Stable public release
- GitHub Release
- Final release notes
- Version tag
- Distribution decision

---

## 9. Definition of Done

AI-Video 1.0 is complete when:

- All Must Have items are completed
- All quality gates pass
- A clean installation succeeds
- Blur and Pixelate processing work reliably
- CLI and GUI entry points work
- Documentation matches the code
- Public API candidates are reviewed
- The benchmark videos show acceptable privacy protection
- A tagged release can be reproduced from the repository

---

## 10. Guiding Principle

Version 1.0 should prioritize:

> Reliability over feature count.

A smaller, stable, well-documented release is more valuable than a feature-rich release with uncertain behavior.