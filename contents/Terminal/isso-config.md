---
title: My Isso Configuration
author: Sim
date: 2019-06-10 09:00
modified: 2019-11-20 00:00
tags:  isso
	 config
summary: I love it!
---

<div id="series" markdown="1">

This post is a part of __My Isso Style__ Series.

1. [Installation](/terminal/2016/07/12/start-to-use-isso/)
2. __Configuration__
3. [Inside the Database](/terminal/2019/06/10/inside-the-isso-database/)

</div>

## Server Configuration

	:::ini
	[general]
	dbpath = /var/lib/isso/comments.db
	host = https://snorl.ax
	notify = smtp
	log-file = /var/lib/isso/snorl.ax.log
	gravatar = true
	gravatar-url = https://www.gravatar.com/avatar/{}?d=https%%3A%%2F%%2Fstatic.snorl.ax%%2Ftheme%%2Fimages%%2Ficon_anonymous.png
	reply-notifications=true

	[moderation]
	enabled = true

	[guard]
	enabled = true
	ratelimit = 1
	direct-reply = 3
	reply-to-self = true

	[smtp]
	host = localhost
	port = 25
	security = none
	to = sim@snorl.ax
	from = "Simputer" <admin@snorl.ax>
	timeout = 10

	[admin]
	enabled = false

For other options I haven't set u could check <a href="https://posativ.org/isso/docs/configuration/server/" target="_blank">the official documentation</a>[^1].  

1. In `[general]`:  

	* `dbpath` is the path of the sqlite database file where I store the data.  
	* `host` is the url where I want the isso to be shown, for isso to be shown in both http and https version, it should be set as:  

			host =
				http://snorl.ax
				https://snorl.ax

	* `notify` is the notification backend for new comments, I set `notify = smtp` so I'll receive a new email when a new comment is successfully submitted to the server, it also make the reply notification possible.  
	* `log-file` is the path of log showing the status of the isso.
	* `gravatar = true` enables the use of gravatar.  
	* `gravatar-url` defines url for gravatar images. The “{}” is where the email hash will be placed. The value after `d=` defines the defalut image  to show if there is no image associated with the requested email hash. If you choose not to set this option, isso will automatically set the value to identicon, which is a geometric pattern based on an email hash.  
	To set my own default image for the situation, I need to urlencode the url for that image. Now for me `https://static.snorl.ax/theme/images/icon_anonymous.png` is the url, so I do it with python[^2]:  

			$ python

	Import the required library for it and do it:  

		>>> import urllib.parse
		>>> the = urllib.parse.quote_plus('https://static.snorl.ax/theme/images/icon_anonymous.png')
		>>> the.replace('%','%%')

	Then it'll return the required url-encoded string:  
	
		'https%%3A%%2F%%2Fstatic.snorl.ax%%2Ftheme%%2Fimages%%2Ficon_anonymous.png'
	
	Now I can set `gravatar-url = https://www.gravatar.com/avatar/{}?d=https%%3A%%2F%%2Fstatic.snorl.ax%%2Ftheme%%2Fimages%%2Ficon_anonymous.png` to see it working. Normally we don't need to replace `%` with `%%`, however in isso if I don't do so, the following error will happen:  
	
		InterpolationSyntaxError: '%' must be followed by '%' or '(', found: u'%3A%2F%2Fstatic.snorl.ax%2Ftheme%2Fimages%2Ficon_anonymous.png'  
	
	To know more about how to tango with Gravatar, see <a href="https://en.gravatar.com/site/implement/images/" target="_blank">the documentation</a>.  

	* `reply-notification=true` enables email notifications of replies to the commenters who have previously subcribed to email notification of replies.  

2. In `[moderation]`:  

	* `enabled` enables comment moderation queue and only affects new comments. Comments in moderation queue are not visible to other users until I activate them.  

3. In `[guard]`:  

	* `enabled` enable guard, for the rest of the section to take into effect.  
	* `ratelimit` is the number of comments each IP address can send in a thread per minute.  
	* `direct-reply` is the number of comments a thread can receive per minute.  
	* `replt-to-self` allows a commenter to reply to his own comment.

4. In `[smtp]`:  

	* `host`, `port`, `security`: the SMTP server, port and security used when a notification is sent through email. Since the isso is located in the same server as my email, the configuration works without `password`. If u want to set email service on ur server and haven't got a clue, u could check out [my post](/terminal/2018/12/27/running-email-service-on-my-own-server/).  
	* `from`: The sender address of the email notification.  
	* `to`: The receiver address of the email notification for every new comments(with their moderation address if moderation is enabled).  
	* `timeout`: Specify a timeout in seconds for blocking operations like the connection attempt.  

5. In `[admin]`:

	* `enabled=false` disable the administration page in `https://isso.snorl.ax/admin/`. No need to open an admin page for that while u could [look into the sqlite urself](/terminal/2019/06/10/inside-the-isso-database/).  

6. `[server]` block has been deleted 'cause it won't work with uwsgi.

## Client Configuration

### Current Configuration

Since I'm using nuxt now, I could easily play with isso API, you can see how I do it from my components in the [source code](https://github.com/SnorlaxYum/Simputer/tree/master/components).

### Previous Configuration  

	<section id=comments data-title="{{ title }}" data-isso-id="/the/path/to/the/page/">

	<script data-isso=https://isso.snorl.ax/ data-isso-gravatar=true data-isso-avatar=false data-isso-reply-notifications=true data-isso-reply-to-self=true data-isso-css=false src=https://static.snorl.ax/theme/js/embed.min.js data-isso-lang=en></script>

For other options I don't use, u can check <a href="https://posativ.org/isso/docs/configuration/client/" target="_blank">the official documention</a>.  

1. The id of the section is `comments`, not `isso-thread`, 'cause I use the edited version of `embed.min.js`, where I replace all the occurences of `isso-thread` with `comments`. That's generally not a recommended practice. Each update of isso will get me busy replacing. So maybe one day I'll revert it back. The `data-title` parses the title to the database as the title of the thread, not working on the thread existing in the database. `data-isso-id` resolves the problem when the same page has several urls. (For example, a soft link on a directory can cause the result.)  
2. I set `data-isso` in the script tag 'cause the `src` is not the original path of the isso.  
3. To get Gravatar working on the site, `data-isso-gravatar=true data-isso-avatar=false` is a must.  
4. To enable the reply notifications on the site, `data-isso-reply-notifications=true` should be set.  
5. `data-isso-reply-to-self=true` allows the commenter to reply to himself.  
6. `data-isso-lang=en` set the language to English. So the language of the running isso on the site won't vary based on the very language the viewer is using.  
7. For my css style of isso to get into effect completely without being interfered, `data-isso-css=false` is a must.  
	Click <a href="https://static.snorl.ax/isso.css">here</a> to seethe css code inside the `embed.min.js` of the newest version of isso as of December 27, 2018. Before applying my own css style completely to the running isso, editing the style based on the original code is generally a recommended practice.  


[^1]: <a href="https://posativ.org/isso/docs/" target="_blank">Isso Official Documentation</a>  
[^2]: <a href="https://stackoverflow.com/a/28874886/9850945" target="_blank">Configparser and string with % - StackOverFlow</a>
