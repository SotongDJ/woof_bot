#!/usr/bin/env python3
import argparse, datetime, random, time
import pytz
import json
from mastodon import Mastodon

parser = argparse.ArgumentParser(description="run Crontime")
parser.add_argument("env", help="Environment config", type=str)
args = parser.parse_args()

class chatbot:
    def __init__(self,env_path):
        env_json = json.load(open(env_path))
        self.host = Mastodon(
            access_token = env_json["host"]["token"],
            api_base_url = env_json["host"]["domain"]
        )
        print("Run: __init__()")
    def push(self,now_time,prefix=""):
        time_str = now_time.strftime("%Y-%m-%d %H:%M:%S %z")
        hour_int = int(now_time.strftime("%H"))
        run_hour_int = hour_int
        print(f"Bot.push({time_str})")

        small_msg = "woof~"
        large_msg = "WOOF!!!!!! WOOF!!!!!!\n"
        if hour_int == 0:
            woof_msg = F"[12AM midnight]\n"
        elif hour_int == 12:
            run_hour_int = run_hour_int - 12
            woof_msg = F"[12PM noon]\n{large_msg}"
        elif hour_int > 12:
            run_hour_int = hour_int - 12
            woof_msg = F"[{run_hour_int}PM]\n{large_msg}"
        else:
            woof_msg = F"[{hour_int}AM]\n"
        while run_hour_int > 0:
            run_hour_int = run_hour_int - 4
            if run_hour_int > 0:
                woof_msg = woof_msg + small_msg * 4 + "\n"
            else:
                woof_msg = woof_msg + small_msg * (4 + run_hour_int)
        the_day_str = now_time.strftime("%Y-%m-%d")
        random.seed(the_day_str)
        magic_int = random.choice(range(8,23))

        ear_list = [
            "V{}V",
            "▼{}▼",
            "U{}U",
            "◖{}◗",
            "(◖{})",
            "(V{})",
            "(▼{})",
            "(U{})",
            "({}V)",
            "({}▼)",
            "({}U)",
            "({}◗)"
        ]
        face_list = [
            " ʘ ᴥ ʘ ",
            " ● ᴥ ● ",
            " ・ᴥ・ ",
            " ´ ꓃ ` ",
            " ^ ｪ ^ ",
            "´• ﻌ •`",
            " ^ ᴥ ^ ",
            " - ᴥ - ",
            " ⁰ ᴥ ⁰ ",
            " ❍ ᴥ ❍ ",
            " ⚆ ᴥ ⚆ ",
            " ◕ ᴥ ◕ ",
            " ・ ᴥ ・ ",
            ]
        random.seed(the_day_str)
        ear_str = random.choice(ear_list)
        face_str = random.choice(face_list)
        emoji_msg = ear_str.format(face_str)

        print(F"Hour number: {hour_int}")
        print(F"Magic number: {magic_int}")
        print(F"Woof msg: {woof_msg}")
        print(F"Emoji msg: {emoji_msg}")
        if hour_int == 0:
            self.host.status_post(prefix+woof_msg+F"\nMagic number: {magic_int}", visibility="public", spoiler_text="Magic are finding their way today! Woof!")
        elif hour_int == magic_int:
            self.host.status_post(prefix+woof_msg, visibility="public", spoiler_text=emoji_msg)
        else:
            self.host.status_post(prefix+woof_msg, visibility="public")
        time.sleep(1)

Bot = chatbot(args.env)
run = True
while run:
    now_time = datetime.datetime.now(pytz.timezone('Asia/Singapore'))
    time_str = now_time.strftime("%Y-%m-%d %H:%M:%S %z")
    min_int = int(now_time.strftime("%M"))
    if min_int == 0:
        print(time_str)
        Bot.push(now_time)
        run = False
    elif min_int < 50:
        print(time_str)
        Bot.push(now_time,prefix="> #DELAYED <\n")
        run = False
    elif min_int >= 50 and min_int < 58:
        print(f"[{time_str}] Countdown 60s")
        time.sleep(60)
    else:
        print(f"[{time_str}] Countdown 5s")
        time.sleep(5)
