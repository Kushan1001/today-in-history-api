from flask import Flask, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

from datetime import datetime

def parse_date(date_str):
    formats = [
        "%Y-%m-%d %H:%M:%S",  
        "%d-%b-%Y",
        "%d-%b"           
    ]    

    for fmt in formats:
        if fmt == "%d-%b":
            date_str = date_str + '1900'
            fmt = "%d-%b-%Y"
        try:
            return datetime.strptime(str(date_str), fmt).strftime("%d-%B")
        except ValueError:
            continue


def format_enteries():
    date_list = []
    title_list = []
    content_list = []
    image_path_list = []

    df = pd.read_excel('/home/kushan/ICP/suraj_work/apis/Today in history.xlsx')
    filtered_df = df[df['Status'] != 'Done']

    for entry in filtered_df.iterrows():
        entry = entry[1]
        date = entry['Today in History - Date(DD-MMM-YYYY)']
        parsed_date = parse_date(date)
        date_list.append(parsed_date)
        title_list.append(entry['Title'])
        content_list.append(entry['Content'])
        image_path_list.append(entry['Image Path'])
    
    return date_list, title_list, content_list, image_path_list


@app.get('/')
def firstMessage():
    return jsonify({"output": "Api is working properly"}), 200


@app.post('/today-in-history')
def today_in_hist_enteries():
    json_list = []

    date_list, title_list, content_list, image_path_list = format_enteries()
        
    for x1, x2, x3, x4 in zip(date_list, title_list, content_list, image_path_list):
        json_object  = {}

        json_object['date'] = x1
        json_object['title'] = x2
        json_object['content'] = x3
        json_object['image_path'] = x4

        json_list.append(json_object)

    return jsonify({'output': json_list}), 200

