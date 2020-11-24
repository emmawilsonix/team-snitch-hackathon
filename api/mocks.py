# /users
mock_user_list = [
    {
        "userID": 4,
        "teamID": 4,
        "emailAddress": "meeral.qureshi@indexexchange.com",
        "points": 2,
        "img": "../../assets/images/meeral.png"
    },
    {
        "userID": 1,
        "teamID": 2,
        "emailAddress": "cameron.ouellette@indexexchange.com",
        "points": 1,
        "img": "../../assets/images/cameron.png"
    },
    {
        "userID": 2,
        "teamID": 2,
        "emailAddress": "kaylin.lee@indexexchange.com",
        "points": 0,
        "img": "../../assets/images/kaylin.png"
    },
    {
        "userID": 3,
        "teamID": 1,
        "emailAddress": "kimberly.smith@indexexchage.com",
        "points": 0,
        "img": "../../assets/images/kim.png"
    }
]

# /teams
mock_teams_list = [
    {
        "name": "Yay Orange",
        "teamID": 4,
        "team_points": 2
    },
    {
        "name": "Coffee Cat",
        "teamID": 2,
        "team_points": 1
    },
    {
        "name": "Party Parrot",
        "teamID": 1,
        "team_points": 0
    },
    {
        "name": "Dancing Banana",
        "teamID": 3,
        "team_points": 0 
    },
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