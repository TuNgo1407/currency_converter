import requests
import os
from DataProcessor import get_latest_exchange_rates_df
from WebHookHandler import send_data_message_to_discord, send_error_to_discord,send_db_update_notification_to_discord
from SupaUpdate import upsert_rates_table


TARGET_CODES = ["VND", "USD"]
BASE_CODE = "EUR"

    
def main():
    process_exchange_rate_API(BASE_CODE)


def process_exchange_rate_API(base_code):
	try:
		exchange_rate_url = get_url(base_code)
		latest_exchange_rate_data = get_data(exchange_rate_url)
		lastest_exchange_rate_df = get_latest_exchange_rates_df (latest_exchange_rate_data,TARGET_CODES)
        
		send_data_message_to_discord(lastest_exchange_rate_df,base_code,TARGET_CODES[0])
          
		upsert_rates_table(lastest_exchange_rate_df)
		send_db_update_notification_to_discord()
	except Exception as e:
		send_error_to_discord(e)
        



def get_url(base_code: str = "EUR") -> str:
    exchange_rate_url = os.environ.get("EXCHANGE_RATE_URL")
    api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
    final_url = exchange_rate_url.format(api_key,base_code)
    return final_url



def get_data(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code ==200:
            data = response.json()
            # print(json.dumps(data,indent=4))
            return data
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print ("API Connection Error: ",e)
        raise
    except requests.exceptions.HTTPError as e:
        print ("HTTP Error", e)
        raise
    
if __name__=="__main__":
    main()
    


