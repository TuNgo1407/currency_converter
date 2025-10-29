from discord_webhook import DiscordWebhook
import os
import pandas as pd
from datetime import datetime



def get_exchange_rate_message (df : pd.DataFrame, base_code:str = "EUR" , target_code: str = "VND") -> str:
	try: 
		sending_data_df = df.loc[(df['base_code'] == base_code) & (df['target_code'] == target_code) ,:]

		sending_data_dict = sending_data_df.to_dict('list')
		date = sending_data_dict['date_readable'][0]
		conversion_rate = sending_data_dict['conversion_rates'][0]
		mess = f"Conversion Rate: {conversion_rate}\nDate: {date} \nBase Currency: {base_code} \nTarget Currency: {target_code}"
		return mess
	except (IndexError, KeyError, ValueError) as e:
		today_date = datetime.today().strftime("%d %b %Y")
		print (f"{today_date}\nError when getting exchange rate message")
		raise
		




def send_data_message_to_discord (df : pd.DataFrame, base_code:str = "EUR" , target_code: str = "VND" ):
    message = get_exchange_rate_message(df,base_code,target_code)
    webhook_url = os.environ.get("WEBHOOK_URL")
    webhook = DiscordWebhook(url=webhook_url, content=message)
    webhook.execute()

def send_db_update_notification_to_discord ():
    message = "Updates Database  successfully"
    webhook_url = os.environ.get("WEBHOOK_URL")
    webhook = DiscordWebhook(url=webhook_url, content=message)
    webhook.execute()

def send_error_to_discord(e):
	webhook_url = os.environ.get("WEBHOOK_URL")
	error_message = f"{type(e).__name__}: {str(e)}"
	webhook = DiscordWebhook(url=webhook_url, content=error_message)
	webhook.execute()
