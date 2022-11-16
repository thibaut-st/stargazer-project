"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: The module provide the fastapi controller with the security and the routes

.. moduleauthor:: Thibaut Stalin <thibaut.st@gmail.com>
"""

from typing import Optional

from fastapi import Depends, FastAPI, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from starneighbours.business import GitHubBusiness
from starneighbours.database import FAKE_DB
from starneighbours.models import RateLimit, Starneighbour

app = FastAPI()

SECRET = "z%CbkT2@r9kc4&OG"
manager = LoginManager(SECRET, "/login")


@manager.user_loader()  # type: ignore
def _query_user(user_id: str) -> Optional[dict[str, str]]:
    """
    Get a user from the db

    :param user_id: Email of the user
    :return: None or the user object
    """
    return FAKE_DB["users"].get(user_id)


@app.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """
    Get an access token from a username/password combination

    :param data: Username and password
    :return: The generated access token
    """
    email = data.username
    password = data.password

    user = _query_user(email)
    if not user:
        raise InvalidCredentialsException
    if password != user["password"]:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": email})
    return {"access_token": access_token}


@app.get("/rate")
async def get_rate_limit() -> RateLimit:
    """
    Return the REST api request rate limit from GitHub

    :return: The rate limit details
    """
    return await GitHubBusiness.get_rate_limit()


@app.get("/repos/{user}/{repo}/starneighbours", dependencies=[Depends(manager)])
async def get_starneighbours(
    user: str,
    repo: str,
    per_page: int = Query(default=30, gt=0, le=100),
    page: int = Query(default=1, ge=1),
) -> list[Starneighbour]:
    """
    Get the list of neighbours repositories of a GitHub repository

    :param user: The username of the repository's owner
    :param repo: The repository's name to check
    :param per_page: The number of stargazers for the repository per page
    :param page: Page number of the result to fetch
    :return: The list of neighbours repositories and common stargazers from the given repository
        (i.e. [
                {"repo": <repoA>, "stargazers": [<stargazers in common>, ...],},
                {"repo": <repoB>, "stargazers": [<stargazers in common>, ...],},
                ...
            ])
    """
    stargazers = await GitHubBusiness.get_stargazers(user, repo, per_page, page)
    starneighbours = await GitHubBusiness.get_starneighbours(stargazers, repo)

    return starneighbours
