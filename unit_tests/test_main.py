"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: The module test the fastapi controller and routes

.. moduleauthor:: Thibaut Stalin <thibaut.st@gmail.com>
"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from main import app
from starneighbours.business import GitHubBusiness
from starneighbours.models import RateLimit

client = TestClient(app)


class TestGitHubBusiness(IsolatedAsyncioTestCase):
    """
    Test the Fastapi main routes
    """

    # RATE_LIMIT DATA
    mock_rate_limit = {
        "rate": {"limit": 5000, "remaining": 4999, "reset": 1372700873, "used": 1},
    }

    # STARRED DATA
    mock_starred_list = [
        {
            "id": 1296270,
            "name": "repository_name",
            "full_name": "octocat/repository_name",
        },
        {
            "id": 1296269,
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
        },
    ]
    mock_stargazer_list = [
        {
            "login": "octocat",
            "id": 1,
        }
    ]

    @patch.object(GitHubBusiness, "_github_http_get", return_value=mock_rate_limit)
    async def test_login_ok(self, _: Mock) -> None:
        """
        Test login at "/login"
        """
        # DATA
        response = client.post("/login", data={"username": "thibaut.st@gmail.com", "password": "admin"})

        # ASSERT
        self.assertEqual(200, response.status_code)
        self.assertIn("access_token", response.json())
        self.assertEqual(144, len(response.json()["access_token"]))

    @patch.object(GitHubBusiness, "_github_http_get", return_value=mock_rate_limit)
    async def test_login_ko(self, _: Mock) -> None:
        """
        Test login at "/login"
        """
        # DATA
        response_wrong_user = client.post("/login", data={"username": "wrong_user", "password": "admin"})
        response_wrong_password = client.post(
            "/login", data={"username": "thibaut.st@gmail.com", "password": "wrong_password"}
        )

        # ASSERT
        self.assertEqual(401, response_wrong_user.status_code)
        self.assertEqual(401, response_wrong_password.status_code)

    @patch.object(GitHubBusiness, "_github_http_get", return_value=mock_rate_limit)
    async def test_get_rate_limit(self, _: Mock) -> None:
        """
        Test get_rate_limit at "/rate"
        """
        # DATA
        response = client.get("/rate")
        expected_result = RateLimit(**self.mock_rate_limit)

        # ASSERT
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_result, response.json())

    @patch.object(GitHubBusiness, "_github_http_get", side_effect=[mock_stargazer_list, mock_starred_list])
    async def test_get_starneighbours(self, _: Mock) -> None:
        """
        Test get_starneighbours at "/repos/{user}/{repo}/starneighbours"
        """
        # DATA
        user = "username"
        repo = "repository_name"
        response_login = client.post("/login", data={"username": "thibaut.st@gmail.com", "password": "admin"})
        token = response_login.json()["access_token"]

        response = client.get(
            f"/repos/{user}/{repo}/starneighbours",
            headers={"Authorization": f"Bearer {token}"},
        )
        expected_result = [{"repo": "Hello-World", "stargazers": ["octocat"]}]

        # ASSERT
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_result, response.json())
