from fastapi import FastAPI
from config import orders

app = FastAPI()

# Daily Sales Total

@app.get("/daily-total-sales",tags=["Total Daily Sales"])
def get_daily_total_sales(start_date:str, end_date:str):
    pipeline = [
        {
            "$match":{
                "status":"completed",
                "order_date":{
                    "$gte":start_date,
                    "$lte":end_date
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


# Top 5 Customers by Spend

@app.get("/top-customers", tags=["Top Customers"])
def top_customers():
    
    pipeline = [
         {
             "$group":{
                 "_id" : "$customer_id",
                 "Total_spent":{"$sum":"$total_amount"},
                 "Orders":{"$sum":1},
                 "Last_order":{"$max":"$order_date"}
             }
         },
         {
             "$project":{
                 "_id":0,
                 "Customer":"$_id",
                 "Total_spent":1,
                 "Orders":1,
                 "Last_order":1
             }
         },
         {
             "$sort": {"Total_spent": -1}
         },
         {
             "$limit":5
         }
         

    ]

    result = orders.aggregate(pipeline)
    return list(result)


# Sales by city

@app.get("/sales-by-city", tags=["Sales by City"])
def sales_by_city():

    pipeline = [
        {
            "$group":{
                
                "_id": "$city",
                "Total_Sales" : {"$sum":"$total_amount"},
                "Orders": {"$sum" :1},
                "Avg_Order":{"$avg": "$total_amount"}
            }
        },
        {
            "$sort":{"Total_Sales": -1}
        },

        {
            "$limit":20
        },
        {
            "$project": {
                "_id":0,
                "City":"$_id",
                "Total_Sales":1,
                "Orders":1,
                "Avg_Order":1    


            }
        }
    ]

    result =orders.aggregate(pipeline)
    return list(result)
    
    # result = list(orders.aggregate(pipeline))

    # table = []
    # header = "City | Total Sales | Orders | Avg Order"
    # table.append(header)

    # for r in result:
    #     row = f"{r['City']} | ${r['Total_Sales']:.2f} | {r['Orders']} | ${r['Avg_Order']:.2f}"
    #     table.append(row)

    # return {"table": table}
 