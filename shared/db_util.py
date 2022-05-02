from supabase import create_client, Client
from dotenv import load_dotenv
import logging
import os
# from tenacity import *
# 加载文件
load_dotenv(".env")
supabase_url = os.environ.get('supabase_url')
supabase_apikey = os.environ.get('supabase_apikey')
supabase_db: Client = create_client(
    supabase_url=supabase_url, supabase_key=supabase_apikey)

def supabase():
# 加载文件
    load_dotenv(".env")
    supabase_url = os.environ.get('supabase_url')
    supabase_apikey = os.environ.get('supabase_apikey')
    supabase_db: Client = create_client(
        supabase_url=supabase_url, supabase_key=supabase_apikey)    
    return supabase_db
def supabase_coldstart(supabase_db):
    data = supabase_db.table("tiktoka_douyin_users").insert({}).execute()

# @retry(stop=stop_after_attempt(10))
def supabaseuserquery(tablename,sec_uid):
    if sec_uid=='' or sec_uid is None:
        data = supabase_db.table(tablename).select().execute()    
    
    else:
        try:
            data = supabase_db.table(tablename).select("*").eq("sec_uid", sec_uid).execute()    
            
        except:
            data.data=''
            raise Exception
    return data.data
# @retry(stop=stop_after_attempt(10))
def supabaseuseradd(tablename,users):
    try:
        data = supabase_db.table(tablename).insert(users).execute()    
    except:
        raise Exception
# @retry(stop=stop_after_attempt(10))
def supabaseuserupdate(tablename,user,uid):
    try:
        data = supabase_db.table(tablename).update(user).eq("uid", uid).execute()    
    except:
        raise Exception