TOOLS_417_426 = [
    "1. Rough",
    "2. Finish",
    "3. Backwards rough",
    "4. Backwards finish",
    "5. Groove",
    "6. Thread",
]

TOOLS_423_424 = [
    "1. Rough (.12 - .20 per pass)",
    "2. Center",
    "3. Finish",
    "4. Drill",
    "5. RH thread",
    "6. Drill for tap",
    "7. LH thread",
    "8. Bore",
    "9. Groove (triangle)",
    "10. Tap",
    "11. Groove",
    "12. Spare",
]

TOOLS_421 = [
    "1. RH rough (.12 - .20 per pass)",
    "2. Open",
    "3. Finish",
    "4. Open",
    "5. RH thread",
    "6. Open",
    "7. LH thread",
    "8. LH finish",
    "9. Groove (triangle)",
    "10. Open",
    "11. LH groove",
    "12. Spare",
]

TOOLS_430_431 = [
    "1. OD",
    "2. Rough face and OD (WNMG 80 deg insert) 432",
    "3. Finish face and OD (WNMG 80 deg insert) 331",
    "4. ID",
    "5. OD groove",
    "6. ID rough bore",
    "7. OD",
    "8. ID finish bore or drill - watch clearance",
    "9. OD",
    "10. ID or drill - watch clearance",
    "11. OD",
    "12. ID finish bore or tap",
]

TOOLS_432_437 = [
    "1. OD thread RH",
    "2. Rough (.15 - .25 per pass)",
    "3. Finish",
    "4. Backward rough",
    "5. Backward finish",
    "6. Center",
    "7. Drill",
    "8. Boring bar, TCMT 2 1.5 1-UF",
    "9. Live tooling for face drill and face tap",
    "10. End mill",
    "11. End mill",
    "12. OD groove / RH thread",
]

TOOLS_433_434 = [
    "1. Rough (about .20 per pass)",
    "2. Center",
    "3. Finish",
    "4. Bore (use CDHH120605 HP520B for center chamfers)",
    "5. RH thread",
    "6. Drill for tap",
    "7. LH thread",
    "8. Finish bore",
    "9. Groove (triangle)",
    "10. Tap",
    "11. Groove",
    "12. Spare",
]

TOOLS_435 = [
    "1. Rough (.18 per pass)",
    "2. Center",
    "3. Finish",
    "4. Bore (use CDHH120605 HP520B for center chamfers)",
    "5. RH thread",
    "6. Drill for tap",
    "7. LH thread",
    "8. Finish bore",
    "9. Groove (triangle)",
    "10. Tap",
    "11. Groove",
    "12. Radial live tooling",
]

TOOLS_436 = [
    "1. Rough DNMG 442-PR",
    "2. Finish DNMG 432FW",
    "3. Reversed DNMG 442-PR",
    "4. Spot drill",
    "5. Reversed DNMG 432FW",
    "6. Boring bar",
    "7. Empty",
    "8. Live woodruff cutter",
    "9. Groove",
    "10. Live 9/32 end mill",
    "11. Tool",
    "12. Live 3/8 end mill",
]

QTS_300_STEADY_REST_MISC = [
    "Steady-rest misc values:",
    "1 = insert comment telling operator to move the rest manually.",
    "2 = open steady rest.",
    "3 = close steady rest.",
    "Any other value = call the rest-move macro.",
    "Close-rest-after-move values:",
    "0 = do not output M87 after the move.",
    "1 = output M87 after the move.",
]

QTS_300_STEADY_REST_CODES = [
    "Steady-rest move sequence:",
    "M05",
    "M09",
    "M98 P'A'00'B' (A = current position, B = next position)",
    "M87",
    "G98 G4 X1.0",
    "M00 or M01",
]

QTS_350_STEADY_REST_MISC = [
    "Steady-rest misc values:",
    "1 = insert comment telling operator to move the rest manually.",
    "2 = open steady rest.",
    "3 = close steady rest.",
    "Any other value = call the rest-move macro, for example 10020000.",
    "Close-rest-after-move values:",
    "0 = do not output M87 after the move.",
    "1 = output M87 after the move.",
    "Always follow a rest move with G98 G4 X1.0.",
]

HAAS_FLIP_SEQUENCE_30 = [
    "Flip sequence:",
    "G91 G28 Z0",
    "G90 G53 X-30. Y0.",
    "M00 (turn part and continue)",
]

MACHINES = {
    "417 Cincinnati Lathe": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 417 / 426 Cincinnati shaft-lathe note set.",
            "Used for shaft work, face-driver work, grooves, and longhand threading.",
        ],
        "program_behavior": [
            "1200 RPM max in high gear.",
            "300 RPM max in low gear.",
            "Use misc values to force high gear with M42.",
            "Finish the body in second operation.",
        ],
        "post_limits": [
            "Post supports subprograms.",
            "Thread pitch address uses F, not E.",
            "Post changed G32 to G33.",
            "Cantext 5 = return tailstock and 6 = advance tailstock.",
        ],
        "code_rules": [
            "Thread format is longhand.",
            "Use equal thread depths.",
            "Use 8 - 15 cuts.",
            "Use 1 spring cut.",
            "Use 0 flank infeed.",
        ],
        "shop_notes": [
            "Most-used groove tool is TLG-3078L relieved.",
            "No holders for triangle inserts.",
            "Facing is done with the finish tool and a shortened endpoint so it stops before center, about .5 per side.",
            "Siemens shafts: do the pulley end first.",
            "Siemens shafts: offset the pulley-end face +.030 in Mastercam before aligning the model to Z.",
        ],
        "workholding": [
            "Steady-rest max diameter is 8.0 in.",
            "Face-driver starter cut: feed .010 for the first .1 in to seat the shaft in the drive blades.",
            "On first-side face-driver roughing, rough .100 past the end of the part.",
        ],
        "tooling": TOOLS_417_426,
        "turning_notes": [
            "Groove target: create an L-shaped line .500 from the shoulder closest to the groove.",
            "Make both line legs .500.",
            "Run a finish toolpath and use those lines as the geometry.",
            "Set feed to 25 IPM.",
            "Spindle off.",
            "Coolant off.",
            "No lead in or lead out.",
            "No tool comp.",
            "Change at point on the horizontal line in chain and add it after / M00.",
        ],
        "posting_cimco": [
            "Verify gear range and RPM cap before release.",
            "Verify groove path settings, especially 25 IPM, spindle off, coolant off, and no tool comp.",
            "Verify longhand thread output and cut count.",
        ],
        "mastercam_rules": [
            "Leave the +.030 pulley-end face stock on Siemens work.",
            "Manually edit face-driver starter-cut feed where needed.",
        ],
        "special_notes": [
            "417 and 426 currently share the same shop-rule set.",
        ],
    },
    "421 Mazak QTS-300": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 421 / 423 / 424 Mazak QTS-300 family rule set.",
            "421 is the face-driven machine in this group.",
        ],
        "program_behavior": [
            "Program start must include #101, #102, and #103.",
            "When roughing for second-op steady-rest prep, 421 can rough to the end of the part.",
        ],
        "post_limits": [
            "Post supports subprograms.",
            "General tailstock codes exist in the post, but 421 restrictions still apply.",
            "Thread pitch address uses F, not E.",
        ],
        "code_rules": [
            "DO NOT do any end work.",
            "DO NOT output any tailstock moves.",
            "If steady-rest code is used, follow the move with G98 G4 X1.0.",
        ],
        "shop_notes": [
            "421 only: this machine is face driven.",
            "Finish the face only to -.3 to -.6 diameter.",
        ],
        "workholding": [
            "Face-driver starter cut: feed .010 for the first .1 on roughing to seat the shaft in the drive blades.",
            "On the rough OD path, edit the early points so the first feed is .010, the added point is .010, and the next point is .015.",
        ],
        "tooling": TOOLS_421,
        "posting_cimco": [
            "Verify #101, #102, and #103 are present.",
            "Verify there is no end-work output.",
            "Verify there are no tailstock moves.",
        ],
        "special_notes": [
            "421 is not interchangeable with 423 / 424 from a programming standpoint.",
        ],
    },
    "423 Mazak QTS-300": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 421 / 423 / 424 Mazak QTS-300 family rule set.",
            "423 is the 3-jaw chuck machine in this group.",
        ],
        "program_behavior": [
            "Program start must include #101, #102, and #103.",
            "When roughing for second-op steady-rest prep, rough back 2 in from the chuck.",
        ],
        "post_limits": [
            "Post supports subprograms.",
            "Thread pitch address uses F, not E.",
        ],
        "code_rules": QTS_300_STEADY_REST_MISC + QTS_300_STEADY_REST_CODES,
        "shop_notes": [
            "Use the steady rest on second operation whenever possible for TIR.",
        ],
        "workholding": [
            "423 only: 3-jaw chuck.",
            "Steady rest cannot get within 13.75 in of the tailstock.",
            "If the rest band is within 3 in of the end, move the tailstock away before moving the rest to the end of the part.",
            "Minimum distance from the chuck face to the tailstock with a standard center is about 16 in.",
            "With the long tailstock, minimum distance is about 12 in.",
            "423 steady-rest table: rest width 1.0 in, min width 1.5 in, min steady-rest to chuck 3.75 in, min steady-rest to tailstock 9.0 in, typical face band length 3.0 in, typical band distance to chuck 1.5 in.",
        ],
        "tooling": TOOLS_423_424,
        "posting_cimco": [
            "Verify #101, #102, and #103 are present.",
            "Verify steady-rest macro numbering and dwell.",
            "Verify tailstock clearance before any rest move.",
        ],
        "special_notes": [
            "423 and 424 share tooling and steady-rest logic, but the reach limits are different.",
        ],
    },
    "424 Mazak QTS-300": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 421 / 423 / 424 Mazak QTS-300 family rule set.",
            "424 is the collet machine in this group.",
        ],
        "program_behavior": [
            "Program start must include #101, #102, and #103.",
            "When roughing for second-op steady-rest prep, rough back 2 in from the collet.",
        ],
        "post_limits": [
            "Post supports subprograms.",
            "Thread pitch address uses F, not E.",
        ],
        "code_rules": QTS_300_STEADY_REST_MISC + QTS_300_STEADY_REST_CODES,
        "shop_notes": [
            "Use the steady rest on second operation whenever possible for TIR.",
        ],
        "workholding": [
            "424 only: collet chuck.",
            "Steady rest cannot get within 5.0 in of the tailstock.",
            "If the rest band is within 3 in of the end, move the tailstock away before moving the rest to the end of the part.",
            "Distance from a standard tailstock to the collet face is 10 in.",
            "With the long tailstock, distance to the collet face is 6 in.",
            "Collet stop lets the part enter the collet from .500 to about 2.500.",
            "Safe minimum part length is about 10.5 in.",
            "424 steady-rest table: rest width 1.0 in, min width 1.5 in, min steady-rest to collet 3.75 in, min steady-rest to tailstock 3.0 in, typical face band length 3.0 in, typical band distance to collet 1.5 in.",
        ],
        "tooling": TOOLS_423_424,
        "posting_cimco": [
            "Verify #101, #102, and #103 are present.",
            "Verify steady-rest macro numbering and dwell.",
            "Verify collet stop, tailstock reach, and part length before release.",
        ],
        "special_notes": [
            "424 planning is driven by collet-stop range and shorter tailstock clearance.",
        ],
    },
    "426 Cincinnati Lathe": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 417 / 426 Cincinnati shaft-lathe note set.",
            "No machine-specific differences were confirmed in the uploaded note file.",
        ],
        "program_behavior": [
            "1200 RPM max in high gear.",
            "300 RPM max in low gear.",
            "Use misc values to force high gear with M42.",
            "Finish the body in second operation.",
        ],
        "post_limits": [
            "Post supports subprograms.",
            "Thread pitch address uses F, not E.",
            "Post changed G32 to G33.",
            "Cantext 5 = return tailstock and 6 = advance tailstock.",
        ],
        "code_rules": [
            "Thread format is longhand.",
            "Use equal thread depths.",
            "Use 8 - 15 cuts.",
            "Use 1 spring cut.",
            "Use 0 flank infeed.",
        ],
        "shop_notes": [
            "Most-used groove tool is TLG-3078L relieved.",
            "No holders for triangle inserts.",
            "Facing is done with the finish tool and a shortened endpoint so it stops before center, about .5 per side.",
            "Siemens shafts: do the pulley end first.",
            "Siemens shafts: offset the pulley-end face +.030 in Mastercam before aligning the model to Z.",
        ],
        "workholding": [
            "Steady-rest max diameter is 8.0 in.",
            "Face-driver starter cut: feed .010 for the first .1 in to seat the shaft in the drive blades.",
            "On first-side face-driver roughing, rough .100 past the end of the part.",
        ],
        "tooling": TOOLS_417_426,
        "turning_notes": [
            "Groove target: create an L-shaped line .500 from the shoulder closest to the groove.",
            "Make both line legs .500.",
            "Run a finish toolpath and use those lines as the geometry.",
            "Set feed to 25 IPM.",
            "Spindle off.",
            "Coolant off.",
            "No lead in or lead out.",
            "No tool comp.",
        ],
        "posting_cimco": [
            "Verify gear range and RPM cap before release.",
            "Verify groove path settings before release.",
            "Verify longhand thread output and cut count.",
        ],
        "special_notes": [
            "417 and 426 currently use the same programmer note set.",
        ],
    },
    "430 Mazak QTS-250": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 430 / 431 Mazak QTS-250 note set.",
            "These machines do not have a steady rest.",
        ],
        "program_behavior": [
            "With tailstock: G50 max 2000 RPM.",
            "Without tailstock: G50 max 1000 RPM.",
        ],
        "post_limits": [
            "Reference math note: #102 = part OAL.",
            "Reference math note: #103 = print part length.",
        ],
        "shop_notes": [
            "No steady rest on this machine.",
        ],
        "tooling": TOOLS_430_431,
        "turning_notes": [
            "Watch clearance on ID finish bore, drill, and tap tools.",
        ],
        "posting_cimco": [
            "Verify the G50 limit matches whether the tailstock is in use.",
        ],
        "special_notes": [
            "430 and 431 share the same uploaded note set.",
        ],
    },
    "431 Mazak QTS-250": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 430 / 431 Mazak QTS-250 note set.",
            "These machines do not have a steady rest.",
        ],
        "program_behavior": [
            "With tailstock: G50 max 2000 RPM.",
            "Without tailstock: G50 max 1000 RPM.",
        ],
        "post_limits": [
            "Reference math note: #102 = part OAL.",
            "Reference math note: #103 = print part length.",
        ],
        "shop_notes": [
            "No steady rest on this machine.",
        ],
        "tooling": TOOLS_430_431,
        "turning_notes": [
            "Watch clearance on ID finish bore, drill, and tap tools.",
        ],
        "posting_cimco": [
            "Verify the G50 limit matches whether the tailstock is in use.",
        ],
        "special_notes": [
            "430 and 431 share the same uploaded note set.",
        ],
    },
    "432 Mazak QTS-450 MY": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 432 / 437 Mazak QTS-450 MY note set.",
            "Turning and live-tool machine with steady-rest, keyway, drill, and tap use.",
        ],
        "program_behavior": [
            "When roughing first side, stop 2 in from the end with gripper jaws.",
            "When roughing first side with hard jaws on a very long part, stop 4 in from the end.",
        ],
        "post_limits": [
            "Machine will not read G91 on incremental moves.",
            "Use U for X incremental moves.",
            "Use W for Z incremental moves.",
            "Use H for C incremental moves.",
            "Use V for Y incremental moves.",
        ],
        "code_rules": [
            "Every C-axis angle must include a decimal point.",
            "First C move format: M200, G0 C90.0, M210.",
            "Later C moves: M212, G0 C##.#, M210.",
            "Local subprogram format uses M98 Q#### and returns with M99.",
            "Non-local subprogram format uses M98 P## Q# and returns with M99.",
        ],
        "shop_notes": [
            "Recenter the second end every time.",
        ],
        "workholding": [
            "Steady-rest max clamp diameter is 7.5 in.",
            "Steady rest can be set flush to the tailstock.",
            "Cut the rest band 2 - 5 in from the tailstock end.",
            "If the first-op chucking diameter is larger than about 10 - 10.5 in, it can hit the right side of the steady rest in second op.",
            "If that crash risk exists, manually center the second end, turn the chucking diameter down near the steady-rest diameter, then face and recenter.",
            "Max diameter through the spindle is 4.5 in.",
            "Max chuck-jaw grip length is 3.55 in.",
        ],
        "tooling": TOOLS_432_437,
        "turning_notes": [
            "Large-diameter second-op parts are the biggest steady-rest crash risk on this machine family.",
        ],
        "live_tooling_notes": [
            "Use T10.6 or T11.6 for milling keyways.",
            "Use T9.11 for tap or face-drill work.",
            "Do off-center end work before milling keyways.",
            "If cutting a woodruff key, cut it below the part or X can overtravel when Y moves.",
        ],
        "milling_notes": [
            "Collets on hand were noted for 3/16, 6 mm, 1/4, 3/8, and 1/2.",
        ],
        "posting_cimco": [
            "Verify no G91 output is used.",
            "Verify every C move includes a decimal.",
            "Verify off-center work is sequenced before keyway milling.",
        ],
        "special_notes": [
            "Uploaded notes had changing steady-rest location values over time. Confirm actual teach positions at the machine before trusting an old program.",
        ],
    },
    "437 Mazak QTS-450 MY": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 432 / 437 Mazak QTS-450 MY note set.",
            "Turning and live-tool machine with steady-rest, keyway, drill, and tap use.",
        ],
        "program_behavior": [
            "When roughing first side, stop 2 in from the end with gripper jaws.",
            "When roughing first side with hard jaws on a very long part, stop 4 in from the end.",
        ],
        "post_limits": [
            "Machine will not read G91 on incremental moves.",
            "Use U for X incremental moves.",
            "Use W for Z incremental moves.",
            "Use H for C incremental moves.",
            "Use V for Y incremental moves.",
        ],
        "code_rules": [
            "Every C-axis angle must include a decimal point.",
            "First C move format: M200, G0 C90.0, M210.",
            "Later C moves: M212, G0 C##.#, M210.",
            "Local subprogram format uses M98 Q#### and returns with M99.",
            "Non-local subprogram format uses M98 P## Q# and returns with M99.",
        ],
        "shop_notes": [
            "Recenter the second end every time.",
        ],
        "workholding": [
            "Steady-rest max clamp diameter is 7.5 in.",
            "Steady rest can be set flush to the tailstock.",
            "Cut the rest band 2 - 5 in from the tailstock end.",
            "If the first-op chucking diameter is larger than about 10 - 10.5 in, it can hit the right side of the steady rest in second op.",
            "If that crash risk exists, manually center the second end, turn the chucking diameter down near the steady-rest diameter, then face and recenter.",
            "Max diameter through the spindle is 4.5 in.",
            "Max chuck-jaw grip length is 3.55 in.",
        ],
        "tooling": TOOLS_432_437,
        "turning_notes": [
            "Large-diameter second-op parts are the biggest steady-rest crash risk on this machine family.",
        ],
        "live_tooling_notes": [
            "Use T10.6 or T11.6 for milling keyways.",
            "Use T9.11 for tap or face-drill work.",
            "Do off-center end work before milling keyways.",
            "If cutting a woodruff key, cut it below the part or X can overtravel when Y moves.",
        ],
        "milling_notes": [
            "Collets on hand were noted for 3/16, 6 mm, 1/4, 3/8, and 1/2.",
        ],
        "posting_cimco": [
            "Verify no G91 output is used.",
            "Verify every C move includes a decimal.",
            "Verify off-center work is sequenced before keyway milling.",
        ],
        "special_notes": [
            "Uploaded notes had changing steady-rest location values over time. Confirm actual teach positions at the machine before trusting an old program.",
        ],
    },
    "433 Mazak QTS-350": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 433 / 434 Mazak QTS-350 steady-rest process.",
            "433 is the chuck version in this group.",
        ],
        "program_behavior": [
            "Standard process: cut rest band, close rest, retract tailstock, do end work, advance tailstock, rough back for the second-op rest band, then finish OD, grooves, and threads.",
            "Rest-move subprogram numbers start with the current rest location, then 00, then the next location, then 0000.",
            "Example: 20030000 moves the rest from position 2 to position 3.",
        ],
        "post_limits": [
            "Thread pitch address uses F, not E.",
        ],
        "code_rules": QTS_350_STEADY_REST_MISC,
        "shop_notes": [
            "First-side rest band is 3.0 in long and starts 5.5 in from the end of the part.",
            "After cutting the rest band, stop spindle and coolant before closing the rest if needed.",
            "Use the steady rest on second operation whenever possible for TIR.",
        ],
        "workholding": [
            "Rest width is 1.75 in.",
            "Minimum shoulder to the rest band is 1.50 in.",
            "433 only: chuck setup can rough back 2 - 3 in from the end when using a jaw stop.",
        ],
        "tooling": TOOLS_433_434,
        "drilling_notes": [
            "For drilling and tapping work, use the smaller center and the bore tool to make the chamfer.",
            "If using metric taps, verify the posted feed is still in inch units.",
        ],
        "posting_cimco": [
            "Verify steady-rest macro numbering.",
            "Verify G98 G4 X1.0 appears after every rest move.",
            "Verify tailstock, spindle, and coolant order around the rest sequence.",
        ],
        "special_notes": [
            "433 and 434 share the same process flow. The main difference is how far back you can rough for the second-op rest band.",
        ],
    },
    "434 Mazak QTS-350": {
        "machine_type": "Lathe",
        "overview": [
            "Shared 433 / 434 Mazak QTS-350 steady-rest process.",
            "434 is the collet version in this group.",
        ],
        "program_behavior": [
            "Standard process: cut rest band, close rest, retract tailstock, do end work, advance tailstock, rough back for the second-op rest band, then finish OD, grooves, and threads.",
            "Rest-move subprogram numbers start with the current rest location, then 00, then the next location, then 0000.",
            "Example: 20030000 moves the rest from position 2 to position 3.",
        ],
        "post_limits": [
            "Thread pitch address uses F, not E.",
        ],
        "code_rules": QTS_350_STEADY_REST_MISC,
        "shop_notes": [
            "First-side rest band is 3.0 in long and starts 5.5 in from the end of the part.",
            "After cutting the rest band, stop spindle and coolant before closing the rest if needed.",
            "Use the steady rest on second operation whenever possible for TIR.",
        ],
        "workholding": [
            "Rest width is 1.75 in.",
            "Minimum shoulder to the rest band is 1.50 in.",
            "434 only: collet setup can rough back 3 - 6 in from the end depending on the stop used.",
        ],
        "tooling": TOOLS_433_434,
        "drilling_notes": [
            "For drilling and tapping work, use the smaller center and the bore tool to make the chamfer.",
            "If using metric taps, verify the posted feed is still in inch units.",
        ],
        "posting_cimco": [
            "Verify steady-rest macro numbering.",
            "Verify G98 G4 X1.0 appears after every rest move.",
            "Verify tailstock, spindle, and coolant order around the rest sequence.",
        ],
        "special_notes": [
            "433 and 434 share the same process flow. The main difference is how far back you can rough for the second-op rest band.",
        ],
    },
    "435 Okuma LB3000": {
        "machine_type": "Lathe",
        "overview": [
            "Okuma LB3000 standard lathe note set.",
            "Includes standard turning tools plus radial live tooling at T12.",
        ],
        "code_rules": [
            "Do not start the program with G13.",
            "Program start must include G270, CLEAR, and DRAW.",
            "Every G74 drill cycle must include a D value for peck.",
        ],
        "tooling": TOOLS_435,
        "live_tooling_notes": [
            "If cutting a woodruff key, cut it below the part or X can overtravel when Y moves.",
        ],
        "posting_cimco": [
            "Verify G13 is removed from the start of the program.",
            "Verify G270, CLEAR, and DRAW are present at start.",
            "Verify every G74 cycle includes a D peck value.",
        ],
        "special_notes": [
            "435 is a new machine entry added from the uploaded note file.",
        ],
    },
    "436 Okuma LB4000": {
        "machine_type": "Lathe",
        "overview": [
            "Okuma LB4000 with steady-rest support and live-tool capability.",
        ],
        "program_behavior": [
            "Steady-rest width is 2.5 in.",
            "Steady-rest zero is the face of the shaft.",
            "Sub spindle max is 6000 RPM.",
        ],
        "workholding": [
            "Watch steady-rest clearance with the turret when the rest is open.",
            "Watch steady-rest clearance with the tailstock.",
        ],
        "tooling": TOOLS_436,
        "live_tooling_notes": [
            "When milling, X is in radius.",
            "Return Y to 0 before the end of the operation.",
            "If cutting a woodruff key, cut it below the part or X can overtravel when Y moves.",
        ],
        "posting_cimco": [
            "Verify steady-rest zero and clearance before release.",
            "Verify milling output uses radius X values.",
            "Verify Y returns to 0 before the operation ends.",
        ],
    },
    "652 Makino A51": {
        "machine_type": "Mill",
        "overview": [
            "Makino A51 4-axis HMC with strict machine-specific posting rules.",
        ],
        "program_behavior": [
            "Program format is O####.NC.",
            "M60 at the start and end of the program.",
        ],
        "post_limits": [
            "Do not output G95. It alarms this mill.",
            "Do not output B moves in the program.",
            "Use M26 for through-spindle coolant.",
            "H offset = tool number.",
            "D offset = tool number + 100.",
        ],
        "code_rules": [
            "If using G41 or G42, program to the tool centerline and use wear.",
            "Tapping can be feed per rev or feed per minute, but the feed mode must match the cycle.",
            "Keep the B axis at B0. Unlock with M11 and lock with M10 if needed.",
        ],
        "shop_notes": [
            "In the vise, the left end is normally the origin because there is a stop there.",
        ],
        "offset_logic": [
            "G54 = left end.",
            "G55 = body.",
            "G56 = right end.",
            "Machine mapping: G54 = B90, G55 = B180, G56 = B270.",
        ],
        "mastercam_rules": [
            "Set the part from the top view with Top as the WCS.",
            "Left end of the part sits on the right side of the screen.",
            "Body keyway sits on the top side of the screen.",
            "Create one plane for each machined face with Z aligned to the spindle.",
            "Viewed from the spindle, +Y is up and +X is right.",
            "Set left end plane offset to 0, body plane offset to 1, and right end plane offset to 2.",
        ],
        "posting_cimco": [
            "Verify no G95 output exists.",
            "Verify no B moves exist.",
            "Verify H and D offsets match the tool numbers.",
            "Verify M26 and M60 placement.",
        ],
    },
    "654 Okuma Genos M560-V": {
        "machine_type": "Mill",
        "overview": [
            "Okuma Genos M560-V for rotary chuck, V-block, flats, hexes, and rotated work.",
        ],
        "program_behavior": [
            "Program format is EM####.MIN.",
            "Max spindle speed is 12000 RPM.",
            "X zero depends on setup: right end for V-blocks, left side for the rotary chuck.",
            "Y zero is shaft centerline.",
            "Z zero is the top of the diameter.",
        ],
        "code_rules": [
            "Rotary axis is A.",
            "Use G11 for coordinate rotation and cancel it with G10 on its own line.",
            "M53 or M54 may be needed at the end of the cycle.",
            "When tapping, verify the spindle is actually turned on.",
        ],
        "workholding": [
            "Rotary chuck limits: about 2.750 max diameter through the chuck, 17 in max through length, 29 in max from chuck face.",
            "V-block limit: 28 in max part length if keyways are on both ends.",
            "Part can overhang 10 in on the left side if that end is not being cut.",
            "Part can overhang 8.5 in on the right side without hitting the chuck.",
        ],
        "mastercam_rules": [
            "For repeated flats or hexes, index A and call the subprogram again.",
            "If using G11 rotation, rotate around the part center and cancel with G10 before continuing.",
        ],
        "posting_cimco": [
            "Verify the zero location matches V-block or rotary setup.",
            "Verify G10 cancels G11 correctly.",
            "Verify tap cycles have spindle on.",
        ],
        "special_notes": [
            "Rotary chuck and V-block length limits are the main setup trap on this machine.",
        ],
    },
    "655 Haas VF6": {
        "machine_type": "Mill",
        "overview": [
            "Haas VF6 for shaft work, rotary fixture work, keyways, woodruffs, and rotated milling.",
        ],
        "program_behavior": [
            "Program format is EM####.NC.",
            "X zero is the right end face unless using the rotary fixture.",
            "Y zero is shaft centerline.",
            "Z zero is shaft centerline.",
        ],
        "code_rules": [
            "Remove G90 G53 X-30. Y0. at the end when using the rotary fixture. It can hit the door.",
            "G83 Q cannot be 0.",
            "Use G98 or G99 intentionally on drill cycles. Do not assume the wrong return mode.",
            "Add a 2-second dwell on woodruff cuts with G04 P2.0.",
        ],
        "workholding": [
            "Rotary fixture mounts on the right side of the table.",
            "Rotary fixture max length from jaw face to tailstock is 30 in.",
            "Rotary fixture through-hole fits shafts under about 3.5 - 4.0 in diameter.",
        ],
        "offset_logic": [
            "Offset 1 is on the right and counts up as you go left.",
        ],
        "milling_notes": HAAS_FLIP_SEQUENCE_30,
        "posting_cimco": [
            "Verify the end-home move clears the door when the rotary fixture is installed.",
            "Verify every G83 cycle has a real Q value.",
            "Verify G98 or G99 is correct before release.",
        ],
    },
    "656 Haas VF3": {
        "machine_type": "Mill",
        "overview": [
            "Haas VF-3/20 using the 655 numbering logic with only 20 tool pockets.",
        ],
        "program_behavior": [
            "Program format is O#####.NC.",
            "Program must start with O#####.",
            "Only one M code per line.",
            "Use the 655 tool numbers, but manage the 20-pocket limit.",
        ],
        "code_rules": [
            "Start offsets at G110.",
            "Count offsets from right front to left back.",
            "Move M8 earlier in the program because the coolant pump is slow to start.",
            "Remove M9 if it is only being used at M01 or M30. Those already shut coolant off.",
            "Change the end home position to X-.020.",
        ],
        "shop_notes": [
            "The first note in the program is shown in the control directory.",
        ],
        "workholding": [
            "Rotary fixture mounts on the right side of the table.",
            "Max length from chuck face to tailstock is 22 in.",
        ],
        "offset_logic": [
            "G110 is on the right and counts up as you go left.",
        ],
        "milling_notes": [
            "Flip sequence:",
            "G91 G28 Z0",
            "G90 G53 X-20. Y0.",
            "M00 (turn part and continue)",
        ],
        "posting_cimco": [
            "Verify O##### format.",
            "Verify one M code per line.",
            "Verify early M8 output and X-.020 home move.",
        ],
        "special_notes": [
            "656 is easy to trip up with pocket-count limits and M-code formatting.",
        ],
    },
    "657 Haas VF5": {
        "machine_type": "Mill",
        "overview": [
            "Haas VF5 with A axis.",
        ],
        "program_behavior": [
            "10000 RPM spindle.",
            "Program format is O#####.NC.",
            "Program must start with O#####.",
        ],
        "code_rules": [
            "Change the end home position to X-.020.",
        ],
        "milling_notes": HAAS_FLIP_SEQUENCE_30,
        "posting_cimco": [
            "Verify the A-axis setup and the X-.020 home position before release.",
        ],
        "special_notes": [
            "Current repo note set for 657 is still light. Verify setup details at the machine.",
        ],
    },
    "Cincinnati Arrow Mill": {
        "machine_type": "Mill",
        "overview": [
            "Cincinnati Millicron 3X VMC / Cincinnati Arrow style machine entry.",
            "Only post file was supplied in this batch, not a dedicated note page.",
        ],
        "program_behavior": [
            "Post supports subprograms.",
        ],
        "post_limits": [
            "Subprogram type in post is external subprograms (M98).",
            "Tool offset override is not matched in the post.",
            "Subprogram numbering starts at 1000.",
        ],
        "code_rules": [
            "Verify actual shop rules before first use because this page is post-driven right now.",
        ],
        "shop_notes": [
            "Add machine-specific shop notes as they are captured.",
        ],
        "workholding": [
            "Verify actual setup.",
        ],
        "tooling": [
            "Verify actual machine loadout.",
        ],
        "posting_cimco": [
            "Backplot and inspect output carefully until notes are added.",
        ],
        "offset_logic": [
            "Verify actual offset behavior.",
        ],
        "mastercam_rules": [
            "Verify origin and post selection before release.",
        ],
        "special_notes": [
            "This page still needs real shop notes.",
        ],
    },
    "411 Manual Lathe": {
        "machine_type": "Manual Lathe",
        "overview": [
            "Manual machine reference page.",
        ],
        "program_behavior": ["Not applicable."],
        "post_limits": ["Not applicable."],
        "code_rules": ["Not applicable."],
        "shop_notes": ["Use for manual-machine reference only."],
        "workholding": ["Verify setup manually."],
        "tooling": ["Manual tooling reference placeholder."],
        "posting_cimco": ["Not applicable."],
        "offset_logic": ["Not applicable."],
        "mastercam_rules": ["Not applicable."],
        "special_notes": ["Add manual-machine-specific notes later."],
    },
    "413 Manual Lathe": {
        "machine_type": "Manual Lathe",
        "overview": [
            "Manual machine reference page.",
        ],
        "program_behavior": ["Not applicable."],
        "post_limits": ["Not applicable."],
        "code_rules": ["Not applicable."],
        "shop_notes": ["Use for manual-machine reference only."],
        "workholding": ["Verify setup manually."],
        "tooling": ["Manual tooling reference placeholder."],
        "posting_cimco": ["Not applicable."],
        "offset_logic": ["Not applicable."],
        "mastercam_rules": ["Not applicable."],
        "special_notes": ["Add manual-machine-specific notes later."],
    },
}
