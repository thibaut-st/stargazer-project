"""
.. module:: business
   :platform: Unix, Windows
   :synopsis: The module provide utility classes (e.g. GitHub requests wrapper)

.. moduleauthor:: Thibaut Stalin <thibaut.st@gmail.com>
"""

from asyncio import ensure_future, gather
from typing import Any

import aiohttp
from aiohttp.client import ClientSession

from starneighbours.models import RateLimit, Stargazer, Starneighbour, Starred

GITHUB_USER = "thibaut-st"
GITHUB_TOKEN = "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"

StarneighbourData = dict[str, list[str]]


class GitHubBusiness:
    """
    GitHubUtils
    """

    @staticmethod
    async def _github_http_get(url: str, session: ClientSession) -> dict[Any, Any]:
        """
        Send a http get request to the given GitHub url

        :param url: The url to request
        :return: The json response as a dict
        """
        async with session.get(url, auth=aiohttp.BasicAuth(GITHUB_USER, GITHUB_TOKEN)) as response:
            return await response.json()  # type: ignore[no-any-return]

    @staticmethod
    async def get_rate_limit() -> RateLimit:
        """
        Return the different rates limit from GitHub

        :return: The rate limit details
            (e.g. {
                  "resources": {
                    "core": {
                      "limit": 5000,
                      "used": 10,
                      "remaining": 4990,
                      "reset": 1668548968
                    },
                    ...
                  },
                  ...
                })
        """
        url_rate_limit = "https://api.github.com/rate_limit"
        async with aiohttp.ClientSession() as session:
            rate_limit_data = await GitHubBusiness._github_http_get(url_rate_limit, session)

        rate_limit = RateLimit(**rate_limit_data)
        return rate_limit

    @staticmethod
    async def get_stargazers(user_name: str, repository_name: str, per_page: int, page: int) -> list[Stargazer]:
        """
        Get the stargazers of the given user's repository

        :param user_name: The username of the repository's owner
        :param repository_name: The repository's name to check
        :return: The list of stargazers
        """
        url_stargazers = (
            f"https://api.github.com/repos/{user_name}/{repository_name}/stargazers?per_page={per_page}&page={page}"
        )
        async with aiohttp.ClientSession() as session:
            stargazer_list_json = await GitHubBusiness._github_http_get(url_stargazers, session)

        stargazers = [Stargazer(**stargazer_json) for stargazer_json in stargazer_list_json]

        return stargazers

    @staticmethod
    async def get_starneighbours(stargazers: list[Stargazer]) -> list[Starneighbour]:
        """
        Get the starneighbours from the given list of stargazers

        :param stargazers: The list of stargazers to check
        :return: The list of starneighbours
            (i.e. [
                {"repo": <repoA>, "stargazers": [<stargazers in common>, ...],},
                {"repo": <repoB>, "stargazers": [<stargazers in common>, ...],},
                ...
            ])
        """
        starneighbours_data: StarneighbourData = {}

        async with aiohttp.ClientSession() as session:
            tasks = []
            for stargazer in stargazers:
                # Create a task pull to speed up the async process
                tasks.append(
                    ensure_future(
                        GitHubBusiness._get_starred_and_format_data(stargazer.login, starneighbours_data, session)
                    )
                )

            await gather(*tasks)

        starneighbours = GitHubBusiness._generate_starneighbours(starneighbours_data)

        return starneighbours

    @staticmethod
    async def _get_starred_and_format_data(
        user_name: str, starneighbours_data: StarneighbourData, session: ClientSession
    ) -> None:
        """
        Request the starred repositories from the given user, and format the data to be handled more easily

        :param user_name: The user to get the starred repositories from
        :param starneighbours_data: A reference to a dictionary that will have the formatted data
        :param session: The aiohttp ClientSession
        """
        starred_list = await GitHubBusiness._get_starred(user_name, session)
        await GitHubBusiness._generate_starneighbours_data(starneighbours_data, user_name, starred_list)

    @staticmethod
    async def _get_starred(user_name: str, session: ClientSession) -> list[Starred]:
        """
        Get the list of starred repositories from a user

        :param user_name: The name of the user to check
        :return: The list of starred repositories
        """
        url_starred = f"https://api.github.com/users/{user_name}/starred"
        starred_list_json = await GitHubBusiness._github_http_get(url_starred, session)

        starred_list = [Starred(**starred_json) for starred_json in starred_list_json]

        return starred_list

    @staticmethod
    async def _generate_starneighbours_data(
        starneighbours_data: StarneighbourData, user_name: str, starred_list: list[Starred]
    ) -> None:
        """
        Generate an easy to deal with data dictionary from user_name and starred_list

        :param starneighbours_data: The reference to the dictionary to update with the formatted data
        :param user_name: The owner's username of the starred repositories
        :param starred_list: The starred repositories
        """
        # Loop through the starred repository of the stargazer
        for starred in starred_list:
            if starred.name not in starneighbours_data:
                # Add the first stargazer if the repository is not added yet
                starneighbours_data[starred.name] = [user_name]
            else:
                if user_name not in starneighbours_data[starred.name]:
                    # Append the new stargazer if not added yet
                    starneighbours_data[starred.name].append(user_name)

    @staticmethod
    def _generate_starneighbours(starneighbours_data: StarneighbourData) -> list[Starneighbour]:
        """
        From the formatted data dictionary, generate a list of Starneighbour objects

        :param starneighbours_data: The formatted data dictionary
        """
        starneighbours: list[Starneighbour] = []
        for repository_name, stargazers_name in starneighbours_data.items():
            starneighbours.append(Starneighbour(repo=repository_name, stargazers=stargazers_name))

        # Sort the list in descending order of repositories with the most common stargazers
        return sorted(starneighbours, key=lambda starneighbour: len(starneighbour.stargazers), reverse=True)
