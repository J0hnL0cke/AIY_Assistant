Assistant built for the Google Voice AIY that can understand and respond to user voice queries.


**Features:**
- Hotword detection
- Speech recognition
- Text-to-speech
- Persistent memory between sessions
- Changing button LED colors
- Ability to change device volume
- Ability to store queries that are not understood
- Ability to give device IP address

More features, such as ability to play music and record audio on demand, are planned for the future

This program is built for the Google AIY Voice Kit. It may not work on other devices.


**Downloading:**

Run `git clone https://github.com/J0hnL0cke/AIY_Assistant.git` or download it.

It shouldn't matter where you download it.

I used ~/AIY-projects-python/src/aiy/recognizer because that's where most of the modules I needed were


**Dependencies:**

Install all necessary dependencies with apt and pip. Modules that are needed have been included.

If you get an error installing with pip, then try running the commands with pip3 instead.

`sudo apt-get install python-pyaudio python3-pyaudio sox`

`pip install pyaudio`

`pip install pyttsx3`

`pip install speech_recognition`


**Configure the project**

You will need an account on [Houndify](houndify.com) to use speech recognition.

Create a project and save the project and client ID keys for later.

Next, head over to the [Snowboy Dashboard](https://snowboy.kitt.ai/dashboard).

You can train a custom voice model or use a universal model.

You will need to download the .pmdl/.umdl file onto the device. 


**First run:**

 `cd` into the repository if not already in it
 
 run `python3 main.py`

 You will immediately run into errors because your configuration files are not set up.
 
 Luckily, you just created them.
 
 `cd data/`
 
 Now you need to change 2 files using your editor of choice:
 
 Open houndify.txt and paste in your ids. Line 1 should be ProjectID and line 2 should be ClientID.
 
 Open path_to_voice_model.txt and paste in the path to your voice model. I suggest putting it in the top folder of the repo.
 
 The path can be relative to the main.py file, such as "./model.pmdl", or abslolute, like "/~/AIY-projects-python/src/aiy/recognizer/model.pmdl"
 
 Now go back to the top level of the repo and run `python3 main.py` again.
 
 You should be good to go. If you have an issue, report it [here](https://github.com/J0hnL0cke/AIY_Assistant/issues/new)
 
 
 **Contribute**
 
 Want to help?
 
 Leave a pull request for features that should be added.
 
 Additional commands that should be added are also welcome.
