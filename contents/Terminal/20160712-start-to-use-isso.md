---
title: Tried ISSO and ......
date: 2016-07-12 01:00
modified: 2019-11-22 15:57
author: Sim
tags:  isso
 	CDN
 	CloudFlare
 	nginx
 	gevent
 	uwsgi
slug: start-to-use-isso
summary: WOW......
---

<div id="series" markdown="1">

This post is a part of __My Isso Style__ Series.

1. __Installation__
2. [Configuration](/terminal/2019/06/10/my-isso-configuration/)
3. [Inside the Database](/terminal/2019/06/10/inside-the-isso-database/)

</div>

Well, looking back from 2018 and I have got to say, it's more than light-weight and keeps getting better.  

Now with isso u could send reply notifications to the subcribed commenters and isso officially supports gravatar.  

If u r following the things below, be sure to replace username, domain with ur own.  

__Environment:__ Debian Stretch, Python 2.7

## Installation

Don't install a python package as root, the python packages in the package manager might be outdated and it might interfere with your globally installed packages.[^2] (My server running Debian is an example). So it is recommended to use a virtualenv to do it as a non-root user.  

I install isso using git below to make sure it's up to date so everything in the official documentation[^1] takes into effect.  

1. Switch to the non-root user if u aren't logged in as it now. For example, I'm logged in as root and want to switch to sim:  

		:::console
		$ su sim

2. Get into the home directory:  

		:::console
		$ cd ~

3. Install the relevant packages:  

		:::console
		$ sudo apt-get install python-setuptools python-virtualenv python-dev python-pip sqlite3 git build-essential

4. Install Nvm[^3].  

		:::console
		$ git clone https://github.com/creationix/nvm.git .nvm

5. Open `~/.bashrc`, ensure the following lines r included in it and save it[^3]:  

		:::bash
		export NVM_DIR="$HOME/.nvm"
		[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
		[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

	Source it.

		:::console
		$ source ~/.bashrc

6. Install nodejs[^3].  

		:::console
		$ nvm install node

7. Install bower.  

		:::console
		$ npm install -g bower

8. Set virtualenv in a place.  

		:::console
		$ virtualenv work

9. Get into the environment:  

		:::console
		$ source work/bin/activate

10. Fetch isso from source and install it.  

		:::console
		$ git clone https://github.com/posativ/isso.git
		$ cd isso
		$ python setup.py develop # or `install`
		$ make init
		$ npm install -g requirejs uglify-js jade
		$ make js

11. Add a user to run isso exclusively:

		:::console
		$ sudo useradd isso -d /var/lib/isso

12. Make a directory for isso and assign it to the user:  

		:::console
		$ sudo mkdir /var/lib/isso
		$ sudo chown -R isso:isso /var/lib/isso

13. Now switch to the user:  

		:::console
		$ sudo su isso

14. Get into the directory:  

		:::console
		$ cd ~

## Configuration

Create `isso.conf`, the host should be ur URL (I only run the blog in SSL version, so in my case, it's https://snorl.ax):  

	:::ini
	[general]
	dbpath = /var/lib/isso/comments.db
	host = https://snorl.ax/

	[server]
	listen = http://localhost:8001/

For other things like SMTP, reply notification and gravatar, u can refer to [my config](/terminal/2019/06/10/my-isso-configuration/)

Exit to come back as the previous user (In my case, `sim`):  

	:::console
	$ exit

Create a symlink to a location in my `PATH`:  

	:::console
	$ sudo ln -s /home/sim/work/bin/isso /usr/local/bin/isso

About Init Script, I'm using Debian which is using systemd, which is most Linux distributions' choice for service management. Take it for example:  

Create a service `/etc/systemd/system/isso.service` with the following lines:

	:::systemd
	[Unit]
	Description=lightweight Disqus alternative

	[Service]
	User=isso
	ExecStart=/usr/local/bin/isso -c /var/lib/isso/isso.conf run

	[Install]
	WantedBy=multi-user.target

Run the thing and check the status

	:::console
	$ sudo systemctl daemon-reload && sudo systemctl start isso && sudo systemctl status isso

When it's active and running, enable it so it will start and run every time u reboot into the system:

	:::console
	$ sudo systemctl enable isso

## Integrate into the web server

Two ways to do this with nginx, I've actually used both:

1. Running it in `/isso` of the domain `snorl.ax`, the relevant server block in `/etc/nginx/conf.d/default.conf` is shown in SUB-URI tab.
2. Running it in a subdomain like `isso.snorl.ax`, the relevant server block in `/etc/nginx/conf.d/default.conf` is shown in Subdomain tab. 

=== "SUB-URI"
	```{.nginx hl_lines="7-13" linenums="1"}
	server {
		#...
		server_name snorl.ax;

		#...

		location /isso {
		proxy_pass http://localhost:8001;
		proxy_set_header X-Script-Name /isso;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-Proto $scheme;
		}

		#...

	}
	```

=== "Subdomain"
	```{.nginx hl_lines="7-12" linenums="1"}
	server {
		#...
		server_name isso.snorl.ax;

		#...

		location ^~ / {
		proxy_pass http://localhost:8001;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-Proto $scheme;
		}

		#...

	}
	```

## Insert into the website

### API Way

This is the way this blog implemented. See [Official doc about API](https://posativ.org/isso/docs/extras/api/) for more. My way of doing it can be seen from [the source code of the blog](https://github.com/SnorlaxYum/Simputer).

### Direct way

The `https://isso.snorl.ax/js/embed.min.js` should be available.
Time to insert the code to comment area (If u get a 404 error it's due to something like the cache settings of ur js files, delete certain lines of it will help):

	:::html
	<script data-isso="https://isso.snorl.ax/" src="https://isso.snorl.ax/js/embed.min.js"></script>

	<section id=“isso-thread”></section>

Now it's online. Try commenting in the browser. <a href="https://posativ.org/isso/docs/troubleshooting/" target="_blank">Troubleshoot</a> if it fails.

## [Optional] Deploy with gevent

Isso ships with a built-in web server, which is useful for the initial setup and may be used in production for low-traffic sites (up to 20 requests per second). Running a “real” WSGI server supports nice things such as UNIX domain sockets, daemonization and solid HTTP handler while being more stable, secure and web-scale than the built-in web server.[^1]

Before deployment, edit the relevant part[^4] in `~/isso/isso/wsgi.py`:  

	:::python
	# ...
	from werkzeug.wrappers import Response
	# ...
	if environ.get("REQUEST_METHOD") == "OPTIONS":
		#add_cors_headers(b"200 Ok", [("Content-Type", "text/plain")])
		#return []
		response = Response("Ok")
		return response(environ, add_cors_headers)
	# ...

Get into the environment:  

	:::console
	$ source ~/work/bin/activate

### Way 1: gevent

It's the easiest deployment method. [^1]  

Install it.

	:::console
	$ pip install gevent

Run and debug:  

	:::console
	$ /usr/local/bin/isso -c /var/lib/isso/isso.conf run

If it succeeds, restart the service:  

	:::console
	$ sudo systemctl restart isso

### Way 2: uWSGI

Isso has special support for uWSGI, namely fast IPC caching, job spooling and delayed jobs. It's isso's author's choice as well as my choice, install it:  

	:::console
	$ pip install uwsgi

Create `/var/lib/isso/uwsgi.ini`:  

	:::ini
	[uwsgi]
	socket = /tmp/isso/%n.sock
	master = true
	chmod-socket = 666
	uid = isso
	gid = isso
	; set to `nproc`
	processes = 2
	cache2 = name=hash,items=1024,blocksize=32
	; you may change this
	spooler = /tmp/isso
	module = isso.run
	; uncomment if you use a virtual environment
	virtualenv = /home/sim/work
	env = ISSO_SETTINGS=/var/lib/isso/isso.conf
	;

Delete or comment out the listen in the server block in `isso.conf` as it won't work:  

	:::ini
	[server]
	; The listen is now useless
	; listen = http://localhost:8001/

Create the directory:

	:::console
	$ mkdir /tmp/isso
	$ chown -R isso:isso /tmp/isso

Change the lines in nginx configuration:  
1. When isso is running in `/isso` of the domain `snorl.ax`, the relevant server block in `/etc/nginx/conf.d/default.conf` is shown in SUB-URI tab.
2. When isso is running in it in a subdomain like `isso.snorl.ax`, the relevant server block in `/etc/nginx/conf.d/default.conf` is shown in Subdomain tab. 
	
=== "SUB-URI"
	```{.nginx hl_lines="7 8 9 10 11 12 13 14" linenums="1"}
	server {
		# ...
		server_name snorl.ax;

		# ...

		location /isso {
			include         uwsgi_params;
			uwsgi_pass unix:/tmp/isso/uwsgi.sock;
			uwsgi_param HTTP_X_SCRIPT_NAME /isso;
			uwsgi_param HTTP_HOST $host;
			uwsgi_param HTTP_X_FORWARDED_FOR $proxy_add_x_forwarded_for;
			uwsgi_param HTTP_X_FORWARDED_PROTO $scheme;
		}

		# ...

	}
	```

=== "Subdomain"
	```{.nginx hl_lines="7 8 9 10 11 12 13" linenums="1"}
	server {
		# ...
		server_name isso.snorl.ax;

		# ...

		location ^~ / {
			include         uwsgi_params;
			uwsgi_pass unix:/tmp/isso/uwsgi.sock;
			uwsgi_param HTTP_HOST $host;
			uwsgi_param HTTP_X_FORWARDED_FOR $proxy_add_x_forwarded_for;
			uwsgi_param HTTP_X_FORWARDED_PROTO $scheme;
		}

		# ...

	}
	```

Restart my nginx:  

	:::console
	$ sudo systemctl restart nginx

Switch to `isso` user and execute the ini file:  

	:::console
	$ /home/sim/work/bin/uwsgi /var/lib/isso/uwsgi.ini --enable-threads

Test and if it works perfectly.  

If everything's okay, then edit `/etc/systemd/system/isso.service` and change the line of `ExecStart`:

	:::systemd
	[Unit]
	Description=lightweight Disqus alternative

	[Service]
	User=isso
	ExecStart=/home/sim/work/bin/uwsgi /var/lib/isso/uwsgi.ini --enable-threads

	[Install]
	WantedBy=multi-user.target

Run the thing and check the status

	:::console
	$ sudo systemctl daemon-reload && sudo systemctl start isso && sudo systemctl status isso

## [Optional] CDN Integration

This is not recommended though, at least Cloudflare CDN slows the loading speed globally. I recommend setting loading balancers by myself. Here's [my way to do it](/terminal/2019/06/08/doing-site-mirroring-with-nginx-on-the-same-domain/).  

I used to use Cloudflare with my isso. Since I ran isso on uwsgi through unix socket without the use of `X-Forwarded-For`, I could get the commenter's IP directly from mail with the default configuration. So no need in doing extra config like the following.  

This is not the case with isso running through a TCP/IP port, where the IP from mail is one of the CDN's IP. So to get the real IP of the commenter's, extra configuration like following one is needed.  

CloudFlare Tutorial about solution: <a href="https://support.cloudflare.com/hc/en-us/articles/200170706-How-do-I-restore-original-visitor-IP-with-Nginx-" target="_blank">Nginx</a> | <a href="https://support.cloudflare.com/hc/en-us/articles/203656534-How-do-I-restore-original-visitor-IP-with-Apache-2-4-" target="_blank">Apache</a>  

I'm using Nginx currently, in the conf the variable `X-Forwarded-For` is set for showing true IP.  

1. Edit `/etc/nginx/nginx.conf`, make sure the `http` section contains `set_real_ip_from` field with the IPs of Cloudflare and real_ip_header is set to `X-Forwarded-For`, just like this:  
	```{.nginx linenums="1"}
	http {
	# ...
	set_real_ip_from 103.21.244.0/22;
	set_real_ip_from 103.22.200.0/22;
	set_real_ip_from 103.31.4.0/22;
	set_real_ip_from 104.16.0.0/12;
	set_real_ip_from 108.162.192.0/18;
	set_real_ip_from 131.0.72.0/22;
	set_real_ip_from 141.101.64.0/18;
	set_real_ip_from 162.158.0.0/15;
	set_real_ip_from 172.64.0.0/13;
	set_real_ip_from 173.245.48.0/20;
	set_real_ip_from 188.114.96.0/20;
	set_real_ip_from 190.93.240.0/20;
	set_real_ip_from 197.234.240.0/22;
	set_real_ip_from 198.41.128.0/17;

	real_ip_header X-Forwarded-For;
	# ...
	}
	# 
	```

	If the Nginx supports ipv6, try the following:  
	```{.nginx linenums="1"}
	http {
	# ...
	set_real_ip_from 103.21.244.0/22;
	set_real_ip_from 103.22.200.0/22;
	set_real_ip_from 103.31.4.0/22;
	set_real_ip_from 104.16.0.0/12;
	set_real_ip_from 108.162.192.0/18;
	set_real_ip_from 131.0.72.0/22;
	set_real_ip_from 141.101.64.0/18;
	set_real_ip_from 162.158.0.0/15;
	set_real_ip_from 172.64.0.0/13;
	set_real_ip_from 173.245.48.0/20;
	set_real_ip_from 188.114.96.0/20;
	set_real_ip_from 190.93.240.0/20;
	set_real_ip_from 197.234.240.0/22;
	set_real_ip_from 198.41.128.0/17;
	set_real_ip_from 2400:cb00::/32;
	set_real_ip_from 2606:4700::/32;
	set_real_ip_from 2803:f800::/32;
	set_real_ip_from 2405:b500::/32;
	set_real_ip_from 2405:8100::/32;
	set_real_ip_from 2c0f:f248::/32;
	set_real_ip_from 2a06:98c0::/29;

	real_ip_header X-Forwarded-For;
	# ...
	}
	```

	Notes that the CloudFlare IPs above were up to date when I modified the article, check for urself. If u use another CDN or find that any of the CloudFlare IPs outdated, replace the IPs with the correct ones.

2. Refresh and try commenting. The IP in the mail turns out to be the true IP of the commenter.  

[^1]: [Isso Official Documentation](https://posativ.org/isso/docs/) 
[^2]: [Why you should not use Python’s easy_install carelessly on Debian](https://workaround.org/easy-install-debian) 
[^3]: [How to install Npm](https://www.npmjs.com/get-npm)
[^4]: [Isso Forces CORS Preflight but is unable to handle CORS Preflight requests](https://github.com/posativ/isso/issues/347#issuecomment-347906155)
