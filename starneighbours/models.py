"""
.. module:: models
   :platform: Unix, Windows
   :synopsis: The module provide the different pydantic models

.. moduleauthor:: Thibaut Stalin <thibaut.st@gmail.com>
"""

from pydantic import BaseModel


class Rate(BaseModel):
    """
    Rate pydantic model ("rate" subpart of GitHub "/rate_limit" response data)
    """

    limit: int
    used: int
    remaining: int
    reset: int


class RateLimit(BaseModel):
    """
    RateLimit pydantic model (partially match GitHub "/rate_limit" response data)
    """

    rate: Rate


class Starneighbour(BaseModel):
    """
    Starneighbour pydantic model
    """

    repo: str
    stargazers: list[str]


class Stargazer(BaseModel):
    """
    Stargazer pydantic model (partially match GitHub "/repos/{owner}/{repo}/stargazers" response data)
    """

    id: int
    login: str


class Starred(BaseModel):
    """
    Starred pydantic model (partially match GitHub "/users/{username}/starred" response data)
    """

    id: int
    name: str
    full_name: str
