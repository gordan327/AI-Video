# Changelog

All notable changes to this project will be documented in this file.

---

## [1.1.0] - 2026-08-01

### Added

- Added a multi-video processing queue.
- Added automatic continuation after each queued video completes.
- Added queue item status tracking for waiting, processing, completed, failed, and cancelled states.
- Added a final queue summary showing completed and failed counts.
- Added five automated controller tests for queue processing behavior.

### Changed

- Simplified failure dialogs while retaining full technical details in the execution log.
- Allowed batch processing to continue after an individual video fails.

### Verified

- Verified successful sequential processing of multiple videos.
- Verified that one failed video does not interrupt the remaining queue.
- Verified all 153 automated tests.

---

## [1.0.1] - 2026-07-28

### Changed

- Updated the project and package version to 1.0.1.
- Updated current-status documentation and release notes for version consistency.
- Published the verified macOS and Windows distributions in GitHub Release v1.0.1.

---

## [1.0.0] - 2026-07-28

### Added

- Added the PySide6 desktop application and command-line interface.
- Added SCRFD face detection and ByteTrack face tracking.
- Added blur, pixelate, and solid-color privacy renderers.
- Added temporal privacy regions, prediction freeze, and expansion.
- Added FFmpeg-based audio preservation.
- Added plugin factories for detectors, trackers, and renderers.
- Added macOS and Windows desktop packaging workflows.
- Added 126 automated tests and continuous integration.
- Added architecture, deployment, packaging, release, and contributor
  documentation.

### Verified

- Verified the macOS `AI-Video.app` distribution.
- Verified the Windows `AI-Video-Windows.zip` distribution on Windows.
- Verified the Version 1.0 source and package metadata.

### Notes

- AI-Video 1.0.0 is the first stable public release.
- Linux remains available as an experimental source installation.

---

## [0.1.0] - 2026-07-01

### Added

- Initialized Git repository.
- Created project directory structure.
- Added README.md.
- Added MIT License.
- Added .gitignore.
- Added DevelopmentLog.md.
- Added requirements.txt.
- Added config/config.yaml.

### Notes

This is the initial project structure of AI-Video.
The project is currently in the planning and infrastructure stage.

## v0.3.0

### Added

- 新增 VideoReader
- 支援讀取影片資訊
- 支援逐格讀取 Frame
- 完成第一個影片測試

## v0.4.0

### Added

- 新增 VideoProcessor
- 打通 PipeLine

## v0.5.0
### Added

- 建立video_writer
- 產生新的影像檔（無聲）

## v0.5.5
### Added

- 加入FFmpeg Audio Merge
- 產生中間檔，並生成有生的影像檔
