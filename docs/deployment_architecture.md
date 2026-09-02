# AI-Video Deployment Architecture

## 1. Purpose

This document defines the deployment and runtime resource architecture for the AI-Video Desktop Edition.

The goals are:

- keep application files separate from user data;
- support macOS, Windows, and Linux;
- provide predictable locations for AI models, logs, cache, and runtime resources;
- avoid hard-coded paths inside application modules;
- prepare the project for standalone desktop packaging.

---

## 2. Application and User Data Separation

AI-Video separates resources into two categories.

### 2.1 Application Resources

Application resources are distributed with the installed application and should normally be treated as read-only.

Examples:

- Python modules;
- default configuration;
- icons and interface assets;
- bundled FFmpeg binaries;
- bundled metadata and documentation.

### 2.2 User Data

User data is created, downloaded, or modified while the application is running.

Examples:

- downloaded AI models;
- logs;
- cache;
- temporary files;
- user preferences.

User data must not be stored inside the installed application package.

---

## 3. Application Support Directory

The runtime data root is the AI-Video application support directory.

### macOS

```text
~/Library/Application Support/AI-Video