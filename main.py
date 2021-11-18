import requests
from typing import List
import subprocess
from pprint import pprint
import os
import random
import logging

logger = logging.getLogger(__name__)


class GithubInteractor:
    """
    https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api

    Endpoints Docs:
    https://docs.github.com/en/rest/overview/endpoints-available-for-github-apps
    """

    def __init__(self):

        # githbub -> settings -> developer settings -> personal access tokens (PAT)
        auth_token = "TOKEN HERE"

        auth_username = "aled1027"
        self.auth = (auth_username, auth_token)

        self.base_url = "https://api.github.com"
        self.repo_owner = auth_username
        self.repo_name = "api_test_repo"

    def make_issue(self):
        url = os.path.join(
            self.base_url, "repos", self.repo_owner, self.repo_name, "issues"
        )
        r = random.randint(0, 1000)
        body = {
            "title": f"Issue Title {r}",
            "body": "Body  of the issue"
        }

        res = requests.post(url, auth=self.auth, json=body)
        logger.debug(f"Response from making issue: {res.text}")

        if not res.ok:
            logger.error("Error making github issue")
            raise RuntimeError("Issue with request")

        response_data = res.json()

        issue_num = response_data["number"]
        logger.debug(f"Num from created issue: {issue_num}")

        return issue_num

    def add_assignees_to_issue(self, issue_num: int, assignees: List[str]):
        """
        Adds assignees to an existing github issue

        issue_url should be the URL of an existing github issue, like:
        "https://github.com/aled1027/api_test_repo/issues/2".
        and assignees should be list of strings, where each string is a github
        user like ["aled1027"].
        """
        #

        url = os.path.join(
            self.base_url, "repos", self.repo_owner,
            self.repo_name, "issues", str(issue_num)
        )

        body = {
            "assignees": assignees
        }

        res = requests.patch(url, auth=self.auth, json=body)
        logger.debug(f"Response from adding assignees to githubb issue: {res.text}")

        if not res.ok:
            logger.error("Error adding assignees to github issue")
            raise RuntimeError("Issue with adding assignees to github issue")

    def mock_dev_work(self, work_id):
        # makes a new branch and pushes a commit with a small change
        subprocess.run(["./dev_work.sh", str(work_id)])

        # and make the pull request with http
        # https://docs.github.com/en/rest/reference/pulls#create-a-pull-request
        url = os.path.join(
            self.base_url, "repos", self.repo_owner, self.repo_name, "pulls"
        )

        branch = f"feature/number_{work_id}"
        body = {
            "head": branch,
            "base": "main",
            "issue": work_id
        }
        res = requests.post(url, auth=self.auth, json=body)
        logger.debug(f"Response from making pr: {res.text}")

        if not res.ok:
            logger.error("Error making PR")
            raise RuntimeError("Issue with making PR")


def go() -> None:
    gi = GithubInteractor()

    issue_num = gi.make_issue()

    assignnees = ["aled1027"]
    gi.add_assignees_to_issue(issue_num, assignnees)

    # offline, suppose branch and commits
    gi.mock_dev_work(issue_num)



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        # filename=f"{log_directory}/logs_{log_datetime}.log",
        format='%(asctime)s,%(msecs)03d %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    go()
