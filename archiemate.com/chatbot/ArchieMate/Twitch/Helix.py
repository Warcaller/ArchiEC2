import requests
from os import environ as env

from typing import Optional, Dict, List, Optional

import ArchieMate.Logger as Logger

logger: Logger = Logger.get_logger(__name__)

CLIENT_ID = env.get("CLIENT_ID")
OAUTH = env.get("OAUTH")

class HelixUser:
  def __init__(self, json):
    logger.debug(f"HelixUser.__init__(json: {json})")
    self.id = json.get("id", None)
    self.login = json.get("login", None)
    self.display_name = json.get("display_name", None)
    self.type = json.get("type", None)
    self.broadcaster_type = json.get("broadcaster_type", None)
    self.description = json.get("description", None)
    self.profile_image_url = json.get("profile_image_url", None)
    self.offline_image_url = json.get("offline_image_url", None)
    self.view_count = json.get("view_count", None)
    self.email = json.get("email", None)
    self.created_at = json.get("created_at", None)
    logger.debug(f"Result: {self.__dict__}")

    """
{
  "data": [
    {
      "id": "141981764",
      "login": "twitchdev",
      "display_name": "TwitchDev",
      "type": "",
      "broadcaster_type": "partner",
      "description": "Supporting third-party developers building Twitch integrations from chatbots to game integrations.",
      "profile_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png",
      "offline_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/3f13ab61-ec78-4fe6-8481-8682cb3b0ac2-channel_offline_image-1920x1080.png",
      "view_count": 5980557,
      "email": "not-real@email.com",
      "created_at": "2016-12-14T20:32:28.894263Z"
    }
  ]
}
    """

def users(login: str) -> HelixUser:
  logger.debug(f"users(login: '{login}')")
  url = f"https://api.twitch.tv/helix/users?login={login}"
  headers = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {OAUTH}"
  }
  response_json = requests.get(url, headers=headers).json()
  logger.debug(f"GET '{url}' with headers '{headers}' returned '{response_json}'")
  return response_json["data"][0] if "data" in response_json else {}
  
