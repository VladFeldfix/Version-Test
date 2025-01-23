# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *
import shutil
import datetime
from datetime import datetime

class main:
    # constructor
    def __init__(self):
        # load smart console
        self.sc = SmartConsole("Version-Test", "2.1")
        
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
        lof_path = self.logs_location+"/list_of_files.txt" # list of files
        lof_file = open(lof_path,'a',encoding='utf-8')
        lof_file.close()
        lof_file = open(lof_path,'r',encoding='utf-8')
        lof_lines = lof_file.readlines()
        lof_file.close()
        projects = []
        existing_files = []
        for root, dirs, files in os.walk(self.projects):
            for file in files:
                path = root+"/"+file
                if self.file_can_be_opened(path):
                    filename = path
                    filename = filename.replace(self.projects, "")
                    filename = filename.replace("\\", "/")
                    filename = filename.split("/")
                    if len(filename) > 2:
                        project = filename[1]
                        if not project in projects:
                            projects.append(project)
                            self.print("\n"+project+":","white")
                        file_in_project = "/".join(filename[2:])
                        file_in_project = file_in_project.replace("/", " + ")
                        existing_files.append(project+"/"+"/".join(filename[2:])+"\n")
                        
                        # create a copy of the projects in my tmp folder
                        if not os.path.isdir(self.backup+"/"+project):
                            os.makedirs(self.backup+"/"+project)
                        
                        # create a copy of the file in the backup folder
                        scr = path
                        dst = self.backup+"/"+project+"/"+file_in_project
                        dst_filename = file_in_project
                        if not os.path.isfile(dst):
                            shutil.copy(scr, dst)
                            self.print("  [+] "+dst_filename+" was created",'yellow')
                            lof_lines.append(project+"/"+"/".join(filename[2:])+"\n")
                        else:
                            same = self.compare_files(scr,dst)
                            if not same:
                                self.print("  [X] "+dst_filename+" was changed",'red')
                                self.display_changes(scr,dst)
                                #if self.sc.question("Save changes?"):
                                shutil.copy(scr, dst)
                            else:
                                self.print("  [+] "+dst_filename+" no changes",'green')

        # display deleted files
        self.print("",'white')
        self.print("DELETED FILES:",'white')
        none = " - None - "
        for file in lof_lines:
            if not file in existing_files:
                self.print(" "+file,'red')
                del lof_lines[lof_lines.index(file)]
                none = ""
        self.print(none,'white')

        # save lof
        lof_file = open(lof_path,'w',encoding='utf-8')
        for file in lof_lines:
            lof_file.write(file)
        lof_file.close()

        # save log
        self.save_log()

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
        self.sc.print("      +-+------+--------------------------------------------+--------------------------------------------+","white")
        column = 44
        for i in range(table_len):
            try:
                scr_l = scr_lines[i]
                scr_l = scr_l.replace("\n","").replace("\t"," ").replace("  "," ")
                scr_l = scr_l[0:column]
                scr_html_line = scr_lines[i]
                scr_html_line = scr_html_line.replace("\n","").replace("\t"," ").replace("  "," ")
                scr_html_line = scr_html_line[0:200]
                add = " "*(column-len(scr_l))
                scr_side = "|"+str(i+1).zfill(6)+"|"+scr_l+add
            except:
                scr_side = "|      |                                            "
                scr_html_line = ""
            try:
                dst_l = dst_lines[i]
                dst_l = dst_l.replace("\n","").replace("\t"," ").replace("  "," ")
                dst_l = dst_l[0:column]
                dst_html_line = dst_lines[i]
                dst_html_line = dst_html_line.replace("\n","").replace("\t"," ").replace("  "," ")
                dst_html_line = dst_html_line[0:200]
                add = " "*(column-len(dst_l))
                dst_side = dst_l+add
            except:
                dst_side = "                                            "
                dst_html_line = ""
            try:
                if scr_lines[i] == dst_lines[i]:
                    color = "green"
                    x = "+"
                else:
                    color = "red"
                    x = "-"
            except:
                color = "red"
                x = "-"
            text = "      |"+x+scr_side+"|"+dst_side+"|"
            self.sc.print(text, color)
            self.add_to_log_table(x,str(i+1),scr_html_line,dst_html_line,color)
        self.sc.print("      +-+------+--------------------------------------------+--------------------------------------------+","white")

    def print(self, text, color):
        self.sc.print(text, color)
        self.log.append((text,color,"TXT"))

    def add_to_log_table(self, x, line_number, scr, dst, color):
        self.log.append(((x, line_number, scr, dst),color,"TABLE"))#

    def save_log(self):
        # log name
        logname = str(datetime.now())
        logname = logname.replace(":", "").replace("-", "").replace(".", "").replace(" ", "")
        time = datetime.now()
        timestamp = time.strftime("%H:%M:%S")

        # write to html
        file = open(self.logs_location+"/"+logname+".html",'w',encoding="UTF-8")
        file.write("<html>\n")
        file.write("    <head>\n")
        file.write("        <style>\n")
        file.write("            body{\n")
        file.write("                background-color: #121212;\n")
        file.write("                font-family:'Courier New', Courier, monospace;\n")
        file.write("                color:white;\n")
        file.write("            }\n")
        file.write("            table{\n")
        file.write("                width: 100%;\n")
        file.write("                overflow-wrap: break-word;\n")
        file.write("            }\n")
        file.write("            table, tr, td{\n")
        file.write("                border-collapse: collapse;\n")
        file.write("                border: #636363 solid 1px;\n")
        file.write("            }\n")
        file.write("            td{\n")
        file.write("                max-width: 500px;\n")
        file.write("            }\n")
        file.write("            .white{\n")
        file.write("                color:white;\n")
        file.write("            }\n")
        file.write("            .red{\n")
        file.write("                color:red;\n")
        file.write("            }\n")
        file.write("            .green{\n")
        file.write("                color:green;\n")
        file.write("            }\n")
        file.write("            .yellow{\n")
        file.write("                color:yellow;\n")
        file.write("            }\n")
        file.write("            table,tr,td{\n")
        file.write("                color:yellow;\n")
        file.write("            }\n")
        file.write("        </style>\n")
        file.write("    </head>\n")
        file.write("    <body>\n")
        file.write("        <h1>VERSION TEST</h1>\n")
        file.write("        <text>TIMESTAMP: "+self.sc.today()+" "+timestamp+"</text><br>\n")
        file.write("        <text>PROJECTS LOCATION: "+self.projects+"</text><br>\n")
        file.write("        <text>BACKUPS LOCATION: "+self.backup+"</text><br>\n")
        file.write("        <text>GENERATED WITH: Version-Test v2.0</text><br>\n")
        
        table = False
        for line in self.log:
            text = line[0]
            color = line[1]
            txt_type = line[2]
            if txt_type == "TXT":
                text = self.clean_html_text(text)
                if table:
                    file.write("        </table>\n")
                    table = False
                file.write("        <text class='"+color+"'>"+text+"</text><br>\n")
            elif txt_type == "TABLE":
                if not table:
                    table = True
                    file.write("        <table>\n")
                file.write("        <tr>\n")
                file.write("            <td class='"+color+"'>"+self.clean_html_text(text[0])+"</td>\n")
                file.write("            <td class='"+color+"'>"+self.clean_html_text(text[1])+"</td>\n")
                file.write("            <td class='"+color+"'>"+self.clean_html_text(text[2])+"</td>\n")
                file.write("            <td class='"+color+"'>"+self.clean_html_text(text[3])+"</td>\n")
                file.write("        </tr>\n")
        file.write("        <text class='white'>---------------------------------------------------------------------------------------------------</text><br>\n")
        file.write("    </body>\n")
        file.write("</html>\n")
        file.close()

        # open html
        os.popen(self.logs_location+"/"+logname+".html") 

        # empty log
        self.log = []
    
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
    
    def clean_html_text(self, text):
        return text.replace("<","&nbsp").replace(">","&nbsp").replace("\n","<br>").replace(" ","&nbsp").replace("\t","&nbsp")

main()