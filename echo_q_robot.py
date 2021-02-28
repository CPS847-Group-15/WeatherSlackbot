import slack
import os
from pathlib import Path
from dotenv import load_dotenv
# Import Flask
from flask import Flask, request, Response
# Handles events from Slack
from slackeventsapi import SlackEventAdapter
import requests

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

message_counts = {}

@slack_event_adapter.on('message')
def message(payload): 
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    
    if BOT_ID != user_id: 
        if  text.endswith('?'):
            client.chat_postMessage(channel=channel_id, text=text)

@app.route('/message-count', methods=['POST'])
def message_count(): 
    data = request.form 
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id, 0)
    
    client.chat_postMessage(channel=channel_id, text=f"Message: {message_count}")
    return Response(), 200 
    
# Get your weather_api from the website
weather_api = 'http://api.openweathermap.org/data/2.5/weather?'
weather_api_key=os.environ['WEATHER_TOKEN']
@app.route('/weather', methods=['POST'])
def weather():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    city_name = event.get('text')
    # The following uses the file 'city.list.json' to find the city id. We will need this file to implement spelling correction
    """
    with open('city.list.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    
    for city in cities:
        if city_name == city['name']:
            city_id = city['id']
            url = f"{weather_api}id={city_id}&appid={weather_api_key}"
            weather = requests.request("GET", url).json()
            response = f"The Weather in {weather['name']} is {weather['weather'][0]['main']}: {weather['weather'][0]['description']}. It's {round(weather['main']['temp'] - 273.15,1)} degrees Celsius."
            client.chat_postMessage(channel=channel_id, text=response)
            return Response(), 200
    
    client.chat_postMessage(channel=channel_id, text=f"Cannot find city: {city_name}")
    return Response(), 200
    """
    # This just uses the name.
    url = f"{weather_api}q={city_name}&appid={weather_api_key}"
    request = requests.request("GET", url).json()
    if weather['cod'] == '200':
        response = f"The Weather in {weather['name']} is {weather['weather'][0]['main']}: {weather['weather'][0]['description']}. It's {round(weather['main']['temp'] - 273.15,1)} degrees Celsius."
        client.chat_postMessage(channel=channel_id, text=response)
        return Response(), 200
    client.chat_postMessage(channel=channel_id, text=weather['cod'] + " : " + weather['message'])
    return Response(), 200
    
    
if __name__ == "__main__":
    app.run(debug=True)

