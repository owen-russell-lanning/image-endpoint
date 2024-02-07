#A client to set the wallpaper of your device from the image endpont#
#author: Owen Russell-Lanning

import json
import wallpaper
from infi.systray import SysTrayIcon


CONFIG_FILE = "config.json"
settings = {}

#host and port of the api
api_host = "https://localhost"
api_port = 7259
image_endpoint = "Today" #which endpoint to grab the wallpaper image from

current_wallpaper_path = None

def main():
    init()

    


#sets settings from the config file
def init():
    global settings
    global api_host
    global api_port
    global current_wallpaper_path
    global image_endpoint

    with open(CONFIG_FILE) as f:
        settings = json.load(f)
    
    api_port = settings["port"]
    api_host = settings["host"]
    current_wallpaper_path = settings["current_wallpaper_path"]
    image_endpoint = settings["image_endpoint"]

    init_sys_tray()



 
#initializes the application in the system tray
def init_sys_tray():
    def change_wallpaper(systray):
        wallpaper.change_wallpaper(api_host, api_port, image_endpoint, current_wallpaper_path)

    menu_options = (("Change Wallpaper", None, change_wallpaper),)
    systray = SysTrayIcon("icon.ico", "Image Endpoint Client", menu_options)
    systray.start()



if __name__ == "__main__":
    main()