import datetime as dt
import pytz
import re


def _sender_ping(message):
    """Substitutes into a ping of the author."""
    return message.author.mention


def _time(message, *args):
    """Substitutes into current time in the specified timezone."""

    timezone_name = args[0].strip() if len(args) >= 1 else 'UTC'  # UTC as default
    fmt = '%I:%M %p, %Z' if len(args) < 2 else args[2]  # Use specified format if possible

    datetime = None

    # Check if timezone name is numerical (eg. +5.5, -10 etc.)
    if re.search('^[+-]?\d+\.?\d*$', timezone_name) == None:
        now = dt.datetime.now(pytz.UTC)
        datetime = now.astimezone(pytz.timezone(timezone_name))
        # datetime = pytz.timezone(timezone_name).localize(now)
    else:
        timezone = dt.timezone(dt.timedelta(hours=float(timezone_name)))
        datetime = dt.datetime.now(timezone)

    return datetime.strftime(fmt)


def _sender_name(message):
    """Substitutes into the author's name."""
    return message.author.name


substitutions = {
    'sender_ping': _sender_ping,
    'time': _time,
    'sender_name': _sender_name
}