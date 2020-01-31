#!/usr/bin/python3

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
	ticket = zp.lib.api_objects.Ticket(subject=message, description=message, requester=zp.lib.api_objects.User(name='Zabbix'))
	zp_client.tickets.create(ticket)
elif action == 'solve_ticket':
	for ticket in zp_client.search(type='ticket',status_less_than='solved',subject=message):
		ticket.status = 'solved'
		zp_client.tickets.update(ticket)
else:
	print('Error: Unknown action: ' + action)
	exit(-1)
