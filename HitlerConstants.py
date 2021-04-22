# nastavení základních údajů o hře při určitém počtu hráčů
players = {
    5: {
        "liberal": 3,
        "fascist": 1,
        "track": [
            None,
            None,
            "policy",
            "kill",
            "kill",
            None
        ]
    },
    6: {
        "liberal": 4,
        "fascist": 1,
        "track": [
            None,
            None,
            "policy",
            "kill",
            "kill",
            None
        ]
    },
    7: {
        "liberal": 4,
        "fascist": 2,
        "track": [
            None,
            "inspect",
            "choose",
            "kill",
            "kill",
            None
        ]
    },
    8: {
        "liberal": 5,
        "fascist": 2,
        "track": [
            None,
            "inspect",
            "choose",
            "kill",
            "kill",
            None
        ]
    },
    9: {
        "liberal": 5,
        "fascist": 3,
        "track": [
            "inspect",
            "inspect",
            "choose",
            "kill",
            "kill",
            None
        ]
    },
    10: {
        "liberal": 6,
        "fascist": 3,
        "track": [
            "inspect",
            "inspect",
            "choose",
            "kill",
            "kill",
            None
        ]
    },
}

board = {
    "policy": {
        "liberal": 6,
        "fascist": 11
    }
}

pass_statements = {
    1 : "I drew three fascists.",
    2 : "I drew two fascists and a liberal, and discarded a fascist",
    3 : "I drew two liberals and a fascist, and discarded a liberal to give a choice.",
    4 : "I drew two liberals and a fascist, and discarded the fascist to force liberal.",
    5 : "I drew three liberals."
}

choice_statements = {
    1 : "I was passed a choice.",
    2 : "I was passed no choice."
}