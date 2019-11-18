---
title: Performance Test on a page - Cloudflare VS Bare Nginx
date: 2019-06-10 22:00
modified: 2019-06-11 09:34
author: Sim
tags: nginx, cloudflare, speed
status: published
summary: Well, nowadays, more and more people says that CloudFlare sucks and slows the website speed. But how slow? I made a test today after I've built my own load balancers with my two servers.
---

## Summary

After doing the load balancing in the [last post](/terminal/2019/06/08/doing-site-mirroring-with-nginx-on-the-same-domain/), I pointed the domain to the CNAME record of the balancer and did some Web Speed Tests[^1].  

Tried comparing the site speed with and without Clouflare CDN using an older version of that post. I have to say, Cloudflare makes the site slower with longer waiting time resulting in a longer TTFB. With the `proxy_cache` in Nginx, the site without Cloudflare CDN is generally faster. So the site is now running without Cloudflare CDN.  

I ran the tests of the old version of the last post on KeyCDN[^1], the test results I need is shown below. The meaning of the table headers:    

* `CF Dev`: The page under Cloudflare Development Mode, where the CDN is used without its caching feature, thus the speed is similar to a site on the CDN visited for the first time when the caching is happening.  
* `CF Cache`: The page visited from cloudflare cache.  
* `Nginx 1st`: The page served directly by the nginx on the server without cached content.  
* `Nginx Cache`: The page served directly by the nginx on the server with saved caches.  
* `The page`: The loading time of the tested post page, in the other words, the html code of the post. This time includes the time of `Blocked`, `DNS`, `Connect`, `SSL`, `Wait` and `Receive` of the domain per request.  
* `CSS`: The loading time of the stylesheet `all.css`.
* `The images`: The loading time of the image taking the longest time to load.  
* `Isoo data 1`: The loading time of the first data request of the isso responded with (a json).  
* `Isoo data 2`: The loading time of the second data request of the isso responded with (html code).  
* `Total Time`: The total loading time of the whole page with all the elements.  
* `Total Time Without Woff2`: `Total Time` minus the loading time of the two google font woff2 files.

## Tests

### Amsterdam

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 249.6 ms       | 279.3 ms | 202.44 ms | 479.2 ms |
| CSS  | 174.2 ms       | 203.6 ms | 52.5 ms | 145.7 ms |
| The images      | 194.956 ms     | 227.1 ms | 192.2 ms | 590.0 ms |
| Isso data 1     | 34.5 ms        | 145.7 ms | 46.6 ms | 466.9 ms |
| Isso data 2     | 37.3 ms        | 143.823 ms | 47.2 ms | 486.3 ms |
| Total Time     | 6.6 s        | 942.8 ms | 9.6 s | 4.3 s |
| Total Time Without woff2     | 0.7 s | 879.7 ms | 0.6 s | 1.75 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-amsterdam.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-amsterdam.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-amsterdam.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-amsterdam.webp) |

This region......Hmm...... Some occasional things happened in it multiple times. Long loading time for google fonts, slow response from Nginx cache.  
Regardless, in this region CloudFlare won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 1       | 0       |

### Bangalore

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 1.8 s          | 1.5 s | 1.1 s | 1 s |
| CSS  | 1.5 s          | 111 ms | 792.0 ms | 227.7 ms |
| The images      | 1.7 s          | 213 ms | 1.5 s | 940.1 ms |
| Isso data 1     | 1.1 s        | 594.7 ms | 565.4 ms | 561.5 ms |
| Isso data 2     | 560.974 ms        | 1.1 s | 565.7 ms | 551.7 ms |
| Total Time     | 4.4 s        | 2.8 s | 2.8 s | 2.5 s |
| Total Time Without woff2 | 4.4 s | 2.7 s | 2.8 s | 2.5 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-bangalore.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-bangalore.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-bangalore.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-bangalore.webp) |

Clearly in this region Nginx won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 1       | 1       |


### Dallas

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 1.2 s          | 900.8 ms | 797.4 ms | 610.9 ms |
| CSS  | 912.2 ms          | 72.9 ms | 510.3 ms | 79.4 ms |
| The images      | 1.1 s          | 89.5 ms | 953.0 ms | 327.8 ms |
| Isso data 1     | 469.2 ms        | 594.2 ms | 414.2 ms | 424.6 ms |
| Isso data 2     | 602.2 ms        | 429.0 ms | 417.4 ms | 417.5 ms |
| Total Time     | 2.9 s        | 1.7 s | 2 s | 1.4 s |
| Total Time Without woff2 | 2.9 s | 1.67 s | 2 s | 1.4 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-dallas.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-dallas.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-dallas.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-dallas.webp) |

In this region Nginx won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 1       | 2       |

### Frankfurt

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 283.1 ms          | 278.9 ms | 309.5 ms | 257.3 ms |
| CSS  | 124.4 ms          | 12.6 ms | 39.0 ms | 35.2 ms |
| The images      | 156.7 s          | 12.5 ms | 154.5 ms | 137.7 ms |
| Isso data 1     | 95.3 ms        | 98.0 ms | 34.1 ms | 34.2 ms |
| Isso data 2     | 101.1 ms        | 31.5 ms | 36.0 ms | 34.3 ms |
| Total Time     | 709.1ms | 623.0 ms | 684.0 ms | 704.3 ms |
| Total Time Without Woff2 | 644 ms | 579.7 ms | 628 ms | 557 ms |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-frankfurt.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-frankfurt.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-frankfurt.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-frankfurt.webp) |

Nginx won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 1       | 3       |

### London

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 405.2 ms | 390.2 ms | 250.8 ms | 229.0 ms |
| CSS  | 200.2 ms | 11.1 ms | 52.1 ms | 47.3 ms |
| The images      | 227.5 ms | 38.4 ms | 198.6 ms | 194.7 ms |
| Isso data 1     | 39.5 ms | 152.2 ms | 48.6 ms | 46.5 ms |
| Isso data 2     | 145.9 ms | 156.5 ms | 49.5 ms | 47.0 ms |
| Total Time     | 1 s | 879.5 ms | 749.5 ms | 641.0 ms |
| Total Time Without Woff2 | 960 ms | 829.5 ms | 723.5 ms | 594.0 ms |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-london.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-london.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-london.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-london.webp) |

Nginx won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 1       | 4       |

### Miami

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 1.2 s | 959.0 ms | 638.3 ms | 554.8 ms |
| CSS  | 951.1 ms | 8.8 ms | 527.0 ms | 70.71 ms |
| The images      | 1.1 s | 16.0 ms | 937.4 ms | 300.1 ms |
| Isso data 1     | 427.7 ms | 600.9 ms | 461.6 ms | 408.8 ms |
| Isso data 2     | 415.8 ms | 614.4 ms | 458.0 ms | 413.2 ms |
| Total Time     | 2.7 s | 1.8 s | 1.9 s | 1.4 s |
| Total Time Without Woff2 | 2.7 s | 1.8 s | 1.9 s | 1.4 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-miami.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-miami.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-miami.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-miami.webp) |

That awfully long waiting time to receive the page can't be saved by the fast speed of static cache...... Clearly Nginx won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 1       | 5       |

### New York

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 1 s | 1 s | 699 ms | 225.6 ms |
| CSS  | 943.3 ms | 12.0 ms | 399.2 ms | 67.6 ms |
| The images      | 1.2 s | 18.3 ms | 945.5 ms | 274.1 ms |
| Isso data 1     | 426.3 ms | 418.4 ms | 403.2 ms | 394.8 ms |
| Isso data 2     | 421.9 ms | 613.1 ms | 395.2 ms | 411.9 ms |
| Total Time     | 2.4 s | 1.8 s | 1.7 s | 1 s |
| Total Time Without Woff2 | 2.4 s | 1.8 s | 1.7 s | 1 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-newyork.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-newyork.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-newyork.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-newyork.webp) |

CloudFlare behaved like a shit on the initial waiting time again which the impressive caching speed can't save...... Nginx won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 1       | 6       |


### Paris

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 319.8 ms | 284.9 ms | 187.5 ms | 501.5 ms |
| CSS  | 244.0 ms | 10.6 ms | 46.9 ms | 148.0 ms |
| The images      | 305.9 ms | 38.7 ms | 174.1 ms | 611.7 ms |
| Isso data 1     | 47.4 ms | 174.9 ms | 43.9 ms | 478.6 ms |
| Isso data 2     | 185.11 ms | 189.7 ms | 44.3 ms | 490.5 ms |
| Total Time     | 1.1 s | 810.66 ms | 635.29 ms | 1.7 s |
| Total Time Without Woff2 | 1.1 s | 755.46 ms | 569.5 ms | 1.7 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-paris.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-paris.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-paris.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-paris.webp) |

Considering something occasional happened to the Nginx Cache, CloudFlare won this round.

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 2       | 6       |

### San Francisco

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 1.2 s | 892.2 ms | 741.0 ms | 414.5 ms |
| CSS  | 741.2 ms | 752.9 ms | 349.8 ms | 13.0 ms |
| The images      | 920.4 ms | 988.4 ms | 892.0 ms | 58.4 ms |
| Isso data 1     | 350.1 ms | 392.6 ms | 362.0 ms | 357.6 ms |
| Isso data 2     | 370.1 ms | 386.9 ms | 355.6 ms | 345.1 ms |
| Total Time     | 2.4 s | 2.2 s | 1.8 s | 1.1 s |
| Total Time Without Woff2 | 2.4 s | 2.2 s | 1.8 s | 1.093 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-san-francisco.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-san-francisco.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-san-francisco.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-san-francisco.webp) |

This round something occasional happened to CloudFlare. Nginx hit Cloudflare so hard and won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 2       | 7       |


### Seattle

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 918.3 ms | 902.7 ms | 741.0 ms | 469.6 ms |
| CSS  | 852.1 ms | 13.6 ms | 349.8 ms | 48.3 ms |
| The images      | 1.1 s | 38.5 ms | 892.0 ms | 199.0 ms |
| Isso data 1     | 513.8 ms | 522.9 ms | 362.0 ms | 393.0 ms |
| Isso data 2     | 398.3 ms | 395.5 ms | 355.6 ms | 384.4 ms |
| Total Time     | 2.4 s | 1.6 s | 1.8 s | 1.2 s |
| Total Time Without Woff2 | 2.4 s | 1.6 s | 1.8 s | 1.18 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-seattle.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-seattle.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-seattle.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-seattle.webp) |

Nginx won 1 score in a similar way as usual.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 2       | 8       |

### Singapore

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 1.7 s | 1.7 s | 1.2 s | 1.2 s |
| CSS  | 1.4 s | 13.2 ms | 530.5 ms | 189.3 ms |
| The images      | 1.6 s | 23.4 ms | 1.3 s | 777.1 ms |
| Isso data 1     | 529.6 ms | 1.1 s | 520.2 ms | 515.6 ms |
| Isso data 2     | 1 s | 532.8 ms | 511.5 ms | 525.3 ms |
| Total Time     | 4.4 s | 3 s | 2.8 s | 2.5 s |
| Total Time Without Woff2 | 4.4 s | 2.97 s | 2.8 s | 2.5 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-singapore.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-singapore.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-singapore.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-singapore.webp) |

When it comes to the global speed, CloudFlare slows down it even more...... Nginx won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 2       | 9       |


### Sydney

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 1.4 s | 1.4 s | 1.1 s | 1 s |
| CSS  | 1.4 s | 9.6 ms | 730.6 ms | 176.6 ms |
| The images      | 1.5 s | 17.6 ms | 1.2 s | 738.7 ms |
| Isso data 1     | 509.6 ms | 1.1 s | 498.9 ms | 497.6 ms |
| Isso data 2     | 491.7 ms | 1 s | 517.4 ms | 507.7 ms |
| Total Time     | 3.5 s | 4.1 s | 2.6 s | 2.3 s |
| Total Time Without Woff2 | 3.5 s | 4.0 s | 2.6 s | 2.3 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-sydney.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-sydney.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-sydney.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-sydney.webp) |

Something occasional happened to Cloudflare again. Nginx won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 2       | 10       |

### Tokyo

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 1.2 s | 1.2 s | 1.2 s | 800.5 ms |
| CSS  | 1.1 s | 1.1 s | 585.8 ms | 129.0 ms |
| The images      | 1.3 s | 1.3 s | 1 s | 529.3 ms |
| Isso data 1     | 456.0 ms | 468.4 ms | 459.8 ms | 461.0 ms |
| Isso data 2     | 781.7 ms | 794.8 ms | 473.7 ms | 451.9 ms |
| Total Time     | 3.2 s | 3.2 s | 2.4 s | 1.8 s |
| Total Time Without Woff2 | 3.2 s | 3.2 s | 2.4 s | 1.8 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-tokyo.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-tokyo.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-tokyo.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-tokyo.webp) |

CloudFlare cache seems not working in Tokyo? Nginx won 1 score.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 2       | 11       |


### Toronto

|                 | CF Dev         | CF Cache | Nginx 1st | Nginx Cache |
| :-------------- | :------------- | :------- | :-------- | :---------- |
| The page  | 918.3 ms | 1.1 s | 703.6 ms | 494.2 ms |
| CSS  | 852.1 ms | 10.0 ms | 401.6 ms | 71.8 ms |
| The images      | 1.1 s | 25.2 ms | 924.8 ms | 279.0 ms |
| Isso data 1     | 513.8 ms | 619.7 ms | 412.5 ms | 412.4 ms |
| Isso data 2     | 398.3 ms | 629.4 ms | 395.4 ms | 404.9 ms |
| Total Time     | 2.4 s | 1.9 s | 1.8 s | 1.2 s |
| Total Time Without Woff2 | 2.4 s | 1.83 s | 1.8 s | 1.2 s |
| Original result | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-dev-toronto.webp) |[The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/cf-cache-toronto.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-dev-toronto.webp) | [The image](https://static.snorl.ax/posts/20190610-cf-vs-bare/bare-cache-toronto.webp) |

Nginx won 1 score again in a usual way.  

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 2       | 12       |

## Result

Score Table:  

| CloudFlare | Nginx     |
| :------------- | :------------- |
| 2       | 12       |

CloudFlare only won two rounds, when something occasional happened. So that result is, almost a total win for bare Nginx. I believe with only one server behind the CloudFlare, Cloudflare will behave worse since there will be some longer paths for CloudFlare to receive responses from thus resulting in a longer waiting time. But CloudFlare is okay as a free service, while I can't expect too much from it with so many users on it. I'm still a user of their DNS. Their DNS is famous for its fast speed.

[^1]: [Website Speed Test | Full Page Performance Check](https://tools.keycdn.com/speed)
