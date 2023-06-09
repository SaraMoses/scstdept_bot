# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import collections

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
 
import sqlite3
import random
from fuzzywuzzy import process

class PositionType(Action):
    def name(self) -> Text:
        return "PositionType"
    # ഫ്രീഷിപ് കാർഡിനായി
    def most_common(self, lst):
        return max(set(lst), key=lst.count)
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot('query_position'))
        position = tracker.get_slot('query_position')
        conn = DbQueryMethods.create_connection(db_file='./career_db/dbConnect')
        answer = DbQueryMethods.select_answers(self.most_common, conn, position )
        dispatcher.utter_message(text=str(answer))
        return
    
class JoiningDate(Action):
    def name(self) -> Text:
        return "JoiningDate"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        print(tracker.get_slot('query_position'))
        position = tracker.get_slot('query_position')
        conn = DbQueryMethods.create_connection(db_file='./career_db/careerDB')
        date = DbQueryMethods.select_date_by_slot(conn=conn,slot_name= "POSITION", slot_value=position.upper())
        dispatcher.utter_message(text="joining date is "+str(date))
        return
    
class JobQualif(Action):
    def name(self) -> Text:
        return "JobQualif"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        print(tracker.get_slot('query_position'))
        position = tracker.get_slot('query_position')
        conn = DbQueryMethods.create_connection(db_file='./career_db/careerDB')
        qualification = DbQueryMethods.select_qualif_by_slot(conn=conn,slot_name= "POSITION", slot_value=position.upper())
        dispatcher.utter_message(text="job qualification is "+str(qualification))
        return



class DbQueryMethods:
    def create_connection(db_file):
        conn = sqlite3.connect(db_file)
        return conn
    
    def select_answers(most_common, conn, question):
        rows = []
        cur = conn.cursor()
        cur.execute(f"select answers from resource where questions like '%{str(question.replace(' ', '%'))}%'")
        rows = cur.fetchall()
        print(rows)
        if rows == []:
            for q in question.split():
                cur.execute(f"select distinct answers from resource where questions like '%{q}%'")
                rows.append(cur.fetchall())
                print(rows)
        flat = [x for sublist in rows for x in sublist]
        print(flat)
        return flat[0]
        
    
    def get_closest_value(conn, slot_name, slot_value):
        #get distinct values from  target column
        fuzzy_match_cur = conn.cursor()
        fuzzy_match_cur.execute(f"""select distinct {slot_name} from careerresource""") 
        column_values = fuzzy_match_cur.fetchall()
        top_match = process.extractOne(slot_value,column_values)
        return(top_match[0])
    
    def get_all(conn, slot_name):
        #get distinct values from  target column
        fuzzy_match_cur = conn.cursor()
        fuzzy_match_cur.execute(f"""select distinct {slot_name} from careerresource""") 
        column_values = fuzzy_match_cur.fetchall()
        return column_values
    
    def select_by_slot(conn, slot_name, slot_value):
        cur = conn.cursor()
        cur.execute(f'''select * from careeresource where {slot_name}="{slot_value}"''')
        rows = cur.fetchall()
        return (rows)
    
    def select_date_by_slot(conn, slot_name, slot_value):
        cur = conn.cursor()
        cur.execute(f'''select JOINING_DATE from careerresource where {slot_name}="{slot_value}"''')
        rows = cur.fetchall()
        return (rows[0][0])
    
    def select_salary_by_slot(conn, slot_name, slot_value):
        cur = conn.cursor()
        cur.execute(f'''select SALARY from careerresource where {slot_name}="{slot_value}"''')
        rows = cur.fetchall()
        return (rows[0][0])
    
    def select_qualif_by_slot(conn, slot_name, slot_value):
        cur = conn.cursor()
        cur.execute(f'''select QUALIF from careerresource where {slot_name}="{slot_value}"''')
        rows = cur.fetchall()
        return (rows[0][0])
    
    def rows_info_as_text(rows):
        if len(list(rows)) < 1:
            return "no result"
        else:
            return ""   
            
            
            

