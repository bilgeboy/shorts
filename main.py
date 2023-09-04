import logging
from making_movie import combine_assets, combine_multiple_video_assets, concat_videos
from services.eleven_labs import get_audio_bytes
from services.pexels import search_videos, VideoOrientation, get_video_bytes
import requests

from utils.months import months
from utils.today_in_history_consts import historical_events


def main():
    user_pick = input("pick option:\n"
                      "1. make all year videos\n"
                      "2. make all month videos\n"
                      "3. make the video of today\n"
                      "4. make a video by selecting month and a day\n"
                      "5. (1-3 is not yet deploy. later auto publishing to youtube shorts will be available)\n")

    if user_pick == '':
        # put here the func that you want to test for shortcut
        # combine_multiple_video_assets(historical_events[months[9]][0], '', '', False)
        concat_videos(historical_events[months[9]][3])
        return

    if int(user_pick) == 4:
        month, day = month_day_selection()
        make_video(month, day)


def make_video(month, day):
    logging.info('make_movie:: started')
    prompt = historical_events[months[month]][day]

    combine_multiple_assets = input("combine multiple assets?\nenter y/n:\t")
    if combine_multiple_assets == 'y':
        use_downloaded_content = input("use downloaded content?\nenter y/n:\t")
        if use_downloaded_content == 'y':
            combine_multiple_video_assets(prompt)
            return
        else:
            audio_b = get_audio_bytes(prompt["text"])
            video_b = get_video_bytes(prompt["key_words"][0])
            combine_multiple_video_assets(prompt, audio_b, video_b)
            return

    use_downloaded_content = input("use downloaded content?\nenter y/n:\t")
    logging.info('make_movie:: got all assets')
    if use_downloaded_content == 'y':
        combine_assets()
        return
    else:
        audio_b = get_audio_bytes(prompt["text"])
        video_b = get_video_bytes(prompt["key_words"][0])
        combine_assets(prompt, audio_b, video_b)
        return


def month_day_selection():
    month = input("enter month (1 - 12):\n")
    day = input("enter day:\n")
    return int(month), int(day)


# pip freeze > requirements.txt


if __name__ == "__main__":
    main()
