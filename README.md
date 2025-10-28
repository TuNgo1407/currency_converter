# EUR-VND Exchange Rate Monitor

*🚀 Automated exchange exchange tracker with database storage and Discord notifications.*


## 🧩 Components
- **Data Source**: [Exchange Rate API](https://www.exchangerate-api.com/) 
- **Processor**: Python
- **Scheduler**: Github Actions 
- **Database**: Supabase PostgreSQL
- **Notifier**: Discord Webhook 

## 🔄 Data flow
1. Github Actions triggers the Python script daily at 8 am (GMT+1)
2. The script fetches latest rates from Exchange Rate API
3. Data is processed, transformed and stored in Cloud Database - Supabase
4. Notifications like: today exchange rate, errors, runtime failures will be sent to Discord


