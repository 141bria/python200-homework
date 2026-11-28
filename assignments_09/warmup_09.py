                            #Supabase Connection#
#Connection#
#Q1#
#Supabase needs a Project URL & API Key to connect to the project. They can be found in Project Setting in the API Keys section & they shouldn't be hardcoded in my python script because they could be shown in Github , which could unintentionally allow unauthorized users to access or change our data#

#Q2#
import os
from dotenv import load_dotenv
from supabase import create_client
def get_client():
    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    if SUPABASE_KEY == None or SUPABASE_URL == None :
        raise ValueError("error: Your Supabase Key or URL is missing, please try again.")
    return create_client(SUPABASE_URL,SUPABASE_KEY)
#Q3#
# Row Level Security(RLS) is a form of security that allows us to control which rows a user can access. We disabled it for this course to make reading & writing data easier without creating access policies. A real world example of when we would need to enable RLS would be a banking app where users should only be able to see their own banking info and not someone else's.
                                            #supabase-py CRUD#
#Q1#
# def insert_test_record(supabase):
#     record = {
#         "date": "2026-11-27",
#         "temperature_2m_max": 10.0,
#         "temperature_2m_min": 5.0,
#         "precipitation_sum" : 0.0,
#         "wind_speed_10m_max" : 7.1

#     }
#     response = supabase.table("weather_raw").insert(record).execute()
#     print(response.data)
supabase = get_client()
# insert_test_record(supabase)
# If we ran the function twice, it would raise an error because a row with the same primary key already exsists. To make it safe to run multiple times in the future, I would use upsert  so it updates exsisiting records.#
#Q2#
def get_records_by_date_range(supabase,start,end):
    response = (
        supabase.table("weather_raw")
        .select("*")
        .gte("date",start )
        .lte("date", end)
        .execute()
    )
    return response.data
print (get_records_by_date_range(supabase,"2026-11-27","2026-12-29"))
#Q3#
# Insert is used to insert a single record or a list of new records. Upsert is used to insert a new record if it doesn't exsist, but if it already exsists, it updates the existing record withoyt a dupliacate key error. I would use insert when someone placesa new pizza order at Domino's because it's a new order. I would use upsert when updating an employee info in an applicant tracking system because the employee may already exsist and if they don't a new record can be made.#
records = [
    {"date": "2026-11-27","temperature_2m_max": 8.0,"temperature_2m_min": 2.0,"precipitation_sum" : 3.0, "wind_speed_10m_max" : 7.1},
    {"date": "2026-10-30","temperature_2m_max": 5.0,"temperature_2m_min": 1.0,"precipitation_sum" : 9.0, "wind_speed_10m_max" : 9.3}
]
def safe_upsert(supabase,records):
    response = (
        supabase.table("weather_raw")
        .upsert(records, on_conflict = "date")
        .execute()
    )
    print(len(response.data))
safe_upsert(supabase,records)
