WOODRUFF_REFERENCE_LABEL = "Reference Starting Values"
WOODRUFF_CARBIDE_SOURCE_TYPE = "Carbide-Tipped Woodruff / Keyseat Cutter"
WOODRUFF_HSS_SOURCE_TYPE = "HSS Woodruff / Keyseat Cutter"
WOODRUFF_SOURCE_TYPES = [
    WOODRUFF_CARBIDE_SOURCE_TYPE,
    WOODRUFF_HSS_SOURCE_TYPE,
]

WOODRUFF_CARBIDE_DEFAULT_IPT = 0.002

WOODRUFF_TOOTH_COUNT_BY_DIAMETER = {
    0.375: 8,
    0.500: 10,
    0.625: 10,
    0.750: 10,
    0.875: 12,
    1.000: 12,
    1.125: 14,
    1.250: 14,
    1.500: 16,
}

WOODRUFF_HSS_DIAMETER_BANDS = [
    {"key": "lte_0_0625", "label": "<= 0.0625", "min_exclusive": None, "max_inclusive": 0.0625},
    {"key": "gt_0_0625_to_0_125", "label": "> 0.0625 to 0.125", "min_exclusive": 0.0625, "max_inclusive": 0.125},
    {"key": "gt_0_125_to_0_250", "label": "> 0.125 to 0.250", "min_exclusive": 0.125, "max_inclusive": 0.250},
    {"key": "gt_0_250_to_0_375", "label": "> 0.250 to 0.375", "min_exclusive": 0.250, "max_inclusive": 0.375},
    {"key": "gt_0_375_to_0_500", "label": "> 0.375 to 0.500", "min_exclusive": 0.375, "max_inclusive": 0.500},
    {"key": "gt_0_500_to_0_750", "label": "> 0.500 to 0.750", "min_exclusive": 0.500, "max_inclusive": 0.750},
    {"key": "gt_0_750_to_1_000", "label": "> 0.750 to 1.000", "min_exclusive": 0.750, "max_inclusive": 1.000},
]

WOODRUFF_REFERENCE_DATA = {
    WOODRUFF_CARBIDE_SOURCE_TYPE: {
        "material_family_map": {
            "10 series": "low_medium_carbon_steel",
            "40 series": "low_medium_carbon_alloy_steel",
            "300 stainless": "stainless_300",
            "400 stainless": "stainless_400",
            "ph stainless": "stainless_ph",
            "titanium": "titanium",
            "aluminum": "aluminum_low_si",
            "brass": "brass_copper",
            "bronze": "brass_copper",
            "copper": "brass_copper",
            "cast iron": "cast_iron",
        },
        "closest_family_map": {
            "duplex": "stainless_300",
            "alloy 20": "stainless_300",
            "hastelloy": "nickel_iron_base_alloy",
            "monel": "nickel_iron_base_alloy",
            "zirconium": "titanium",
        },
        "families": {
            "low_medium_carbon_steel": {"sfm_min": 200, "sfm_max": 400, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "low_medium_carbon_alloy_steel": {"sfm_min": 130, "sfm_max": 330, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "stainless_300": {"sfm_min": 75, "sfm_max": 175, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "stainless_400": {"sfm_min": 135, "sfm_max": 375, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "stainless_400_free_machining": {"sfm_min": 250, "sfm_max": 500, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "stainless_ph": {"sfm_min": 75, "sfm_max": 175, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "nickel_iron_base_alloy": {"sfm_min": 75, "sfm_max": 175, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "titanium": {"sfm_min": 75, "sfm_max": 200, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "aluminum_low_si": {"sfm_min": 1200, "sfm_max": 1500, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "brass_copper": {"sfm_min": 400, "sfm_max": 550, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
            "cast_iron": {"sfm_min": 150, "sfm_max": 350, "default_ipt": WOODRUFF_CARBIDE_DEFAULT_IPT},
        },
    },
    WOODRUFF_HSS_SOURCE_TYPE: {
        "material_family_map": {
            "10 series": "carbon_steels",
            "40 series": "medium_alloy_steels",
            "300 stainless": "stainless_300",
            "400 stainless": "stainless_400",
            "ph stainless": "stainless_ph",
            "titanium": "titanium",
            "aluminum": "aluminum",
            "brass": "brass_bronze",
            "bronze": "brass_bronze",
            "copper": "copper_alloys",
            "cast iron": "cast_iron_gray",
        },
        "closest_family_map": {
            "duplex": "stainless_300",
            "alloy 20": "stainless_300",
            "hastelloy": "high_strength_tool_steels",
            "monel": "copper_alloys",
            "zirconium": "titanium",
        },
        "families": {
            "carbon_steels": {
                "sfm_min": 80,
                "sfm_max": 200,
                "ipt_ranges": {
                    "lte_0_0625": (0.0003, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0011),
                    "gt_0_250_to_0_375": (0.0005, 0.0012),
                    "gt_0_375_to_0_500": (0.0006, 0.0013),
                    "gt_0_500_to_0_750": (0.0009, 0.0015),
                    "gt_0_750_to_1_000": (0.0010, 0.0030),
                },
            },
            "medium_alloy_steels": {
                "sfm_min": 60,
                "sfm_max": 150,
                "ipt_ranges": {
                    "lte_0_0625": (0.0003, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0011),
                    "gt_0_250_to_0_375": (0.0005, 0.0012),
                    "gt_0_375_to_0_500": (0.0006, 0.0013),
                    "gt_0_500_to_0_750": (0.0009, 0.0015),
                    "gt_0_750_to_1_000": (0.0010, 0.0030),
                },
            },
            "stainless_ph": {
                "sfm_min": 30,
                "sfm_max": 75,
                "ipt_ranges": {
                    "lte_0_0625": (0.0003, 0.0008),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0012),
                    "gt_0_250_to_0_375": (0.0005, 0.0014),
                    "gt_0_375_to_0_500": (0.0006, 0.0016),
                    "gt_0_500_to_0_750": (0.0009, 0.0018),
                    "gt_0_750_to_1_000": (0.0010, 0.0020),
                },
            },
            "stainless_300_free_machining": {
                "sfm_min": 50,
                "sfm_max": 100,
                "ipt_ranges": {
                    "lte_0_0625": (0.0002, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0012),
                    "gt_0_250_to_0_375": (0.0005, 0.0014),
                    "gt_0_375_to_0_500": (0.0006, 0.0016),
                    "gt_0_500_to_0_750": (0.0009, 0.0018),
                    "gt_0_750_to_1_000": (0.0010, 0.0022),
                },
            },
            "stainless_300": {
                "sfm_min": 30,
                "sfm_max": 75,
                "ipt_ranges": {
                    "lte_0_0625": (0.0003, 0.0008),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0012),
                    "gt_0_250_to_0_375": (0.0005, 0.0014),
                    "gt_0_375_to_0_500": (0.0006, 0.0016),
                    "gt_0_500_to_0_750": (0.0009, 0.0018),
                    "gt_0_750_to_1_000": (0.0010, 0.0020),
                },
            },
            "stainless_400_free_machining": {
                "sfm_min": 50,
                "sfm_max": 100,
                "ipt_ranges": {
                    "lte_0_0625": (0.0002, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0012),
                    "gt_0_250_to_0_375": (0.0005, 0.0014),
                    "gt_0_375_to_0_500": (0.0006, 0.0016),
                    "gt_0_500_to_0_750": (0.0009, 0.0018),
                    "gt_0_750_to_1_000": (0.0010, 0.0022),
                },
            },
            "stainless_400": {
                "sfm_min": 30,
                "sfm_max": 75,
                "ipt_ranges": {
                    "lte_0_0625": (0.0003, 0.0008),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0012),
                    "gt_0_250_to_0_375": (0.0005, 0.0014),
                    "gt_0_375_to_0_500": (0.0006, 0.0016),
                    "gt_0_500_to_0_750": (0.0009, 0.0018),
                    "gt_0_750_to_1_000": (0.0010, 0.0020),
                },
            },
            "titanium": {
                "sfm_min": 30,
                "sfm_max": 65,
                "ipt_ranges": {
                    "lte_0_0625": (0.0002, 0.0007),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0010),
                    "gt_0_250_to_0_375": (0.0005, 0.0011),
                    "gt_0_375_to_0_500": (0.0006, 0.0012),
                    "gt_0_500_to_0_750": (0.0007, 0.0012),
                    "gt_0_750_to_1_000": (0.0007, 0.0016),
                },
            },
            "cast_iron_gray": {
                "sfm_min": 60,
                "sfm_max": 180,
                "ipt_ranges": {
                    "lte_0_0625": (0.0002, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0010),
                    "gt_0_125_to_0_250": (0.0004, 0.0012),
                    "gt_0_250_to_0_375": (0.0005, 0.0014),
                    "gt_0_375_to_0_500": (0.0007, 0.0016),
                    "gt_0_500_to_0_750": (0.0009, 0.0018),
                    "gt_0_750_to_1_000": (0.0010, 0.0025),
                },
            },
            "cast_iron_ductile": {
                "sfm_min": 50,
                "sfm_max": 120,
                "ipt_ranges": {
                    "lte_0_0625": (0.0003, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0011),
                    "gt_0_250_to_0_375": (0.0005, 0.0012),
                    "gt_0_375_to_0_500": (0.0006, 0.0013),
                    "gt_0_500_to_0_750": (0.0009, 0.0015),
                    "gt_0_750_to_1_000": (0.0010, 0.0030),
                },
            },
            "aluminum": {
                "sfm_min": 70,
                "sfm_max": 300,
                "ipt_ranges": {
                    "lte_0_0625": (0.0003, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0011),
                    "gt_0_125_to_0_250": (0.0004, 0.0013),
                    "gt_0_250_to_0_375": (0.0005, 0.0015),
                    "gt_0_375_to_0_500": (0.0006, 0.0017),
                    "gt_0_500_to_0_750": (0.0009, 0.0020),
                    "gt_0_750_to_1_000": (0.0010, 0.0035),
                },
            },
            "copper_alloys": {
                "sfm_min": 70,
                "sfm_max": 300,
                "ipt_ranges": {
                    "lte_0_0625": (0.0003, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0011),
                    "gt_0_125_to_0_250": (0.0004, 0.0013),
                    "gt_0_250_to_0_375": (0.0005, 0.0015),
                    "gt_0_375_to_0_500": (0.0006, 0.0017),
                    "gt_0_500_to_0_750": (0.0009, 0.0020),
                    "gt_0_750_to_1_000": (0.0010, 0.0035),
                },
            },
            "brass_bronze": {
                "sfm_min": 70,
                "sfm_max": 300,
                "ipt_ranges": {
                    "lte_0_0625": (0.0003, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0011),
                    "gt_0_125_to_0_250": (0.0004, 0.0013),
                    "gt_0_250_to_0_375": (0.0005, 0.0015),
                    "gt_0_375_to_0_500": (0.0006, 0.0017),
                    "gt_0_500_to_0_750": (0.0009, 0.0020),
                    "gt_0_750_to_1_000": (0.0010, 0.0035),
                },
            },
            "high_strength_tool_steels": {
                "sfm_min": 30,
                "sfm_max": 65,
                "ipt_ranges": {
                    "lte_0_0625": (0.0002, 0.0009),
                    "gt_0_0625_to_0_125": (0.0003, 0.0009),
                    "gt_0_125_to_0_250": (0.0004, 0.0012),
                    "gt_0_250_to_0_375": (0.0005, 0.0014),
                    "gt_0_375_to_0_500": (0.0007, 0.0016),
                    "gt_0_500_to_0_750": (0.0009, 0.0018),
                    "gt_0_750_to_1_000": (0.0010, 0.0025),
                },
            },
        },
    },
}


def resolve_woodruff_material_family(material_name: str, source_type: str) -> dict:
    normalized_name = material_name.strip().lower()
    source_reference = WOODRUFF_REFERENCE_DATA[source_type]

    exact_material_map = {
        WOODRUFF_CARBIDE_SOURCE_TYPE: {
            "10 series steel": "low_medium_carbon_steel",
            "40 series steel": "low_medium_carbon_alloy_steel",
            "17-4 / 300 series": "stainless_300",
            "17-4/300 series": "stainless_300",
            "duplex / alloy 20": "stainless_300",
            "duplex/alloy 20": "stainless_300",
            "hastelloy": "nickel_iron_base_alloy",
            "titanium": "titanium",
            "monel": "nickel_iron_base_alloy",
            "zirconium": "titanium",
        },
        WOODRUFF_HSS_SOURCE_TYPE: {
            "10 series steel": "carbon_steels",
            "40 series steel": "medium_alloy_steels",
            "17-4 / 300 series": "stainless_300",
            "17-4/300 series": "stainless_300",
            "duplex / alloy 20": "stainless_300",
            "duplex/alloy 20": "stainless_300",
            "hastelloy": "titanium",
            "titanium": "titanium",
            "monel": "titanium",
            "zirconium": "titanium",
        },
    }

    exact_family = exact_material_map[source_type].get(normalized_name)
    if exact_family is not None:
        return {
            "material_family": exact_family,
            "match_type": "direct",
            "match_note": None,
        }

    for match_text, material_family in source_reference["material_family_map"].items():
        if match_text in normalized_name:
            return {
                "material_family": material_family,
                "match_type": "direct",
                "match_note": None,
            }

    for match_text, material_family in source_reference["closest_family_map"].items():
        if match_text in normalized_name:
            return {
                "material_family": material_family,
                "match_type": "closest",
                "match_note": "Closest available Woodruff reference family used for this current material label.",
            }

    return {
        "material_family": None,
        "match_type": "unmapped",
        "match_note": "No local Woodruff reference family match was found for this material.",
    }


def get_woodruff_tooth_lookup(cutter_diameter: float) -> dict:
    supported_diameters = sorted(WOODRUFF_TOOTH_COUNT_BY_DIAMETER.keys())
    matched_diameter = min(supported_diameters, key=lambda supported: (abs(supported - cutter_diameter), supported))

    return {
        "matched_diameter": matched_diameter,
        "tooth_count": WOODRUFF_TOOTH_COUNT_BY_DIAMETER[matched_diameter],
        "exact_match": abs(matched_diameter - cutter_diameter) < 1e-9,
    }


def get_hss_diameter_band(cutter_diameter: float) -> dict:
    for band in WOODRUFF_HSS_DIAMETER_BANDS:
        min_exclusive = band["min_exclusive"]
        max_inclusive = band["max_inclusive"]
        if min_exclusive is None and cutter_diameter <= max_inclusive:
            return band
        if min_exclusive is not None and min_exclusive < cutter_diameter <= max_inclusive:
            return band

    return WOODRUFF_HSS_DIAMETER_BANDS[-1]


def build_woodruff_reference(material_name: str, cutter_diameter: float, source_type: str) -> dict:
    material_match = resolve_woodruff_material_family(material_name, source_type)
    tooth_lookup = get_woodruff_tooth_lookup(cutter_diameter)

    reference = {
        "reference_label": WOODRUFF_REFERENCE_LABEL,
        "source_type": source_type,
        "material_family": material_match["material_family"],
        "material_match_type": material_match["match_type"],
        "material_match_note": material_match["match_note"],
        "cutter_diameter": cutter_diameter,
        "matched_diameter": tooth_lookup["matched_diameter"],
        "tooth_count": tooth_lookup["tooth_count"],
        "exact_diameter_match": tooth_lookup["exact_match"],
        "default_ipt": 0.0,
        "ipt_min": None,
        "ipt_max": None,
        "diameter_band_label": None,
    }

    material_family = material_match["material_family"]
    if material_family is None:
        reference.update(
            {
                "sfm_min": None,
                "sfm_max": None,
                "default_sfm": None,
            }
        )
        return reference

    family_reference = WOODRUFF_REFERENCE_DATA[source_type]["families"][material_family]
    default_sfm = (family_reference["sfm_min"] + family_reference["sfm_max"]) / 2

    reference.update(
        {
            "sfm_min": family_reference["sfm_min"],
            "sfm_max": family_reference["sfm_max"],
            "default_sfm": default_sfm,
        }
    )

    if source_type == WOODRUFF_CARBIDE_SOURCE_TYPE:
        reference["default_ipt"] = family_reference["default_ipt"]
        return reference

    diameter_band = get_hss_diameter_band(cutter_diameter)
    ipt_min, ipt_max = family_reference["ipt_ranges"][diameter_band["key"]]
    default_ipt = (ipt_min + ipt_max) / 2

    reference.update(
        {
            "default_ipt": default_ipt,
            "ipt_min": ipt_min,
            "ipt_max": ipt_max,
            "diameter_band_label": diameter_band["label"],
        }
    )
    return reference
