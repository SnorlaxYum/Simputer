---
title: Purchased a NAT VPS From CloudIPLC
date: 2019-06-22 17:55
modified: 2019-08-05 18:08
author: Sim
tags: CloudIPLC, VPS, NAT, Chinese, BBR, Proxy
summary: Whether living in China or not, that could be a must for me.  
---

Today I purchased a NAT VPS from [CloudIPLC](https://www.cloudiplc.com/aff.php?aff=371). The plan was `CN-XZ CT-NAT Micro`, the price was 39.99 RMB a month. Luckily that was the last one. Though I found out that it was not faster than a websocket v2ray proxy running through a Chinese CDN.  

## Forwarding The Traffic

Thank the tutorial for the detailed information.[^1]

I reinstalled Debian Stretch so the following steps were done on it.  

### Step 1: Check if `ipv4.ip_forward` is open

Firstly, ensure ip forwarding feature of ipv4 is open.  

    root@server:~$ sysctl net.ipv4.ip_forward

Good to go to the `Step 2` if the following output is shown:  

    > net.ipv4.ip_forward = 1

Otherwise add the option to `/etc/sysctl.conf`:  

    root@server:~$ echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
    root@server:~$ sysctl -p

### Step 2: Add rules to iptables

`[the local ip of this server]` can be seen from the admin panel of their site.  

Suppose I want to forward a port from the original server to a port with the same number from this server:  

    root@server:~$ iptables -t nat -A PREROUTING -p tcp --dport [port] -j DNAT --to-destination [original server ip]
    root@server:~$ iptables -t nat -A PREROUTING -p udp --dport [port] -j DNAT --to-destination [original server ip]
    root@server:~$ iptables -t nat -A POSTROUTING -p tcp -d [original server ip] --dport [port] -j SNAT --to-source [the local ip of this server]
    root@server:~$ iptables -t nat -A POSTROUTING -p udp -d [original server ip] --dport [port] -j SNAT --to-source [the local ip of this server]

Suppose I want to forward port 1111 from the original server to port 11111 from this server:  

    root@server:~$ iptables -t nat -A PREROUTING -p tcp -m tcp --dport 11111 -j DNAT --to-destination [original server ip]:1111
    root@server:~$ iptables -t nat -A PREROUTING -p udp -m udp --dport 11111 -j DNAT --to-destination [original server ip]:1111
    root@server:~$ iptables -t nat -A POSTROUTING -d [original server ip] -p tcp -m tcp --dport 1111 -j SNAT --to-source [the local ip of this server]
    root@server:~$ iptables -t nat -A POSTROUTING -d [original server ip] -p udp -m udp --dport 1111 -j SNAT --to-source [the local ip of this server]

### Step 3: Apply The Changes

    root@server:~$ iptables-save > /etc/iptables.up.rules
    root@server:~$ iptables-restore < /etc/iptables.up.rules

## Speed Up Using BBR

It's a must and helpful[^2].

Install `speedtest-cli` and test the speed:  

    root@server:~$ apt install ca-certificates speedtest-cli && speedtest-cli

Append the needed lines to `/etc/sysctl.conf`, then reload the changes:  

    root@server:~$ echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
    root@server:~$ echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
    root@server:~$ sysctl --system

Then test again:  

    root@server:~$ speedtest-cli

In my test, the download speed went up by around 1 MB/s. It's only a value. I could feel the change when I was watching Youtube and seeing the debug info.

## Create A Chinese Proxy

Since it's a VPS with a domain with constantly changed __Chinese IP__, it's possible to create a proxy on with with packages like V2Ray. With the Chinese IP it's possible to unblock some Chinese-restricted contents like some contents in Bilibili. I think it's the main use of it.    

I'm gonna skip the `How To` part here. There are enough tutorials about it. Since I've created V2Ray Proxy on servers and `git push` the config files to Gitlab, I just `git pull` the files and changed the port and got them into use.    

[^1]: [通过iptables实现IP端口数据包转发服务配置](https://www.cloudiplc.com/knowledgebase.php?action=displayarticle&id=9)
[^2]: [Increase your Linux server Internet speed with TCP BBR congestion control](https://www.cyberciti.biz/cloud-computing/increase-your-linux-server-internet-speed-with-tcp-bbr-congestion-control/)
