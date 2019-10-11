#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime:19-8-29 下午8:02
# project: spider

from os import rename
import youtube_dl
import time
import os

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class GetItem(object):

    def rename_hook(self,d):
        # 重命名下载的视频名称
        if d['status'] == 'finished':
            file_name = 'downloads/{}.mp4'.format(int(time.time()))
            rename(d['filename'], file_name)
            print('下载完成{}'.format(file_name))

    @classmethod
    def already_download(cls, video_id):
        return video_id in os.listdir('downloads')

    def download(self, youtube_url):

        # 定义某些下载参数
        ydl_opts = {
            # 也可以填写 best/worst/worstaudio 等等
            'format':'bestaudio/140/m4a/worstaudio',   #'bestaudio/140/m4a/,best',  # 136/137/mp4/bestvideo,140/m4a/bestaudio
            # 'progress_hooks': [self.rename_hook],
            # 格式化下载后的文件名，避免默认文件名太长无法保存
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            # 打印日志
            'logger': MyLogger(),
            'proxy': 'socks5://127.0.0.1:1080',
            'extract-audio': True,
            'audio-format': 'mp3',
            'audio-quality': 0,
            'keepvideo': False,
            'fragment_retries':10,
            'retries':9,
            'abort-on-unavailable-fragment':True,
            '--verbose':True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            result = ydl.download([youtube_url])






# if __name__ == '__main__':
#     getItem = GetItem()
#     getItem.download('https://www.youtube.com/watch?v=iTEss4qFCzI')
#     # os.system('youtube-dl')
'''
best: Select the best quality format represented by a single file with video and audio.
worst: Select the worst quality format represented by a single file with video and audio.
bestvideo: Select the best quality video-only format (e.g. DASH video). May not be available.
worstvideo: Select the worst quality video-only format. May not be available.
bestaudio: Select the best quality audio only-format. May not be available.
worstaudio: Select the worst quality audio only-format. May not be available.
'''