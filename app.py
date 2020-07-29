## This script was written by Codefred on Fiverr
######################################################################################
# main purpose is to first join specified telegram group
# and send custom messages to all their members

from config import *


customMsg = ''
targetGrp = ''
user = ''
admins = [] # Administrators of the group

# registered users on Users.txt
Userfile = open("Users.txt", "r")
idlist = list(csv.reader(Userfile))
registeredusers = [n[0] for n in idlist]



print("Ready")

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
    customMsg = msg.text

    client.loop.run_until_complete(sendMessage(user.id))


async def sendMessage(id):
    """Send The Custom Message To A Target Group"""
       

    bot.send_message(id, "Sending Messages.....")


    try:
        group = await client.get_entity(targetGrp)

        # Join Group
        await client(JoinChannelRequest(group))

        bot.send_message(id, f'Joined {group.title} Group Succesfully!')

        ## Get All the users from the target group
        members = await client.get_participants(group)

        ## Send message to the members individually
        for user in members[1:]:

            if user.bot == False:

                if user.id not in admins and str(user.id) not in registeredusers:

                    try:
                        await client.send_message(user.id, customMsg)

                        # Writing To Db File
                        register = open("Users.txt", "a", newline="\n")
                        register.write(f"{user.id}\n")
                        register.close()

                        bot.send_message(id, f"Sent to {user.username}")
                        
                    except Exception as e:
                        print(f"Warning ! {e}")
                        sleep(60)
                        pass

                    sleep(random.randrange(60,120))

    except Exception as e:
        print(e)
        bot.send_message(id, "Error in your input! Try again with requested valid data")

   

# bot.polling(none_stop=True)

# while True:
#     pass
