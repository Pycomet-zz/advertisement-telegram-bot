from config import *

class Campaign:
    
    def __init__(self, user_id, message, group, image, file_name, campaign_id):
        self.administrators = []
        self.chat_id = ''
        self.campaign_id = campaign_id # Referencing the campain message id
        self.user_id = user_id
        # self.starter_msg = starter_msg # The onboarding message to get started

        self.sent = 0
        self.read = 0
        self.warning = 0

        self.file_name = file_name
        self.image_attached = bool(image)
        self.message = message # Custom message to be sent
        self.group = group  # target group

        self.client = None

    def start_client(self):
        """STARTING THE CLIENT SESSION"""

        loop = asyncio.new_event_loop()

        self.client = TelegramClient(
            StringSession(session),
            API_ID,
            API_HASH,
            loop=loop
        ).start(bot_token=TOKEN)

        self.client.loop.run_until_complete(
            self.send_message()
        )

    def get_admins(self):
        "Fetch Group Administrators"
        for admin in bot.get_chat_administrators(self.group):
            self.administrators.append(admin.user.id)


    async def send_message(self):
        """ACTION ON SENDING MESSAGES"""

        bot.edit_message_text(
            chat_id = self.user_id,
            message_id = self.campaign_id,
            text = f"""
    🏳️ <b>CAMPAIGN ACTIVE</b>
    Your campaign is live

    Target Audience -> {self.group}
    Target number of administrators -> {len(self.administrators)}

    <b>Sent</b> -> {self.sent}
    <b>Views</b> -> {self.read}
            """,
            parse_mode = "html",
        )
        # self.get_admins()

        # for user in self.administrators:
        async for user in self.client.iter_participants(self.group):
            if user.bot == False:
            
                try:
                    if self.image_attached == False:
                        message = await self.client.send_message(
                            user,
                            self.message
                            )
                    else:
                        message = await self.client.send_message(
                            user,
                            self.message,
                            file=f'images/{self.file_name}'
                            )

                    self.send_to_scheduler(
                        msg=message.id
                    )
                    self.sent += 1

                except Exception as e:

                    self.warning += 1
                    if self.warning >= 5:
                        bot.send_message(self.user_id, f"Failed to send messages")
                        self.quit()
                    else:
                        print(f"Warning ! {e}")
                    sleep(5)

                self.update_campaign()
            else:
                pass


    def update_campaign(self):
        "UPDATING THE CAMPAGIN"

        bot.edit_message_text(
            chat_id = self.user_id,
            message_id = self.campaign_id,
            text = f"""
🏳️ <b>CAMPAIGN ACTIVE</b>
---------------------------
Target Audience -> {self.group}
Administrators excluded -> {len(self.administrators)}

<b>Sent</b> -> {self.sent}
<b>Views</b> -> {self.read}
            """,
            parse_mode = "html",
        )

        
    def send_to_scheduler(self, msg):
        "POST TO REGISTER FOR DELETE"

        post_data = {
            'sender': session_user,
            'message_id': msg,
            'sent_date': datetime.now(),
        }
        result = message_db.messages.insert_one(post_data)
        print('One post: {0}'.format(result.inserted_id))
        

    def quit(self):
        self.client.disconnect()

    


