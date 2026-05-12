# Formula Validation Report

## Scope

Verification pass for the public CNC Programmer Toolkit calculator logic and machining formulas. This review focused on calculator correctness, public safety, and regression coverage without changing app behavior.

Agents applied:

- Machining Logic Agent
- Testing & Formula Validation Agent
- Privacy/Safety Review Agent

## Files Inspected

- `utils/formulas.py`
- `utils/holemaking.py`
- `utils/triangle.py`
- `pages/1_Speeds_Feeds.py`
- `pages/2_Threads.py`
- `pages/3_Calculators.py`
- `data/materials.py`
- `data/threads_data.py`
- `data/woodruff_keys.py`
- `data/woodruff_reference.py`
- `data/center_drills.py`
- `tests/test_woodruff_display_rows.py`

## Tests Added

Added `tests/test_formula_validation.py` with coverage for:

- RPM from SFM and diameter.
- SFM/RPM round trip.
- IPM from RPM, flutes, and chipload.
- Turning feed staying in IPR unless intentionally converted to IPM.
- Drill feed in IPM from RPM and IPR.
- Tap feed from TPI and metric pitch.
- Chamfer diameter math using documented included-angle assumptions.
- Center drill depth/diameter inverse behavior.
- Right-triangle 3-4-5 case.
- Imperial and metric thread parsing.
- ID tap drill calculations.
- OD thread model diameter, thread depth estimate, and IPR feed.
- Inch/mm conversion reference cases.

Added `pytest.ini` so pytest ignores generated cache folders named `pytest-cache-files-*` during collection.

## Formulas Verified

### RPM From SFM

Implementation:

```text
RPM = (SFM * 12) / (pi * diameter)
```

This is equivalent to the common shop approximation:

```text
RPM = SFM * 3.82 / diameter
```

Status: verified.

### SFM From RPM

Implementation:

```text
SFM = (RPM * pi * diameter) / 12
```

Status: verified by round-trip test.

### Feed Conversions

Turning feed remains IPR in turning workflows and is only converted to IPM for display when RPM is known.

Verified formulas:

```text
IPM = IPR * RPM
IPR = IPM / RPM
```

Status: verified.

### Milling Chipload Feed

Formula inspected in the speeds/feeds page:

```text
IPM = RPM * flutes * chipload
```

Status: verified by reference test case.

### Drill Feed

Implementation:

```text
IPM = RPM * IPR
```

Status: verified.

### Tap Feed

Imperial tap feed:

```text
IPM = RPM / TPI
```

Metric tap feed:

```text
mm/min = RPM * pitch_mm
IPM = RPM * pitch_mm / 25.4
```

Status: verified.

### Chamfer and Pilot Hole Math

Chamfer diameter growth uses the included angle:

```text
target_diameter = existing_diameter + 2 * axial_drop * tan(included_angle / 2) - backoff
```

Chamfer axial depth uses the inverse cone relationship:

```text
axial_depth = (target_diameter - existing_diameter) / (2 * tan(included_angle / 2))
```

Per-side angle inputs are converted to included angle before the same formula is used.

Status: verified with 90 degree included-angle, per-side angle equivalence, and invalid geometry cases.

### Center Drill Math

Center drill depth and diameter calculations use the same included-angle geometry and were verified as inverse operations for a 90 degree included-angle tool.

```text
required_depth = C_offset + (target_spot_diameter - pilot_diameter) / (2 * tan(included_angle / 2))
```

Status: verified with 90 degree and 60 degree included-angle cases, inverse diameter checks, and invalid geometry cases.

### Triangle Calculator

Right-triangle solver verified with a 3-4-5 case.

Status: verified.

### Thread Calculations

Verified:

- Imperial thread callout parsing, including fractional nominal sizes.
- Metric thread callout parsing.
- ID basic drill estimate: `nominal_dia - pitch`.
- ID percent drill estimate: `nominal_dia - thread_percent * pitch`.
- OD model diameter drop: `0.07 * pitch`.
- OD thread depth estimate: `0.6495 * pitch`.
- OD threading feed remains pitch in IPR.

Status: verified.

### Woodruff Logic

Existing Woodruff tests continue to cover display rows and key lookup compatibility. No Woodruff formula changes were made.

Status: existing coverage retained.

## Bugs Found

No clear calculator formula bug was found during this pass.

## Notes For Future Cleanup

- `pages/1_Speeds_Feeds.py` uses the common `3.82` RPM shortcut in the Woodruff section, while `utils/formulas.py` uses the more exact `12 / pi` constant. The numerical difference is tiny and not a current bug, but using the shared helper later would improve consistency.
- `utils.triangle.solve_triangle` treats zero values as missing because it checks truthiness. Current UI inputs require positive values, so this does not affect normal app use.
- Some center drill reference wording mentions shop/Mastercam-derived measurements. That is not a formula bug, but should be reviewed before public release for source clarity and public-safe wording.

## Privacy/Safety Review

No customer names, job numbers, private Windows paths, Empower references, drawings, setup sheets, or real CNC programs were found in the inspected calculator/source files during this pass.

Generic policy wording in safety documents may still mention terms such as customer, drawing, or job number as examples of prohibited content. Those are documentation guardrails, not private data.
