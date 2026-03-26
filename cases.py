cases = [
    {
        "title": "the missing necklace",
        "difficulty": "easy",
        "story": "A diamond necklace went missing during a party at a luxury mansion.",
        "environment": {
            "location": "Main Hall",
            "time": "8 PM",
            "weather": "Rainy night",
            "sounds": "Background chatter, soft piano music"
        },
        "clues": [
            "The window was open.",
            "No signs of forced entry.",
            "Only 3 people had access: Alice, Bob, Clara."
        ],
        "objects": [
            {"name": "necklace case", "description": "A small velvet box, now empty."},
            {"name": "window", "description": "Slightly open, rain droplets outside."},
            {"name": "kitchen", "description": "Clean, with traces of cookies."}
        ],
        "suspects": {
            "Alice": {
                "description": "Was in the kitchen all night.",
                "dialogue": [
                    "I didn’t see anything unusual.",
                    "I only baked cookies, that’s it!"
                ]
            },
            "Bob": {
                "description": "Left early.",
                "dialogue": [
                    "I had to leave for a meeting.",
                    "I didn’t go near the jewelry."
                ]
            },
            "Clara": {
                "description": "Stayed near the jewelry table.",
                "dialogue": [
                    "I was admiring the necklaces.",
                    "I didn’t touch any of them!"
                ]
            }
        },
        "answer": "Clara",
        "reward_points": 10,
        "hints": [
            "Think about who was closest to the necklace.",
            "Consider who had the opportunity."
        ]
    },
    {
        "title": "the office theft",
        "difficulty": "medium",
        "story": "Money disappeared from the office drawer during a busy day.",
        "environment": {
            "location": "Office Room 3B",
            "time": "2 PM",
            "weather": "Sunny",
            "sounds": "Typing, printers running"
        },
        "clues": [
            "Drawer was not broken.",
            "Only employees had keys.",
            "Camera was off for 10 minutes."
        ],
        "objects": [
            {"name": "drawer", "description": "Locked but undamaged."},
            {"name": "camera system", "description": "Shows a 10-minute blind spot."}
        ],
        "suspects": {
            "John": {
                "description": "Was working late.",
                "dialogue": [
                    "I was in my office the whole afternoon.",
                    "I didn’t go near the drawers."
                ]
            },
            "Emma": {
                "description": "Had access to camera system.",
                "dialogue": [
                    "I noticed the camera glitching, but I didn’t touch the money.",
                    "I was monitoring reports."
                ]
            },
            "Mike": {
                "description": "Left early.",
                "dialogue": [
                    "I finished my tasks and left at noon.",
                    "I didn’t see anything suspicious."
                ]
            }
        },
        "answer": "Emma",
        "reward_points": 15,
        "hints": [
            "Who could have manipulated the cameras?",
            "Check who had both opportunity and access."
        ]
    },
    {
        "title": "the silent witness",
        "difficulty": "hard",
        "story": "A man was found unconscious in his living room. No witnesses and no noise were reported.",
        "environment": {
            "location": "Victim’s apartment",
            "time": "11 PM",
            "weather": "Clear night",
            "sounds": "Clock ticking, faint music"
        },
        "clues": [
            "A glass with residue was found.",
            "The victim had no visible injuries.",
            "Only close friends visited earlier."
        ],
        "objects": [
            {"name": "glass", "description": "Contains a strange residue."},
            {"name": "couch", "description": "Where the victim was found."},
            {"name": "bookshelf", "description": "Books are slightly disturbed."}
        ],
        "suspects": {
            "Liam": {
                "description": "Brought drinks.",
                "dialogue": [
                    "I offered a drink to the victim.",
                    "I left quietly after that."
                ]
            },
            "Noah": {
                "description": "Left quickly.",
                "dialogue": [
                    "I only stopped by briefly.",
                    "I didn’t interact with the drinks."
                ]
            },
            "Olivia": {
                "description": "Stayed longest.",
                "dialogue": [
                    "I was reading with the victim.",
                    "I didn’t touch anything suspicious."
                ]
            }
        },
        "answer": "Liam",
        "reward_points": 20,
        "hints": [
            "Check who handled the drinks.",
            "Think about timing of visits and actions."
        ]
    }
]