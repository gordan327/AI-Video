# AI-Video Publication Style Guide

Version: 1.0

---

# Purpose

This document defines the editorial, formatting, and publication standards for all
AI-Video documentation.

Its purpose is to ensure that every document in the project maintains a
consistent writing style, naming convention, document structure, and publication
quality.

This guide applies to:

- Architecture Handbook
- Technical documentation
- API Reference
- Design documents
- Release documents
- Project documentation

---

# Writing Principles

Documentation should be:

- Clear
- Concise
- Consistent
- Professional
- Maintainable

Avoid unnecessary repetition.

Prefer explanation over decoration.

Write for long-term maintainability.

---

# Language

Documentation is written in English.

Technical terminology should remain consistent throughout the project.

Avoid mixing multiple names for the same concept.

---

# Naming Conventions

## Project Name

Always use:

AI-Video

Do not use:

- AI Video
- AIVideo
- AI_VIDEO

---

## Python Package

Always use:

`ai_video`

---

## Command Line Interface

Always use:

`ai-video`

Example:

```text
ai-video --help
```

---

## Book Title

Always use:

AI-Video Architecture Handbook

---

## Document Names

Use lowercase filenames.

Words are separated with underscores.

Examples:

```text
architecture.md
api_reference.md
project_status.md
release_plan_1.0.md
publication_style_guide.md
```

---

# Heading Style

Use Markdown headings only.

Allowed levels:

```text
# H1
## H2
### H3
```

Avoid H4 and deeper unless absolutely necessary.

---

# Chapter Numbering

Use numbered H2 headings.

Example:

```markdown
## 3.1 Detector Factory

## 7.4 Plugin Architecture
```

---

# Code Blocks

Use language-specific fences whenever possible.

Example:

````markdown
```python
```

```bash
```

```yaml
```
