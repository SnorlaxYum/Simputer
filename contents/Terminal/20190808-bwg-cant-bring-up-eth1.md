---
title: ifup cannot bring up eth1 after upgrading
date: 2019-08-08 22:39
author: Sim
tags: Bandwagonhost, Debian
status: published
summary: Happened after I upgraded to Debian Buster on my Bandwagonhost VPS.
---
This happened some hours after I upgraded to Debian Buster on my Bandwagonhost VPS. The IP timed out all over the world. Then I did a research in the root shell. It turned out to be `networking.service` failure:  

```
ifup[478]: Failed to bring up eth1.
systemd[1]: networking.service: Failed with result 'exit-code'.
```

Searched and found a solution[^1]:  

```
# apt install network-manager
# systemctl enable systemd-networkd
# systemctl enable systemd-resolved
# systemctl start systemd-networkd
# systemctl start systemd-resolved
# apt install isc-dhcp-client
# dpkg-reconfigure resolvconf
```

Then the IP worked again, but `networking.service` still failed with the same error. I searched again and found it related to `/etc/network/interfaces`[^2].  

My `/etc/network/interfaces` looked like this:  

```
source /etc/network/interfaces.d/*
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet dhcp
auto eth1
iface eth1 inet dhcp
```

Meanwhile the output of `networkctl` looked like this:  

```
IDX LINK             TYPE               OPERATIONAL SETUP     
  1 lo               loopback           carrier     unmanaged
  2 eth0             ether              routable    unmanaged
```

There's nothing to do with so-called eth1, so this is my edited `/etc/network/interfaces` now:  

```
source /etc/network/interfaces.d/*
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet dhcp
#auto eth1
#iface eth1 inet dhcp
```

The reason why that happened might be due to my selection of using the config file from maintainer's package when I did the upgrade.  

[^1]: [networking - ifup cannot bring up eth0 after upgrading to 16.04 - Ask Ubuntu](https://askubuntu.com/a/769239)
[^2]: [networking - Failed to start Raise network interfaces after upgrading to 16.04 - Ask Ubuntu](https://askubuntu.com/questions/824376/failed-to-start-raise-network-interfaces-after-upgrading-to-16-04)
