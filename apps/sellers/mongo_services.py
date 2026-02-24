from apps.db.mongo.db_collections import sellers_collection

def get_seller_by_email(email):
    return sellers_collection.find_one({"email": email})


def create_seller(data):
    return sellers_collection.insert_one(data)


def get_seller_by_id(id):
    return sellers_collection.find_one({"_id": id})