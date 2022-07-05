# Sentry exception tagger

**Note**: This is just a proof of concept, this isn't meant to be used in production. It isn't
properly packaged for distribution, nor does it contain proper setting handling right now.


Used to "automatically" add an `actionability` tag to sentry events.

The `actionability` tag decides whether or not an error is caused by the system (e.g. it's a real
exception that should be fixed) or an user (e.g. it's an exception caused by user 
providing incorrect credentials/configuration and it should be handled by displaying a proper 
error/CTA to the user).

The `actionability` can have one of two values: `user` or `system`.

## Configuration

Modify the call to `sentry_sdk.init()` in settings by adding a `before_send` callable:

```python
from sentry_tagger.utils import tag_sentry_event

sentry_sdk.init(
    # ...
    before_send=tag_sentry_event
)

```
Modify `sentry_tagger/utils.py` `PROCESSORS` constant:

```python
from sentry_tagger import processors

PROCESSORS = [
    processors.ExceptionBasedProcessor(),
    processors.HttpResponseBasedProcessor(),
    processors.SystemTagProcessor(),
]
```

## Processors

A processor is a class that decides how a particular exception/event should be processed. It's job 
is to return a tag that should be attached to a specific event, or `None` in case it cannot tag
the event properly.

The order of the `PROCESSORS` constant matters - the tagger tries each processor sequentially, 
until a first one returns a valid tag.

### `ExceptionBasedProcessor`

This processor uses a registry to map exception classes to tags. It requires explicit registration,
e.g.:

```python
from sentry_tagger.enums import Target
from sentry_tagger.processors.exception_based import register


@register(Target.SYSTEM)
class ExampleSystemException(Exception):
    pass


@register(Target.USER)
class ExampleUserException(Exception):
    pass

```

### `HttpResponseBasedProcessor`

This processor works by handling `requests` package `HttpError` exceptions. It tries to investigate
the http status code and return a proper tag based on it. 

Rules:

* Tagged as `user`:
  * `401`
* Tagged as `system`:
  * `500` 


### `SystemTagProcessor`

This processor tags all events as `system`. It's meant to be used as the last, "fallback" processor
to tag events that weren't tagged by any prior processors.
