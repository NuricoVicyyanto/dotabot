import random
from urllib.request import urlopen
from tabulate import tabulate
import pandas as pd
import json

url = "https://dotabot.mitrajamurbondowoso.com/public/get-matches-player"
response = urlopen(url)
data_json = json.loads(response.read())

df = pd.DataFrame(data_json['matches'])
df['result'] = df['details'].apply(lambda x: x['result'])
df['date'] = df['details'].apply(lambda x: x['date'])
df['kills'] = df['details'].apply(lambda x: x['kills'])
df['deaths'] = df['details'].apply(lambda x: x['deaths'])
df['assists'] = df['details'].apply(lambda x: x['assists'])
df['gpm'] = df['details'].apply(lambda x: x['gpm'])

table_dt = tabulate(df[['match_id', 'kills', 'deaths', 'assists', 'gpm', 'result', 'date']], headers='keys', tablefmt='fancy_grid')
# df = pd.json_normalize(data_json,sep="_")
# table_str = df.to_string(index=False, justify='center', header=True).replace('\n ', '\n')

def handle_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'Haii!'

    if p_message == 'ngapain':
        return 'Ga Ngapa Ngapain'

    if p_message == 'roll':
        return str(random.randint(1, 10))

    if p_message == 'pagi':
        return 'Pagi Juga'

    if p_message == '!help':
        return "`This is a help message that you can modify.`"

    if p_message == 'data':
        return table_dt