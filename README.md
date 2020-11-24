# team-snitch-hackathon
A Hogwarts House Cup App for Slack

# Run the entire application end-to-end:
- `docker-compose up -d`

# Running the backend:
- `cd api && pip3 install pipenv`
- `pipenv install`
- `pipenv shell`
- `python3 app.py`

# Running the backend with Docker:
- `cd api && docker build -t api .`
- `docker run api -d`

# Running the frontend with Docker (without APIs)
- `docker-compose up --build -d leaderboard-ui`
