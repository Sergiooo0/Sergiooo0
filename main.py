import githubInfo

markDown = f"""## <img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="25"><b> Github Stats </b>

<p align="center">
<a href="https://github.com/{githubInfo.AUTHOR}">
  <img width="600px" src="https://github-readme-stats-liard-nu-21.vercel.app/api?username={githubInfo.AUTHOR}&show_icons=true&hide_title=true&show=reviews,prs_merged&include_all_commits=true" alt="GitHub Stats"/>
  <img width="600px" src="https://github-readme-stats-liard-nu-21.vercel.app/api/top-langs/?username={githubInfo.AUTHOR}&show_icons=true"/>
  
</a>
</p>
"""


if __name__ == "__main__":
    print(githubInfo.getRepositoriesWithCommits())

    print(f"Number of API calls: {githubInfo.NUMBERCALLSAPI}")
    print(f"Number of normal calls: {githubInfo.NUMBERCALLSNORMAL}")

    # Now we will write the markdown to README.md
    with open("README.md", "w") as file:
        file.write(markDown)
