# 安装驱动
sudo pip install pymongo
# 启动mongo失败
sudo ./bin/mongod -dbpath ./data/db/

# 校验安装结果
import pymongo
pymongo.version
# hello-world
# 链接数据库
from pymongo import MongoClient
uri="mongodb://127.0.0.1:27017"
client = MongoClient(uri)
print(client)

# insert
db = client["eshop"]
user_coll = db["users"]
new_user = {"username":"nina", "password":"123", "eamil": "123@163.com"}
result = user_coll.insert_one(new_user)
result

# update
result = user_coll.update_one({"username":"nina"}, {"$set":{"phone":"456"}})
print(result)

# query
result = user_coll.find_one()

