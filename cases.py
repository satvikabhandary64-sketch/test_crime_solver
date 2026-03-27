cases = [
    {
        "title": "The Missing Necklace",
        "difficulty": "easy",
        "story": (
            "A priceless diamond necklace vanished during a high-society party at Hargrove Mansion. "
            "The host discovered the empty velvet case at 8 PM sharp. Rain lashed the windows. "
            "Soft piano drifted through the halls. Three guests had private access to the display room — "
            "but only one of them is lying."
        ),
        "environment": {
            "location": "Hargrove Mansion",
            "time": "8 PM",
            "weather": "Stormy night",
            "sounds": "Distant piano, rain on glass"
        },
        "clues": [
            "The display case lock was picked cleanly — no forced entry.",
            "A faint floral perfume lingered near the jewelry table.",
            "Clara was seen near the display room twice before dinner.",
            "Bob claims he left by 7:30 PM, but a staff member saw him at 7:55 PM.",
            "Alice's alibi: baking in the kitchen — but the oven was stone cold.",
        ],
        "rooms": [
            {
                "name": "Kitchen",
                "icon": "🥄",
                "suspect": "Alice",
                "object": "Cold oven",
                "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80",
                "description": "The kitchen smells faintly of cookies, but the oven is stone cold — Alice's alibi is crumbling.",
                "clue_revealed": "Alice claimed to have been baking all evening, but the oven hasn't been on.",
                "grid_x": 0, "grid_y": 0
            },
            {
                "name": "Display Room",
                "icon": "💎",
                "suspect": "Clara",
                "object": "Empty velvet case",
                "image_url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=600&q=80",
                "description": "The velvet case sits open and empty. A floral scent hangs in the air near the display stand.",
                "clue_revealed": "The lock was picked — not forced. And that perfume matches Clara's.",
                "grid_x": 1, "grid_y": 0
            },
            {
                "name": "Main Hall",
                "icon": "🚪",
                "suspect": "Bob",
                "object": "Guest logbook",
                "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&q=80",
                "description": "The entrance logbook shows Bob signed out at 7:30 — but a staff member places him here at 7:55.",
                "clue_revealed": "Bob lied about his departure time. He had opportunity.",
                "grid_x": 2, "grid_y": 0
            },
            {
                "name": "Library",
                "icon": "📚",
                "object": "Torn page",
                "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=80",
                "description": "A page torn from a notebook rests on the floor — too dark to read.",
                "clue_revealed": "Nothing conclusive here.",
                "grid_x": 0, "grid_y": 1
            },
            {
                "name": "Garden",
                "icon": "🌷",
                "object": "Muddy footprints",
                "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4ffe0?w=600&q=80",
                "description": "Muddy footprints lead from the garden window toward the display room. Small shoe size.",
                "clue_revealed": "Someone may have re-entered through the garden window — Clara wears size 5.",
                "grid_x": 1, "grid_y": 1
            },
            {
                "name": "Powder Room",
                "icon": "🪞",
                "object": "Floral perfume bottle",
                "image_url": "https://images.unsplash.com/photo-1541643600914-78b084683702?w=600&q=80",
                "description": "A perfume bottle sits on the shelf — the same floral scent from the display room.",
                "clue_revealed": "This is Clara's perfume. She was near the jewelry.",
                "grid_x": 2, "grid_y": 1
            },
        ],
        "suspects": {
            "Alice": {
                "description": "Claims she was baking all evening in the kitchen.",
                "dialogue": [
                    "I was in the kitchen the entire time! I didn't go anywhere near the jewelry.",
                    "I baked cookies — ask anyone! Well... the oven was being finicky, but still.",
                    "I don't even like diamonds. Too flashy.",
                ]
            },
            "Bob": {
                "description": "Says he left early for a business meeting.",
                "dialogue": [
                    "I signed out at 7:30. You can check the logbook.",
                    "I had nothing to do with the necklace — I was already gone.",
                    "Why would I risk my reputation for a piece of jewelry?",
                ]
            },
            "Clara": {
                "description": "Was spotted near the display room multiple times.",
                "dialogue": [
                    "I was just admiring the collection. Is that a crime?",
                    "That perfume? Lots of people wear that brand.",
                    "I didn't touch anything. You can't prove otherwise.",
                ]
            },
        },
        "answer": "Clara",
        "explanation": (
            "Clara was the culprit. Her perfume matched the scent at the crime scene, "
            "her shoe size matched the muddy footprints from the garden window, and she "
            "was seen near the display room twice. The cold oven ruled out Alice's alibi. "
            "Bob lied about timing but had no physical evidence linking him."
        ),
        "reward_points": 10,
        "hints": [
            "Follow the scent — it leads somewhere familiar.",
            "Who had both opportunity AND physical evidence linking them?",
            "The garden window footprints are key.",
        ]
    },
    {
        "title": "The Office Theft",
        "difficulty": "medium",
        "story": (
            "Fifteen hundred dollars vanished from the petty cash drawer in Office 3B on a busy Tuesday afternoon. "
            "The drawer was locked and undamaged. The security camera suffered a mysterious 10-minute blackout "
            "between 2:00 and 2:10 PM. Three employees were in the building — and one of them knew exactly "
            "how to go undetected."
        ),
        "environment": {
            "location": "Meridian Corp — Floor 3",
            "time": "2 PM",
            "weather": "Sunny afternoon",
            "sounds": "Keyboards, printer hum, distant phones"
        },
        "clues": [
            "The drawer was opened with a key — no damage whatsoever.",
            "The security camera had a manual override at exactly 2:00 PM.",
            "Emma is the only employee with admin access to the camera system.",
            "John's keycard logs show he was on Floor 3 at 2:04 PM.",
            "Mike's access log confirms he left the building at 11:58 AM.",
        ],
        "rooms": [
            {
                "name": "Office 3B",
                "icon": "🗄️",
                "suspect": "John",
                "object": "Cash drawer",
                "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&q=80",
                "description": "The locked drawer sits undisturbed — but it's empty. John's desk is right beside it.",
                "clue_revealed": "John's keycard places him on this floor during the blackout window.",
                "grid_x": 0, "grid_y": 0
            },
            {
                "name": "Server Room",
                "icon": "🖥️",
                "suspect": "Emma",
                "object": "Camera control panel",
                "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=80",
                "description": "The camera control panel shows a manual override was triggered at exactly 2:00 PM.",
                "clue_revealed": "Only Emma has admin access to this system. The override was deliberate.",
                "grid_x": 1, "grid_y": 0
            },
            {
                "name": "Break Room",
                "icon": "☕",
                "object": "Sign-in sheet",
                "image_url": "https://images.unsplash.com/photo-1572119865084-43c285814d63?w=600&q=80",
                "description": "The break room sign-in sheet shows John made coffee at 1:45 PM — then nothing until 2:15.",
                "clue_revealed": "John was unaccounted for between 1:45 and 2:15 PM.",
                "grid_x": 2, "grid_y": 0
            },
            {
                "name": "Lobby",
                "icon": "🚶",
                "suspect": "Mike",
                "object": "Visitor log",
                "image_url": "https://images.unsplash.com/photo-1497366412874-3415097a27e7?w=600&q=80",
                "description": "The visitor log confirms Mike badged out at 11:58 AM and never returned.",
                "clue_revealed": "Mike has a solid alibi — he wasn't in the building during the theft.",
                "grid_x": 0, "grid_y": 1
            },
            {
                "name": "Manager's Office",
                "icon": "🪑",
                "object": "Petty cash log",
                "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&q=80",
                "description": "The petty cash log shows the last withdrawal was at 9 AM — $1,500 was confirmed there at noon.",
                "clue_revealed": "The money was definitely taken during the 2 PM camera blackout.",
                "grid_x": 1, "grid_y": 1
            },
            {
                "name": "Hallway 3C",
                "icon": "🔑",
                "object": "Duplicate key",
                "image_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=600&q=80",
                "description": "A duplicate key to the petty cash drawer lies beneath a floor mat — recently cut.",
                "clue_revealed": "Someone had a copy made. Emma requested a locksmith visit last week.",
                "grid_x": 2, "grid_y": 1
            },
        ],
        "suspects": {
            "John": {
                "description": "Senior accountant, works next to the petty cash drawer.",
                "dialogue": [
                    "I was in my office the whole afternoon. I don't know anything about this.",
                    "Sure, I have a key — but so does Emma and the manager.",
                    "I got coffee and came straight back. Ask anyone.",
                ]
            },
            "Emma": {
                "description": "IT administrator with access to camera systems.",
                "dialogue": [
                    "The camera glitched. These things happen — hardware isn't perfect.",
                    "Yes, I have admin access, but I didn't touch it at 2 PM.",
                    "Why would I steal from my own company? I'm up for a promotion.",
                ]
            },
            "Mike": {
                "description": "Sales rep who left the building before lunch.",
                "dialogue": [
                    "I left before noon. I wasn't even there — check the logs.",
                    "Honestly, this has nothing to do with me.",
                    "I had a client lunch across town. I can prove it.",
                ]
            },
        },
        "answer": "Emma",
        "explanation": (
            "Emma orchestrated the theft. She used her admin access to trigger a manual camera blackout at 2:00 PM — "
            "not a hardware glitch. A duplicate key she'd had cut was found in Hallway 3C. "
            "John was on the floor but couldn't disable cameras. Mike wasn't even in the building."
        ),
        "reward_points": 15,
        "hints": [
            "A 'glitch' that happens at exactly the right moment is no accident.",
            "Who had the ability to cover their tracks electronically?",
            "The duplicate key in the hallway is a major lead.",
        ]
    },
    {
        "title": "The Silent Witness",
        "difficulty": "hard",
        "story": (
            "Victor Hale was found unconscious on his living room couch at 11 PM — no injuries, no forced entry. "
            "A glass with strange residue sat on the coffee table. His three closest friends had visited that evening. "
            "One of them didn't leave when they said they did — and one of them brought the drinks."
        ),
        "environment": {
            "location": "Victor Hale's Apartment, Unit 4F",
            "time": "11 PM",
            "weather": "Clear, cold night",
            "sounds": "Ticking clock, faint jazz record"
        },
        "clues": [
            "A glass contained traces of sedative — lab-confirmed.",
            "Victor's will was updated 2 weeks ago — Liam is the new primary beneficiary.",
            "Liam brought drinks and served them personally to everyone.",
            "Noah claims he left at 9 PM, but a neighbor heard voices from the apartment at 10:30 PM.",
            "Olivia says she was reading with Victor — but the bookmark never moved.",
        ],
        "rooms": [
            {
                "name": "Living Room",
                "icon": "🛋️",
                "suspect": "Olivia",
                "object": "Untouched book",
                "image_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&q=80",
                "description": "Victor lies on the couch. An open book sits on the end table — the bookmark hasn't moved an inch.",
                "clue_revealed": "Olivia claimed to be reading with Victor, but the book was untouched all night.",
                "grid_x": 1, "grid_y": 0
            },
            {
                "name": "Kitchen",
                "icon": "🍶",
                "suspect": "Liam",
                "object": "Drinks tray",
                "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80",
                "description": "A tray of glasses sits on the counter. One glass has a faint oily residue along the rim.",
                "clue_revealed": "Liam prepared and served all drinks. The residue glass was the one he handed Victor.",
                "grid_x": 0, "grid_y": 0
            },
            {
                "name": "Study",
                "icon": "📖",
                "object": "Victor's will",
                "image_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=600&q=80",
                "description": "A printed copy of Victor's will in a half-open drawer. Liam's name — primary beneficiary, updated 2 weeks ago.",
                "clue_revealed": "Liam stands to inherit Victor's entire estate. That's a powerful motive.",
                "grid_x": 2, "grid_y": 0
            },
            {
                "name": "Hallway",
                "icon": "🚪",
                "suspect": "Noah",
                "object": "Forgotten coat",
                "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80",
                "description": "A jacket hangs near the door — Noah's, but he claims to have left hours ago.",
                "clue_revealed": "Noah left his coat. He may have returned after claiming to leave.",
                "grid_x": 0, "grid_y": 1
            },
            {
                "name": "Balcony",
                "icon": "🌙",
                "object": "Cigarette butt",
                "image_url": "https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?w=600&q=80",
                "description": "A fresh cigarette butt on the balcony railing — still warm. Only Liam smokes.",
                "clue_revealed": "Liam was on the balcony late into the night — waiting to see the sedative take effect.",
                "grid_x": 1, "grid_y": 1
            },
            {
                "name": "Bathroom",
                "icon": "🪥",
                "object": "Empty vial",
                "image_url": "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=600&q=80",
                "description": "Behind the toilet: a tiny empty vial with no label — the type used for liquid sedatives.",
                "clue_revealed": "The vial was disposed of here. Only Liam used this bathroom alone during the visit.",
                "grid_x": 2, "grid_y": 1
            },
        ],
        "suspects": {
            "Liam": {
                "description": "Brought drinks and served them. Recently named in Victor's updated will.",
                "dialogue": [
                    "I brought some wine — we always drink together. Nothing unusual about that.",
                    "Victor seemed completely fine when I left. I swear on it.",
                    "The will thing is old news. Victor and I were close — he wanted me to have it.",
                ]
            },
            "Noah": {
                "description": "Claims he left at 9 PM, but voices were heard at 10:30 PM.",
                "dialogue": [
                    "I left around 9. Early night for me — I had work in the morning.",
                    "I have no idea what happened after I walked out that door.",
                    "Maybe someone else stopped by later. Don't look at me.",
                ]
            },
            "Olivia": {
                "description": "Claims she was reading with Victor all evening.",
                "dialogue": [
                    "We were reading together — well, he was tired so he lay down on the couch.",
                    "I left around 10. He was dozing off, perfectly peaceful.",
                    "I didn't notice anything strange about the drinks at all.",
                ]
            },
        },
        "answer": "Liam",
        "explanation": (
            "Liam poisoned Victor's drink with a sedative. He had motive (updated will naming him beneficiary), "
            "means (he served the drinks personally and used the bathroom alone to dispose of the vial), "
            "and opportunity (the cigarette butt placed him on the balcony late — waiting to ensure the plan worked). "
            "Noah's coat and Olivia's false alibi were red herrings."
        ),
        "reward_points": 20,
        "hints": [
            "Who served the drinks — and who benefits if Victor doesn't wake up?",
            "The cigarette on the balcony places someone there very late at night.",
            "An empty vial in the bathroom tells the true story.",
        ]
    }
]