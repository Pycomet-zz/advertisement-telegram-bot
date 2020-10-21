## This script was written by Codefred on Fiverr
######################################################################################
# main purpose is to first join specified telegram group
# and send custom messages to all their members

from config import *

customMsg = ''
targetGrp = ''

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


@bot.message_handler(commands=['start'])
def targetGroup(msg):
    """Request The Target Group From User"""
    global user

    user = msg.from_user

    bot.reply_to(msg, f"Hello {user.username}")

    # Ask Request
    question = bot.send_message(user.id, "Please reply with a valid telegram group link..")

    bot.register_next_step_handler(question, joinGroup)


def joinGroup(msg):
    """Join The Target Group And Request Message From User"""

    global targetGrp
    global admins

    try:
        targetGrp = msg.text
        
        # Extracting Admin Information For the target group
        [admins.append(admin.user.id) for admin in bot.get_chat_administrators(targetGrp)]
        

        # Ask Request
        question = bot.send_message(user.id, "Paste your custom message content here --")

        bot.register_next_step_handler(question, send)   

    except Exception as e:

        bot.send_message(user.id, f"Invalid Request! - {e}")
        targetGroup(msg)

def send(msg):
    """Save and start sending message"""

    global customMsg
    global imageAttached

    if msg.content_type != 'text':
        customMsg = msg.caption
        imageAttached = True
        download_attachment(msg.photo)
    else:
        customMsg = msg.text
        imageAttached = False

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
        time = datetime.now() + timedelta(minutes=2)
        scheduler.add_job(delete_message, trigger='date', run_date=time, id=f'by_{session_user}', args=(msg_ids, client, messages))



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

    global index
    global warning
    bot.send_message(id, f"{session_user} Sending Messages.....")

    try:
        group = await client.get_entity(targetGrp)
        # Join Group
        await client(JoinChannelRequest(group))

        bot.send_message(id, f'{session_user} Joined {group.title} Group Successfully!')

        ## Get All the users from the target group
        members = await client.get_participants(group)

        ## Send message to the members individually
        for user in members[index::]:
            if user.bot == False:
                if user.id not in admins and str(user.id) not in registeredusers:

                    try:
                        if imageAttached == False:
                            message = await client.send_message(
                                user.id,
                                customMsg,
                                buttons=[
                                    Button.inline("Click me", b'well'),
                                    Button.url('Join Group', 'https://t.me/globaltradegroupvip')
                                    ]
                                )
                        # message = await client.send_messages(user.id, [raw_msg.message_id], id)
                        else:
                            message = await client.send_message(
                                user.id,
                                customMsg,
                                file=f'images/{fileName}',
                                buttons=[
                                    Button.inline("Click me", b'well'),
                                    Button.url('Join Group', 'https://t.me/globaltradegroupvip')
                                    ]
                                )

                        post_data = {
                            'sender': session_user,
                            'message_id': message.id,
                            'sent_date': datetime.now(),
                        }
                        result = message_db.messages.insert_one(post_data)
                        print('One post: {0}'.format(result.inserted_id))

                        bot.send_message(id, f"Sent to {user.username}")
                        
                    except Exception as e:
                        warning += 1

                        if warning >= 5:
                            bot.send_message(id, f"Failed to send anymore message with {user.username}")
                            warning = 0
                            return None
                        else:
                            print(f"Warning ! {e}")
                        sleep(60)

            #Setting the state
            index += 1

    except Exception as e:
        print(e)
        bot.send_message(id, "Error in your input! Try again with requested valid data")


def delete(msg_ids, client, messages):
    "Function To Activate The Scheduler For the Deleting Of Sent Messages"
    client.loop.run_until_complete(deleteMessages(msg_ids, client, messages))


async def deleteMessages(ids, client, messages):
    "Deletes messsages recorded to be sent"

    await client.delete_messages(entity=None, message_ids=list(ids))

    [message_db.messages.delete_one(payload) for payload in messages]
    return await client.disconnect()