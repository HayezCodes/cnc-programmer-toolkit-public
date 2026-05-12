# General Reference Expansion

## Added References

Added a public-safe reference library inside the existing G/M Codes destination. The page now includes tabs for:

- Common G/M codes and quick-use examples
- Center drill chart-style reference
- Spot drill angle reference
- Countersink and chamfer terminology
- Drill depth and chip evacuation guidelines
- Thread class quick reference
- Locknut and bearing nut reference categories
- Tap drill percent starting points
- Insert naming breakdown
- Toolholder shorthand
- Decimal/fraction conversion
- Surface finish reference
- Common reamer allowance starting points

## Data Cleanup

- Removed CAM-derived center drill calibration depth fields from `data/center_drills.py`.
- Reworded center drill preset notes as general chart-style references.
- Replaced a vendor-specific drill category with the generic `Carbide Drill` category.
- Reworded the Woodruff cutter placeholder to avoid shop-specific approval language.

## Locknut Reference Scope

Added generic locknut and bearing nut identification guidance for KM, AN, N, and general bearing locknut families. The Threads page now includes an interactive Locknut Lookup.

Loaded designations and guide entries:

- KM0 through KM10 with metric thread/pitch and matching MB washer reference, all marked catalog-verify.
- N 07 through N 14 with Timken catalog-reference bearing bore, thread/TPI, shaft S-3, and W washer references.
- AN 15 through AN 40 with Timken catalog-reference bearing bore, thread/TPI, shaft S-3, and W washer references.
- Bearing locknut guide entries for KM/KML metric, N inch, AN inch, HM/HME metric, and integral-locking families.

Dimensions, washer compatibility, locking device, keyway, and spanner data are explicitly marked as manufacturer-catalog verification items. Locknut source guidance points users to SKF, Timken, Whittet-Higgins, or the current locknut manufacturer catalog before machining.

Source families used:

- Timken inch accessories locknut/lockwasher catalog tables.
- SKF lock nuts requiring a keyway catalog family.
- Whittet-Higgins industry standard locknut and lockwasher catalog families.

## Public-Safety Notes

All newly added values are broad reference starting points. They are not company standards, customer requirements, or machine-specific setup instructions.

Users should verify all values against:

- the print
- tool vendor data
- machine/control documentation
- material condition
- inspection requirements

## Questionable Data Needing Future Review

Existing Woodruff key references cite public-looking sources, but source/licensing review should still be completed before a formal public release.
