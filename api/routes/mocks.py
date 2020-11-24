# /users
mock_user_list = [
    {
        "userID": 1,
        "teamID": 1,
        "emailAddress": "hackathon@tumblr.com",
        "points": 123
    },
    {
        "userID": 2,
        "teamID": 2,
        "emailAddress": "something@nowhere.com",
        "points": 456
    },
    {
        "userID": 3,
        "teamID": 1,
        "emailAddress": "2020@didnthappen.com",
        "points": 789
    },
    {
        "userID": 4,
        "teamID": 1,
        "emailAddress": "josh@josh.net",
        "points": 111
    },
    {
        "userID": 5,
        "teamID": 3,
        "emailAddress": "michaelangelo@ninjaturtles.ca",
        "points": 1337
    },
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
    },
    {
        "userID": 8,
        "teamID": 4,
        "emailAddress": "jonsnow@thewalltbh.com",
        "points": 34
    }
]
# /teams
mock_teams_list = [
    {
        "name": "Party Parrot",
        "teamID": 1,
    },

    {
        "name": "Dancing Banana",
        "teamID": 2
    },
    {
        "name": "Coffee Cat",
        "teamID": 4
    },
    {
        "name": "Yay Orange",
        "teamID": 3
    }
]
# /teams/<id>
mock_team_with_users = [
    {
        "name": "Party Parrot",
        "teamID": 1,
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
        "name": "Dancing Banana",
        "teamID": 2,
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
        "name": "Yay Orange",
        "teamID": 3,
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
        "name": "Coffee Cat",
        "teamID": 4,
        "users": [{
            "userID": 8,
            "teamID": 4,
            "emailAddress": "jonsnow@thewalltbh.com",
            "points": 34
        }]
    }
]
# team/<id>
mock_team = {
    "name": "Flatbush Zombies",
    "teamID": 3
}