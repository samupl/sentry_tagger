from sentry_tagger import processors

PROCESSORS = [
    processors.ExceptionBasedProcessor(),
    processors.HttpResponseBasedProcessor(),
    processors.SystemTagProcessor(),
]


def tag_sentry_event(event, hint):
    for processor in PROCESSORS:
        tag = processor.tag(event, hint)
        if tag is not None:
            event.setdefault('tags', {})['actionability'] = tag.value
            break
    return event
