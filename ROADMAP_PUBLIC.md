# Public CNC Programmer Toolkit Roadmap

This repository is a copied working folder that is being turned into a new, separate public GitHub repository named `cnc-programmer-toolkit-public`.

The old/internal GitHub remote has been removed. Do not add a new remote or push until the new public GitHub repo exists and the user confirms it is ready.

## Goal

Create a polished public CNC Programmer Toolkit for machinists and CNC programmers while preserving useful general machining tools and removing or separating private/internal content.

The public version should be:

- Useful for general CNC programming support
- Clean, fast, and easy to use in a shop or office
- Free of company-specific and customer-specific data
- Clear that machining values are general reference starting points
- Separate from the private/internal toolkit

## Current Public-Safe Core

These areas look suitable to keep after public cleanup and validation:

- Speeds and feeds workflows for lathe and mill
- Thread parsing and ID/OD thread calculations
- Tap feed calculations
- Triangle calculator
- Keyway calculator
- Woodruff key lookup and related shop math
- Chamfer calculators
- Drill breakthrough calculator
- Center drill depth calculator
- Inch/mm conversion
- General G-code and M-code references after private machine-specific notes are removed
- Shared formula helpers in `utils/`
- General data modules after private labels and internal assumptions are cleaned

## Private/Internal Content To Remove Or Isolate

These areas must not ship publicly in their current form:

- Company branding and logo assets
- Any references to the private company or internal author branding
- Customer or company standards PDFs under `standards/`
- Customer names and drawing/document names embedded in standards folder paths
- Machine-specific internal notes and post behavior in machine data
- Checklist fields or saved data paths involving job numbers, drawing numbers, customers, programmer names, and internal review workflow
- Private shop process notes tied to specific machines, posts, fixtures, or customer work
- Internal workflow docs and prompt bridge docs if they reference private process
- Any generated local logs, exports, databases, or data files containing private job/customer information

## Proposed Public Repo Structure

Target structure after cleanup:

```text
cnc-programmer-toolkit-public/
  app.py
  pages/
    1_Speeds_Feeds.py
    2_Threads.py
    3_Calculators.py
    4_References.py
    5_G_M_Codes.py
  data/
    materials.py
    threads_data.py
    center_drills.py
    woodruff_keys.py
    woodruff_reference.py
    g_m_codes.py
  utils/
    formulas.py
    holemaking.py
    triangle.py
    ui_helpers.py
  tests/
    test_formulas.py
    test_threads.py
    test_calculators.py
    test_woodruff.py
  docs/
    data_editing.md
    formula_notes.md
    public_safety.md
  README.md
  ROADMAP_PUBLIC.md
  AGENTS.md
  requirements.txt
```

Private-only content should be moved out of the public repo or ignored before release, not hidden behind public UI switches.

## Conversion Phases

### Phase 1: Repository Safety

- Confirm `git remote -v` does not point to the old/internal repo.
- Do not push anywhere until the public GitHub repo exists.
- Add public roadmap and AI agent rules.
- Identify all private/company/customer content before refactoring.

### Phase 2: Public Content Audit

- Search for company names, customer names, job numbers, drawing numbers, private paths, and proprietary standards.
- Inventory all files under `standards/`, `machines/`, `data/`, `docs/`, `archive/`, and `pages/`.
- Decide whether each item is public-safe, needs generalization, or must be removed from the public repo.
- Preserve calculator and formula logic during the audit.

### Phase 3: Public Branding And Navigation

- Replace private branding with `CNC Programmer Toolkit`.
- Remove logo and company-specific captions.
- Remove or rename pages that expose private content.
- Keep the app layout consistent and uncluttered.

### Phase 4: Data Generalization

- Mark materials, speeds, feeds, inserts, and tooling values as general reference starting points.
- Make data easy to edit in plain Python or structured data files.
- Remove internal machine-specific and customer-specific assumptions.
- Keep lathe feeds in IPR and mill feeds in IPM.

### Phase 5: Calculator Validation

- Add tests for formulas and calculators.
- Validate thread parsing, tap feeds, OD/ID thread values, keyway math, chamfer math, center drill math, drill breakthrough, and unit conversion.
- Run tests before behavior changes and after cleanup.
- Do not change formulas without tests.

### Phase 6: Documentation

- Update README for the public app.
- Add clear setup instructions.
- Document that reference values are starting points only.
- Add data editing guidance.
- Add public safety/release checklist.

### Phase 7: Public Repo Release Prep

- Confirm no old/internal remote exists.
- Add the new public remote only after the user confirms the GitHub repo exists.
- Run a final private-content scan.
- Run tests.
- Commit focused public-safe changes.
- Push only to the new public repo.

## Release Blockers

Do not publish while any of these are true:

- Old/internal remote is configured.
- Company-specific PDFs or standards are present.
- Customer names, drawing numbers, job numbers, or private paths are present.
- Internal machine notes are exposed.
- Calculator formulas are untested.
- Public README still describes private/internal workflows.
- App branding still references private/internal ownership.

## Current Assumptions

- This copied folder is the intended working directory for the public repo.
- The private/internal toolkit should remain untouched.
- Public cleanup should happen incrementally so useful calculators are preserved.
- No app behavior should change until the user asks for the cleanup/refactor phase.
