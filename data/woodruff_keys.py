WOODRUFF_KEY_SOURCE = "ANSI B17.2-1967 (R1998) Table 10 - ANSI Keyseat Dimensions for Woodruff Keys"
WOODRUFF_KEY_MAPPING_SOURCE = 'FastenerMart "Woodruff Key Dimensions" PDF'

WOODRUFF_TOLERANCES = {
    "shaft_depth": "+0.005 / -0.000",
    "key_above_shaft": "+0.005 / -0.005",
    "hub_width": "+0.002 / -0.000",
    "hub_depth": "+0.005 / -0.000",
}

_WOODRUFF_KEYS_RAW = [
    {"key_number": "202", "nominal_size": "1/16 x 1/4", "keyseat_width_min": 0.0615, "keyseat_width_max": 0.0630, "shaft_depth": 0.0728, "cutter_diameter_min": 0.2500, "cutter_diameter_max": 0.2680, "key_above_shaft": 0.0312, "hub_width": 0.0635, "hub_depth": 0.0372},
    {"key_number": "202.5", "nominal_size": "1/16 x 5/16", "keyseat_width_min": 0.0615, "keyseat_width_max": 0.0630, "shaft_depth": 0.1038, "cutter_diameter_min": 0.3120, "cutter_diameter_max": 0.3300, "key_above_shaft": 0.0312, "hub_width": 0.0635, "hub_depth": 0.0372},
    {"key_number": "302.5", "nominal_size": "3/32 x 5/16", "keyseat_width_min": 0.0928, "keyseat_width_max": 0.0943, "shaft_depth": 0.0882, "cutter_diameter_min": 0.3120, "cutter_diameter_max": 0.3300, "key_above_shaft": 0.0469, "hub_width": 0.0948, "hub_depth": 0.0529},
    {"key_number": "203", "nominal_size": "1/16 x 3/8", "keyseat_width_min": 0.0615, "keyseat_width_max": 0.0630, "shaft_depth": 0.1358, "cutter_diameter_min": 0.3750, "cutter_diameter_max": 0.3930, "key_above_shaft": 0.0312, "hub_width": 0.0635, "hub_depth": 0.0372},
    {"key_number": "303", "nominal_size": "3/32 x 3/8", "keyseat_width_min": 0.0928, "keyseat_width_max": 0.0943, "shaft_depth": 0.1202, "cutter_diameter_min": 0.3750, "cutter_diameter_max": 0.3930, "key_above_shaft": 0.0469, "hub_width": 0.0948, "hub_depth": 0.0529},
    {"key_number": "403", "nominal_size": "1/8 x 3/8", "keyseat_width_min": 0.1240, "keyseat_width_max": 0.1255, "shaft_depth": 0.1045, "cutter_diameter_min": 0.3750, "cutter_diameter_max": 0.3930, "key_above_shaft": 0.0625, "hub_width": 0.1260, "hub_depth": 0.0685},
    {"key_number": "204", "nominal_size": "1/16 x 1/2", "keyseat_width_min": 0.0615, "keyseat_width_max": 0.0630, "shaft_depth": 0.1668, "cutter_diameter_min": 0.5000, "cutter_diameter_max": 0.5180, "key_above_shaft": 0.0312, "hub_width": 0.0635, "hub_depth": 0.0372},
    {"key_number": "304", "nominal_size": "3/32 x 1/2", "keyseat_width_min": 0.0928, "keyseat_width_max": 0.0943, "shaft_depth": 0.1511, "cutter_diameter_min": 0.5000, "cutter_diameter_max": 0.5180, "key_above_shaft": 0.0469, "hub_width": 0.0948, "hub_depth": 0.0529},
    {"key_number": "404", "nominal_size": "1/8 x 1/2", "keyseat_width_min": 0.1240, "keyseat_width_max": 0.1255, "shaft_depth": 0.1355, "cutter_diameter_min": 0.5000, "cutter_diameter_max": 0.5180, "key_above_shaft": 0.0625, "hub_width": 0.1260, "hub_depth": 0.0685},
    {"key_number": "305", "nominal_size": "3/32 x 5/8", "keyseat_width_min": 0.0928, "keyseat_width_max": 0.0943, "shaft_depth": 0.1981, "cutter_diameter_min": 0.6250, "cutter_diameter_max": 0.6430, "key_above_shaft": 0.0469, "hub_width": 0.0948, "hub_depth": 0.0529},
    {"key_number": "405", "nominal_size": "1/8 x 5/8", "keyseat_width_min": 0.1240, "keyseat_width_max": 0.1255, "shaft_depth": 0.1825, "cutter_diameter_min": 0.6250, "cutter_diameter_max": 0.6430, "key_above_shaft": 0.0625, "hub_width": 0.1260, "hub_depth": 0.0685},
    {"key_number": "505", "nominal_size": "5/32 x 5/8", "keyseat_width_min": 0.1553, "keyseat_width_max": 0.1568, "shaft_depth": 0.1669, "cutter_diameter_min": 0.6250, "cutter_diameter_max": 0.6430, "key_above_shaft": 0.0781, "hub_width": 0.1573, "hub_depth": 0.0841},
    {"key_number": "605", "nominal_size": "3/16 x 5/8", "keyseat_width_min": 0.1863, "keyseat_width_max": 0.1880, "shaft_depth": 0.1513, "cutter_diameter_min": 0.6250, "cutter_diameter_max": 0.6430, "key_above_shaft": 0.0937, "hub_width": 0.1885, "hub_depth": 0.0997},
    {"key_number": "406", "nominal_size": "1/8 x 3/4", "keyseat_width_min": 0.1240, "keyseat_width_max": 0.1255, "shaft_depth": 0.2455, "cutter_diameter_min": 0.7500, "cutter_diameter_max": 0.7680, "key_above_shaft": 0.0625, "hub_width": 0.1260, "hub_depth": 0.0685},
    {"key_number": "506", "nominal_size": "5/32 x 3/4", "keyseat_width_min": 0.1553, "keyseat_width_max": 0.1568, "shaft_depth": 0.2299, "cutter_diameter_min": 0.7500, "cutter_diameter_max": 0.7680, "key_above_shaft": 0.0781, "hub_width": 0.1573, "hub_depth": 0.0841},
    {"key_number": "606", "nominal_size": "3/16 x 3/4", "keyseat_width_min": 0.1863, "keyseat_width_max": 0.1880, "shaft_depth": 0.2143, "cutter_diameter_min": 0.7500, "cutter_diameter_max": 0.7680, "key_above_shaft": 0.0937, "hub_width": 0.1885, "hub_depth": 0.0997},
    {"key_number": "806", "nominal_size": "1/4 x 3/4", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.1830, "cutter_diameter_min": 0.7500, "cutter_diameter_max": 0.7680, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "507", "nominal_size": "5/32 x 7/8", "keyseat_width_min": 0.1553, "keyseat_width_max": 0.1568, "shaft_depth": 0.2919, "cutter_diameter_min": 0.8750, "cutter_diameter_max": 0.8950, "key_above_shaft": 0.0781, "hub_width": 0.1573, "hub_depth": 0.0841},
    {"key_number": "607", "nominal_size": "3/16 x 7/8", "keyseat_width_min": 0.1863, "keyseat_width_max": 0.1880, "shaft_depth": 0.2763, "cutter_diameter_min": 0.8750, "cutter_diameter_max": 0.8950, "key_above_shaft": 0.0937, "hub_width": 0.1885, "hub_depth": 0.0997},
    {"key_number": "707", "nominal_size": "7/32 x 7/8", "keyseat_width_min": 0.2175, "keyseat_width_max": 0.2193, "shaft_depth": 0.2607, "cutter_diameter_min": 0.8750, "cutter_diameter_max": 0.8950, "key_above_shaft": 0.1093, "hub_width": 0.2198, "hub_depth": 0.1153},
    {"key_number": "807", "nominal_size": "1/4 x 7/8", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.2450, "cutter_diameter_min": 0.8750, "cutter_diameter_max": 0.8950, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "608", "nominal_size": "3/16 x 1", "keyseat_width_min": 0.1863, "keyseat_width_max": 0.1880, "shaft_depth": 0.3393, "cutter_diameter_min": 1.0000, "cutter_diameter_max": 1.0200, "key_above_shaft": 0.0937, "hub_width": 0.1885, "hub_depth": 0.0997},
    {"key_number": "708", "nominal_size": "7/32 x 1", "keyseat_width_min": 0.2175, "keyseat_width_max": 0.2193, "shaft_depth": 0.3237, "cutter_diameter_min": 1.0000, "cutter_diameter_max": 1.0200, "key_above_shaft": 0.1093, "hub_width": 0.2198, "hub_depth": 0.1153},
    {"key_number": "808", "nominal_size": "1/4 x 1", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.3080, "cutter_diameter_min": 1.0000, "cutter_diameter_max": 1.0200, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "1008", "nominal_size": "5/16 x 1", "keyseat_width_min": 0.3111, "keyseat_width_max": 0.3130, "shaft_depth": 0.2768, "cutter_diameter_min": 1.0000, "cutter_diameter_max": 1.0200, "key_above_shaft": 0.1562, "hub_width": 0.3135, "hub_depth": 0.1622},
    {"key_number": "1208", "nominal_size": "3/8 x 1", "keyseat_width_min": 0.3735, "keyseat_width_max": 0.3755, "shaft_depth": 0.2455, "cutter_diameter_min": 1.0000, "cutter_diameter_max": 1.0200, "key_above_shaft": 0.1875, "hub_width": 0.3760, "hub_depth": 0.1935},
    {"key_number": "609", "nominal_size": "3/16 x 1-1/8", "keyseat_width_min": 0.1863, "keyseat_width_max": 0.1880, "shaft_depth": 0.3853, "cutter_diameter_min": 1.1250, "cutter_diameter_max": 1.1450, "key_above_shaft": 0.0937, "hub_width": 0.1885, "hub_depth": 0.0997},
    {"key_number": "709", "nominal_size": "7/32 x 1-1/8", "keyseat_width_min": 0.2175, "keyseat_width_max": 0.2193, "shaft_depth": 0.3697, "cutter_diameter_min": 1.1250, "cutter_diameter_max": 1.1450, "key_above_shaft": 0.1093, "hub_width": 0.2198, "hub_depth": 0.1153},
    {"key_number": "809", "nominal_size": "1/4 x 1-1/8", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.3540, "cutter_diameter_min": 1.1250, "cutter_diameter_max": 1.1450, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "1009", "nominal_size": "5/16 x 1-1/8", "keyseat_width_min": 0.3111, "keyseat_width_max": 0.3130, "shaft_depth": 0.3228, "cutter_diameter_min": 1.1250, "cutter_diameter_max": 1.1450, "key_above_shaft": 0.1562, "hub_width": 0.3135, "hub_depth": 0.1622},
    {"key_number": "610", "nominal_size": "3/16 x 1-1/4", "keyseat_width_min": 0.1863, "keyseat_width_max": 0.1880, "shaft_depth": 0.4483, "cutter_diameter_min": 1.2500, "cutter_diameter_max": 1.2730, "key_above_shaft": 0.0937, "hub_width": 0.1885, "hub_depth": 0.0997},
    {"key_number": "710", "nominal_size": "7/32 x 1-1/4", "keyseat_width_min": 0.2175, "keyseat_width_max": 0.2193, "shaft_depth": 0.4327, "cutter_diameter_min": 1.2500, "cutter_diameter_max": 1.2730, "key_above_shaft": 0.1093, "hub_width": 0.2198, "hub_depth": 0.1153},
    {"key_number": "810", "nominal_size": "1/4 x 1-1/4", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.4170, "cutter_diameter_min": 1.2500, "cutter_diameter_max": 1.2730, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "1010", "nominal_size": "5/16 x 1-1/4", "keyseat_width_min": 0.3111, "keyseat_width_max": 0.3130, "shaft_depth": 0.3858, "cutter_diameter_min": 1.2500, "cutter_diameter_max": 1.2730, "key_above_shaft": 0.1562, "hub_width": 0.3135, "hub_depth": 0.1622},
    {"key_number": "1210", "nominal_size": "3/8 x 1-1/4", "keyseat_width_min": 0.3735, "keyseat_width_max": 0.3755, "shaft_depth": 0.3545, "cutter_diameter_min": 1.2500, "cutter_diameter_max": 1.2730, "key_above_shaft": 0.1875, "hub_width": 0.3760, "hub_depth": 0.1935},
    {"key_number": "811", "nominal_size": "1/4 x 1-3/8", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.4640, "cutter_diameter_min": 1.3750, "cutter_diameter_max": 1.3980, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "1011", "nominal_size": "5/16 x 1-3/8", "keyseat_width_min": 0.3111, "keyseat_width_max": 0.3130, "shaft_depth": 0.4328, "cutter_diameter_min": 1.3750, "cutter_diameter_max": 1.3980, "key_above_shaft": 0.1562, "hub_width": 0.3135, "hub_depth": 0.1622},
    {"key_number": "1211", "nominal_size": "3/8 x 1-3/8", "keyseat_width_min": 0.3735, "keyseat_width_max": 0.3755, "shaft_depth": 0.4015, "cutter_diameter_min": 1.3750, "cutter_diameter_max": 1.3980, "key_above_shaft": 0.1875, "hub_width": 0.3760, "hub_depth": 0.1935},
    {"key_number": "812", "nominal_size": "1/4 x 1-1/2", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.5110, "cutter_diameter_min": 1.5000, "cutter_diameter_max": 1.5230, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "1012", "nominal_size": "5/16 x 1-1/2", "keyseat_width_min": 0.3111, "keyseat_width_max": 0.3130, "shaft_depth": 0.4798, "cutter_diameter_min": 1.5000, "cutter_diameter_max": 1.5230, "key_above_shaft": 0.1562, "hub_width": 0.3135, "hub_depth": 0.1622},
    {"key_number": "1212", "nominal_size": "3/8 x 1-1/2", "keyseat_width_min": 0.3735, "keyseat_width_max": 0.3755, "shaft_depth": 0.4485, "cutter_diameter_min": 1.5000, "cutter_diameter_max": 1.5230, "key_above_shaft": 0.1875, "hub_width": 0.3760, "hub_depth": 0.1935},
    {"key_number": "617-1", "nominal_size": "3/16 x 2-1/8", "keyseat_width_min": 0.1863, "keyseat_width_max": 0.1880, "shaft_depth": 0.3073, "cutter_diameter_min": 2.1250, "cutter_diameter_max": 2.1600, "key_above_shaft": 0.0937, "hub_width": 0.1885, "hub_depth": 0.0997},
    {"key_number": "817-1", "nominal_size": "1/4 x 2-1/8", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.2760, "cutter_diameter_min": 2.1250, "cutter_diameter_max": 2.1600, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "1017-1", "nominal_size": "5/16 x 2-1/8", "keyseat_width_min": 0.3111, "keyseat_width_max": 0.3130, "shaft_depth": 0.2448, "cutter_diameter_min": 2.1250, "cutter_diameter_max": 2.1600, "key_above_shaft": 0.1562, "hub_width": 0.3135, "hub_depth": 0.1622},
    {"key_number": "1217-1", "nominal_size": "3/8 x 2-1/8", "keyseat_width_min": 0.3735, "keyseat_width_max": 0.3755, "shaft_depth": 0.2135, "cutter_diameter_min": 2.1250, "cutter_diameter_max": 2.1600, "key_above_shaft": 0.1875, "hub_width": 0.3760, "hub_depth": 0.1935},
    {"key_number": "617", "nominal_size": "3/16 x 2-1/8", "keyseat_width_min": 0.1863, "keyseat_width_max": 0.1880, "shaft_depth": 0.4323, "cutter_diameter_min": 2.1250, "cutter_diameter_max": 2.1600, "key_above_shaft": 0.0937, "hub_width": 0.1885, "hub_depth": 0.0997},
    {"key_number": "817", "nominal_size": "1/4 x 2-1/8", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.4010, "cutter_diameter_min": 2.1250, "cutter_diameter_max": 2.1600, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "1017", "nominal_size": "5/16 x 2-1/8", "keyseat_width_min": 0.3111, "keyseat_width_max": 0.3130, "shaft_depth": 0.3698, "cutter_diameter_min": 2.1250, "cutter_diameter_max": 2.1600, "key_above_shaft": 0.1562, "hub_width": 0.3135, "hub_depth": 0.1622},
    {"key_number": "1217", "nominal_size": "3/8 x 2-1/8", "keyseat_width_min": 0.3735, "keyseat_width_max": 0.3755, "shaft_depth": 0.3385, "cutter_diameter_min": 2.1250, "cutter_diameter_max": 2.1600, "key_above_shaft": 0.1875, "hub_width": 0.3760, "hub_depth": 0.1935},
    {"key_number": "822-1", "nominal_size": "1/4 x 2-3/4", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.4640, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "1022-1", "nominal_size": "5/16 x 2-3/4", "keyseat_width_min": 0.3111, "keyseat_width_max": 0.3130, "shaft_depth": 0.4328, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.1562, "hub_width": 0.3135, "hub_depth": 0.1622},
    {"key_number": "1222-1", "nominal_size": "3/8 x 2-3/4", "keyseat_width_min": 0.3735, "keyseat_width_max": 0.3755, "shaft_depth": 0.4015, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.1875, "hub_width": 0.3760, "hub_depth": 0.1935},
    {"key_number": "1422-1", "nominal_size": "7/16 x 2-3/4", "keyseat_width_min": 0.4360, "keyseat_width_max": 0.4380, "shaft_depth": 0.3703, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.2187, "hub_width": 0.4385, "hub_depth": 0.2247},
    {"key_number": "1622-1", "nominal_size": "1/2 x 2-3/4", "keyseat_width_min": 0.4985, "keyseat_width_max": 0.5005, "shaft_depth": 0.3390, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.2500, "hub_width": 0.5010, "hub_depth": 0.2560},
    {"key_number": "822", "nominal_size": "1/4 x 2-3/4", "keyseat_width_min": 0.2487, "keyseat_width_max": 0.2505, "shaft_depth": 0.6200, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.1250, "hub_width": 0.2510, "hub_depth": 0.1310},
    {"key_number": "1022", "nominal_size": "5/16 x 2-3/4", "keyseat_width_min": 0.3111, "keyseat_width_max": 0.3130, "shaft_depth": 0.5888, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.1562, "hub_width": 0.3135, "hub_depth": 0.1622},
    {"key_number": "1222", "nominal_size": "3/8 x 2-3/4", "keyseat_width_min": 0.3735, "keyseat_width_max": 0.3755, "shaft_depth": 0.5575, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.1875, "hub_width": 0.3760, "hub_depth": 0.1935},
    {"key_number": "1422", "nominal_size": "7/16 x 2-3/4", "keyseat_width_min": 0.4360, "keyseat_width_max": 0.4380, "shaft_depth": 0.5263, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.2187, "hub_width": 0.4385, "hub_depth": 0.2247},
    {"key_number": "1622", "nominal_size": "1/2 x 2-3/4", "keyseat_width_min": 0.4985, "keyseat_width_max": 0.5005, "shaft_depth": 0.4950, "cutter_diameter_min": 2.7500, "cutter_diameter_max": 2.7850, "key_above_shaft": 0.2500, "hub_width": 0.5010, "hub_depth": 0.2560},
    {"key_number": "1228", "nominal_size": "3/8 x 3-1/2", "keyseat_width_min": 0.3735, "keyseat_width_max": 0.3755, "shaft_depth": 0.7455, "cutter_diameter_min": 3.5000, "cutter_diameter_max": 3.5350, "key_above_shaft": 0.1875, "hub_width": 0.3760, "hub_depth": 0.1935},
    {"key_number": "1428", "nominal_size": "7/16 x 3-1/2", "keyseat_width_min": 0.4360, "keyseat_width_max": 0.4380, "shaft_depth": 0.7143, "cutter_diameter_min": 3.5000, "cutter_diameter_max": 3.5350, "key_above_shaft": 0.2187, "hub_width": 0.4385, "hub_depth": 0.2247},
    {"key_number": "1628", "nominal_size": "1/2 x 3-1/2", "keyseat_width_min": 0.4985, "keyseat_width_max": 0.5005, "shaft_depth": 0.6830, "cutter_diameter_min": 3.5000, "cutter_diameter_max": 3.5350, "key_above_shaft": 0.2500, "hub_width": 0.5010, "hub_depth": 0.2560},
    {"key_number": "1828", "nominal_size": "9/16 x 3-1/2", "keyseat_width_min": 0.5610, "keyseat_width_max": 0.5630, "shaft_depth": 0.6518, "cutter_diameter_min": 3.5000, "cutter_diameter_max": 3.5350, "key_above_shaft": 0.2812, "hub_width": 0.5635, "hub_depth": 0.2872},
    {"key_number": "2028", "nominal_size": "5/8 x 3-1/2", "keyseat_width_min": 0.6235, "keyseat_width_max": 0.6255, "shaft_depth": 0.6205, "cutter_diameter_min": 3.5000, "cutter_diameter_max": 3.5350, "key_above_shaft": 0.3125, "hub_width": 0.6260, "hub_depth": 0.3185},
    {"key_number": "2228", "nominal_size": "11/16 x 3-1/2", "keyseat_width_min": 0.6860, "keyseat_width_max": 0.6880, "shaft_depth": 0.5893, "cutter_diameter_min": 3.5000, "cutter_diameter_max": 3.5350, "key_above_shaft": 0.3437, "hub_width": 0.6885, "hub_depth": 0.3497},
    {"key_number": "2428", "nominal_size": "3/4 x 3-1/2", "keyseat_width_min": 0.7485, "keyseat_width_max": 0.7505, "shaft_depth": 0.5580, "cutter_diameter_min": 3.5000, "cutter_diameter_max": 3.5350, "key_above_shaft": 0.3750, "hub_width": 0.7510, "hub_depth": 0.3810},
]

WOODRUFF_KEY_NO_TO_ANSI = {
    "201": "202",
    "206": "202.5",
    "207": "302.5",
    "211": "203",
    "212": "303",
    "213": "403",
    "1": "204",
    "2": "304",
    "3": "404",
    "4": "305",
    "5": "405",
    "6": "505",
    "61": "605",
    "7": "406",
    "8": "506",
    "9": "606",
    "91": "806",
    "10": "507",
    "11": "607",
    "12": "707",
    "A": "807",
    "13": "608",
    "14": "708",
    "15": "808",
    "B": "1008",
    "152": "1208",
    "16": "609",
    "17": "709",
    "18": "809",
    "C": "1009",
    "19": "610",
    "20": "710",
    "21": "810",
    "D": "1010",
    "E": "1210",
    "22": "811",
    "23": "1011",
    "F": "1211",
    "24": "812",
    "25": "1012",
    "G": "1212",
    "126": "617-1",
    "127": "817-1",
    "128": "1017-1",
    "129": "1217-1",
    "26": "617",
    "27": "817",
    "28": "1017",
    "29": "1217",
    "RX": "822-1",
    "SX": "1022-1",
    "TX": "1222-1",
    "UX": "1422-1",
    "VX": "1622-1",
    "R": "822",
    "S": "1022",
    "T": "1222",
    "U": "1422",
    "V": "1622",
    "30": "1228",
    "31": "1428",
    "32": "1628",
    "33": "1828",
    "34": "2028",
    "35": "2228",
    "36": "2428",
}

_WOODRUFF_ANSI_TO_KEY_NO = {ansi_key_no: key_no for key_no, ansi_key_no in WOODRUFF_KEY_NO_TO_ANSI.items()}


def _normalize_woodruff_lookup(value: str) -> str:
    return str(value).strip().upper()


def _build_woodruff_key_row(raw_row: dict) -> dict:
    ansi_key_no = raw_row["key_number"]
    key_no = _WOODRUFF_ANSI_TO_KEY_NO.get(ansi_key_no)
    if key_no is None:
        raise KeyError(f"Missing Key No. mapping for ANSI Key No. {ansi_key_no}")

    return {
        "key_no": key_no,
        "ansi_key_no": ansi_key_no,
        "key_number": ansi_key_no,
        "nominal_size": raw_row["nominal_size"],
        "keyseat_width_min": raw_row["keyseat_width_min"],
        "keyseat_width_max": raw_row["keyseat_width_max"],
        "shaft_depth": raw_row["shaft_depth"],
        "cutter_diameter_min": raw_row["cutter_diameter_min"],
        "cutter_diameter_max": raw_row["cutter_diameter_max"],
        "key_above_shaft": raw_row["key_above_shaft"],
        "hub_width": raw_row["hub_width"],
        "hub_depth": raw_row["hub_depth"],
    }


WOODRUFF_KEYS = [_build_woodruff_key_row(row) for row in _WOODRUFF_KEYS_RAW]

WOODRUFF_KEY_NOS = [row["key_no"] for row in WOODRUFF_KEYS]
WOODRUFF_ANSI_KEY_NOS = [row["ansi_key_no"] for row in WOODRUFF_KEYS]
WOODRUFF_KEY_NUMBERS = [row["key_number"] for row in WOODRUFF_KEYS]
WOODRUFF_NOMINAL_SIZES = list(dict.fromkeys(row["nominal_size"] for row in WOODRUFF_KEYS))


def get_woodruff_key_by_key_no(key_no: str) -> dict | None:
    normalized_key_no = _normalize_woodruff_lookup(key_no)
    for row in WOODRUFF_KEYS:
        if _normalize_woodruff_lookup(row["key_no"]) == normalized_key_no:
            return row
    return None


def get_woodruff_key_by_ansi_key_no(ansi_key_no: str) -> dict | None:
    normalized_ansi_key_no = _normalize_woodruff_lookup(ansi_key_no)
    for row in WOODRUFF_KEYS:
        if _normalize_woodruff_lookup(row["ansi_key_no"]) == normalized_ansi_key_no:
            return row
    return None


def get_woodruff_key_by_number(key_number: str) -> dict | None:
    return get_woodruff_key_by_ansi_key_no(key_number)


def get_woodruff_keys_by_nominal_size(nominal_size: str) -> list[dict]:
    return [row for row in WOODRUFF_KEYS if row["nominal_size"] == nominal_size]
