---
title: Running email service on my own server!
date: 2018-12-27 13:00
modified: 2019-05-28 13:14
author: Sim
tags: email, postfix, dovecot, saslauthd, Debian, imap, smtp, SendGrid, Amazon SES, dkim, spf, dmarc, mailutils, spamassassin
summary: I've done it! Yes!
---

__Env:__ Debian Stretch[^1][^2]

If u want to follow the procedures below, be sure to replace informations like URL with ur own choice of configuration,  

## Update Hosts

Verify that the `/etc/hosts` file contains lines for the server's public IP address and is associated with the Fully Qualified Domain Name (FQDN). In the examples below, the public IP address of my VPS is `12.34.56.78` and `2aaa:bbb:dddd:eeee::1` and the FQDN is `mail.snorl.ax`.   

	...
	12.34.56.78 mail.snorl.ax mail
	...
	2aaa:bbb:dddd:eeee::1

Be sure to add an A Record for it. If assigned, AAAA of IPV6 is also needed.  

	mail.snorl.ax	A 10 12.34.56.78
	mail.snorl.ax AAAA 10 2aaa:bbb:dddd:eeee::1

Change the hostname to it as well[^10].  

	$ sudo hostname mail.snorl.ax

Be sure to configure Reverse DNS for the IP to point to `mail.snorl.ax`.  

## Software Installation

I'm using Debian Stretch on my Linode VPS, so I installed from stretch-backports[^3]. For backports to work, a line like the following one should be added to the `/etc/apt/sources.list`:  

	deb http://ftp.debian.org/debian stretch-backports main

The address could be my choice of source containing the backports, what I added before installation is:  

	deb http://mirrors.linode.com/debian stretch-backports main

Then I installed the packages using the command:  

	:::console
	$ sudo apt -t stretch-backports install postfix-pgsql sasl2-bin libsasl2-modules postgresql libpam-pgsql dovecot-pgsql dovecot-imapd dovecot-pop3d

## Configuring PostgreSQL

Edit `/etc/postgresql/pg_hba.conf` to accept password authentication for localhost:  

	host    all         all         127.0.0.1         255.255.255.255   password

Create the database:  

	:::console
	$ sudo su postgres
	$ createdb mails
	$ psql mails

Create tables:  

	:::PostgreSQL
	CREATE TABLE transport (
	domain VARCHAR(128) NOT NULL,
	transport VARCHAR(128) NOT NULL,
	PRIMARY KEY (domain)
	);
	CREATE TABLE users (
	userid VARCHAR(128) NOT NULL,
	password VARCHAR(128),
	realname VARCHAR(128),
	uid INTEGER NOT NULL,
	gid INTEGER NOT NULL,
	home VARCHAR(128),
	mail VARCHAR(255),
	PRIMARY KEY (userid)
	);
	CREATE TABLE virtual (
	address VARCHAR(255) NOT NULL,
	userid VARCHAR(255) NOT NULL,
	PRIMARY KEY (address)
	);
	create view postfix_mailboxes as
	select userid, home||'/' as mailbox from users
	union all
	select domain as userid, 'dummy' as mailbox from transport;
	create view postfix_virtual as
	select userid, userid as address from users
	union all
	select userid, address from virtual;

Create separate users for read and write accesses. Postfix and Dovecot needs only read access. I may want to use the writer user for your own purposes.  

	:::sql
	CREATE USER mailreader PASSWORD 'secret';
	grant select on transport, users, virtual, postfix_mailboxes, postfix_virtual to mailreader;
	create user mailwriter password 'secret';
	grant select, insert, update, delete on transport, users, virtual, postfix_mailboxes, postfix_virtual to mailwriter;

Add domain, user to the database. The examples below add the domain `snorl.ax` and a user with the mail address `kim@snorl.ax`:  

	:::sql
	insert into transport (domain, transport) values ('snorl.ax', 'virtual:');
	insert into users (userid, uid, gid, home) values ('user@snorl.ax', 5000, 5000, 'snorl.ax/mails/user');
	insert into users (userid, uid, gid, home) values ('user2@snorl.ax', 5000, 5000, 'snorl.ax/mails/user2');
	insert into virtual (address, userid) values ('kim@snorl.ax', 'user@snorl.ax');

The password for a user can be generated using `doveadm` utility[^4]:  

	:::console
	$ doveadm pw -s CRYPT

It will prompt me to enter the password twice:  

	Enter new password:
	Retype new password:

Then it will print a encrypted string like the one below for me to write into the database:  

	:::console
	{CRYPT}1cElWVzS3.EVg

To do something with the password, access the `psql` utility again:  

	:::console
	$ sudo su postgres
	$ psql mails

To update an existing user with the password:  

	:::sql
	UPDATE users SET password='{CRYPT}1cElWVzS3.EVg' WHERE userid='user@snorl.ax';

To set the password when creating the user:  

	:::sql
	insert into users (userid, password, uid, gid, home) values ('user3@snorl.ax', '{CRYPT}1cElWVzS3.EVg', 5000, 5000, 'snorl.ax/mails/user3');

Self-check.  

To check the existing user:  

	:::sql
	SELECT * FROM users;

A table like this will be shown:  

	:::console
		userid     |       password       | realname | uid  | gid  |         home         | mail
	----------------+----------------------+----------+------+------+----------------------+------
	user1@snorl.ax | {CRYPT}xxxxxxxxxxxxx |          | 5000 | 5000 | snorl.ax/mails/user1 |
	user@snorl.ax  | {CRYPT}xxxxxxxxxxxxx |          | 5000 | 5000 | snorl.ax/mails/user  |

To check the correspondence between username and mail address:  

	:::sql
	SELECT * FROM virtual;

A table similar to the following one will be shown:  

	    address     |     userid     
	----------------+----------------
	 kim@snorl.ax   | user@snorl.ax
	 xxx@snorl.ax   | user2@snorl.ax
	 xxxx@snorl.ax  | user1@snorl.ax

## Create the folder and user for mail

Create `/var/mail/vhosts/` and the folder named my domain:

	:::console
	$ sudo mkdir -p /var/mail/vhosts/snorl.ax

Create the group and the user for it:  

	:::console
	$ sudo groupadd -g 5000 vmail
	$ sudo useradd -g vmail -u 5000 vmail -d /var/mail

Change the owner of the `/var/mail/` folder and its contents to belong to `vmail`:  

	:::console
	$ sudo chown -R vmail:vmail /var/mail

## Configuring Postfix

Edit `/etc/postfix/main.cf` to set the following values[^12]:  

	:::ini
	transport_maps = pgsql:/etc/postfix/transport.cf
	virtual_uid_maps = pgsql:/etc/postfix/uids.cf
	virtual_gid_maps = pgsql:/etc/postfix/gids.cf
	virtual_mailbox_base = /var/mail/vhosts
	virtual_mailbox_maps = pgsql:/etc/postfix/mailboxes.cf
	virtual_maps = pgsql:/etc/postfix/virtual.cf

	mydestination = localhost.$mydomain, $myhostname
	smtpd_relay_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination
	local_transport = virtual
	local_recipient_maps = $virtual_mailbox_maps
	smtpd_sasl_auth_enable = yes
	smtpd_sasl_security_options = noanonymous
	smtpd_sasl_local_domain = mail.snorl.ax
	smtp_sasl_auth_enable = no
	myorigin = $mydomain

These defines mailbox domains and relevant settings such as sasl, mailbox location, rejecting unknown local recipients[^19].

Edit `/etc/postfix/sasl/smtpd.conf` to include the following lines:  

	:::ini
	pwcheck_method: saslauthd
	saslauthd_path: /etc/mux

`/etc/postfix/transport.cf`  

	:::ini
	user=mailreader
	password=secret
	dbname=mails
	table=transport
	select_field=transport
	where_field=domain
	hosts=localhost

`/etc/postfix/uids.cf`  

	:::ini
	user=mailreader
	password=secret
	dbname=mails
	table=users
	select_field=uid
	where_field=userid
	hosts=localhost

`/etc/postfix/gids.cf`  

	:::ini
	user=mailreader
	password=secret
	dbname=mails
	table=users
	select_field=gid
	where_field=userid
	hosts=localhost

`/etc/postfix/mailboxes.cf`  

	:::ini
	user=mailreader
	password=secret
	dbname=mails
	table=postfix_mailboxes
	select_field=mailbox
	where_field=userid
	hosts=localhost

`/etc/postfix/virtual.cf`  

	:::ini
	user=mailreader
	password=secret
	dbname=mails
	table=postfix_virtual
	select_field=userid
	where_field=address
	hosts=localhost

By default, these two lines are included in `/etc/postfix/main.cf`:  

	:::ini
	alias_maps = hash:/etc/aliases
	alias_database = hash:/etc/aliases

It's for the local delivery, meant to be sent to the users on the computer. Since I have the virtual domain and mailboxes, it will be more convenient to forward it to the mailbox. Put the lines in `/etc/aliases`:  

	:::ini
	# user:	the mail address
	kim:	kim@snorl.ax
	root:	root@snorl.ax

Then update:  

	:::console
	$ sudo newaliases

In this case, local delivery will work. System messages to `kim ` will be delivered to `kim@snorl.ax`.

## Configuring SASL2

Edit `/etc/default/saslauthd`:  

	:::ini
	START=yes
	MECHANISMS=pam
	PARAMS="-r -m /var/spool/postfix/etc"

`/etc/pam_pgsql.conf`  

	:::ini
	database = mails
	host = localhost
	user = mailreader
	password = secret
	table = users
	user_column = userid
	pwd_column = password
	#expired_column = acc_expired
	#newtok_column = acc_new_pwreq
	pw_type = crypt
	#debug

Create `/etc/pam.d/smtp`:  

	:::ini
	auth        required    pam_pgsql.so
	account     required    pam_pgsql.so
	password    required    pam_pgsql.so

Put the following line to `/etc/postfix/sasl/smtpd.conf`:  

	:::ini
	mech_list: login plain

## Configuring Dovecot

Put the following lines in the `/etc/dovecot/dovecot.conf`:  

	:::ini
	mail_location = maildir:~/
	passdb {
	  args = /usr/local/etc/dovecot-sql.conf
	  driver = sql
	}
	userdb {
	  args = /usr/local/etc/dovecot-sql.conf
	  driver = sql
	}
	mail_privileged_group = vmail

`/usr/local/etc/dovecot-sql.conf`:  

	:::ini
	driver = pgsql
	connect = host=localhost dbname=mails user=mailreader password=secret
	default_pass_scheme = CRYPT
	password_query = SELECT userid as user, password FROM users WHERE userid = '%u'
	user_query = SELECT '/var/mail/vhosts/'||home AS home, uid, gid FROM users WHERE userid = '%u'

Ensure the following line is included in `/etc/dovecot/conf.d/10-auth.conf`[^5]:  

	:::ini
	disable_plaintext_auth = no

I'll switch this back to `yes` or other options afterward. Plain text is for test.  

## Configure DNS

When I'm ready to send and receive mails from my server, I should edit the domain's MX record so it points to the IP address of the server, similar to the examples below:  

	:::dns
	mail.snorl.ax A 10 12.34.56.78
	mail.snorl.ax AAAA 10 2aaa:bbb:dddd:eeee::1
	snorl.ax MX 10 mail.snorl.ax

## Testing Imap

Restart the relevant services before testing:  

	:::console
	$ sudo systemctl restart saslauthd postgresql postfix dovecot

Install the Mailutils package:

	:::console
	$ sudo apt-get install mailutils

Log into an email account like gmail to send an email to `kim@snorl.ax`, then check if there's any message:  

	:::console
	$ sudo mail -f /var/mail/vhosts/snorl.ax/mails/user

Now test imap using an Email Client like ThunderBird:  

* __Username:__ `user@snorl.ax`, the login name of `kim@snorl.ax`.  
* __Password:__  The one I just set, not the encrypted string. The one before being encrypted.  
* __Server name:__ `mail.snorl.ax`, or the IP address of the server.  
* __SSL:__ `None`  
* __Port:__ 143

## SMTP Method 1: SMTP Relay

An email sent from a server IP can easily go to Spam Folder if the IP reputation is bad or something is not configured correctly on the server, so it is safe to use an email delivery service.  
I've used Amazon SES and Sendgrid. Both of them perform perfectly. Amazon SES charges $0.10 for every 1,000 emails you send. Sendgrid charges at least $14.95 monthly if u exceed 100 mails/day.  
However u'll need request for a sending quota increase to get started with Amazon SES, while u can start with it as soon as u register on Sendgrid.  
The documentations below r quite useful if u r using either of the email delivery services. They clarify how to configure the service and integrate it with Postfix and email client.  

Some documentations useful for using __Sendgrid__:  

* <a href="https://sendgrid.com/docs/ui/account-and-settings/how-to-set-up-domain-authentication/" target="_blank">How to set up domain authentication</a>
* <a href="https://sendgrid.com/docs/API_Reference/SMTP_API/integrating_with_the_smtp_api.html" target="_blank">Integrating With the SMTP API</a>
* <a href="https://sendgrid.com/docs/for-developers/sending-email/postfix/" target="_blank">Integrate SendGrid with Postfix</a>

Some documentations useful for using __Amazon SES__:  

* <a href="https://docs.aws.amazon.com/ses/latest/DeveloperGuide/quick-start.html" target="_blank">Amazon SES Quick Start</a>
* <a href="https://docs.aws.amazon.com/ses/latest/DeveloperGuide/postfix.html" target="_blank">Integrating Amazon SES with Postfix</a>
* <a href="https://docs.aws.amazon.com/ses/latest/DeveloperGuide/configure-email-client.html" target="
_blank">Configuring Email Clients to Send Through Amazon SES</a>
* <a href="https://docs.aws.amazon.com/ses/latest/DeveloperGuide/mail-from.html" target="_blank">Using a Custom MAIL FROM Domain with Amazon SES</a>

## SMTP Method 2: Postfix SASL

It is generally better to use my own server to send mails if I wanna have my own business and the IP reputation starts at least neutral.  

To find out what SASL implementations are compiled into Postfix[^6], use the following commands:  

	:::console
	$ postconf -a (SASL support in the SMTP server)
	$ postconf -A (SASL support in the SMTP+LMTP client)

### Configure SSL

Generate a certificate for the domain (I use certbot) and configure postfix and dovecot to use it.

My ceritficate location:  
Cert: `/etc/letsencrypt/live/snorl.ax/fullchain.pem`  
Key: `/etc/letsencrypt/live/snorl.ax/privkey.pem`

Set the values in `/etc/postfix/main.cf`:  

	:::ini
	smtpd_tls_cert_file=/etc/letsencrypt/live/snorl.ax/fullchain.pem
	smtpd_tls_key_file=/etc/letsencrypt/live/snorl.ax/privkey.pem

Add the block into `/etc/dovecot/conf.d/10-ssl.conf`[^18]:  

	:::ini
	local_name mail.snorl.ax {
		ssl_cert = </etc/letsencrypt/live/snorl.ax/fullchain.pem
		ssl_key = </etc/letsencrypt/live/snorl.ax/privkey.pem
	}

Restart them to see the effect:  

	:::console
	$ sudo systemctl restart dovecot postfix

### Postfix to Dovecot SASL communication

It saves hassle to configure Postfix to Dovecot SASL communication.  

Relevant block in `/etc/dovecot/conf.d/10-master.conf` (to place the Dovecot SASL socket in the path and make it writable and readable by user and group `postfix` only):  

	:::ini
	service auth {
	  ...
	  unix_listener /var/spool/postfix/private/auth {
	    mode = 0660
	    # Assuming the default Postfix user and group
	    user = postfix
	    group = postfix        
	  }
	  ...
	}

Specify the following value in `/etc/dovecot/conf.d/10-auth.conf`:  

	:::ini
	auth_mechanisms = plain login

### Enabling SASL authentication in the Postfix SMTP server

Specify the following value in `/etc/postfix/main.cf`:  

	:::ini
	smtpd_sasl_type = dovecot
	smtpd_sasl_path = private/auth
	smtpd_sasl_auth_enable = yes
	broken_sasl_auth_clients = yes

### Postfix SMTP Server policy - SASL mechanism properties

Set the desired values in `/etc/postfix/main.cf`.  

Deny anonymous authentication:  

	:::ini
	smtpd_sasl_security_options = noanonymous
	smtpd_sasl_tls_security_options = $smtpd_sasl_security_options

A more sophisticated policy allows plaintext mechanisms, but only over a TLS-encrypted connection:   

	:::ini
	smtpd_sasl_security_options = noanonymous, noplaintext
	smtpd_sasl_tls_security_options = noanonymous

To offer SASL authentication only after a TLS-encrypted session has been established specify this:  

	:::ini
	smtpd_tls_auth_only = yes

### Mail relay authorization

Set the desired values in `/etc/postfix/main.cf`. With `permit_sasl_authenticated` the Postfix SMTP server can allow SASL-authenticated SMTP clients to send mail to remote destinations. Examples:  

	:::ini hl_lines="3"
	smtpd_relay_restrictions =
		permit_mynetworks
		permit_sasl_authenticated
		reject_unauth_destination
		...other rules...

### Envelope sender address authorization

In `/etc/postfix/main.cf`, configure `smtpd_sender_login_maps` and add `reject_sender_login_mismatch` before `permit_sasl_authenticated` in `smtpd_recipient_restrictions`:  

	:::ini hl_lines="1 4"
	smtpd_sender_login_maps = hash:/etc/postfix/controlled_envelope_senders
	smtpd_relay_restrictions =
		...
		reject_sender_login_mismatch
		permit_sasl_authenticated
		...

The table in `/etc/postfix/controlled_envelope_senders` should be configured like this:  

	:::ini
    # envelope sender           owners (SASL login names)
    kim@snorl.ax                user@snorl.ax
    som@snorl.ax                user1@snorl.ax

On the left is the email address, on the right is the login name.  

Generate the database:

	:::console
	$ sudo postmap /etc/postfix/controlled_envelope_senders

Now, the Postfix SMTP server knows who the sender is. Given a table of envelope sender addresses and SASL login names, the Postfix SMTP server can decide if the SASL authenticated client is allowed to use a particular envelope sender address.  

### Testing SASL authentication in the Postfix SMTP Server

To test the server side, connect (for example, with `telnet`) to the Postfix SMTP server port and you should be able to have a conversation as shown below. Information sent by the client is shown in highlighted font.  

	:::console hl_lines="1 4 11"
	$ telnet server.example.com 25
	...
	220 server.example.com ESMTP Postfix
	EHLO client.example.com
	250-server.example.com
	250-PIPELINING
	250-SIZE 10240000
	250-ETRN
	250-AUTH DIGEST-MD5 PLAIN CRAM-MD5
	250 8BITMIME
	AUTH PLAIN AHRlc3QAdGVzdHBhc3M=
	235 Authentication successful

To test this over a connection that is encrypted with TLS, use openssl s_client instead of telnet:

	:::console hl_lines="1 4"
	$ openssl s_client -connect server.example.com:25 -starttls smtp
	...
	220 server.example.com ESMTP Postfix
	EHLO client.example.com
	...see above example for more...

Use a recent version of `bash` shell and replace the `AHRlc3QAdGVzdHBhc3M=` above with the output of this command:  

	:::console
	$ echo -ne '\000username\000password' | openssl base64

### Enabling SASL authentication in the Postfix SMTP/LMTP client

Set the values in `/etc/postfix/main.cf`:  

	:::ini
	smtp_sasl_auth_enable = yes
	smtp_tls_security_level = encrypt
	smtp_sasl_password_maps = pgsql:/etc/postfix/password.cf

In `/etc/postfix/password.cf`:  

	:::ini
	user=mailreader
	password=secret
	dbname=mails
	table=users
	select_field=password
	where_field=userid
	hosts=localhost

Restart postfix to see the effect:  

	:::console
	$ sudo systemctl restart postfix

### Open the submission port

The submission port is recommended to be used for smtp.  

Uncomment the following line in `/etc/postfix/master.cf`:  

	:::ini
	submission inet n       -       y       -       -       smtpd

Restart postfix to see the effect:  

	:::console
	$ sudo systemctl restart postfix

### Configure SPF and DKIM

Install DKIM, SPF and Postfix-pcre[^7],  

	:::console
	$ sudo apt-get install opendkim opendkim-tools postfix-policyd-spf-python postfix-pcre

#### SPF

Add spf as a TXT Record to DNS:  

	snorl.ax TXT "v=spf1 mx -all"

Add the following entry to `/etc/postfix/master.cf`:  

	:::ini
	policyd-spf  unix  -       n       n       -       0       spawn
	    user=policyd-spf argv=/usr/bin/policyd-spf

Configure the following value in `/etc/postfix/main.cf`:  

	:::ini
	policyd-spf_time_limit = 3600

In `/etc/postfix/main.cf`, edit the `smtpd_relay_restrictions` entry to add a `check_policy_service` entry:  

	:::ini hl_lines="4"
	smtpd_relay_restrictions =
	    ...
	    reject_unauth_destination,
	    check_policy_service unix:private/policyd-spf,
	    ...

Make sure to add the `check_policy_service` entry after the `reject_unauth_destination` entry to avoid having your system become an open relay. If `reject_unauth_destination` is the last item in your restrictions list, add the comma after it and omit the comma at the end of the `check_policy_service` item above.  

Restart Postfix.

	:::console
	$ sudo systemctl restart postfix

Check the operation of the policy agent by looking at raw headers on incoming email messages for the SPF results header. The header the policy agent adds to messages should look something like this:  

	:::txt
	Received-SPF: Pass (sender SPF authorized) identity=mailfrom; client-ip=127.0.0.1; helo=mail.snorl.ax; envelope-from=text@snorl.ax; receiver=tknarr@silverglass.org

#### DKIM

Edit `/etc/opendkim.conf` and uncomment or edit certain lines:  

	:::ini
	# This is a basic configuration that can easily be adapted to suit a standard
	# installation. For more advanced options, see opendkim.conf(5) and/or
	# /usr/share/doc/opendkim/examples/opendkim.conf.sample.

	# Log to syslog
	Syslog          yes
	# Required to use local socket with MTAs that access the socket as a non-
	# privileged user (e.g. Postfix)
	UMask           002
	# OpenDKIM user
	# Remember to add user postfix to group opendkim
	UserID          opendkim

	# Map domains in From addresses to keys used to sign messages
	KeyTable        /etc/opendkim/key.table
	SigningTable        refile:/etc/opendkim/signing.table

	# Hosts to ignore when verifying signatures
	ExternalIgnoreList  /etc/opendkim/trusted.hosts
	InternalHosts       /etc/opendkim/trusted.hosts

	# Commonly-used options; the commented-out versions show the defaults.
	Canonicalization    relaxed/simple
	Mode            sv
	SubDomains      no
	#ADSPAction     continue
	AutoRestart     yes
	AutoRestartRate     10/1M
	Background      yes
	DNSTimeout      5
	SignatureAlgorithm  rsa-sha256

	# Always oversign From (sign using actual From and a null From to prevent
	# malicious signatures header fields (From and/or others) between the signer
	# and the verifier.  From is oversigned by default in the Debian package
	# because it is often the identity key used by reputation systems and thus
	# somewhat security sensitive.
	OversignHeaders     From


	# Socket smtp://localhost
	#
	# ##  Socket socketspec
	# ##
	# ##  Names the socket where this filter should listen for milter connections
	# ##  from the MTA.  Required.  Should be in one of these forms:
	# ##
	# ##  inet:port@address           to listen on a specific interface
	# ##  inet:port                   to listen on all interfaces
	# ##  local:/path/to/socket       to listen on a UNIX domain socket
	#
	Socket                  local:/var/spool/postfix/opendkim/opendkim.sock

	##  PidFile filename
	###      default (none)
	###
	###  Name of the file where the filter should write its pid before beginning
	###  normal operations.
	#
	PidFile               /var/run/opendkim/opendkim.pid

Ensure the permission is correctly set:  

	:::console
	$ sudo chmod u=rw,go=r /etc/opendkim.conf

Create directory for the socket:  

	:::console
	$ sudo mkdir /var/spool/postfix/opendkim
	$ chown opendkim:postfix /var/spool/postfix/opendkim

Create directory for OpenDKIM's data files:  

	:::console
	$ sudo mkdir -p /etc/opendkim/keys
	$ sudo chown -R opendkim:opendkim /etc/opendkim
	$ sudo chmod go-rw /etc/opendkim/keys

Create `/etc/opendkim/signing.table`  

	*@snorl.ax   sim

Create `/etc/opendkim/key.table`  

	sim     snorl.ax:YYYYMM:/etc/opendkim/keys/example.private

replace the `YYYYMM` with the current 4-digit year and 2-digit month (this is referred to as the selector)

Create `/etc/opendkim/trusted.hosts`

	127.0.0.1
	::1
	localhost
	sim
	sim.snorl.ax
	snorl.ax

Set the permission:  

	:::console
	$ sudo chown -R opendkim:opendkim /etc/opendkim
	$ sudo chmod -R go-rwx /etc/opendkim/keys

Generate the key:  

	:::console
	$ sudo opendkim-genkey -b 2048 -h rsa-sha256 -r -s YYYYMM -d example.com -v

Move it to the set path:  

	:::console
	$ sudo mv YYYYMM.private /etc/opendkim/keys/example.private
	$ sudo mv YYYYMM.txt /etc/opendkim/keys/example.txt

Make sure all the files in the dir have correct permissions:  

	:::console
	$ cd /etc
	$ sudo chown -R opendkim:opendkim /etc/opendkim
	$ sudo chmod -R go-rw /etc/opendkim/keys

Restart to see if there's any error:   

	:::console
	$ sudo systemctl restart opendkim

Check it if there's any error:  

	:::console
	$ sudo systemctl status -l opendkim

For example, in `/etc/opendkim/keys/example.txt`:  

	201510._domainkey  IN  TXT ( "**v=DKIM1; h=rsa-sha256; k=rsa; s=email; "
	    "p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu5oIUrFDWZK7F4thFxpZa2or6jBEX3cSL6b2TJdPkO5iNn9vHNXhNX31nOefN8FksX94YbLJ8NHcFPbaZTW8R2HthYxRaCyqodxlLHibg8aHdfa+bxKeiI/xABRuAM0WG0JEDSyakMFqIO40ghj/h7DUc/4OXNdeQhrKDTlgf2bd+FjpJ3bNAFcMYa3Oeju33b2Tp+PdtqIwXR"
	    "ZksfuXh7m30kuyavp3Uaso145DRBaJZA55lNxmHWMgMjO+YjNeuR6j4oQqyGwzPaVcSdOG8Js2mXt+J3Hr+nNmJGxZUUW4Uw5ws08wT9opRgSpn+ThX2d1AgQePpGrWOamC3PdcwIDAQAB**" )  ; ----- DKIM key 201510 for example.com

The value inside the parentheses is needed. Select and copy the entire region from (but not including) the double-quote before v=DKIM1 on up to (but not including) the final double-quote before the closing parentheses. Then edit out the double-quotes within the copied text and the whitespace between them. Also change h=rsa-sha256 to h=sha256. From the above file the result would be:  

	v=DKIM1; h=sha256; k=rsa; s=email; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu5oIUrFDWZK7F4thFxpZa2or6jBEX3cSL6b2TJdPkO5iNn9vHNXhNX31nOefN8FksX94YbLJ8NHcFPbaZTW8R2HthYxRaCyqodxlLHibg8aHdfa+bxKeiI/xABRuAM0WG0JEDSyakMFqIO40ghj/h7DUc/4OXNdeQhrKDTlgf2bd+FjpJ3bNAFcMYa3Oeju33b2Tp+PdtqIwXRZksfuXh7m30kuyavp3Uaso145DRBaJZA55lNxmHWMgMjO+YjNeuR6j4oQqyGwzPaVcSdOG8Js2mXt+J3Hr+nNmJGxZUUW4Uw5ws08wT9opRgSpn+ThX2d1AgQePpGrWOamC3PdcwIDAQAB

Paste that into the value for the TXT record in DNS:

	201510._domainkey.snorl.ax	 TXT  The_Value

Test the key:  

	:::console
	$ opendkim-testkey -d snorl.ax -s YYYYMM

To hook it into the postfix, edit `/etc/postfix/main.cf`:  

	:::ini
	# OpenDKIM
	milter_default_action = accept
	# Postfix ≥ 2.6 milter_protocol = 6, Postfix ≤ 2.5 milter_protocol = 2
	milter_protocol = 6
	smtpd_milters = local:opendkim/opendkim.sock
	non_smtpd_milters = $smtpd_milters

Add user postfix to group opendkim:  

	:::console
	$ sudo usermod -a -G opendkim postfix

Restart them.  

	:::console
	$ sudo systemctl restart opendkim postfix

Verify if everything’s working by sending a test e-mail to `check-auth@verifier.port25.com` using an email client configured to submit mail to the submission port on the mail server.

### Set up Domain Message Authentication, Reporting & Conformance (DMARC)

Add the following TXT record in DNS:  

	_dmarc.snorl.ax	TXT	v=DMARC1;p=quarantine;sp=quarantine;adkim=r;aspf=r;fo=1;rf=afrf;rua=mailto:admin@snorl.ax

This requests mail servers to quarantine (do not discard, but separate from regular messages) any email that fails either SPF or DKIM checks. The report will be `admin@snorl.ax`.

### Optional: Set up Author Domain Signing Practices (ADSP)

Add an ADSP policy to the domain saying that all emails from the domain should be DKIM-signed:  

	_adsp._domainkey.snorl.ax	TXT	dkim=all

### Key Rotation

The reason the YYYYMM format is used for the selector is that best practice calls for changing the DKIM signing keys every so often (monthly is recommended, and no longer than every 6 months).

Generate it in my home dir:  

	:::console
	$ opendkim-genkey -b 2048 -h rsa-sha256 -r -s YYYYMM -d snorl.ax -v

Set the DNS the way it is done above, test it:

	:::console
	$ opendkim-testkey -d example.com -s YYYYMM -k example.private

Stop opendkim for a moment:  

	:::console
	$ sudo systemctl stop opendkim

Copy it to the path:

	:::console
	$ cp *.private /etc/opendkim/keys/
	$ chown opendkim:opendkim /etc/opendkim/keys/*
	$ chmod go-rw /etc/opendkim/keys/*

Edit `/etc/opendkim/key.table` and change the old YYYYMM values to the new selector, reflecting the current year and month. Save the file. Then restart postfix and opendkim to see the effect. Be sure to delete the old `YYYYMM._domainkey` TXT record.

## Improve The Password Encryption

`CRYPT` is weak, only uses the first 8 characters of the password, the rest are ignored.  
`CRAM-MD5` protects the password in transit against eaves droppers and somewhat gets good support in clients.  
So it's the default method doveadm uses[^13][^14]. To generate a CRAM-MD5 for a password:  

	:::console
	$ doveadm pw

Enter the password twice:  

	Enter new password:
	Retype new password:

Then a hash like this will be generated and printed:  

	:::console
	{CRAM-MD5}26b633ec8bf9dd526293c5897400bddeef9299fad

To do something with the password, access the `psql` utility again:  

	:::console
	$ sudo su postgres
	$ psql mails

To check the existing user:  

	SELECT * FROM users;

A table like this will be shown:  

	:::ini
	     userid     |       password       | realname | uid  | gid  |         home         | mail
	----------------+----------------------------------------------------------------------------+----------+------+------+----------------------+------
	 user1@snorl.ax | {CRYPT}xxxxxxxxxxxxx |          | 5000 | 5000 | snorl.ax/mails/user1 |
	 user@snorl.ax  | {CRYPT}xxxxxxxxxxxxx |          | 5000 | 5000 | snorl.ax/mails/user  |

To check the correspondence between username and mail address:  

	SELECT * FROM virtual;

A table similar to the following one will be shown:  

	:::ini
	    address     |     userid     
	----------------+----------------
	 xxxx@snorl.ax  | user@snorl.ax
	 xxx@snorl.ax   | user2@snorl.ax
	 xxxx@snorl.ax  | user@snorl.ax

To update an existing user with the password:  

	UPDATE users SET password='{CRAM-MD5}26b633ec8bf9dd526293c5897400bddeef9299fad' WHERE userid='user@snorl.ax';

In `/etc/dovecot/conf.d/10-auth.conf`, disable plaintext login and add cram-md5 to the mechanisms:  

	:::ini hl_lines="2 4"
	...
	disable_plaintext_auth = yes
	...
	auth_mechanisms = plain login cram-md5

In `/etc/postfix/sasl/smtpd.conf`, set the corresponding option to include `cram-md5`:  

	mech_list: login plain cram-md5

In `/etc/pam_pgsql.conf`, set it to cram-md5:  

	:::ini hl_lines="2"
	...
	pw_type = cram-md5
	...

In `/usr/local/etc/dovecot-sql.conf`, set it to cram-md5:  

	:::ini hl_lines="2"
	...
	default_pass_scheme = CRAM-MD5
	...

Then test logging in with `encrypted password` over SSL in imap and STARTTLS in smtp.   

## Testing SMTP

Test sending mail outside of my mail server, like a Gmail account.  

	:::console
	$ echo "Email body text" | sudo mail -s "Email subject line" recipient@gmail.com -aFrom:kim@snorl.ax

Sometimes if I test sending while having the `@snorl.ax` omitted, like this:  

	:::console
	$ echo "Email body text" | sudo mail -s "Email subject line" recipient@gmail.com -aFrom:kim

The mail sender will be `kim@mail.snorl.ax` instaed, due to the default behaviour that mailutils append the hostname to usernames like this. Then the mail will be sent to `/var/mail/kim` instead. To change the appended domain to the desired `@snorl.ax`, create `/etc/mailutils.conf` with the setting:  

	:::ini
	address {
	  email-domain snorl.ax;
	};

Other configurable options can be seen via `$ mail --config-help`.  

Now test SMTP using an Email Client like ThunderBird:  

* __Username:__ `user@snorl.ax`, the login name of `kim@snorl.ax`.  
* __Password:__  The one I set above, not the encrypted string. The one before being encrypted.  
* __Server name:__ `mail.snorl.ax`, or the IP address of the server.  
* __SSL:__ `StartTls`  
* __Port:__ 587

## Block some Brute Forcers

Try looking into `/var/log/mail.log`:  

	:::console
	Jan 18 15:22:14 snorlax dovecot: auth-worker(5228): pam(tyler@snorl.ax,37.49.224.186): pam_authenticate() failed: Authentication failure (password mismatch?)

It's normal that some IP I've never known keeps brute-forcing. Neither do I use any IP from that IP range.

Install the package to make the change permanent.  

	:::console
	$ sudo apt-get install iptables-persistent

In this case, block the ip range might be a good idea:  

	:::console
	$ sudo iptables -A INPUT -s 37.49.224.0/24 -j DROP

## Hide sender's IP in the sent mail's header

I'm using submission port. Uncomment and add and edit the relevant lines in `/etc/postfix/master.cf`, the relevant lines should look like this[^9]:   

	:::ini
	submission inet n       -       -       -       -       smtpd
	  -o smtpd_tls_security_level=encrypt
	  -o smtpd_sasl_auth_enable=yes
	  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
	  -o milter_macro_daemon_name=ORIGINATING
	  -o cleanup_service_name=subcleanup

Pass `header_checks` to the new cleanup service in `/etc/postfix/master.cf`, relevant lines look like this:  

	:::ini
	cleanup   unix  n       -       -       -       0       cleanup
	subcleanup unix n       -       -       -       0       cleanup
	  -o header_checks=regexp:/etc/postfix/submission_header_checks

Create the file `/etc/postfix/submission_header_checks`, which will contain the regex that filters offending Received header lines.  

If `smtpd_sasl_authenticated_header` is `yes`, then use this in the file:  

	:::ini
	/^Received:.*\(Authenticated sender:/ IGNORE

Otherwise(also by default when `smtpd_sasl_authenticated_header` is not set), use this in the file:  

	:::ini
	/^Received:.*\(Postfix/ IGNORE

Restart postfix to see the effect.

## Integrate Spamassassin

It's one of the most well-known mail spam filters. Speaking of spam filter, it can be regarded as the most mentioned[^15][^17].  

Install Spamassassin and its dependencies and dovecot-sieve.  

	:::console
	$ sudo apt install spamassassin spamc dovecot-sieve

Start the service and enable it.

	:::console
	$ sudo systemctl start spamassassin
	$ sudo systemctl enable spamassassin

Modify `/etc/postfix/master.cf`:  

1. Change the smtp line to:  

		:::ini
		smtp      inet  n       -       -       -       -       smtpd -o content_filter=spamassassin

2. Add the following (a call to our newly-created spamfilter script) at the end:  

		:::ini
		spamassassin unix -     n   n   -   -   pipe
		    flags=ROhu user=vmail:vmail argv=/usr/bin/spamc -f -e
		    /usr/lib/dovecot/deliver -f ${sender} -d ${user}@${nexthop}

	The flags flags=ROhu don't add anything abnormal but they can be understood [here](http://www.postfix.org/pipe.8.html).  

Modify `/etc/mail/spamassassin/local.cf` to include the following settings:  

	:::ini
	# Just add an X-Spam-Report header to suspected spam, rather than rewriting the content of the e-mail
	report_safe 0
	# Also we want to add a detailed ham report header to even e-mail that ISN'T suspected to be spam
	add_header ham HAM-Report _REPORT_
	# Set the threshold at which a message is considered spam (3 is usually sufficient)
	required_score 3.0

Modify `/etc/dovecot/conf.d/15-mailboxes.conf` to ensure the following lines are included(By default they are included):  

	:::ini
	mailbox Junk {
	   special_use = \Junk
	}

Edit `/etc/dovecot/conf.d/90-sieve.conf` and comment the line `sieve = ~/.dovecot.sieve`, like this:  

	:::ini hl_lines="4"
	...
	plugin {
	...
	#sieve = file:~/sieve;active=~/.dovecot.sieve

Edit `/etc/dovecot/conf.d/90-plugin.conf` as:  

	:::ini hl_lines="4"
	...
	plugin {
		...
		sieve = /etc/dovecot/sieve/default.sieve
	}

Edit `/etc/dovecot/conf.d/15-lda.conf`:  

	:::ini hl_lines="2"
	protocol lda {
		mail_plugins = $mail_plugins sieve
	}

Create folder `/etc/dovecot/sieve/`:  

	:::console
	$ mkdir /etc/dovecot/sieve/

Create file `/etc/dovecot/sieve/default.sieve` with this content:  

	require "fileinto";
	if header :contains "X-Spam-Flag" "YES" {
	    fileinto "Junk";
	}

Change the folder permissions to the virtual email user and group like:  

	:::console
	$ chown vmail:vmail /etc/dovecot/sieve/ -R

Restart postfix, dovecot and spamassassin.  

	:::console
	$ sudo systemctl restart spamassassin dovecot postfix

Try sending a mail to the mail account. The output of `tail /var/log/mail.log` will be like:  

	Jan 25 13:54:47 pelipper postfix/qmgr[23283]: 9C2C5DBBA7: from=<yumsnorlax@gmail.com>, size=3031, nrcpt=1 (queue active)
	Jan 25 13:54:47 pelipper spamd[23286]: spamd: connection from ::1 [::1]:33756 to port 783, fd 5
	Jan 25 13:54:47 pelipper spamd[23286]: spamd: setuid to vmail succeeded
	Jan 25 13:54:47 pelipper spamd[23286]: spamd: creating default_prefs: /var/mail/.spamassassin/user_prefs
	Jan 25 13:54:47 pelipper spamd[23286]: config: created user preferences file: /var/mail/.spamassassin/user_prefs
	Jan 25 13:54:47 pelipper spamd[23286]: spamd: processing message <1548420881.1041.0@gmail.com> for vmail:5000
	Jan 25 13:54:47 pelipper postfix/smtpd[23313]: disconnect from mail-pg1-x530.google.com[2607:f8b0:4864:20::530] ehlo=2 starttls=1 mail=1 rcpt=1 data=1 quit=1 commands=7
	Jan 25 13:54:49 pelipper spamd[23286]: spamd: clean message (0.9/3.0) for vmail:5000 in 2.7 seconds, 3164 bytes.
	Jan 25 13:54:49 pelipper spamd[23286]: spamd: result: . 0 - DKIM_SIGNED,DKIM_VALID,DKIM_VALID_AU,DKIM_VALID_EF,FREEMAIL_FROM,HTML_MESSAGE,RCVD_IN_DNSWL_NONE,SPF_PASS,TRACKER_ID,TVD_SPACE_RATIO scantime=2.7,size=3164,user=vmail,uid=5000,required_score=3.0,rhost=::1,raddr=::1,rport=33756,mid=<1548420881.1041.0@gmail.com>,autolearn=no autolearn_force=no
	Jan 25 13:54:49 pelipper dovecot: lda(user2@snorl.ax): sieve: msgid=<1548420881.1041.0@gmail.com>: stored mail into mailbox 'INBOX'
	Jan 25 13:54:49 pelipper postfix/pipe[23326]: 9C2C5DBBA7: to=<user2@snorl.ax>, orig_to=<kim@snorl.ax>, relay=spamassassin, delay=3.3, delays=0.58/0.01/0/2.7, dsn=2.0.0, status=sent (delivered via spamassassin service)
	Jan 25 13:54:49 pelipper postfix/qmgr[23283]: 9C2C5DBBA7: removed

Try sending another mail with this subject: `XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X`. The output of `tail /var/log/mail.log` will be like this:  

	Jan 25 13:56:31 pelipper postfix/qmgr[23283]: 43CFADBBA7: from=<yumsnorlax@gmail.com>, size=3103, nrcpt=1 (queue active)
	Jan 25 13:56:31 pelipper spamd[23286]: spamd: connection from ::1 [::1]:33770 to port 783, fd 5
	Jan 25 13:56:31 pelipper spamd[23286]: spamd: setuid to vmail succeeded
	Jan 25 13:56:31 pelipper spamd[23286]: spamd: processing message <1548420985.1041.1@gmail.com> for vmail:5000
	Jan 25 13:56:31 pelipper postfix/smtpd[23334]: disconnect from mail-pl1-x62d.google.com[2607:f8b0:4864:20::62d] ehlo=2 starttls=1 mail=1 rcpt=1 data=1 quit=1 commands=7
	Jan 25 13:56:33 pelipper spamd[23286]: spamd: identified spam (999.8/3.0) for vmail:5000 in 2.4 seconds, 3235 bytes.
	Jan 25 13:56:33 pelipper spamd[23286]: spamd: result: Y 999 - DKIM_SIGNED,DKIM_VALID,DKIM_VALID_AU,DKIM_VALID_EF,FREEMAIL_FROM,GTUBE,HTML_MESSAGE,RCVD_IN_DNSWL_NONE,SPF_PASS,TVD_SPACE_RATIO scantime=2.4,size=3235,user=vmail,uid=5000,required_score=3.0,rhost=::1,raddr=::1,rport=33770,mid=<1548420985.1041.1@gmail.com>,autolearn=no autolearn_force=no
	Jan 25 13:56:33 pelipper dovecot: lda(user2@snorl.ax): sieve: msgid=<1548420985.1041.1@gmail.com>: stored mail into mailbox 'Junk'
	Jan 25 13:56:34 pelipper postfix/pipe[23343]: 43CFADBBA7: to=<user2@snorl.ax>, orig_to=<kim@snorl.ax>, relay=spamassassin, delay=2.9, delays=0.46/0.01/0/2.4, dsn=2.0.0, status=sent (delivered via spamassassin service)
	Jan 25 13:56:34 pelipper postfix/qmgr[23283]: 43CFADBBA7: removed

The spam filter is now working. A spam will go directly into the Junk Folder.  

### Solve URIBL_BLOCKED

	X-Spam-HAM-Report:
		*  0.0 URIBL_BLOCKED ADMINISTRATOR NOTICE: The query to URIBL was
		*      blocked.  See
		*      http://wiki.apache.org/spamassassin/DnsBlocklists#dnsbl-block
		*      for more information.

SpamAssassin will perform many DNS lookups for NetworkTests to significantly improve scoring of messages primarily by DNSBlocklists like Spamhaus, SORBS, etc. This information needs to be cached locally to improve performance and limit the number of external DNS queries since some DNSBlockLists have limits on free usage. A local DNS caching server should not forward to other DNS servers to ensure your queries are not combined with others. Forwarding to other DNS servers often results in URIBL_BLOCKED or similar rule hits meaning you have gone over their free usage limit.[^16]  

	:::console
	$ sudo apt-get update
	$ sudo apt-get install unbound

Then it is running and the corresponding service is enabled.  
Add this to `/etc/spamassassin/local.cf`:  

	dns_available yes
	dns_server 127.0.0.1

Test it out. With these output it's now working.  

Spamhaus Zen:  

	:::console
	$ dig +short 2.0.0.127.zen.spamhaus.org @127.0.0.1
	127.0.0.10
	127.0.0.4
	127.0.0.2

SORBS DUL:

	:::console
	$ dig 2.0.0.127.dul.dnsbl.sorbs.net +short @127.0.0.1
	127.0.0.10

URIBL:

	:::console
	$ dig test.uribl.com.multi.uribl.com txt +short @127.0.0.1
	"permanent testpoint"

[^1]: [HowTo/DovecotPostgresql - Dovecot Wiki](https://wiki2.dovecot.org/HowTo/DovecotPostgresql)
[^2]: [Email with Postfix, Dovecot, and MySQL - Linode](https://www.linode.com/docs/email/postfix/email-with-postfix-dovecot-and-mysql/)
[^3]: [Debian Backports - Instructions](https://backports.debian.org/Instructions/)
[^4]: [centos - How do I change Dovecot virtual user passwords? - Server Fault](https://serverfault.com/a/440616)
[^5]: [BasicConfiguration - Dovecot Wiki](https://wiki.dovecot.org/BasicConfiguration)
[^6]: [Postfix SASL Howto](http://www.postfix.org/SASL_README.html)
[^7]: [Configure SPF and DKIM With Postfix on Debian 9](https://www.linode.com/docs/email/postfix/configure-spf-and-dkim-in-postfix-on-debian-9/)
[^9]: [When sending email with Postfix, how can I hide the sender’s IP and username in the Received header?](https://askubuntu.com/a/78168)
[^10]: [Checking FQDN, Reverse-DNS/PTR, MX record](https://easyengine.io/tutorials/mail/fqdn-reverse-dns-ptr-mx-record-checks)
[^12]: [Postfix Configuration Parameters](http://www.postfix.org/postconf.5.html)
[^13]: [HowToCRAM/MD5 - Dovecot Wiki](https://wiki.dovecot.org/HowTo/CRAM-MD5)
[^14]: [Authentication/PasswordSchemes - Dovecot Wiki](https://wiki1.dovecot.org/Authentication/PasswordSchemes)
[^15]: [IntegratedSpamdInPostfix - Spamassassin Wiki](https://wiki.apache.org/spamassassin/IntegratedSpamdInPostfix)
[^16]: [CachingNameserver - Spamassassin Wiki](https://wiki.apache.org/spamassassin/CachingNameserver)
[^17]: [postfix mta - How to move spam to spam folder? - Stack Overflow](https://stackoverflow.com/a/34571858/9850945)
[^18]: [SSL/DovecotConfiguration - Dovecot Wiki](https://wiki.dovecot.org/SSL/DovecotConfiguration)
[^19]: [Rejecting Unknown Local Recipients with Postfix](http://www.postfix.org/LOCAL_RECIPIENT_README.html#format)
