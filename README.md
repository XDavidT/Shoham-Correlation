# Shoham SIEM System: Correlation

## What it does ?
The main core of the Siem system: check the new logs in the DB and check if they are violted the policy that configured in Admin Panel.
Check by time range. In global scope checking a lot of violted devices, and in local - check if one device violet given rule. When rule is violted, it been alerted by email and reported by DB to relevante table.

## How to use ?
Checkout *setting/base-setting.json*, in that file you can update the DB server.
Please do not change db/collection names, since other projects use it in that way.

Checkout *setting/alert-setting.json*, in that file you can update the email account to send alerts, or to add other account to alerting.

Tested on 'CentOS 7' with python3, but you can run it in any other OS you want.
Clone it to your machine, then run `python3 MainService.py`
