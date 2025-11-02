import os
import pandas as pd
from supabase import create_client
from postgrest.exceptions import APIError



def get_extreme_values():
	try:
		url = os.environ.get("SUPABASE_URL")
		key = os.environ.get("SUPABASE_KEY")

		if not url or not key:
			raise ValueError ("Missing Supabase URL or Key")
		supabase = create_client(url,key)

	
		response = (supabase.rpc("get_extreme_exchange_rate", {
			"target_currency":"VND"
		})).execute()
		if response.data:
			return response.data[0]
		else: return []
	except ValueError as e:
		print (f"Error: {e}")
		raise
	except APIError as e:
		print (f"Supabase API Error")
		raise



def upsert_rates_table (df : pd.DataFrame):
	rates_table = os.environ.get("CURRENTCY_TABLE")
	try:
		url = os.environ.get("SUPABASE_URL")
		key = os.environ.get("SUPABASE_KEY")

		if not url or not key:
			raise ValueError ("Missing Supabase URL or Key")
		supabase = create_client(url,key)

		if df.empty:
			raise ValueError ("Dataframe is empty")
		
		records = df.to_dict('records')
		response = supabase.table(rates_table).upsert(records,on_conflict="base_code,target_code,date_iso").execute()
		print(response)

	except ValueError as e:
		print (f"Error: {e}")
		raise
	except APIError as e:
		print (f"Supabase API Error")
		raise




