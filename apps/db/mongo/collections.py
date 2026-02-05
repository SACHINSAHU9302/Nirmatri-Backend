from .client import db

users_collection = db["users"]
products_collection = db["products"]
orders_collection = db["orders"]


#USERS Collection
{
  "_id": "ObjectId",
  "name": "Prajjwal Sen",
  "email": "prajjwal@gmail.com",
  "role": "buyer",
  "created_at": "2026-02-03"
}
#PRODUCTS Collection
{
  "_id": "ObjectId",
  "name": "Product Name",
  "description": "Product Description",
  "price": 100.0,
  "stock": 50,
  "created_at": "2026-02-03"
}   
#ORDERS Collection
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "product_ids": ["ObjectId1", "ObjectId2"],
  "total_amount": 200.0,
  "status": "pending",
  "created_at": "2026-02-03"
}

