# Desktop Architecture Freeze

**Project:** AI-Video

**Version:** 1.0 Desktop Edition

**Status:** Frozen

**Date:** 2026-07-24

---

# Purpose

This document records the completion of the desktop runtime architecture.

From this point forward, the core desktop architecture is considered stable.
Future work should focus on packaging, deployment, installation, and user experience rather than redesigning the runtime architecture.

---

# Frozen Components

The following components are considered architecture-stable.

## ResourceManager

Responsibilities

- Package resource paths
- Application Support paths
- InsightFace resource paths
- Ultralytics resource paths
- Log directory
- Cache directory
- Temporary directory
- FFmpeg path management

---

## ConfigManager

Responsibilities

- Configuration loading
- YAML parsing
- Default configuration discovery
- User supplied configuration support

---

## ModelManager

Responsibilities

- InsightFace initialization
- Runtime model loading
- Provider selection

---

## ResourceMigrator

Responsibilities

- Legacy model detection
- Safe resource migration
- Copy-only migration
- Existing resource protection

---

# Design Principles

The desktop runtime follows these principles.

## Single Responsibility

Each manager is responsible for one domain only.

## No Hard-coded Paths

All runtime paths are provided by ResourceManager.

## Safe Migration

Migration never deletes existing user data.

## Testability

All components support isolated testing.

---

# Future Work

Future development should concentrate on:

- Desktop packaging
- Application bundle generation
- DMG installer
- Windows installer
- Linux package
- Auto update
- Resource download optimization

---

# Architecture Freeze

The following runtime architecture is frozen.

- ResourceManager
- ConfigManager
- ModelManager
- ResourceMigrator

Changes to these components should only be made for:

- Critical bug fixes
- Security fixes
- Cross-platform compatibility

Large architectural redesigns should be avoided after this point.

---

# Current Test Status

```
126 tests passed
```

The desktop runtime architecture is considered stable.