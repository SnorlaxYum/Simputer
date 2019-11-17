---
title: Updated to Debian Buster
date: 2019-06-17 13:30
modified: 2019-08-05 17:49
author: Sim
tags: Debian, Buster, openssl, dovecot
status: published
summary: Some packages changed and needed some changes.
---

## Update To Debian Buster

`/etc/apt/sources.list`:

```
deb http://debian-mirror.westus.cloudapp.azure.com/debian/ buster main
deb-src http://debian-mirror.westus.cloudapp.azure.com/debian/ buster main

deb http://security.debian.org/ buster/updates main
deb-src http://security.debian.org/ buster/updates main

deb http://debian-mirror.westus.cloudapp.azure.com/debian/ buster-backports main

deb http://nginx.org/packages/mainline/debian/ buster nginx
deb-src http://nginx.org/packages/mainline/debian/ buster nginx

deb http://debian-mirror.westus.cloudapp.azure.com/debian/ buster-updates main
deb-src http://debian-mirror.westus.cloudapp.azure.com/debian/ buster-updates main
```

In the configuration file above I replaced `stretch` with buster.

In my case I found files in `/etc/apt/sources.list.d/` too so I did similar changes there.  

Then upgrade:  

```
sim@server:~$ sudo apt update && sudo apt upgrade && sudo apt dist-upgrade
```

Answer to the prompts in the process. Then it's done.  

## Dovecot: dh key too small

Upon update, I can't log in to my imap anymore with the following log:  

```
Jun 17 06:37:01 server dovecot: imap-login: Error: Failed to initialize SSL server context: Can't load DH parameters: error:1408518A:SSL routines:ssl3_ctx_ctrl:dh key too small: user=<>, rip=*.*.*.*, lip=*.*.*.*, session=<eUofjH2LSO2wer5W>
```

It's because from version 2.3 I must specify path to DH parameters file using[^1]:  

```
ssl_dh=</path/to/dh.pem
```

So to resolve this:  

```
sim@server:~$ su
root@server:~$ openssl dhparam 4096 > /var/mail/dh.pem
```

In `/etc/dovecot/conf.d/10-ssl.conf`, specidy this:  

```
...
ssl_dh=</var/mail/dh.pem
...
```

Specifying this is recommended as well:  

```
...
ssl_prefer_server_ciphers=yes
...
```

Then restart:  

```
root@server:~$ systemctl restart dovecot
```

Now I'm able to log in to my imap again.

[^1]: [SSL/DovecotConfiguration - Dovecot Wiki](https://wiki.dovecot.org/SSL/DovecotConfiguration)
