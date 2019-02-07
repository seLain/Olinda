import inspect
import logging


logger = logging.getLogger(__name__)


class IntentHandler:
    def handle(self, intent):
        return None


class Unknown(IntentHandler):

    def handle(self, intent):
        return "Sorry, I don't understand."


class GoodJob(IntentHandler):

    def handle(self, intent):
        return 'Thank you :)'


class Hello(IntentHandler):

    def handle(self, intent):
        return 'Hello. What can I do for you ?'


handlers = {}
g = globals().copy()
for name, obj in g.items():
    if inspect.isclass(obj) and issubclass(obj, IntentHandler) and \
        not obj == IntentHandler:
        handlers[name] = obj


def dispatch(intent):

    try:
        if intent.get_name() == 'None':
            return Unknown().handle(intent)
        else:
            return handlers[intent.get_name()]().handle(intent)
    except KeyError as e:
        logger.warning('No intent key %s was found.' % intent.get_name())
        return None