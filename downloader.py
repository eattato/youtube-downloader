import os
import pytube
from pytube import YouTube

downloadSetting = "mp4"  # downloading type
getSetting = {
    "mp3": "best",  # quality of dowloading flie
    "mp4": "best"
}
downloadList = []

print("명령을 입력하세요. 명령 리스트는 help를 참조하세요.")
while True:
    command = input()  # get command
    command = command.split(" ")
    if len(command) == 1:
        if command[0] == "download":
            for ind, vid in enumerate(downloadList):
                try:
                    print("{} 영상을 다운로드 하는 중..".format(vid.title))
                    if downloadSetting == "mp4":
                        vids = vid.streams.filter(
                            progressive=True, file_extension="mp4").order_by("resolution")  # gets mp4 sources and order by resolution
                    elif downloadSetting == "mp3":
                        vids = vid.streams.filter(
                            only_audio=True, file_extension="mp4").order_by("abr")  # gets sound sources and order by abr(sound quality)
                    if len(vids) >= 1:
                        # download finest quality
                        foundVid = False
                        if getSetting[downloadSetting] == "best":
                            foundVid = True
                            vids[-1].download(".\\files")
                        else:
                            for vid in vids:
                                if downloadSetting == "mp4":
                                    if vid.res == getSetting[downloadSetting]:
                                        foundVid = True
                                elif downloadSetting == "mp3":
                                    if vid.abr == getSetting[downloadSetting]:
                                        foundVid = True
                                if foundVid == True:
                                    vid.download(".\\files")
                                    break
                        if foundVid == True:
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
            downloadList = []  # reset download list after download
            print("다운로드를 완료했습니다.")
        elif command[0] == "help":
            print("download\t다운로드 목록을 모두 현재 설정으로 다운로드합니다.")
            print("type <type>\t다운로드할 파일 확장명을 변경합니다.")
            print("add <link>\t해당 링크의 영상을 다운로드 목록에 추가합니다.")
            print("setting <type> <to>\t해당 확장자의 설정을 변경합니다.")
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
    elif len(command) == 3:
        if command[0] == "setting":
            if command[1] in getSetting:
                getSetting[command[1]] = command[2]
                print("설정을 적용했습니다.")
            else:
                print("해당 다운로드 타입을 발견하지 못했습니다.")
