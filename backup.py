import os

class files:
    @classmethod
    def write_file(cls,file,info):
        with open(file, "w+") as data:
            data.write(info)
    
    @classmethod
    def load_file(cls,file,strip_lines):
        contents=""
        with open(file) as data:
            for each_line in data:
                try:
                    if strip_lines:
                        line=each_line.strip()
                    else:
                        line=each_line
                    contents+=line
                except IOError:
                    print("File not found")
                    raise
        return contents
        
class ask:
    
    @classmethod
    def yesOrNo(cls,text):
        while True:
            #Loop until y or n is chosen
            build=str(text)+" (y/n) >"
            ans=cls._get_input(build).lower()
            if ans=="y":
                return True
            elif ans=="n":
                return False
            else:
                print("Not a valid option.")
                
    @classmethod
    def customMultiChoice(cls,text,ch1,ch2):
        while True:
            #Loop until y or n is chosen
            build=str(text)+" ("+ch1+"/"+ch2+") >"
            ans=cls._get_input(build).lower()
            if ans==ch1:
                return 1
            elif ans==ch2:
                return 2
            else:
                print("Not a valid option.")
    
    @classmethod
    def getPath(cls,text,acceptEmpty=True):
        build=str(text)+"\n>"
        while True:
            ans=cls._get_input(build)
            if acceptEmpty and ans=="":
                return ""
            if os.path.exists(ans) and os.path.isdir(ans):
                return ans
            else:
                if cls.yesOrNo("This directory does not exist. Create it?"):
                    os.mkdir(ans)
    
    @classmethod
    def getFile(cls,text,acceptEmpty=True):
        build=str(text)+"\n>"
        while True:
            ans=cls._get_input(build)
            if acceptEmpty and ans=="":
                return ""
            if os.path.exists(ans) and os.path.isfile(ans):
                return ans
            else:
                print("Not a valid file.")
    
    @classmethod
    def get(cls,text,acceptEmpty=True):
        build=str(text)+" >"
        while True:
            ans=cls._get_input(build)
            if not ans=="":
                return ans
            elif acceptEmpty:
                return ans
            else:
                print("Please enter an answer.")

    @classmethod
    def _get_input(cls,question):
        try:
            return input(question)
        except KeyboardInterrupt:
            print("\nInterrupted, build process canceled.")
            exit()


action=ask.customMultiChoice("Do you wish to create a backup or load a backup?","create","load")
if action==2:
    conf_file="config backup file"
else:
    conf_file="config file"
    
check_path=True
while check_path:
    current_dir=os.getcwd()
    print("\nCurrent directory is", current_dir)
    if not ask.yesOrNo("Is this where your "+conf_file+" is located?"):
        path=ask.getPath("Enter a relative or absolute path to the directory where your "+conf_file+" is located.",False)
        try:
            os.chdir(path)
        except:
            print("Not a valid path")
    else:
        check_path=False

if ask.yesOrNo("Is your "+conf_file+" named config.bespon?"):
    f="config.bespon"
else:
    f=""

get_config=True
while get_config:
    if f!="":
        if os.path.exists(f) and os.path.isfile(f):
            print("Found "+conf_file+":", f)
            get_config=False
            
    if get_config:
        if f!="":
            print("Could not find",conf_file)
        f=ask.getFile("Enter name of your "+conf_file,False)
        
        
            
if action==1:
            
    if ask.yesOrNo("Backup config file to ../saves ?"):
        loc="../saves"
        if not os.path.exists(loc):
            print("Location does not exist, creating.")
            os.mkdir(loc)
    else:
        if ask.yesOrNo("Backup config file to parent directory?"):
            loc=".."
        else:
            loc=ask.getPath("Enter location to save config files to")
            
    if os.path.exists(loc) and os.path.isdir(loc):
        pass
    else:
        loc=ask.getPath("Enter location to save config files to")
        
    print("Ready to backup. Your config file will be saved to",loc)
    
    if ask.yesOrNo("Back up data?"):
        info=files.load_file(f,False)
        files.write_file(loc+"/"+f,info)
    else:
        print("Backup canceled")
    
else:
    loc=ask.getPath("Enter location to load config files to")
    print("Ready to load files. Your "+conf_file+" will be loaded to",loc)
    
    if ask.yesOrNo("Load config data?"):
        info=files.load_file(f,False)
        files.write_file(loc+"/"+f,info)
    else:
        print("Load canceled")
