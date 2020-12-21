import json
import os.path
from typing import List
from botbuilder.core import MessageFactory, TurnContext,ActivityHandler
from botbuilder.schema import Attachment, ChannelAccount,AttachmentLayoutTypes
from graph import welcome


class WelcomeBot(ActivityHandler):

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                welcome_card = self.create_adaptive_card_attachment()
                response = MessageFactory.attachment(welcome_card)
                await turn_context.send_activity(response)
                text = welcome()
                await turn_context.send_activity("Bienvenu(e) chez "+text)

    # Load attachment from file.
    def create_adaptive_card_attachment(self):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "./cards/welcomeCard.json")
        with open(path) as card_file:
            card = json.load(card_file)
        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card
        )