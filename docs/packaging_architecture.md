# Packaging Architecture

**Project:** AI-Video

**Version:** Desktop Edition

**Status:** Draft

---

# Purpose

This document defines the packaging architecture of AI-Video Desktop Edition.

The objective is to produce a native desktop application for macOS first, while keeping the architecture extensible for future Windows and Linux releases.

---

# Packaging Goals

The packaged application should:

- Require no Python installation.
- Require no manual dependency installation.
- Launch by double-clicking.
- Keep user data outside the application bundle.
- Support future automatic updates.

---

# Packaging Strategy

AI-Video adopts the following deployment strategy.

```
Source Code
      │
      ▼
pyside6-deploy
      │
      ▼
AI-Video.app
      │
      ▼
DMG Installer
```

---

# Runtime Layout

The application bundle only contains executable resources.

```
AI-Video.app
    Contents
        MacOS
        Frameworks
        Resources
```

Runtime data is stored outside the application.

```
~/Library/Application Support/AI-Video

    config/

    models/

    cache/

    logs/

    temp/
```

---

# Resource Ownership

Application Bundle

Responsible for:

- Executable
- Qt Framework
- Icons
- Built-in resources

Application Support

Responsible for:

- AI models
- User configuration
- Runtime cache
- Temporary files
- Logs

---

# Resource Access

The application never accesses runtime resources directly.

All runtime paths must be provided by:

- ResourceManager

Migration is handled by:

- ResourceMigrator

---

# Packaging Tool

Current target:

- pyside6-deploy

Future evaluation:

- Nuitka
- PyInstaller
- Briefcase

Current decision:

Desktop Edition adopts pyside6-deploy.

---

# Build Output

Development

```
build/
```

Release

```
dist/

AI-Video.app

AI-Video.dmg
```

---

# Packaging Workflow

Developer

↓

Run tests

↓

Build application

↓

Verify application

↓

Create DMG

↓

Release

---

# Platform Support

Current

- macOS

Future

- Windows
- Linux

---

# Design Principles

Packaging should not change runtime architecture.

Packaging only assembles the existing runtime.

Runtime architecture remains platform-independent.

---

# Current Status

Desktop runtime architecture has been frozen.

Packaging work starts after Architecture Freeze.