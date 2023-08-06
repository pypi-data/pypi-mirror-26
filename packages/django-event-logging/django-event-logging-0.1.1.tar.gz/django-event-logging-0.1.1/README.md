# Event Logging

Log events using database

*Current version:* 0.1.1 (dev)

## Installation

Run `pip install django-event-logging`

## Setting up

Add `event_logging` into `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'event_logging',
]
```

Run command `python manage.py migrate event_logging`