from fastapi import FastAPI
from config import orders

app = FastAPI()

@app.get("/")
def get_orders():
    pipeline = [
        {
            "$match":{
                "status":"completed",
                "order_date":{
                    "$gte":"2025-01-12",
                    "$lte":"2025-01-15"
                }
            }
        },

{
 "$group": {
     "_id": {
         "$dateToString": {
             "format": "%Y-%m-%d",
             "date": {"$toDate": "$order_date"}
         }
     },
     "total_sales": {"$sum": "$total_amount"},
     "orders_count": {"$sum": 1}
 }
},

{
    "$project":{
        "_id":0,
        "Date":"$_id",
        "Total_sales":"$total_sales",
        "Orders Count": "$orders_count"
    }
},

{"$sort": {"Date": -1}}

    ]
    result = orders.aggregate(pipeline)
    return list(result)

    