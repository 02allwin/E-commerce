import spacy
import mysql.connector as con 
from home.database import *
from home.admin_action import display_category

class ChatBot:
    
    def __init__(self,text):
        self.nlp = spacy.load("en_core_web_sm")
        self.category_keywords ={data['name'].lower() for data in display_category() }
        print(self.category_keywords)
        self.text = text


    def detect_price(self,docs):
        price=0
        for doc in docs.ents:
            if doc.label_  in ["CARDINAL" , "MONEY"]:
                price=doc

        return price

    def detect_brand(self,docs):
        brand=""
        for doc in docs.ents:
            if doc.label_ in ["ORG","PRODUCT"]:                
                brand=doc
        return brand


    def detect_category(self,doc):
        for token in doc:
                lemma = token.lemma_.lower()
                if lemma in self.category_keywords:
                    return lemma
        return None
    
    def get_query(self):

        self.text = self.text.lower()
        doc = self.nlp(self.text)

        price =self. detect_price(doc)
        brand = self.detect_brand(doc)
        cate = self. detect_category(doc)

        print("res ",price,brand,cate)

        if cate:
            if brand !="":
                sql = f"SELECT * FROM service  WHERE (category={cate} or price <={price}) OR name={brand}"
                print(sql)
                return sql,(cate,price,brand)
            else:
                sql = f""" SELECT s.*, sc.*
                    FROM service s
                    INNER JOIN services_category sc ON sc.category_id = s.category_id
                    WHERE s.service_price <= {price} or sc.category_name='{cate}';
                """
                #sql = f"SELECT * FROM service  WHERE (category={cate} AND price <={price})"
                print(sql)
                return sql,(cate,price)
        else:
            return False,False
    

    
class RunQuery:

    def __init__(self):
        self.mycon , self.cur = connect()
    
    def run_chatbot_query(self,sql,val):

        try:
            print(sql)
            self.cur.execute(sql)
            data = self.cur.fetchall()
            print(data)

            if data:
                services = [
                    {
                        'service_id': row[0],
                        'service_name': row[1],
                        'service_description': row[2],
                        'service_price': row[3],
                        'serimage': row[4],  # Ensure this matches the column name in DB
                        'city_pincode': row[5]
                    } for row in data
                ]
                return services
            else:
                return False

        except Exception as e:
            print("Error ",e)
            return False
    
