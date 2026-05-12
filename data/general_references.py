REFERENCE_NOTE = (
    "General reference only. Treat values as starting points and verify against the print, tool vendor data, "
    "machine manual, material condition, and shop quality requirements."
)


SPOT_DRILL_ANGLE_REFERENCES = [
    {
        "Angle": "60 deg included",
        "Common use": "Center-drill style spotting or matching 60 deg center features",
        "Programming note": "Verify the actual tool point and pilot geometry.",
    },
    {
        "Angle": "82 deg included",
        "Common use": "Imperial flat-head screw countersink reference",
        "Programming note": "Use a countersink/chamfer calculator for diameter-to-depth math.",
    },
    {
        "Angle": "90 deg included",
        "Common use": "General spot/chamfer reference and metric flat-head countersink reference",
        "Programming note": "Common for edge breaks and spotting before drilling.",
    },
    {
        "Angle": "100 deg included",
        "Common use": "Aerospace-style flat-head fastener reference in some applications",
        "Programming note": "Confirm the fastener/print requirement before using.",
    },
    {
        "Angle": "120 deg included",
        "Common use": "Spotting before 118 deg drills or bell-style center features",
        "Programming note": "Often chosen to keep the drill web centered without a narrow 90 deg spot.",
    },
]


COUNTERSINK_CHAMFER_REFERENCES = [
    {
        "Feature": "Edge break chamfer",
        "Typical callout": ".005-.015 x 45 deg or similar",
        "Use note": "A general deburr/edge-break callout; verify inspection expectation.",
    },
    {
        "Feature": "Hole chamfer",
        "Typical callout": "Diameter or width plus angle",
        "Use note": "Program from pilot diameter, target OD, and included/per-side angle.",
    },
    {
        "Feature": "Countersink",
        "Typical callout": "Major diameter plus included angle",
        "Use note": "Usually tied to fastener seating; verify fastener standard and depth tolerance.",
    },
    {
        "Feature": "Break sharp edges",
        "Typical callout": "Remove burrs / break sharp",
        "Use note": "Do not assume a large chamfer unless the print gives a size.",
    },
]


DRILLING_GUIDELINES = [
    {
        "Topic": "Peck depth",
        "Reference starting point": "Short chips: light pecks or no peck. Stringy/deep holes: reduce peck length.",
        "Check": "Chip packing, coolant reach, flute length, drill style.",
    },
    {
        "Topic": "Deep-hole threshold",
        "Reference starting point": "Watch chip evacuation once depth exceeds about 3x diameter.",
        "Check": "Use vendor guidance for coolant-through drills and high-performance drills.",
    },
    {
        "Topic": "Breakthrough",
        "Reference starting point": "Add point height plus a small clearance past breakthrough.",
        "Check": "Avoid excessive exit burrs and tool overtravel into fixtures.",
    },
    {
        "Topic": "Spotting",
        "Reference starting point": "Spot only enough to guide the drill or meet the chamfer/countersink requirement.",
        "Check": "Spot angle, drill point angle, and final hole size tolerance.",
    },
]


THREAD_CLASS_REFERENCES = [
    {
        "System": "Unified inch",
        "Class": "1A / 1B",
        "Quick meaning": "Loose fit, easy assembly",
        "Use note": "Uncommon for precision machined parts unless specified.",
    },
    {
        "System": "Unified inch",
        "Class": "2A / 2B",
        "Quick meaning": "General-purpose external/internal thread fit",
        "Use note": "Common default when no tighter fit is required.",
    },
    {
        "System": "Unified inch",
        "Class": "3A / 3B",
        "Quick meaning": "Closer fit with less allowance",
        "Use note": "Use when the print calls it out; inspection is more sensitive.",
    },
    {
        "System": "ISO metric",
        "Class": "6g / 6H",
        "Quick meaning": "Common external/internal metric thread fit",
        "Use note": "Verify pitch, tolerance class, and gage requirement.",
    },
]


LOCKNUT_REFERENCE_NOTE = (
    "Locknut and bearing nut labels vary by manufacturer and standard. Use these rows as identification guidance only; "
    "verify dimensions, thread, washer, and spanner data with SKF, Timken, Whittet-Higgins, "
    "or the locknut manufacturer's current catalog before machining."
)


LOCKNUT_REFERENCE_CATEGORIES = [
    {
        "Family": "KM locknuts",
        "Common context": "Metric bearing locknuts with tab washer or locking clip variants",
        "Thread reference": "Metric fine threads; examples include KM0 M10x0.75, KM1 M12x1, KM2 M15x1, KM3 M17x1",
        "Washer / lock": "Often paired with MB tab washers where applicable",
    },
    {
        "Family": "AN locknuts",
        "Common context": "Inch-series bearing locknuts used with bearing adapter sleeves and shafts",
        "Thread reference": "Inch thread series varies by size and manufacturer",
        "Washer / lock": "Often paired with compatible lock washers or locking plates",
    },
    {
        "Family": "N locknuts",
        "Common context": "Inch-series bearing retaining nuts in some catalogs",
        "Thread reference": "Catalog-specific inch threads",
        "Washer / lock": "Verify matching washer or locking device by nut series",
    },
    {
        "Family": "Bearing locknuts",
        "Common context": "General term for nuts retaining bearings, sleeves, gears, or precision components",
        "Thread reference": "Can be metric or inch; never assume interchange from label alone",
        "Washer / lock": "May use tab washers, lock plates, set screws, or clamp-style locking",
    },
]


LOCKNUT_WORKFLOW_CHECKS = [
    {"Check": "Thread form and pitch", "Why it matters": "A similar nut number can still differ by thread standard or catalog family."},
    {"Check": "Washer / locking device", "Why it matters": "Tab washer, clip, plate, or set-screw locking features are not interchangeable by appearance alone."},
    {"Check": "Bearing or sleeve series", "Why it matters": "Bearing locknuts often pair with adapter sleeves or withdrawal sleeves."},
    {"Check": "Face clearance and spanner access", "Why it matters": "Nut OD, slot geometry, and nearby shoulders affect assembly tooling."},
]


TAP_DRILL_PERCENT_REFERENCES = [
    {
        "Thread percent": "55-65%",
        "General use": "Tough materials or hand tapping relief",
        "Note": "Lower torque, less thread engagement.",
    },
    {
        "Thread percent": "70-75%",
        "General use": "Common starting range for many cut taps",
        "Note": "Balance holding strength and tapping load.",
    },
    {
        "Thread percent": "80%+",
        "General use": "Only when print/process requires high engagement",
        "Note": "Higher torque and greater tap breakage risk.",
    },
]


INSERT_NAMING_BREAKDOWN = [
    {"Position": "1", "Example": "D in DNMG", "Meaning": "Insert shape"},
    {"Position": "2", "Example": "N in DNMG", "Meaning": "Clearance angle"},
    {"Position": "3", "Example": "M in DNMG", "Meaning": "Tolerance class"},
    {"Position": "4", "Example": "G in DNMG", "Meaning": "Hole/chipbreaker/clamping style"},
    {"Position": "Numbers", "Example": "432 or 1506", "Meaning": "Size, thickness, and nose radius family"},
]


SURFACE_FINISH_REFERENCES = [
    {"Ra microinch": "250", "Typical context": "Rough machined surface", "Programming note": "Heavy feed marks usually acceptable only where specified."},
    {"Ra microinch": "125", "Typical context": "General machined finish", "Programming note": "Common non-critical machined surface target."},
    {"Ra microinch": "63", "Typical context": "Improved machined finish", "Programming note": "Often needs controlled feed, nose radius, and stable setup."},
    {"Ra microinch": "32", "Typical context": "Fine machined finish", "Programming note": "May require finish pass, sharp/stable tool, or process control."},
    {"Ra microinch": "16 or finer", "Typical context": "Precision/sealing surfaces", "Programming note": "May require grinding, honing, polishing, or special tooling."},
]


REAMER_ALLOWANCE_REFERENCES = [
    {"Hole size": "Under .250 in", "Stock before ream": ".003-.006 in", "Note": "Use the low end for tight control and rigid setups."},
    {"Hole size": ".250-.500 in", "Stock before ream": ".005-.010 in", "Note": "Common starting range for chucking reamers."},
    {"Hole size": ".500-1.000 in", "Stock before ream": ".008-.015 in", "Note": "Adjust for material, tool style, and hole condition."},
    {"Hole size": "Over 1.000 in", "Stock before ream": ".010-.020 in", "Note": "Verify with reamer vendor and inspection requirement."},
]


TOOLHOLDER_SHORTHAND = [
    {"Shorthand": "ER collet", "Meaning": "General collet system for round tools", "Use note": "Good all-purpose holding; verify runout and projection."},
    {"Shorthand": "Endmill holder", "Meaning": "Set-screw side-lock holder", "Use note": "Strong axial retention; can add runout versus precision collets/shrink."},
    {"Shorthand": "Shrink fit", "Meaning": "Thermal clamping holder", "Use note": "Good rigidity/runout when tooling and holder are in good condition."},
    {"Shorthand": "Hydraulic holder", "Meaning": "Hydraulic expansion holder", "Use note": "Good damping and runout for many finishing applications."},
    {"Shorthand": "Boring bar L/D", "Meaning": "Length-to-diameter ratio", "Use note": "Longer projection increases chatter risk; reduce stickout where possible."},
]


DECIMAL_FRACTION_ROWS = [
    {"Fraction": "1/64", "Decimal": "0.0156", "MM": "0.397"},
    {"Fraction": "1/32", "Decimal": "0.0313", "MM": "0.794"},
    {"Fraction": "1/16", "Decimal": "0.0625", "MM": "1.588"},
    {"Fraction": "3/32", "Decimal": "0.0938", "MM": "2.381"},
    {"Fraction": "1/8", "Decimal": "0.1250", "MM": "3.175"},
    {"Fraction": "3/16", "Decimal": "0.1875", "MM": "4.763"},
    {"Fraction": "1/4", "Decimal": "0.2500", "MM": "6.350"},
    {"Fraction": "5/16", "Decimal": "0.3125", "MM": "7.938"},
    {"Fraction": "3/8", "Decimal": "0.3750", "MM": "9.525"},
    {"Fraction": "1/2", "Decimal": "0.5000", "MM": "12.700"},
]


GM_QUICK_EXAMPLES = [
    {
        "Scenario": "Safe start line",
        "Example": "G17 G20 G40 G49 G80 G90",
        "Note": "Common mill-style modal reset pattern. Verify control and post requirements.",
    },
    {
        "Scenario": "Work offset call",
        "Example": "G54",
        "Note": "Calls the first work coordinate system on many controls.",
    },
    {
        "Scenario": "Coolant state",
        "Example": "M08 / M09",
        "Note": "Coolant on/off on many controls.",
    },
    {
        "Scenario": "End program",
        "Example": "M30",
        "Note": "End and reset/rewind behavior on many controls.",
    },
]
