# Linux Server Configuration

Baseline linux server using Amazon Lightsail prepared to host web applications.
The server will be secured using a firewall with a configured database.
This server is than used to host a previous Udacity web application.

## Server Specifics

URL: <br/>

IP: <br/>

SSH Port: 2200 <br/>
HTTP Port: 80 <br/>
NTP Port: 123 <br/>

## Package Install from Ubuntu (See packages.ubuntu.com for descriptions)

`sudo apt-get install

`sudo apt-get install finger`
`sudo apt-get install apache2`
`sudo apt-get install libapache2-mod-wsgi`
`sudo apt-get install postgresql`

Note: After modifying the WSGIScriptAlias, restart Apache <br/>
`sudo apache2ctl restart`

### Create postgresql user

`sudo -u postgres createuser -P grader`

### Create empty DB

`sudo -u postgres createdb -O grader catalogDB`

Note: You can view all the databases using the command below:

`psql -U 'USER' -l`

## User Management

Added user grader <br/>
`sudo adduser grader` <br/>

Giving grader sudo permission <br/>
`sudo usermod -aG sudo grader`<br/>

Confirm user with Finger <br/>
`finger grader`<br/>

Note: Remote login for user root is disabled

## Installing Public Key

`mkdir .ssh`
`touch .ssh/authorized_keys`
`nano .ssh/authorized_keys`
`chmod 700 .ssh`
`chmod 644 .ssh/authorized_keys`

## Install Flask and SQLAlchemy


## Timezone

## Update and Upgrades

`sudo apt-get update` <br/>
`sudo apt-get upgrade`

## Remove Unrequired packages

`sudo apt-get autoremove`












