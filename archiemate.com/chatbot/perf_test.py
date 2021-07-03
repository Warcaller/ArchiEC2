import time
from ArchieMate.TwitchIRC import Messages
import timeit
import sys
import inspect
import statistics


def timelog(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print(f"{method.__name__} {(te - ts) * 1000}")
        return result
    return timed


def test_decode_message_login_1():
    return Messages.decode_message(":tmi.twitch.tv 001 <user> :Welcome, GLHF!")


def test_decode_message_login_2():
    return Messages.decode_message(":tmi.twitch.tv 002 <user> :Your host is tmi.twitch.tv")


def test_decode_message_login_3():
    return Messages.decode_message(":tmi.twitch.tv 003 <user> :This server is rather new")


def test_decode_message_login_4():
    return Messages.decode_message(":tmi.twitch.tv 004 <user> :-")


def test_decode_message_login_5():
    return Messages.decode_message(":tmi.twitch.tv 375 <user> :-")


def test_decode_message_login_6():
    return Messages.decode_message(":tmi.twitch.tv 372 <user> :You are in a maze of twisty passages.")


def test_decode_message_login_7():
    return Messages.decode_message(":tmi.twitch.tv 376 <user> :>")


def test_decode_message_ping():
    return Messages.decode_message("PING :tmi.twitch.tv")


def test_decode_message_unknown_command():
    return Messages.decode_message(":tmi.twitch.tv 421 <user> WHO :Unknown command")


def test_decode_message_join_1():
    return Messages.decode_message(":<user>!<user>@<user>.tmi.twitch.tv JOIN #<channel>")


def test_decode_message_join_2():
    return Messages.decode_message(":<user>.tmi.twitch.tv 353 <user> = #<channel> :<user>")


def test_decode_message_join_3():
    return Messages.decode_message(":<user>.tmi.twitch.tv 366 <user> #<channel> :End of /NAMES list")


def test_decode_message_acknowledge_membership():
    return Messages.decode_message(":tmi.twitch.tv CAP * ACK :twitch.tv/membership")


def test_decode_message_acknowledge_tags():
    return Messages.decode_message(":tmi.twitch.tv CAP * ACK :twitch.tv/tags")


def test_decode_message_acknowledge_commands():
    return Messages.decode_message(":tmi.twitch.tv CAP * ACK :twitch.tv/commands")


def test_decode_message_join():
    return Messages.decode_message(":ronni!ronni@ronni.tmi.twitch.tv JOIN #dallas")


def test_decode_message_part():
    return Messages.decode_message(":ronni!ronni@ronni.tmi.twitch.tv PART #dallas")


def test_decode_message_perma_ban():
    return Messages.decode_message(":tmi.twitch.tv CLEARCHAT #dallas :ronni")


def test_decode_message_1_min_ban():
    return Messages.decode_message("@ban-duration=60 :tmi.twitch.tv CLEARCHAT #dallas :ronni")


def test_decode_message_clear_chat():
    return Messages.decode_message(":tmi.twitch.tv CLEARCHAT #dallas")


def test_decode_message_clear_msg():
    return Messages.decode_message("@login=ronni;target-msg-id=abc-123-def :tmi.twitch.tv CLEARMSG #dallas :HeyGuys")


def test_decode_message_global_user_state():
    return Messages.decode_message("@badge-info=subscriber/8;badges=subscriber/6;color=#0D4200;display-name=dallas;emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;turbo=0;user-id=1337;user-type=admin :tmi.twitch.tv GLOBALUSERSTATE")


def test_decode_message_non_bits_priv_msg():
    return Messages.decode_message("@badge-info=;badges=global_mod/1,turbo/1;color=#0D4200;display-name=ronni;emotes=25:0-4,12-16/1902:6-10;id=b34ccfc7-4977-403a-8a94-33c6bac34fb8;mod=0;room-id=1337;subscriber=0;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=global_mod :ronni!ronni@ronni.tmi.twitch.tv PRIVMSG #ronni :Kappa Keepo Kappa")


def test_decode_message_bits_priv_msg():
    return Messages.decode_message("@badge-info=;badges=staff/1,bits/1000;bits=100;color=;display-name=ronni;emotes=;id=b34ccfc7-4977-403a-8a94-33c6bac34fb8;mod=0;room-id=1337;subscriber=0;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=staff :ronni!ronni@ronni.tmi.twitch.tv PRIVMSG #ronni :cheer100")


def test_decode_message_room_state_join():
    return Messages.decode_message("@emote-only=0;followers-only=0;r9k=0;slow=0;subs-only=0 :tmi.twitch.tv ROOMSTATE #dallas")


def test_decode_message_slowmode_room_state():
    return Messages.decode_message("@slow=10 :tmi.twitch.tv ROOMSTATE #dallas")


def test_decode_message_resub_user_notice():
    return Messages.decode_message("@badge-info=;badges=staff/1,broadcaster/1,turbo/1;color=#008000;display-name=ronni;emotes=;id=db25007f-7a18-43eb-9379-80131e44d633;login=ronni;mod=0;msg-id=resub;msg-param-cumulative-months=6;msg-param-streak-months=2;msg-param-should-share-streak=1;msg-param-sub-plan=Prime;msg-param-sub-plan-name=Prime;room-id=1337;subscriber=1;system-msg=ronni\\shas\\ssubscribed\\sfor\\s6\\smonths!;tmi-sent-ts=1507246572675;turbo=1;user-id=1337;user-type=staff :tmi.twitch.tv USERNOTICE #dallas :Great stream -- keep it up!")


def test_decode_message_sub_gift_user_notice():
    return Messages.decode_message("@badge-info=;badges=staff/1,premium/1;color=#0000FF;display-name=TWW2;emotes=;id=e9176cd8-5e22-4684-ad40-ce53c2561c5e;login=tww2;mod=0;msg-id=subgift;msg-param-months=1;msg-param-recipient-display-name=Mr_Woodchuck;msg-param-recipient-id=89614178;msg-param-recipient-name=mr_woodchuck;msg-param-sub-plan-name=House\\sof\\sNyoro~n;msg-param-sub-plan=1000;room-id=19571752;subscriber=0;system-msg=TWW2\\sgifted\\sa\\sTier\\s1\\ssub\\sto\\sMr_Woodchuck!;tmi-sent-ts=1521159445153;turbo=0;user-id=13405587;user-type=staff :tmi.twitch.tv USERNOTICE #forstycup")


def test_decode_message_anon_sub_gift_user_notice():
    return Messages.decode_message("@badge-info=;badges=broadcaster/1,subscriber/6;color=;display-name=qa_subs_partner;emotes=;flags=;id=b1818e3c-0005-490f-ad0a-804957ddd760;login=qa_subs_partner;mod=0;msg-id=anonsubgift;msg-param-months=3;msg-param-recipient-display-name=TenureCalculator;msg-param-recipient-id=135054130;msg-param-recipient-user-name=tenurecalculator;msg-param-sub-plan-name=t111;msg-param-sub-plan=1000;room-id=196450059;subscriber=1;system-msg=An\\sanonymous\\suser\\sgifted\\sa\\sTier\\s1\\ssub\\sto\\sTenureCalculator!\\s;tmi-sent-ts=1542063432068;turbo=0;user-id=196450059;user-type= :tmi.twitch.tv USERNOTICE #qa_subs_partner")


def test_decode_message_raid_user_notice():
    return Messages.decode_message("@badge-info=;badges=turbo/1;color=#9ACD32;display-name=TestChannel;emotes=;id=3d830f12-795c-447d-af3c-ea05e40fbddb;login=testchannel;mod=0;msg-id=raid;msg-param-displayName=TestChannel;msg-param-login=testchannel;msg-param-viewerCount=15;room-id=56379257;subscriber=0;system-msg=15\\sraiders\\sfrom\\sTestChannel\\shave\\sjoined\n!;tmi-sent-ts=1507246572675;tmi-sent-ts=1507246572675;turbo=1;user-id=123456;user-type= :tmi.twitch.tv USERNOTICE #othertestchannel")


def test_decode_message_new_chatter_ritual_user_notice():
    return Messages.decode_message("@badge-info=;badges=;color=;display-name=SevenTest1;emotes=30259:0-6;id=37feed0f-b9c7-4c3a-b475-21c6c6d21c3d;login=seventest1;mod=0;msg-id=ritual;msg-param-ritual-name=new_chatter;room-id=6316121;subscriber=0;system-msg=Seventoes\\sis\\snew\\shere!;tmi-sent-ts=1508363903826;turbo=0;user-id=131260580;user-type= :tmi.twitch.tv USERNOTICE #seventoes :HeyGuys")


def test_decode_message_user_state():
    return Messages.decode_message("@badge-info=;badges=staff/1;color=#0D4200;display-name=ronni;emote-sets=0,33,50,237,793,2126,3517,4578,5569,9400,10337,12239;mod=1;subscriber=1;turbo=1;user-type=staff :tmi.twitch.tv USERSTATE #dallas")


def performance_test(function, number: int, repeat: int):
    function_str = function.__name__
    elapsed = timeit.repeat(f"{function_str}()", f"from __main__ import {function_str}", number=number, repeat=repeat)
    elapsed_min = min(elapsed)
    elapsed_median = statistics.median(elapsed)
    elapsed_max = max(elapsed)
    return f'{function_str[5:]:60s}: min - {elapsed_min:.40f}s | median - {elapsed_median:.40f}s | max - {elapsed_max:.40f}s'


def performance_test_suite(test_suite, number_repeat_list):
    print(f"TEST SUITE '{test_suite}'")
    test_functions = [obj for name, obj in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(obj) and name.startswith(f"test_{test_suite}"))]
    for number_repeat in number_repeat_list:
        print("-"*220)
        print(f"Performing {number_repeat[0]} calls {number_repeat[1]} times:")
        for test_function in test_functions:
            print(performance_test(test_function, number=number_repeat[0], repeat=number_repeat[1]))
    print("="*220)


def main():
    performance_test_suite("decode_message", [(1, 10_000_000), (10_000, 1_000)])
    return 0


if __name__=="__main__":
    exit(main())
