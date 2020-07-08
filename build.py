
#Build file to simplify install of recognizer

import os

def write(file,info):
    with open(file, "w+") as data:
        data.write(info)

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
    def getPath(cls,text,acceptEmpty=True):
        build=str(text)+"\n>"
        while True:
            ans=cls._get_input(build)
            if acceptEmpty and ans=="":
                return ""
            if os.path.exists(ans) and os.path.isdir(ans):
                return ans
            else:
                print("Not a valid directory.")
    
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

#Get the path to install to
check_path=True
while check_path:
    current_dir=os.getcwd()
    
    print("\nCurrent directory is", current_dir)
    if not ask.yesOrNo("Install here?"):
        path=ask.getPath("Enter a relative or absolute path to install to.",False)
        try:
            os.chdir(path)
        except:
            print("Not a valid path")
    else:
        check_path=False

#Get API keys
if ask.yesOrNo("\nDo you have Houndify API keys?"):
    client_id=ask.get("Enter Client ID")
    client_key=ask.get("Enter Client Key")
else:
    client_id=""
    client_key=""

client_info=client_id+"\n"+client_key

#Get path to voice model
if ask.yesOrNo("\nDo you have a path to your Snowboy voice model?"):
    model_path=ask.getFile("Enter path to voice model")
else:
    model_path=""

#Check missing
missing=False
print("")
if client_id=="" or client_key=="":
    print("It appears you do not have a Houndify ID. Because of this, you won't be able to use Houndify voice recongition.")
    missing=True
    
if model_path=="":
    print("It appears you do not have a Snowboy voice model. Because of this, you won't be able to use Snowboy wake word detection.")
    missing=True

#Make directories
print("\nFinished questions.")
if ask.yesOrNo("Run build script?"):
    needed_dirs=["data","music"]
    for name in needed_dirs:
        try:
            os.mkdir(name)
        except FileExistsError:
            print("Could not create directory",name+": Directory already exists")
        
    #Make needed files
    write("data/houndify.txt",client_info)
    write("data/path_to_voice_model.txt",model_path)
    
    print("\nFinished writing files.\nIf you didn't have one or more of the items required to complete the build process, you can always run it again later.")
    print("Don't forget to install dependencies listed in the README if you haven't already.")
else:
    print("Operation canceled")
