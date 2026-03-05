from fastapi import FastAPI
from faker import Faker
import random
from config import users, cities  

app = FastAPI()
fake = Faker("en_US")


@app.get("/")
def setup_data():

    # Clear old data
    users.delete_many({})
    cities.delete_many({})

    # Insert Cities
    city_list = [
    {"_id": 1, "city": "New York", "address": "5th Avenue"},
    {"_id": 2, "city": "Los Angeles", "address": "Sunset Boulevard"},
    {"_id": 3, "city": "London", "address": "Baker Street"},
    {"_id": 4, "city": "Paris", "address": "Champs-Élysées"},
    {"_id": 5, "city": "Berlin", "address": "Alexanderplatz"},
    {"_id": 6, "city": "Tokyo", "address": "Shibuya Crossing"},
    {"_id": 7, "city": "Sydney", "address": "George Street"},
    {"_id": 8, "city": "Toronto", "address": "Queen Street"},
    {"_id": 9, "city": "Dubai", "address": "Sheikh Zayed Road"},
    {"_id": 10, "city": "Singapore", "address": "Orchard Road"}
]

    cities.insert_many(city_list)

    # Insert Users
    user_list = []

    for i in range(100):
        user = {
            "name": fake.name(),
            "email": fake.email(),
            "age": random.randint(18, 60),
            "city_id": random.randint(1, 10)
        }
        user_list.append(user)

    users.insert_many(user_list)

  

    return {"message": "100 fake users inserted"}

# find the users less than 25 age

# @app.get("/user_age")
# def user_age():

#     result = users.find(
#         {"age": {"$lt": 25}},
#          {"_id": 0}
#     )

#     return list(result)

@app.get("/users-under-25")
def users_under_25():

    pipeline = [
        {
            "$match": {
                "age": {"$lt": 25}
            }
        },
        {
            "$project":{"_id":0}
        }
 ]

    result = users.aggregate(pipeline)

    return list(result)


# Get Users From Particular City

@app.get("/users-by-city")
def users_by_city(page: int = 1, limit: int = 10):

    skip = (page-1) * limit

    pipeline = [

        {
            "$lookup": {
                "from": "cities",
                "localField": "city_id",
                "foreignField": "_id",
                "as": "city_info"
            }
        },

        {
            "$match": {
                "city_info.city": "London"
            }
        },
        {
            "$project":{
                "_id":0,
                "name":1,
                "age":1,
               "city": "$city_info.city"
                }
        },
        {
            "#skip":skip
        },
        {
            "#limit":limit
        }

    ]

    result = users.aggregate(pipeline)

    return list(result)


# Count users in each city

@app.get("/total-by-city")
def users_by_city():

    pipeline = [
        {
            "$group":{
                "_id":"$city_id",
                "total_users":{"$sum":1}
            }
        }
    ]

    result = users.aggregate(pipeline)

    return list(result)










    

    

