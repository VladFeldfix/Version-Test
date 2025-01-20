# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *
import shutil
import datetime
from datetime import datetime

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
        self.logs_location = self.sc.get_setting("Logs")

        # test locations 
        self.sc.test_path(self.projects)
        self.sc.test_path(self.backup)
        self.sc.test_path(self.logs_location)

        # start
        self.log = []
        self.sc.start()
    
    def run(self):
        self.sc.print("PROCESSING...")
        projects = {}
        for root, dirs, files in os.walk(self.projects):
            for file in files:
                path = root+"/"+file
                if self.file_can_be_opened(path):
                    scr_path = path
                    scr_filename = scr_path.replace(self.projects, "").replace("\\", "/")
                    print(scr_filename)
    
    def file_can_be_opened(self,file):
        result = False
        try:
            file = open(file,'r')
            lines = file.readlines()
            file.close()
            result = True
        except:
            result = False
        return result

main()