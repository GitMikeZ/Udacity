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

### Package Install (See packages.ubuntu.com)

--sudo apt-get install finger

## User Management

Added User grader <br/>
--sudo adduser grader <br/>

Confirm User with Finger <br/>
--finger grader

grader SSH key: <br/>

Note: Remote login for user root is disabled

## Timezone

## Update and Upgrades

--sudo apt-get update <br/>
--sudo apt-get upgrade

## Remove Unrequired packages

--sudo apt-get autoremove












