# UI Flow Plan

## Goal

Make CutWise feel like a connected programming workbench instead of a set of unrelated pages.

## Primary Navigation

The main navigation should focus on the three work areas a machinist/programmer reaches for most:

- Speeds & Feeds
- Math Workbench
- G/M Codes

Home remains available as the entry point, but the sidebar should not make every utility feel like a separate top-level app.

## Speeds & Feeds Workbench

Speeds & Feeds should become the working hub for cutting data and nearby utility actions:

- Keep current lathe and mill speeds/feeds behavior intact.
- Add a compact utility drawer near the top with quick links to:
  - Threads
  - Spot Drill & Hole Chamfer
  - Center Drill Calculator
  - Triangle Calculator
  - Keyway / Slot Calculator
- Add a Threading tab/panel inside Speeds & Feeds that points users to the existing thread worksheet and explains that thread feed, tap drill, and OD model values live there.
- Do not remove or duplicate the full Threads page yet; keep it available as the complete worksheet.

## Calculator Flow

Machining math tools remain available as a continuous workbench:

- The general math page stays available as the main machining math workspace.
- Spot Drill & Hole Chamfer and Center Drill remain separate calculator pages.
- Speeds & Feeds provides direct links into the calculator tools so users can jump there mid-work.

## Home Page

Simplify the home page around three primary cards:

- Speeds & Feeds Workbench
- Math Workbench
- G/M Codes

Show secondary utility links under the primary tools instead of giving every utility a full top-level card.

## Constraints

- Preserve all formulas and tests.
- Do not remove thread functionality.
- Do not remove calculators.
- Do not add private/company-specific data.
- Keep edits targeted and reviewable.
