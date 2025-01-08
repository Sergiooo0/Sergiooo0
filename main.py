import requests

AUTHOR = "SantiagoRR2004"
NUMBERCALLSAPI = 0


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

    return list(repositories)


def getStoredRepositories() -> list:
    """
    Get the list of stored repositories.

    The stored repositories are stored as their ids
    so they are converted to the "owner/repo" format.

    Args:
        - None

    Returns:
        - list: The list of stored repositories.
    """
    ids = [
        707606529,  # https://github.com/LucachuTW/IS-Grupo301
        886898130,  # https://github.com/LucachuTW/CARDS-PokemonPocket-scrapper
        543282129,  # https://github.com/santipvz/PRO_I-Chatbot
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


