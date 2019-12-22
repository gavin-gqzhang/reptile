import pymongo

class Connect:
    def conn(self):
        global db
        client=pymongo.MongoClient(host='localhost',port=27017)
        db=client.analyze

        print('连接成功')

    def insert_python(self,data):
        collection=db.python
        result=collection.insert(data)


    def select_python(self):
        collection=db.python
        results=collection.find()

        return results

    def remove(self):
        collection=db.python
        results=collection.remove()

    def insert_Java(self,data):
        collection=db.Java
        result=collection.insert(data)


    def select_Java(self):
        collection=db.Java
        results=collection.find()

        return results

    def insert_PHP(self,data):
        collection=db.PHP
        result=collection.insert(data)


    def select_PHP(self):
        collection=db.PHP
        results=collection.find()

        return results