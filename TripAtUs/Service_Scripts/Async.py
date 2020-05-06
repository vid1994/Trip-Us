from celery import Celery
from .PlanMyTrip_main import plan_my_trip
from pymongo import MongoClient

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def add(x, y):
    return x + y


@app.task
def Plan_My_trip(username,email):
    Mongourl = "mongodb+srv://vidish:tripatus@cluster0-jzyrn.mongodb.net/test"
    
    client = MongoClient(Mongourl)
    
    d = dict((db, [collection for collection in client[db].collection_names()])
        for db in client.database_names())

    db = client.TravelPlan

    collection = db.PlacesToVisit
    
    try:
        plan_my_trip(username,email)
        outcome_dict = {'Outcome':'Sucess'}
        collection.update({'username':username},{'$set':outcome_dict},upsert=True)
    except:
        plan_my_trip(username,email)
        outcome_dict = {'Outcome':'Failure'}
        collection.update({'username':username},{'$set':outcome_dict},upsert=True)
