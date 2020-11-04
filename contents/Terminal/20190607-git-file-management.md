---
title: Git - An Excellent File Transferer
date: 2019-06-07 22:08
modified: 2019-07-31 18:28
author: Sim
tags: git, file, ssh
summary: I recently found that git is an excellent file transferer.  
---

I did migration of my site from firebase to my server. And then I found out that git is far more better than scp. Normally scp transfer files one by one to the server, while git glues all files together, speeding up the process. Afterwards, the version control will take care of the changes of the whole git project and only process the changes to the server.  

I did through the official guide 4.3[^1] and 4.4[^2] and created a user `git` for doing git.  

However doing without a git account is also possible.  

## Working with a remote

Generate my own SSH public key on my local computer:

    :::bash
    $ ssh-keygen

Upload my ~/.ssh/id_rsa.pub to somewhere on the server:  

    :::bash
    sim@localhost:~$ scp -P port ~/.ssh/id_rsa.pub sim@server:/home/sim/id_rsa.sim.pub

On the server in the home, make dir for ssh if `.ssh` hasn't been created:  

    :::bash
    sim@server:~$ mkdir .ssh

append the key to `authorized_keys`:  

    :::bash
    sim@server:~$ cat id_rsa.sim.pub >> .ssh/authorized_keys

Initialize a new dir for new git project:  

    :::bash
    sim@server:~$ git init --bare new_dir.git

On my local computer:  

    :::bash
    sim@localhost:~$ cd project
    sim@localhost:~/project$ git init && git add . && git commit -m "initial commit" && git remote add origin ssh://sim@server:port/home/sim/new_dir.git && git push origin master

Then on the server, I can do this:  

    :::bash
    sim@server:~$ git clone ~/new_dir.git ~/new_dir

`new_dir` is a new dir with all files checked out from the git project `new_dir.git` and the git settings.  

I could create `~/new_dir.git/hooks/post-receive`:  

    #!/bin/sh
    cd /home/sim/new_dir || exit
    unset GIT_DIR
    git pull origin master

The `unset` is needed 'cause git uses the variable `GIT_DIR` instead of `PWD`, `cd` changes `PWD` instead of `GIT_DIR`. There must be a fallback from `GIT_DIR` to `PWD`[^3].

Make it executable:  

    :::bash
    sim@server:~$ chmod +x ~/new_dir.git/hooks/post-receive

Everytime I need update files on the server, I could do it via a bash:  

    #!/bin/bash
    cd /home/sim/project
    echo -n "Enter the commit message: "
    read message
    git add .
    git commit -m "${message}"
    git push origin master

Then everytime I push to the git project, the `new_dir` will be also updated with new contents.

## Working with multiple remotes

Sometimes I need to work with serveral remotes, for example, I need to upload to multiple servers, then I have to do some extra things.  

Upload my ~/.ssh/id_rsa.pub to somewhere on another server:  

    :::bash
    sim@localhost:~$ scp -P port ~/.ssh/id_rsa.pub sim@server2:/home/sim/id_rsa.sim.pub

On the server in the home, make dir for ssh if `.ssh` hasn't been created:  

    :::bash
    sim@server2:~$ mkdir .ssh

Append the key to `authorized_keys`:  

    :::bash
    sim@server2:~$ cat id_rsa.sim.pub >> .ssh/authorized_keys

Initialize a new dir for new git project:  

    :::bash
    sim@server2:~$ git init --bare new_dir.git

On my local computer:  

    :::bash
    sim@localhost:~$ cd project
    sim@localhost:~/project$ git remote add origin2 ssh://sim@server2:port/home/sim/new_dir.git
    sim@localhost:~/project$ git push origin2 master

Then on the server, I can do this:  

    :::bash
    sim@server2:~$ git clone ~/new_dir.git ~/new_dir

`new_dir` is a new dir with all files checked out from the git project `new_dir.git` and the git settings.  

I could create `~/new_dir.git/hooks/post-receive`:  

    :::sh
    #!/bin/sh
    cd /home/sim/new_dir || exit
    unset GIT_DIR
    git stash
    git pull origin master

Make it executable:  

    :::bash
    sim@server2:~$ chmod +x ~/new_dir.git/hooks/post-receive

Everytime I need update files on both servers, I could do it via a bash:  

    :::bash
    #!/bin/bash
    cd /home/sim/project
    echo -n "Enter the commit message: "
    read message
    git add .
    git commit -m "${message}"
    git push origin master
    git push origin2 master

Then everytime I push to both git projects, the `new_dir` on both servers will be also updated with new contents.  

[^1]: [Git - Generating Your SSH Public Key](https://git-scm.com/book/en/v2/Git-on-the-Server-Generating-Your-SSH-Public-Key)
[^2]: [Git - Setting Up the Server](https://git-scm.com/book/en/v2/Git-on-the-Server-Setting-Up-the-Server)
[^3]: [githooks - getting "fatal: not a git repository: '.'" when using post-update hook to execute 'git pull' on another repo - Stack Overflow](https://stackoverflow.com/a/4100577/9850945)
