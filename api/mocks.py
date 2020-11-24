# /users
mock_user_list = [
    {
        "userID": 1,
        "teamID": 1,
        "emailAddress": "hackathon.lastname@tumblr.com",
        "points": 123
    },
    {
        "userID": 2,
        "teamID": 2,
        "emailAddress": "something.weird@nowhere.com",
        "points": 456
    },
    {
        "userID": 3,
        "teamID": 1,
        "emailAddress": "2020.didnthappen@didnthappen.com",
        "points": 789
    },
    {
        "userID": 4,
        "teamID": 1,
        "emailAddress": "josh.thebest@josh.net",
        "points": 111
    },
    {
        "userID": 5,
        "teamID": 3,
        "emailAddress": "michaelangelo.ninja@ninjaturtles.ca",
        "points": 1337
    },
    {
        "userID": 6,
        "teamID": 2,
        "emailAddress": "jeff.bezos@match.com",
        "points": 1010101010101
    },
    {
        "userID": 7,
        "teamID": 1,
        "emailAddress": "arya.stark@kingslanding.io",
        "points": 2323
    },
    {
        "userID": 8,
        "teamID": 4,
        "emailAddress": "jon.snow@thewalltbh.com",
        "points": 34
    }
]

# /teams
mock_teams_list = [
    {
        "name": "Coffee Cat",
        "teamID": 2,
    },
    {
        "name": "Party Parrot",
        "teamID": 1
    },
    {
        "name": "Dancing Banana",
        "teamID": 3
    },
    {
        "name": "Yay Orange",
        "teamID": 4
    }
]

# /teams/<id>
mock_team_with_users = [
    {
        "name": "The Underachievers",
        "teamID": 2,
        "users": [
            {
            "userID": 3,
            "teamID": 2,
            "emailAddress": "2020@didnthappen.com",
            "points": 789
        },
        {
            "userID": 4,
            "teamID": 2,
            "emailAddress": "josh@josh.net",
            "points": 111
        },
        {
            "userID": 5,
            "teamID": 2,
            "emailAddress": "michaelangelo@ninjaturtles.ca",
            "points": 1337
        }
        ]
    },
    {
        "name": "NWA",
        "teamID": 1,
        "users": [
        {
            "userID": 6,
            "teamID": 2,
            "emailAddress": "jeffbezos@match.com",
            "points": 1010101010101
        },
        {
            "userID": 7,
            "teamID": 1,
            "emailAddress": "aryastark@kingslanding.io",
            "points": 2323
        }
        ]
    },
    {
        "name": "Flatbush Zombies",
        "teamID": 3,
        "users": []
    },
    {
        "name": "Onyx",
        "teamID": 4,
        "users": [
        {
            "userID": 5,
            "teamID": 3,
            "emailAddress": "michaelangelo@ninjaturtles.ca",
            "points": 1337
        }
        ]
    },
    {
        "name": "Wu Tang Clan",
        "teamID": 5,
        "users": []
    }
]

# team/<id>
mock_team = {
    "name": "Flatbush Zombies",
    "teamID": 3
}