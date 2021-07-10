import regex as re
from typing import Optional, Dict, List, Optional
import datetime
from enum import Enum

import ArchieMate.Logger as Logger
import ArchieMate.Socket as Socket
import ArchieMate.Poller as Poller

logger = Logger.get_logger(__name__)
irc_logger = Logger.get_irc_logger(__name__)


def parse_tags(tags: Optional[str]) -> Dict[str, str]:
  if tags is not None and tags.startswith("@"): tags = tags[1:]
  return {} if tags is None or len(tags) == 0 else {one_tag[0]: one_tag[1] for tag in tags.split(";") if (one_tag := tag.split("="))}


def parse_badges(badges: Optional[str]) -> Dict[str, int]:
  return {} if badges is None or len(badges) == 0 else {one_badge[0]: int(one_badge[1]) for badge in badges.split(",") if (one_badge := badge.split("/"))}


def parse_badge_info(badge_info: Optional[str]) -> Dict[str, int]:
  return {} if badge_info is None or len(badge_info) == 0 else {one_badge_info[0]: int(one_badge_info[1]) for badge_info_unsplitted in badge_info.split(",") if (one_badge_info := badge_info_unsplitted.split("/"))}


def escape_irc_string(string: Optional[str]) -> str:
  result = ""
  test = False
  if string is not None:
    for character in string:
      if not test:
        if character == "\\":
          test = True
        else:
          result += character
      else:
        if character == ":":
          result += ";"
        elif character == "s":
          result += " "
        elif character == "\\":
          result += "\\"
        elif character in "rn":
          pass
        else:
          result += character
        test = False
  return result


def escape_irc(irc_text: Optional[str]) -> str:
  return "" if irc_text is None or len(irc_text) == 0 else escape_irc_string(irc_text)


def parse_emote_range(emote_range: Optional[str]) -> List[tuple[int, int]]:
  return [] if emote_range is None or len(emote_range) == 0 else [(int(one_range[0]), int(one_range[1]) - int(one_range[0]) + 1) for rng in emote_range.split(",") if (one_range := rng.split("-"))]


def parse_emotes(emotes: Optional[str]) -> Dict[int, List[tuple[int, int]]]:
  return {} if emotes is None or len(emotes) == 0 else {int(one_emote[0]): parse_emote_range(one_emote[1]) for emote in emotes.split("/") if (one_emote := emote.split(":"))}


def parse_emote_sets(emote_sets: Optional[str]) -> List[int]:
  return [] if emote_sets is None or len(emote_sets) == 0 else [int(emote_set) for emote_set in emote_sets.split(",")]


class NoticeMessageId(Enum):
  AlreadyBanned = "already_banned"
  AlreadyEmoteOnlyOff = "already_emote_only_off"
  AlreadyEmoteOnlyOn = "already_emote_only_on"
  AlreadyR9KOff = "already_r9k_off"
  AlreadyR9KOn = "already_r9k_on"
  AlreadySubsOff = "already_subs_off"
  AlreadySubsOn = "already_subs_on"
  BadBanAdmin = "bad_ban_admin"
  BadBanAnon = "bad_ban_anon"
  BadBanBroadcaster = "bad_ban_broadcaster"
  BadBanGlobalMod = "bad_ban_global_mod"
  BadBanMod = "bad_ban_mod"
  BadBanSelf = "bad_ban_self"
  BadBanStaff = "bad_ban_staff"
  BadCommercialError = "bad_commercial_error"
  BadDeleteMessageBroadcaster = "bad_delete_message_broadcaster"
  BadDeleteMessageMod = "bad_delete_message_mod"
  BadHostError = "bad_host_error"
  BadHostHosting = "bad_host_hosting"
  BadHostRateExceeded = "bad_host_rate_exceeded"
  BadHostRejected = "bad_host_rejected"
  BadHostSelf = "bad_host_self"
  BadMarkerClient = "bad_marker_client"
  BadModBanned = "bad_mod_banned"
  BadModMod = "bad_mod_mod"
  BadSlowDuration = "bad_slow_duration"
  BadTimeoutAdmin = "bad_timeout_admin"
  BadTimeoutAnon = "bad_timeout_anon"
  BadTimeoutBroadcaster = "bad_timeout_broadcaster"
  BadTimeoutDuration = "bad_timeout_duration"
  BadTimeoutGlobalMod = "bad_timeout_global_mod"
  BadTimeoutMod = "bad_timeout_mod"
  BadTimeoutSelf = "bad_timeout_self"
  BadTimeoutStaff = "bad_timeout_staff"
  BadUnbanNoBan = "bad_unban_no_ban"
  BadUnhostError = "bad_unhost_error"
  BadUnmodMod = "bad_unmod_mod"
  BanSuccess = "ban_success"
  CommandsAvailable = "cmds_available"
  ColorChange = "color_change"
  CommercialSuccess = "commercial_success"
  DeleteMessageSuccess = "delete_message_success"
  EmoteOnlyOff = "emote_only_off"
  EmoteOnlyOn = "emote_only_on"
  FollowersOff = "followers_off"
  FollowersOn = "followers_on"
  FollowersOnZero = "followers_onzero"
  HostOff = "host_off"
  HostOn = "host_on"
  HostSuccess = "host_success"
  HostSuccessViewers = "host_success_viewers"
  HostTargetWentOffline = "host_target_went_offline"
  HostsRemaining = "hosts_remaining"
  InvalidUser = "invalid_user"
  ModSuccess = "mod_success"
  MessageBanned = "msg_banned"
  MessageBadCharacters = "msg_bad_characters"
  MessageChannelBlocked = "msg_channel_blocked"
  MessageChannelSuspended = "msg_channel_suspended"
  MessageDuplicate = "msg_duplicate"
  MessageEmoteOnly = "msg_emoteonly"
  MessageFacebook = "msg_facebook"
  MessageFollowersOnly = "msg_followersonly"
  MessageFollowersOnlyFollowed = "msg_followersonly_followed"
  MessageR9K = "msg_r9k"
  MessageRateLimit = "msg_ratelimit"
  MessageRejected = "msg_rejected"
  MessageRejectedMandatory = "message_rejected_mandatory"
  MessageRoomNotFound = "message_room_not_found"
  MessageSlowMode = "message_slowmode"
  MessageSubsOnly = "message_subsonly"
  MessageSuspended = "msg_suspended"
  MessageTimedOut = "msg_timedout"
  MessageVerifiedEmail = "msg_verified_email"
  NoHelp = "no_help"
  NoMods = "no_mods"
  NotHosting = "not_hosting"
  NoPermission = "no_permission"
  R9KOff = "r9k_off"
  R9KOn = "r9k_on"
  RaidErrorAlreadyRaiding = "raid_error_already_raiding"
  RaidErrorForbidden = "raid_error_forbidden"
  RaidErrorSelf = "raid_error_self"
  RaidErrorTooManyViewers = "raid_error_too_many_viewers"
  RaidErrorUnexpected = "raid_error_unexpected"
  RaidNoticeMature = "raid_notice_mature"
  RaidNoticeRestrictedChat = "raid_notice_restricted_chat"
  RoomMods = "room_mods"
  SlowOff = "slow_off"
  SlowOn = "slow_on"
  SubsOff = "subs_off"
  SubsOn = "subs_on"
  TimeoutNoTimeout = "timeout_no_timeout"
  TimeoutSuccess = "timeout_success"
  TosBan = "tos_ban"
  TurboOnlyColor = "turbo_only_color"
  UnbanSuccess = "unban_success"
  UnmodSuccess = "unmod_success"
  UnraidErrorNoActiveRaid = "unraid_error_no_active_raid"
  UnraidErrorUnexpected = "unraid_error_unexpected"
  UnraidSuccess = "unraid_success"
  UnrecognizedCommand = "unrecognized_cmd"
  UnsupportedChatroomsCommand = "unsupported_chatrooms_cmd"
  UntimeoutBanned = "untimeout_banned"
  UntimeoutSuccess = "untimeout_success"
  UsageBan = "usage_ban"
  UsageClear = "usage_clear"
  UsageColor = "usage_color"
  UsageCommercial = "usage_commercial"
  UsageDisconnect = "usage_disconnect"
  UsageEmoteOnlyOff = "usage_emote_only_off"
  UsageEmoteOnlyOn = "usage_emote_only_on"
  UsageFollowersOff = "usage_followers_off"
  UsageFollowersOn = "usage_followers_on"
  UsageHelp = "usage_help"
  UsageHost = "usage_host"
  UsageMarker = "usage_marker"
  UsageMe = "usage_me"
  UsageMod = "usage_mod"
  UsageMods = "usage_mods"
  UsageR9KOff = "usage_r9k_off"
  UsageR9KOn = "usage_r9k_on"
  UsageRaid = "usage_raid"
  UsageSlowOff = "usage_slow_off"
  UsageSlowOn = "usage_slow_on"
  UsageSubsOff = "usage_subs_off"
  UsageSubsOn = "usage_subs_on"
  UsageTimeout = "usage_timeout"
  UsageUnban = "usage_unban"
  UsageUnhost = "usage_unhost"
  UsageUnmod = "usage_unmod"
  UsageUnraid = "usage_unraid"
  UsageUntimeout = "usage_untimeout"
  WhisperBanned = "whisper_banned"
  WhisperBannedRecipients = "whisper_banned_recipient"
  WhisperInvalidArguments = "whisper_invalid_args"
  WhisperInvalidLogin = "whisper_invalid_login"
  WhisperInvalidSelf = "whisper_invalid_self"
  WhisperLimitPerMinute = "whisper_limit_per_min"
  WhisperLimitPerSecond = "whisper_limit_per_sec"
  WhisperRestricted = "whisper_restricted"
  WhisperRestrictedRecipient = "whisper_restricted_recipient"


class Message:
  def __init__(self):
    pass

  def __repr__(self) -> str:
    return f"{type(self).__name__}: {self.__dict__}"

  def __str__(self) -> str:
    return self.__repr__()


class Notice(Message):
  regex = re.compile(r":tmi\.twitch\.tv\sNOTICE\s\*\s:(?P<message>.*)")
  
  @staticmethod
  def match(message: str):
    return Notice.regex.match(message)
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"Notice.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.message = group_dict["message"]
    
    logger.debug(f"Result: {self.__dict__}")


class Generic(Message):
  regex = re.compile(r":tmi\.twitch\.tv\s(?P<message_number>\d{3})\s(?P<bot_user>\S+)\s:(?P<message>.*)")
  
  @staticmethod
  def match(message: str):
    regex = Generic.regex.match(message)
    logger.debug(f"Generic.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"Generic.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.message_number: int = int(group_dict["message_number"])
    self.bot_user: str = group_dict["bot_user"]
    self.message: str = group_dict["message"]
    
    logger.debug(f"Result: {self.__dict__}")


class Ping(Message):
  regex = re.compile(r"^PING\s:(?P<server>.*)$")
  
  @staticmethod
  def match(message: str):
    regex = Ping.regex.match(message)
    logger.debug(f"Ping.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"Ping.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.server: str = group_dict["server"]
    
    logger.debug(f"Result: {self.__dict__}")


class PrivMsg(Message):
  regex = re.compile(r"^@(?P<tags>\S+=\S*;?)\s:(?P<user>\S+)!\S+@\S+\.tmi\.twitch\.tv\sPRIVMSG\s#(?P<channel>\S+)\s:(?P<message>.*)$")

  @staticmethod
  def match(message):
    regex = PrivMsg.regex.match(message)
    logger.debug(f"PrivMsg.match(message: '{message}') -> {regex}")
    return regex

  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"PrivMsg.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.badge_info: Dict[str, int] = parse_badge_info(tags.get("badge-info", ""))
    self.badges: Dict[str, int] = parse_badges(tags.get("badges", ""))
    self.bits: int = int(tags.get("bits", "0"))
    self.client_nonce: str = tags.get("client-nonce", "")
    self.color: str = tags.get("color", "")
    self.display_name: str = escape_irc(tags.get("display-name", ""))
    self.emotes: Dict[int, List[tuple[int, int]]] = parse_emotes(tags.get("emotes", ""))
    self.flags: str = tags.get("flags", "")
    self.message_id: str = tags.get("id", "")
    self.mod: Optional[bool] = tags.get("mod", "-1") == "1" if tags.get("mod", "-1") != "-1" else None
    self.reply_parent_message_id: Optional[str] = tags.get("reply-parent-msg-id", None)
    self.reply_parent_user_id: Optional[int] = int(tags.get("reply-parent-user-id", -1)) if tags.get("reply-parent-user-id", "-1") != "-1" else None
    self.reply_parent_user_login: Optional[str] = tags.get("reply-parent-user-login", None)
    self.reply_parent_display_name: Optional[str] = tags.get("reply-parent-display-name", None)
    self.reply_parent_message_body: Optional[str] = escape_irc(tags.get("reply-parent-msg-body", None)) if tags.get("reply-parent-msg-body", None) is not None else None
    self.room_id: int = int(tags.get("room-id", "-1"))
    self.subscriber: Optional[bool] = tags.get("subscriber", "-1") == "1" if tags.get("subscriber", "-1") != "-1" else None
    tmi_sent_ts: int = int(tags.get("tmi-sent-ts", "0"))
    self.tmi_sent_timestamp: Optional[datetime.datetime] = datetime.datetime.utcfromtimestamp(tmi_sent_ts // 1000).replace(microsecond=tmi_sent_ts % (1000 * 1000)) if tmi_sent_ts > 0 else None
    self.turbo: Optional[bool] = tags.get("turbo", "-1") == "1" if tags.get("turbo", "-1") != "-1" else None
    self.user_id: int = int(tags.get("user-id", "-1"))
    self.user: str = group_dict["user"]
    self.user_type: str = tags.get("user-type", "")
    self.channel: str = group_dict["channel"]
    self.message: str = group_dict["message"]
    logger.debug(f"Result: {self.__dict__}")


class Join(Message):
  regex = re.compile(r"^:(?P<user>\S+)!(?P<user_1>\S+)@(?P<user_2>\S+)\.tmi\.twitch\.tv\sJOIN\s#(?P<channel>\S+)$")
  
  @staticmethod
  def match(message: str):
    regex = Join.regex.match(message)
    logger.debug(f"Join.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"Join.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.user: str = group_dict["user"]
    self.channel: str = group_dict["channel"]


class Part(Message):
  regex = re.compile(r"^:(?P<user>\S+)!(?P<user_1>\S+)@(?P<user_2>\S+)\.tmi\.twitch\.tv\sPART\s#(?P<channel>\S+)$")
  
  @staticmethod
  def match(message: str):
    regex = Part.regex.match(message)
    logger.debug(f"Part.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"Part.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.user: str = group_dict["user"]
    self.channel: str = group_dict["channel"]


class CapabilityAcknowledge(Message):
  regex = re.compile(r"^:tmi\.twitch\.tv\sCAP\s\*\sACK\s:(?P<capabilities>.*)$")
  
  @staticmethod
  def match(message: str):
    regex = CapabilityAcknowledge.regex.match(message)
    logger.debug(f"CapabilityAcknowledge.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"CapabilityAcknowledge.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.capabilities: List[str] = group_dict["capabilities"].split()


class HostTarget(Message):
  regex = re.compile(r"^:tmi\.twitch\.tv\sHOSTTARGET\s#(?P<channel>\S+)\s:(?P<hosted_channel>\S+)( (?P<viewers>\S+))?$")
  
  @staticmethod
  def match(message: str):
    regex = HostTarget.regex.match(message)
    logger.debug(f"HostTarget.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"HostTarget.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    self.channel: str = group_dict["channel"]
    self.hosted_channel: str = group_dict["hosted_channel"] if group_dict["hosted_channel"] != "-" else ""
    self.viewers: Optional[int] = int(group_dict["viewers"]) if group_dict["viewers"] not in ("-", "", None) else None


class NoticeCommands(Message):
  regex = re.compile(r"^@(?P<tags>\S+=\S*;?)\s:tmi\.twitch\.tv\sNOTICE\s#(?P<channel>\S+)\s:(?P<message>.*)$")
  
  @staticmethod
  def match(message: str):
    regex = NoticeCommands.regex.match(message)
    logger.debug(f"NoticeCommands.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"NoticeCommands.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.message_id: NoticeMessageId = NoticeMessageId(tags["msg-id"])
    self.channel: str = group_dict["channel"]
    self.message: str = group_dict["message"]


class Reconnect(Message):
  regex = re.compile(r"^RECONNECT$")
  
  @staticmethod
  def match(message: str):
    regex = Reconnect.regex.match(message)
    logger.debug(f"Reconnect.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    logger.debug(f"Reconnect.__init__(regex: {regex})")
    Message.__init__(self)


class ClearChat(Message):
  regex = re.compile(r"^@(?P<tags>\S+=\S*;?)\s:tmi\.twitch\.tv\sCLEARCHAT\s#(?P<channel>\S+)(\s:(?P<user>\S+))?$")
  
  @staticmethod
  def match(message: str):
    regex = ClearChat.regex.match(message)
    logger.debug(f"ClearChat.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"ClearChat.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.ban_duration: Optional[str] = tags.get("ban-duration", None)
    self.room_id: int = int(tags.get("room-id", -1)) if tags.get("room-id") != -1 else None
    tmi_sent_ts: int = int(tags.get("tmi-sent-ts", "0"))
    self.tmi_sent_timestamp: Optional[datetime.datetime] = datetime.datetime.utcfromtimestamp(tmi_sent_ts // 1000).replace(microsecond=tmi_sent_ts % (1000 * 1000)) if tmi_sent_ts > 0 else None
    self.channel: str = group_dict["channel"]
    self.user: Optional[str] = group_dict.get("user", None)


class ClearMessage(Message):
  regex = re.compile(r"^@(?P<tags>\S+=\S*;?)\s:tmi\.twitch\.tv\sCLEARMSG\s#(?P<channel>\S+)\s:(?P<message>.*)$")
  
  @staticmethod
  def match(message: str):
    regex = ClearMessage.regex.match(message)
    logger.debug(f"ClearMessage.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"ClearMessage.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.user: str = tags.get("login", "")
    self.target_message_id: str = tags.get("target-msg-id", "")
    self.channel: str = group_dict["channel"]
    self.message: str = group_dict["message"]


class GlobalUserState(Message):
  regex = re.compile(r"^@(?P<tags>\S+=\S*;?)\s:tmi\.twitch\.tv\sGLOBALUSERSTATE$")
  
  @staticmethod
  def match(message: str):
    regex = GlobalUserState.regex.match(message)
    logger.debug(f"GlobalUserState.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"Global.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.badge_info: Dict[str, int] = parse_badge_info(tags.get("badge-info", ""))
    self.badges: Dict[str, int] = parse_badges(tags.get("badges", ""))
    self.color: str = tags.get("color", "")
    self.display_name: str = tags.get("display-name", "")
    self.emote_sets: List[int] = parse_emote_sets(tags.get("emote-sets", ""))
    self.turbo: Optional[bool] = tags.get("turbo", "-1") == "1" if tags.get("turbo", "-1") != "-1" else None
    self.user_id: int = int(tags.get("user-id", "-1"))
    self.user_type: str = tags.get("user-type", "")


class RoomState(Message):
  regex = re.compile(r"^@(?P<tags>\S+=\S*;?)\s:tmi\.twitch\.tv\sROOMSTATE\s#(?P<channel>\S+)$")
  
  @staticmethod
  def match(message: str):
    regex = RoomState.regex.match(message)
    logger.debug(f"RoomState.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"RoomState.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.emote_only: Optional[bool] = tags.get("emote-only", "-1") == "1" if tags.get("emote-only", "-1") != "-1" else None
    self.followers_only: Optional[bool] = tags.get("followers-only", "-1") == "1" if tags.get("followers-only", "-1") != "-1" else None
    self.r9k: Optional[bool] = tags.get("r9k", "-1") == "1" if tags.get("r9k", "-1") != "-1" else None
    self.slow: Optional[int] = int(tags.get("slow", "-1")) if tags.get("slow", "-1") != "-1" else None
    self.subs_only: Optional[bool] = tags.get("subs-only", "-1") == "1" if tags.get("subs-only", "-1") != "-1" else None
    self.channel: str = group_dict["channel"]


class UserNotice(Message):
  regex = re.compile(r"^@(?P<tags>\S+=\S*;?)\s:tmi\.twitch\.tv\sUSERNOTICE\s#(?P<channel>\S+)(\s:(?P<message>.*))?$")
  
  @staticmethod
  def match(message: str):
    regex = UserNotice.regex.match(message)
    logger.debug(f"UserNotice.match(message: '{message}') -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNotice.__init__(regex: '{regex}')")
    Message.__init__(self)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.badge_info: Dict[str, int] = parse_badge_info(tags.get("badge-info", ""))
    self.badges: Dict[str, int] = parse_badges(tags.get("badges", ""))
    self.color: str = tags.get("color", "")
    self.display_name: str = escape_irc(tags.get("display-name", ""))
    self.emotes: Dict[int, List[tuple[int, int]]] = parse_emotes(tags.get("emotes", ""))
    self.flags: str = tags.get("flags", "")
    self.message_id: str = tags.get("id", "")
    self.user: str = tags.get("login", "")
    self.message: str = group_dict.get("message", "")
    self.mod: Optional[bool] = tags.get("mod", "-1") == "1" if tags.get("mod", "-1") != "-1" else None
    self.room_id: int = int(tags.get("room-id", "-1"))
    self.subscriber: Optional[bool] = tags.get("subscriber", "-1") == "1" if tags.get("subscriber", "-1") != "-1" else None
    self.system_message: str = escape_irc(tags.get("system-msg", ""))
    tmi_sent_ts: int = int(tags.get("tmi-sent-ts", "0"))
    self.tmi_sent_timestamp: Optional[datetime.datetime] = datetime.datetime.utcfromtimestamp(tmi_sent_ts // 1000).replace(microsecond=tmi_sent_ts % (1000 * 1000))
    self.turbo: Optional[bool] = tags.get("turbo", "-1") == "1" if tags.get("turbo", "-1") != "-1" else None
    self.user_id: int = int(tags.get("user-id", "-1"))
    self.user_type: str = tags.get("user-type", "")
    self.channel: str = group_dict["channel"]


class SubPlan(Enum):
  Prime = "Prime"
  Tier1 = "1000"
  Tier2 = "2000"
  Tier3 = "3000"

class UserNoticeSubscription(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "sub"
    logger.debug(f"UserNoticeSubscription.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeSubscription.__init__(regex: {group_dict})")
    UserNotice.__init__(self, regex)
    
    tags = parse_tags(group_dict["tags"])
    self.cumulative_months: int = int(tags.get("msg-param-cumulative-months", "0"))
    self.should_share_streak: bool = tags.get("msg-param-should-share-streak", "0") == "1"
    self.streak_months: int = int(tags.get("msg-param-streak-months", "0"))
    self.sub_plan: SubPlan = SubPlan(tags.get("msg-param-sub-plan", "1000"))
    self.sub_plan_name: str = escape_irc(tags.get("msg-param-sub-plan-name", ""))


class UserNoticeResubscription(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "resub"
    logger.debug(f"UserNoticeResubscription.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeResubscription.__init__(regex: {group_dict})")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.cumulative_months: int = int(tags.get("msg-param-cumulative-months", "1"))
    self.should_share_streak: bool = tags.get("msg-param-should-share-streak", "0") == "1"
    self.streak_months: int = int(tags.get("msg-param-streak-months", "0"))
    self.sub_plan: SubPlan = SubPlan(tags.get("msg-param-sub-plan", "1000"))
    self.sub_plan_name: str = escape_irc(tags.get("msg-param-sub-plan-name", ""))


class UserNoticeSubscriptionGift(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str ]= parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "subgift"
    logger.debug(f"UserNoticeSubscriptionGift.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeSubscriptionGift.__init__(regex: {group_dict})")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.months: int = int(tags.get("msg-param-months", "1"))
    self.recipient_display_name: str = tags["msg-param-recipient-display-name"]
    self.recipient_id: int = int(tags["msg-param-recipient-id"])
    self.recipient_name: str = tags["msg-param-recipient-name"]
    self.sub_plan: SubPlan = SubPlan(tags.get("msg-param-sub-plan", "1000"))
    self.sub_plan_name: str = escape_irc(tags.get("msg-param-sub-plan-name", ""))
    self.gift_months: int = int(tags.get("msg-param-gift-months", "1"))


class UserNoticeAnonymousSubscriptionGift(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "anonsubgift"
    logger.debug(f"UserNoticeAnonymousSubscriptionGift.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeAnonymousSubscriptionGift.__init__(regex: {group_dict})")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.months: int = int(tags.get("msg-param-months", "1"))
    self.recipient_display_name: str = tags["msg-param-recipient-display-name"]
    self.recipient_id: int = int(tags["msg-param-recipient-id"])
    self.recipient_name: str = tags["msg-param-recipient-name"]
    self.sub_plan: SubPlan = SubPlan(tags.get("msg-param-sub-plan", "1000"))
    self.sub_plan_name: str = escape_irc(tags.get("msg-param-sub-plan-name", ""))
    self.gift_months: int = int(tags.get("msg-param-gift-months", "1"))


class UserNoticeSubscriptionMysteryGift(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "submysterygift"
    logger.debug(f"UserNoticeSubscriptionMysteryGift.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeSubscriptionMysteryGift.__init__(regex: {group_dict}")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])


class UserNoticeGiftPaidUpgrade(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "giftpaidupgrade"
    logger.debug(f"UserNoticeGiftPaidUpgrade.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeGiftPaidUpgrade.__init__(regex: {group_dict}")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.promo_gift_total: int = int(tags["msg-param-promo-gift-total"])
    self.promo_name: str = escape_irc(tags["msg-param-promo-name"])
    self.sender_login: str = tags["msg-param-sender-login"]
    self.sender_display_name: str = tags["msg-param-sender-name"]


class UserNoticeAnonymousGiftPaidUpgrade(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "giftpaidupgrade"
    logger.debug(f"UserNoticeAnonymousGiftPaidUpgrade.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeAnonymousGiftPaidUpgrade.__init__(regex: {group_dict}")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.promo_gift_total: int = int(tags["msg-param-promo-gift-total"])
    self.promo_name: str = escape_irc(tags["msg-param-promo-name"])


class UserNoticeRewardGift(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "rewardgift"
    logger.debug(f"UserNoticeRewardGift.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeRewardGift.__init__(regex: {group_dict}")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])


class UserNoticeRaid(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "raid"
    logger.debug(f"UserNoticeRaid.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeRaid.__init__(regex: {group_dict}")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.raider_display_name: str = tags["msg-param-displayName"]
    self.login: str = tags["msg-param-login"]
    self.viewer_count: int = int(tags.get("msg-param-viewerCount", "0"))
    

class UserNoticeUnraid(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "unraid"
    logger.debug(f"UserNoticeUnraid.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeUnraid.__init__(regex: {group_dict}")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    


class UserNoticeRitual(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "ritual"
    logger.debug(f"UserNoticeRitual.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeRitual.__init__(regex: {group_dict}")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.ritual_name: str = tags["msg-param-ritual-name"]


class UserNoticeBitsBadgeTier(UserNotice):
  @staticmethod
  def match(regex) -> bool:
    group_dict = regex.groupdict()
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    result: bool = tags["msg-id"] == "bitsbadgetier"
    logger.debug(f"UserNoticeBitsBadgeTier.match(group_dict: {group_dict}) -> {result}")
    return result
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserNoticeBitsBadgeTier.__init__(regex: {group_dict}")
    UserNotice.__init__(self, regex)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    threshold: int = int(group_dict["msg-param-threshold"])


class UserState(Message):
  regex = re.compile(r"^@(?P<tags>\S+=\S*;?)\s:tmi\.twitch\.tv\sUSERSTATE\s#(?P<channel>\S+)$")
  
  @staticmethod
  def match(message: str):
    regex = UserState.regex.match(message)
    logger.debug(f"UserState.match(message: {message}) -> {regex}")
    return regex
  
  def __init__(self, regex):
    group_dict = regex.groupdict()
    
    logger.debug(f"UserState.__init__(regex: {group_dict})")
    Message.__init__(self)
    
    tags: Dict[str, str] = parse_tags(group_dict["tags"])
    self.badge_info: Dict[str, int] = parse_badge_info(tags.get("badge-info", ""))
    self.badges: Dict[str, int] = parse_badges(tags.get("badges", ""))
    self.color: str = tags.get("color", "")
    self.display_name: str = tags.get("display-name", "")
    self.emote_sets: List[int] = parse_emote_sets(tags.get("emote-sets", ""))
    self.mod: Optional[bool] = tags.get("mod", "-1") == "1" if tags.get("mod", "-1") != "-1" else None
    self.subscriber: Optional[bool] = tags.get("subscriber", "-1") == "1" if tags.get("subscriber", "-1") != "-1" else None
    self.turbo: Optional[bool] = tags.get("turbo", "-1") == "1" if tags.get("turbo", "-1") != "-1" else None
    self.user_type: str = tags.get("user-type", "")
    self.channel: str = group_dict["channel"]


class UnknownMessage(Message):
  def __init__(self, message: str):
    logger.debug(f"UnknownMessage.__init__(message: '{message}')")
    Message.__init__(self)
    self.message: str = message
    logger.debug(f"Result: {self.__dict__}")


def decode_message(message: str) -> Message:
  result: Optional[Message] = None
  
  for message_class in (
    PrivMsg, Join, Part, UserState, UserNotice, GlobalUserState, RoomState,
    NoticeCommands, Ping, ClearChat, ClearMessage, HostTarget, Reconnect, Notice, Generic, CapabilityAcknowledge
  ):
    if regex := message_class.match(message):
      if message_class == UserNotice:
        for user_notice_type in (
          UserNoticeSubscription, UserNoticeResubscription, UserNoticeSubscriptionGift, UserNoticeAnonymousSubscriptionGift,
          UserNoticeRaid, UserNoticeUnraid, UserNoticeRitual, UserNoticeBitsBadgeTier,
          UserNoticeSubscriptionMysteryGift, UserNoticeGiftPaidUpgrade, UserNoticeAnonymousGiftPaidUpgrade, UserNoticeRewardGift
        ):
          if user_notice_type.match(regex):
            result = user_notice_type(regex)
            break
      else:
        result = message_class(regex)
      break
  
  if result is None:
    result = UnknownMessage(message)
  
  irc_logger.debug(f"Received: '{message}'")
  irc_logger.debug(f"Result: {result}")
  
  return result

def send(channel: str, message: str) -> str:
  logger.debug(f"send(message: '{message}')")
  ret: str = f"PRIVMSG #{channel} :{message}"
  logger.debug(f"Result: '{ret}'")
  return ret

twitch_irc_address: str = "irc.chat.twitch.tv"
twitch_irc_port: int = 6667


class IRC:
  def __init__(self, bot_name: str, channel: str, oauth: str, poller: Poller.Poller):
    logger.debug(f"IRC.__init__(bot_name: '{bot_name}', channel: '{channel}', oauth: '{oauth}')")
    self.channel: str = channel
    self.socket: Socket.Socket = Socket.Socket(twitch_irc_address, twitch_irc_port, poller)
    self.socket.send(f"PASS oauth:{oauth}")
    self.socket.send(f"NICK {bot_name}")
    self.socket.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
    self.socket.send(f"JOIN #{channel}")
    
    if not(
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 1, "Welcome, GLHF!") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 2, "Your host is tmi.twitch.tv") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 3, "This server is rather new") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 4, "-") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 375, "-") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 372, "You are in a maze of twisty passages, all alike.") and
      checkGenericMessage(decode_message(self.socket.recv_nowait()), 376, ">")
    ):
      logger.error("Authentication failed!")
      raise ValueError("Authentication failed!")
  
  def __del__(self):
    logger.debug("IRC.__del__()")
    self.flush()
  
  def send_message(self, message):
    logger.debug(f"IRC.send_message(message: '{message}')")
    self.socket.send(f"PRIVMSG #{self.channel} :{message}")
  
  def send_pong(self, server):
    logger.debug(f"IRC.send_pong(server: '{server}')")
    self.socket.send(f"PONG :{server}")
  
  def recv(self) -> str:
    ret: str = self.socket.recv()
    logger.debug(f"IRC.recv() -> '{ret}'")
    return ret
  
  def flush(self):
    logger.debug("IRC.flush()")
    self.socket.flush()


def checkGenericMessage(message: Message, message_number: int, generic_message: str) -> bool:
  logger.debug(f"checkGenericMessage(message: {message}, message_number: {message_number}, generic_message: '{generic_message})")
  ret: bool = True
  is_generic_message: bool = False
  is_right_generic_message: bool = False
  if is_generic_message := isinstance(message, Generic):
    generic: Generic = message
    is_right_generic_message = generic.message_number == message_number and generic.message == generic_message
    ret = is_right_generic_message
  else:
    ret = False
  
  logger.debug(f"is_generic_message: {is_generic_message}, is_right_generic_message: {is_right_generic_message} => Result: {ret}")
  return ret
