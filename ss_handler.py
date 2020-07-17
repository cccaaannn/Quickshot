from datetime import datetime
import mss.tools
import mss
import os



class ss_handler():
    def __init__(self):
        self.set_options()

    

    def set_options(self, 
    save_path = "HOME", 
    create_root_file = "Sshot", 
    before_ss_name = "ss_", 
    after_ss_name = "", 
    before_number = "(", 
    after_number = ")", 
    date_formatting = "%y-%m-%d_%H-%M", 
    png_compression_level = -1, 
    multi_screen = False):
        
        self.save_path = save_path

        self.create_root_file = create_root_file

        self.before_ss_name = before_ss_name
        self.after_ss_name = after_ss_name

        self.before_number = before_number
        self.after_number = after_number

        self.date_formatting = date_formatting

        self.png_compression_level = png_compression_level

        self.multi_screen = multi_screen


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


    def __create_dir_if_not_exists(self, path):
        if(not os.path.exists(path)):
            os.makedirs(path)


    def __path_handler(self):
    
        # handle path
        if(self.save_path == "HOME"):

            if(os.name == "nt"):
                save_path = os.getenv("HOMEPATH")
                save_path = os.path.join(save_path, "Desktop")

                if(not save_path):
                    save_path = os.path.expanduser(os.getenv('USERPROFILE'))
                    save_path = os.path.join(save_path, "Desktop")

                    if(not save_path):
                        save_path = os.getenv("HOMEPATH")

                        if(not save_path):
                            return False

            else:
                save_path = os.getenv("HOME")
                if(not save_path):
                    return False

        elif(self.save_path == ""):
            save_path = ""
        
        else:
            if(os.path.exists(self.save_path)):
                save_path = self.save_path
            else:
                return False
                

        # create root file
        if(self.create_root_file):
            save_path = os.path.join(save_path, self.create_root_file)
            self.__create_dir_if_not_exists(save_path)

        return save_path


    def take_ss(self, ss_bbox = None, ss_extension = ".png"):

        save_path = self.__path_handler()

        if(not save_path):
            return False, "ss could not be saved: path handler returned error"


        # format date
        now = datetime.now()
        formatted_now = datetime.strftime(now, self.date_formatting)

        # create path
        temp_ss_name = "{0}{1}{2}{3}".format(self.before_ss_name, formatted_now, self.after_ss_name, ss_extension)
        temp_ss_name = os.path.join(save_path, temp_ss_name)
        ss_full_name = self.__create_unique_file_name(temp_ss_name)

        # take ss
        try:
            with mss.mss() as sct:
                sct.compression_level = self.png_compression_level

                if(self.multi_screen):
                    sct.shot(mon = -1, output = ss_full_name)
                else:
                    if(ss_bbox):
                        im = sct.grab(ss_bbox)
                    else:
                        im = sct.grab(sct.monitors[1])

                    mss.tools.to_png(im.rgb, im.size, level = self.png_compression_level, output = ss_full_name)


        except:
            return False, "ss could not be saved: ss handler returned error"


        return True, ss_full_name 





# ss_h = ss_handler()
# a = ss_h.take_ss(ss_bbox=(50,50,500,500))

# print(a)



# from PIL import Image

# im = Image.open("Ba_b_do8mag_c6_big.png")
# rgb_im = im.convert('RGB')
# rgb_im.save('colors.jpg')







