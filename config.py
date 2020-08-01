# Importing necessary libraries
import os
from flask import Flask, request
from pymongo import MongoClient
from telethon import TelegramClient, events, sync
import telebot
import asyncio
from time import sleep
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sessions import StringSession
import random
import csv
from datetime import datetime, timedelta
from decouple import config
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
scheduler.start()


DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")


# Database Tool
database_client = MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASS}@cluster0-fj4um.mongodb.net/?retryWrites=true&w=majority")
db = database_client.tool_database
sessions = db.sessions.find()

message_db = database_client.test


SESSIONS = [sessions[i]['SessionString'] for i in range(sessions.count())]
SESSION_USERS = [sessions[i]['first_name'] for i in range(sessions.count())]

API_ID = config("API_ID")
API_HASH = config("API_HASH")

TOKEN = config("TOKEN")

# SESSION = config("SESSION")

app = Flask(__name__)

# Starting Bot
bot = telebot.TeleBot(token=TOKEN)
