#!python3
import json
import conf as c
import zenpy as zp
import sys

if len(sys.argv) < 4:
	print('Error: expected three arguments: Zendesk subdomain, action and trigger message')
	exit(-1)

zendesk_subdomain = sys.argv[1]
action = sys.argv[2]
json_payload = sys.argv[3]

def map_priority(zabbix_severity):
	if zabbix_severity == 'Warning':
		return 'low'
	elif zabbix_severity == 'Average':
		return 'normal'
	elif zabbix_severity == 'High':
		return 'high'
	elif zabbix_severity == 'Disaster':
		return 'urgent'
	else:
		return 'normal'

zabbix_body = json.loads(json_payload)

if 'event_name' not in zabbix_body.keys():
	# not recoverable.. you need at least the event name
	print('Error: event_name missing from JSON object')
	exit(-1)

if action == 'create_ticket':
	ticket_body = {}
	ticket_body['tags'] = ['Zabbix']

	ticket_body['subject'] = zabbix_body['event_name']
	ticket_body['description'] = zabbix_body['event_name']

	if 'event_severity' in zabbix_body.keys():
		ticket_body['priority'] = map_priority(zabbix_body['event_severity'])

	if 'host_name' in zabbix_body.keys():
		ticket_body['tags'].append(zabbix_body['host_name'])

	zp_client = zp.Zenpy(**c.configurations[zendesk_subdomain]['zendesk_instance'])

	ticket_body['requester'] = zp_client.users(id=int(c.configurations[zendesk_subdomain]['zabbix_user_id']))

	ticket = zp.lib.api_objects.Ticket(**ticket_body)
	zp_client.tickets.create(ticket)
elif action == 'solve_ticket':
	for ticket in zp_client.search(type='ticket',status_less_than='solved',subject=zabbix_body['event_name']):
		ticket.status = 'solved'
		zp_client.tickets.update(ticket)
else:
	print('Error: Unknown action: ' + action)
	exit(-1)
