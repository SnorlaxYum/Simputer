title: Git Notes - Submodule && detached HEAD
date: 2019-11-17 20:49
modified: 2019-11-22 13:56
author: Sim
tags: git, detached HEAD, submodule
summary: The solution about forgetting to add submodule and detached HEAD.

## When I forget to add submodule

I moved my `media` directory to the project as well, since it's a git project I have to add it as a `git submodule add`, however I forgot to do so and did `git add .` instead, so on my earlier commit, the folder is shown as a text on Github.  

Solution[^1]:  

1. Unstage it

        $ git rm --cached media

2. Add it in a correct way

        $ git submodule add url_to_repo media

## Detached HEAD

My git in `media` directory somehow got a detached state:  

```
$ git commit -m "aaa"
HEAD detached from 8799335
```

To fix that[^2] and merge the untracked changes, so I need to checkout the corresponding branch:  

```
$ git checkout master
```

Then it shows the log:  

```
Warning: you are leaving 4 commits behind, not connected to
any of your branches:

  69c7986 yEd try
  7f5f6d2 new pics
  eb3656a new pic
  19a5966 2 new pics

If you want to keep them by creating a new branch, this may be a good time
to do so with:

git branch <new-branch-name> 69c7986

Switched to branch 'master'
```

Then follow the instruction and push:  

```
$ git branch tmp 69c7986
$ git push origin master
```

[^1]: [Issue with adding common code as git submodule: "already exists in the index" - Stack Overflow](https://stackoverflow.com/a/12902857)
[^2]: [Fix a Git detached head? - Stack Overflow](https://stackoverflow.com/a/10229202/9850945)