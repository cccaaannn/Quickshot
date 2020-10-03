from datetime import datetime
from io import BytesIO
from PIL import Image
import win32clipboard
import mss.tools
import locale
import mss
import os

class ss_handler():
    def __init__(self,     
    ss_extension = ".png",
    save_path = "HOME", 
    create_root_file = "Qshot", 
    before_ss_name = "qs_", 
    after_ss_name = "", 
    before_number = "(", 
    after_number = ")", 
    date_formatting = "%y-%m-%d_%H-%M", 
    use_system_local_date_naming = True,
    png_compression_level = -1, 
    multi_screen = False,
    save_clipboard = True
    ):

        self.ss_extension = ss_extension

        self.save_path = save_path

        self.create_root_file = create_root_file

        self.before_ss_name = before_ss_name
        self.after_ss_name = after_ss_name

        self.before_number = before_number
        self.after_number = after_number

        self.date_formatting = date_formatting

        self.png_compression_level = png_compression_level

        self.multi_screen = multi_screen
        
        self.save_clipboard = save_clipboard

        if(use_system_local_date_naming):
            locale.setlocale(locale.LC_ALL, "")
        else:
            locale.setlocale(locale.LC_ALL, "en_EN")


    def __create_unique_file_name(self, file_path):
        temp_file_path = file_path
        file_name_counter = 1
        if(os.path.isfile(temp_file_path)):
            while(True):
                save_path, temp_file_name = os.path.split(temp_file_path)
                temp_file_name, temp_file_extension = os.path.splitext(temp_file_name)
                temp_file_name = "{0}{1}{2}{3}{4}".format(temp_file_name, self.before_number, file_name_counter, self.after_number, temp_file_extension)
                temp_file_path = os.path.join(save_path, temp_file_name)
                file_name_counter += 1
                if(os.path.isfile(temp_file_path)):
                    temp_file_path = file_path
                else:
                    file_path = temp_file_path
                    break

        return file_path


    def __path_handler(self):
        """handles path"""
        # if path is set to HOME try to get desktop
        if(self.save_path == "HOME"):
            
            # windows
            if(os.name == "nt"):
                save_path = os.getenv("HOMEPATH")
                save_path = os.path.join(save_path, "Desktop")

                if(not save_path):
                    save_path = os.path.expanduser(os.getenv('USERPROFILE'))
                    save_path = os.path.join(save_path, "Desktop")

                    if(not save_path):
                        save_path = os.getenv("HOMEPATH")

                        if(not save_path):
                            return False, "Path error: could not get Desktop path, you can give it manually"

            # other os
            else:
                save_path = os.getenv("HOME")
                if(not save_path):
                    return False, "Path error: could not get Home path, you can give it manually"

        elif(self.save_path == ""):
            save_path = ""
        
        else:
            if(os.path.exists(self.save_path)):
                save_path = self.save_path
            else:
                return False, "Path error: path does not exists"
                

        # create root file
        if(self.create_root_file):
            save_path = os.path.join(save_path, self.create_root_file)
            if(not os.path.exists(save_path)):
                os.makedirs(save_path)

        return save_path, "Path constructed successfully"


    def __copy_image_to_clipboard(self, image_path):
        """saves image to win32 clipboard"""
        
        image = Image.open(image_path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()


    def to_jpg(self, raw_pixels, output = None):
        """Converts raw pixels to jpg
        pil usage example from mss documentation"""

        # Create an Image
        temp_image = Image.new("RGB", raw_pixels.size)
        # Best solution: create a list(tuple(R, G, B), ...) for putdata()
        pixels = zip(raw_pixels.raw[2::4], raw_pixels.raw[1::4], raw_pixels.raw[0::4])
        temp_image.putdata(list(pixels))
        
        if(output):
            temp_image.save(output)
        else:
            return temp_image



    def take_ss(self, ss_bbox = None):
        
        # get path
        save_path, path_info = self.__path_handler()
        if(not save_path):
            return False, path_info

        # format date
        try:
            now = datetime.now()
            formatted_now = datetime.strftime(now, self.date_formatting)
        except Exception as e:
            print(e)
            return False, "ss could not be saved: date format is wrong"

        # create path
        temp_ss_name = "{0}{1}{2}{3}".format(self.before_ss_name, formatted_now, self.after_ss_name, self.ss_extension)
        temp_ss_name = os.path.join(save_path, temp_ss_name)
        ss_full_name = self.__create_unique_file_name(temp_ss_name)

        # take ss
        try:
            with mss.mss() as sct:

                if(ss_bbox):
                    sct_img = sct.grab(ss_bbox)
                elif(self.multi_screen):
                    sct_img = sct.grab(sct.monitors[0])
                else:
                    sct_img = sct.grab(sct.monitors[1])

                # convert and save
                if(self.ss_extension == ".png"):
                    sct.compression_level = self.png_compression_level
                    mss.tools.to_png(sct_img.rgb, sct_img.size, level = self.png_compression_level, output = ss_full_name)
                elif(self.ss_extension == ".jpg"):
                    self.to_jpg(sct_img, output = ss_full_name)
                else:
                    return False, "ss could not be saved: extension type is not supported"

            # clipboard stuff
            if(self.save_clipboard):
                try:
                    self.__copy_image_to_clipboard(ss_full_name)
                except Exception as e:
                    print(e)
                    return False, "clipboard error: ss saved but clipboard returned error (try without this setting)"
                
        except Exception as e:
            print(e)
            return False, "ss could not be saved: ss handler returned error (path could have bad chars)"


        return True, ss_full_name 


