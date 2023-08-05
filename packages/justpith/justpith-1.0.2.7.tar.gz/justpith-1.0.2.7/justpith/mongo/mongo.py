from pymongo import MongoClient
from time import time

class Mongo(object):

    ##### GENERAL #####
    def __init__(self, host, port, db):
        self.host       = host
        self.port       = port
        self.db         = db

        self.client     = None
        self.connection = None
        self.connect()

    def connect(self):
        self.client     = MongoClient(self.host, self.port)
        self.connection = self.client[self.db]


    ##### JUSTPITH SERVER #####
    def insert_news(self, news):
        selected_collection = self.connection['News']
        result = selected_collection.insert(news)

    def update_news_report(self, id_news, queue_name, queue_op):
        selected_collection = self.connection['News']
        result = selected_collection.update_one({'_id': id_news}, {'$push': {'report': {'queue_name': queue_name, 'queue_op': queue_op, 'timestamp': str(time())}}}, upsert=True)

    def update_news_after_parsing(self, id_news, ttl, article, article_cleaned, queue_name):
        selected_collection = self.connection['News']
        result = selected_collection.update_one({'_id': id_news}, {'$set': {'TTL': ttl, 'article': article, 'article_cleaned': article_cleaned}, '$push': {'report': {'queue_name': queue_name, 'queue_op': 'IN', 'timestamp': str(time())}}}, upsert=True)

    def update_news_after_similarity(self, id_news, doc_sim, topic_sim):
        selected_connection = self.connection['News']
        result = selected_connection.update_one({'_id': id_news}, {'$set': {'doc_sims': doc_sim, 'topic_sims': topic_sim}})


    ##### JUSTPITH WEB SERVICE TEXT ANALYSIS #####
    def get_docs_to_build_model(self, category):
        selected_collection = self.connection['News']
        result = selected_collection.find({'category_title': category, 'in_model': 1})
        # docs = []
        # for doc in result:
        #     docs.append(doc['article'])
        # return docs
        return result

    def update_news_id_for_model(self, id_news, id_news_corpus):
        selected_connection = self.connection['News']
        result = selected_connection.update_one({'_id': id_news}, {'$set': {'id_corpus': id_news_corpus}})


    def update_reccomended_users(self, id_news, users_list):
        selected_connection = self.connection['News']
        result = selected_connection.update_one({'_id': id_news}, {'$set': {'users_list': users_list}})

    def get_reccomended_users(self, id_news):
        selected_connection = self.connection['News']
        result = selected_connection.find_one({'_id': id_news})
        return result['users_list']

    def insert_list_id_corpus(self,id_index, list_id_corpus):
        selected_connection = self.connection['Indexes']
        result = selected_connection.update_one({'_id': id_index}, {'$set': {'list_id_corpus': list_id_corpus}})


    def insert_index(self, data):
        selected_collection = self.connection['Indexes']
        _id = data['_id']
        model_exist = selected_collection.find({'_id': _id}).count()
        if model_exist == 0:
            result = selected_collection.insert(data)

    def update_active_index(self, id_index, active, category, type):
        if active == 1:
            #result1 = self.connection['Indexes'].update_many({"active": 1, "category":category, "type": type}, {"$set": {"active": 0}})
            result2 = self.connection['Indexes'].find_one_and_update({'_id': id_index}, {'$set': {'active': active}})
        elif active == 0:
            result3 = self.connection['Indexes'].find_one_and_update({'_id': id_index}, {'$set': {'active': active}})

    def set_in_model(self, category):
        selected_connection = self.connection["News"]
        result = selected_connection.update_many({ "article_cleaned": { "$gt": [] }, "category_title": category }, {"$set": {"in_model": 1}})
        result = selected_connection.find({"category_title": category, "in_model": 1}).count()
        return int(result)

    def get_news_parsed(self, category):
        selected_connection = self.connection["News"]
        result = selected_connection.find({"article_cleaned": {"$gt": []}, "category_title": category})
        return result


    def get_info_active_model(self, category, type):
        selected_collection = self.connection['Indexes']
        result = selected_collection.find_one({'category': category, 'type': type, 'active': 1})
        return result

    def get_info_active_model_by_id(self, id):
        selected_collection = self.connection['Indexes']
        result = selected_collection.find_one({'_id': id, 'active': 1})
        return result


    def update_news_similarities(self, doc_id, doc_sims, topic_sims=[]):
        selected_connection = self.connection["News"]
        result = selected_connection.update({"_id": doc_id}, {"$set": {"doc_sims": doc_sims, "topic_sims": topic_sims}})

    def get_news_from_idcorpus(self,list_id):
        docs = []
        selected_connection = self.connection["News"]
        result = selected_connection.find({"id_corpus": {"$in": list_id}}, {"_id":1, "id_corpus":1,"category_title":1,"title":1,"tags":1,"url":1,"article":1})
        for doc in result:
            docs.append(doc)
        return docs

    def get_one_news_from_idcorpus(self,id,category):
        docs = []
        selected_connection = self.connection["News"]
        result = selected_connection.find_one({"id_corpus": id, "category_title":category},
                                          {"_id": 1, "id_corpus": 1, "category_title": 1, "title": 1, "tags": 1,
                                           "url": 1, "article": 1})
        return result

    def get_news_from_id(self,id):
        selected_connection = self.connection["News"]
        result = selected_connection.find_one({"_id":id})
        return result


    def get_id_corpus(self, id):
        selected_connection = self.connection["Indexes"]
        result = selected_connection.find_one({"_id":id}, {"id_to_idcorpus":1})['id_to_idcorpus']

        return result

    def get_all_models(self):
        models = []
        selected_collection = self.connection['Indexes']
        result = selected_collection.find()
        for elem in result:
            models.append(elem)
        return models

    def remove_model(self, id):
        selected_connection = self.connection["Indexes"]
        result = selected_connection.delete_one({'_id': id})
        return result

    def get_categories(self):
        selected_collection = self.connection['Indexes']
        selected_collection.find({'category_title'})

    ###########  NEWS CONSUMER  #####################

    def get_mf_users_raccomandations(self, job_id):
        selected_collection = self.connection['Users']
        #result = selected_collection.find({},{'mf_raccomandations.{}'.format(str(job_id)):1})
        result = selected_collection.find({"mf_raccomandations.{}".format(str(job_id)):{"$exists": True}}, {'mf_raccomandations.{}'.format(str(job_id)):1})
        #result = selected_collection.find({})
        return result

    def update_users_raccomandations(self, news_id, users_to_raccomand):
        selected_collection = self.connection['Users']
        for elem in users_to_raccomand:
            id_user = elem[0]
            weight_racc = elem[1]
            selected_collection.update({'_id': str(id_user)}, {'$set': {'raccomandations.{}'.format(str(news_id)): weight_racc}}, upsert=True)

    def get_index(self, id_index):
        selected_collection = self.connection['Indexes']
        return selected_collection.find_one({'_id': id_index})


    def get_all_categories(self):
        selected_collection = self.connection['Categories']
        return selected_collection.find()

