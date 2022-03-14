import os
from click import progressbar
from pytube import *
from moviepy.editor import *
import threading
import time
# import ffmpeg
# import subprocess

downloadSetting = "mp4"  # downloading type
getSetting = {
    "mp3": "best",  # quality of dowloading flie
    "mp4": "best",
    "pmp3": "best",
    "webm": "best"
}
downloadList = []
coadd = True


def addVideo(playlist, ind):
    try:
        vid = YouTube(playlist.video_urls[ind])
        downloadList.append(vid)
        print("{} 를 다운로드 목록에 추가했습니다.".format(vid.streams[0].title))
    except Exception as error:
        print(error)
        print("해당 영상을 찾지 못했습니다.")


def downloadVideo(vid, ind):
    try:
        print("{} 영상을 다운로드 하는 중..".format(vid.title))
        if downloadSetting == "mp4":
            vids = vid.streams.filter(
                progressive=True, file_extension="mp4").order_by("resolution")  # gets mp4 sources and order by resolution
        elif downloadSetting == "mp3" or downloadSetting == "pmp3":
            vids = vid.streams.filter(
                only_audio=True, file_extension="mp4").order_by("abr")  # gets sound sources and order by abr(sound quality)
        elif downloadSetting == "webm":
            vids = vid.streams.filter(
                only_audio=True, file_extension="webm").order_by("abr")
        if len(vids) >= 1:
            # download finest quality
            foundVid = None
            if getSetting[downloadSetting] == "best":
                foundVid = vids[-1]
                vids[-1].download(".\\files")
            else:
                for vid in vids:
                    if downloadSetting == "mp4":
                        if vid.res == getSetting[downloadSetting]:
                            foundVid = vid
                    elif downloadSetting == "mp3":
                        if vid.abr == getSetting[downloadSetting]:
                            foundVid = vid
                    if foundVid != None:
                        vid.download(".\\files")
                        break
            if foundVid != None:
                vidFullName = foundVid.default_filename
                vidName, vidExt = os.path.splitext(vidFullName)
                if downloadSetting == "pmp3":  # convert mp4 to mp3
                    print(os.path.exists(os.path.join(os.path.abspath(
                        ".\\files"), vidFullName)))
                    print(os.path.join(os.path.abspath(
                        ".\\files"), vidName) + ".mp3")
                    # vidAudio = ffmpeg.input(os.path.join(
                    #     os.path.abspath(".\\files"), vidFullName))
                    # print("input done")
                    # audioStream = ffmpeg.output(vidAudio, os.path.join(
                    #     os.path.abspath(".\\files"), vidName) + ".mp3")
                    # print("output done")
                    # ffmpeg.run(audioStream)
                    # print("stream done")

                    # subprocess.run([
                    #     "ffmpeg",
                    #     "-i", os.path.join(os.path.abspath(
                    #         ".\\files"), vidFullName),
                    #     os.path.join(os.path.abspath(
                    #         ".\\files"), vidName) + ".mp3"
                    # ])
                elif downloadSetting == "mp3":
                    vidAudio = AudioFileClip(os.path.join(
                        os.path.abspath(".\\files"), vidFullName))
                    vidAudio.write_audiofile(os.path.join(
                        os.path.abspath(".\\files"), vidName) + ".mp3", logger=None)
                    os.remove(os.path.join(
                        os.path.abspath(".\\files"), vidFullName))
                print("{} 영상을 다운로드 하였습니다. 남은 대기열 {}".format(
                    vid.title, len(downloadList) - ind - 1))
            else:
                print(
                    "{} 영상의 설정된 품질의 영상을 발견할 수 없습니다.".format(vid.title))
        else:
            print(
                "{} 영상의 설정된 품질의 영상을 발견할 수 없습니다.".format(vid.title))
    except Exception as error:
        print(error)
        print("{} 영상을 다운로드 하지 못했습니다.".format(
            vid.title))


print("명령을 입력하세요. 명령 리스트는 help를 참조하세요.")
while True:
    command = input()  # get command
    command = command.split(" ")
    if len(command) == 1:
        if command[0] == "download":
            startTime = time.perf_counter()
            threads = []
            for ind, vid in enumerate(downloadList):
                if coadd == True:
                    t = threading.Thread(target=downloadVideo, args=(vid, ind))
                    t.start()
                    threads.append(t)
                else:
                    downloadVideo(vid, ind)
            for t in threads:
                t.join()
            downloadList = []  # reset download list after download
            print("다운로드를 완료했습니다. 소요시간 {}초.".format(
                time.perf_counter() - startTime))
        elif command[0] == "help":
            print("download\t다운로드 목록을 모두 현재 설정으로 다운로드합니다.")
            print("type <type>\t다운로드할 파일 확장명을 변경합니다.")
            print("add <link>\t해당 링크의 영상을 다운로드 목록에 추가합니다.")
            print("addlist <link>\t해당 링크의 재생목록 영상을 모두 다운로드 목록에 추가합니다.")
            print("setting <type> <to>\t해당 확장자의 설정을 변경합니다.")
            print("co <true|false>\t다중 작업(멀티 태스킹) 여부를 설정합니다.")
    elif len(command) == 2:
        if command[0] == "type":
            if command[1] in getSetting:
                downloadSetting = command[1]
                print("다운로드 타입을 {}로 변경했습니다.".format(command[1]))
            else:
                print("해당 다운로드 타입을 발견하지 못했습니다.")
        elif command[0] == "add":
            try:
                vid = YouTube(command[1])
                downloadList.append(vid)
                print("{} 를 다운로드 목록에 추가했습니다.".format(vid.streams[0].title))
            except:
                print("해당 영상을 찾지 못했습니다.")
        elif command[0] == "addlist":
            startTime = time.perf_counter()
            try:
                playlist = Playlist(command[1])
                print("{}개의 영상을 추가합니다..".format(len(playlist.video_urls)))
                videoCounts = len(playlist.video_urls)
                threads = []
                for count in range(videoCounts):
                    if coadd == True:  # fast add
                        t = threading.Thread(
                            target=addVideo, args=(playlist, count))
                        t.start()
                        threads.append(t)
                    else:
                        addVideo(playlist, count)
                for t in threads:
                    t.join()  # wait until all threads close
                print("재생목록을 모두 추가했습니다. 소요시간 {}초.".format(
                    time.perf_counter() - startTime))
            except Exception as error:
                print(error)
                print("해당 재생목록을 찾지 못했습니다.")
        elif command[0] == "co":
            if command[1] == "true":
                coadd = True
                print("멀티 작업을 활성화 하였습니다.")
            elif command[1] == "false":
                coadd = False
                print("멀티 작업을 비활성화 하였습니다.")
            else:
                print("입력이 잘못되었습니다. true나 false를 사용하세요.")
    elif len(command) == 3:
        if command[0] == "setting":
            if command[1] in getSetting:
                getSetting[command[1]] = command[2]
                print("설정을 적용했습니다.")
            else:
                print("해당 다운로드 타입을 발견하지 못했습니다.")
