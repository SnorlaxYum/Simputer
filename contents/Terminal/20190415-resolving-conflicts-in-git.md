---
title: Resolving Conflicts in Git
date: 2019-04-15 20:46
author: Sim
tags: git, Conflicts
summary: Recently when I was working with my branch of isso, I found a conflict on a file. Easy to resolve but kinda important for my future work with git.  
---

First add the upstream remote then fetch it. [^1]  

	:::bash
	git remote add upstream https://repoA
	git fetch upstream

Check out the branch (in this case, `notification`) and auto-merge it with the upstream master. [^1]

	:::bash
	git checkout notification
	git merge upstream/master

[^1]: [How to solve merge conflicts across forks? - stackoverflow](https://stackoverflow.com/a/38955036/9850945)

Resolve the conflicts by fully accept my or their version[^2]:  

Accept my version (local, ours):  

	:::bash
	git checkout --ours -- [filename]
	git add [filename]
	git commit -m "merged bla bla"

Accept their version (remote, theirs):  

	:::bash
	git checkout --theirs -- [filename]
	git add [filename]
	git commit -m "merged bla bla"

Do __all conflict files__ with either mine or theirs:  

	:::bash
	git merge --strategy-option ours

or  

	:::bash
	git merge --strategy-option theirs

[^2]: [How to resolve merge conflicts in Git - stackoverflow](https://stackoverflow.com/a/39771096/9850945)
