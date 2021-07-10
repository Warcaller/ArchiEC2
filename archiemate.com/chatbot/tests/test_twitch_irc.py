import datetime
from typing import Dict, List
import pytest
import ArchieMate.Twitch.IRC as TwitchIRC

@pytest.mark.parametrize("tags,expected", [
  (
    "@login=ronni;target-msg-id=abc-123-def",
    {
      "login": "ronni",
      "target-msg-id": "abc-123-def",
    }
  ),
  (
    "badge-info=subscriber/8;badges=subscriber/6;color=#0D4200;display-name=dallas;" \
    "emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;" \
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
  ("", {}),
  (None, {}),
])
def test_parse_tags(tags: str, expected: Dict[str, str]):
  assert(TwitchIRC.parse_tags(tags) == expected)


@pytest.mark.parametrize("badges,expected", [
  (
    "global_mod/1,turbo/1",
    {
      "global_mod": 1,
      "turbo": 1
    }
  ),
  (
    "broadcaster/1,subscriber/0,premium/1",
    {
      "broadcaster": 1,
      "subscriber": 0,
      "premium": 1
    }
  ),
  (
    "moderator/1",
    {
      "moderator": 1
    }
  ),
  (
    "staff/1,bits/1000",
    {
      "staff": 1,
      "bits": 1000
    }
  ),
  ("", {}),
  (None, {})
])
def test_parse_badges(badges: str, expected: Dict[str, int]):
  assert(TwitchIRC.parse_badges(badges) == expected)


@pytest.mark.parametrize("badge_info,expected", [
  (
    "subscriber/43",
    {"subscriber": 43}
  ),
  ("", {}),
  (None, {}),
])
def test_parse_badge_info(badge_info: str, expected: Dict[str, int]):
  assert(TwitchIRC.parse_badge_info(badge_info) == expected)

@pytest.mark.parametrize("string,expected", [
  (
    "This\\sis\\sa\\stest\\sof\\san\\sescaped\\smessage\\:\\sAll\\sescaped\\scharacters\\sare\\sincluded.\\r\\n",
    "This is a test of an escaped message; All escaped characters are included."
  ),
  (
    "This\\sis\\san\\s\\invalid\\sescaped\\scharacter.",
    "This is an invalid escaped character."
  ),
  (
    "This\\sstring\\scontains\\sa\\scharacter\\s\\\\\\sat\\sthe\\send.\\",
    "This string contains a character \\ at the end."
  ),
])
def test_escape_irc_string(string: str, expected: str):
  assert(TwitchIRC.escape_irc_string(string) == expected)


@pytest.mark.parametrize("irc_text,expected", [
  (
    "ronni\\shas\\ssubscribed\\sfor\\s6\\smonths!",
    "ronni has subscribed for 6 months!"
  ),
  (
    "TWW2\\sgifted\\sa\\sTier\\s1\\ssub\\sto\\sMr_Woodchuck!",
    "TWW2 gifted a Tier 1 sub to Mr_Woodchuck!"
  ),
  (
    "An\\sanonymous\\suser\\sgifted\\sa\\sTier\\s1\\ssub\\sto\\sTenureCalculator!",
    "An anonymous user gifted a Tier 1 sub to TenureCalculator!"
  ),
  (
    "15\\sraiders\\sfrom\\sTestChannel\\shave\\sjoined\\n!",
    "15 raiders from TestChannel have joined!"
  ),
  (
    "Seventoes\\sis\\snew\\shere!",
    "Seventoes is new here!"
  ),
  ("", ""),
  (None, ""),
])
def test_escape_irc(irc_text: str, expected: str):
  assert(TwitchIRC.escape_irc_string(irc_text) == expected)


@pytest.mark.parametrize("emote_range,expected", [
  (
    "0-4,12-16",
    [
      (0, 5),
      (12, 5),
    ]
  ),
  (
    "6-10",
    [
      (6, 5),
    ]
  ),
  ("", []),
  (None, []),
])
def test_parse_emote_range(emote_range: str, expected: List[tuple]):
  assert(TwitchIRC.parse_emote_range(emote_range) == expected)

@pytest.mark.parametrize("emotes,expected", [
  (
    "25:0-4,12-16/1902:6-10",
    {
      25:
        [
          (0, 5),
          (12, 5),
        ],
      1902:
        [
          (6, 5),
        ],
    }
  ),
  ("", {}),
  (None, {}),
])
def test_parse_emotes(emotes: str, expected: Dict[int, List[tuple]]):
  assert(TwitchIRC.parse_emotes(emotes) == expected)


@pytest.mark.parametrize("emote_sets,expected", [
  (
    "0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239",
    [0, 33, 50, 237,793, 2126, 3517, 4578, 5569, 9400, 10337, 12239],
  ),
  ("", []),
  (None, []),
])
def test_parse_emote_sets(emote_sets: str, expected: List[int]):
  assert(TwitchIRC.parse_emote_sets(emote_sets) == expected)


def test_message_notice_authentication_unsuccessful():
  message = ":tmi.twitch.tv NOTICE * :Login failed"
  regex = TwitchIRC.Notice.match(message)
  assert(regex is not None)
  message_notice: TwitchIRC.Notice = TwitchIRC.Notice(regex)
  assert(message_notice.message == "Login failed")


def test_message_generic_authentication_successful():
  message = ":tmi.twitch.tv 001 archiemate :Welcome, GLHF!"
  regex = TwitchIRC.Generic.match(message)
  assert(regex is not None)
  message_generic: TwitchIRC.Generic = TwitchIRC.Generic(regex)
  assert(message_generic.message_number == 1)
  assert(message_generic.bot_user == "archiemate")
  assert(message_generic.message == "Welcome, GLHF!")


def test_message_ping():
  message = "PING :tmi.twitch.tv"
  regex = TwitchIRC.Ping.match(message)
  assert(regex is not None)
  message_ping: TwitchIRC.Ping = TwitchIRC.Ping(regex)
  assert(message_ping.server == "tmi.twitch.tv")


def test_message_privmsg_nonbits_message():
  message = "@badge-info=;badges=global_mod/1,turbo/1;color=#0D4200;display-name=ronni;emotes=25:0-4,12-16/1902:6-10;" \
  "id=b34ccfc7-4977-403a-8a94-33c6bac34fb8;mod=0;room-id=1337;subscriber=0;tmi-sent-ts=1507246572675;turbo=1;" \
  "user-id=1337;user-type=global_mod :ronni!ronni@ronni.tmi.twitch.tv PRIVMSG #ronni :Kappa Keepo Kappa"
  regex = TwitchIRC.PrivMsg.match(message)
  assert(regex is not None)
  message_privmsg: TwitchIRC.PrivMsg = TwitchIRC.PrivMsg(regex)
  assert(message_privmsg.badge_info == {})
  assert(message_privmsg.badges == {"global_mod": 1, "turbo": 1})
  assert(message_privmsg.bits == 0)
  assert(message_privmsg.client_nonce == "")
  assert(message_privmsg.color == "#0D4200")
  assert(message_privmsg.display_name == "ronni")
  assert(message_privmsg.emotes == {25: [(0, 5), (12, 5),], 1902: [(6, 5)]})
  assert(message_privmsg.message_id == "b34ccfc7-4977-403a-8a94-33c6bac34fb8")
  assert(message_privmsg.flags == "")
  assert(message_privmsg.mod == False)
  assert(message_privmsg.reply_parent_display_name is None)
  assert(message_privmsg.reply_parent_message_body is None)
  assert(message_privmsg.reply_parent_message_id is None)
  assert(message_privmsg.reply_parent_user_id is None)
  assert(message_privmsg.reply_parent_user_login is None)
  assert(message_privmsg.room_id == 1337)
  assert(message_privmsg.subscriber == False)
  assert(message_privmsg.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1507246572675 // 1000).replace(microsecond=1507246572675 % (1000 * 1000))))
  assert(message_privmsg.turbo == True)
  assert(message_privmsg.user_id == 1337)
  assert(message_privmsg.user_type == "global_mod")
  assert(message_privmsg.user == "ronni")
  assert(message_privmsg.channel == "ronni")
  assert(message_privmsg.message == "Kappa Keepo Kappa")


def test_message_privmsg_bits_message():
  message = "@badge-info=;badges=staff/1,bits/1000;bits=100;color=;display-name=ronni;emotes=;" \
  "id=b34ccfc7-4977-403a-8a94-33c6bac34fb8;mod=0;room-id=1337;subscriber=0;tmi-sent-ts=1507246572675;" \
  "turbo=1;user-id=1337;user-type=staff :ronni!ronni@ronni.tmi.twitch.tv PRIVMSG #ronni :cheer100"
  regex = TwitchIRC.PrivMsg.match(message)
  assert(regex is not None)
  message_privmsg: TwitchIRC.PrivMsg = TwitchIRC.PrivMsg(regex)
  assert(message_privmsg.badge_info == {})
  assert(message_privmsg.badges == {"staff": 1, "bits": 1000})
  assert(message_privmsg.bits == 100)
  assert(message_privmsg.client_nonce == "")
  assert(message_privmsg.color == "")
  assert(message_privmsg.display_name == "ronni")
  assert(message_privmsg.emotes == {})
  assert(message_privmsg.message_id == "b34ccfc7-4977-403a-8a94-33c6bac34fb8")
  assert(message_privmsg.flags == "")
  assert(message_privmsg.mod == False)
  assert(message_privmsg.reply_parent_display_name is None)
  assert(message_privmsg.reply_parent_message_body is None)
  assert(message_privmsg.reply_parent_message_id is None)
  assert(message_privmsg.reply_parent_user_id is None)
  assert(message_privmsg.reply_parent_user_login is None)
  assert(message_privmsg.room_id == 1337)
  assert(message_privmsg.subscriber == False)
  assert(message_privmsg.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1507246572675 // 1000).replace(microsecond=1507246572675 % (1000 * 1000))))
  assert(message_privmsg.turbo == True)
  assert(message_privmsg.user_id == 1337)
  assert(message_privmsg.user_type == "staff")
  assert(message_privmsg.user == "ronni")
  assert(message_privmsg.channel == "ronni")
  assert(message_privmsg.message == "cheer100")


def test_message_privmsg_reply_to_message():
  message = "@reply-parent-msg-id=b34ccfc7-4977-403a-8a94-33c6bac34fb8 :ronni!ronni@ronni.tmi.twitch.tv PRIVMSG #ronni :Good idea!"
  regex = TwitchIRC.PrivMsg.match(message)
  assert(regex is not None)
  message_privmsg: TwitchIRC.PrivMsg = TwitchIRC.PrivMsg(regex)
  assert(message_privmsg.badge_info == {})
  assert(message_privmsg.badges == {})
  assert(message_privmsg.bits == 0)
  assert(message_privmsg.client_nonce == "")
  assert(message_privmsg.color == "")
  assert(message_privmsg.display_name == "")
  assert(message_privmsg.emotes == {})
  assert(message_privmsg.message_id == "")
  assert(message_privmsg.flags == "")
  assert(message_privmsg.mod == None)
  assert(message_privmsg.reply_parent_display_name is None)
  assert(message_privmsg.reply_parent_message_body is None)
  assert(message_privmsg.reply_parent_message_id == "b34ccfc7-4977-403a-8a94-33c6bac34fb8")
  assert(message_privmsg.reply_parent_user_id is None)
  assert(message_privmsg.reply_parent_user_login is None)
  assert(message_privmsg.room_id == -1)
  assert(message_privmsg.subscriber == None)
  assert(message_privmsg.tmi_sent_timestamp == None)
  assert(message_privmsg.turbo == None)
  assert(message_privmsg.user_id == -1)
  assert(message_privmsg.user_type == "")
  assert(message_privmsg.user == "ronni")
  assert(message_privmsg.channel == "ronni")
  assert(message_privmsg.message == "Good idea!")


def test_message_privmsg_reply_to_message_real():
  message = "@badge-info=subscriber/43;badges=broadcaster/1,subscriber/0,premium/1;" \
  "client-nonce=98e934335aa3ee520760985fd4624a2f;color=#00FF00;display-name=Archimond7450;" \
  "emotes=64138:19-27;flags=;id=b7f4e6da-9097-4844-a2bf-5a7fdaa2c7b1;mod=0;reply-parent-display-name=ArchieMate;" \
  "reply-parent-msg-body=I'm\\shere\\sMrDestructoid;reply-parent-msg-id=8b2b093a-ac9d-4c7e-9871-69a08b7d9e6e;" \
  "reply-parent-user-id=174976810;reply-parent-user-login=archiemate;room-id=147113965;subscriber=1;" \
  "tmi-sent-ts=1625575404359;turbo=0;user-id=147113965;user-type= " \
  ":archimond7450!archimond7450@archimond7450.tmi.twitch.tv PRIVMSG #archimond7450 :@ArchieMate I know SeemsGood"
  regex = TwitchIRC.PrivMsg.match(message)
  assert(regex is not None)
  message_privmsg: TwitchIRC.PrivMsg = TwitchIRC.PrivMsg(regex)
  assert(message_privmsg.badge_info == {"subscriber": 43})
  assert(message_privmsg.badges == {"broadcaster": 1, "subscriber": 0, "premium": 1})
  assert(message_privmsg.bits == 0)
  assert(message_privmsg.client_nonce == "98e934335aa3ee520760985fd4624a2f")
  assert(message_privmsg.color == "#00FF00")
  assert(message_privmsg.display_name == "Archimond7450")
  assert(message_privmsg.emotes == {64138: [(19, 9)]})
  assert(message_privmsg.message_id == "b7f4e6da-9097-4844-a2bf-5a7fdaa2c7b1")
  assert(message_privmsg.flags == "")
  assert(message_privmsg.mod == False)
  assert(message_privmsg.reply_parent_display_name == "ArchieMate")
  assert(message_privmsg.reply_parent_message_body == "I'm here MrDestructoid")
  assert(message_privmsg.reply_parent_message_id == "8b2b093a-ac9d-4c7e-9871-69a08b7d9e6e")
  assert(message_privmsg.reply_parent_user_id == 174976810)
  assert(message_privmsg.reply_parent_user_login == "archiemate")
  assert(message_privmsg.room_id == 147113965)
  assert(message_privmsg.subscriber == True)
  assert(message_privmsg.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1625575404359 // 1000).replace(microsecond=1625575404359 % (1000 * 1000))))
  assert(message_privmsg.turbo == False)
  assert(message_privmsg.user_id == 147113965)
  assert(message_privmsg.user_type == "")
  assert(message_privmsg.user == "archimond7450")
  assert(message_privmsg.channel == "archimond7450")
  assert(message_privmsg.message == "@ArchieMate I know SeemsGood")


def test_message_join():
  message = ":discord_for_streamers!discord_for_streamers@discord_for_streamers.tmi.twitch.tv JOIN #archimond7450"
  regex = TwitchIRC.Join.match(message)
  assert(regex is not None)
  message_join: TwitchIRC.Join = TwitchIRC.Join(regex)
  assert(message_join.user == "discord_for_streamers")
  assert(message_join.channel == "archimond7450")


def test_message_part():
  message = ":anotherttvviewer!anotherttvviewer@anotherttvviewer.tmi.twitch.tv PART #archimond7450"
  regex = TwitchIRC.Part.match(message)
  assert(regex is not None)
  message_part: TwitchIRC.Part = TwitchIRC.Part(regex)
  assert(message_part.user == "anotherttvviewer")
  assert(message_part.channel == "archimond7450")
  

def test_message_capability_acknowledge():
  message = ":tmi.twitch.tv CAP * ACK :twitch.tv/membership twitch.tv/tags twitch.tv/commands"
  regex = TwitchIRC.CapabilityAcknowledge.match(message)
  assert(regex is not None)
  message_capability_acknowledge: TwitchIRC.CapabilityAcknowledge = TwitchIRC.CapabilityAcknowledge(regex)
  assert(message_capability_acknowledge.capabilities == ["twitch.tv/membership", "twitch.tv/tags", "twitch.tv/commands"])


def test_message_host_target_start():
  message = ":tmi.twitch.tv HOSTTARGET #archimond7450 :deathknlght22 0"
  regex = TwitchIRC.HostTarget.match(message)
  assert(regex is not None)
  message_host_target: TwitchIRC.HostTarget = TwitchIRC.HostTarget(regex)
  assert(message_host_target.channel == "archimond7450")
  assert(message_host_target.hosted_channel == "deathknlght22")
  assert(message_host_target.viewers == 0)


def test_message_host_target_end():
  message = ":tmi.twitch.tv HOSTTARGET #archimond7450 :wtii -"
  regex = TwitchIRC.HostTarget.match(message)
  assert(regex is not None)
  message_host_target: TwitchIRC.HostTarget = TwitchIRC.HostTarget(regex)
  assert(message_host_target.channel == "archimond7450")
  assert(message_host_target.hosted_channel == "wtii")
  assert(message_host_target.viewers is None)


def test_message_notice_commands_host_start():
  message = "@msg-id=host_on :tmi.twitch.tv NOTICE #archimond7450 :Now hosting Back2Warcraft."
  regex = TwitchIRC.NoticeCommands.match(message)
  assert(regex is not None)
  message_notice: TwitchIRC.NoticeCommands = TwitchIRC.NoticeCommands(regex)
  assert(message_notice.message_id == TwitchIRC.NoticeMessageId.HostOn)
  assert(message_notice.channel == "archimond7450")
  assert(message_notice.message == "Now hosting Back2Warcraft.")


def test_message_notice_commands_host_target_went_offline():
  message = "@msg-id=host_target_went_offline :tmi.twitch.tv NOTICE #archimond7450 :deathknlght22 has gone offline. Exiting host mode."
  regex = TwitchIRC.NoticeCommands.match(message)
  assert(regex is not None)
  message_notice: TwitchIRC.NoticeCommands = TwitchIRC.NoticeCommands(regex)
  assert(message_notice.message_id == TwitchIRC.NoticeMessageId.HostTargetWentOffline)
  assert(message_notice.channel == "archimond7450")
  assert(message_notice.message == "deathknlght22 has gone offline. Exiting host mode.")


def test_message_reconnect():
  message = "RECONNECT"
  regex = TwitchIRC.Reconnect.match(message)
  assert(regex is not None)
  message_reconnect: TwitchIRC.Reconnect = TwitchIRC.Reconnect(regex)
  assert(isinstance(message_reconnect, TwitchIRC.Reconnect))


def test_message_clear_chat_clear():
  message = "@room-id=147113965;tmi-sent-ts=1625583668766 :tmi.twitch.tv CLEARCHAT #archimond7450"
  regex = TwitchIRC.ClearChat.match(message)
  assert(regex is not None)
  message_clear_chat: TwitchIRC.ClearChat = TwitchIRC.ClearChat(regex)
  assert(message_clear_chat.ban_duration is None)
  assert(message_clear_chat.room_id == 147113965)
  assert(message_clear_chat.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1625583668766 // 1000).replace(microsecond=1625583668766 % (1000 * 1000))))
  assert(message_clear_chat.channel == "archimond7450")
  assert(message_clear_chat.user is None)


def test_message_clear_chat_timeout():
  pass
  """message = ""
  regex = TwitchIRC.ClearChat.match(message)
  assert(regex is not None)
  message_clear_chat: TwitchIRC.ClearChat = TwitchIRC.ClearChat(regex)
  assert(message_clear_chat.ban_duration is None)
  assert(message_clear_chat.room_id == 147113965)
  assert(message_clear_chat.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1625583668766 // 1000).replace(microsecond=1625583668766 % (1000 * 1000))))
  assert(message_clear_chat.channel == "archimond7450")
  assert(message_clear_chat.user is None)"""


def test_message_clear_chat_ban():
  pass
  """message = ""
  regex = TwitchIRC.ClearChat.match(message)
  assert(regex is not None)
  message_clear_chat: TwitchIRC.ClearChat = TwitchIRC.ClearChat(regex)
  assert(message_clear_chat.ban_duration is None)
  assert(message_clear_chat.room_id == 147113965)
  assert(message_clear_chat.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1625583668766 // 1000).replace(microsecond=1625583668766 % (1000 * 1000))))
  assert(message_clear_chat.channel == "archimond7450")
  assert(message_clear_chat.user is None)"""


def test_message_clear_message():
  message = "@login=ronni;target-msg-id=abc-123-def :tmi.twitch.tv CLEARMSG #dallas :HeyGuys"
  regex = TwitchIRC.ClearMessage.match(message)
  assert(regex is not None)
  message_clear_message: TwitchIRC.ClearMessage = TwitchIRC.ClearMessage(regex)
  assert(message_clear_message.user == "ronni")
  assert(message_clear_message.target_message_id == "abc-123-def")
  assert(message_clear_message.channel == "dallas")
  assert(message_clear_message.message == "HeyGuys")


def test_message_global_user_state():
  message = "@badge-info=subscriber/8;badges=subscriber/6;color=#0D4200;display-name=dallas;" \
  "emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;turbo=0;user-id=1337;user-type=admin :tmi.twitch.tv GLOBALUSERSTATE"
  regex = TwitchIRC.GlobalUserState.match(message)
  assert(regex is not None)
  message_global_user_state: TwitchIRC.GlobalUserState = TwitchIRC.GlobalUserState(regex)
  assert(message_global_user_state.badge_info == {"subscriber": 8})
  assert(message_global_user_state.badges == {"subscriber": 6})
  assert(message_global_user_state.color == "#0D4200")
  assert(message_global_user_state.display_name == "dallas")
  assert(message_global_user_state.emote_sets == [0, 33, 50, 237, 793, 2126, 3517, 4578, 5569, 9400, 10337, 12239])
  assert(message_global_user_state.turbo == 0)
  assert(message_global_user_state.user_id == 1337)
  assert(message_global_user_state.user_type == "admin")


def test_message_room_state_join_in_channel():
  message = "@emote-only=0;followers-only=0;r9k=0;slow=0;subs-only=0 :tmi.twitch.tv ROOMSTATE #dallas"
  regex = TwitchIRC.RoomState.match(message)
  assert(regex is not None)
  message_room_state: TwitchIRC.RoomState = TwitchIRC.RoomState(regex)
  assert(message_room_state.emote_only == 0)
  assert(message_room_state.followers_only == 0)
  assert(message_room_state.r9k == 0)
  assert(message_room_state.slow == 0)
  assert(message_room_state.subs_only == 0)
  assert(message_room_state.channel == "dallas")


def test_message_room_state_slow_mode_is_set():
  message = "@slow=10 :tmi.twitch.tv ROOMSTATE #dallas"
  regex = TwitchIRC.RoomState.match(message)
  assert(regex is not None)
  message_room_state: TwitchIRC.RoomState = TwitchIRC.RoomState(regex)
  assert(message_room_state.emote_only is None)
  assert(message_room_state.followers_only is None)
  assert(message_room_state.r9k is None)
  assert(message_room_state.slow == 10)
  assert(message_room_state.subs_only is None)
  assert(message_room_state.channel == "dallas")


def test_message_user_notice_sub():
  message = "@badge-info=;badges=staff/1,broadcaster/1,turbo/1;color=#008000;display-name=ronni;" \
  "emotes=;id=db25007f-7a18-43eb-9379-80131e44d633;login=ronni;mod=0;msg-id=sub;msg-param-cumulative-months=1;" \
  "msg-param-streak-months=0;msg-param-should-share-streak=0;msg-param-sub-plan=Prime;" \
  "msg-param-sub-plan-name=Prime;room-id=1337;subscriber=1;system-msg=ronni\\shas\\ssubscribed\\sfor\\sthe\\sfirst\\smonth!;" \
  "tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=staff :tmi.twitch.tv USERNOTICE #dallas :Great stream -- keep it up!"
  regex = TwitchIRC.UserNotice.match(message)
  assert(regex is not None)
  boolean: bool = TwitchIRC.UserNoticeSubscription.match(regex)
  assert(boolean == True)
  message_user_notice: TwitchIRC.UserNoticeSubscription = TwitchIRC.UserNoticeSubscription(regex)
  assert(message_user_notice.badge_info == {})
  assert(message_user_notice.badges == {"staff": 1, "broadcaster": 1, "turbo": 1})
  assert(message_user_notice.color == "#008000")
  assert(message_user_notice.display_name == "ronni")
  assert(message_user_notice.emotes == {})
  assert(message_user_notice.flags == "")
  assert(message_user_notice.message_id == "db25007f-7a18-43eb-9379-80131e44d633")
  assert(message_user_notice.user == "ronni")
  assert(message_user_notice.mod == False)
  assert(message_user_notice.cumulative_months == 1)
  assert(message_user_notice.streak_months == 0)
  assert(message_user_notice.should_share_streak == False)
  assert(message_user_notice.sub_plan == TwitchIRC.SubPlan.Prime)
  assert(message_user_notice.sub_plan_name == "Prime")
  assert(message_user_notice.room_id == 1337)
  assert(message_user_notice.subscriber == True)
  assert(message_user_notice.system_message == "ronni has subscribed for the first month!")
  assert(message_user_notice.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1507246572675 // 1000).replace(microsecond=1507246572675 % (1000 * 1000))))
  assert(message_user_notice.turbo == True)
  assert(message_user_notice.user_id == 1337)
  assert(message_user_notice.user_type == "staff")
  assert(message_user_notice.channel == "dallas")
  assert(message_user_notice.message == "Great stream -- keep it up!")


def test_message_user_notice_resub():
  message = "@badge-info=;badges=staff/1,broadcaster/1,turbo/1;color=#008000;display-name=ronni;" \
  "emotes=;id=db25007f-7a18-43eb-9379-80131e44d633;login=ronni;mod=0;msg-id=resub;msg-param-cumulative-months=6;" \
  "msg-param-streak-months=2;msg-param-should-share-streak=1;msg-param-sub-plan=Prime;" \
  "msg-param-sub-plan-name=Prime;room-id=1337;subscriber=1;system-msg=ronni\\shas\\ssubscribed\\sfor\\s6\\smonths!;" \
  "tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=staff :tmi.twitch.tv USERNOTICE #dallas :Great stream -- keep it up!"
  regex = TwitchIRC.UserNotice.match(message)
  assert(regex is not None)
  boolean: bool = TwitchIRC.UserNoticeResubscription.match(regex)
  assert(boolean == True)
  message_user_notice: TwitchIRC.UserNoticeResubscription = TwitchIRC.UserNoticeResubscription(regex)
  assert(message_user_notice.badge_info == {})
  assert(message_user_notice.badges == {"staff": 1, "broadcaster": 1, "turbo": 1})
  assert(message_user_notice.color == "#008000")
  assert(message_user_notice.display_name == "ronni")
  assert(message_user_notice.emotes == {})
  assert(message_user_notice.flags == "")
  assert(message_user_notice.message_id == "db25007f-7a18-43eb-9379-80131e44d633")
  assert(message_user_notice.user == "ronni")
  assert(message_user_notice.mod == False)
  assert(message_user_notice.cumulative_months == 6)
  assert(message_user_notice.streak_months == 2)
  assert(message_user_notice.should_share_streak == True)
  assert(message_user_notice.sub_plan == TwitchIRC.SubPlan.Prime)
  assert(message_user_notice.sub_plan_name == "Prime")
  assert(message_user_notice.room_id == 1337)
  assert(message_user_notice.subscriber == True)
  assert(message_user_notice.system_message == "ronni has subscribed for 6 months!")
  assert(message_user_notice.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1507246572675 // 1000).replace(microsecond=1507246572675 % (1000 * 1000))))
  assert(message_user_notice.turbo == True)
  assert(message_user_notice.user_id == 1337)
  assert(message_user_notice.user_type == "staff")
  assert(message_user_notice.channel == "dallas")
  assert(message_user_notice.message == "Great stream -- keep it up!")


def test_message_user_notice_gift_sub():
  message = "@badge-info=;badges=staff/1,premium/1;color=#0000FF;display-name=TWW2;emotes=;id=e9176cd8-5e22-4684-ad40-ce53c2561c5e;" \
  "login=tww2;mod=0;msg-id=subgift;msg-param-months=1;msg-param-recipient-display-name=Mr_Woodchuck;msg-param-recipient-id=89614178;" \
  "msg-param-recipient-name=mr_woodchuck;msg-param-sub-plan-name=House\\sof\\sNyoro~n;msg-param-sub-plan=1000;room-id=19571752;subscriber=0;" \
  "system-msg=TWW2\\sgifted\\sa\\sTier\\s1\\ssub\\sto\\sMr_Woodchuck!;tmi-sent-ts=1521159445153;turbo=0;user-id=13405587;" \
  "user-type=staff :tmi.twitch.tv USERNOTICE #forstycup"
  regex = TwitchIRC.UserNotice.match(message)
  assert(regex is not None)
  boolean: bool = TwitchIRC.UserNoticeSubscriptionGift.match(regex)
  assert(boolean == True)
  message_user_notice: TwitchIRC.UserNoticeSubscriptionGift = TwitchIRC.UserNoticeSubscriptionGift(regex)
  assert(message_user_notice.badge_info == {})
  assert(message_user_notice.badges == {"staff": 1, "premium": 1})
  assert(message_user_notice.color == "#0000FF")
  assert(message_user_notice.display_name == "TWW2")
  assert(message_user_notice.emotes == {})
  assert(message_user_notice.flags == "")
  assert(message_user_notice.message_id == "e9176cd8-5e22-4684-ad40-ce53c2561c5e")
  assert(message_user_notice.user == "tww2")
  assert(message_user_notice.mod == False)
  assert(message_user_notice.months == 1)
  assert(message_user_notice.recipient_display_name == "Mr_Woodchuck")
  assert(message_user_notice.recipient_id == 89614178)
  assert(message_user_notice.recipient_name == "mr_woodchuck")
  assert(message_user_notice.sub_plan == TwitchIRC.SubPlan.Tier1)
  assert(message_user_notice.sub_plan_name == "House of Nyoro~n")
  assert(message_user_notice.room_id == 19571752)
  assert(message_user_notice.subscriber == False)
  assert(message_user_notice.system_message == "TWW2 gifted a Tier 1 sub to Mr_Woodchuck!")
  assert(message_user_notice.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1521159445153 // 1000).replace(microsecond=1521159445153 % (1000 * 1000))))
  assert(message_user_notice.turbo == False)
  assert(message_user_notice.user_id == 13405587)
  assert(message_user_notice.user_type == "staff")
  assert(message_user_notice.channel == "forstycup")
  assert(message_user_notice.message is None)


### TODO: NEED TO CHECK ALL GIFT SUBS IS msg-param-recipient-user-name OR msg-param-recipient-name FOR ALL OR IF IT'S DIFFERENT FOR EACH ###
def test_message_user_notice_anon_gift_sub():
  message = "@badge-info=;badges=broadcaster/1,subscriber/6;color=;display-name=qa_subs_partner;emotes=;flags=;" \
  "id=b1818e3c-0005-490f-ad0a-804957ddd760;login=qa_subs_partner;mod=0;msg-id=anonsubgift;msg-param-months=3;" \
  "msg-param-recipient-display-name=TenureCalculator;msg-param-recipient-id=135054130;msg-param-recipient-user-name=tenurecalculator;" \
  "msg-param-sub-plan-name=t111;msg-param-sub-plan=1000;room-id=196450059;subscriber=1;" \
  "system-msg=An\\sanonymous\\suser\\sgifted\\sa\\sTier\\s1\\ssub\\sto\\sTenureCalculator!\\s;tmi-sent-ts=1542063432068;turbo=0;user-id=196450059;" \
  "user-type= :tmi.twitch.tv USERNOTICE #qa_subs_partner"
  regex = TwitchIRC.UserNotice.match(message)
  assert(regex is not None)
  boolean: bool = TwitchIRC.UserNoticeAnonymousSubscriptionGift.match(regex)
  assert(boolean == True)
  message_user_notice: TwitchIRC.UserNoticeAnonymousSubscriptionGift = TwitchIRC.UserNoticeAnonymousSubscriptionGift(regex)
  assert(message_user_notice.badge_info == {})
  assert(message_user_notice.badges == {"broadcaster": 1, "subscriber": 6})
  assert(message_user_notice.color == "")
  assert(message_user_notice.display_name == "qa_subs_partner")
  assert(message_user_notice.emotes == {})
  assert(message_user_notice.flags == "")
  assert(message_user_notice.message_id == "b1818e3c-0005-490f-ad0a-804957ddd760")
  assert(message_user_notice.user == "qa_subs_partner")
  assert(message_user_notice.mod == False)
  assert(message_user_notice.months == 3)
  assert(message_user_notice.recipient_display_name == "TenureCalculator")
  assert(message_user_notice.recipient_id == 135054130)
  assert(message_user_notice.recipient_name == "tenurecalculator")
  assert(message_user_notice.sub_plan == TwitchIRC.SubPlan.Tier1)
  assert(message_user_notice.sub_plan_name == "t111")
  assert(message_user_notice.room_id == 196450059)
  assert(message_user_notice.subscriber == True)
  assert(message_user_notice.system_message == "An anonymous user gifted a Tier 1 sub to TenureCalculator! ")
  assert(message_user_notice.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1542063432068 // 1000).replace(microsecond=1542063432068 % (1000 * 1000))))
  assert(message_user_notice.turbo == False)
  assert(message_user_notice.user_id == 196450059)
  assert(message_user_notice.user_type == "")
  assert(message_user_notice.channel == "qa_subs_partner")
  assert(message_user_notice.message is None)


### NO TEST FOR USER NOTICE SUBSCRIPTION MYSTERY GIFT AS THERE IS NO INFO ABOUT THIS USER NOTICE IN TWITCH DOCS ###


### TEST FOR USER NOTICE (ANONYMOUS) GIFT PAID UPGRADE WILL BE CREATED WHEN THE BOT RECEIVES THIS LEGIT USER NOTICE ###


### TEST FOR USER NOTICE REWARD GIFT WILL BE CREATED WHEN THE BOT RECEIVES THIS LEGIT USER NOTICE ###


def test_user_notice_raid():
  message = "@badge-info=;badges=turbo/1;color=#9ACD32;display-name=TestChannel;emotes=;id=3d830f12-795c-447d-af3c-ea05e40fbddb;login=testchannel;" \
  "mod=0;msg-id=raid;msg-param-displayName=TestChannel;msg-param-login=testchannel;msg-param-viewerCount=15;room-id=56379257;subscriber=0;" \
  "system-msg=15\\sraiders\\sfrom\\sTestChannel\\shave\\sjoined\\n!;tmi-sent-ts=1507246572675;tmi-sent-ts=1507246572675;turbo=1;user-id=123456;" \
  "user-type= :tmi.twitch.tv USERNOTICE #othertestchannel"
  regex = TwitchIRC.UserNotice.match(message)
  assert(regex is not None)
  boolean: bool = TwitchIRC.UserNoticeRaid.match(regex)
  assert(boolean == True)
  message_user_notice: TwitchIRC.UserNoticeRaid = TwitchIRC.UserNoticeRaid(regex)
  assert(message_user_notice.badge_info == {})
  assert(message_user_notice.badges == {"turbo": 1})
  assert(message_user_notice.color == "#9ACD32")
  assert(message_user_notice.display_name == "TestChannel")
  assert(message_user_notice.emotes == {})
  assert(message_user_notice.flags == "")
  assert(message_user_notice.message_id == "3d830f12-795c-447d-af3c-ea05e40fbddb")
  assert(message_user_notice.user == "testchannel")
  assert(message_user_notice.mod == False)
  assert(message_user_notice.raider_display_name == "TestChannel")
  assert(message_user_notice.login == "testchannel")
  assert(message_user_notice.viewer_count == 15)
  assert(message_user_notice.room_id == 56379257)
  assert(message_user_notice.subscriber == False)
  assert(message_user_notice.system_message == "15 raiders from TestChannel have joined!")
  assert(message_user_notice.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1507246572675 // 1000).replace(microsecond=1507246572675 % (1000 * 1000))))
  assert(message_user_notice.turbo == True)
  assert(message_user_notice.user_id == 123456)
  assert(message_user_notice.user_type == "")
  assert(message_user_notice.channel == "othertestchannel")
  assert(message_user_notice.message is None)


### NO TEST FOR USER NOTICE UNRAID AS THERE IS NO INFO ABOUT THIS USER NOTICE IN TWITCH DOCS ###


def test_user_notice_ritual():
  message = "@badge-info=;badges=;color=;display-name=SevenTest1;emotes=30259:0-6;id=37feed0f-b9c7-4c3a-b475-21c6c6d21c3d;login=seventest1;mod=0;" \
  "msg-id=ritual;msg-param-ritual-name=new_chatter;room-id=6316121;subscriber=0;system-msg=Seventoes\\sis\\snew\\shere!;tmi-sent-ts=1508363903826;" \
  "turbo=0;user-id=131260580;user-type= :tmi.twitch.tv USERNOTICE #seventoes :HeyGuys"
  regex = TwitchIRC.UserNotice.match(message)
  assert(regex is not None)
  boolean: bool = TwitchIRC.UserNoticeRitual.match(regex)
  assert(boolean == True)
  message_user_notice: TwitchIRC.UserNoticeRitual = TwitchIRC.UserNoticeRitual(regex)
  assert(message_user_notice.badge_info == {})
  assert(message_user_notice.badges == {})
  assert(message_user_notice.color == "")
  assert(message_user_notice.display_name == "SevenTest1")
  assert(message_user_notice.emotes == {30259: [(0, 7)]})
  assert(message_user_notice.flags == "")
  assert(message_user_notice.message_id == "37feed0f-b9c7-4c3a-b475-21c6c6d21c3d")
  assert(message_user_notice.user == "seventest1")
  assert(message_user_notice.mod == False)
  assert(message_user_notice.ritual_name == "new_chatter")
  assert(message_user_notice.room_id == 6316121)
  assert(message_user_notice.subscriber == False)
  assert(message_user_notice.system_message == "Seventoes is new here!")
  assert(message_user_notice.tmi_sent_timestamp == (datetime.datetime.utcfromtimestamp(1508363903826 // 1000).replace(microsecond=1508363903826 % (1000 * 1000))))
  assert(message_user_notice.turbo == False)
  assert(message_user_notice.user_id == 131260580)
  assert(message_user_notice.user_type == "")
  assert(message_user_notice.channel == "seventoes")
  assert(message_user_notice.message == "HeyGuys")


### TEST FOR USER NOTICE BITS BADGE TIER WILL BE CREATED WHEN THE BOT RECEIVES THIS LEGIT USER NOTICE ###


def test_user_state():
  message = "@badge-info=;badges=staff/1;color=#0D4200;display-name=ronni;emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;mod=1;" \
  "subscriber=1;turbo=1;user-type=staff :tmi.twitch.tv USERSTATE #dallas"
  regex = TwitchIRC.UserState.match(message)
  assert(regex is not None)
  message_user_state: TwitchIRC.UserState = TwitchIRC.UserState(regex)
  assert(message_user_state.badge_info == {})
  assert(message_user_state.badges == {"staff": 1})
  assert(message_user_state.color == "#0D4200")
  assert(message_user_state.display_name == "ronni")
  assert(message_user_state.emote_sets == [0, 33, 50, 237, 793, 2126, 3517, 4578, 5569, 9400, 10337, 12239])
  assert(message_user_state.mod == True)
  assert(message_user_state.subscriber == True)
  assert(message_user_state.turbo == True)
  assert(message_user_state.user_type == "staff")
  assert(message_user_state.channel == "dallas")


def test_unknown_message():
  message = "Unknown message"
  message_unknown = TwitchIRC.UnknownMessage(message)
  assert(message_unknown.message == message)


### TODO: HERE WILL BE DECODE_MESSAGE TEST ###


def test_send():
  message: str = "This is a test message."
  channel: str = "archimond7450"
  sent_message: str = TwitchIRC.send(channel, message)
  assert(sent_message == f"PRIVMSG #{channel} :{message}")
  
