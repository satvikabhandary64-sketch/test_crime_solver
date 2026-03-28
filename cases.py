# ---------------------------------------------------------------
# CASES — Crime Solver Pro
# Replace each "image_url" value with your own photo path/URL.
#
# PUZZLE SYSTEM:
#   Each room may have a "lock" (must solve to enter) and/or
#   a "puzzle" (must solve to reveal the real clue).
#
#   lock = {
#       "type": "riddle" | "cipher",
#       "question": str,         # what the player sees
#       "answer": str,           # correct answer (lowercase, stripped)
#       "hint": str,             # shown after 1 wrong attempt
#   }
#
#   puzzle = {
#       "type": "riddle" | "cipher",
#       "question": str,
#       "cipher_text": str,      # only for cipher type — the encoded string
#       "answer": str,           # correct answer (lowercase, stripped)
#       "hint": str,
#       "false_clue": str,       # shown if player answers WRONG
#   }
#
#   "locked": True               # room requires solving lock before entering
#
# LOGIC GRID is case-level (not per-room) — see "logic_grid" key.
# ---------------------------------------------------------------

cases = [
    # ===========================================================
    # EASY — THEFT: The Stolen Watch
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
            "The watch was confirmed on the mantelpiece at 7 PM by two guests.",
            "No signs of forced entry anywhere in the house.",
            "One guest was seen alone in the drawing room for several minutes.",
            "One guest has a documented history of financial trouble.",
            "A coat by the door had an unusually heavy pocket.",
        ],

        # ----------------------------------------------------------
        # LOGIC GRID — used in Step 1 (Evidence Board)
        # rows = suspects, cols = attributes to cross-reference
        # correct_solution: dict of {suspect: [true attributes]}
        # ----------------------------------------------------------
        "logic_grid": {
            "intro": "Cross-reference each suspect against the known facts. Tick every box that applies.",
            "suspects": ["Diana", "Frank", "Helen"],
            "attributes": ["Was alone in Drawing Room", "Has financial debt", "Left dinner table", "Has kitchen alibi", "Coat felt heavy"],
            "correct": {
                "Diana":  [True,  True,  True,  False, False],
                "Frank":  [False, False, False, False, True],
                "Helen":  [False, False, False, True,  False],
            },
            "reward_clue": "The grid confirms it: only one suspect was alone in the drawing room AND had financial motive AND left the table.",
            "false_clue":  "Inconclusive — the evidence seems to point toward Frank's suspicious coat.",
        },

        "rooms": [
            {
                "name": "Drawing Room",
                "icon": "🛋️",
                "suspect": "Diana",
                "object": "Empty mantelpiece",
                "image_url": "Drawing room.jpg",
                "description": "The mantelpiece shelf has a faint ring where the watch sat. Diana was found alone here.",
                "clue_revealed": "Diana was alone in this room at 8:20 PM — exactly when the watch disappeared.",
                "false_clue": "The dust patterns suggest someone short stood here — pointing more toward Helen.",
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 This room holds the key clue — but the evidence is locked behind a riddle.\n\n"
                        "*I have hands but cannot clap. I have a face but cannot smile. "
                        "I tell you when things happen, but I am always still. What am I?*"
                    ),
                    "answer": "clock",
                    "hint": "You check it every morning. It hangs on walls or sits on wrists.",
                    "false_clue": "The dust patterns suggest someone short stood here — pointing more toward Helen.",
                },
            },
            {
                "name": "Dining Room",
                "icon": "🍽️",
                "object": "Dinner table",
                "image_url": "Dining room.jpg",
                "description": "The dinner table is cleared. One seat was empty between 8:15 and 8:30 PM.",
                "clue_revealed": "The empty seat belongs to Diana — she slipped away during the main course.",
                "false_clue": "The seating chart shows Frank sat nearest the door — he could have slipped out easily.",
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 The waiter remembers something — unlock it.\n\n"
                        "*The more you take, the more you leave behind. What am I?*"
                    ),
                    "answer": "footsteps",
                    "hint": "Think about walking away from a scene.",
                    "false_clue": "The seating chart shows Frank sat nearest the door — he could have slipped out easily.",
                },
            },
            {
                "name": "Entrance Hall",
                "icon": "🚪",
                "locked": True,
                "suspect": "Frank",
                "object": "Heavy coat",
                "image_url": "Hall.jpg",
                "description": "Three coats hang by the door. One feels unusually heavy in the left pocket.",
                "clue_revealed": "The coat belongs to Frank — the pocket holds only spare change. Not the watch.",
                "false_clue": "The coat lining has a hidden inner pocket — exactly the right size for a Rolex.",
                "lock": {
                    "type": "cipher",
                    "question": "🔐 The entrance is sealed. Decode this message to enter:\n\nCipher (reverse the text): **TAOC YVAeH**",
                    "answer": "heavy coat",
                    "hint": "Read it backwards, letter by letter.",
                },
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 The coat holds a secret — solve this to find out what.\n\n"
                        "*I'm light as a feather, yet the strongest man can't hold me for more than a few minutes. What am I?*"
                    ),
                    "answer": "breath",
                    "hint": "You do it constantly without thinking. You can't hold it for long.",
                    "false_clue": "The coat lining has a hidden inner pocket — exactly the right size for a Rolex.",
                },
            },
            {
                "name": "Kitchen",
                "icon": "🥘",
                "suspect": "Helen",
                "object": "Staff logbook",
                "image_url": "Kitchen.jpg",
                "description": "The kitchen staff logbook shows all staff were present from 7:30 to 9 PM.",
                "clue_revealed": "Helen was in the kitchen all night — confirmed by two staff members.",
                "false_clue": "There's a 12-minute gap in Helen's logbook entries — unaccounted time.",
                "puzzle": {
                    "type": "cipher",
                    "question": "🔒 The logbook has a coded entry. Decode it (Caesar shift +3 — shift each letter back by 3):",
                    "cipher_text": "KHOHA ZDV KHUH",
                    "answer": "helen was here",
                    "hint": "Each letter is shifted forward by 3. A→D, B→E... so reverse it: D→A, E→B.",
                    "false_clue": "There's a 12-minute gap in Helen's logbook entries — unaccounted time.",
                },
            },
            {
                "name": "Study",
                "icon": "📋",
                "locked": True,
                "object": "Debt notice",
                "image_url": "Study.jpg",
                "description": "A crumpled letter on the desk — a debt collection notice addressed to Diana Voss.",
                "clue_revealed": "Diana is $30,000 in debt. She had a powerful financial motive.",
                "false_clue": "The debt notice is addressed to Gerald Mercer himself — perhaps he staged the theft.",
                "lock": {
                    "type": "riddle",
                    "question": "🔐 The study door is locked. Answer to enter:\n\n*I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?*",
                    "answer": "echo",
                    "hint": "You hear me in mountains and empty halls.",
                },
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 A letter lies folded on the desk. To read it, solve this:\n\n"
                        "*The more of me there is, the less you see. What am I?*"
                    ),
                    "answer": "darkness",
                    "hint": "Turn off the lights.",
                    "false_clue": "The debt notice is addressed to Gerald Mercer himself — perhaps he staged the theft.",
                },
            },
            {
                "name": "Back Garden",
                "icon": "🌿",
                "object": "Disturbed soil",
                "image_url": "Backgarden.jpg",
                "description": "A patch of soil near the garden wall is freshly disturbed.",
                "clue_revealed": "Someone planned to retrieve something buried here later — a stash point.",
                "false_clue": "Gardening tools are freshly used — the groundskeeper was here after dark, suspicious.",
                "puzzle": {
                    "type": "cipher",
                    "question": "🔒 A note is buried in a small tin. Decode it (reverse the text):",
                    "cipher_text": "EREHEREHTKCABEHT",
                    "answer": "the back here here",
                    "hint": "Simply read the letters in reverse order.",
                    "false_clue": "Gardening tools are freshly used — the groundskeeper was here after dark, suspicious.",
                },
            },
        ],

        "suspects": {
            "Diana": {
                "description": "Interior decorator, currently in serious financial trouble.",
                "dialogue": [
                    "I stepped away for some air — the dining room was stuffy.",
                    "I've admired that watch before, sure. Doesn't mean I took it.",
                    "Check Frank's coat. He was acting strange all evening.",
                ]
            },
            "Frank": {
                "description": "Gerald's business partner, a frequent visitor.",
                "dialogue": [
                    "I was at the table the whole time — ask Gerald.",
                    "My coat pocket? Spare change. Go ahead and look.",
                    "Diana was gone for at least fifteen minutes. Nobody noticed?",
                ]
            },
            "Helen": {
                "description": "Caterer hired for the evening.",
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
            "her financial motive. Frank's coat held only spare change. Helen had a confirmed alibi."
        ),
        "reward_points": 10,
        "hints": [
            "Who was unaccounted for at the dinner table?",
            "Check the study — financial trouble is a classic motive.",
            "The empty seat tells you exactly when the theft happened.",
        ]
    },

    # ===========================================================
    # MEDIUM — ARSON: The Burnfield Warehouse
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
            "intro": "Map each suspect against the physical evidence. Mark every fact that applies to them.",
            "suspects": ["Ray Corbin", "Sandra Oakes", "Pete Dunne"],
            "attributes": ["On site after 1 AM", "Has supervisor system access", "Fingerprint on canister", "Left before midnight", "Co-signed insurance"],
            "correct": {
                "Ray Corbin":   [True,  True,  True,  False, False],
                "Sandra Oakes": [False, False, False, False, True],
                "Pete Dunne":   [False, False, False, True,  False],
            },
            "reward_clue": "Only one person was on site after 1 AM, had system access to wipe footage, AND left a fingerprint.",
            "false_clue":  "The insurance co-signature places Sandra Oakes as the primary financial beneficiary — strong motive.",
        },

        "rooms": [
            {
                "name": "East Entrance",
                "icon": "🔥",
                "suspect": "Ray Corbin",
                "object": "Accelerant trail",
                "image_url": "eastentrance.jpg",
                "description": "Burn patterns show the fire started here. Lighter fluid pooled near the door frame.",
                "clue_revealed": "Ray Corbin's keycard logged entry at 1:47 AM through this door.",
                "false_clue": "The burn pattern suggests the fire spread from outside — possibly an outsider.",
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 The fire marshal's report is locked behind a riddle.\n\n"
                        "*I destroy everything I touch, yet I give life and warmth. "
                        "I have no mouth yet I consume. What am I?*"
                    ),
                    "answer": "fire",
                    "hint": "You're standing in its aftermath right now.",
                    "false_clue": "The burn pattern suggests the fire spread from outside — possibly an outsider.",
                },
            },
            {
                "name": "Storage Bay 4",
                "icon": "📦",
                "locked": True,
                "object": "Engraved lighter",
                "image_url": "storagebay4.jpg",
                "description": "Charred shelving and a second ignition point. A scorched lighter near the bay post.",
                "clue_revealed": "The lighter is engraved 'R.C.' — Ray Corbin's initials. Hard to explain away.",
                "false_clue": "The initials 'R.C.' could also stand for the company name — Rylance Corp. Red herring.",
                "lock": {
                    "type": "cipher",
                    "question": "🔐 Bay 4 is sealed with a padlock code. The combination is hidden in this cipher.\n\nDecode (reverse): **4 YAB RETTAM SDLEIF**",
                    "answer": "fields matter bay 4",
                    "hint": "Read each word in reverse order.",
                },
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 Something small on the floor holds the key. Solve this to identify it:\n\n"
                        "*I can start a war or end one. I fit in your pocket. "
                        "My spark can destroy a forest. What am I?*"
                    ),
                    "answer": "lighter",
                    "hint": "You use it to ignite things. Small, metal, engraved.",
                    "false_clue": "The initials 'R.C.' could stand for Rylance Corp — the former building owner.",
                },
            },
            {
                "name": "Manager's Office",
                "icon": "🗂️",
                "suspect": "Sandra Oakes",
                "object": "Insurance paperwork",
                "image_url": "managersoffice.jpg",
                "description": "Insurance policy in the filing cabinet — tripled six weeks ago. Sandra co-signed.",
                "clue_revealed": "Sandra co-signed the inflated insurance. Financial motive exists — but she wasn't on site.",
                "false_clue": "Sandra's handwriting on the policy is shaky — possibly signed under duress or forged.",
                "puzzle": {
                    "type": "cipher",
                    "question": "🔒 The policy has a handwritten note in code. Decode it (Caesar shift +4 — shift each letter back by 4):",
                    "cipher_text": "WERHXVE'W ASVOW",
                    "answer": "sandra's works",
                    "hint": "Each letter was shifted forward by 4. Reverse that: E→A, F→B, etc.",
                    "false_clue": "Sandra's handwriting on the policy appears shaky — possibly forged or signed under pressure.",
                },
            },
            {
                "name": "Security Room",
                "icon": "📷",
                "locked": True,
                "object": "Wiped hard drive",
                "image_url": "securityroom.jpg",
                "description": "The DVR is wiped. Logs show supervisor login at 1:52 AM — Ray Corbin's credentials.",
                "clue_revealed": "Ray used his own supervisor login to erase footage — 18 minutes before the fire.",
                "false_clue": "The login credentials were stolen — someone impersonated Ray to frame him.",
                "lock": {
                    "type": "riddle",
                    "question": "🔐 The security room requires a verbal code. Answer this to gain entry:\n\n*I watch everything but remember nothing once you clear me. I see all crimes but cannot speak. What am I?*",
                    "answer": "camera",
                    "hint": "It records. It watches. It can be wiped.",
                },
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 The wipe log has a timestamp anomaly. Solve this to read it:\n\n"
                        "*I have a beginning and middle but no end. I can be deleted "
                        "but I always leave a trace. What am I?*"
                    ),
                    "answer": "record",
                    "hint": "Think about what a DVR stores.",
                    "false_clue": "The wipe was triggered remotely — from an external IP address, not on-site.",
                },
            },
            {
                "name": "Loading Dock",
                "icon": "🚚",
                "suspect": "Pete Dunne",
                "object": "Keycard swipe log",
                "image_url": "loadingdock.jpg",
                "description": "Pete Dunne's keycard shows entry at 12:30 AM and exit at 1:15 AM.",
                "clue_revealed": "Pete left over an hour before the fire — his exit timestamp is verified.",
                "false_clue": "Keycard logs can be spoofed — Pete may have stayed on site without swiping again.",
                "puzzle": {
                    "type": "cipher",
                    "question": "🔒 The access log has an encrypted entry. Decode it (reverse the text):",
                    "cipher_text": "MA 51:1 TA TUO DEPPAWS ENNUD",
                    "answer": "dunne swapped out at 1:15 am",
                    "hint": "Read the entire string backwards.",
                    "false_clue": "Keycard logs can be spoofed — Pete may have stayed on-site without swiping out.",
                },
            },
            {
                "name": "Roof Access",
                "icon": "🏗️",
                "object": "Fuel canister",
                "image_url": "roofaccess.jpg",
                "description": "A half-empty lighter fluid canister behind the roof hatch — same brand as the trail below.",
                "clue_revealed": "Partial fingerprint on the canister — lab match: Ray Corbin.",
                "false_clue": "The canister brand is sold in bulk to the warehouse — any employee could have left it.",
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 The canister is tagged with evidence tape. Read the forensics note — solve this first:\n\n"
                        "*I touch everything you touch, yet you cannot see me. "
                        "I can place you at the scene of any crime. What am I?*"
                    ),
                    "answer": "fingerprint",
                    "hint": "You leave me on every surface. No two are alike.",
                    "false_clue": "The canister brand is sold in bulk to the warehouse — any employee could have left it.",
                },
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
    # HARD — MURDER: The Coldwell Inheritance
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
            "Toxicology confirmed: aconitine poisoning — slow-acting and odourless.",
            "The will was rewritten 14 days ago — sole beneficiary changed to Marcus Coldwell.",
            "Only one person delivered the nightly whisky to the study.",
            "A chemistry textbook hidden in the guest room was marked at the aconitine chapter.",
            "Reginald's doctor confirms symptoms for 48 hours — poison administered days earlier.",
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
            "reward_clue": "One suspect delivered the whisky, stands to inherit everything, and has documented chemistry knowledge.",
            "false_clue":  "Evelyn was cut from the will and has no alibi for the 48-hour window before death — she had time and motive.",
        },

        "rooms": [
            {
                "name": "Private Study",
                "icon": "🪑",
                "suspect": "Marcus Coldwell",
                "object": "Poisoned whisky glass",
                "image_url": "privatestudy.jpg",
                "description": "Reginald slumped in his armchair. The whisky glass tests positive for aconitine.",
                "clue_revealed": "Marcus served Reginald his nightly whisky every evening this week — confirmed by Iris.",
                "false_clue": "The glass was poured by Iris in the kitchen — she had access to the whisky before Marcus.",
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 The forensics report is sealed. Solve this to read it:\n\n"
                        "*I have no taste, no smell, no colour — yet I can end a life quietly. "
                        "I am feared by many but seen by none. What am I?*"
                    ),
                    "answer": "poison",
                    "hint": "Think about what killed the victim. Silent, invisible, deadly.",
                    "false_clue": "The glass was poured and handled by Iris in the kitchen — she touched it before Marcus.",
                },
            },
            {
                "name": "Guest Room",
                "icon": "🛏️",
                "locked": True,
                "object": "Hidden chemistry book",
                "image_url": "guestroom.jpg",
                "description": "A chemistry textbook wedged under the mattress, worn at the aconitine chapter.",
                "clue_revealed": "This is Marcus's room. His name is written in the front cover of the book.",
                "false_clue": "The book belongs to Evelyn — she studied biochemistry before dropping out.",
                "lock": {
                    "type": "cipher",
                    "question": "🔐 The guest room is locked from inside. The spare key code is encoded:\n\nDecode (reverse): **TSEUG EHT SI SUCRAM**",
                    "answer": "marcus is the guest",
                    "hint": "Read every word backwards.",
                },
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 The book is wedged shut. Answer this to open it:\n\n"
                        "*I am taken from a mine, shut up in a wooden case, "
                        "from which I am never released, yet I am used by almost every person. What am I?*"
                    ),
                    "answer": "pencil",
                    "hint": "Used for writing. Made of wood and graphite.",
                    "false_clue": "The book belongs to Evelyn — her old university text from before she dropped out.",
                },
            },
            {
                "name": "Solicitor's Room",
                "icon": "📜",
                "locked": True,
                "object": "Rewritten will",
                "image_url": "solicitorsroom.jpg",
                "description": "Revised will in a forced-open drawer. Marcus is named sole heir.",
                "clue_revealed": "The will was changed 14 days ago. Marcus accompanied Reginald to the solicitor.",
                "false_clue": "The will signature has irregularities — it may have been forged without Reginald's knowledge.",
                "lock": {
                    "type": "riddle",
                    "question": "🔐 The solicitor's filing room is locked. Answer to enter:\n\n*I am always in front of you but cannot be seen. What am I?*",
                    "answer": "future",
                    "hint": "It hasn't happened yet. It's coming regardless.",
                },
                "puzzle": {
                    "type": "cipher",
                    "question": "🔒 The will has a handwritten margin note in code. Decode it (Caesar shift +2 — shift each letter back by 2):",
                    "cipher_text": "OCTEWU EJCPIGF YJGP OCTEWU ECOG",
                    "answer": "marcus changed when marcus came",
                    "hint": "Each letter is shifted forward by 2. Reverse: C→A, D→B, etc.",
                    "false_clue": "The will signature appears irregular — possibly signed under duress or forged entirely.",
                },
            },
            {
                "name": "Kitchen",
                "icon": "🍶",
                "suspect": "Iris",
                "object": "Whisky decanter",
                "image_url": "kitchen1.jpg",
                "description": "The whisky decanter tests completely clean. Poison was not added here.",
                "clue_revealed": "Iris prepared the tray but Marcus took it at the study door and delivered the glass himself.",
                "false_clue": "There is a small unlabelled bottle in the back of the spice cupboard — suspicious.",
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 The kitchen log is written in shorthand. Solve this to decipher it:\n\n"
                        "*I am always hungry, I must always be fed. "
                        "The finger I touch will soon turn red. What am I?*"
                    ),
                    "answer": "fire",
                    "hint": "Think heat. It consumes everything it touches.",
                    "false_clue": "There's a small unlabelled bottle in the back of the spice cupboard — contents unknown.",
                },
            },
            {
                "name": "Library",
                "icon": "📚",
                "suspect": "Evelyn",
                "object": "Phone with timestamps",
                "image_url": "library1.jpg",
                "description": "Evelyn was reading here all evening. Three time-stamped messages confirm she never left.",
                "clue_revealed": "Evelyn's phone data places her in the library from 8 PM to midnight. Solid alibi.",
                "false_clue": "Phones can be left in a room while the owner moves around — the alibi is not airtight.",
                "puzzle": {
                    "type": "cipher",
                    "question": "🔒 Evelyn left a note in a book. Decode it (reverse the text):",
                    "cipher_text": "YRARBILETFELREVENE",
                    "answer": "i never left the library",
                    "hint": "Read the string of letters in reverse.",
                    "false_clue": "A phone can be left in a room — the timestamps don't prove Evelyn never moved.",
                },
            },
            {
                "name": "Cellar",
                "icon": "🧪",
                "locked": True,
                "object": "Empty poison vial",
                "image_url": "cellar.jpg",
                "description": "Behind the wine rack: a tiny glass vial, empty. Traces of aconitine inside.",
                "clue_revealed": "Partial fingerprint on the vial — forensic match to Marcus Coldwell.",
                "false_clue": "The vial is a standard medicinal bottle — Reginald may have self-administered something.",
                "lock": {
                    "type": "cipher",
                    "question": "🔐 The cellar padlock has a word combination. Decode it:\n\nCipher (reverse): **RALLECEHT**",
                    "answer": "the cellar",
                    "hint": "Read the letters backwards.",
                },
                "puzzle": {
                    "type": "riddle",
                    "question": (
                        "🔒 The vial is inside a sealed evidence bag. Solve this to open the case file:\n\n"
                        "*The more you have of me, the less you see. "
                        "I am the friend of guilt and the enemy of truth. What am I?*"
                    ),
                    "answer": "darkness",
                    "hint": "Criminals hide in me. I'm what you need to conceal a crime.",
                    "false_clue": "The vial is a standard medicinal bottle — Reginald had a heart condition and self-medicated.",
                },
            },
        ],

        "suspects": {
            "Marcus Coldwell": {
                "description": "Reginald's nephew and sole beneficiary under the new will.",
                "dialogue": [
                    "Uncle Reginald asked me to bring the tray — I was just being helpful.",
                    "That chemistry book is old. I studied biochemistry at university, years ago.",
                    "I loved my uncle. The will change was entirely his own decision.",
                ]
            },
            "Iris": {
                "description": "Housekeeper at Coldwell Manor for 22 years.",
                "dialogue": [
                    "I prepared the tray as I do every night. Mr Marcus took it from me at the study door.",
                    "Mr Coldwell seemed unwell these past two days — I thought it was his age.",
                    "I have served this family faithfully for decades.",
                ]
            },
            "Evelyn": {
                "description": "Reginald's niece, recently removed from the will.",
                "dialogue": [
                    "I was in the library all evening. Check my phone.",
                    "Yes, I was cut from the will — and I was furious. But I didn't do this.",
                    "Look at Marcus. He took that tray to the study himself.",
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