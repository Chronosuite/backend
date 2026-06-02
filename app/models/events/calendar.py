from urllib.parse import quote, unquote

from app.models.database import db
from app.models.classes import Calendar, Event
from app.models.auth import sessions


# Fetch user's calendars
def getCalEvents(sessID: str) -> dict[str[int, Calendar | Event]]:
	"""
	Retrieve the calendars and events a user has access to in class format
	
	Return Format: 
	{
		'calendars' : {
				1: Calendar()
			},
		'events': {
				1: Event()
			}
	}
	"""

	# Get UUID
	user = sessions.getSession(sessID)
	uuid = user['id']
	email = user['email']

	# Get calendars with direct access
	calendarsRawDirect = db().fetch(f"""
		SELECT id, name, color FROM cal
		WHERE owner='{uuid}';
	""")

	calendars = {}
	events = {}

	# Create calendar objects
	for id, name, color in calendarsRawDirect:
		newCal = Calendar(int(id), name, uuid, color)
		calendars[int(id)] = newCal

	# Get calendars with access
	calendarsIds = db().fetch(f"""
		SELECT calendar FROM cal_share
		WHERE user='{uuid}';
	""")
	
	# Parse and create calendar objects
	for calId in calendarsIds:
		newCalRaw = db().fetch(f"""
			SELECT name, owner, color FROM cal
			WHERE id={calId};
		""")[0]

		newCal = Calendar(int(calId), newCalRaw[0], newCalRaw[1], newCalRaw[2])
		calendars[int(calId)] = newCal

		# Retrieve calendar's events
		calEventsRaw = db().fetch(f"""
			SELECT id, name, descr, starttime, endtime, all_day FROM cal_events
			WHERE calendar={calId};
		""")

		calEvents = []

		for id, name, descr, starttime, endtime, allDay in calEventsRaw:
			newEvent = Event(id, int(calId), name, descr, starttime, endtime, allDay, calID=int(calId))
			events[int(id)] = newEvent

			calEvents.append(newEvent)
		
		calendars[int(calId)].events = calEvents

	# Get indirectly added events
	eventsRaw = db().fetch(f"""
		SELECT event FROM cal_events_share
		WHERE email='{email}';
	""")

	for eventId in eventsRaw:
		if eventId not in list(events.keys()):
			event = db().fetch(f"""
				SELECT calendar, name, descr, starttime, endtime, all_day, linked_task FROM cal_events
				WHERE id={eventId};
			""")[0]

			newEvent = Event(int(eventId), event[1], event[2], event[3], event[4], event[5], calID=int(event[0]), linkedTaskID=int(event[6]))
			events[int(eventId)] = newEvent

	# Retrieve event attendance lists
	for eventId, event in events.items():
		attendees = db().fetch(f"""
			SELECT email FROM cal_events_share
			WHERE event={eventId};
		""")

		for attendee in attendees:
			events[eventId].attendees.append(attendee[0])

	# Return results
	return {
		'calendars': calendars,
		'events': events
	}
