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
    #message.reply('Send to LUIS')
    intent = client.predict(str(message)).get_top_intent()
    #message.reply(intent.get_name())
    response_msg = dispatch(intent)
    if response_msg and isinstance(response_msg, str):
        message.reply(response_msg)
