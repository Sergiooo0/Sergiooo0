import os
import requests

# GitHub API endpoint for GraphQL
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# Your GitHub token
TOKEN = os.getenv("GITHUB_TOKEN")

# GraphQL query
query = """
{
  viewer {
    repositoriesContributedTo(first: 100, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
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


def run_query(query, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(GITHUB_GRAPHQL_URL, json={"query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Query failed with status code {response.status_code}: {response.text}"
        )


try:
    result = run_query(query, TOKEN)
    # Pretty-print the result
    print("Repositories Contributed To:")
    for repo in result["data"]["viewer"]["repositoriesContributedTo"]["nodes"]:
        print(repo["nameWithOwner"])
except Exception as e:
    print(e)
