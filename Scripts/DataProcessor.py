import pandas as pd



def get_latest_exchange_rates_df(data: dict, target_codes) -> pd.DataFrame:
    try:
        if not isinstance(data, dict):
            raise TypeError(f"Expected input as dict got {type(data).__name__}" )


        required_keys = ['conversion_rates', 'result', 'time_last_update_unix', 'base_code']
        for key in required_keys:
            if key not in data:
                raise KeyError(f"Missing required key: {key}")

        rates_df = pd.DataFrame(
            data=data['conversion_rates'].items(),
            columns=['target_code', 'conversion_rates']
        )
        rates_df.insert(0, 'result', data['result'])
        rates_df.insert(1, 'time_last_update_unix', data['time_last_update_unix'])
        rates_df.insert(2, 'base_code', data['base_code'])

        rates_df = rates_df.loc[rates_df['target_code'].isin(target_codes), :].reset_index(drop=True)
        rates_df['date_iso'] = pd.to_datetime(rates_df['time_last_update_unix'],unit ='s').dt.strftime("%Y-%m-%d")
        rates_df['date_readable'] = pd.to_datetime(rates_df['time_last_update_unix'],unit ='s').dt.strftime("%d %b %Y")
        rates_df.drop('time_last_update_unix', axis=1, inplace=True)
        
        print(rates_df)
        return rates_df

    except (TypeError, KeyError) as e:
        print(f"Input Error: {e}")
        raise
        