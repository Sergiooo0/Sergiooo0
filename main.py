import githubInfo

markDown = f"""## <img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="25"><b> Github Stats </b>

<p align="center">
  <a href="https://github.com/{githubInfo.AUTHOR}">
    <img
      width="600px"
      src="https://github-readme-stats-liard-nu-21.vercel.app/api?username={githubInfo.AUTHOR}&show_icons=true&hide_title=true&show=reviews,prs_merged&include_all_commits=true"
      alt="GitHub Stats"
      />
    <img
      width="600px"
      src="https://github-readme-stats-liard-nu-21.vercel.app/api/top-langs/?username={githubInfo.AUTHOR}&langs_count=20"
      />
  </a>
</p>
"""


if __name__ == "__main__":
    repositories = githubInfo.getRepositoriesWithCommits()

    # We order the repositories by the number of commits in descending order
    # And in case of a tie, we order them alphabetically
    repositories = dict(
        sorted(
            repositories.items(), key=lambda item: (-item[1], item[0]), reverse=False
        )
    )

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

    # Now we make a markdown table with the repositories and the commit count
    markDownTable = """
| <img width="1000"><br><p align="center">Repository | <img width="1000" height="1"><br><p align="center">Commits  |
|:----------|----------:|
"""

    for repository, commitCount in repositories.items():
        repoName = repository[len(githubInfo.BASE) :]

        if repoName.startswith(githubInfo.AUTHOR):
            repoName = repoName[len(githubInfo.AUTHOR) + 1 :]

        markDownTable += f"| [{repoName}]({repository}) | {commitCount} |\n"

    # Now we add the total number of commits
    markDownTable += f"| Total | {sum(repositories.values())} |\n"

    # We add the table
    markDown += markDownTable

    # # Now we will write the markdown to README.md
    # with open("README.md", "w") as file:
    #     file.write(markDown)

