---
title: Permission issues with dovecot stats-writer
date: 2019-07-11 17:00
author: Sim
tags: email, postfix, dovecot, Debian, spamassassin
summary: Today I encountered an error when trying to receive new messages from my mailbox.  
---
__Env:__ Debian 10

Today I encountered an error when trying to receive new messages from my mailbox.  
Then I checked `/var/log/mail.log` and found this:  

    :::ini
    Jul 11 10:54:00 mail postfix/pipe[27149]: 0A3FBDBE26: to=<xxx@snorl.ax>, orig_to=<sim@snorl.ax>, relay=spamassassin, delay=1.4, delays=0.45/0.02/0/0.98, dsn=2.0.0, status=sent (delivered via spamassassin service (lda(xxx@snorl.ax,)Error: net_connect_unix(/var/run/dovecot/stats-writer) failed: Permission denied))

I googled and found this solution[^1] work well. Just append the following settings to `/etc/dovecot/dovecot.conf`:  

    :::ini
    service stats {
        unix_listener stats-reader {
            user = vmail
            group = vmail
            mode = 0660
        }

        unix_listener stats-writer {
            user = vmail
            group = vmail
            mode = 0660
        }
    }

Then restart dovecot:  

    sim@mail:~$ sudo systemctl restart dovecot

[^1]: [net_connect_unix(/var/run/dovecot/stats-writer) failed (Page 1) — iRedMail Support — iRedMail](https://forum.iredmail.org/post67035.html#p67035)
