from pymongo import MongoClient


def Feedback_to_db(request, username, email):

    Mongourl = "mongodb+srv://vidish:tripatus@cluster0-jzyrn.mongodb.net/test"
    
    client = MongoClient(Mongourl)
    
    d = dict((db, [collection for collection in client[db].collection_names()])
        for db in client.database_names())

    db = client.TravelPlan
    
    collection = db.Feedback

    print(request, username, email)

    Feedback_dict = {'email': email,
                    'ServiceRating': request['Service_Rating'],
                    'ServiceFeedback': request['Service_Feedback']}

    collection.update_one({'username': username},{'$set': Feedback_dict}, upsert=True)

    print("Update Successful")

    return