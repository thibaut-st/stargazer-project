"""
.. module:: test_business
   :platform: Unix, Windows
   :synopsis: The module test the business classes

.. moduleauthor:: Thibaut Stalin <thibaut.st@gmail.com>
"""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch

from pydantic.error_wrappers import ValidationError

from starneighbours.business import GitHubBusiness
from starneighbours.models import RateLimit, Stargazer, Starneighbour


class TestGitHubBusiness(IsolatedAsyncioTestCase):
    """
    Test the GitHubBusiness class
    """

    # RATE_LIMIT DATA
    mock_wrong_rate_data = {"rate": "wrong data"}
    mock_rate_data = {"rate": {"limit": 5000, "remaining": 4999, "reset": 1372700873, "used": 1}}
    mock_rate_limit_data = {
        "resources": {
            "core": {"limit": 5000, "remaining": 4999, "reset": 1372700873, "used": 1},
            "search": {"limit": 30, "remaining": 18, "reset": 1372697452, "used": 12},
            "graphql": {"limit": 5000, "remaining": 4993, "reset": 1372700389, "used": 7},
            "integration_manifest": {"limit": 5000, "remaining": 4999, "reset": 1551806725, "used": 1},
            "code_scanning_upload": {"limit": 500, "remaining": 499, "reset": 1551806725, "used": 1},
        },
        "rate": mock_rate_data["rate"],
    }

    # STARGAZER DATA
    mock_stargazer_list_data = [
        {
            "login": "octocat",
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "",
            "url": "https://api.github.com/users/octocat",
            "html_url": "https://github.com/octocat",
            "followers_url": "https://api.github.com/users/octocat/followers",
            "following_url": "https://api.github.com/users/octocat/following{/other_user}",
            "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
            "organizations_url": "https://api.github.com/users/octocat/orgs",
            "repos_url": "https://api.github.com/users/octocat/repos",
            "events_url": "https://api.github.com/users/octocat/events{/privacy}",
            "received_events_url": "https://api.github.com/users/octocat/received_events",
            "type": "User",
            "site_admin": False,
        }
    ]
    mock_wrong_stargazer_list_data = [
        {
            "login": "octocat",
        }
    ]
    mock_stargazer_list = [Stargazer(**mock_stargazer_list_data[0])]

    # STARRED DATA
    mock_stargazer_list_for_starred = [Stargazer(login="octocat", id=1), Stargazer(login="octopus", id=2)]
    mock_starred_list_data = [
        {
            "id": 1296270,
            "name": "repository_name",
            "full_name": "octocat/repository_name",
        },
        {
            "id": 1296269,
            "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "owner": {
                "login": "octocat",
                "id": 1,
                "node_id": "MDQ6VXNlcjE=",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                "gravatar_id": "",
                "url": "https://api.github.com/users/octocat",
                "html_url": "https://github.com/octocat",
                "followers_url": "https://api.github.com/users/octocat/followers",
                "following_url": "https://api.github.com/users/octocat/following{/other_user}",
                "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
                "organizations_url": "https://api.github.com/users/octocat/orgs",
                "repos_url": "https://api.github.com/users/octocat/repos",
                "events_url": "https://api.github.com/users/octocat/events{/privacy}",
                "received_events_url": "https://api.github.com/users/octocat/received_events",
                "type": "User",
                "site_admin": False,
            },
            "private": False,
            "html_url": "https://github.com/octocat/Hello-World",
            "description": "This your first repo!",
            "fork": False,
            "url": "https://api.github.com/repos/octocat/Hello-World",
            "archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
            "assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
            "blobs_url": "https://api.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
            "branches_url": "https://api.github.com/repos/octocat/Hello-World/branches{/branch}",
            "collaborators_url": "https://api.github.com/repos/octocat/Hello-World/collaborators{/collaborator}",
            "comments_url": "https://api.github.com/repos/octocat/Hello-World/comments{/number}",
            "commits_url": "https://api.github.com/repos/octocat/Hello-World/commits{/sha}",
            "compare_url": "https://api.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
            "contents_url": "https://api.github.com/repos/octocat/Hello-World/contents/{+path}",
            "contributors_url": "https://api.github.com/repos/octocat/Hello-World/contributors",
            "deployments_url": "https://api.github.com/repos/octocat/Hello-World/deployments",
            "downloads_url": "https://api.github.com/repos/octocat/Hello-World/downloads",
            "events_url": "https://api.github.com/repos/octocat/Hello-World/events",
            "forks_url": "https://api.github.com/repos/octocat/Hello-World/forks",
            "git_commits_url": "https://api.github.com/repos/octocat/Hello-World/git/commits{/sha}",
            "git_refs_url": "https://api.github.com/repos/octocat/Hello-World/git/refs{/sha}",
            "git_tags_url": "https://api.github.com/repos/octocat/Hello-World/git/tags{/sha}",
            "git_url": "git:github.com/octocat/Hello-World.git",
            "issue_comment_url": "https://api.github.com/repos/octocat/Hello-World/issues/comments{/number}",
            "issue_events_url": "https://api.github.com/repos/octocat/Hello-World/issues/events{/number}",
            "issues_url": "https://api.github.com/repos/octocat/Hello-World/issues{/number}",
            "keys_url": "https://api.github.com/repos/octocat/Hello-World/keys{/key_id}",
            "labels_url": "https://api.github.com/repos/octocat/Hello-World/labels{/name}",
            "languages_url": "https://api.github.com/repos/octocat/Hello-World/languages",
            "merges_url": "https://api.github.com/repos/octocat/Hello-World/merges",
            "milestones_url": "https://api.github.com/repos/octocat/Hello-World/milestones{/number}",
            "notifications_url": "https://api.github.com/repos/octocat/Hello-World/"
            "notifications{?since,all,participating}",
            "pulls_url": "https://api.github.com/repos/octocat/Hello-World/pulls{/number}",
            "releases_url": "https://api.github.com/repos/octocat/Hello-World/releases{/id}",
            "ssh_url": "git@github.com:octocat/Hello-World.git",
            "stargazers_url": "https://api.github.com/repos/octocat/Hello-World/stargazers",
            "statuses_url": "https://api.github.com/repos/octocat/Hello-World/statuses/{sha}",
            "subscribers_url": "https://api.github.com/repos/octocat/Hello-World/subscribers",
            "subscription_url": "https://api.github.com/repos/octocat/Hello-World/subscription",
            "tags_url": "https://api.github.com/repos/octocat/Hello-World/tags",
            "teams_url": "https://api.github.com/repos/octocat/Hello-World/teams",
            "trees_url": "https://api.github.com/repos/octocat/Hello-World/git/trees{/sha}",
            "clone_url": "https://github.com/octocat/Hello-World.git",
            "mirror_url": "git:git.example.com/octocat/Hello-World",
            "hooks_url": "https://api.github.com/repos/octocat/Hello-World/hooks",
            "svn_url": "https://svn.github.com/octocat/Hello-World",
            "homepage": "https://github.com",
            "language": None,
            "forks_count": 9,
            "stargazers_count": 80,
            "watchers_count": 80,
            "size": 108,
            "default_branch": "master",
            "open_issues_count": 0,
            "is_template": True,
            "topics": ["octocat", "atom", "electron", "api"],
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True,
            "has_pages": False,
            "has_downloads": True,
            "archived": False,
            "disabled": False,
            "visibility": "public",
            "pushed_at": "2011-01-26T19:06:43Z",
            "created_at": "2011-01-26T19:01:12Z",
            "updated_at": "2011-01-26T19:14:43Z",
            "permissions": {"admin": False, "push": False, "pull": True},
            "allow_rebase_merge": True,
            "template_repository": None,
            "temp_clone_token": "ABTLWHOULUVAXGTRYU7OC2876QJ2O",
            "allow_squash_merge": True,
            "allow_auto_merge": False,
            "delete_branch_on_merge": True,
            "allow_merge_commit": True,
            "subscribers_count": 42,
            "network_count": 0,
            "license": {
                "key": "mit",
                "name": "MIT License",
                "url": "https://api.github.com/licenses/mit",
                "spdx_id": "MIT",
                "node_id": "MDc6TGljZW5zZW1pdA==",
                "html_url": "https://github.com/licenses/mit",
            },
            "forks": 1,
            "open_issues": 1,
            "watchers": 1,
        },
    ]
    mock_wrong_starred_list_data = [
        {
            "id": 1296270,
            "full_name": "octocat/repository_name",
        },
    ]

    @patch.object(GitHubBusiness, "_github_http_get", return_value=mock_rate_limit_data)
    async def test_get_rate_limit_ok(self, mock__github_http_get: Mock) -> None:
        """
        Test get_rate_limit method should succeed
        """
        # DATA
        result = await GitHubBusiness.get_rate_limit()
        expected_result = RateLimit(**self.mock_rate_data)

        # ASSERT
        mock__github_http_get.assert_called_once()
        self.assertEqual(expected_result, result)

    @patch.object(GitHubBusiness, "_github_http_get", return_value=mock_wrong_rate_data)
    async def test_get_rate_limit_ko(self, _: Mock) -> None:
        """
        Test get_rate_limit method should raise
        """
        # ASSERT
        with self.assertRaises(ValidationError):
            await GitHubBusiness.get_rate_limit()

    @patch.object(GitHubBusiness, "_github_http_get", return_value=mock_stargazer_list_data)
    async def test_get_stargazers_ok(self, mock__github_http_get: Mock) -> None:
        """
        Test get_stargazers method should succeed
        """
        # DATA
        result = await GitHubBusiness.get_stargazers("username", "repository_name", 30, 1)

        # ASSERT
        mock__github_http_get.assert_called_once()
        self.assertEqual(self.mock_stargazer_list, result)

    @patch.object(GitHubBusiness, "_github_http_get", return_value=mock_wrong_stargazer_list_data)
    async def test_get_stargazers_ko(self, _: Mock) -> None:
        """
        Test get_stargazers method should raise
        """
        # ASSERT
        with self.assertRaises(ValidationError):
            await GitHubBusiness.get_stargazers("username", "repository_name", 30, 1)

    @patch.object(GitHubBusiness, "_github_http_get", return_value=mock_starred_list_data)
    async def test_get_starneighbours_ok(self, mock__github_http_get: Mock) -> None:
        """
        Test get_starneighbours method should succeed
        """
        # DATA
        result = await GitHubBusiness.get_starneighbours(self.mock_stargazer_list_for_starred, "repository_name")
        expected_result = [Starneighbour(repo="Hello-World", stargazers=["octocat", "octopus"])]

        # ASSERT
        mock__github_http_get.assert_called()
        self.assertEqual(expected_result, result)

    @patch.object(GitHubBusiness, "_github_http_get", return_value=mock_wrong_starred_list_data)
    async def test_get_starneighbours_ko(self, _: Mock) -> None:
        """
        Test get_starneighbours method should raise
        """
        # ASSERT
        with self.assertRaises(ValidationError):
            await GitHubBusiness.get_starneighbours(self.mock_stargazer_list, "repository_name")
