## This script was written by Codefred on Fiverr
######################################################################################
# main purpose is to first join specified telegram group
# and send custom messages to all their members

from config import *

customMsg = ''
targetGrp = ''
questionId = 0

imageAttached = False
fileName = ""

user = ''

## State variable
warning = 0
index = 1
admins = [] # Administrators of the group

# registered users on Users.txt
Userfile = open("Users.txt", "r")
idlist = list(csv.reader(Userfile))
registeredusers = [n[0] for n in idlist]



sent = 0
views = 0
clicks = 0
campaignId = ''
starter_msg = ''
error_msg = ''


@bot.message_handler(commands=['start'])
def targetGroup(msg):
    """Request The Target Group From User"""
    global user, starter_msg, error_msg
    user = msg.from_user

    if error_msg != '':
        bot.delete_message(error_msg.chat.id, error_msg.message_id)

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(
        text= 'Start New Campaign 🎤',
        callback_data= 'new'
        )
    markup.add(btn1)

    starter_msg = bot.reply_to(
        msg,
        f"""
Hello {user.username}!

Welcome to <a href="https://t.me/tg_Adbot"><b>The Ultimate Ads Bot</b></a>, helping business owners reach out to more potential customers worldwide through telegram.

You can <b>get started</b> by creating your first campaign 🎟 and see your audience on your content grow from zero to hero 
        """,
        parse_mode = "html",
        reply_markup = markup,
        disable_web_page_preview = True
        )

    return starter_msg


# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    """
    Button Response
    """
    global questionId

    bot.delete_message(starter_msg.chat.id, starter_msg.message_id)

    if call.data == "new":
        # Ask Request
        question = bot.send_message(
            user.id,
            "Paste a valid and active telegram group link to be used for audience referencing...",
            reply_markup=types.ForceReply(selective=True)
            )
        questionId = question.message_id
        
        bot.register_next_step_handler(question, joinGroup)

    elif call.data == "old":

        print("Not yet fixed!")

    else:
        pass

    return questionId



def joinGroup(msg):
    """Join The Target Group And Request Message From User"""

    global targetGrp, admins, questionId, error_msg

    # delete incoming 
    bot.delete_message(msg.chat.id, questionId)

    try:
        targetGrp = msg.text
        
        # Extracting Admin Information For the target group
        [admins.append(admin.user.id) for admin in bot.get_chat_administrators(targetGrp)]

        # Ask Request
        question = bot.send_message(
            user.id,
            "Paste in your advert content to be shared on your campaign...",
            reply_markup=types.ForceReply(selective=True)
            )
        questionId = question.message_id

        bot.register_next_step_handler(question, send)   

    except Exception as e:

        error_msg = bot.send_message(user.id, f"Invalid Request! Try All Over Again 😟")
        targetGroup(msg)
    
    # import pdb; pdb.set_trace()
    bot.delete_message(msg.chat.id, msg.message_id)
    return questionId, targetGrp, admins, error_msg



def send(msg):
    """Save and start sending message"""

    global customMsg, imageAttached, sent, views, clicks, campaignId

    # delete incoming 
    bot.delete_message(msg.chat.id, questionId)

    if msg.content_type != 'text':
        customMsg = msg.caption
        imageAttached = True
        download_attachment(msg.photo)
    else:
        customMsg = msg.text
        imageAttached = False

    # CAMPAIGN MESSAGE
    message = bot.send_message(
        user.id,
        text = f"""
🏁 <b>CAMPAIGN STATUS</b>
Your campaign has just been created and your content is going out....

Target Audience -> {targetGrp}
Administrators excluded -> {len(admins)}

<b>Sent</b> -> {sent}
<b>Views</b> -> {views}
<b>Clicks</b> -> {clicks}
        """,
        parse_mode= "html",
    )
    campaignId = message.message_id

    bot.delete_message(msg.chat.id, msg.message_id)

    for session, session_user in zip(SESSIONS, SESSION_USERS):
    
        loop = asyncio.new_event_loop()

        client = TelegramClient(
            StringSession(session),
            API_ID,
            API_HASH,
            loop = loop
        ).start(bot_token=TOKEN)

        client.loop.run_until_complete(sendMessage(user.id, session_user, client))

        messages = message_db.messages.find()

        msg_ids = [messages[i]['message_id'] for i in range(messages.count()) if messages[i]['sender'] == str(session_user)]

        imageAttached = False

        #Add scheduler job
        time = datetime.now() + timedelta(minutes=30)
        scheduler.add_job(delete_message, trigger='date', run_date=time, id=f'by_{session_user}', args=(msg_ids, client, messages))

    bot.edit_message_text(
        chat_id = user.id,
        message_id = campaignId,
        text = f"""
🏴 <b>CAMPAIGN CLOSED</b>
---------------------------
Target Audience -> {targetGrp}
Administrators excluded -> {len(admins)}

<b>Sent</b> -> {sent}
<b>Views</b> -> {views}
<b>Clicks</b> -> {clicks}
        """,
        parse_mode = "html",
    )



def download_attachment(img):
    "Downloads the Attached Image File To Source Directory So It Can Be Reused"
    
    global fileName
    file_id = img[0].file_id

    file_url = bot.get_file_url(file_id)

    fileName = file_url.split("/")[-1]

    #Download image
    image = requests.get(file_url, allow_redirects=True)
    open(f"images/{fileName}", "wb").write(image.content)
    return


async def sendMessage(id, session_user, client):
    """Send The Custom Message To A Target Group"""

    global index, warning, sent, views, clicks

    bot.edit_message_text(
        chat_id = id,
        message_id = campaignId,
        text = f"""
🏳️ <b>CAMPAIGN ACTIVE</b>
Your campaign is live, active with <b>{session_user}</b>

<b>Sent</b> -> {sent}
<b>Views</b> -> {views}
<b>Clicks</b> -> {clicks}   
        """,
        parse_mode = "html",
    )

    try:
        group = await client.get_entity(targetGrp)

        try:
            # Join Group
            await client(JoinChannelRequest(group))
        except Exception as e:
            pass

        ## Get All the users from the target group
        members = await client.get_participants(group)

        ## Send message to the members individually
        for user in members[index:5]:
            if user.bot == False:
                if user.id not in admins and str(user.id) not in registeredusers:

                    try:
                        if imageAttached == False:
                            message = await client.send_message(
                                user.id,
                                customMsg
                                )
                        # message = await client.send_messages(user.id, [raw_msg.message_id], id)
                        else:
                            message = await client.send_message(
                                user.id,
                                customMsg,
                                file=f'images/{fileName}'
                                )

                        post_data = {
                            'sender': session_user,
                            'message_id': message.id,
                            'sent_date': datetime.now(),
                        }
                        result = message_db.messages.insert_one(post_data)
                        print('One post: {0}'.format(result.inserted_id))
                        sent += 1
                        
                    except Exception as e:
                        warning += 1

                        if warning >= 5:
                            bot.send_message(id, f"Failed to send anymore message with {session_user}")
                            warning = 0
                            return None
                        else:
                            print(f"Warning ! {e}")
                        sleep(60)

            #Setting the state
            index += 1
            bot.edit_message_text(
                chat_id = id,
                message_id = campaignId,
                text = f"""
🏳️ <b>CAMPAIGN ACTIVE</b>
---------------------------
<b>Sent</b> -> {sent}
<b>Views</b> -> {views}
<b>Clicks</b> -> {clicks}
                """,
                parse_mode = "html",
            )

    except Exception as e:
        print(e)
        bot.edit_message_text(
            chat_id = id,
            message_id = campaignId,
            text = """
🚩 <b>CAMPAGIN INACTIVE</b>
---------------------------
Error in your input! Please verify the group link provided and try creating the campaign again
            """,
            parse_mode = "html",
        )


def delete(msg_ids, client, messages):
    "Function To Activate The Scheduler For the Deleting Of Sent Messages"
    client.loop.run_until_complete(deleteMessages(msg_ids, client, messages))


async def deleteMessages(ids, client, messages):
    "Deletes messsages recorded to be sent"

    await client.delete_messages(entity=None, message_ids=list(ids))

    [message_db.messages.delete_one(payload) for payload in messages]

    return await client.disconnect()