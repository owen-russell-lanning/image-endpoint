#Helpers to get an set the wallpaper

import base64
import os
import requests
import ctypes
import platform

#returns an image from the endpoint in base 64 format
def get_base_64_wallpaper_image(api_host, api_port, image_endpoint):
    img_src = api_host + ":" + str(api_port) + "/Image/" + image_endpoint
    return base64.b64encode(requests.get(img_src, verify=False).content)

#sets the wallpaper of the current device to the given base 64 image
def set_wallpaper(base_64, current_wallpaper_path):
    if os.path.isfile(current_wallpaper_path):
        os.remove(current_wallpaper_path)
    
    #save base64 to file
    with open(current_wallpaper_path, "wb") as f:
        f.write(base64.decodebytes(base_64))

    current_wallpaper_path_absolute = os.path.abspath(current_wallpaper_path)
    user_os = platform.system()
    if user_os == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, current_wallpaper_path_absolute, 0)

#changes the wallpaper based on the specified endpoint
def change_wallpaper(api_host, api_port, image_endpoint, current_wallpaper_path):
    img = get_base_64_wallpaper_image(api_host, api_port, image_endpoint)
    set_wallpaper(img, current_wallpaper_path)

