#Helpers to get an set the wallpaper

import base64
import os
import requests
import ctypes
import platform
from screeninfo import get_monitors
import sys
from PIL import Image, ImageOps




#returns resolution for all displays
def get_display_resolutions():
    return list(map(lambda m : (m.width, m.height), get_monitors()))



#shuffles the img path list to best suit the resolutions
def shuffle_imgs_for_resolution(img_paths, resolutions):
    imgs_info = []
    for i in range(len(img_paths)):
        img = Image.open(img_paths[i])
        ImageOps.exif_transpose(img, in_place=True)
        res_comp = []
        #compare to all resolutions and calculate the total difference 
        for res in resolutions:
            adjusted_res = img.size
            mult_factor = 1
            if res[0] > res[1]:
                mult_factor = res[0] / adjusted_res[0]
            else:
                mult_factor = res[1] / adjusted_res[1]

            adjusted_res = (adjusted_res[0] * mult_factor, adjusted_res[1] * mult_factor)
            res_comp.append(abs(res[0] - adjusted_res[0])+ abs(res[1] - adjusted_res[1]))

        imgs_info.append({"og_ind": i, "res_comp": res_comp, "picked": False})
        img.close()

    out_paths = []
    for i in range(len(resolutions)):
        highest = float("inf")
        highest_ind = 0
        for j in range(len(imgs_info)):
            if (not imgs_info[j]["picked"]) and (imgs_info[j]["res_comp"][i] < highest):
                highest = imgs_info[j]["res_comp"][i]
                highest_ind = j
        
        imgs_info[highest_ind]["picked"] = True
        out_paths.append(img_paths[highest_ind])
    
    return out_paths



    


#adapts an image to a resolution by padding it with black bars
def adapt_img_to_resolution(img_path, resolution):
    img = Image.open(img_path)
    ImageOps.exif_transpose(img, in_place=True)
    img.thumbnail(resolution,Image.Resampling.LANCZOS)
    img = ImageOps.pad(img, resolution, color="black")
    img.save(img_path)

class WallpaperManager():
    
    def __init__(self, api_host, api_port, image_endpoint, current_wallpaper_path_prefix):
        self.api_host = api_host
        self.api_port = api_port
        self.image_endpoint = image_endpoint
        self.current_wallpaper_path_prefix = current_wallpaper_path_prefix

    #changes the wallpaper based on the initialized endpoint
    def change_wallpaper(self):
        self.resolutions = get_display_resolutions()

        #get an image for each resolution
        imgs = []
        for res in self.resolutions:
            new_img = self.get_base_64_wallpaper_image()
            imgs.append(new_img)

        self.set_wallpaper(imgs)

    #returns an image from the endpoint in base 64 format
    def get_base_64_wallpaper_image(self):
        img_src = self.api_host + ":" + str(self.api_port) + "/Image/" + self.image_endpoint
        return base64.b64encode(requests.get(img_src, verify=False).content)

    #sets the wallpaper of the current device to the given base 64 images
    def set_wallpaper(self, base_64s):

        current_wallpaper_paths = []
        for i in range(len(base_64s)):
            new_path = self.current_wallpaper_path_prefix + "_" + str(i) + ".png"


            if os.path.isfile(new_path):
                os.remove(new_path)
            
            #save base64 to file
            with open(new_path, "wb") as f:
                f.write(base64.decodebytes(base_64s[i]))

            current_wallpaper_path_absolute = os.path.abspath(new_path)
            current_wallpaper_paths.append(current_wallpaper_path_absolute)

        

        current_wallpaper_paths = shuffle_imgs_for_resolution(current_wallpaper_paths, self.resolutions)
        user_os = platform.system()
        if user_os == "Windows":
            self.set_wallpaper_windows(current_wallpaper_paths)

    #sets the wallpaper for windows. user must have display set to tile mdoe
    def set_wallpaper_windows(self, current_wallpaper_paths):
        for i in range(len(current_wallpaper_paths)):
            adapt_img_to_resolution(current_wallpaper_paths[i], self.resolutions[i])

        #put all images next to each
        images = [Image.open(x) for x in current_wallpaper_paths]
        widths, heights = zip(*(i.size for i in images))
        

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            y_offset = (max_height / 2) -  (im.height / 2)
            y_offset = int(y_offset)
            new_im.paste(im, (x_offset,y_offset))
            x_offset += im.size[0]

        win_wallpaper_path = self.current_wallpaper_path_prefix + "_win.png"
        new_im.save(win_wallpaper_path)


        ctypes.windll.user32.SystemParametersInfoW(20, 0,  os.path.abspath(win_wallpaper_path), 0)
