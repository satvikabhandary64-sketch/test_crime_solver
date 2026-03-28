# ---------------------------------------------------------------
# CASES — Crime Solver Pro
# ---------------------------------------------------------------

cases = [
    # ===========================================================
    # EASY — THEFT: The Stolen Watch (NO PUZZLES)
    # ===========================================================
    {
        "title": "The Stolen Watch",
        "difficulty": "easy",
        "story": (
            "A vintage Rolex worth $12,000 vanished from the Mercer family's drawing room "
            "during a small dinner gathering. The host, Gerald Mercer, noticed it missing "
            "from the mantelpiece shelf at 9 PM. No windows were broken. No strangers "
            "entered the house. One of the three dinner guests took it — and left no obvious trace."
        ),
        "environment": {
            "location": "Mercer Residence",
            "time": "9 PM",
            "weather": "Mild evening",
            "sounds": "Dinner chatter, clinking glasses"
        },
        "clues": [
            "The watch was on the mantelpiece at 7 PM — two guests confirmed this.",
            "Diana left the dinner table for 15 minutes between 8:15 and 8:30 PM.",
            "Frank's coat pocket felt unusually heavy when he hung it up.",
            "Helen was in the kitchen with staff the entire evening — confirmed by two employees.",
            "A debt collection letter addressed to Diana was found in the study.",
        ],
        "logic_grid": {
            "intro": "As you investigate, tick the boxes that apply to each suspect.",
            "suspects": ["Diana", "Frank", "Helen"],
            "attributes": ["Left dinner table for 15+ min", "Has financial problems", "Was alone in Drawing Room", "Heavy coat pocket", "Kitchen alibi"],
            "correct": {
                "Diana":  [True,  True,  True,  False, False],
                "Frank":  [False, False, False, True,  False],
                "Helen":  [False, False, False, False, True],
            },
            "reward_clue": "Diana left the table, has debt problems, and was alone in the drawing room.",
            "false_clue":  "Frank's heavy coat seems suspicious — maybe he hid the watch there.",
        },
        "rooms": [
            {
                "name": "Drawing Room",
                "icon": "🛋️",
                "grid_x": 1,
                "grid_y": 0,
                "suspect": "Diana",
                "object": "Empty mantelpiece",
                "image_url": "Drawing room.jpg",
                "description": "The mantelpiece shelf has a faint ring where the watch sat. A maid saw Diana here alone around 8:20 PM.",
                "clue_revealed": "✓ Diana was alone in the drawing room at 8:20 PM — exactly when the watch disappeared.",
                "false_clue": "✗ The dust patterns suggest someone short stood here — pointing more toward Helen.",
                "puzzle": None,  # No puzzle for easy mode
            },
            {
                "name": "Dining Room",
                "icon": "🍽️",
                "grid_x": 0,
                "grid_y": 0,
                "object": "Dinner table",
                "image_url": "Dining room.jpg",
                "description": "The dinner table is cleared. One seat was empty between 8:15 and 8:30 PM.",
                "clue_revealed": "✓ Diana's seat was empty for 15 minutes — she slipped away during the main course.",
                "false_clue": "✗ The seating chart shows Frank sat nearest the door — he could have slipped out easily.",
                "puzzle": None,
            },
            {
                "name": "Entrance Hall",
                "icon": "🚪",
                "grid_x": 2,
                "grid_y": 0,
                "locked": False,  # No lock for easy mode
                "suspect": "Frank",
                "object": "Heavy coat",
                "image_url": "Hall.jpg",
                "description": "Three coats hang by the door. Frank's coat feels unusually heavy in the left pocket.",
                "clue_revealed": "✓ Frank's coat pocket holds only spare change and keys — not the watch.",
                "false_clue": "✗ The coat lining has a hidden inner pocket — exactly the right size for a Rolex.",
                "puzzle": None,
            },
            {
                "name": "Kitchen",
                "icon": "🥘",
                "grid_x": 0,
                "grid_y": 1,
                "suspect": "Helen",
                "object": "Staff logbook",
                "image_url": "Kitchen.jpg",
                "description": "The kitchen staff logbook shows all staff were present from 7:30 to 9 PM.",
                "clue_revealed": "✓ Helen was in the kitchen all night — confirmed by two staff members.",
                "false_clue": "✗ There's a 12-minute gap in Helen's logbook entries — unaccounted time.",
                "puzzle": None,
            },
            {
                "name": "Study",
                "icon": "📋",
                "grid_x": 1,
                "grid_y": 1,
                "locked": False,
                "object": "Debt notice",
                "image_url": "Study.jpg",
                "description": "A crumpled letter on the desk — a debt collection notice addressed to Diana Voss for $30,000.",
                "clue_revealed": "✓ Diana is $30,000 in debt — she had a powerful financial motive to steal the watch.",
                "false_clue": "✗ The debt notice is addressed to Gerald Mercer himself — perhaps he staged the theft.",
                "puzzle": None,
            },
            {
                "name": "Back Garden",
                "icon": "🌿",
                "grid_x": 2,
                "grid_y": 1,
                "object": "Disturbed soil",
                "image_url": "Backgarden.jpg",
                "description": "A patch of soil near the garden wall is freshly disturbed.",
                "clue_revealed": "✓ The garden soil was disturbed by the gardener earlier that day — unrelated to the theft.",
                "false_clue": "✗ Someone planned to retrieve something buried here later — a possible stash point.",
                "puzzle": None,
            },
        ],
        "suspects": {
            "Diana": {
                "description": "Interior decorator, currently in serious financial trouble ($30,000 debt).",
                "dialogue": [
                    "I stepped away for some air — the dining room was stuffy.",
                    "I've admired that watch before, sure. Doesn't mean I took it.",
                    "Check Frank's coat. He was acting strange all evening.",
                ]
            },
            "Frank": {
                "description": "Gerald's business partner, a frequent visitor with no financial troubles.",
                "dialogue": [
                    "I was at the table the whole time — ask Gerald.",
                    "My coat pocket? Spare change and keys. Go ahead and look.",
                    "Diana was gone for at least fifteen minutes. Nobody noticed?",
                ]
            },
            "Helen": {
                "description": "Caterer hired for the evening, worked in the kitchen all night.",
                "dialogue": [
                    "I was in the kitchen from seven-thirty. I never left.",
                    "My staff can vouch for me — we were plating dessert.",
                    "I don't even know where the drawing room is.",
                ]
            },
        },
        "answer": "Diana",
        "explanation": (
            "Diana stole the watch. She slipped away from the dinner table between 8:15 and 8:30 PM, "
            "went to the drawing room alone, and pocketed the Rolex. The debt notice in the study confirms "
            "her financial motive ($30,000). Frank's coat held only spare change. Helen had a confirmed alibi "
            "in the kitchen with staff."
        ),
        "reward_points": 10,
        "hints": [
            "Who left the dinner table during the critical time window?",
            "Check the study — financial trouble is a classic motive.",
            "Who was alone in the drawing room when the watch vanished?",
        ]
    },

    # ===========================================================
    # MEDIUM — ARSON: The Burnfield Warehouse (SIMPLIFIED)
    # ===========================================================
    {
        "title": "The Burnfield Warehouse",
        "difficulty": "medium",
        "story": (
            "At 2:14 AM, a fire tore through Burnfield Storage Warehouse on the east docks. "
            "The blaze was ruled deliberate — accelerant was found at two separate ignition points. "
            "The building was insured for three times its market value. Three people had "
            "keycard access that night. One of them set the fire."
        ),
        "environment": {
            "location": "Burnfield Storage, East Docks",
            "time": "2:14 AM",
            "weather": "Dry, windy night",
            "sounds": "Crackling fire, distant sirens"
        },
        "clues": [
            "Lighter fluid was poured at two points — east entrance and storage bay 4.",
            "Keycard logs show three entries between midnight and 2 AM.",
            "The building's insurance was tripled six weeks ago — owner's signature.",
            "A lighter engraved 'R.C.' was found near bay 4.",
            "Security footage was manually erased — requires supervisor credentials.",
        ],
        "logic_grid": {
            "intro": "As you investigate, tick the boxes that apply to each suspect.",
            "suspects": ["Ray Corbin", "Sandra Oakes", "Pete Dunne"],
            "attributes": ["On site after 1 AM", "Has supervisor system access", "Fingerprint on canister", "Left before midnight", "Co-signed insurance"],
            "correct": {
                "Ray Corbin":   [True,  True,  True,  False, False],
                "Sandra Oakes": [False, False, False, False, True],
                "Pete Dunne":   [False, False, False, True,  False],
            },
            "reward_clue": "Only Ray was on site after 1 AM, had system access to wipe footage, AND left a fingerprint.",
            "false_clue":  "Sandra co-signed the insurance — she had financial motive.",
        },
        "rooms": [
            {
                "name": "East Entrance",
                "icon": "🔥",
                "grid_x": 0,
                "grid_y": 0,
                "suspect": "Ray Corbin",
                "object": "Accelerant trail",
                "image_url": "eastentrance.jpg",
                "description": "Burn patterns show the fire started here. Lighter fluid pooled near the door frame.",
                "clue_revealed": "✓ Ray Corbin's keycard logged entry at 1:47 AM through this door.",
                "false_clue": "✗ The burn pattern suggests the fire spread from outside — possibly an outsider.",
                "puzzle": {
                    "type": "riddle",  # Only riddle, no cipher
                    "question": (
                        "🔒 The fire marshal's report is locked behind a riddle.\n\n"
                        "*I destroy everything I touch, yet I give life and warmth. "
                        "I have no mouth yet I consume. What am I?*"
                    ),
                    "answer": "fire",
                    "hint": "You're standing in its aftermath right now.",
                    "false_clue": "✗ The burn pattern suggests the fire spread from outside — possibly an outsider.",
                },
            },
            {
                "name": "Storage Bay 4",
                "icon": "📦",
                "grid_x": 1,
                "grid_y": 0,
                "locked": False,  # Remove lock for medium
                "object": "Engraved lighter",
                "image_url": "storagebay4.jpg",
                "description": "Charred shelving and a second ignition point. A scorched lighter near the bay post.",
                "clue_revealed": "✓ The lighter is engraved 'R.C.' — Ray Corbin's initials. Hard to explain away.",
                "false_clue": "✗ The initials 'R.C.' could also stand for the company name — Rylance Corp.",
                "puzzle": None,
            },
            {
                "name": "Manager's Office",
                "icon": "🗂️",
                "grid_x": 2,
                "grid_y": 0,
                "suspect": "Sandra Oakes",
                "object": "Insurance paperwork",
                "image_url": "managersoffice.jpg",
                "description": "Insurance policy in the filing cabinet — tripled six weeks ago. Sandra co-signed.",
                "clue_revealed": "✓ Sandra co-signed the inflated insurance. Financial motive exists — but she wasn't on site.",
                "false_clue": "✗ Sandra's handwriting on the policy is shaky — possibly signed under duress.",
                "puzzle": None,
            },
            {
                "name": "Security Room",
                "icon": "📷",
                "grid_x": 0,
                "grid_y": 1,
                "locked": False,
                "object": "Wiped hard drive",
                "image_url": "securityroom.jpg",
                "description": "The DVR is wiped. Logs show supervisor login at 1:52 AM — Ray Corbin's credentials.",
                "clue_revealed": "✓ Ray used his own supervisor login to erase footage — 18 minutes before the fire.",
                "false_clue": "✗ The login credentials were stolen — someone impersonated Ray to frame him.",
                "puzzle": {
                    "type": "cipher",  # Only cipher with helper
                    "question": "🔒 The wipe log has an encrypted entry. Decode it (Caesar cipher, shift +3):",
                    "cipher_text": "UDB UH ZDV KHUH DW 1:52 DP",
                    "answer": "ray was here at 1:52 am",
                    "hint": "Shift each letter BACK by 3: D→A, E→B, etc.",
                    "false_clue": "✗ The wipe was triggered remotely — from an external IP address.",
                },
            },
            {
                "name": "Loading Dock",
                "icon": "🚚",
                "grid_x": 1,
                "grid_y": 1,
                "suspect": "Pete Dunne",
                "object": "Keycard swipe log",
                "image_url": "loadingdock.jpg",
                "description": "Pete Dunne's keycard shows entry at 12:30 AM and exit at 1:15 AM.",
                "clue_revealed": "✓ Pete left over an hour before the fire — his exit timestamp is verified.",
                "false_clue": "✗ Keycard logs can be spoofed — Pete may have stayed on site without swiping again.",
                "puzzle": None,
            },
            {
                "name": "Roof Access",
                "icon": "🏗️",
                "grid_x": 2,
                "grid_y": 1,
                "object": "Fuel canister",
                "image_url": "roofaccess.jpg",
                "description": "A half-empty lighter fluid canister behind the roof hatch — same brand as the trail below.",
                "clue_revealed": "✓ Partial fingerprint on the canister — lab match: Ray Corbin.",
                "false_clue": "✗ The canister brand is sold in bulk to the warehouse — any employee could have left it.",
                "puzzle": None,
            },
        ],
        "suspects": {
            "Ray Corbin": {
                "description": "Warehouse supervisor with full keycard and system access.",
                "dialogue": [
                    "I came in late to do a stocktake. Completely routine.",
                    "That lighter? I lost it weeks ago — anyone could have found it.",
                    "I cleared old footage to free disk space. Standard procedure.",
                ]
            },
            "Sandra Oakes": {
                "description": "Warehouse co-owner who co-signed the insurance upgrade.",
                "dialogue": [
                    "The insurance increase was Ray's suggestion — he said stock value had risen.",
                    "I wasn't there that night. I was home, asleep.",
                    "I had nothing to gain from burning my own business.",
                ]
            },
            "Pete Dunne": {
                "description": "Night shift worker who clocked out early.",
                "dialogue": [
                    "I finished my shift at half one and went straight home.",
                    "The place was completely fine when I left.",
                    "Check the door logs — I was gone long before any fire.",
                ]
            },
        },
        "answer": "Ray Corbin",
        "explanation": (
            "Ray Corbin set the fire. His keycard placed him on site at 1:47 AM. He used his own "
            "supervisor login to erase security footage at 1:52 AM — then started the blaze. "
            "His engraved lighter was at the second ignition point and his fingerprint matched "
            "the fuel canister on the roof. Sandra had financial motive but wasn't present. "
            "Pete had a verified exit timestamp."
        ),
        "reward_points": 15,
        "hints": [
            "The engraved lighter 'R.C.' is hard to explain away.",
            "Who had system access to wipe the security footage?",
            "Check keycard timestamps — not everyone was there at 2 AM.",
        ]
    },

    # ===========================================================
    # HARD — MURDER: The Coldwell Inheritance (IMPROVED)
    # ===========================================================
    {
        "title": "The Coldwell Inheritance",
        "difficulty": "hard",
        "story": (
            "Reginald Coldwell, 71, was found dead in his private study at 11:30 PM. "
            "Cause of death: a slow-acting poison mixed into his nightly whisky. "
            "His estate — valued at £4 million — was the subject of a will quietly rewritten "
            "two weeks before his death. Three people were in the manor that evening. "
            "One of them knew exactly what was in that glass."
        ),
        "environment": {
            "location": "Coldwell Manor",
            "time": "11:30 PM",
            "weather": "Cold, fog on the grounds",
            "sounds": "Grandfather clock, wind in the eaves"
        },
        "clues": [
            "Toxicology confirmed: aconitine poisoning — slow-acting and odourless, takes 48 hours to be fatal.",
            "The will was rewritten 14 days ago — sole beneficiary changed to Marcus Coldwell.",
            "Marcus delivered the nightly whisky to the study every evening.",
            "A chemistry textbook hidden in the guest room has notes on aconitine extraction.",
            "Reginald's doctor confirms symptoms began 2 days ago — poison was administered earlier.",
        ],
        "logic_grid": {
            "intro": "This is a murder. Every detail matters. Cross-reference suspects against all known facts.",
            "suspects": ["Marcus Coldwell", "Iris", "Evelyn"],
            "attributes": ["Delivered the whisky", "Named in new will", "Has chemistry knowledge", "Phone alibi in library", "No motive found"],
            "correct": {
                "Marcus Coldwell": [True,  True,  True,  False, False],
                "Iris":            [False, False, False, False, True],
                "Evelyn":          [False, False, False, True,  False],
            },
            "reward_clue": "Marcus delivered the whisky, inherits £4 million, and has chemistry knowledge.",
            "false_clue":  "Evelyn was cut from the will — she had motive and opportunity.",
        },
        "rooms": [
            {
                "name": "Private Study",
                "icon": "🪑",
                "grid_x": 1,
                "grid_y": 0,
                "suspect": "Marcus Coldwell",
                "object": "Poisoned whisky glass",
                "image_url": "privatestudy.jpg",
                "description": "Reginald slumped in his armchair. The whisky glass tests positive for aconitine.",
                "clue_revealed": "✓ Marcus served Reginald his nightly whisky every evening this week — confirmed by Iris.",
                "false_clue": "✗ The glass was poured by Iris in the kitchen — she had access to the whisky before Marcus.",
                "puzzle": {
                    "type": "riddle",  # Only riddle, consistent
                    "question": (
                        "🔒 The forensics report is sealed. Solve this to read it:\n\n"
                        "*I have no taste, no smell, no colour — yet I can end a life quietly. "
                        "I am feared by many but seen by none. What am I?*"
                    ),
                    "answer": "poison",
                    "hint": "Think about what killed the victim. Silent, invisible, deadly.",
                    "false_clue": "✗ The glass was poured and handled by Iris in the kitchen — she touched it before Marcus.",
                },
            },
            {
                "name": "Guest Room",
                "icon": "🛏️",
                "grid_x": 0,
                "grid_y": 0,
                "locked": False,
                "object": "Hidden chemistry book",
                "image_url": "guestroom.jpg",
                "description": "A chemistry textbook wedged under the mattress, worn at the aconitine chapter.",
                "clue_revealed": "✓ This is Marcus's room. His name is written in the front cover of the book, with notes on poison extraction.",
                "false_clue": "✗ The book belongs to Evelyn — she studied biochemistry before dropping out.",
                "puzzle": None,
            },
            {
                "name": "Solicitor's Room",
                "icon": "📜",
                "grid_x": 2,
                "grid_y": 0,
                "locked": False,
                "object": "Rewritten will",
                "image_url": "solicitorsroom.jpg",
                "description": "Revised will in a forced-open drawer. Marcus is named sole heir to £4 million.",
                "clue_revealed": "✓ The will was changed 14 days ago. Marcus accompanied Reginald to the solicitor.",
                "false_clue": "✗ The will signature has irregularities — it may have been forged without Reginald's knowledge.",
                "puzzle": None,
            },
            {
                "name": "Kitchen",
                "icon": "🍶",
                "grid_x": 0,
                "grid_y": 1,
                "suspect": "Iris",
                "object": "Whisky decanter",
                "image_url": "kitchen1.jpg",
                "description": "The whisky decanter tests completely clean. Poison was not added here.",
                "clue_revealed": "✓ Iris prepared the tray but Marcus took it at the study door and delivered the glass himself.",
                "false_clue": "✗ There is a small unlabelled bottle in the back of the spice cupboard — suspicious.",
                "puzzle": {
                    "type": "cipher",  # One cipher with helper
                    "question": "🔒 The kitchen log has a coded entry. Decode it (Caesar cipher, shift +2):",
                    "cipher_text": "OCTEWU VQWM VJG VTC[",
                    "answer": "marcus took the tray",
                    "hint": "Shift each letter BACK by 2. Use the Caesar cipher helper above!",
                    "false_clue": "✗ There's a small unlabelled bottle in the back of the spice cupboard — contents unknown.",
                },
            },
            {
                "name": "Library",
                "icon": "📚",
                "grid_x": 1,
                "grid_y": 1,
                "suspect": "Evelyn",
                "object": "Phone with timestamps",
                "image_url": "library1.jpg",
                "description": "Evelyn was reading here all evening. Three time-stamped messages confirm she never left.",
                "clue_revealed": "✓ Evelyn's phone data places her in the library from 8 PM to midnight. Solid alibi.",
                "false_clue": "✗ A phone can be left in a room — the timestamps don't prove Evelyn never moved.",
                "puzzle": None,
            },
            {
                "name": "Cellar",
                "icon": "🧪",
                "grid_x": 2,
                "grid_y": 1,
                "locked": False,
                "object": "Empty poison vial",
                "image_url": "cellar.jpg",
                "description": "Behind the wine rack: a tiny glass vial, empty. Traces of aconitine inside.",
                "clue_revealed": "✓ Partial fingerprint on the vial — forensic match to Marcus Coldwell.",
                "false_clue": "✗ The vial is a standard medicinal bottle — Reginald may have self-administered something.",
                "puzzle": {
                    "type": "riddle",  # Different puzzle type from kitchen
                    "question": (
                        "🔒 The vial is inside a sealed evidence bag. Solve this to open the case file:\n\n"
                        "*I am taken from a mine, shut up in a wooden case, "
                        "from which I am never released, yet I am used by almost every person. What am I?*"
                    ),
                    "answer": "pencil lead",
                    "hint": "Used for writing. Made of wood and graphite.",
                    "false_clue": "✗ The vial is a standard medicinal bottle — Reginald had a heart condition and self-medicated.",
                },
            },
        ],
        "suspects": {
            "Marcus Coldwell": {
                "description": "Reginald's nephew and sole beneficiary under the new will (£4 million).",
                "dialogue": [
                    "Uncle Reginald asked me to bring the tray — I was just being helpful.",
                    "That chemistry book is old. I studied biochemistry at university, years ago.",
                    "I loved my uncle. The will change was entirely his own decision.",
                ]
            },
            "Iris": {
                "description": "Housekeeper at Coldwell Manor for 22 years, loyal servant.",
                "dialogue": [
                    "I prepared the tray as I do every night. Mr Marcus took it from me at the study door.",
                    "Mr Coldwell seemed unwell these past two days — I thought it was his age.",
                    "I have served this family faithfully for decades. I would never harm him.",
                ]
            },
            "Evelyn": {
                "description": "Reginald's niece, recently removed from the will.",
                "dialogue": [
                    "I was in the library all evening. Check my phone.",
                    "Yes, I was cut from the will — and I was furious. But I didn't do this.",
                    "Look at Marcus. He took that tray to the study himself every night.",
                ]
            },
        },
        "answer": "Marcus Coldwell",
        "explanation": (
            "Marcus Coldwell poisoned his uncle over several days using aconitine — researched "
            "using the chemistry textbook hidden in his room. He intercepted the whisky tray from "
            "Iris at the study door, adding the poison directly to the glass. The rewritten will "
            "gave him sole inheritance of £4 million. A poison vial in the cellar bore his "
            "fingerprint. Evelyn had motive but a watertight phone alibi. Iris had no motive "
            "and never handled the final glass."
        ),
        "reward_points": 20,
        "hints": [
            "The poison wasn't in the decanter — it was added to the glass at the last moment.",
            "Who had knowledge of aconitine AND handled the final glass?",
            "The vial in the cellar with a fingerprint is the hardest evidence.",
        ]
    },
]