import conf as c
import zenpy as zp
import sys

if len(sys.argv) < 4:
	print('Error: expected three arguments: Zendesk instance, action and trigger message')
	exit(-1)

zendesk_instance = sys.argv[1]
action = sys.argv[2]
message = sys.argv[3]

zp_client = zp.Zenpy(**c.zendesk_instances[zendesk_instance])

if action == 'create_ticket':
	ticket = zp.lib.api_objects.Ticket(description=message)
	ticket.tags.extend(['created_from_zabbix'])
	zp_client.tickets.create(ticket)
else:
	print('Error: Unknown action: ' + action)
