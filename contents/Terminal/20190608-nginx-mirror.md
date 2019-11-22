---
title: Doing site mirroring with nginx on the same domain
date: 2019-06-08 22:08
modified: 2019-06-18 17:47
author: Sim
tags: nginx, load balancing, PerfOps, cloudflare
summary: Hmm, found a way to do that.
---

Since I have got two differnt servers (one in Finland, one in Los Angeles) I wanna load balance my site using nginx.  

## Basic settings

I don't recommend proxying static files. Instead, upload the files to both servers and serve them directly from each server. ([My method of doing this](/terminal/2019/06/07/git-an-excellent-file-transferer/) In this way no need in putting up with the latency from fetching files......  

The way here only applies to a backend needing updating dynamically.  

Having been searching a long way, I've found that it's viable via a port.  

`/etc/nginx/conf.d/default.conf`:  

    :::nginx
    server {
      listen 443 ssl http2;
      server_name snorl.ax;
      # ...site-configurations...
    }

I could separate it into two parts, for example I'm gonna use port 123 on the main server:  

    :::nginx
    server {
      listen 123;
      server_name _;
      if ($host !~ snorl.ax) {
        return 444;
      }
      if ($http_custom !~ acustomheader) {
        return 444;
      }
      # ...site-configurations, use $host variable where I originally use $server_name...
      location ^~ /isso {
        include         uwsgi_params;
        uwsgi_pass unix:///tmp/isso/uwsgi.sock;
        uwsgi_param HTTP_X_SCRIPT_NAME /isso;
        uwsgi_param HTTP_HOST $host;
        uwsgi_param HTTP_X_REAL_IP $http_x_real_ip;
      }
    }

    server {
      listen 443 ssl http2;
      server_name snorl.ax;

      location ^~ / {
        proxy_pass http://localhost:123;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Custom acustomheader;
      }

      location ^~ /isso {
        uwsgi_pass unix:///tmp/isso/uwsgi.sock;
        uwsgi_param HTTP_X_SCRIPT_NAME /isso;
        uwsgi_param HTTP_HOST $host;
        uwsgi_param HTTP_X_FORWARDED_FOR $proxy_add_x_forwarded_for;
        include         uwsgi_params;
      }

    }

The `^~` ensures that the static files are loaded correctly[^1].  

The two `if`[^4] blocks ensure the `Host` header received[^5] is `snorl.ax` and `Custom` is `acustomheader`. Otherwise the server will return an error page, denying the further access.  

`X-Forwarded-For` is useful when it comes to the true IP of the client. Be sure to include the lines in the http block in `/etc/nginx/nginx.conf` on the main server:  

    :::nginx
    http {
      # ...
      set_real_ip_from the_second_server_ip;
      real_ip_header X-Forwrded-For;
    }

Be sure to include this in `/etc/nginx/nginx.conf` in the http block:  

    :::nginx
    http {
      # ...
      port_in_redirect off;
      # ...
    }

Thus it'll support adding a trailing slash through proxy_pass if there's none, without redirecting the user to a url like `url:port/uri`.[^7]  

Then reload on this server:  

    :::bash
    sim@server:~$ sudo systemctl reload nginx

`/etc/nginx/conf.d/default.conf` on the second server:  

    :::nginx
    server {
      listen 443 ssl http2;
      server_name snorl.ax;

      location ^~ / {
        proxy_pass http://external_ip_of_main:123;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Custom acustomheader;
      }
    }

It is allowed to proxy the the apps like isso in the first server block of the first server on this server. As I said above, `X-Forwarded-For` is useful when it comes to the true IP of the client.

`X-Forwarded-Proto` make the scheme the same with the proxy frontend (In this case, it's `https` rather than the `http` of the backend).

Be sure to include this in `/etc/nginx/nginx.conf` in the http block as well for the same reason above:  

    :::nginx
    http {
      # ...
      port_in_redirect off;
      # ...
    }

Reload on this server:   

    :::bash
    sim@server:~$ sudo systemctl reload nginx

## `proxy_cache` for them

This could improve site performance a lot if many static files from the backend need proxying. However as I said before, it's recommended to upload the files to both servers and serve them directly from each server. Files from the same server can be more easy to control and enjoy features like `brotli_static`. So in a way `proxy_cache` kinda sucks for static files in my opinion.  

For example, on the second server, I want to use cache for the paths other than `/isso` with longer caching expiration period for `/img` folder, my settings will be like this:  

    :::nginx
    proxy_cache_path  /etc/nginx/cache  levels=1:2    keys_zone=snorlax:10m
    inactive=24h  max_size=1g;
    server {
      # ...
      server_name snorl.ax;
      # ...
    # Default: expires in 1 hour
    location ^~ / {
        proxy_pass http://external_ip_of_main:123;
        proxy_set_header Host $host;
        proxy_set_header Custom acustomheader;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering        on;
        proxy_cache_revalidate on;
        proxy_cache            snorlax;
        proxy_cache_valid      200  1h;
        proxy_cache_use_stale  error timeout invalid_header updating
                              http_500 http_502 http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;
        add_header X-Cache-Status $upstream_cache_status;

    }

    # /isso path: Micro-caching for faster speed and less loads on the origin
    location ^~ /isso {
        proxy_pass http://external_ip_of_main:123;
        proxy_set_header Host $host;
        proxy_set_header Custom acustomheader;
        proxy_buffering        off;
        proxy_cache_revalidate on;
        proxy_cache            snorlax;
        proxy_cache_valid      200 404 1s;
        proxy_cache_use_stale  updating;
        proxy_cache_background_update on;
        proxy_cache_lock on;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # /img path: expires in 1 year.

    location ^~ /img {
        proxy_pass http://external_ip_of_main:123;
        proxy_set_header Host $host;
        proxy_set_header Custom acustomheader;
        proxy_buffering        on;
        proxy_cache_revalidate on;
        proxy_cache            snorlax;
        proxy_cache_valid      200  1y;
        proxy_cache_use_stale  error timeout invalid_header updating
                              http_500 http_502 http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;
        add_header X-Cache-Status $upstream_cache_status;
    }
    # ...
    }

For the details about these settings, check the official guide[^6].  

Then create a directory for it and reload:  

    :::bash
    sim@server:~$ sudo mkdir /etc/nginx/cache
    sim@server:~$ sudo chown -R nginx:nginx /etc/nginx/cache
    sim@server:~$ sudo systemctl reload nginx

## Load Balancing the servers

Two choices for it: Load Balancer CNAME, GeoDNS.

### Load Balancer CNAME

Cloudflare has this and charges it for at least 5 dollars a month just for subscription fee. Then they will charge according to the bandwidth usage.

Another choice[^2] is a free alternative [PerfOps](https://perfops.net/). I highly recommend this. Their free tier usage (100,000,000  Queries, 3 FlexBalancers) can be good enough. I added answers to various locations according to the result of the App Synthetic Monitor Ping Tool[^3]. I have to say, works like a charm.   

### GeoDNS

However CNAME have its shortages:  

1. They could be slower than A records.
2. Root CNAME Flattening is not that accurate.  

That's where GeoDNS comes in, with which there's no need in resolving a hostname into an IP, adding an additional request.  

[NS1](https://ns1.com/) has a free tier with a limit of 500,000 queries, 50 Records. So it's my go-to solution for load balancing. I'm waiting for DNS propagation to complete. But it's not cost-efficient when overages are billed at $8/million queries.  

[Route53](https://aws.amazon.com/route53/pricing/) is cost-efficient and charges for $1.2 a month if the domain uses their GeoDNS and has 1 million DNS queries. So once I have more than 500,000 queries I will switch to this.  

__A Note:__ I followed nginxconfig.io[^8] to enhance and simplify my nginx config. After doing that, I found TLS speed was slow, the lines of the nginx config from letsencrypt helped and boosted the TLS speed greatly:  

    :::nginx
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # generated by Certbot when their nginx plugin is used

    # The two lines below are from their config /etc/letsencrypt/options-ssl-nginx.conf
    ssl_session_cache shared:le_nginx_SSL:50m; # I modified the original 1m to 50m
    ssl_ciphers "ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS";

[^1]: [nginx reverse proxy images and css are not loaded - Stack Overflow](https://stackoverflow.com/questions/25187817/nginx-reverse-proxy-images-and-css-are-not-loaded/35065881#35065881)
[^2]: [How to make an A record load balancer with HAProxy? : sysadmin](https://www.reddit.com/r/sysadmin/comments/by6lnh/how_to_make_an_a_record_load_balancer_with_haproxy/eqdiyib/)
[^3]: [CA App Synthetic Monitor website monitoring service - Ping - IPv6 now supported, give it a shot!](https://asm.ca.com/en/ping.php)
[^4]: [conditional within an "if" in Nginx | DigitalOcean](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html#if)
[^5]: [Nginx: Reject request if header is not present or wrong - Stack Overflow](https://stackoverflow.com/questions/18970620/nginx-reject-request-if-header-is-not-present-or-wrong/18972508#18972508)
[^6]: [A Guide to Caching with NGINX and NGINX Plus - NGINX](https://www.nginx.com/blog/nginx-caching-guide/)
[^7]: [Re: nginx add trailing slash](https://forum.nginx.org/read.php?2,234131,234141)
[^8]: [nginxconfig.io](https://nginxconfig.io/)
