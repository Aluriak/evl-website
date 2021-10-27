"""Read a targeted remote CALDAV, and generates a markdown page
that pelican can translate into a blog page.

"""

import os
import configparser
from caldav import DAVClient
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from collections import namedtuple


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__)).rstrip('/') + '/'
CALDAV_ACCESS_INI_FILE = SCRIPT_PATH + 'caldav-access.ini'
CALDAV_ACCESS_INI_FILE_TEMPLATE = SCRIPT_PATH + 'caldav-access-template.ini'
EVLEvent = namedtuple('EVLEvent', 'title, image, description, location, start, end, wholeday')

def read_caldav_access():
    config_parser = configparser.ConfigParser()
    config_parser.read(CALDAV_ACCESS_INI_FILE)
    config = config_parser[config_parser.default_section]
    return config['url'], config['calendar'], config['username'], config['password']

try:
    URL, CAL, USERNAME, PASSWORD = read_caldav_access()
except Exception as err:
    print(f"Invalid config file {CALDAV_ACCESS_INI_FILE}: {repr(err)}")
    print("It must look like the provided template ({CALDAV_ACCESS_INI_FILE_TEMPLATE}):\n")
    with open(CALDAV_ACCESS_INI_FILE_TEMPLATE) as fd:
        print(''.join('\t'+line.strip()+'\n' for line in fd.readlines()))
    print("\nAbort.")
    exit(1)



def events_from_calendar(calendar: 'caldav.Calendar') -> [Event]:
    for event in calendar.events():
        event = Event.from_ical(event.data)  # transform it into a icalendar.Event object
        assert isinstance(event, Calendar)   # that's a weirdness of icalendar package: the Event object is hidden into a Calendar object
        event = next((e for e in event.walk() if isinstance(e, Event)), None)  # let's get the Event inside
        assert isinstance(event, Event)
        yield event

def get_evl_events(max_events: int = 5, only_events_of_a_few_days_old_max: bool = False, only_the_last_five: bool = False):
    client = DAVClient(URL, username=USERNAME, password=PASSWORD)
    calendar = next((calendar for calendar in client.principal().calendars() if calendar.name == CAL), None)
    if not calendar:
        print(f'No calendar "{CAL}" found at {URL}. Abort.')
        exit()
    all_events = tuple(events_from_calendar(calendar))

    if only_the_last_five:
        all_previous_events = tuple(e for e in all_events if is_previous_event(e['DTEND'].dt))
        all_events = sorted(all_previous_events, key=lambda e: e['DTSTART'].dt.date() if isinstance(e['DTSTART'].dt, datetime) else e['DTSTART'].dt)[:5]

    for event in all_events:
        # should we keep it ?
        if only_events_of_a_few_days_old_max and is_previous_event(event['DTEND'].dt):
            continue  # pass to the next event

        # get description and image
        description = event['DESCRIPTION']
        if description.strip().lower().startswith('image: '):
            first_line, *other_lines = description.splitlines(True)
            image = first_line[len('image: '):].strip()
            description = ''.join(other_lines)
        elif description.strip().lower().startswith('image:\n'):
            _, second_line, *other_lines = description.splitlines(True)
            image = second_line.strip()
            description = ''.join(other_lines)
        else:
            image = None

        # get start and end times (either date (whole days), or datetime (specific hours))
        assert event['DTSTART'].params.get('VALUE') == event['DTEND'].params.get('VALUE'), "Start and end times are not of the same type, and that's not handled by this script. Sorry."
        if event['DTSTART'].params.get('VALUE') == 'DATE':  # it's a whole day event
            start = as_simple_date_repr(event['DTSTART'].dt)
            end = as_simple_date_repr(minus_one_day(event['DTEND'].dt))  # make it inclusive, not exclusive date
            wholeday = True  # means start and end are date, not datetime
        else:  # it's an event with specific hours
            start = as_simple_datetime_repr(event['DTSTART'].dt)
            end = as_simple_datetime_repr(event['DTEND'].dt)
            wholeday = False

        # create and yield
        yield EVLEvent(
            event['SUMMARY'],
            image,
            description,
            event.get('LOCATION', 'EVL'),
            start,
            end,
            wholeday
        )


def evlevent_as_markdown(event: EVLEvent) -> [str]:
    """Yield markdown paragraphs describing given EVLEvent"""
    yield f'## {event.title}'
    if event.image:
        yield f'![image d\'illustration]({event.image})'
    if event.wholeday:
        assert len(event.start) == len(event.end) == 3, (event.start, event.end)
        if event.start == event.end:  # takes place on a whole, single day
            yield f'{event.location}, le {event.start[2]} {named_month(event.start[1])} {event.start[0]}'
        else:  # takes place on multiple days
            assert is_spanning_multiple_days(event.start, event.end)
            yield f'{event.location}, du {event.start[2]} {named_month(event.start[1])} {event.start[0]}'
    else:  # specific times
        assert len(event.start) == len(event.end) == 5, (event.start, event.end)
        if is_spanning_multiple_days(event.start, event.end):
            yield f'{event.location}, du {event.start[2]} {named_month(event.start[1])} {event.start[0]} à {event.start[3]}h{event.start[4]}, au {event.end[2]} {named_month(event.end[1])} {event.end[0]} à {event.end[3]}h{event.end[4]}'
        else:  # same day
            yield f'{event.location}, le {event.start[2]} {named_month(event.start[1])} {event.start[0]}, de {event.start[3]}h{event.start[4]} à {event.end[3]}h{event.end[4]}'
    yield event.description


def is_previous_event(dt: datetime) -> bool:
    ref = (dt + timedelta(days=3))  # consider that an event 3 days old belong to the past
    if isinstance(dt, datetime):
        ref = ref.date()
    return ref <= datetime.utcnow().date()
def named_month(num: int) -> str:
    return 'janvier,février,mars,avril,mai,juin,juillet,août,septembre,octobre,novembre,décembre'.split(',')[int(num)-1]
def as_simple_date_repr(obj: datetime) -> (int, int, int):
    return obj.year, obj.month, obj.day
def as_simple_datetime_repr(obj: datetime) -> (int, int, int, int, int):
    return obj.year, obj.month, obj.day, obj.hour, obj.minute
def is_spanning_multiple_days(one: tuple, two: tuple) -> bool:
    return one[:3] != two[:3]
def minus_one_day(date: datetime) -> datetime:
    return date - timedelta(days=1)


def whole_markdown_page(next_events: [EVLEvent], previous_events: [EVLEvent]) -> [str]:
    """Yield paragraphs of markdown to write in output file"""
    metadatas = {
        'Title': 'Évènements',
        'Date': '-'.join(map(str, as_simple_date_repr(datetime.now()))),
        'Tags': 'meta',
        'Summary': 'les prochaines activités à l\'écovillage !',
        'Slug': 'calendrier',
        'Status': 'published',
    }
    yield '\n'.join(f'{k}: {v}' for k, v in metadatas.items())
    has_one_event = False
    events = tuple(next_events)
    if events:
        yield f'# Évènements publics à venir de l\'EVL'
        for event in events:
            yield from evlevent_as_markdown(event)

    else:  # no event
        yield f'Il n\'y aucun évènement public à venir dans l\'écovillage… Contactez nous [par mail](mailto:contact@ecovillage-la-lanterne.net) pour savoir pourquoi !'

    events = tuple(previous_events)
    if events:
        yield f'# Quelques évènements publics précédents'
        for event in events:
            yield from evlevent_as_markdown(event)
    else:  # no previous event
        pass  # nothing to yield


if __name__ == "__main__":
    print('\n\n'.join(whole_markdown_page(
        get_evl_events(only_events_of_a_few_days_old_max=True),
        get_evl_events(only_the_last_five=True)
    )))

