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
        # create database
        self.sc.print("PROCESSING...")
        projects = []
        for root, dirs, files in os.walk(self.projects):
            for file in files:
                path = root+"/"+file
                filename = path
                filename = filename.replace(self.projects, "")
                filename = filename.replace("\\", "/")
                filename = filename.split("/")
                if len(filename) > 2:
                    project = filename[1]
                    if not project in projects:
                        projects.append(project)
                        self.print(project+":","white")
                    file_in_project = "/".join(filename[2:])
                    file_in_project = file_in_project.replace("/", " + ")
                    
                    # create a copy of the projects in my tmp folder
                    if not os.path.isdir(self.backup+"/"+project):
                        os.makedirs(self.backup+"/"+project)
                    
                    # create a copy of the file in the backup folder
                    scr = path
                    dst = self.backup+"/"+project+"/"+file_in_project
                    dst_filename = file_in_project
                    if not os.path.isfile(dst):
                        shutil.copy(scr, dst)
                        self.sc.good(dst_filename+" was created")
                    else:
                        same = self.compare_files(scr,dst)
                        if not same:
                            self.print("  [X] "+dst_filename+" was changed",'red')
                            self.display_changes(scr,dst)
                            if self.sc.question("Save changes?"):
                                shutil.copy(scr, dst)
                        else:
                            self.print("  [+] "+dst_filename+" no changes",'green')
        
        # save log
        logname = str(datetime.now())
        logname = logname.replace(":", "").replace("-", "").replace(".", "").replace(" ", "")
        file = open(self.logs_location+"/"+logname+".txt",'w')
        for line in self.log:
            file.write(line+"\n")
        os.popen(self.logs_location+"/"+logname+".txt")
        file.close()
        self.log = []

        # restart
        self.sc.restart()

    def compare_files(self, scr, dst):
        scr_lines = []
        dst_line = []

        # get scr file content
        try:
            scr_file = open(scr,'r')
            scr_lines = scr_file.readlines()
            scr_file.close()
        except:
            pass

        # get dst file content
        try:
            dst_line = open(dst,'r')
            dst_line = dst_line.readlines()
            dst_line.close()
        except:
            pass

        # compare
        return scr_lines == dst_line

    def display_changes(self, scr, dst):
        scr_lines = []
        dst_lines = []

        # get scr file content
        try:
            scr_file = open(scr,'r')
            scr_lines = scr_file.readlines()
            scr_file.close()
        except:
            pass

        # get dst file content
        try:
            dst_file = open(dst,'r')
            dst_lines = dst_file.readlines()
            dst_file.close()
        except:
            pass

        # display changes
        if len(scr_lines) > len(dst_lines):
            table_len = len(scr_lines)
        else:
            table_len = len(dst_lines)
        
        self.print("+------+---------------------------------------------+---------------------------------------------+","white")
        column = 45
        for i in range(table_len):
            try:
                scr_l = scr_lines[i][0:column]
                scr_l = scr_l.replace("\n","\\n")
                add = " "*(column-len(scr_l))
                scr_side = "|"+str(i+1).zfill(6)+"|"+scr_l+add
            except:
                scr_side = ""

            try:
                dst_l = dst_lines[i][0:column]
                dst_l = dst_l.replace("\n","\\n")
                dst_side = dst_l
            except:
                dst_side = ""
            
            try:
                if scr_lines[i] == dst_lines[i]:
                    color = "green"
                else:
                    color = "red"
            except:
                color = "red"
            self.print(scr_side+"|"+dst_side, color)
        self.print("+------+---------------------------------------------+---------------------------------------------+","white")

    def print(self, text, color):
        self.sc.print(text, color)
        self.log.append(text)
main()