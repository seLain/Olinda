import re

from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

from luis.adapters import LUISClient
from bot_settings import LUIS_APP_ID, LUIS_APP_KEY
from .intent_handlers import dispatch


client = LUISClient(app_id=LUIS_APP_ID, app_key=LUIS_APP_KEY)


@listen_to('.*', re.IGNORECASE)
@respond_to('.*', re.IGNORECASE)
def any(message):
    intent = client.predict(message.get_message()).get_top_intent()
    response_msg = dispatch(intent) if intent else None
    if response_msg and isinstance(response_msg, str):
        message.reply(response_msg)
