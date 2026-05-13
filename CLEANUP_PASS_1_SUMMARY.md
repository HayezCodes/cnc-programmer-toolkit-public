# Cleanup Pass 1 Summary

Cleanup date: 2026-05-11

Scope: removed only obvious public-release blockers identified in `PUBLIC_SAFETY_AUDIT.md` and `PUBLIC_CLEANUP_PLAN.md`. No calculator formulas were changed. No push was performed.

## Removed Files And Folders

### Company/Customer Standards And Drawings

Removed the entire tracked `standards/` content because it contained company/customer standards, drawing-like filenames, revision IDs, and proprietary-looking PDFs.

- Private/customer standards PDFs and drawing/process documents under the removed `standards/` tree.

Why: these are not public-safe and should not ship in a public repo.

### Private Standards Browser

- `pages/4_Standards.py`

Why: browsed company/customer standards folders, opened local files/folders, and displayed local file paths.

### Machine-Specific Internal Notes

- `pages/5_Machines.py`
- `data/machines_data.py`
- `data/machine_change_log.csv`
- `machines/data/lathe_specs.py`
- `machines/data/machine_list.py`
- `machines/data/mill_specs.py`

Why: contained internal machine names/numbers, post behavior, workholding notes, steady-rest details, machine correction workflow, and shop-specific process notes.

### Checklist / Job Workflow

- `pages/99_Checklist.py`
- `archive/99_Checklist_legacy.py`
- `checklist_utils.py`

Why: contained job number, drawing number, customer, programmer, private job-folder path, internal checklist flow, and internal software/process references.

### Private Prompt Bridge / Internal Dev Tooling

- `bridge.config.json`
- `scripts/start_prompt_bridge.ps1`
- `docs/prompt_bridge.md`
- `docs/prompts/done/.gitkeep`
- `docs/prompts/inbox/example.md`
- `docs/prompts/master_prompt.txt`

Why: internal prompt bridge workflow, not part of the public CutWise app.

### Private Branding And Private Path Script

- Private company logo asset
- `run_toolkit.bat`

Why: company logo/private branding and a local private path pointing at the old private toolkit folder.

## Minimal Public-Safety Edits Made

- `app.py`
  - Removed logo usage and private branding.
  - Removed Standards and Machines cards/links so the app does not point at deleted private pages.
  - Kept public entry points for Speeds & Feeds, Threads, Calculators, and G & M Codes.
- `utils/ui_helpers.py`
  - Removed Standards and Machines sidebar links.
- `pages/1_Speeds_Feeds.py`
  - Replaced private caption with a general reference disclaimer.
- `pages/2_Threads.py`
  - Replaced private caption with a public thread-reference disclaimer.
- `pages/3_Calculators.py`
  - Replaced private caption with public calculator wording.
- `pages/6_G_M_Codes.py`
  - Replaced private caption with public control-variation wording.
  - Removed machine-specific filter options.
- `data/materials.py`
  - Removed obvious private-company/machine-brand wording from remaining public material notes.
- `data/g_m_codes.py`
  - Removed machine-specific rows and warnings.
  - Generalized control-dependent notes.

## Preserved Public-Safe Core

- Speeds and feeds page and formulas
- Thread tools and thread data
- Calculator page
- Triangle, keyway, chamfer, drill breakthrough, center drill, unit conversion, and Woodruff support
- General material data pending future review/disclaimer pass
- General G/M code reference after first-pass private machine cleanup
- Existing Woodruff display tests

## Validation

- `python -m pytest`
  - Result: 7 passed
  - Warning: pytest could not create `.pytest_cache` due to sandbox permission; tests still passed.
- `python -m compileall app.py pages utils data tests`
  - Result: passed
- Public app/data source scan for obvious private markers outside audit/plan docs:
  - No remaining hits in `app.py`, `pages/`, `data/`, `utils/`, `README.md`, `docs/`, or `tests` for the first-pass blocker terms checked.

## Not Done In Pass 1

- No formulas were changed.
- No calculator behavior was refactored.
- No UI redesign was performed.
- No unsure data was deleted.
- No commit was created.
- No push was performed.

## Remaining Follow-Up

- Review and generalize `data/center_drills.py` shop/Mastercam-derived wording and values.
- Review source/licensing for `data/woodruff_keys.py` and `data/woodruff_reference.py`.
- Add formula tests beyond the current Woodruff display tests.
- Update README for the cleaned public app.
- Run a final privacy scan before any public push.
