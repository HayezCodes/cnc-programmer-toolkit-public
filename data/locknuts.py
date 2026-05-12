LOCKNUT_VERIFICATION_NOTE = (
    "Reference only. Verify dimensions, thread, washer, and spanner data with SKF, Timken, "
    "Whittet-Higgins, or the locknut manufacturer's current catalog before machining."
)


TIMKEN_INCH_SOURCE = "Timken inch accessories locknut/lockwasher catalog table"
WHITTET_STANDARD_SOURCE = "Whittet-Higgins industry standard locknut and lockwasher catalog families"
SKF_KEYWAY_SOURCE = "SKF lock nuts requiring a keyway catalog family"


LOCKNUT_SERIES = {
    "KM": {
        "label": "KM locknuts",
        "description": "Metric bearing locknut family commonly paired with MB or MBL style tab washers.",
        "standard_reference": "KM / metric bearing locknut family. Verify ISO/DIN/manufacturer catalog details.",
    },
    "AN": {
        "label": "AN locknuts",
        "description": "Heavy inch-design bearing locknut family commonly paired with W lock washers.",
        "standard_reference": "AN / inch bearing locknut family. Verify ANSI/ABMA/manufacturer catalog details.",
    },
    "N": {
        "label": "N locknuts",
        "description": "Inch-design bearing retaining nut family commonly paired with W lock washers or plates.",
        "standard_reference": "N / inch bearing locknut family. Verify ANSI/ABMA/manufacturer catalog details.",
    },
    "Bearing locknut": {
        "label": "Bearing locknuts",
        "description": "Selector guide for common bearing, sleeve, gear, and precision-component retention nuts.",
        "standard_reference": "Catalog-specific. Verify the actual bearing/sleeve/nut series.",
    },
}


def _base_entry(
    *,
    series: str,
    designation: str,
    thread: str,
    thread_size: str,
    pitch_tpi: str,
    source_family: str,
    source_note: str,
    matching_lock: str,
    bearing_bore: str = "catalog lookup required",
    shaft_diameter_reference: str = "catalog lookup required",
    major_diameter_reference: str = "catalog lookup required",
    od_reference: str = "catalog lookup required",
    thickness_reference: str = "catalog lookup required",
    keyway_spanner_reference: str = "catalog lookup required",
    programming_notes: str = "",
    needs_review: str = "Verify against current catalog.",
) -> dict:
    return {
        "series": series,
        "designation": designation,
        "thread": thread,
        "thread_size": thread_size,
        "pitch_tpi": pitch_tpi,
        "bearing_bore": bearing_bore,
        "shaft_diameter_reference": shaft_diameter_reference,
        "major_diameter_reference": major_diameter_reference,
        "source_family": source_family,
        "source_note": source_note,
        "standard_reference": LOCKNUT_SERIES[series]["standard_reference"],
        "matching_lock": matching_lock,
        "od_reference": od_reference,
        "thickness_reference": thickness_reference,
        "keyway_spanner_reference": keyway_spanner_reference,
        "programming_notes": programming_notes,
        "verification_note": LOCKNUT_VERIFICATION_NOTE,
        "verification_required": True,
        "manufacturer_catalog_required": True,
        "needs_review": needs_review,
    }


def _km_entry(designation: str, thread_size: str, pitch: str, washer: str) -> dict:
    thread = f"{thread_size}x{pitch.replace(' mm', '')}"
    return _base_entry(
        series="KM",
        designation=designation,
        thread=thread,
        thread_size=thread_size,
        pitch_tpi=pitch,
        source_family=f"{SKF_KEYWAY_SOURCE} / {WHITTET_STANDARD_SOURCE}",
        source_note="KM thread and washer references are catalog-reference values; verify current manufacturer dimensions before machining.",
        matching_lock=washer,
        major_diameter_reference=f"{thread_size} nominal metric thread",
        keyway_spanner_reference="Requires shaft/sleeve keyway for tab washer; spanner slots vary by catalog size.",
        programming_notes="Useful when checking bearing journal threads, reliefs, lock washer clearance, and wrench access.",
        needs_review="Catalog verification required before production.",
    )


def _timken_inch_entry(
    series: str,
    designation: str,
    bearing_bore_mm: str,
    major_diameter_mm: str,
    major_diameter_in: str,
    tpi: str,
    shaft_s3_mm: str,
    shaft_s3_in: str,
    washer: str,
) -> dict:
    thread = f"{major_diameter_in}-{tpi} TPI"
    return _base_entry(
        series=series,
        designation=designation,
        thread=thread,
        thread_size=major_diameter_in,
        pitch_tpi=f"{tpi} TPI",
        bearing_bore=f"{bearing_bore_mm} mm",
        shaft_diameter_reference=f"Timken Diameter S-3: {shaft_s3_mm} mm / {shaft_s3_in} in",
        major_diameter_reference=f"{major_diameter_mm} mm / {major_diameter_in} in",
        source_family=f"{TIMKEN_INCH_SOURCE} / {SKF_KEYWAY_SOURCE} / {WHITTET_STANDARD_SOURCE}",
        source_note="Bearing bore, major diameter, TPI, shaft S-3, locknut, and lockwasher are catalog-reference values from Timken inch accessory tables.",
        matching_lock=washer,
        od_reference="catalog lookup required",
        thickness_reference="catalog lookup required",
        keyway_spanner_reference="Requires shaft/sleeve keyway for W washer or catalog locking plate; verify spanner slot data by manufacturer.",
        programming_notes="Use for shaft thread, relief, washer clearance, and bearing-bore cross-checks before modeling or machining.",
        needs_review="Catalog-derived reference. Verify current catalog before production.",
    )


def _bearing_guide_entry(
    designation: str,
    source_family: str,
    matching_lock: str,
    programming_notes: str,
    thread: str = "catalog lookup required",
    thread_size: str = "catalog lookup required",
    pitch_tpi: str = "catalog lookup required",
) -> dict:
    return _base_entry(
        series="Bearing locknut",
        designation=designation,
        thread=thread,
        thread_size=thread_size,
        pitch_tpi=pitch_tpi,
        source_family=source_family,
        source_note="Guide entry only; select the exact catalog series and size before adding production dimensions.",
        matching_lock=matching_lock,
        keyway_spanner_reference="Confirm keyway, locking method, spanner slots, and wrench access in the current catalog.",
        programming_notes=programming_notes,
        needs_review="Guide entry only - catalog lookup required.",
    )


LOCKNUT_DATA = {
    "KM": [
        _km_entry("KM0", "M10", "0.75 mm", "MB0 tab washer where applicable"),
        _km_entry("KM1", "M12", "1.0 mm", "MB1 tab washer where applicable"),
        _km_entry("KM2", "M15", "1.0 mm", "MB2 tab washer where applicable"),
        _km_entry("KM3", "M17", "1.0 mm", "MB3 tab washer where applicable"),
        _km_entry("KM4", "M20", "1.0 mm", "MB4 tab washer where applicable"),
        _km_entry("KM5", "M25", "1.5 mm", "MB5 tab washer where applicable"),
        _km_entry("KM6", "M30", "1.5 mm", "MB6 tab washer where applicable"),
        _km_entry("KM7", "M35", "1.5 mm", "MB7 tab washer where applicable"),
        _km_entry("KM8", "M40", "1.5 mm", "MB8 tab washer where applicable"),
        _km_entry("KM9", "M45", "1.5 mm", "MB9 tab washer where applicable"),
        _km_entry("KM10", "M50", "1.5 mm", "MB10 tab washer where applicable"),
    ],
    "N": [
        _timken_inch_entry("N", "N 07", "35", "34.95", "1.376", "18", "31.75", "1.25", "W 07"),
        _timken_inch_entry("N", "N 08", "40", "39.70", "1.563", "18", "36.51", "1.4375", "W 08"),
        _timken_inch_entry("N", "N 09", "45", "44.88", "1.767", "18", "42.86", "1.6875", "W 09"),
        _timken_inch_entry("N", "N 10", "50", "49.96", "1.967", "18", "47.63", "1.875", "W 10"),
        _timken_inch_entry("N", "N 11", "55", "54.79", "2.157", "18", "52.39", "2.0625", "W 11"),
        _timken_inch_entry("N", "N 12", "60", "59.94", "2.360", "18", "57.15", "2.25", "W 12"),
        _timken_inch_entry("N", "N 13", "65", "64.72", "2.548", "18", "61.91", "2.4375", "W 13"),
        _timken_inch_entry("N", "N 14", "70", "69.88", "2.751", "18", "66.68", "2.625", "W 14"),
    ],
    "AN": [
        _timken_inch_entry("AN", "AN 15", "75", "74.50", "2.933", "12", "71.44", "2.8125", "W 15"),
        _timken_inch_entry("AN", "AN 16", "80", "79.68", "3.137", "12", "76.20", "3", "W 16"),
        _timken_inch_entry("AN", "AN 17", "85", "84.84", "3.340", "12", "80.96", "3.1875", "W 17"),
        _timken_inch_entry("AN", "AN 18", "90", "89.59", "3.527", "12", "85.73", "3.375", "W 18"),
        _timken_inch_entry("AN", "AN 19", "95", "94.74", "3.730", "12", "90.49", "3.5625", "W 19"),
        _timken_inch_entry("AN", "AN 20", "100", "99.52", "3.918", "12", "96.84", "3.8125", "W 20"),
        _timken_inch_entry("AN", "AN 21", "105", "104.70", "4.122", "12", "100.01", "3.9375", "W 21"),
        _timken_inch_entry("AN", "AN 22", "110", "109.86", "4.325", "12", "106.36", "4.1875", "W 22"),
        _timken_inch_entry("AN", "AN 24", "120", "119.79", "4.716", "12", "115.89", "4.5625", "W 24"),
        _timken_inch_entry("AN", "AN 26", "130", "129.69", "5.106", "12", "125.41", "4.9375", "W 26"),
        _timken_inch_entry("AN", "AN 28", "140", "139.62", "5.497", "12", "134.94", "5.3125", "W 28"),
        _timken_inch_entry("AN", "AN 30", "150", "149.56", "5.888", "12", "146.05", "5.75", "W 30"),
        _timken_inch_entry("AN", "AN 32", "160", "159.61", "6.284", "8", "153.99", "6 1/16", "W 32"),
        _timken_inch_entry("AN", "AN 34", "170", "169.14", "6.659", "8", "163.51", "6.4375", "W 34"),
        _timken_inch_entry("AN", "AN 36", "180", "179.48", "7.066", "8", "174.63", "6.875", "W 36"),
        _timken_inch_entry("AN", "AN 38", "190", "189.79", "7.472", "8", "184.15", "7.25", "W 38"),
        _timken_inch_entry("AN", "AN 40", "200", "199.31", "7.847", "8", "193.68", "7.625", "W 40"),
    ],
    "Bearing locknut": [
        _bearing_guide_entry(
            "KM / KML metric",
            f"{SKF_KEYWAY_SOURCE} / {WHITTET_STANDARD_SOURCE}",
            "MB, MBL, MBA, or catalog-compatible metric lock washer",
            "Metric shaft threads. Check nominal thread, washer tab/keyway, nut OD, width, and hook-spanner clearance.",
        ),
        _bearing_guide_entry(
            "N inch",
            f"{TIMKEN_INCH_SOURCE} / {SKF_KEYWAY_SOURCE} / {WHITTET_STANDARD_SOURCE}",
            "W washer through common catalog ranges; larger sizes may use locking plates",
            "Inch-design bearing nuts. Check bore/shaft size, major diameter, TPI, W washer or locking plate, and slot access.",
        ),
        _bearing_guide_entry(
            "AN inch",
            f"{TIMKEN_INCH_SOURCE} / {SKF_KEYWAY_SOURCE} / {WHITTET_STANDARD_SOURCE}",
            "W washer in Timken inch accessory tables",
            "Heavy inch-design bearing nuts. Useful for larger bearing bore sizes; verify TPI changeover and washer match.",
        ),
        _bearing_guide_entry(
            "HM / HME metric",
            f"{SKF_KEYWAY_SOURCE} / manufacturer metric locknut catalog family",
            "MS locking clip or catalog-specified locking device",
            "Larger metric locknut family. Check trapezoidal/metric thread form, clip hardware, and handling/eyebolt notes.",
        ),
        _bearing_guide_entry(
            "Integral-locking",
            "SKF / Whittet-Higgins / manufacturer integral-locking locknut catalog family",
            "Integral pins, screws, clamp section, or manufacturer-specific locking feature",
            "Use when the design avoids a shaft keyway. Confirm lock feature clearance, tightening sequence, and reusable limits.",
        ),
    ],
}


REQUIRED_LOCKNUT_FIELDS = (
    "series",
    "designation",
    "thread",
    "thread_size",
    "pitch_tpi",
    "bearing_bore",
    "shaft_diameter_reference",
    "major_diameter_reference",
    "source_family",
    "source_note",
    "standard_reference",
    "matching_lock",
    "od_reference",
    "thickness_reference",
    "keyway_spanner_reference",
    "programming_notes",
    "verification_note",
    "verification_required",
    "manufacturer_catalog_required",
    "needs_review",
)


def get_locknut_series_options() -> list[str]:
    return list(LOCKNUT_DATA.keys())


def get_locknut_size_options(series: str) -> list[str]:
    return [row["designation"] for row in LOCKNUT_DATA[series]]


def get_locknut_entry(series: str, designation: str) -> dict:
    for row in LOCKNUT_DATA[series]:
        if row["designation"] == designation:
            return row
    raise KeyError(f"Unknown locknut designation: {series} {designation}")
