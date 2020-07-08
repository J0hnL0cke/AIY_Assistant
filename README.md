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
- Ability to stream or download and play audio from YouTube

More features, such as ability to play music and record audio on demand, are planned for the future

This program is built for the Google AIY Voice Kit. It may not work on other devices.


**Downloading:**

Run `git clone https://github.com/J0hnL0cke/AIY_Assistant.git` or download it.

It shouldn't matter where you download it.

I used ~/AIY-projects-python/src/aiy/recognizer because that's where most of the modules I needed were


**Dependencies:**

Install all necessary dependencies with apt and pip. Modules that are needed have been included.

If you get an error installing with pip3, then try running the commands using pip instead.

`sudo apt-get install python-pyaudio python3-pyaudio sox`

`sudo apt-get install libatlas-base-dev`

`sudo apt-get install espeak`

`sudo -H pip3 install --upgrade youtube-dl`

`pip3 install pyaudio`

`pip3 install pyttsx3`

`pip3 install speechrecognition`

`pip3 install python-vlc`

**Configure the project**

You will need an account on [Houndify](houndify.com) to use speech recognition.

Create a project and save the project and client ID keys for later.

Next, head over to the [Snowboy Dashboard](https://snowboy.kitt.ai/dashboard).

You can train a custom voice model or use a universal model.

You will need to download the .pmdl/.umdl file onto the device.

Now run the build.py file and follow the instructions.

When you are asked to enter a path to install to, you can use a relative path like "./files", or an absolute path, like "/~/AIY-projects-python/src/aiy/recognizer/files"

When you are asked to enter a path to your Snowboy model, you can use a relative path from the main.py file, such as "./model.pmdl", or an abslolute path, like "/~/AIY-projects-python/src/aiy/recognizer/model.pmdl"

**First run:**

`cd` into the repository if not already in it

run `python3 main.py`

You should be good to go. If you have an issue, report it [here](https://github.com/J0hnL0cke/AIY_Assistant/issues/new)


**Contribute**

Want to help?

Leave a pull request for features that should be added.

Additional commands that should be added are also welcome.
