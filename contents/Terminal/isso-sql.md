---
title: Inside The Isso Database
author: Sim
date: 2019-06-10 09:00
tags:
- isso
- sqlite
summary: Of course it's a table with threads and comments
---

<div id="series">
        <p>This post is a part of "<b>My Isso Style</b>" Series.</p>
        <ol class="parts">
					<li>
					<a href="/terminal/2016/07/12/start-to-use-isso/">Installation</a>
					</li>
					<li>
					<a href="/terminal/2019/06/10/my-isso-configuration/">Configuration</a>
					</li>
					<li id="i">
					<b>Inside the Database</b>
					</li>
        </ol>
</div>

## The Tables

Remember the time when the admin interface was not a feature in isso, I submitted two issues in Github: <a href="https://github.com/posativ/isso/issues/264" target="_blank">#264</a>, <a href="https://github.com/posativ/isso/issues/270" target="_blank">#270</a>.  
Now looking back, I think that more and more questions alike could be there without a knowledge for the very database file we r using. Thus it's really important to get into it[^1].  
Switch to a user with enough permission to the sqlite databse file and get into the directory where there's database file:  
```
$ su isso
$ cd ~
```
It's recommended to backup the database before editing:  
```
$ cp comments.db comments.db.bak
```
Now launch the sqlite3 utility.  
```
$ sqlite3
```
Turn the headers on and attach the database to the variable for editing.  

```
sqlite> .headers ON
sqlite> ATTACH 'comments.db' AS isso;
```

List the tables.

```
sqlite> .tables
```

The output are three self-explaining table names:  
```
isso.comments     isso.preferences  isso.threads
```
Check the contents in `isso.comments`:  

```
sqlite> SELECT * FROM isso.comments;
```

Take a glimpse of a part of them:  
```
tid|id|parent|created|modified|mode|remote_addr|text|author|email|website|likes|dislikes|voters|notification
1|1||1469977655.38995|1469977994.84019|1|104.86.45.0|Goodbye Disqus!  
Hello __ISSO__!  
It's really amazing and I could use __MarkDown__ to comment!  
__I'm So GLAD To Become an _ISSO USER_!__  
BTW, much faster than Disqus!|Sim|sim@snorl.ax||2|0||0
```
It's a comment table with columns named `tid`, `id`, `parent`, `created`, `modified`, `mode`, `remote_addr`, `text`, `author`, `email`, `website`, `likes`, `dislikes`, `voters`, `notification`.  

* `tid`: The id of the thread the comment belongs to.  
* `id`: The id of the comment.  
* `parent`: If the comment is meant to reply to a comment, then the comment has the id of the comment it's meant to reply to.  
* `created`: The time when the comment is created. Stored in Unix Time format.  
* `modified`: The time when the comment is modified. Stored in Unix Time format.  
* `mode`: 1 if the comment is published. 2 if the comment is waiting for approval.  
* `remote_addr`: The IP address of the commenter.  
* `text`: The content of the comment.  
* `author`: The name of the user. Blank if the user didn't fill in the field.  
* `email`: The email of the user. Blank if the user didn't fill in the field.  
* `website`: The url of the website of the user. Blank if the user didn't fill in the field.  
* `likes`: Likes the comment has received so far.  
* `dislikes`: Dislikes the comment has received so far.  
* `voters`: The number of voters of the comments.  
* `notification`: 1 if the author chose to receive reply notification.  

Check the contents in `isso.preferences`:  

```
sqlite> SELECT * FROM isso.preferences;
```

Take a glimpse of it:  
```
key|value
session-key|s0394578gjhsa23sadjhg23asxcnjk423xjzg2131xzmjhde
```
It's table with a session key. I haven't done anything with it. It might be not much useful in sqlite editing.  

Check the contents in `isso.threads`:  

```
sqlite> SELECT * FROM isso.threads;
```

Take a glimpse of a part of them:  
```
id|uri|title
1|/terminal/2016/07/12/start-to-use-isso/|Tried ISSO and......
7|/terminal/2016/05/27/make-full-use-of-cloudflare/|Make full use of CloudFlare
9|/browser/2016/06/04/panic-at-the-disco-bohemian-rhapsody/|Panic! At The Disco - Bohemian Rhapsody
```
It's a thread table with columns named `id`, `uri` and `title`.  

* `id`: The id of the thread.  
* `uri`: The URL of the page the thread serves to.  
* `title`: The title of the thread, used in the title of email notification of the thread.

The following examples might help.   

## Ex 1: Delete Comments

In the examples above, the contents in `isso.comments` was checked:  

```
sqlite> SELECT * FROM isso.comments;
```

Take a glimpse of a part of them:  
```
tid|id|parent|created|modified|mode|remote_addr|text|author|email|website|likes|dislikes|voters|notification
1|1||1469977655.38995|1469977994.84019|1|104.86.45.0|Goodbye Disqus!  
Hello __ISSO__!  
It's really amazing and I could use __MarkDown__ to comment!  
__I'm So GLAD To Become an _ISSO USER_!__  
BTW, much faster than Disqus!|Sim|sim@snorl.ax||2|0||0
7|2||1470373481.55917||1|54.210.166.0|nice blog i like it||||0|0||0
```
Suppose I'm gonna delete the first comment in the table, that's all I have to do:  

```
sqlite> DELETE FROM isso.comments WHERE id=1;
```

To deal similar things with the author Sim, check with care first, to simplify the thngs, only show the column I need:  

```
sqlite> SELECT id, author, text FROM isso.comments WHERE author='Sim';
```

A part of the output:  

```
id|author|text
8|Sim|<p>It depends.If u prefer a FBI icon,just do it!</p>
12|Sim|<p>It's not easy to keep balanced diet</p>
```

To delete the first comment of the table:  

```
sqlite> DELETE FROM isso.comments WHERE id=8;
```

To delete all of Sim's comments:  

```
sqlite> DELETE FROM isso.comments WHERE author='Sim';
```

To delete all of Anonymous user's comments:  

```
sqlite> DELETE FROM isso.comments WHERE author IS NULL;
```

To delete the comments whose `id` are between 1 and 7 (1 and 7 included):  

```
sqlite> DELETE FROM isso.comments WHERE id>=1 AND id<=7;
```

To delete the comment of which `id` is 1 or 7:  

```
sqlite> DELETE FROM isso.comments WHERE id==1 AND id==7;
```

## Ex 2: Approve Comments

This can be useful when u r not able to receive the moderation link via email.  
To check all the comments under approval in sqlite:  

```
sqlite> SELECT id,author,text FROM isso.comments WHERE mode=2;
```

The output:  

```
id|author|text
72|Sim|Test
73|Sim|Test
```

To publish the first comment:  

```
sqlite> UPDATE isso.comments SET mode=1 WHERE id=72;
```

To publish all the comments waiting for approval:  

```
sqlite> UPDATE isso.comments SET mode=1 WHERE mode=2;
```

To delete all the comments waiting for approval:  

```
sqlite> DELETE FROM isso.comments WHERE mode=2;
```

## Ex 3: Delete And Update Threads

To check the threads:  

```
sqlite> SELECT * FROM isso.threads;
```

Take a glimpse of a part of them:  

```
id|uri|title
1|/terminal/2016/07/12/start-to-use-isso/|Tried ISSO and......
7|/terminal/2016/05/27/make-full-use-of-cloudflare/|Make full use of CloudFlare
9|/browser/2016/06/04/panic-at-the-disco-bohemian-rhapsody/|Panic! At The Disco - Bohemian Rhapsody
```

To delete the first thread:  

```
sqlite> DELETE FROM isso.threads WHERE id=1;
```

To delete the comments to the first thread:  

```
sqlite> DELETE FROM isso.comments WHERE tid=1;
```

To move the comments of the first thread to the second one:  

```
sqlite> UPDATE isso.comments SET tid=7 WHERE tid=1;
```

To check all the threads whose url start with `/terminal`:  

```
sqlite> SELECT * FROM isso.threads WHERE uri LIKE '/terminal%';
```

To delete all the threads whose url start with `/terminal`:  

```
sqlite> DELETE FROM isso.threads WHERE uri LIKE '/terminal%';
```

To edit the url the third thread is shown on:  

```
sqlite> UPDATE isso.threads SET uri='/the/path/to/it/' WHERE id=9;
```

To edit the third thread's title:  

```
sqlite> UPDATE isso.threads SET title='The new title' WHERE id=9;
```


[^1]: <a href="https://www.tutorialspoint.com/sqlite/index.htm" target="_blank">SQLite Tutorial - tutorialspoint</a>
