---
title: Site Migration History
date: 2016-12-08 01:40
modified: 2019-06-10 12:51
author: Sim
tags: KeyCDN, Gitlab, Github, Netlify, speed, CloudFlare, Firebase, CDN
status: published
summary: KeyCDN → Gitlab → Github + CloudFlare → Gitlab + Netlify → Github + Cloudflare → Firebase → Cloudflare+Firebase → Cloudflare+Gitlab → Github + Cloudflare → Firebase → My VPS + CloudFlare → My VPS
---

## Summary

The site is hosted on my own VPS now.  
Judging from my experience, my rank of my used hosting of static sites:  

1. Firebase Hosting
2. Github Pages
3. Gitlab Pages / Netlify
4. KeyCDN

Firebase is the champion 'cause its speed is on par with GitHub Pages (Both are using Fastly CDN) and it's really customizable when it comes to things like 301 redirection and caching. BTW, Firebase Hosting also supports dynamic content through Cloud Functions and Cloud Run. As for shortcomings, the SSL cert issued by them have multiple domains from various customers. (I asked the support and they told me I can move to the clean cert with only my domains for free if I switch to Blaze plan which is their pay-as-you-go plan. So I am now on the clean cert several days after I made the switch. Their free usage is like overkill for this site so not a bad deal).  
Github Pages is second to Gitlab Pages due to the shortage of customizability in things like 301, caching and dynamic contents. However the cert of Github Pages is clean with only my own domain there.  
The rest of them are not the fastest. Gitlab Pages supports my own certs. Netlify is feature-rich and the bandwidth limit is 100GB for free. KeyCDN's speed is just poor.  

My current choice is excluded from the list, 'cause VPS itself does much more than all of them and not in the same category.

## 2016-12-08: From KeyCDN To Gitlab

Well the site had been hosted on KeyCDN for about weeks before I couldn't bear the waiting time for even a minor file.   
See the result below:  
<a href="{static}/img/keycdn1.png" title="Wait that long?"><img src="{static}/img/keycdn1-150x150.png" height="150" width="150"></a><a href="{static}/img/keycdn2.png" title="Wait that long?"><img src="{static}/img/keycdn2-150x150.png" height="150" width="150"></a><a href="{static}/img/keycdn3.png" title="Wait that long?"><img src="{static}/img/keycdn3-150x150.png" height="150" width="150"></a>  

That lagging time is not worth the money, I decided to try on Gitlab cause there's no need to spend much on other CDNs, whose SSL support is SNI and SAN support is rather expensive.  

After a while of cloning and pushing and assign SSL, I ran the tests below:  
<a href="{static}/img/gitlab1.png" title="Much better now!"><img src="{static}/img/gitlab1-150x150.png" height="150" width="150"></a><a href="{static}/img/gitlab2.png" title="Much better now!"><img src="{static}/img/gitlab2-150x150.png" height="150" width="150"></a><a href="{static}/img/gitlab3.png" title="Despite the lagging Chinese spot, it's only 0.1 sec lower on avg time. And it defeats KeyCDN almost every spot, meaning KeyCDN sucks."><img src="{static}/img/gitlab3-150x150.png" height="150" width="150"></a>  

It's really a waste of money when it comes to KeyCDN, while Gitlab is an amazing choice, though the SSL things need manually updating on Gitlab.   

Goodbye KeyCDN! Hello Gitlab!   

I've just been using Gitlab for a while and begin to love it! All I need to do is write and update and the rest procedures r automatically done by the runner!  

To make things better, I just used CloudFlare's CDN for it, the speed has improved dramatically, which is well worth the loss of the old browser users, meaning I am finally back to CloudFlare CDN!  

<a href="{static}/img/cloudflare1.png" title="CloudFlare is AMAZING!"><img src="{static}/img/cloudflare1-150x150.png" height="150" width="150"></a><a href="{static}/img/cloudflare2.png" title="CloudFlare is AMAZING!"><img src="{static}/img/cloudflare2-150x150.png" height="150" width="150"></a><a href="{static}/img/cloudflare3.png" title="CloudFlare is AMAZING!"><img src="{static}/img/cloudflare3-150x150.png" height="150" width="150"></a>  

## 2016-12-30: Moved To Github

Just made some tests between Gitlab Pages and Github Pages about the speed. They were both sped up with Cloudflare. No need in uploading those things, 'cause it's basically about data.   

On the same image 33 kb, in Stockholm Github pages performed better with the time of 450 ms while Gitlab spent 995 ms, in Melbourne Github did it again with 497 ms while Gitlab spent 1.54 s. Globally, Github is faster.   

Just moved to Github.  

## 2018-01-12: Stick With Github

To migrate from a server to another, I have to restore my backup. Then today I tried Gitlab to backup and restore. Everything worked like a charm fastly and conveniently with a __free gitlab private__ (which I hadn't really care about when switching from Gitlab Pages to Github pages) repository in which there exists several branches. Then I realized how long I hadn't used Github since the last time. Also, with Netlify, the cert will look much more decent and be auto-renewed. So I just migrated the blog to Gitlab. After speedtest, I finally couldn't stand the speed loss again. 184.8kB in 2s or so almost everywhere. Is a Netlify page really using CDN? For the speed, I moved the blog back to Github PAGES + Cloudflare again.  

## 2018-01-14: Moved To Firebase

Moved to Google Firebase. It's not as fast as Github pages + Cloudflare, but the SSL time beats the CF. I can have enough privacy with my files.

## 2018-01-15 ~ 2019-05-06: My Time With Github Pages

__2018-01-15:__ No way. It's a shared cert on Firebase. After the comparation below, I decided to move back to Gitlab+Cloudflare, 'cause I know I value more about privacy now. Gitlab+CloudFlare has an okay speed for larger files.

Repeated Views Load Time Of a 220.7 kB image (With CloudFlare CDN):  

|Area      |Gitlab |Firebase |
|----------|-------|---------|
|San Jose  |300ms  |49ms     |
|New York  |374ms  |173ms    |
|Melbourne |64ms   |52ms     |
|Stockholm |115ms  |34ms     |

More about Gitlab+CF:  

|Area      |DNS |SSL  |Connect |Send |Wait  |Receive |Total |
|----------|----|-----|--------|-----|------|--------|------|
|San Jose  |2ms |22ms |23ms    |1ms  |268ms |6ms     |322ms |
|New York  |0ms |79ms |114ms   |1ms  |105ms |150ms   |451ms |
|Melbourne |0ms |18ms |19ms    |0ms  |25ms  |19ms    |81ms  |
|Stockholm |0ms |18ms |19ms    |0ms  |88ms  |7ms     |132ms |

More about Firebase+CF:  

|Area     |DNS |SSL |Connect|Send|Wait|Receive|Total|
|---------|----|----|-------|----|----|-------|-----|
|San Jose |2ms |34ms|34ms   |0ms |6ms |6ms    |49ms |
|New York |0ms |58ms|77ms   |1ms |22ms|72ms   |230ms|
|Melbourne|0ms |20ms|21ms   |0ms |9ms |19ms   |69ms |
|Stockholm|0ms |17ms|18ms   |0ms |9ms |6ms    |50ms |

About first-time view? The difference is larger. For instance, in Australia, Gitlab is 1.2s and Firebase is 58ms.

Also, just made a comparation between Gitlab, Github and Firebase on larger files:

The First of Repeated Views Load Time Of a 4.8MB image (With Cloudflare CDN):

|Area      |Github |Firebase |Gitlab |
|----------|-------|---------|-------|
|San Jose  |342ms  |1.27s    |839ms  |
|New York  |659ms  |1.17s    |677ms  |
|Melbourne |2.36s  |3.85s    |2.87s  |
|Stockholm |3.80s  |1.25s    |1.46s  |

Github+CF:  

|Area      |DNS |SSL  |Connect |Send |Wait  |Receive |Total |
|----------|----|-----|--------|-----|------|--------|------|
|San Jose  |2ms |24ms |25ms    |0ms  |247ms |68ms    |366ms |
|New York  |2ms |47ms |49ms    |1ms  |146ms |459ms   |705ms |
|Melbourne |2ms |19ms |19ms    |0ms  |1.90s |440ms   |2.38s |
|Stockholm |2ms |19ms |20ms    |0ms  |3.71s |68ms    |3.81s |

Firebase+CF:  

|Area     |DNS |SSL |Connect|Send|Wait |Receive|Total|
|---------|----|----|-------|----|-----|-------|-----|
|San Jose |2ms |30ms|30ms   |0ms |866ms|373ms  |1.30s|
|New York |3ms |61ms|63ms   |1ms |634ms|468ms  |1.23s|
|Melbourne|2ms |18ms|19ms   |0ms |3.37s|455ms  |3.87s|
|Stockholm|2ms |17ms|18ms   |0ms |1.15s|74ms   |1.26s|

Gitlab+CF:  

|Area     |DNS |SSL |Connect|Send|Wait |Receive|Total|
|---------|----|----|-------|----|-----|-------|-----|
|San Jose |0ms |30ms|31ms   |0ms |321ms|486ms  |868ms|
|New York |0ms |39ms|41ms   |0ms |112ms|523ms  |715ms|
|Melbourne|0ms |23ms|24ms   |0ms |1.04s|1.80s  |2.89s|
|Stockholm|0ms |21ms|21ms   |0ms |577ms|862ms  |1.48s|

__2018-01-20:__ All the static assets on the site will be using the original CDN on the github.io domain.  

__2018-01-21:__ After testing and pondering, the assets of my blog, hosted on Github are now sped up by Cloudflare.  

__2018-05-01:__ <a href="https://blog.github.com/2018-05-01-github-pages-custom-domains-https/" target="_blank">The News: Custom domains on GitHub Pages gain support for HTTPS</a>, now the blog's cert is automatically generated by Github. Even better!  

## 2019-05-06 ~ 2019-06-06: Back To Firebase

__2019-05-06:__ I switched back to Firebase. There I could have control over caching, redirects, etc. No longer rely on soft link. I'm now directly using Firebase.

Just made a speed test on GTMetrix about the isso loading speed on [the article](/terminal/2018/12/27/running-email-service-on-my-own-server/):  

|Area     |With CloudFlare|Bare speed|
|---------|---------------|----------|
|Canada   |1641.6ms       |1322ms    |
|USA      |1351.1ms       |1074.3ms  |
|UK       |430.5ms        |260.6ms   |
|Brazil   |2.72s          |1.75s     |
|Australia|2.92s          |1.998s    |
|China    |3.12s          |1.83s     |
|India    |1.49s          |1.25s     |

Not faster at all. So I'll just stop CF it and make it run barely.  

__2019-05-07:__ I ran a test between Firebase and bare nginx about the static file loading speed on [the article](/terminal/2018/12/27/running-email-service-on-my-own-server/):  

|Area     |With Firebase  |Bare speed|With Github|
|---------|---------------|----------|-----------|
|Canada   |293ms          |1.4s      |0.6s       |
|USA      |0.8s           |1.0s      |308ms      |
|UK       |0.6s           |1.0s      |356ms      |
|Brazil   |1.2s           |1.7s      |0.8s       |
|Australia|419ms          |2.2s      |0.5s       |
|China    |0.9s           |1.9s      |0.8s       |
|India    |0.6s           |1.3s      |1.2s       |

This time Firebase outspeed the bare speed everywhere. Right choice on Firebase about static site. I put Github on the right on purpose. Seems like nowadays GIthub pages and Firebase are almost on par when it comes to speed. To me, it's a right choice to switch to Firebase.  

Just did a lookup about github pages' and Firebase's IP, they are both using Fastly. No wonder the performances are similar. The tests past were totally wrong 'cause I didn't take a look and check which time belonged to the CDN and they are generally affected by CF layer.

__2019-05-27:__ Reused CloudFlare on isso for security purpose.

## 2019-06-06 ~ 2019-06-10: Back To VPS + CloudFlare

Firebase ssl needs checking in every month, which is awful. Also, learning FLask recently, I want to tango with Nginx and CloudFlare. The contents will load fast if cached on CF's server. Otherwise meh...... But Cf is a security company. I use it for security purpose.

## 2019-06-10 ~ Now: My VPS

This site is now served by two servers without Cloudflare as a frontend. (As I found out that Cloudflare CDN generally slows down the site speed). Here's [the relevant results](/terminal/2019/06/10/performance-test-on-a-page-cloudflare-vs-bare-nginx/).
