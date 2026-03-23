from pymongo import MongoClient

connection_string = "mongodb+srv://dianakov_db_user:QhlttWmzwksqA7yY@habitcluster1.yzrxxet.mongodb.net/goalsplatform?retryWrites=true&w=majority"

client = MongoClient(connection_string)
db = client["goalsplatform"]  # точна назва бази

print("MongoDB connected successfully")
print("Collections:", db.list_collection_names())


from pymongo import MongoClient

connection_string = "mongodb+srv://dianakov_db_user:QhlttWmzwksqA7yY@habitcluster1.yzrxxet.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)

print("MongoDB connected successfully")
print("Databases:", client.list_database_names())  # покаже всі бази в кластері
