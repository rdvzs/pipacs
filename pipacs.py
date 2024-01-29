import time
from tkinter import *
from tkinter import filedialog

from pytube import YouTube
from pytube import Playlist
from pytube.helpers import safe_filename
import threading
import os
#import ffmpeg

#from PIL import Image, ImageTk

BCKGND_COLOR = "white"
YT_RED = "#cc0000"

def url_click(handle):
    if url_text.get() == "Add meg a videó linkjét!":
        url_text.set("")
        url_entry.config(fg="black")

def path_click(handle):
    if path_text.get() == "Nincs megadva!":
        path_text.set("")
        path_entry.config(fg="black")


def saving_path():
    global path
    path = filedialog.askdirectory()

    if path:
        path_text.set(path)
        path_entry.config(fg="black")
    else:
        path_text.set("Nincs megadva!")
        path_entry.config(fg="grey")


def start_download_video():
    threading.Thread(target=download_video).start()

def format_720p(yt):
    video = yt.streams.get_highest_resolution()
    global filesize
    filesize = video.filesize
    progress_text.config(text=video.title, fg="black")
    video.download(output_path=path_text.get())


def download_video():
    global filesize
    yt_url = url_text.get()
    url_entry.config(state='disabled')
    path_entry.config(state='disabled')
    btn_dwn.config(state='disabled', bg='white')
    btn_dir.config(state='disabled', bg='white')

    # Single
    if radio_value.get() == 0:
        yt = YouTube(yt_url, on_progress_callback=progress)

        # 720p
        if radio_resolution_value.get() == 0:
            format_720p(yt)

        # 1080p
        if radio_resolution_value.get() == 1:
            try:
                video = yt.streams.filter(resolution="1080p").first()
                yt_a = YouTube(yt_url)
                audio = yt_a.streams.get_audio_only()
                filesize = video.filesize + audio.filesize

                progress_text.config(text=video.title, fg="black")

                video_name = f"{safe_filename(video.title)}_v.mp4"
                video_path = f"{path_text.get()}/{video_name}"
                audio_name = f"{safe_filename(audio.title)}_a.mp3"
                audio_path = f"{path_text.get()}/{audio_name}"
                merged_name = f"{safe_filename(video.title)}_FHD.mp4"
                merged_path = f"{path_text.get()}/{merged_name}"

                video.download(output_path=path_text.get(), filename=video_name)
                audio.download(output_path=path_text.get(), filename=audio_name)

                #ffmpeg_path = f"{os.getcwd()}/ffmpeg/bin/ffmpeg.exe"
                ffmpeg_path = "/usr/bin/ffmpeg"

                os.system(f'{ffmpeg_path} -i "{video_path}" -i "{audio_path}" -c copy "{merged_path}"')

                os.remove(video_path)
                os.remove(audio_path)
            except:
                format_720p(yt)

        # mp3
        if radio_resolution_value.get() == 2:

            audio = yt.streams.get_audio_only()
            filesize = audio.filesize
            progress_text.config(text=audio.title, fg="black")
            audio_name = f"{safe_filename(audio.title)}.mp3"
            audio.download(output_path=path_text.get(), filename=audio_name)

    # PlayList
    if radio_value.get() == 1:
        #playlist_url = url_text.get()
        pl = Playlist(yt_url)
        current_num = 0
        number_of_videos = len(pl.video_urls)


        for current_video in pl.videos:
            current_num += 1
            progress_text.config(text=current_video.title, fg="black")
            percent_label.config(text=f"{current_num}/{number_of_videos}", bg="#F0EEEE")
            # 720p
            if radio_resolution_value.get() == 0:
                video = current_video.streams.get_highest_resolution()
                video.download(output_path=path_text.get())
            # 1080p
            if radio_resolution_value.get() == 1:

                video = current_video.streams.filter(resolution="1080p").first()
                audio = current_video.streams.get_audio_only()
                video_name = f"{safe_filename(audio.title)}_v.mp4"
                video_path = f"{path_text.get()}/{video_name}"
                audio_name = f"{safe_filename(audio.title)}_a.mp3"
                audio_path = f"{path_text.get()}/{audio_name}"
                merged_name = f"{safe_filename(audio.title)}_FHD.mp4"
                merged_path = f"{path_text.get()}/{merged_name}"
                try:
                    video.download(output_path=path_text.get(), filename=video_name)
                    audio.download(output_path=path_text.get(), filename=audio_name)

                    #ffmpeg_path = f"{os.getcwd()}/ffmpeg/bin/ffmpeg.exe"
                    ffmpeg_path = "/usr/bin/ffmpeg"
                    os.system(f'{ffmpeg_path} -i "{video_path}" -i "{audio_path}" -c copy "{merged_path}"')

                    os.remove(video_path)
                    os.remove(audio_path)
                except:
                    video_name = video_name.replace("_v.mp4", ".mp4")
                    video = current_video.streams.get_highest_resolution()
                    video.download(output_path=path_text.get(), filename=video_name)

            if radio_resolution_value.get() == 2:
                audio = current_video.streams.get_audio_only()
                audio_name = f"{safe_filename(audio.title)}.mp3"
                audio.download(output_path=path_text.get(), filename=audio_name)

    url_entry.config(state='normal')
    path_entry.config(state='normal')
    btn_dwn.config(state='normal', bg=YT_RED)
    btn_dir.config(state='normal', bg=YT_RED)

    progress_text.config(text="A letöltés befejeződött.")
    percent_label.config(text="", bg="white")



def progress(chunk, file_handle, bytes_remaining):
    global filesize
    remaining = (100 * bytes_remaining) / filesize
    step = 100 - int(remaining)
    percent_label.config(text=f"{step}%", bg="#F0EEEE")


# Window
win = Tk()
win.geometry("650x350+400+200")
win.resizable(False, False)
win.config(background=BCKGND_COLOR)

# Titlebar
win.title("Pipacs YouTube Downloader - v0.1.2")

iconImage = b'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'
icon = PhotoImage(data=iconImage)

win.iconphoto(True, icon)

label_blank = Label(win, pady=0)

headerImage = b'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'

logo = PhotoImage(data=headerImage)

logo = logo.subsample(2)
Label(win, image=logo, bg=BCKGND_COLOR).pack()


# Radiobuttons
radio_frame = Frame(win, bg="blue", bd=0)
radio_frame.place(x=150, y=85)
radio_value = IntVar()
radio_single = Radiobutton(radio_frame, text="Video", font=("Ubuntu", 10, "bold"),
                           variable=radio_value, value=0, bg=BCKGND_COLOR)
radio_playlist = Radiobutton(radio_frame, text="PlayList", font=("Ubuntu", 10, "bold"),
                             variable=radio_value, value=1, bg=BCKGND_COLOR)
radio_single.pack(side=LEFT)
radio_playlist.pack(side=RIGHT)


radio_resolution_value = IntVar()
radio_resolution_720p = Radiobutton(win, text="mp3", font=("Ubuntu", 9, "bold"),
                                    variable=radio_resolution_value, value=2, bg=BCKGND_COLOR)
radio_resolution_720p.place(x=515, y=100)
radio_resolution_720p = Radiobutton(win, text="720p", font=("Ubuntu", 9, "bold"),
                                    variable=radio_resolution_value, value=0, bg=BCKGND_COLOR)
radio_resolution_720p.place(x=515, y=120)
radio_resolution_1080p = Radiobutton(win, text="1080p", font=("Ubuntu", 9, "bold"),
                                    variable=radio_resolution_value, value=1, bg=BCKGND_COLOR)
radio_resolution_1080p.place(x=515, y=140)

# URL label
url_label = Label(win, text="URL:", bg="white", font=("Ubuntu", 12, "bold"))
url_label.place(x=100, y=120)
url_entry_border = Frame(win, bg=YT_RED, bd=2)
url_entry_border.place(x=150, y=120)

url_text = StringVar()
url_text.set("Add meg a videó linkjét!")
url_entry = Entry(url_entry_border, textvariable=url_text, border=0, highlightthickness=1, highlightcolor="red",
                  font=("Ubuntu", 10), fg="grey", width=40)
url_entry.pack()
url_entry.bind("<1>", url_click)

# Directory chooser
download_label = Label(win, text="Letöltés helye:", font=("Ubuntu", 12, "bold"), bg="white")
download_label.place(x=28, y=170)
path_entry_border = Frame(win, bg=YT_RED, bd=2)
path_entry_border.place(x=150, y=170)

path_text = StringVar()
path_text.set("Nincs megadva!")
path_entry = Entry(path_entry_border, textvariable=path_text, border=0, highlightthickness=1, highlightcolor="red",
                   font=("Ubuntu", 10), fg="grey", width=40)
path_entry.pack()
path_entry.bind("<1>", path_click)

btn_dir = Button(win, text="Megnyitás", padx=10, font=("Ubuntu", 10, "bold"), fg="white", bg=YT_RED, bd=0,
                 command=saving_path)
btn_dir.place(x=520, y=170)

# Progress status
progress_label = Label(win, text="Folyamatban:", font=("Ubuntu", 12, "bold"), bg="white")
progress_label.place(x=36, y=220)
progress_text = Label(win, text="A letöltés még nem kezdődött el.", font=("Ubuntu", 10), bg="white", fg="grey")
progress_text.place(x=150, y=222)

percent_label = Label(win, text="", font=("Ubuntu", 8), bg="white", width=11)
percent_label.place(x=300, y=265)


# Download button
btn_dwn = Button(win, text="LETÖLTÉS", font=("Ubuntu", 10, "bold"), fg="white", bg=YT_RED, bd=0, padx=10,
                 command=start_download_video)
btn_dwn.place(x=290, y=300)


win.mainloop()
