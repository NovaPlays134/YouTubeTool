import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from pytube import Search
import os
from urllib.parse import urlparse
from tkinter import filedialog
import time
import math
import pyperclip

# https://pytube.io/en/latest/api.html#youtube-object

# root
root = tk.Tk()
root.title("YouTube Tool")
root.resizable(False, False)
start_time = 0

# geometry
window_width, window_height= 1200, 800

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# main Frame
main_frame = tk.Frame(root, bg = "#1e1f22")
main_frame.place(relwidth = 1, relheight = 1)

# functions
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    
    # Calculate the download percentage
    percentage = (bytes_downloaded / total_size) * 100
    
    # Calculate the remaining time
    elapsed_time = time.time() - start_time
    download_speed = bytes_downloaded / elapsed_time
    remaining_bytes = total_size - bytes_downloaded
    remaining_time = remaining_bytes / download_speed if download_speed > 0 else 0
    
    # Update the progress label
    remaining_time_label.config(text="Downloading: {:.2f}% | Time Remaining: {:.2f} seconds".format(percentage, remaining_time))

def check_download_vid_url(url):
    if is_valid_url(url) and ".youtube" in url:
        download_url_label.config(text = "URL:")
        youtube_id = YouTube(url, on_progress_callback=on_progress)
        available_resolutions = []

        dir = filedialog.asksaveasfilename(defaultextension = video_ex_combobox.get())
        download_path = os.path.dirname(dir)
        file_name = os.path.basename(dir)
        if os.path.exists(download_path) and file_name != "":
            start_time = time.time()

            for stream in youtube_id.streams.filter(progressive = True):
                if stream.resolution:
                    available_resolutions.append(stream.resolution)

            desired_resolution = resolution_combobox.get()

            if desired_resolution in available_resolutions:
                print(f"in res {desired_resolution}")
                video = youtube_id.streams.filter(progressive=True, resolution=desired_resolution)
                video.first().download(output_path = download_path, filename = file_name)
            else:
                print(f"not in res {desired_resolution}")
                video = youtube_id.streams.get_highest_resolution()
                video.download(output_path = download_path, filename = file_name)

            elapsed_time = time.time() - start_time
            remaining_time_label.config(text= f"Download Complete, took {math.ceil(elapsed_time*100)/100} seconds")
    else:
        download_url_label.config(text = "URL: Invalid URL (make sure the URL is correct and a YouTube URL)")


def check_download_sound_url(url):
    if is_valid_url(url) and ".youtube" in url:
        download_url_label.config(text = "URL:")
        youtube_id = YouTube(url, on_progress_callback = on_progress)
        audio = youtube_id.streams.filter(only_audio = True).first()
        dir = filedialog.asksaveasfilename(defaultextension = audio_ex_combobox.get())
        download_path = os.path.dirname(dir)
        file_name = os.path.basename(dir)
        if os.path.exists(download_path) and file_name != "":
            start_time = time.time()
            audio.download(output_path = download_path, filename = file_name)
            elapsed_time = time.time() - start_time
            remaining_time_label.config(text= f"Download Complete, took {math.ceil(elapsed_time*100)/100} seconds")
    else:
        download_url_label.config(text = "URL: Invalid URL (make sure the URL is correct and a YouTube URL)")

def get_info_from_url(url):
    if is_valid_url(url) and ".youtube" in url:
        info_url_label.config(text = "URL:")
        youtube_id = YouTube(url, on_progress_callback = on_progress)

        length = youtube_id.length
        minutes = length // 60
        seconds = length % 60

        info_window_canvas.itemconfig(title_text_item, text = f"Title: {youtube_id.title}")
        info_window_canvas.itemconfig(author_text_item, text = f"Author: {youtube_id.author}")
        info_window_canvas.itemconfig(views_text_item, text = f"Views: {format(youtube_id.views, ',')}")
        info_window_canvas.itemconfig(length_text_item, text = f"Length: {minutes:02d}:{seconds:02d}")
        info_window_canvas.itemconfig(publish_date_text_item, text = f"Publish Date: {youtube_id.publish_date}")
        info_window_canvas.itemconfig(channel_url_text_item, text = f"Channel URL: {youtube_id.channel_url}")
        info_window_canvas.itemconfig(thumbnail_url_text_item, text = f"Thumbnail URL: {youtube_id.thumbnail_url}")
        info_window_canvas.itemconfig(channel_id_text_item, text = f"Channel ID: {youtube_id.channel_id}")
    else:
        info_url_label.config(text = "URL: Invalid URL (make sure the URL is correct and a YouTube URL)")

def copy_text(convas, text_item):
    string = convas.itemcget(text_item, "text")
    parts = string.split(": ")
    if len(parts) > 1:
        extracted_part = parts[1].strip()
        pyperclip.copy(extracted_part)

# downloader frame
download_frame = tk.Frame(root, bg = "#313338")
download_frame.place(width = 1120, height = 250, relx = 0.03, rely = 0.05)

download_title_canvas = tk.Canvas(download_frame, width = 1120, height = 40, bg = "#2b2d31", highlightthickness = 0)
download_title_canvas.create_text(560, 20, text = "Downloader", fill = "white", font = ("Segoe UI", 14))
download_title_canvas.pack()

download_url_label = tk.Label(download_frame, text = "URL:", fg="white", bg="#313338", font = ("Segoe UI", 9))
download_url_label.pack(padx = 10, pady = 10, anchor=tk.NW)

download_entry = tk.Entry(download_frame, width = 181, bg = "#313338", fg = "white", highlightcolor="white", highlightthickness = 1)
download_entry.place(relx = 0.5, rely = 0.34, anchor = tk.CENTER)


# download buttons
video_file_extensions = [".mp4", ".mov", ".wmv", ".avi", ".mkv"]
audio_file_extensions = [".mp3", ".acc", ".flac", ".wav", ".aiff"]
resolutions = ["144p", "360p", "720p"]

extensions_frame = tk.Frame(download_frame, bg = "#313338")
extensions_frame.place(width = 400, height = 50, relx = 0.3, rely = 0.61, anchor = tk.CENTER)

video_ex_combobox = ttk.Combobox(extensions_frame, values = video_file_extensions, width = 15, font = ("Segoe UI", 14))
video_ex_combobox["state"] = "readonly"
video_ex_combobox.pack(side = tk.LEFT, anchor = tk.N)
video_ex_combobox.set(".mp4")

resolution_combobox = ttk.Combobox(extensions_frame, values = resolutions, width = 15, font = ("Segoe UI", 14), style = "TCombobox")
resolution_combobox["state"] = "readonly"
resolution_combobox.pack(side = tk.LEFT, anchor = tk.N, padx = 7)
resolution_combobox.set("720p")

extensions_frame2 = tk.Frame(download_frame, bg = "#313338")
extensions_frame2.place(width = 400, height = 50, relx = 0.3, rely = 0.73, anchor = tk.CENTER)

audio_ex_combobox = ttk.Combobox(extensions_frame2, values = audio_file_extensions, width = 33, font = ("Segoe UI", 14), style = "TCombobox")
audio_ex_combobox["state"] = "readonly"
audio_ex_combobox.pack(side = tk.LEFT)
audio_ex_combobox.set(".mp3")

download_frame.option_add('*TCombobox*Listbox.font', ("Segoe UI", 14))

download_button_frame = tk.Frame(download_frame, bg = "#313338")
download_button_frame.place(width = 400, height = 100, relx = 0.7, rely = 0.7, anchor = tk.CENTER)

download_video_button = tk.Button(download_button_frame, text = "Download Video", font = ("Segoe UI", 12), command = lambda: check_download_vid_url(download_entry.get()),
                    width = 50, bg = "#1f1f1f", fg = "#b3b3b3", bd = 0, highlightbackground = "#1f1f1f", highlightcolor = "#1f1f1f", activebackground = "#1f1f1f", activeforeground = "white")
download_video_button.pack(anchor = tk.CENTER)

download_video_button.bind("<Enter>", lambda event: download_video_button.config(fg = "white"))
download_video_button.bind("<Leave>", lambda event: download_video_button.config(fg = "#b3b3b3"))

download_sound_button = tk.Button(download_button_frame, text = "Download Audio", font = ("Segoe UI", 12), command = lambda: check_download_sound_url(download_entry.get()),
                    width = 50, bg = "#1f1f1f", fg = "#b3b3b3", bd = 0, highlightbackground = "#1f1f1f", highlightcolor = "#1f1f1f", activebackground = "#1f1f1f", activeforeground = "white")
download_sound_button.pack(pady = 10, anchor = tk.CENTER)

download_sound_button.bind("<Enter>", lambda event: download_sound_button.config(fg = "white"))
download_sound_button.bind("<Leave>", lambda event: download_sound_button.config(fg = "#b3b3b3"))

remaining_time_label = tk.Label(download_frame, text = "", fg="white", bg="#313338", font = ("Segoe UI", 8))
remaining_time_label.pack(padx = 20, pady = 15, anchor=tk.NE)


# Video Info
info_frame = tk.Frame(root, bg = "#313338")
info_frame.place(width = 1120, height = 450, relx = 0.03, rely = 0.4)

info_title_canvas = tk.Canvas(info_frame, width = 1120, height = 40, bg = "#2b2d31", highlightthickness = 0)
info_title_canvas.create_text(560, 20, text = "Info", fill = "white", font = ("Segoe UI", 14))
info_title_canvas.pack()

info_url_label = tk.Label(info_frame, text = "URL:", fg="white", bg="#313338", font = ("Segoe UI", 9))
info_url_label.pack(padx = 10, pady = 10, anchor=tk.NW)

info_entry = tk.Entry(info_frame, width = 181, bg = "#313338", fg = "white", highlightcolor="white", highlightthickness = 1)
info_entry.place(relx = 0.5, rely = 0.19, anchor = tk.CENTER)

# Video Info buttons
getinfo_button_frame = tk.Frame(info_frame, bg = "#313338")
getinfo_button_frame.place(width = 500, height = 100, relx = 0.5, rely = 0.4, anchor = tk.CENTER)


get_info_button = tk.Button(getinfo_button_frame, text = "Get Info", font = ("Segoe UI", 12), command = lambda: get_info_from_url(info_entry.get()),
                    width = 60, bg = "#1f1f1f", fg = "#b3b3b3", bd = 0, highlightbackground = "#1f1f1f", highlightcolor = "#1f1f1f", activebackground = "#1f1f1f", activeforeground = "white")
get_info_button.pack(anchor = tk.CENTER)

get_info_button.bind("<Enter>", lambda event: get_info_button.config(fg = "white"))
get_info_button.bind("<Leave>", lambda event: get_info_button.config(fg = "#b3b3b3"))


info_window_canvas = tk.Canvas(info_frame, width = 1060, height = 250, bg = "#2b2d31", highlightthickness = 0)
title_text_item = info_window_canvas.create_text(15, 20, text = "Title:", fill = "white", font = ("Segoe UI", 14), anchor = tk.W)
author_text_item = info_window_canvas.create_text(15, 50, text = "Author:", fill = "white", font = ("Segoe UI", 14), anchor = tk.W)
views_text_item = info_window_canvas.create_text(15, 80, text = "Views:", fill = "white", font = ("Segoe UI", 14), anchor = tk.W)
length_text_item = info_window_canvas.create_text(15, 110, text = "Length:", fill = "white", font = ("Segoe UI", 14), anchor = tk.W)
publish_date_text_item = info_window_canvas.create_text(15, 140, text = "Publish Date:", fill = "white", font = ("Segoe UI", 14), anchor = tk.W)
channel_url_text_item = info_window_canvas.create_text(15, 170, text = "Channel URL:", fill = "white", font = ("Segoe UI", 14), anchor = tk.W)
thumbnail_url_text_item = info_window_canvas.create_text(15, 200, text = "Thumbnail URL:", fill = "white", font = ("Segoe UI", 14), anchor = tk.W)
channel_id_text_item = info_window_canvas.create_text(15, 230, text = "Channel ID:", fill = "white", font = ("Segoe UI", 14), anchor = tk.W)
info_window_canvas.place(x = 30, y = 180)

# copy buttons
getinfo_button_frame = tk.Frame(info_frame, bg = "#313338")
getinfo_button_frame.place(width = 35, height = 250, relx = 0.001, rely = 0.675, anchor = tk.W)

copy_channel_id_button = tk.Button(getinfo_button_frame, text = "copy", font = ("Segoe UI", 9), command = lambda: copy_text(info_window_canvas, channel_id_text_item),
                    width = 60, bg = "#313338", fg = "#b3b3b3", bd = 0, highlightbackground = "#313338", highlightcolor = "#313338", activebackground = "#313338", activeforeground = "white")
copy_channel_id_button.pack(pady = 5, side = tk.BOTTOM)

copy_channel_id_button.bind("<Enter>", lambda event: copy_channel_id_button.config(fg = "white"))
copy_channel_id_button.bind("<Leave>", lambda event: copy_channel_id_button.config(fg = "#b3b3b3"))

copy_thumbnail_url_button = tk.Button(getinfo_button_frame, text = "copy", font = ("Segoe UI", 9), command = lambda: copy_text(info_window_canvas, thumbnail_url_text_item),
                    width = 60, bg = "#313338", fg = "#b3b3b3", bd = 0, highlightbackground = "#313338", highlightcolor = "#313338", activebackground = "#313338", activeforeground = "white")
copy_thumbnail_url_button.pack(pady = 6, side = tk.BOTTOM)

copy_thumbnail_url_button.bind("<Enter>", lambda event: copy_thumbnail_url_button.config(fg = "white"))
copy_thumbnail_url_button.bind("<Leave>", lambda event: copy_thumbnail_url_button.config(fg = "#b3b3b3"))


copy_channel_url_button = tk.Button(getinfo_button_frame, text = "copy", font = ("Segoe UI", 9), command = lambda: copy_text(info_window_canvas, channel_url_text_item),
                    width = 60, bg = "#313338", fg = "#b3b3b3", bd = 0, highlightbackground = "#313338", highlightcolor = "#313338", activebackground = "#313338", activeforeground = "white")
copy_channel_url_button.pack(side = tk.BOTTOM)

copy_channel_url_button.bind("<Enter>", lambda event: copy_channel_url_button.config(fg = "white"))
copy_channel_url_button.bind("<Leave>", lambda event: copy_channel_url_button.config(fg = "#b3b3b3"))

root.mainloop()