## This script was written by Codefred on Fiverr
######################################################################################
# main purpose is to first join specified telegram group
# and send custom messages to all their members

from config import *
from .classes import Campaign


starter_msg = ""
targetGrp = ""
questionId = ""
error_msg = ""
admins = []

@bot.message_handler(commands=['start'])
def getStarted(msg):
    "Ignite from the start command"
    global starter_msg

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(
        text= 'Start New Campaign 🎤',
        callback_data= 'new'
        )
    markup.add(btn1)

    starter_msg = bot.reply_to(
        msg,
        f"""
Hello {msg.from_user.username}!

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
            call.from_user.id,
            "Paste a valid and active telegram group link to be used for audience referencing...",
            reply_markup=types.ForceReply(selective=True)
            )
        questionId = question.message_id
        
        bot.register_next_step_handler(question, join_group)

    elif call.data == "old":

        print("Not yet fixed!")

    else:
        pass

    return questionId



def join_group(msg):
    """Join The Target Group And Request Message From User"""
    global targetGrp, questionId, error_msg, admins

    # delete incoming 
    bot.delete_message(msg.chat.id, questionId)

    try:
        targetGrp = msg.text
        
        # Extracting Admin Information For the target group
        admins = [admin.user.id for admin in bot.get_chat_administrators(targetGrp)]

        # Ask Request
        question = bot.send_message(
            msg.from_user.id,
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
    if error_msg:
        return error_msg
    else:
        return questionId, admins, targetGrp



def send(msg):
    """Save and start sending message"""
    # delete incoming 
    bot.delete_message(msg.chat.id, questionId)
    
     # CAMPAIGN MESSAGE
    message = bot.send_message(
        msg.from_user.id,
        text = f"""
🏁 <b>CAMPAIGN STATUS</b>
Your campaign has just been created and your content is going out....

Target Audience -> {targetGrp}
Administrators excluded -> {len(admins)}
        """,
        parse_mode= "html",
    )
    campaign_id = message.message_id

    if msg.content_type != 'text':
        file = download_attachment(msg.photo)
        campaign = Campaign(
            user_id = msg.from_user.id,
            message = msg.caption,
            group = targetGrp,
            image = True,
            file_name = file,
            campaign_id = campaign_id
        )
    else:
        campaign = Campaign(
            user_id = msg.from_user.id,
            message = msg.text,
            group = targetGrp,
            image = False,
            file_name = "",
            campaign_id = campaign_id
        )


    # CAMPAIGN RUNNER
    campaign.start_client()
  



def download_attachment(img):
    "Downloads the Attached Image File To Source Directory So It Can Be Reused"
    file_id = img[0].file_id

    file_url = bot.get_file_url(file_id)
    fileName = file_url.split("/")[-1]

    #Download image
    image = requests.get(file_url, allow_redirects=True)
    open(f"images/{fileName}", "wb").write(image.content)
    return fileName
