# zabbix_zendesk_alerts
Alertscript for creating tickets in Zendesk from Zabbix problems.

# Setup
## Zabbix
### Media type

Create a new media type with the following values:  

**Name:** Zendesk  
**Type:** Script  
**Script name:** zendesk_alert.py  
**Script parameters:** {ALERT.SENDTO}, {ALERT.SUBJECT}, {ALERT.MESSAGE} (in that order)  

### User

Create a new user for each zendesk instance you will connect with. Let's say your Zendesk domain is your_zendesk_subdomain.zendesk.com  
User values:

**Alias:** Zendesk (your_zendesk_subdomain)  
**Groups:** whatever groups you need for the correct permissions  

Under the media tab, click Add and fill in the following values:  
**Type:** Zendesk  
**Send to:** your_zendesk_subdomain  

### Action
Create a new action with the following values:  
**Name:** Create Zendesk ticket (your_zendesk_subdomain)

Under the Operations tab:  
**Default subject:** create_ticket  
**Default message:**  
```
{  
    "event_name": "{EVENT.NAME}",  
    "event_severity": "{EVENT.SEVERITY}",  
    "host_name": "{HOST.NAME}"  
}
```

In the Operations section, click New.  
**Operation type:** Send message  
**Send to users:** Zendesk (your_zendesk_subdomain)  
**Send only to:** Zendesk  

Remember to click Add to actually add it.

Under the Recovery operations, it's identical as Operations, except the subject should be solve_ticket.
