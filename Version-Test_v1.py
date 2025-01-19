# Download SmartConsole.py from: https://github.com/VladFeldfix/Smart-Console/blob/main/SmartConsole.py
from SmartConsole import *
import os
from string import printable

class main:
    # constructor
    def __init__(self):
        # load smart console
        self.sc = SmartConsole("Version-Test", "1.0")
        
        # set-up main memu
        self.sc.add_main_menu_item("RUN", self.run)

        # display main menu
        try:
            self.sc.start()
        except Exception as e:
            self.sc.fatal_error(str(e))
    
    def run(self):
        # setup database
        db = {}
        self.log = []
        self.errors = 0
        # get two folders
        foler1 = self.sc.input("Insert Folder 1")
        foler1 = foler1.replace("\\","/")
        foler2 = self.sc.input("Insert Folder 2")
        foler2 = foler2.replace("\\","/")

        # test location
        self.sc.test_path(foler1)
        self.sc.test_path(foler2)

        # get format
        formatt = self.sc.input("Insert format [for example: txt, csv, ini]")
        options = ("path from root/filename.format","filename.format")
        fullpath = self.sc.choose("How to compare files?", options)

        # get file content from folder 1
        self.log_print("",'white')
        self.log_print("Gathering data...",'white')
        for root, dirs, files in os.walk(foler1):
            root = root.replace("\\", "/")
            for file in files:
                if formatt in file:
                    # get file name
                    if fullpath == options[0]:
                        fullfilename = root+"/"+file
                        fullfilename = fullfilename.replace(foler1+"/", "")
                    else:
                        fullfilename = file
                    
                    # read file
                    try:
                        f = open(root+"/"+file,'r',encoding="UTF-8")
                        if not fullfilename in db:
                            db[fullfilename] = f.readlines()
                            self.log_good("File "+fullfilename+" added to the database")
                        else:
                            self.log_error("The filename "+fullfilename+" is not unique and cannot be inserted into the database")
                        f.close()
                    except Exception as e:
                        self.log_error("Filename: "+root+"/"+file+" "+str(e))
        
        # scan folder 2
        self.log_print("",'white')
        self.log_print("Comparing data...",'white')
        for root, dirs, files in os.walk(foler2):
            root = root.replace("\\", "/")
            for file in files:
                if formatt in file:
                    # get file name
                    if fullpath == options[0]:
                        fullfilename = root+"/"+file
                        fullfilename = fullfilename.replace(foler2+"/", "")
                    else:
                        fullfilename = file

                    # find it in database
                    if not fullfilename in db:
                        self.log_error("The filename "+fullfilename+" is not in the database")
                    else:
                        # compare lines
                        try:
                            f = open(root+"/"+file,'r',encoding="UTF-8")
                            lines = f.readlines()
                            f.close()
                        except Exception as e:
                            self.log_error("Filename: "+root+"/"+file+" "+str(e))
                        src = db[fullfilename]
                        ln = 0
                        self.log_print("",'white')
                        self.log_print("Filename: "+fullfilename,'white')
                        for line in lines:
                            ln += 1
                            if len(src) >= ln:
                                line1 = self.show_as_table(line)
                                line2 = self.show_as_table(src[ln-1])
                                if line != src[ln-1]:
                                    self.log_print("[-] #"+str(ln).zfill(5)+". "+line1+" | "+line2,"red")
                                else:
                                    self.log_print("[+] #"+str(ln).zfill(5)+". "+line1+" | "+line2,"green")
        self.save_log()
        self.sc.restart()
    
    def show_as_table(self, data):
        table_len = 50
        result = data.replace("\n", "")
        result = result.replace("\t", " ")
        result = re.sub("[^{}]+".format(printable), "", result)
        result = result[:table_len]
        while len(result) != table_len:
            result += " "
        return result
    
    def log_print(self, text, color):
        self.sc.print(text, color)
        self.log.append(text)
        if color == "red":
            self.errors += 1
    
    def log_good(self, text):
        self.sc.good(text)
        self.log.append(text)

    def log_error(self, text):
        self.errors += 1
        self.sc.error(text)
        self.log.append("[X] "+text)
    
    def save_log(self):
        file = open("log.txt", "w", encoding="utf-8")
        for line in self.log:
            file.write(line+"\n")
        file.write("Found: "+str(self.errors)+" errors (search for [-] or [X] to see them)")
        file.close()
        os.popen("log.txt")
main()