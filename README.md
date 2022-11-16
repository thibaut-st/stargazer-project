# Project Starneighbours

This project allow to get the neighbours of a repository through GitHub.

For more information see https://mergify.notion.site/Stargazer-4cf5427e34a542f0aee4e829bb6d9035

----

# Install

Run "poetry install"

# Usage

To start the API run "python -m uvicorn main:app"
(with "--reload" for hot reload of the project)

Once started, to easily try the application, go to http://127.0.0.1:8000/docs

# Improvement

Ways to improve the application as it is:

## Technical way

- Add functional testing
- Improve the user management system
    - external source authentication
    - or addition of a database + routes to handle the management of users (create/update/delete)
- Move sensible data to environment variable (e.g. secret key)
- Improve the efficiency (need research)

## Functional way

- Allow the user to provide its own GitHub user and token for API requests
- Allow the user to fetch multiple (all) pages for the starneighbours endpoint
- Allow the user to order the starneighbours as he wants
- Add error message if the rate limit of GitHub REST API is met
- Improve documentation (e.g. sphinx)