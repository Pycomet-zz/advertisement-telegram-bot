# Importing necessary libraries
import os
from telethon import TelegramClient, events, sync
import telebot
from time import sleep
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sessions import StringSession
import random
import csv
from decouple import config


API_ID = config("API_ID")
API_HASH = config("API_HASH")

TOKEN = config("TOKEN")

SESSION = config("SESSION")

