# -*- coding: utf-8 -*-
"""
Created on Sat May  2 23:51:15 2020

@author: vidish
"""

"""
Please do not run this file as the telebot is already hosted on the cloud with additional features.

You may directly install telegram and search for travelBot --> click /start to see the magic

"""

TOKEN = "1118412663:AAF--8DOLgbgRBYmFICkb0Dit8qcH6HpMBw"

import telegram
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import requests
import re
from pymongo import MongoClient
from uuid import uuid4
from pymongo import MongoClient
import dns


def usernames_check(MongoUrl, username, chat_id):
    client = MongoClient(MongoUrl)
    db = client.TravelPlan
    collection = db.PlacesToVisit
    print("Connection Successful")
    usernames = []
    for doc in collection.find():
        usernames.append(doc['username'])
    print(usernames)
    if username in usernames:
        reply = "Hi "+username+", Welcome to Singapore! To get started, would you please share your current location by typing command /location?"
        chatBot = {'username':username}
        client = MongoClient(MongoUrl)
        db = client.TravelPlan
        collection = db.ChatInfo
        collection.update_one({'Chat_Id':chat_id},{'$set':chatBot},upsert=True)
        
    else:
        reply = "Hi "+username+", we were not able to retrieve your data! Please try again! If you are yet to sign up, please sign up at Trip@Us"
    
    return reply
    


def Itinerary(bot, update):
    reply = "Sure, we will pull out your itinerary, please let us know which day by typing /Day1 for example."
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, reply)
    
    
def itinerary_check(MongoUrl, day_of_itinerary, chat_id):
    client = MongoClient(MongoUrl)
    db = client.TravelPlan
    collection = db.ChatInfo
    print("Connection Successful")
    chat_ids = []
    for doc in collection.find():
        chat_ids.append(doc['Chat_Id'])
    username = []
    if chat_id in chat_ids:
        for doc in collection.find({'Chat_Id': chat_id}):
            username.append(doc['username'])
        username = username[0]
        client = MongoClient(MongoUrl)
        db = client.TravelPlan
        collection = db.PlacesToVisit
        print("Connection Successful")
        Day =[]
        for doc in collection.find({'username': username}):
            Day.append(doc['travelPlan'])
        TravelPlan = Day[0]
        for items in TravelPlan:
            if day_of_itinerary in items.keys():
                return ",".join(items[day_of_itinerary])
            else:
                pass            
    else:
        return "Please authenticate yourelf"
        


def split(msg):
    return[chars for chars in msg]    

def strip_at(msg):
    list2=[]
    msg = split(msg)
    for char in msg:
        if char == '@':
            pass
        else:
            list2.append(char)
    
    return "".join(list2)

def strip_at2(msg):
    list2=[]
    msg = split(msg)
    for char in msg:
        if char == '/':
            pass
        else:
            list2.append(char)
    
    return "".join(list2)


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def start(bot, update):
    reply = "Thank you for contacting your friendly Travel Bot. \n\nPlease type /info for all the common commands you can use. \n\nTo begin using our dynamic planner, please enter your username with @"
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id, reply)


def text_update_callback(bot,update):
    chat_id = update.message.chat_id
    message = update.message.text
    
    MongoUrl = "mongodb+srv://vidish:tripatus@cluster0-jzyrn.mongodb.net/test"
    
    if "@" in message:
        username = strip_at(message)
        reply = usernames_check(MongoUrl, username, chat_id)
    elif "/" in message:
        day_of_itinerary = strip_at2(message)
        reply = itinerary_check(MongoUrl, day_of_itinerary, chat_id)
        
    
    bot.sendMessage(chat_id, reply)
        

def put(update, context):
    """Usage: /put value"""
    # Generate ID and seperate value from command
    key = str(uuid4())
    value = update.message.text.partition(' ')[2]

    user_id = update.message.from_user.id

    # Create user dict if it doesn't exist
    if user_id not in all_user_data:
        all_user_data[user_id] = dict()

    # Store value
    user_data = all_user_data[user_id]
    user_data[key] = value

    update.message.reply_text(key)

def get(update, context):
    """Usage: /get uuid"""
    # Seperate ID from command
    key = update.message.text.partition(' ')[2]

    user_id = update.message.from_user.id

    # Load value
    try:
        user_data = all_user_data[user_id]
        value = user_data[key]
        update.message.reply_text(value)

    except KeyError:
        update.message.reply_text('Not found')
    






def Location(bot, update):

    loc_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
    custom_keyboard = [[loc_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

    bot.sendMessage(update.message.chat_id, 
              text="Please press the button below to provide us access to your location", 
              reply_markup=reply_markup)




def location_callback(bot, update):
    message = None
    if update.edited_message:
        message = update.edited_message
        chat_id = update.edited_message.chat_id
    else:
        message = update.message
        chat_id = update.message.chat_id
    current_pos = (message.location.latitude, message.location.longitude)
    if (1.30 < message.location.latitude < 1.50) and (102 < message.location.longitude < 104):
        reply = "Welcome to Singapore"
        
        
    else:
        reply = "We have checked that you are not in Singapore yet! Please contact us once you have reached Singapore!"
        
    bot.sendMessage(chat_id,reply)



def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('location',Location))
    dp.add_handler(CommandHandler('Add',start))
    dp.add_handler(CommandHandler('Itinerary',Itinerary))
    dp.add_handler(CommandHandler('location',Location))
    dp.add_handler(MessageHandler(Filters.location, location_callback))
    dp.add_handler(MessageHandler(Filters.text, text_update_callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


#%%
def split(msg):
    return[chars for chars in msg]    

def strip_at(msg):
    list2=[]
    msg = split(msg)
    for char in msg:
        if char == "@":
            pass
        else:
            list2.append(char)
    
    return "".join(list2)
    

from pymongo import MongoClient
import dns


def usernames_check(MongoUrl, username):
    client = MongoClient(MongoUrl)
    db = client.TravelPlan
    collection = db.PlacesToVisit
    print("Connection Successful")
    usernames = []
    for doc in collection.find():
        usernames.append(doc['username'])
    print(usernames)
    if username in usernames:
        reply = "Hi "+username+", we have all your information ready with us. To get started, would you please share your current location by typing command /location?"
    else:
        reply = "Hi "+username+", we were not able to retrieve your data! Please try again! If you are yet to sign up, please sign up at Trip@Us"
    
    return reply
    



def makeReply(msg):
    Mongourl = "mongodb+srv://vidish:tripatus@cluster0-jzyrn.mongodb.net/test"
    if msg == "Hi":
        reply = 'Thank you for contacting your friendly, travel bot. Please provide your username beginning with /'
    elif "@" in msg:
        print("Its coming here")
        username = strip_at(msg)
        print(username)
        
        client = MongoClient(Mongourl)
    
        db = client.TravelPlan
        collection = db.PlacesToVisit
        
        usernames = []
        for doc in collection.find():
            usernames.append(doc['username'])
        print(usernames)
        if username in usernames:
            reply = "Hi "+username+", Welcome to Singapore! To get started, would you please share your current location by typing command /location?"
        else:
            reply = "Hi "+username+", we were not able to retrieve your data! Please try again! If you are yet to sign up, please sign up at Trip@Us"
            
        
    return reply
    