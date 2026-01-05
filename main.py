import githubInfo
import json
import os


def formatBytes(num: int) -> str:
    """
    Format bytes as human-readable text.

    Args:
        - num (int): The number of bytes.

    Returns:
        - str: The formatted string.
    """
    for unit in ["B", "kB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} PB"


markDown = f"""# [{githubInfo.AUTHOR}](https://{githubInfo.AUTHOR}.github.io/)

## <a href="https://{githubInfo.AUTHOR}.github.io/"><img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="25" alt=""></a> <b> Github Stats </b>

<p align="center">
  <a href="https://{githubInfo.AUTHOR}.github.io/">
    <img
      width="600px"
      src="https://github-readme-stats-liard-nu-21.vercel.app/api?username={githubInfo.AUTHOR}&show_icons=true&hide_title=true&show=reviews,prs_merged&include_all_commits=true"
      alt="GitHub Stats"
      />
  </a>
</p>
"""


if __name__ == "__main__":
    repositories = githubInfo.getRepositoriesInformation()

    # We order the repositories by the number of commits in descending order
    # And in case of a tie, we order them alphabetically
    repositories = dict(
        sorted(
            repositories.items(),
            key=lambda item: (-item[1]["userCommits"], item[0]),
            reverse=False,
        )
    )

    # We save the repositories information in a json file
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "repositories.json"),
        "w",
    ) as file:
        json.dump(repositories, file, indent=2, ensure_ascii=False)
        file.write("\n")

    print(f"Number of API calls: {githubInfo.NUMBERCALLSAPI}")
    print(f"Number of normal calls: {githubInfo.NUMBERCALLSNORMAL}")
    print(f"Number of GraphQL calls: {githubInfo.NUMBERCALLSGRAPHQL}")

    r"""
    I wanted to put the repository and the commits in the same line.
    I was only able to do this by using a markdown table.
    
    This are other ways I tried to do it:
    
    <p align="left">L</p> <p align="right">R</p>

    $$
    \begin{array}{l r}
    \text{L} \hspace{3cm} \text{R}
    \end{array}
    $$
    """

    # Markdown table with the languages
    languages = {}

    for repoData in repositories.values():
        for lang, bytesCount in repoData["languages"].items():
            languages[lang] = languages.get(lang, 0) + bytesCount

    # Sort by byte count then by language name
    languages = dict(
        sorted(
            languages.items(),
            key=lambda item: (-item[1], item[0]),
            reverse=False,
        )
    )

    totalBytes = sum(languages.values())

    markDownTableLang = """
## Languages

| <img width="1000"><br><p align="center">Language | <img width="1000" height="1"><br><p align="center">Bytes | <img width="1000" height="1"><br><p align="center">Percentage |
|:----------|:----------:|----------:|
"""

    for lang, byteCount in languages.items():
        markDownTableLang += f"| [{lang}](https://github.com/search?q=user:{githubInfo.AUTHOR}+language:{lang}) | {formatBytes(byteCount)} | {byteCount / totalBytes:.2%} |\n"

    # Add the total bytes
    markDownTableLang += (
        f"| Total | {formatBytes(totalBytes)} | {totalBytes / totalBytes:.2%} |\n"
    )

    # We add the languages table to the markdown
    markDown += markDownTableLang

    # The collaborators table
    collaborators = {}

    for repoData in repositories.values():
        for contId, contName in repoData["contributors"].items():
            if contId not in collaborators:
                collaborators[contId] = {"username": contName, "count": 0}

            collaborators[contId]["count"] += 1

    # Sort by number of repositories collaborated on, then by username
    collaborators = dict(
        sorted(
            collaborators.items(),
            key=lambda item: (-item[1]["count"], item[1]["username"]),
            reverse=False,
        )
    )

    markDownTableCollab = """
## Collaborators

| <img width="1000"><br><p align="center">User | <img width="1000" height="1"><br><p align="center">Collaborations |
|:----------|----------:|
"""

    for collabId, collabData in collaborators.items():
        profilePicture = f"<span><a href=\"https://github.com/{collabData['username']}\"><img src=\"https://avatars.githubusercontent.com/u/{collabId}\" style=\"width:1ch;\" alt=\"\"></span>"

        markDownTableCollab += f"| {profilePicture}&ensp;[{collabData['username']}](https://github.com/{collabData['username']})&ensp;{profilePicture} | {collabData['count']} |\n"

    # Add the total number of collaborations
    markDownTableCollab += (
        f"| Total | {sum([data['count'] for data in collaborators.values()])} |\n"
    )

    # We add the collaborators table to the markdown
    markDown += markDownTableCollab

    # Now we make a markdown table with the repositories and the commit count
    markDownTable = """
## Repositories

| <img width="1000"><br><p align="center">Repository | <img width="1000" height="1"><br><p align="center">Commits  |
|:----------|----------:|
"""

    for repository, commitCount in repositories.items():
        repoName = repository[len(githubInfo.BASE) :]

        if repoName.startswith(githubInfo.AUTHOR):
            repoName = repoName[len(githubInfo.AUTHOR) + 1 :]

        markDownTable += (
            f"| [{repoName}]({repository}) | {commitCount["userCommits"]} |\n"
        )

    # Now we add the total number of commits
    markDownTable += (
        f"| Total | {sum([data["userCommits"] for data in repositories.values()])} |\n"
    )

    # We add the table
    markDown += markDownTable

    # Now we will write the markdown to README.md
    with open("README.md", "w") as file:
        file.write(markDown)
