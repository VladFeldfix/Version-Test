# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *
import shutil

class main:
    # constructor
    def __init__(self):
        # load smart console
        self.sc = SmartConsole("Version-Test", "2.0")
        
        # set-up main memu
        self.sc.add_main_menu_item("RUN", self.run)

        # load settings
        self.projects = self.sc.get_setting("Projects")
        self.backup = self.sc.get_setting("Backups")

        # test locations 
        self.sc.test_path(self.projects)
        self.sc.test_path(self.backup)

        # start
        self.sc.start()
    
    def run(self):
        # create database
        self.sc.print("PROCESSING...")
        for root, dirs, files in os.walk(self.projects):
            for file in files:
                path = root+"/"+file
                filename = path
                filename = filename.replace(self.projects, "")
                filename = filename.replace("\\", "/")
                filename = filename.split("/")
                if len(filename) > 2:
                    project = filename[1]
                    file_in_project = "/".join(filename[2:])
                    file_in_project = file_in_project.replace("/", " + ")
                    
                    # create a copy of the projects in my tmp folder
                    if not os.path.isdir(self.backup+"/"+project):
                        os.makedirs(self.backup+"/"+project)
                    
                    # create a copy of the file in the backup folder
                    if not os.path.isfile(self.backup+"/"+project+"/"+file_in_project):
                        shutil.copy(path, self.backup+"/"+project+"/"+file_in_project)
                    else:
                        same = self.compare_files(path,self.backup+"/"+project+"/"+file_in_project)
    
    def compare_files(self, scr, dst):
        result = True
        return result

main()