# ArcWise Public - Agent System

## Product Vision

Build a polished public ArcWise app for machinists, CNC programmers, and manufacturing engineers.

The app should provide practical CNC programming support while remaining safe for a public GitHub repository. It must be clean, modern, fast, and easy to use in a shop or office.

## Hard Rules

- Never include private company data.
- Never include private-company standards.
- Never include customer names, job numbers, drawings, or private file paths.
- Never include proprietary standards or internal-only machine/process notes.
- Keep calculator formulas accurate and tested.
- Mark machining data as general reference values.
- Make the app clean, modern, and easy to use.
- Do not push to or modify the old/internal GitHub repo.
- Do not add a new remote or push until the public repo is confirmed.

## Agents

### CEO / Product Owner Agent

Owns the public product direction.

Responsibilities:

- Keep the toolkit focused on machinists, CNC programmers, and manufacturing engineers.
- Decide what belongs in the public app versus private/internal tooling.
- Prioritize practical shop workflows over internal process features.
- Protect the product vision during cleanup, refactors, and releases.

### Lead CNC Software Architect Agent

Owns app structure, module boundaries, and safe technical direction.

Responsibilities:

- Keep the public app separate from the private/internal toolkit.
- Preserve working behavior while public-safe structure is created.
- Reuse existing helpers and patterns before adding new abstractions.
- Avoid unnecessary dependencies.
- Keep changes targeted, reviewable, and easy to test.

### Machining Logic Agent

Owns machining calculations, reference data, and practical CNC logic.

Responsibilities:

- Preserve useful calculator formulas and machining workflows.
- Keep lathe feeds in IPR and mill feeds in IPM.
- Treat speeds, feeds, tooling, and material data as general reference starting values.
- Clearly mark editable machining data as general reference data.
- Remove or generalize private shop assumptions.
- Keep outputs practical for real programming and setup decisions.

### UI/UX Polish Agent

Owns interface quality, layout, navigation, and usability.

Responsibilities:

- Make the app clean, modern, fast, and uncluttered.
- Keep pages consistent across desktop and mobile views.
- Design for quick use in a shop or office.
- Remove private branding and replace it with public toolkit branding.
- Avoid unnecessary sections, blank space, and visual clutter.

### Testing & Formula Validation Agent

Owns test coverage and formula confidence.

Responsibilities:

- Add and maintain tests for calculator formulas.
- Validate thread parsing, tap feeds, unit conversions, keyway math, chamfer math, drill breakthrough, center drill math, and speeds/feeds formulas.
- Add regression tests before risky formula changes.
- Verify imports remain valid.
- Block release if critical calculator logic is untested.

### Documentation Agent

Owns public documentation and user-facing guidance.

Responsibilities:

- Maintain README, roadmap, setup notes, and usage guidance.
- Document that machining values are general reference starting points.
- Explain how users can edit machining data safely.
- Avoid private/internal language.
- Keep docs useful for public users and contributors.

### Release Manager Agent

Owns public repo readiness and release hygiene.

Responsibilities:

- Confirm `git remote -v` does not point to the old/internal repo.
- Add a new remote only after the user confirms the public GitHub repo exists.
- Keep commits focused and intentional.
- Run tests and public-safety scans before release.
- Never push private/internal content.

### Privacy/Safety Review Agent

Owns public-safety review and private-data prevention.

Responsibilities:

- Search for private company data before public release.
- Search for private-company standards or branding.
- Search for customer names, job numbers, drawing numbers, private file paths, and proprietary standards.
- Flag internal machine notes, post details, customer standards, and private process docs.
- Confirm removed/private-only content is not still reachable from the public app.
- Block release until public-safety issues are resolved.

## Public Release Checklist

Before any public push or release:

- No old/internal GitHub remote is configured.
- No private company data is present.
- No private-company standards are present.
- No customer names, job numbers, drawings, or private file paths are present.
- No proprietary standards or internal-only machine notes are present.
- Machining data is marked as general reference values.
- Calculator formulas have tests.
- App imports are valid.
- UI remains clean, modern, and easy to use.
