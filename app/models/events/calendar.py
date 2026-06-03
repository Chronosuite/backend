from urllib.parse import quote, unquote
from datetime import datetime

from app.models.database import db
from app.models.classes import Calendar, Event
from app.models.auth import sessions
from app.utils.exceptions import NoAccess


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


# ==============
# === EVENTS ===
# ==============

# Determine edit access
def canModify(uuid: str, linkedID: int, forCal: bool = True) -> None:
	"""
	Determine if the user can modify the calendar or task category

	If forCal is true then means this event is linked to a calendar (linkedID references calendar) otherwise linkedID references tasks 
	
	Raises exception if no
	"""

	# Check if user has access to calendar/task category
	if forCal:
		# If adding to calendar, then determine if user owns
		userCalsIncl = db().fetch(f"""
			SELECT id FROM cal
			WHERE owner='{uuid}' AND id={linkedID};
		""")

		# Determine if calendar is owned by user
		if len(userCalsIncl) == 0:
			# If not, then check if shared with user
			userSharedCals = db().fetch(f"""
				SELECT id FROM cal_share
				WHERE calendar={linkedID} AND user='{uuid}';
			""")

			if len(userSharedCals) == 0:
				raise NoAccess()
	else:
		# If adding to tasks, determine if user part of category
		userTasksIncl = db().fetch(f"""
			SELECT id FROM tasks_categories
			WHERE owner='{uuid}' AND id={linkedID};
		""")

		# Determine if calendar is owned by user
		if len(userTasksIncl) == 0:
			# If not, then check if shared with user
			userSharedCats = db().fetch(f"""
				SELECT id FROM tasks_category_share
				WHERE task_category={linkedID} AND user='{uuid}';
			""")

			if len(userSharedCats) == 0:
				raise NoAccess()


# Create event
def createEvent(sessID: str, name: str, descr: str, linkedID: int, starttime: datetime, endtime: datetime, allDay: bool, forCal: bool = True) -> int:
	"""
	Create an event

	If forCal is true then means this event is linked to a calendar (linkedID references calendar) otherwise linkedID references tasks 

	Returns eventID
	TODO: decide if wanna return a class obj instead
	"""

	# Get user to ensure valid
	uuid = sessions.getSession(sessID)['id']

	canModify(uuid, linkedID, forCal) # Determine if has access

	# Get table to insert linkedID into
	selectedTable = 'calendar' if forCal else 'linked_task'

	# Create event in DB
	eventID = db().modifyAndReturn("""
		INSERT INTO cal_events (%s, name, descr, starttime, endtime, all_day)
		VALUES (%s, %s, %s, %s, %s, %s)
		RETURNING id;
	""", (selectedTable, linkedID, name, descr, starttime, endtime, allDay))

	return int(eventID)


# Delete event
def deleteEvent(sessID: str, eventID: int) -> None:
	"""
	Delete an event given its ID

	TODO: decide if eventID should really be UUID since it might be sent to client side for storing
	"""

	# Get user to ensure valid
	uuid = sessions.getSession(sessID)['id']

	# Determine forCal and LinkedID
	event = db().fetch("""
		SELECT calendar, linked_task FROM cal_events
		WHERE id=%s;
	""", (eventID,))

	if type(event[0]) is int:
		forCal = True
		linkedID = event[0]
	else:
		forCal = False
		linkedID = event[1]

	canModify(uuid, linkedID, forCal) # Determine if has access

	# Create event in DB
	db().modify(f"""
		DELETE FROM cal_events
		WHERE id={eventID};
	""")


# Modify event
def modifyEvent(sessID: str, eventID: int, name: str, descr: str, starttime: datetime, endtime: datetime, allDay: bool) -> None:
	"""
	Modify an event given its ID

	TODO: decide if eventID should really be UUID since it might be sent to client side for storing
	"""

	# Get user to ensure valid
	uuid = sessions.getSession(sessID)['id']

	# Determine forCal and LinkedID
	event = db().fetch("""
		SELECT calendar, linked_task FROM cal_events
		WHERE id=%s;
	""", (eventID,))

	if type(event[0]) is int:
		forCal = True
		linkedID = event[0]
	else:
		forCal = False
		linkedID = event[1]

	canModify(uuid, linkedID, forCal) # Determine if has access

	# Get table to insert linkedID into
	selectedTable = 'calendar' if forCal else 'linked_task'

	# Modify event
	db().modify("""
		UPDATE cal_events
		SET %s = %s, 
			name = %s,
			descr = %s,
			starttime = %s,
			endtime = %s,
			all_day = %s
		WHERE id = %s;
	""", (
			selectedTable, linkedID,
			name,
			descr,
			starttime,
			endtime,
			allDay,
			eventID
		))
