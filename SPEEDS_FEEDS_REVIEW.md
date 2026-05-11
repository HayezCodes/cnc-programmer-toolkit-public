# Speeds and Feeds Review

## Scope

Review of public safety and machining reasonableness for speeds/feeds and related reference data. This pass did not change values or app behavior.

## Files Reviewed

- `pages/1_Speeds_Feeds.py`
- `data/materials.py`
- `data/tooling.py`
- `data/woodruff_reference.py`
- `data/woodruff_keys.py`
- `data/center_drills.py`

## Public Safety Status

The speeds/feeds page currently states that values are general reference starting values and must be verified against vendor data, machine condition, setup, and material.

No obvious private/company/customer data was found in the active speeds/feeds source files during this pass.

## Data That Appears Public-Safe

- General material families such as 10 Series Steel, 40 Series Steel, Stainless, Aluminum, Brass/Bronze, Cast Iron, Titanium, Inconel, Hastelloy, Monel, Tool Steel, and Plastic.
- Generic turning roughing/finishing groupings.
- General drill, tap, endmill, thread, chamfer, center drill, and Woodruff reference workflows.
- General ANSI-style Woodruff key size references, pending source/licensing review.

## Questionable Or Review-Needed Values

These are not confirmed bugs. They should be reviewed by a human machinist/programmer before public release or clearly treated as conservative/general starting points.

### Steel Turning Baselines

Some 10 Series Steel roughing and finishing SFM/DOC values may be aggressive depending on insert grade, holder rigidity, machine horsepower, workholding, coolant, and part geometry.

Recommendation: keep the disclaimer prominent and review values against common vendor catalogs before public release.

### Hi-Feed Milling Ranges

Hi-feed endmill values can be very tool-specific. Current ranges may be reasonable for some insert cutters but unsafe for others.

Recommendation: mark hi-feed values as tool-vendor-dependent starting points or generalize the tool names later.

### Vendor-Specific Tool Names

The data and UI include names such as:

- `CoroDrill`
- `1/2 Ingersoll Rougher (Hi-Feed)`

These are not private company data, but they are vendor/tool-specific. Public release may be cleaner if these become generic categories such as carbide drill, indexable drill, and hi-feed insert mill.

Recommendation: generalize labels in a later cleanup pass without changing formulas.

### Woodruff Reference Data

Woodruff reference data is useful for machinists, but the public source and licensing basis should be reviewed before release.

Recommendation: retain tests and logic, then document source assumptions or replace with clearly public/reference-derived data.

### Center Drill Reference Data

Some center drill wording and values appear shop-derived or Mastercam-calibration-derived. No private customer data was found, but the source should be clarified.

Recommendation: change wording later to public-safe reference language and document assumptions.

### Shop-Approval Wording

Some placeholder/reference notes mention shop-approved values. This is not private by itself, but a public toolkit should probably use wording like user-verified, vendor-verified, or locally approved.

Recommendation: revise wording in a later documentation/data cleanup pass.

## Disclaimers

Current page-level disclaimer is appropriate for a public app:

- Values are general reference starting values.
- Users must verify against tool vendor data.
- Users must account for machine condition, setup, workholding, coolant, and material condition.

Recommendation: keep this disclaimer visible anywhere speeds/feeds are shown.

## Data Changes Made

No speeds/feeds values were changed during this review.

## Privacy/Safety Notes

No obvious Empower-specific standards, customer names, job numbers, drawings, private shop file paths, setup sheets, or real CNC programs were found in the reviewed speeds/feeds files.

