import time
import requests
import pandas as pd

from important_events import important_events

def event_name(event: str) -> str:
    if '(' in event:
        split = event.split(' ')
        event_new = ' '.join(split[:-1])
        return event_new
    else:
        return event
    
def update_event_histories(path: str, events: list=important_events().keys()) -> None:
    """
    Iterates through all events in events list (events_to_update) and updates the event histories
    in csvs folder
    """
    events_codes = important_events()

    for event in events:

        url = f'https://sbcharts.investing.com/events_charts/us/{events_codes[event]}.json'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Referer': 'https://www.investing.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            }
        
        response = requests.get(url, headers=headers)
        name = event_name(event)

        if response.status_code == 200:
            print(f'{name} - OK!')
        else:
            print(f'{name} - ERROR!')

        response_json = response.json()
        attr = response_json['attr']

        df = pd.DataFrame(attr)
        df['actual'] = df['revised'].where(df['revised'].notna(), df['actual'])
        df['previous'] = df['actual'].shift(1)
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True).dt.tz_convert('US/Eastern').dt.date
        df = df.drop(columns='timestamp')

        if 'revised' in df.columns: 
            df = df[['datetime','actual_state','actual','forecast', 'previous', 'revised']]
        else:
            df = df[['datetime','actual_state','actual','forecast', 'previous']]

        df.to_csv(f'{path}{name}.csv')
        time.sleep(2)

if __name__ == "__main__":
    update_event_histories('./event_histories/')
    print("Event histories update complete.")
