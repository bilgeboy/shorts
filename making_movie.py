import logging

from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

from services.pexels import get_video_bytes
from services.whisper_open_ai import speech_to_text
from io import BytesIO


def save_file(file_bytes: bytes, file_format: str, file_name: str = ''):
    with open(f'./output/{file_name}output.{file_format}', 'wb') as f:
        f.write(file_bytes)


def text_clip(text: str, duration: int, start_time: int = 0):
    return (TextClip(text, font="Rubik", fontsize=60, color='white', bg_color='rgba(0, 0, 0, 0.4)', method='caption')
            .set_position('center')
            .set_duration(duration)
            .set_start(start_time))


def combine_assets(prompt='', audio_b: bytes = '', video_b: bytes = ''):
    logging.info('combine_assets:: started')
    if prompt != '' or audio_b != '' or video_b != '':
        save_file(video_b, 'mp4')
        save_file(audio_b, 'mp3')

    audio_clip = AudioFileClip('./output/output.mp3')
    video_clip = VideoFileClip('./output/output.mp4')

    audio_from_vid = video_clip.audio
    # TODO: think about passing the volumex parameter as an argument
    if audio_from_vid is not None:
        audio_concat = CompositeAudioClip([audio_from_vid.fx(volumex, 0.1), audio_clip])
        video_clip.audio = audio_concat
    else:
        video_clip.audio = audio_clip

    transcription = speech_to_text('./output/output.mp3')

    text_clips = []
    for segment in transcription['segments']:
        duration = segment['end'] - segment['start']
        txt_clip = text_clip(segment['text'], duration, segment['start'])
        text_clips.append(txt_clip)

    result = CompositeVideoClip([video_clip, *text_clips]).subclip(0, audio_clip.duration)

    # Export the final video with the new audio
    output_path = "./output/output_video_with_audio.mp4"
    result.write_videofile(output_path, codec="libx264")


def combine_multiple_video_assets(prompt='', audio_b: bytes = '', video_b: bytes = '', skip_save = True):
    logging.info('combine_assets:: started')
    if (prompt != '' or audio_b != '' or video_b != '') and skip_save is True:
        save_file(video_b, 'mp4')
        save_file(audio_b, 'mp3')

    audio_clip = AudioFileClip('./output/output.mp3')
    video_clip = VideoFileClip('./output/output.mp4')

    transcription = speech_to_text('./output/output.mp3')

    text_clips = []
    no_use_again_list = [prompt["key_words"][0]]
    list_of_videos = []
    video_cnt = 0
    only_once = True
    for segment in transcription['segments']:
        next_segment = False
        duration = segment['end'] - segment['start']
        txt_clip = text_clip(segment['text'], duration, segment['start'])
        text_clips.append(txt_clip)

        for index, value in enumerate(prompt['key_words']):
            if next_segment is True:
                break
            words_in_value = value.split()
            for word in words_in_value:
                if word in segment['text'] and prompt['key_words'][index] not in no_use_again_list:
                    no_use_again_list.append(prompt['key_words'][index])
                    video_b = get_video_bytes(prompt["key_words"][index])
                    if video_b == None:
                        continue
                    video_cnt += 1
                    save_file(video_b, 'mp4', f'{video_cnt}_')
                    video_b = VideoFileClip(f'./output/{video_cnt}_output.mp4').subclip(0, duration)
                    list_of_videos.append(video_b)
                    break
                elif prompt['key_words'][index] in no_use_again_list and only_once is True:
                    only_once = False
                    video_clip = video_clip.subclip(0, duration)
                    list_of_videos.append(video_clip)

    concat_videos = concatenate_videoclips(list_of_videos)
    # TODO: add gifs and emojis and watermarks
    result = CompositeVideoClip([concat_videos, *text_clips]).set_audio(audio_clip).subclip(0, audio_clip.duration)

    # Export the final video with the new audio
    output_path = "./output/output_video_with_audio.mp4"
    result.write_videofile(output_path, codec="libx264")


def concat_videos(prompt):
    video_concat = []

    vid1 = get_video_bytes(prompt["key_words"][0])
    save_file(vid1, 'mp4', 'temp2_')
    vid1 = VideoFileClip('./output/temp2_output.mp4')

    video_concat.append(vid1)

    vid1 = get_video_bytes(prompt["key_words"][2])
    save_file(vid1, 'mp4', 'temp1_')
    vid1 = VideoFileClip('./output/temp1_output.mp4')

    video_concat.append(vid1)

    final_video = concatenate_videoclips(video_concat)

    emoji = ImageClip('./assets/watermark_no_bg.png')
    emoji_position = (10, 10)

    video_with_emoji = CompositeVideoClip([final_video.set_position("center"), emoji.set_position(emoji_position)]).subclip(0, final_video.duration)

    output_path = "./output/output_video_with_audio.mp4"
    video_with_emoji.write_videofile(output_path, codec="libx264")
