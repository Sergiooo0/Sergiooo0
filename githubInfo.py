import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import tqdm

TOKEN = os.getenv("GITHUB_TOKEN")

NUMBERCALLSAPI = 0
NUMBERCALLSNORMAL = 0
NUMBERCALLSGRAPHQL = 0
BASE = "https://github.com/"
GITHUBGRAPHQLURL = "https://api.github.com/graphql"

if os.getenv("REPO_OWNER"):
    AUTHOR = os.getenv("REPO_OWNER")
else:
    AUTHOR = "Sergiooo0"


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
    global NUMBERCALLSAPI

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
        NUMBERCALLSAPI += 1

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


def getListOfRepositories() -> list:
    """
    Get the list of repositories from the user.

    It will return the in the format "owner/repo".

    Args:
        - None

    Returns:
        - list: The list of repositories.
    """
    repositories = set()

    repositories.update(set(getStoredRepositories()))

    repositories.update(set(getOwnedRepositories()))

    repositories.update(set(getRepositoriesWithGraphQL()))

    # We eliminate the None if it exists
    repositories.discard(None)

    return list(repositories)


def getStoredRepositories() -> list:
    """
    Get the list of stored repositories.

    The stored repositories are stored as their ids
    so they are converted to the "owner/repo" format.

    The list is empty so forks don't add my repositories.

    Args:
        - None

    Returns:
        - list: The list of stored repositories.
    """
    ids = [
        # 707606529
    ]

    repositories = []

    for id in ids:
        repository = getRepositoryFromID(id)
        repositories.append(repository)

    return repositories


def getRepositoryFromID(id: int) -> str:
    """
    Get the repository name from the ID.

    Args:
        - id (int): The repository ID.

    Returns:
        - str: The repository name.
    """
    url = f"https://api.github.com/repositories/{id}"

    response = requests.get(url)
    global NUMBERCALLSAPI
    NUMBERCALLSAPI += 1

    if response.status_code == 200:
        repository = response.json()
        return repository["full_name"]


def getOwnedRepositories() -> list:
    """
    Get my repositories

    It will return them in the format:
        - "owner/repo"

    Args:
        - None

    Returns:
        - list: The list of URLs for the repositories.
    """
    global NUMBERCALLSNORMAL
    url = f"{urljoin(BASE,AUTHOR)}?tab=repositories"

    repositories = []

    while url:
        response = requests.get(url)
        NUMBERCALLSNORMAL += 1

        soup = BeautifulSoup(response.text, "html.parser")

        # Get the repositories
        repoBlocks = soup.find_all("h3", class_="wb-break-all")

        # Extract the url of the repositories
        for repo in repoBlocks:
            if repo.find("a"):
                repositories.append(urljoin(f"{AUTHOR}/", repo.find("a").text))

        # Find the 'Next' button link to go to the next page of repositories
        next_page = soup.find("a", string="Next")

        if next_page:
            # If there is a 'Next' link, update the URL to the next page
            url = urljoin(BASE, next_page["href"])
        else:
            # No more pages, break the loop
            url = None

    return repositories


def getRepositoriesWithCommits() -> dict:
    """
    Get the repositories with the number of commits by the author.

    Args:
        - None

    Returns:
        - dict: The repositories with the number of commits.
    """
    repositories = getListOfRepositories()

    repositoriesWithCommits = {}

    for repository in tqdm.tqdm(repositories, total=len(repositories), desc="Commit count"):
        commitCount = getCommitCount(repository)
        repositoriesWithCommits[urljoin(BASE, repository)] = commitCount

    return repositoriesWithCommits


def runQuery(query: str, token: str) -> dict:
    """
    Run a query using the GitHub GraphQL API.

    Args:
        - query (str): The query to run.
        - token (str): The GitHub token.

    Returns:
        - dict: The response from the API.
    """
    global NUMBERCALLSGRAPHQL
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(GITHUBGRAPHQLURL, json={"query": query}, headers=headers)
    NUMBERCALLSGRAPHQL += 1

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Query failed with status code {response.status_code}: {response.text}")

    return None

def getRepositoriesWithGraphQL() -> list:
    """
    Get the repositories by the author using GraphQL.
    It doesn't return the repositories that he owns.

    The query is based on the following StackOverflow answer:
    https://stackoverflow.com/questions/20714593/github-api-repositories-contributed-to

    Example:
        {
            "data": {
                "user": {
                    "login": "SantiagoRR2004",
                    "repositoriesContributedTo": {
                        "totalCount": 5,
                        "nodes": [
                            {"nameWithOwner": "hsahovic/poke-env"},
                            {"nameWithOwner": "santipvz/PRO_I-Chatbot"},
                            {"nameWithOwner": "LucachuTW/IS-Grupo301"},
                            {"nameWithOwner": "esei-si-dagss/tasador-24"},
                            {"nameWithOwner": "LucachuTW/CARDS-PokemonPocket-scrapper"},
                        ],
                        "pageInfo": {
                            "endCursor": "Y3Vyc29yOnYyOpHONNz90g==",
                            "hasNextPage": False,
                        },
                    },
                }
            }
        }

    Args:
        - None

    Returns:
        - list: The list of repositories.
    """
    # GraphQL query
    queryTemplate = """
    {
    user(login: "{login}") {
        login
        repositoriesContributedTo(first: 100, after: {cursor}, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
        totalCount
        nodes {
            nameWithOwner
        }
        pageInfo {
            endCursor
            hasNextPage
        }
        }
    }
    }
    """

    queryTemplate = queryTemplate.replace("{login}", AUTHOR)

    cursor = "null"
    repositories = []

    while True:
        query = queryTemplate.replace(
            "{cursor}", f'"{cursor}"' if cursor != "null" else "null"
        )
        result = runQuery(query, TOKEN)
        if result:
            data = result["data"]["user"]["repositoriesContributedTo"]

            for repo in data["nodes"]:
                repositories.append(repo["nameWithOwner"])

            if not data["pageInfo"]["hasNextPage"]:
                break

            cursor = data["pageInfo"]["endCursor"]
        else:
            break

    return repositories
