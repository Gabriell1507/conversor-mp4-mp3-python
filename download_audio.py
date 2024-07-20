import os
import sys
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, Radiobutton, messagebox, Frame

from yt_dlp import YoutubeDL

def download_video():
    try:
        video_url = url_entry.get()
        platform = platform_choice.get()
        device_platform = device_choice.get()

        if platform == 'twitter' and 'x.com' in video_url:
            video_url = video_url.replace('x.com', 'twitter.com')

        if device_platform == 'android':
            download_dir = os.path.join(os.path.expanduser('~'), 'storage', 'emulated', '0', 'Download')
        else:
            download_dir = download_path or os.path.join(os.path.expanduser('~'), 'Downloads')

        ydl_opts = {
            'format': 'bestaudio/best' if format_choice.get() == 'mp3' else 'best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s')
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info_dict)

            if format_choice.get() == 'mp3':
                base, ext = os.path.splitext(file_name)
                new_file = base + '.mp3'
                os.rename(file_name, new_file)
                file_name = new_file

        messagebox.showinfo("Sucesso", f"Download concluído com sucesso em {file_name}!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def select_directory():
    global download_path
    download_path = filedialog.askdirectory()
    if not download_path:
        download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    path_label.config(text=f"Diretório: {download_path}")

root = Tk()

bg_color = "#f2f2f2"
text_color = "#333333"
font = ("Arial", 12)
button_color = "#007bff"
button_text_color = "white"

root.configure(bg=bg_color)

frame = Frame(root, bg=bg_color, padx=20, pady=20)
frame.grid(row=0, column=0, padx=10, pady=10)

title_label = Label(frame, text="Baixar Vídeo", bg=bg_color, fg=text_color, font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

Label(frame, text="URL do vídeo:", bg=bg_color, fg=text_color, font=font).grid(row=1, column=0, sticky="e", padx=10, pady=10)
url_entry = Entry(frame, width=50, font=font, relief="solid", borderwidth=1)
url_entry.grid(row=1, column=1, padx=10, pady=10)

Label(frame, text="Plataforma:", bg=bg_color, fg=text_color, font=font).grid(row=2, column=0, sticky="e", padx=10, pady=10)
platform_choice = StringVar(value='youtube')
platforms_frame = Frame(frame, bg=bg_color)
platforms_frame.grid(row=2, column=1, padx=10, pady=5, sticky="w")
Radiobutton(platforms_frame, text="YouTube", variable=platform_choice, value='youtube', bg=bg_color, fg=text_color, font=font).pack(side="left", padx=5)
Radiobutton(platforms_frame, text="Instagram", variable=platform_choice, value='instagram', bg=bg_color, fg=text_color, font=font).pack(side="left", padx=5)
Radiobutton(platforms_frame, text="Facebook", variable=platform_choice, value='facebook', bg=bg_color, fg=text_color, font=font).pack(side="left", padx=5)
Radiobutton(platforms_frame, text="Twitter", variable=platform_choice, value='twitter', bg=bg_color, fg=text_color, font=font).pack(side="left", padx=5)

Label(frame, text="Dispositivo:", bg=bg_color, fg=text_color, font=font).grid(row=3, column=0, sticky="e", padx=10, pady=10)
device_choice = StringVar(value='pc')
device_frame = Frame(frame, bg=bg_color)
device_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")
Radiobutton(device_frame, text="PC", variable=device_choice, value='pc', bg=bg_color, fg=text_color, font=font).pack(side="left", padx=5)
Radiobutton(device_frame, text="Android", variable=device_choice, value='android', bg=bg_color, fg=text_color, font=font).pack(side="left", padx=5)

Label(frame, text="Formato:", bg=bg_color, fg=text_color, font=font).grid(row=4, column=0, sticky="e", padx=10, pady=10)
format_choice = StringVar(value='mp3')
format_frame = Frame(frame, bg=bg_color)
format_frame.grid(row=4, column=1, padx=10, pady=5, sticky="w")
Radiobutton(format_frame, text="MP3", variable=format_choice, value='mp3', bg=bg_color, fg=text_color, font=font).pack(side="left", padx=5)
Radiobutton(format_frame, text="MP4", variable=format_choice, value='mp4', bg=bg_color, fg=text_color, font=font).pack(side="left", padx=5)

path_label = Label(frame, text="Diretório: Não selecionado", bg=bg_color, fg=text_color, font=font)
path_label.grid(row=5, column=0, columnspan=2, pady=(10, 10))
Button(frame, text="Selecionar Diretório", command=select_directory, bg=button_color, fg=button_text_color, font=font, relief="solid", borderwidth=1).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

download_button = Button(frame, text="Download", command=download_video, bg=button_color, fg=button_text_color, font=font, relief="solid", borderwidth=1)
download_button.grid(row=7, column=0, columnspan=2, padx=10, pady=20)

download_path = ''

root.mainloop()
