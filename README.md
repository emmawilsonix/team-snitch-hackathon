# team-snitch-hackathon
A Hogwarts House Cup App for Slack

# Run the entire application end-to-end:
- `docker-compose up -d`

# Running the backend:
- `cd api && pip install pipenv`
- `pipenv install`
- `pipenv shell`
- `python3 app.py`

# Running the backend with Docker:
- `cd api && docker build -t api .`
- `docker run api -d`