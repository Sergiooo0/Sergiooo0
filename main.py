import os
import requests

# GitHub API endpoint for GraphQL
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# Your GitHub token
TOKEN = os.getenv("GITHUB_TOKEN")

# GraphQL query
query = """
{
  user(login: "SantiagoRR2004") {
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


def run_query(query, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(GITHUB_GRAPHQL_URL, json={"query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Query failed with status code {response.status_code}: {response.text}"
        )


cursor = "null"
all_repos = []

while True:


    query = query.replace("{cursor}", f'"{cursor}"' if cursor != "null" else "null")
    result = run_query(query, TOKEN)
    data = result['data']['user']['repositoriesContributedTo']
    all_repos.extend(data['nodes'])
    
    if not data['pageInfo']['hasNextPage']:
        break
    
    cursor = data['pageInfo']['endCursor']


    # try:
    #     result = run_query(query, TOKEN)
    #     print(result)
    #     # Pretty-print the result
    #     print("Repositories Contributed To:")
    #     for repo in result["data"]["user"]["repositoriesContributedTo"]["nodes"]:
    #         print(repo["nameWithOwner"])
    #     # print("Authenticated as:", result["data"]["viewer"]["login"])
    # except Exception as e:
    #     print(e)


print(all_repos)