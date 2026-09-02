# Editorial Guidelines

## Purpose

The AI-Video documentation is intended to communicate architectural knowledge
clearly, consistently, and accurately.

These editorial guidelines establish the editorial standards used throughout the
project documentation.

Their purpose is to ensure that every document presents a unified voice,
consistent terminology, and long-term maintainability.

Good documentation is an essential part of software architecture.

It preserves knowledge, supports collaboration, and enables future contributors
to understand not only how the framework works, but also why it was designed in
its current form.

---

# 1. Scope

These guidelines apply to all official AI-Video documentation, including but
not limited to:

- README
- Architecture Handbook
- API Reference
- Developer Guide
- Design Documents
- Architecture Decision Records (ADRs)
- Release Plans
- Roadmaps
- Contributing Guide
- Changelog
- User Documentation

Any newly created documentation should follow these editorial standards unless
there is a clear reason to do otherwise.

---

# 2. Writing Philosophy

Documentation exists to communicate ideas.

It should prioritize understanding over sophistication.

The following principles guide all technical writing within AI-Video.

- Prefer clarity over cleverness.
- Prefer simplicity over complexity.
- Prefer precision over ambiguity.
- Prefer consistency over variety.
- Prefer explanation over assumption.
- Prefer long-term readability over short-term convenience.

Every sentence should improve the reader's understanding.

---

# 3. Audience

AI-Video documentation serves multiple audiences.

These include:

- framework users
- application developers
- plugin developers
- maintainers
- contributors
- reviewers

Always assume readers are technically capable but unfamiliar with the project.

Documentation should teach without overwhelming.

---

# 4. Language Style

Documentation should use clear, professional English.

Preferred writing style:

- concise
- objective
- technically accurate
- active voice whenever practical
- one primary idea per paragraph

Avoid:

- marketing language
- exaggerated claims
- unnecessary humor
- conversational filler
- subjective opinions
- vague descriptions

Documentation should remain timeless rather than fashionable.

---

# 5. Terminology

Technical terminology should remain consistent throughout the project.

Preferred capitalization includes:

- AI-Video
- Framework
- Architecture
- Plugin
- Factory
- Detector
- Tracker
- Renderer
- Configuration
- Public API
- Architecture Decision Record (ADR)

Do not introduce multiple names for the same concept.

Once terminology has been established, continue using it consistently.

---

# 6. Document Structure

Long-form technical documents should maintain a predictable structure whenever
appropriate.

Typical chapter organization:

1. Purpose
2. Goals (optional)
3. Main Discussion
4. Architectural Anti-patterns (optional)
5. Review Checklist (optional)
6. Design Principle (optional)

Not every document requires every section.

However, structural differences should always be intentional.

---

# 7. Headings

Headings should describe content rather than attract attention.

Good headings are:

- concise
- descriptive
- technically accurate

Avoid decorative, humorous, or ambiguous titles.

---

# 8. Paragraphs

Each paragraph should communicate one primary idea.

Prefer:

- short paragraphs
- logical progression
- clear separation of topics

Whitespace should improve readability rather than decorate the page.

---

# 9. Lists

Use bullet lists when presenting related concepts.

Bullet items should:

- follow parallel grammatical structure
- remain concise
- describe related concepts

Use numbered lists only when sequence or priority is important.

---

# 10. Code Examples

Code examples exist to explain architectural concepts.

Examples should:

- remain minimal
- emphasize readability
- compile whenever practical
- demonstrate recommended practices

Example code represents production-quality engineering.

---

# 11. Architectural Writing

Architecture documents should describe principles rather than implementation
details.

Whenever possible:

- explain why before how
- describe intent before mechanism
- emphasize long-term design
- avoid implementation-specific assumptions

Architecture documentation should remain valuable even after implementation
changes.

---

# 12. Markdown Style

Documentation should use consistent Markdown formatting.

General rules include:

- ATX headings (`#`)
- fenced code blocks
- unordered lists using `-`
- blank lines between sections
- consistent indentation

Formatting should support readability and maintainability.

---

# 13. Consistency

Consistency is more important than personal writing preference.

Editors should preserve the established documentation style rather than
introduce individual variations.

Readers should experience the documentation as a unified body of work.

---

# 14. Editorial Changes

Editorial revisions may include:

- grammar
- spelling
- punctuation
- wording
- formatting
- terminology
- consistency
- readability

Editorial revisions should never change architectural intent.

Substantive design changes belong to the normal design review process.

---

# 15. Editorial Review

Every editorial review should verify:

- consistency
- readability
- terminology
- formatting
- grammar
- technical accuracy
- cross-reference integrity

The purpose of editorial review is to improve communication while preserving
meaning.

---

# 16. Long-Term Maintenance

Documentation evolves together with the framework.

When updating documentation:

- preserve established terminology
- avoid unnecessary rewrites
- update related documents together
- remove obsolete information
- document significant architectural changes

Documentation should evolve incrementally.

Large rewrites should remain exceptional.

---

# Editorial Checklist

Before publishing documentation, verify the following.

- Is the terminology consistent?
- Is the writing clear and concise?
- Are headings descriptive?
- Is formatting consistent?
- Are architectural principles preserved?
- Are examples accurate?
- Are references still valid?
- Will future contributors understand this document?

---

# Editorial Principle

> Good documentation explains software.
>
> Great documentation preserves understanding.
>
> The highest goal of technical writing is not to describe today's
> implementation,
> but to help tomorrow's engineers make better decisions.