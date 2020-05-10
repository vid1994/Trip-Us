from celery import Celery
from .PlanMyTrip_main import plan_my_trip
from pymongo import MongoClient
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


#app = Celery('tasks', broker='pyamqp://guest@localhost//')


@shared_task
def test_celery_worker():
    print("Celery Workers are working fine.")


@shared_task
def add(x, y):
    return x + y


@shared_task
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
