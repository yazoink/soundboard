#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from sys import exit as sys_exit
from math import ceil
from os import path, environ
from json import loads as json_loads
from functools import partial
import subprocess
import threading

def main():
    config = get_config()

    win = Gtk.Window(title="Soundboard")
    win.set_border_width(15)

    vbox = Gtk.Box(
        spacing=10,
        orientation=Gtk.Orientation.VERTICAL
    )

    buttons = []
    i = 0

    for b in config["buttons"]:
        buttons.append(Gtk.Button(label=b["label"]))
        buttons[i].connect("clicked", partial(on_button_clicked, b["audio"]))
        i += 1

    button_num = len(buttons)
    buttons_per_row = config["max_per_row"]
    row_num = 1

    if button_num < buttons_per_row:
        buttons_per_row = button_num
    else:
        row_num = ceil(button_num / buttons_per_row)

    rows = []
    button_index = 0

    for i in range(0, row_num):
        rows.append(Gtk.Box(spacing=10))
        for j in range(button_index, button_index + buttons_per_row):
            if j >= button_num:
                break
            rows[i].pack_start(buttons[j], True, True, 0)
        button_index += buttons_per_row
        vbox.pack_start(rows[i], True, True, 0)

    win.add(vbox)

    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

def get_config():
    config = {}
    original_config = {
        "max_per_row": 5,
        "buttons": [
            {
                "label": "Ahhh",
                "audio": "/usr/share/soundboard/sounds/ahhh.wav",
            },
            {
                "label": "Android Beep",
                "audio": "/usr/share/soundboard/sounds/android-beep.wav",
            },
            {
                "label": "Fart",
                "audio": "/usr/share/soundboard/sounds/fart.wav",
            },
            {
                "label": "Hey Guys",
                "audio": "/usr/share/soundboard/sounds/hey-guys-whats-going-on.wav",
            },
            {
                "label": "Kahoot",
                "audio": "/usr/share/soundboard/sounds/kahoot.wav",
            },
            {
                "label": "Snore Mimimimi",
                "audio": "/usr/share/soundboard/sounds/snore-mimimimimimi.wav",
            },
            {
                "label": "Sus",
                "audio": "/usr/share/soundboard/sounds/sus.wav",
            },
            {
                "label": "Vine Boom",
                "audio": "/usr/share/soundboard/sounds/vine-boom.wav",
            },
            {
                "label": "Windows Error",
                "audio": "/usr/share/soundboard/sounds/win-error.wav",
            },
            {
                "label": "Windows XP Shutdown",
                "audio": "/usr/share/soundboard/sounds/winxp-shutdown.wav",
            },
        ]
    }

    home = environ['HOME']
    config_dir = home + "/.config/soundboard/"
    config_file = None

    if path.exists(config_dir + "config.json"):
        config_file = config_dir + "config.json"
    elif path.exists("/usr/share/soundboard/config.json"):
        config_file = "/usr/share/soundboard/config.json"

    if config_file == None:
        return original_config

    if config_file:
        with open(config_file, "r") as f:
            c = f.read()

        try:
            config = json_loads(c)
        except ValueError:
            print("Error: could not parse config.json, please check for syntax errors.")
            sys_exit(1)

        if "max_per_row" not in config or config["max_per_row"] <= 0:
            config["max_per_row"] = original_config["max_per_row"]

        if "buttons" not in config or len(config["buttons"]) < 1:
            print("Error: no buttons in config.json.")
            sys_exit(1)

    return config

def on_button_clicked(audio, _):
    t = threading.Thread(target=play_sound, args=(audio,))
    t.start()

def play_sound(audio):
    subprocess.run(["aplay", audio])

main()
