# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from datetime import datetime
from pytz import timezone
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

# timezones = {
#     "London":"UTC + 1:00",
#     "Sofia":"UTC + 3:00",
#     "Lisbon":"UTC + 2:00",
#     "Mumbai":"UTC + 4:00"
# }

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time_zone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")

        locator = Nominatim(user_agent="myGeocoder")
        location = locator.geocode(city)

        tf = TimezoneFinder()
        latitude, longitude = location.latitude, location.longitude
        time_zone_find = tf.timezone_at(lng=longitude, lat=latitude)  # returns 'Europe/Berlin'
        show_time = timezone(time_zone_find)
        sa_time = datetime.now(show_time)
        output = sa_time.strftime('%Y-%m-%d_%H-%M-%S')


        dispatcher.utter_message(text= output)

        return []
