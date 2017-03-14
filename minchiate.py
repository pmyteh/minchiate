#!/usr/bin/env python3

import ephem
import datetime
import icalendar
import uuid

START_DATE = datetime.datetime.utcnow()
END_DATE = datetime.date(year=2030, month=12, day=31)

def gen_minchiate_dates(start, end):
    # Minchiate tournaments are six weeks and twelve weeks after each equinox
    # and solstice, with the cutoff time being midnight Saturday.
    astro = min(ephem.next_solstice(start),
                ephem.next_equinox(start)
               )
    six_date = (this_or_next_weekday(astro.datetime(), 5)
                    + datetime.timedelta(weeks=5))
    if six_date <= end:
        yield six_date
        twelve_date = six_date + datetime.timedelta(weeks=6)
        if twelve_date <= end:
            yield twelve_date
            # Get the next equinox/solstice and keep going
            for item in gen_minchiate_dates(astro, end):
                yield item

def this_or_next_weekday(d, weekday): # weekday=0 is Mon, =1 is Tue...
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return (d + datetime.timedelta(days_ahead)).date()

def main():
    cal = icalendar.Calendar()
    # Compulsory boilerplate
    cal.add('prodid', '-//IDN tomnicholls.me.uk//minchiate.py')
    cal.add('version', '2.0')
    for date in gen_minchiate_dates(START_DATE, END_DATE):
        print(date)
        event = icalendar.Event()
        event.add('summary', 'Minchiate tournament')
        event.add('dtstart', date)
        event.add('dtend', date + datetime.timedelta(days=2))
        # Stupid compulsory boilerplate
        event.add('dtstamp', datetime.datetime.utcnow())
        event.add('uid', str(uuid.uuid4()))
        cal.add_component(event)

    with open("minchiate.ics", "wb") as f:
        f.write(cal.to_ical())
        
if __name__ == '__main__':
    main()
