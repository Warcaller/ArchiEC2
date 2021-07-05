import pytest
from typing import Dict, List
import ArchieMate.Twitch.IRC as TwitchIRC

@pytest.mark.parametrize("description", "tags", "expected", [
  (
    "Simple user's message info in tags with @ in the beginning"
    "@login=ronni;target-msg-id=abc-123-def",
    {
      "login": "ronni",
      "target-msg-id": "abc-123-def",
    }
  ),
  (
    "User's info in GLOBALUSERSTATE's tags",
    "badge-info=subscriber/8;badges=subscriber/6;color=#0D4200;display-name=dallas;"
    "emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;"
    "turbo=0;user-id=1337;user-type=admin",
    {
      "badge-info": "subscriber/8",
      "badges": "subscriber/6",
      "color": "#0D4200",
      "display-name": "dallas",
      "emote-sets": "0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239",
      "turbo": "0",
      "user-id": "1337",
      "user-type": "admin",
    }
  ),
  ("Empty tags", "", {}),
  ("Failsafe", None, {}),
])
def test_parse_tags(description: str, tags: str, expected: Dict[str, str]):
  assert(TwitchIRC.parse_tags(tags) == expected), description


@pytest.mark.parametrize("description", "badges", "expected", [
  (
    "Example badge of a global mod with turbo",
    "global_mod/1,turbo/1",
    {
      "global_mod": 1,
      "turbo": 1
    }
  ),
  (
    "Example badge of a streamer with Twitch Prime",
    "broadcaster/1,subscriber/0,premium/1",
    {
      "broadcaster": 1,
      "subscriber": 0,
      "premium": 1
    }
  ),
  (
    "Example of a moderator pleb",
    "moderator/1",
    {
      "moderator": 1
    }
  ),
  (
    "Example of a staff member with bits",
    "staff/1,bits/1000",
    {
      "staff": 1,
      "bits": 1000
    }
  ),
  ("Example of an ultra pleb", "", {}),
  ("Failsafe", None, {})
])
def test_parse_badges(description: str, badges: str, expected: Dict[str, int]):
  assert(TwitchIRC.parse_badges(badges) == expected), description


@pytest.mark.parametrize("description", "badge_info", "expected", [
  (
    "Example badge info of a streamer",
    "subscriber/43",
    {"subscriber": 43}
  ),
  ("Example badge info of a pleb", "", {}),
  ("Failsafe", None, {}),
])
def test_parse_badge_info(description: str, badge_info: str, expected: Dict[str, int]):
  assert(TwitchIRC.parse_badge_info(badge_info) == expected), description

@pytest.mark.parametrize("description", "string", "expected", [
  (
    "Test string containing all possible escaped characters",
    "This\\sis\\sa\\stest\\sof\\san\\sescaped\\smessage\\:\\sAll\\sescaped\\scharacters\\sare\\sincluded.\\r\\n",
    "This is a test of an escaped message; All escaped characters are included."
  ),
  (
    "Test string also containing invalid escaped characters",
    "This\\sis\\san\\s\\invalid\\sescaped\\scharacter.",
    "This is an invalid escaped character."
  ),
  (
    "Test string containing \\ at the end",
    "This\\sstring\\scontains\\sa\\scharacter\\s\\\\\\sat\\sthe\\end.\\",
    "This string contains a character \\ at the end."
  ),
])
def test_escape_irc_string(description: str, string: str, expected: str):
  assert(TwitchIRC.escape_irc_string(string) == expected), description


@pytest.mark.parametrize("description", "irc_text", "expected", [
  (
    "Example IRC text of a system message for user ronni who just resubscribed",
    "ronni\\shas\\ssubscribed\\sfor\\s6\\smonths!",
    "ronni has subscribed for 6 months!"
  ),
  (
    "Example IRC text of a system message for user TWW2 who just gifted subscription to Mr_Woodchuck",
    "TWW2\\sgifted\\sa\\sTier\\s1\\ssub\\sto\\sMr_Woodchuck!",
    "TWW2 gifted a Tier 1 sub to Mr_Woodchuck!"
  ),
  (
    "Example IRC text of a system message for an anonymous user who just gifted subscription to TenureCalculator",
    "An\\sanonymous\\suser\\sgifted\\sa\\sTier\\s1\\ssub\\sto\\sTenureCalculator!",
    "An anonymous user gifted a Tier 1 sub to TenureCalculator!"
  ),
  (
    "Example IRC text of a system message for a raid of 15 people from TestChannel"
    "15\\sraiders\\sfrom\\sTestChannel\\shave\\sjoined\n!",
    "15 raiders from TestChannel have joined!"
  ),
  (
    "Example IRC text of a system message for a new chatter ritual for a user Seventoes",
    "Seventoes\\sis\\snew\\shere!",
    "Seventoes is new here!"
  ),
  ("Empty display name", "", ""),
  ("Failsafe", None, ""),
])
def test_escape_irc_text(description: str, irc_text: str, expected: str):
  assert(TwitchIRC.escape_irc_text(irc_text) == expected), description



