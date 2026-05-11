# Public Safety Audit

Audit date: 2026-05-11

Repo target: `cnc-programmer-toolkit-public`

Scope: public safety audit only. No app behavior was changed during this audit.

## Git Safety Status

- Current remote points to the new public repo.
- No push should happen until the audit is reviewed and cleanup is complete.

## Safe Public Files And Features

These appear broadly suitable for the public app after normal validation and branding cleanup:

- `README.md`
  - General Streamlit run instructions and public-facing feature list.
- `requirements.txt`
  - Small dependency set.
- `app.py`
  - Public-safe app shell concept, but current branding/logo must be removed.
- `pages/1_Speeds_Feeds.py`
  - Useful public feature: lathe/mill speeds and feeds workflows.
  - Needs branding cleanup and data disclaimers.
- `pages/2_Threads.py`
  - Useful public feature: thread callout parsing, ID tap drill support, OD modeling guidance.
  - Needs branding cleanup and formula tests.
- `pages/3_Calculators.py`
  - Useful public feature: triangle, keyway, Woodruff, chamfer, drill breakthrough, center drill, and unit conversion calculators.
  - Needs branding cleanup and formula tests.
- `pages/6_G_M_Codes.py`
  - Useful public feature: searchable G-code/M-code reference.
  - Needs machine-specific internal notes removed or generalized.
- `utils/formulas.py`
  - Public-safe formula helper module candidate.
- `utils/holemaking.py`
  - Public-safe holemaking formula helper candidate.
- `utils/triangle.py`
  - Public-safe triangle helper candidate.
- `utils/ui_helpers.py`
  - Public-safe navigation helper candidate after page list cleanup.
- `data/threads_data.py`
  - Public-safe thread reference candidate.
- `data/woodruff_keys.py`
  - Public-safe Woodruff key reference candidate if source/licensing is acceptable.
- `data/woodruff_reference.py`
  - Public-safe general Woodruff feed reference candidate if values are labeled as general starting points.
- `data/materials.py`
  - Public-useful material/feed data candidate, but needs private-company/machine-brand wording removed and general-reference disclaimer.
- `data/center_drills.py`
  - Useful public center drill presets, but shop/Mastercam-derived calibration values need human review.
- `tests/test_woodruff_display_rows.py`
  - Public-safe test candidate.
- `AGENTS.md`
  - Public safety/team rules are appropriate for this repo.
- `ROADMAP_PUBLIC.md`
  - Public conversion plan is appropriate for this repo.

## Private Or Internal Items That Must Be Removed Or Generalized

### Company Branding

- Private company logo asset
  - Private/company branding asset. Must be removed before public release.
- `app.py`
  - References a private company logo asset.
  - Displays private company branding.
  - Displays an individual author name.
- `pages/1_Speeds_Feeds.py`
  - Caption contains private company branding and an individual author name.
- `pages/2_Threads.py`
  - Caption contains private company branding and an individual author name.
- `pages/3_Calculators.py`
  - Caption contains private company branding and an individual author name.
- `pages/4_Standards.py`
  - Displays private company programming standards branding.
- `pages/5_Machines.py`
  - Caption contains private company branding.
- `pages/6_G_M_Codes.py`
  - Caption contains private company branding.
- `pages/99_Checklist.py`
  - Caption contains private company branding and an individual author name.
- `data/materials.py`
  - Several material notes reference a private-company baseline.

### Customer, Drawing, And Proprietary Standards PDFs

The entire `standards/` tree is not public-safe in its current form. It includes customer/company names, drawing-like filenames, revision identifiers, and likely proprietary documents.

- Multiple private/customer standards folders.

Examples of public blockers:

- Customer/company drawing PDFs, revisioned standards, process instructions, and private reference documents.

Recommendation: remove `standards/` from the public repo or replace it with a small public-safe sample/reference directory containing only original, generic content.

### Standards Browser Page

- `pages/4_Standards.py`
  - Browses company/customer standards folders directly.
  - Opens local documents/folders.
  - Displays selected local file paths.
  - Must be removed, hidden, or rewritten as a public generic references page before release.

### Machine-Specific Internal Notes

These files expose internal machine identifiers, machine-specific behavior, post rules, workholding details, steady-rest behavior, tool lists, and process notes:

- `pages/5_Machines.py`
- `data/machines_data.py`
- `machines/data/machine_list.py`
- `machines/data/lathe_specs.py`
- `machines/data/mill_specs.py`
- `data/machine_change_log.csv`

Specific concerns:

- Internal machine numbers and names, including 417, 421, 423, 424, 426, 430, 431, 432, 433, 434, 435, 436, 437, 652, 654, 655, 656, and 657.
- Machine/post-specific warnings and program behavior.
- Steady-rest macros and process values.
- Mastercam rules and CIMCO/posting checks.
- Customer-specific shaft notes in `data/machines_data.py`.
- Machine correction log workflow in `pages/5_Machines.py`.

Recommendation: remove the private Machines page from public navigation and either delete these datasets after review or replace them with a generic public machine-capability template.

### Checklist And Job Workflow

These files include job numbers, drawing numbers, customers, programmer names, internal checklist workflow, local exports, and internal software/process references:

- `pages/99_Checklist.py`
- `archive/99_Checklist_legacy.py`
- `checklist_utils.py`

Specific blockers:

- `checklist_utils.py` hard-codes a private manufacturing job-folder path.
- Checklist DB fields include job number, drawing number, revision, customer, programmer, machine, material, and notes.
- Checklist exports write job-numbered files into `data/checklist_exports`.
- Checklist references internal CAD/CAM/verification tools and a machine file location.

Recommendation: remove the checklist feature from public app scope or redesign later as a generic local checklist without customer/job/private path fields.

### Private File Paths

- `run_toolkit.bat`
  - Contains a private local Windows path that points to the old/private folder name.
- `checklist_utils.py`
  - Contains a private network/local manufacturing job-folder path.
- `pages/4_Standards.py`
  - Displays selected local document paths in the UI.

### Internal Prompt Bridge / Development Workflow

These are not machining app features and should not ship publicly unless intentionally documented for contributors:

- `bridge.config.json`
- `scripts/start_prompt_bridge.ps1`
- `docs/prompt_bridge.md`
- `docs/prompts/master_prompt.txt`
- `docs/prompts/inbox/example.md`
- `docs/prompts/done/.gitkeep`

Recommendation: remove from public app repo or move to private developer tooling.

### G/M Code Machine-Specific Content

- `data/g_m_codes.py`
  - Contains machine-specific warnings.
  - Contains steady-rest family references.
  - Uses wording like `Your machine notes`.
- `pages/6_G_M_Codes.py`
  - Includes machine-specific filters.

Recommendation: keep general G/M codes, but remove internal machine-specific filters and notes.

### Center Drill Shop Calibration Data

- `data/center_drills.py`
- `pages/3_Calculators.py`

Specific concern:

- Multiple entries include `mastercam_full_z_depth` and calibration notes saying values came from a handwritten shop/Mastercam list.

Recommendation: human review required. Either generalize to chart-only center drill data or clearly document source and remove shop-specific calibration wording.

## Unsure Items That Need Human Review

- `data/woodruff_keys.py`
  - Looks useful and likely general, but source/licensing should be confirmed before public release.
- `data/woodruff_reference.py`
  - General reference values may be acceptable, but sources and licensing should be confirmed.
- `data/materials.py`
  - Machining values may be public-useful but should be reviewed for whether they are private shop-proven values. Public version should label them as general starting points.
- `data/tooling.py`
  - Needs review for whether it contains vendor/private tool choices or private shop preferences.
- `data/center_drills.py`
  - Needs review because of Mastercam/shop-derived depth values.
- `pages/3_Calculators.py`
  - Contains calculator logic that should be kept, but wording around shop/Mastercam-derived center drill values needs review.
- `docs/workflow.md`
  - Current internal agent workflow may be harmless, but it duplicates older private-agent language and should be replaced by public contributor docs.
- `archive/`
  - Archive content should not ship publicly unless explicitly cleaned and reviewed.
- `machines/`
  - Entire folder appears internal-machine oriented and should be reviewed for removal.
- `run_toolkit.bat`
  - Could be rewritten later for public repo path, but currently contains a private local path.

## Recommended Cleanup Order

1. Freeze pushes until this audit is reviewed.
2. Remove or ignore generated/private runtime data before release, including checklist databases/exports if present.
3. Remove private standards PDFs and the `standards/` tree from the public repo, or replace with original generic reference docs.
4. Remove private branding from app pages and delete private logo assets.
5. Remove or hide the Standards page until it is rewritten as a public generic References page.
6. Remove or hide the Machines page and private machine datasets until a generic public machine template exists.
7. Remove the Checklist page, archive checklist, and `checklist_utils.py`, or redesign as a generic public checklist with no job/customer/private path fields.
8. Clean `data/g_m_codes.py` and `pages/6_G_M_Codes.py` to keep only general public G/M code references.
9. Review `data/materials.py`, `data/tooling.py`, `data/center_drills.py`, `data/woodruff_keys.py`, and `data/woodruff_reference.py` for source/licensing and public wording.
10. Add disclaimers that speeds, feeds, and machining values are general reference starting points.
11. Add tests for formulas before changing calculator behavior.
12. Replace internal docs and prompt bridge files with public contributor documentation.
13. Run a final privacy scan for company names, customer names, job numbers, drawings, private paths, proprietary standards, and machine-specific internal notes.
14. Run tests and import checks.
15. Commit focused cleanup changes only after review.
16. Push only to the confirmed public repo.

## Current Release Risk Summary

This repo is not ready for public release yet.

Primary blockers:

- Private/company branding is visible in the app.
- Customer/company/proprietary standards PDFs are present.
- Internal machine notes and post behavior are present.
- Checklist/job/customer/drawing workflows are present.
- Private local file paths are present.
- Calculator formulas are not broadly tested yet.

The calculator and general reference features are worth preserving, but the private/internal surfaces should be removed or generalized before the first public push/release.
