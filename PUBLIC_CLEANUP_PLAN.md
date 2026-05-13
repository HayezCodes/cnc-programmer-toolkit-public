# Public Cleanup Plan

Plan date: 2026-05-11

Scope: planning only. Do not delete, move, refactor, commit, or push until this plan is reviewed and approved.

Goal: turn this copied repo into a clean public CutWise app while preserving public-safe calculators, thread tools, drill/tap charts, chamfer/triangle math, Woodruff/keyway support, and general machining references.

## 1. Remove Completely Before Public Release

These files/folders should not remain in the public repo after the approved cleanup pass.

### Private Standards And Drawings

- `standards/`

Reason: contains customer/company folders, drawing-like filenames, revision IDs, proprietary standards, and private standards PDFs.

Examples:

- Private/customer standards folders with company/customer names.

Risk before removing:

- Confirm no public-safe original reference document is mixed into `standards/`.
- Confirm calculators do not depend on PDF contents at runtime.

### Private Branding Assets

- Private company logo asset

Reason: private/company branding asset.

Risk before removing:

- Remove or replace all app references to this image first so the home page does not show a missing asset.

### Private Job/Checklist Runtime Data

Remove if present:

- `data/checklist_logs.db`
- `data/checklist_exports/`

Reason: may contain job numbers, drawing numbers, customer names, programmer names, and notes.

Risk before removing:

- Confirm whether any local-only records need to be backed up outside the public repo before deletion.

### Internal Prompt Bridge Tooling

Recommended removal from public repo:

- `bridge.config.json`
- `scripts/start_prompt_bridge.ps1`
- `docs/prompt_bridge.md`
- `docs/prompts/`

Reason: internal development workflow, not part of the public CNC app.

Risk before removing:

- Confirm the public repo does not need this workflow for contributors.

## 2. Move To A Private-Only Backup Folder Outside This Repo

Before deleting from the public repo, copy these to a private backup location outside `cnc-programmer-toolkit-public`.

Recommended private backup root:

```text
<private-backup-folder-outside-this-repo>
```

Do not commit that backup folder. Do not place it inside this repo.

### Must Back Up Outside Repo

- `standards/`
- `archive/99_Checklist_legacy.py`
- `pages/99_Checklist.py`
- `checklist_utils.py`
- `data/machines_data.py`
- `machines/`
- `data/machine_change_log.csv`
- `bridge.config.json`
- `scripts/start_prompt_bridge.ps1`
- `docs/prompt_bridge.md`
- `docs/prompts/`
- `run_toolkit.bat` if the old private path is still useful

Reason:

- These files contain private workflow, private file paths, internal machine notes, customer/job fields, internal post behavior, or private development tooling.

Risks before moving:

- Verify the private backup folder is outside this repo.
- Verify copied backup files are readable before removing originals from the public repo.
- Verify `.gitignore` will ignore the backup folder if the backup path is ever near the workspace.

## 3. Generalize With Sample Data

These should stay in the public app after cleanup, but need private wording removed, public disclaimers added, and sample/general data substituted where needed.

### Public Machining Data

- `data/materials.py`

Generalize:

- Replace private-company baseline notes with `general reference starting point`.
- Replace vendor/machine-specific notes with generic wording.
- Add a clear data-level disclaimer that values are starting points and must be verified by tool vendor, machine condition, setup, and material lot.

Risk before editing:

- Preserve lathe IPR and mill IPM behavior.
- Preserve material keys used by pages and tests.

### Center Drill Data

- `data/center_drills.py`
- related center drill wording in `pages/3_Calculators.py`

Generalize:

- Keep chart-style center drill geometry if public-safe.
- Remove `Mastercam` and `handwritten shop list` wording.
- Decide whether `mastercam_full_z_depth` values are private shop calibration data or acceptable reference values.
- If unsure, use chart-derived geometry only.

Risk before editing:

- Center drill calculator behavior may depend on `mastercam_full_z_depth` and `full_z_verified`.
- Add formula tests before changing this logic.

### Woodruff Data

- `data/woodruff_keys.py`
- `data/woodruff_reference.py`

Generalize:

- Keep only if source/licensing is acceptable for public use.
- Label feed values as general reference starting points.
- Keep Woodruff lookup and keyway support because they are core public value.

Risk before editing:

- Confirm source/licensing for dimensional tables.
- Preserve `tests/test_woodruff_display_rows.py`.

### G/M Code Reference

- `data/g_m_codes.py`
- `pages/6_G_M_Codes.py`

Generalize:

- Keep common G/M codes.
- Remove machine-specific filters/entries and wording like `Your machine notes`.
- Replace with generic control-warning language where useful.

Risk before editing:

- Preserve searchable table behavior.
- Avoid implying all controls use identical meanings for ambiguous codes.

### Public Docs

- `README.md`
- `docs/workflow.md`
- `ROADMAP_PUBLIC.md`
- `PUBLIC_SAFETY_AUDIT.md`
- `AGENTS.md`

Generalize:

- Update docs toward public contributor/user guidance.
- Keep safety and cleanup docs until the public release is clean.
- Add data editing docs later.

Risk before editing:

- Avoid documenting private paths or internal workflow.

## 4. Disable Temporarily Instead Of Deleting

These app-facing features should be disabled from navigation first, then removed or rewritten after review.

### Standards Page

- `pages/4_Standards.py`

Temporary action:

- Remove from sidebar/home navigation.
- Do not expose `standards/` browsing in public UI.

Long-term public replacement:

- `pages/4_References.py` with original generic reference notes, no PDFs, no customer/company names, no local file opening.

Risk before disabling:

- Update `utils/ui_helpers.py` and `app.py` navigation together so no dead links remain.

### Machines Page

- `pages/5_Machines.py`

Temporary action:

- Remove from sidebar/home navigation.
- Do not expose machine-specific internal notes.

Long-term public replacement:

- Optional generic machine capability planner using sample machine profiles only.

Risk before disabling:

- `pages/99_Checklist.py` imports `MACHINES`; if Checklist remains present, removing machine data can break it.

### Checklist Page

- `pages/99_Checklist.py`
- `archive/99_Checklist_legacy.py`
- `checklist_utils.py`

Temporary action:

- Keep out of navigation and do not expose in public app.
- Prefer moving to private backup before first public release.

Long-term public replacement:

- Optional generic setup checklist with no job/customer/drawing fields and no private file paths.

Risk before disabling:

- Streamlit may still discover numbered files under `pages/`; confirm page visibility behavior after moving/removing.

### Machine-Specific G/M Filters

- `pages/6_G_M_Codes.py`
- `data/g_m_codes.py`

Temporary action:

- Disable machine-specific filters/rows after generalization begins.

Long-term public replacement:

- Generic `Lathe`, `Mill`, and `Both` categories only.

Risk before disabling:

- Verify dataframe filtering handles the remaining categories.

## 5. Exact Recommended Cleanup Sequence

### Step 1: Confirm Git Safety

Actions:

- Run `git remote -v`.
- Confirm remote is only the intended public repo or no remote.
- Confirm no push will happen during cleanup.

Risks to check:

- Remote accidentally points to old/internal repo.
- Dirty worktree contains unrelated user changes.

### Step 2: Create Private Backup Outside Repo

Actions:

- Create a private backup folder outside this repo.
- Copy private-risk folders/files listed in section 2.
- Verify backup exists and files are readable.

Risks to check:

- Backup accidentally created inside repo.
- Backup accidentally staged.
- Files removed before backup is verified.

### Step 3: Disable Private UI Entry Points

Actions:

- Remove Standards, Machines, and Checklist links from public navigation.
- Remove private page cards from `app.py`.
- Keep public links for Speeds & Feeds, Threads, Calculators, and G/M Codes.

Risks to check:

- Dead links in sidebar/home page.
- Streamlit still exposes hidden pages.
- App import errors from disabled pages.

### Step 4: Remove Standards PDFs From Public Repo

Actions:

- Remove `standards/` after backup.
- Replace later with original generic docs only if needed.

Risks to check:

- `pages/4_Standards.py` still expects `standards/`.
- PDFs or customer names remain elsewhere.

### Step 5: Remove Private Checklist Workflow

Actions:

- Remove or move `pages/99_Checklist.py`, `archive/99_Checklist_legacy.py`, and `checklist_utils.py`.
- Remove generated checklist DB/exports if present.

Risks to check:

- Job/customer/drawing strings remain in docs or tests.
- `MACHINES` imports remain only in removed/disabled files.

### Step 6: Remove Or Replace Machine Notes

Actions:

- Remove/move `pages/5_Machines.py`, `data/machines_data.py`, and `machines/`.
- Remove `data/machine_change_log.csv`.
- Later add generic machine sample data only if public-safe.

Risks to check:

- Machine-specific references remain in G/M code data.
- Imports break after removing `data/machines_data.py`.
- Public app still references Machines page.

### Step 7: Remove Private Branding

Actions:

- Delete the private company logo asset.
- Replace private company/author captions with CutWise branding.
- Clean `data/materials.py` private-company notes.

Risks to check:

- Missing image reference.
- Branding remains in app pages, docs, or data.

### Step 8: Remove Private Paths And Internal Tooling

Actions:

- Remove or rewrite `run_toolkit.bat`.
- Remove prompt bridge files and prompt docs if not public contributor tooling.

Risks to check:

- Private local/network Windows paths remain.
- Prompt docs still reference private workflow.

### Step 9: Generalize G/M Code Reference

Actions:

- Keep common G/M code rows.
- Remove machine-specific rows/filters.
- Use generic control-dependent warnings.

Risks to check:

- Filter categories match available data.
- No machine-specific warnings remain.

### Step 10: Review And Generalize Machining Data

Actions:

- Review `data/materials.py`, `data/tooling.py`, `data/center_drills.py`, `data/woodruff_keys.py`, and `data/woodruff_reference.py`.
- Mark values as general reference starting points.
- Resolve source/licensing questions.

Risks to check:

- Calculator keys/data structures change without tests.
- Private shop-proven values are presented as universal facts.
- Licensed/proprietary tables are published without permission.

### Step 11: Add Formula And Import Tests

Actions:

- Add tests for formulas before behavior changes.
- Cover threads, tap feed, RPM/feed helpers, triangle math, keyway math, chamfer math, drill breakthrough, center drill math, and Woodruff display rows.
- Run full test suite.

Risks to check:

- Existing calculators rely on UI-only code, making tests harder.
- Formula changes happen before tests exist.

### Step 12: Public Docs Pass

Actions:

- Update `README.md`.
- Add data editing guidance.
- Add formula notes and public safety notes.
- Keep or archive public audit/cleanup docs as desired.

Risks to check:

- Docs mention private/internal files that no longer exist.
- Docs overpromise accuracy of reference machining data.

### Step 13: Final Public Safety Scan

Actions:

- Search for company names, customer names, job numbers, drawing names, private paths, internal machine notes, proprietary standards, and old repo references.
- Confirm no private PDFs or generated data remain.

Risks to check:

- Binary files still contain private names.
- Case-only filename issues on Windows hide duplicate/renamed files.

### Step 14: Final App Verification

Actions:

- Run tests.
- Start the Streamlit app locally.
- Click through public pages.
- Verify no hidden private pages are reachable.

Risks to check:

- Navigation broken after page removals.
- Streamlit discovers files that were intended to be disabled.
- Public pages import removed private modules.

### Step 15: Commit And Push Only After Review

Actions:

- Review `git status`.
- Commit focused cleanup changes.
- Confirm `git remote -v`.
- Push only after user approval.

Risks to check:

- Untracked private files remain.
- New public remote is wrong.
- Old/internal repo is configured.

## 6. Preserve During Cleanup

Do not remove these public-value features unless a later human review finds a source/licensing problem:

- Speeds and feeds page concept
- Thread tools
- Tap/feed calculations
- Drill charts and drill/feed helpers
- Triangle calculator
- Chamfer calculators
- Keyway calculator
- Woodruff key lookup/calculator
- Drill breakthrough calculator
- Center drill calculator after source review
- Inch/mm converter
- General G/M code reference after machine-specific cleanup
- Formula helper modules under `utils/`
- Public-safe data modules after generalization

## Release Readiness Gate

The repo is not public-release ready until:

- Private standards and drawings are gone.
- Private branding is gone.
- Private file paths are gone.
- Checklist/job/customer workflows are gone or fully generalized.
- Internal machine notes are gone or replaced with sample data.
- Machining data is marked as general reference values.
- Calculator formulas are tested.
- Final privacy scan is clean.
- User approves push.
