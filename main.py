import requests

AUTHOR = "SantiagoRR2004"


def getCommitCount(repository: str) -> int:
    """
    Get the commit count for the specified author in the repository.

    Args:
        - repository (str): The repository name.
            It needs to be in the format "owner/repo".

    Returns:
        - int: The number of commits by the author.
    """
    commitCount = 0

    # GitHub API URL for commits
    url = f"https://api.github.com/repos/{repository}/commits"

    # Set the parameters for the API request
    params = {
        "author": AUTHOR,
        "per_page": 100,  # Adjust this to get more commits per request (max 100)
    }

    page = 1

    continueFetching = True

    while continueFetching:
        params["page"] = page
        response = requests.get(url, params=params)

        if response.status_code == 200:
            commits = response.json()

            if not commits:  # No more commits
                continueFetching = False

            else:
                commitCount += len(commits)
                page += 1

        else:
            print("Error fetching commits:", response.status_code)
            continueFetching = False

    return commitCount
