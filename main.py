#Import statements at bottom of file

def tab(text, tabs=1):
    print('\t'*tabs+text)

def say_importing(text,tabs=1):
    text='Importing '+text+'...'
    tab(text, tabs)

def imp(package_name,**kwargs):
    
    say_importing(package_name,kwargs.get('tabs',1))
    
    if kwargs.get('real',True):
        if kwargs.get('pkg','')=='':
            return importlib.import_module(package_name)
        else:
            return importlib.import_module(package_name,kwargs.get('pkg',''))

class speak:
    @classmethod
    def init(cls):
        tab('Initalizing voice...')
        cls.engine = tts.init()
        
        #Should customize voice properties
        
    @classmethod
    def say(cls, *args):
        build=''
        for text in args:
            if not len(build)==0:
                build+=' '
            build+=str(text)
        print('Speaking "'+build+'"')
        cls.engine.say(build)
        cls.engine.runAndWait()

class lights:
    
    led_inst=None
    current_color=None
    
    @classmethod
    def _get_led_inst(cls):
        try:
            cls.led_inst=leds.Leds()
        except:
            #Creating an instance of Leds() sometimes fails when running program at boot.
            #If an instance hasn't been created, try to create one when changing the led color.
            #This should provide some delay to allow the Leds() package to initialize.
            
            cls.led_inst=None
            print("Error: couldn't initalize leds")
    
    @classmethod
    def init(cls):
        #Have to set this after importing aiy.leds, cannot go in class body
        cls.colors=['off', leds.Color.CYAN, leds.Color.WHITE, leds.Color.PURPLE, leds.Color.YELLOW, leds.Color.BLUE, leds.Color.GREEN, Color.RED]
        cls.names=['off', 'cyan', 'white', 'purple', 'yellow', 'blue', 'green', 'red']
        
        tab('Initalizing status light...')
        #cls.status_ui=aiy.voicehat.get_status_ui()
        #TODO: keep or remove?
        tab('Setting status...', 2)
        cls.status_change('starting')
        tab('Initalizing leds...')
        cls._get_led_inst()
        tab('Setting LED...', 2)
        cls.button_change('purple')
    
    @classmethod
    def status_change(cls, info):
        print('Status light=', info)
        #cls.status_ui.status(info)
    
    @classmethod
    def button_change(cls, c):
        #Try to initalize if instance doesn't exist
        if cls.led_inst is None:
            cls._get_led_inst()
        
        #If instance exists
        if cls.led_inst is not None:
            print('Changing LED color to', c)
            color=cls.colors[cls.names.index(c)]
            
            if color==cls.current_color:
                print("led is already set to", color)
            elif color=='off':
                cls.led_inst.update(leds.Leds.rgb_off())
            else:
                cls.led_inst.update(leds.Leds.rgb_on(color))
            cls.current_color=color
            print('led:',color)
        else:
            print("Cannot change led color: Leds() not yet initalized.")
        
    @classmethod
    def reset_led(cls):
        #Turn off leds before the program exits so they are not left on
        if not cls.led_inst is None:
            print('Resetting led')
            try:
                cls.button_change('off')
                #Delete the associated variables for Leds() instance and aiy.leds package respectively
                #IDK if this actually helps anything
                del cls.led_inst
                #This throws error for some reason
                #del leds
            except:
                print("When resetting led, another error ocurred:")
                raise

class files:
    
    #This is relative to the path that is changed at the beginning of the program
    data_loc='data/'
    
    @classmethod
    def init(cls):
        tab('Initalizing files...')
        tab('Loading playlist...', 2)
        cls.playlist=cls.load_file('playlist', '')
        if type(cls.playlist)!=list:
            cls.playlist=[]
        tab('Playlist has '+str(len(cls.playlist))+' items.', 2)
        tab('Loading name...', 2)
        cls.name=cls.load_file('name', 'human')
        tab('Name is '+str(cls.name), 2)
        tab('Loading location...', 2)
        cls.location=cls.load_file('location', 'Null Island')
        tab('Location is '+cls.location, 2)
    
    @classmethod
    def _nofile(cls, file, contents, use_default=True):
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        print('Data file', loc+file+'.txt', 'missing, creating...')
        cls.write_file(file, contents, use_default)
    
    @classmethod
    def write_file(cls, file, info, use_default=True):
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        with open(loc+file+'.txt', "w+") as data:
            data.write(info)
            print('Wrote "'+str(info)+'" to', loc+file+'.txt')
    
    @classmethod
    def load_file(cls, file, not_found='', use_default=True):
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        try:
            contents=[]
            with open(loc+file+'.txt') as data:
                for each_line in data:
                    try:
                        line=each_line.strip()
                        if line!='':
                            contents.append(line)
                    except ValueError:
                        pass
        except IOError:
            cls._nofile(file, not_found, use_default)
            contents=not_found
        if len(contents)==1:
            contents=contents[0]
        return contents
    
    @classmethod
    def append_file(cls, file, info, use_default=True):
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        try:
            with open(loc+file+'.txt', "a") as data:
                data.write('\n'+str(info))
                print('Appended "'+str(info)+'" to', loc+file+'.txt')
        except IOError:
            cls._nofile(file, info, use_default)

    @classmethod
    def item_exists(cls, name, use_default=True):
        #returns true if a file or directory with the given name exists
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        return os.path.exists(loc+name)
        
    @classmethod
    def file_exists(cls, name, use_default=True):
        if not cls.item_exists(name, use_default):
            return False
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        return os.path.isfile(loc+name)
        
    @classmethod
    def dir_exists(cls, name, use_default=True):
        if not cls.item_exists(name, use_default):
            return False
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        return os.path.isdir(loc+name)

class volume:
    @classmethod
    def init(cls):
        tab('Loading volume...')
        tab('Getting current volume...', 2)
        cls.volume=cls._get()
        tab('Volume is set to '+str(cls.volume))
    
    @classmethod
    def change(cls, vol):
        subprocess.call('amixer -q set Master %d%%' % vol, shell=True)
        speak.say('Volume at'+str(vol))
        print('Volume set to', vol)
        cls.volume=vol
    
    @classmethod
    def _get(cls):
        #res=subprocess.check_output(r'amixer get Master | grep "Front Left:" | sed "s/.*\[\([0-9]\+\)%\].*/\1/"', shell=True).strip()
        res=5
        return int(res)
    
    @classmethod
    def move(ammount):
        #raise or lower the volume by the given ammount
        cls.change(cls.volume+ammount)

class music:
    
    has_music=False
    playing=False
    is_playlist=False
    last_song=''
    playlist_item=0
    
    #Save files to the ./music/ directory to enable faster playback. Set to false to disable saving.
    save_files=True
    #Convert files that are saved to mp3 format. Does nothing if file saving is disabled.
    convert_to_mp3=True
    
    @classmethod
    def init(cls):
        tab('Loading music...')
        
        tab('Loading Youtube_DL', 2)
        #Set Youtube DL options
        cls.ydl_opts={
            'default_search': 'ytsearch1:',
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': False, #Quiet is false, should show info when loading songs
            'ignore-errors': True,
            'restrict-filenames': True,
        }
        
        if cls.save_files and cls.convert_to_mp3:
            #This section saves the file as an .mp3.
            cls.ydl_saving={'audio-format': 'mp3',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            cls.ydl_opts.update(cls.ydl_saving)
        
        #Make a list of characters that can be said by the tts program
        #Prevents it from saying words like "opening parenthesis"
        cls.title_chars=list(string.ascii_letters)+list(range(0,9))+[' ']
        
        cls._load_dicts()
        
        tab('Loading VLC...', 2)
        cls.vlc_instance=vlc.get_default_instance()
        
        #create a playlist?
        #cls.vlc_playlist=cls.vlc.media_list_new()
        #cls.vlc_player=cls.vlc_instance.media_list_player_new()
        
        cls.vlc_player=cls.vlc_instance.media_player_new()
        
        cls.vlc_event_manager=cls.vlc_player.event_manager()
        cls.vlc_event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, cls._song_finished, 1)
    
    @classmethod
    def find_music(cls,search_term):
        can_play=True
        keyboard_int=False
        print("Searching for song...")
        song_id=cls._get_id_from_term(search_term)
        
        if song_id is None:
            tab("Not sure what song you meant. Searching Youtube...")
            speak.say("Searching for "+search_term)
            #Song isn't indexed, search YT
            try:
                with youtube_dl.YoutubeDL(cls.ydl_opts) as ydl:
                    meta=ydl.extract_info(search_term, download=False)
                    
            except KeyboardInterrupt:
                keyboard_int=True
                
            except Exception:
                #Error when song doesn't exist
                meta=None
                
            if meta is None:
                #Song doesn't exist
                can_play=False
                
            else if not keyboard_int:
                meta=meta['entries'][0]
                #Song exists but search term not known
                song_id=meta["id"]
                song_url = meta["url"]
                song_title= meta["title"]
                print("Found song:", song_title)
                
                title=cls._get_title_from_id(song_id)
                
                if title is None or not cls.file_exists('music/'+song_url+'.mp3'):
                    #Song exists but is not saved locally
                    if cls.save_files:
                        print("Song not downloaded, downloading...")
                        speak.say("Downloading "+cls.cleanup_title(song_title))
                        try:
                            cls.download_music(song_url,song_id)
                            print("Finished downloading.")
                            #Index title
                        title=song_title
                        cls.song_ids[song_id]=song_title
                        except KeyboardInterruption:
                            keyboard_int=True
                        
                    else:
                        print("Song not downloaded. Save_files is set to False.")
                        print("Streaming song...")
                        cls._stream_music(song_url)
                
                if not keyboard_int:
                    #Index the search term
                    cls.song_terms[search_term]=song_id
                    #Save dicts to file
                    cls._save_dicts()
                
        else:
            title=cls._get_title_from_id(song_id)
            print("Found song:", title)
            
        if can_play and not keyboard_int:
            print("Playing song...")
            cls.playing=True
            cls.has_music=True
            build_song=' '.join(['Playing', cls.cleanup_title(title)])
            print(build_song)
            cls.last_song=title
            speak.say(build_song)
            try:
                cls._play_from_file(song_id)
                cls.vlc_player.play()
            
            except KeyboardInterrupt:
                keyboard_int=True
            
            except:
                print(sys.exc_info()[0])
                speak.say('Sorry, there was an error')
                cls.has_music=False
                cls.playing=False
            
        else if not keyboard_int:
            print("Can't find", name)
            speak.say("Sorry, I can't find", search_term)
            
        if keyboard_int:
            print("Keyboard interruption detected, song operation canceled.")
        
    @classmethod
    def _get_id_from_term(cls, term):
        return cls.song_terms.get(term)
        
    @classmethod
    def _get_title_from_id(cls, song_id):
        return cls.song_terms.get(song_id)
        
    @classmethod
    def _save_dicts(cls):
        files.write_file('song_ids',str(cls.song_ids))
        files.write_file('song_terms',str(cls.song_terms))
        
    @classmethod
    def _load_dicts(cls):
        error=False
        try:
            cls.song_ids=ast.literal_eval(files.load_file('song_ids',"{}"))
        except:
            cls.song_ids={}
            error=True
        try:
            cls.song_terms=ast.literal_eval(files.load_file('song_terms',"{}"))
        except:
            cls.song_terms={}
            error=True
            
        if error:
            cls._save_dicts()
        
    @classmethod
    def download_music(cls, url, song_name):
        opts=cls.ydl_opts
        opts['outtmpl']='music/{0}.%(ext)s'.format(song_name)
        #download with output as the id
        try:
            with youtube_dl.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except:
          print("Error downloading song:", sys.exc_info()[0])
        
    @classmethod
    def _stream_music(cls, url):
        #todo: implement this
        cls.vlc_player.set_media(cls.vlc_instance.media_new(url))
    
    @classmethod
    def _play_from_file(cls, music_file):
        #todo: check if this works
        cls.vlc_player.set_media(cls.vlc_instance.media_new("music/"+music_file+".mp3"))
        
    @classmethod
    def cleanup_title(cls,title):
        build=''
        for character in title:
            if character in cls.title_chars:
                build+=character
        return build.replace("  "," ")
    
    @classmethod
    def play_multiple(cls, reset=False):
        print('Loading the song')
        if reset:
            cls.playlist_item=0
            cls.is_playlist=True
        else:
            cls.playlist_item+=1
            
        next_song=files.playlist[cls.playlist_item]
        print('Next song is', next_song)
        time.sleep(2)
        cls.find_music(next_song)
    
    @classmethod
    def _song_finished(cls, data):
        print('Song over')
        print('Playlist:', cls.is_playlist)
        if cls.is_playlist==True:
            if cls.playlist_item==len(playlist):
                print('Playlist finished')
            else:
                print('Song finished.')
                cls.play_multiple()
    
    @classmethod
    def pause(cls, paused=True):
        cls.vlc_player.set_pause(paused)
    
class btn:
    
    @classmethod
    def init(cls):
        tab('Initalizing button...')
        cls.board=aiy_board.Board()
        cls.event_was_set=False
    
    @classmethod
    def wait(cls):
        cls.board.button.wait_for_press()
        
    @classmethod
    def set_event(cls):
        cls.done = threading.Event()
        cls.board.button.when_pressed=cls.done.set
        cls.event_was_set=True
        print("Set up button pressed event")
        
    @classmethod
    def was_pressed(cls):
        assert cls.event_was_set
        return cls.done.is_set()
   
class record:

    callback=None

    @classmethod
    def init(cls,fname='recording.wav'):
        cls.filename=fname
        tab("Setting up args...")
        parser = argparse.ArgumentParser()
        parser.add_argument('--filename', '-f', default=cls.filename)
        cls.args = parser.parse_args()
    
    @classmethod
    def new(cls):
        btn.set_event()
        print("Recording started, press button to stop recording")
        record_file(AudioFormat.CD, filename=cls.args.filename, wait=cls.interval, filetype='wav')
        print("Recording stopped")
        return cls.filename
    
    @classmethod
    def interval(cls):
        if cls.callback==None:
            cls.default_cb()
        else:
            cls.callback()
        
    @classmethod
    def default_cb(cls):
        start = time.monotonic()
        duration=0
        finished=False
        while not finished:
            if btn.was_pressed() or duration > 5:
                finished=True
            else:
                duration = time.monotonic() - start
                print('Recording: %.02f seconds [Press button to stop]' % duration)
                time.sleep(0.5)

class recognize:
    
    #Speech-to-text
    
    @classmethod
    def init(cls,fname='houndify'):
        tab('Loading Houndify credentials from file...')
        file_data=files.load_file(fname, '') #credential location, should be stored as 2 lines: client ID and client key
        assert file_data!='' #Credentials file is missing or empty
        cls.HOUNDIFY_CLIENT_ID = file_data[0].replace("\n","") # Houndify client IDs are Base64-encoded strings
        cls.HOUNDIFY_CLIENT_KEY = file_data[1].replace("\n","") # Houndify client keys are Base64-encoded strings
        
    
    @classmethod
    def main(cls):
        
        #Record what the user said
        file_name=record.new()
        lights.button_change('cyan')
        print("Interpreting speech...")
        
        #Get path to the audio file and load it
        audio=cls.parse_audio(file_name)
        
        #Send the audio file to Houndify for recognition, return text
        text=cls.get_text(audio)
        
        #return the text that the user said so it can be interpreted
        return text
    
    @classmethod
    def parse_audio(cls,fname):
        # obtain path to the given file in the same folder as this script
        AUDIO_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), fname)
        
        # use the audio file as the audio source
        #Create a new recognizer instance
        cls.r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = cls.r.record(source)  # read the entire audio file
        return audio
        
    @classmethod
    def get_text(cls,audio):
        # recognize speech using Houndify
        resp=None
        try:
            resp=cls.r.recognize_houndify(audio, client_id=cls.HOUNDIFY_CLIENT_ID, client_key=cls.HOUNDIFY_CLIENT_KEY)
            print("Result: client said", resp)
        except sr.UnknownValueError:
            print("Houndify could not understand audio")
        except sr.RequestError as e:
            speak.say("Sorry, I cannot connect to the speech recognition service. Please try again later.")
            print("Could not request results from Houndify service; {0}".format(e))
            
        return resp

class hotword:
    
    started=False
    detected=False
    
    @classmethod
    def init(cls):
        cls.detector_thread = threading.Thread(target=cls.start, daemon=True)
        cls.detector_thread.start()
        
    @classmethod
    def start(cls):
        cls.started=True
        print("Starting detector")
        cls.detector = snowboy.HotwordDetector(files.load_file('path_to_voice_model', './model.pmdl'), sensitivity=0.4, audio_gain=1)
        try:
            cls.detector.start(cls.detected_callback)
        except:
            print('Error starting detector')
        print("Detector running")

    @classmethod
    def reset_detector(cls):
        print("Detector trigger has been reset")
        cls.detected=False

    @classmethod
    def detected_callback(cls):
        print("Hotword detected")
        cls.detected=True
        
    @classmethod
    def was_said(cls):
        return cls.detected
    
class trigger:
    
    #Waits for a trigger from the user
    #Stops when the user presses the button or speaks the hotword
    
    def wait():
        hotword.reset_detector()
        btn.set_event()
        
        looping=True
        print('looping, started =',hotword.started)
        
        while looping:
            if hotword.was_said() or btn.was_pressed():
                print('Exiting loop')
                looping=False
            else:
                time.sleep(0.5)

class main_thread:
    
    initialized=False
    keep_running=True
    
    @classmethod
    def init(cls):
        
        print('Initalizing main...')
        
        #Set class variables that will be used to recognize the intent of a speaker
        
        cls.greeting=['good morining', 'hello', 'good afternoon', 'hi', 'hey', 'hey there', 'hi there', 'hello there']
        cls.replay=['replay', 'start over', 'restart the song', 'start the song over']
        cls.names=['one hundred', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty', 'fourty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
        cls.numbers=[100, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 40, 50, 60, 70, 80, 90]
        cls.current_weather=['sunny', 'cloudy', 'stormy', 'foggy', 'snowing', 'sleeting', 'hailing', 'windy', 'humid']
        cls.future_weather=['rain', 'thunder and lightning', 'clouds', 'increased humidity', 'high winds', 'fog', 'storms', 'hail', 'sleet', 'tornado', 'snow', 'solar flare', 'tsunami', 'zombie apocalypse', 'raining tacos', 'wildfire', 'avalanche', 'sand storms', 'drought']
        
        #Initalize packages that have been imported
        
        #lights.init() #This is called right after importing leds
        speak.init()
        files.init()
        volume.init()
        music.init()
        btn.init()
        recognize.init()
        record.init()
        hotword.init()
        
        #Set initialized flag, allowing main.run() to be called without error
        cls.initialized=True
    
    @classmethod
    def run(cls):
        
        #Packages must have been imported and initalized before use, return an error otherwise
        assert cls.initialized
        
        print('Ready!')
        lights.button_change('green')
        speak.say('Hello')
        
        #separate function/class?
        while cls.keep_running:
            lights.status_change('ready')
            lights.button_change('green')
            print('Press the button or say the hotword')
            
            trigger.wait()
            
            if music.playing:
                print('Pausing song for button press')
                music.pause()
            
            lights.status_change('listening')
            lights.button_change('yellow')
            print('Listening...')
            
            text=recognize.main()
            
            print('You said "'+str(text)+'".')
            lights.button_change('blue')
            lights.status_change('thinking')
            
            if len(str(text))==0:
                #Nothing was heard
                speak.say("Sorry, I didn't hear you.")
                print("I didn't hear you. Please press the button and try again.")
            elif text is None:
                print("Nothing to recognize")
            else:
                main_thread.recognize(text.lower())
    
    @classmethod
    def starts(cls, text, beginning):
        #Could also be a static method, does not need cls param
        #Easier to leave as-is
        return text.startswith(beginning)
    
    @classmethod
    def recognize(cls, text):
        #Interpret what the person said
        
        if text=='power off' or text=='shut down':
            #assistant.stop_conversation()
            lights.status_change('stopping')
            speak.say('Good bye!')
            lights.reset_led()
            subprocess.call('sudo shutdown now', shell=True)
        
        elif text=='reboot' or text=='restart':
            speak.say('See you in a bit!')
            lights.reset_led()
            subprocess.call('sudo reboot', shell=True)
            
        elif text=='close program' or text=='stop program' or text=='stop recongizer' or text=='stop recognizer':
            speak.say('Goodbye for now.')
            print("Closing program...")
            cls.keep_running=False
        
        elif text=='ip address':
            #assistant.stop_conversation()
            ip_address=str(subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True))
            speak.say("Your IP is", ip_address.replace('\n',''))
        
        elif text=='never mind' or text=='nevermind':
            speak.say('Canceling')
        
        elif text in cls.greeting:
            greeting=random.choice(cls.greeting)
            greeting=greeting+', '+files.name
            speak.say(greeting)
        
        elif text=='what is my name' or text=="what's my name":
            build_name=''.join(['Your name is ', files.name, '. You can change it by telling me to call you by a different name.'])
            speak.say(build_name)
            
        elif text=='where am I' or text=='what is my location':
            speak.say('Realtime GPS data and satellite imagery indicates that your last known location is', files.location)
        
        #This section is music/volume related
        
        elif text in cls.replay:
            print("Can't do this yet!")
            #TODO: playlists
            if music.has_music:
                if music.last_song=='':
                    speak.say('You have not played a song recently')
                else:
                    speak.say('Replaying the song')
                    find_music(last_song)
                
            else:
                print('No song is currently playing.')
                speak.say('No song is playing.')
        
        elif text=='shuffle my playlist':
            if files.playlist==[]:
                speak.say("You don't have any songs on your playlist yet.")
            else:
                print('Cannot play playlists yet!')
                #TODO
                music.find_music(random.choice(files.playlist))
        
        elif text=='pause' or text=='stop':
            if music.has_music==True and music.playing==True:
                #no need to pause because song is already paused
                music.playing=False
                speak.say('Song paused')
        
        elif text=='resume' or text=='play' or text=='resume the song':
            if music.has_music==True and music.playing==False:
                music.playing=True
                speak.say('Okay')
        
        #Here, recognition of the string based on text.startswith('x') is allowed.
        
        elif cls.starts(text, 'simon says '):
            #assistant.stop_conversation()
            speak.say(text.replace('simon says ', ''))
        
        elif cls.starts(text, 'play '):
            #assistant.stop_conversation()
            if text=='play my playlist' or text=='play playlist':
                if files.playlist==[]:
                    speak.say("You don't have any songs on your playlist yet.")
                else:
                    speak.say('Playing your playlist')
                    music.play_multiple(True)
            else:
                music.has_music=False
                music.playing=False
                music.find_music(text.replace('play ', '', 1))
        
        elif cls.starts(text, 'volume'):
            if text=='volume':
                speak.say('Volume is set to'+str(volume.volume))
            else:
                text=text.replace('volume ', '')
                if text=='up':
                    volume.move(+5)
                elif text=='down':
                    volume.move(-5)
                else:
                    try:
                        for index, item in enumerate(cls.names):
                            vol=vol.replace(item, cls.numbers[index])
                        total=0
                        for num in vol.split:
                            if num!='':
                                total+=int(num)
                        vol=total
                        if vol >=1 and vol <=100:
                            volume.change(vol)
                        else:
                            speak.say('Please give a number from one to one hundred.')
                    except:
                        speak.say('You can say volume up or down or say volume followed by a number from one to one hundred.')
                    
        elif cls.starts(text, 'call me'):
            if text=='call me':
                build_name='Your name is '+files.name+'. You can change it by saying call me, followed by your name.'
                speak.say(build_name)
            else:
                text=text.replace('call me ', '')
                files.write_file('name', text)
                files.name=text
                print('Name changed to', text)
                speak.say(random.choice(cls.greeting), text)
        
        elif cls.starts(text, 'set my location to ') or cls.starts(text, 'change my location to '):
            text=text.replace('set my loaction to ', '')
            text=text.replace('change my location to ', '')
            files.write_file('location', text)
            files.location=text
            speak.say("Your location has been set to", files.location)
        
        #After this point, efforts to recognize the string by items in the substring are allowed.
        #They are not allowed above in case someone says "play sounds of weather" or "simon says my playlist can add"
        
        elif 'weather' in text or 'forecast' in text:
            current_weather=random.choice(cls.current_weather)
            percent_chance=random.randint(1,101)
            percent_chance=str(percent_chance)
            future_weather=random.choice(cls.future_weather)
            build_weather=' '.join(['Right now, in', files.location, 'it is', current_weather, 'with a', percent_chance, 'percent chance of', future_weather])
            speak.say(build_weather)
        
        elif 'add' in text and 'playlist' in text:
            if music.last_song=='':
                speak.say('You have not played a song recently')
            else:
                if files.playlist==[]:
                    files.write_file('playlist', music.last_song)
                else:
                    files.append_file('playlist', music.last_song)
                build_added_song=' '.join(["I've added", music.last_song, 'to your playlist'])
                speak.say(build_added_song)
        
        #No command was recognized
        else:
            #assistant.stop_conversation()
            speak.say("Sorry, I don't know what you just said.")
            files.append_file("unknown_responses", text)
            
        #Unpause music
        if music.playing==True and music.has_music==True and cls.keep_running:
            music.pause(False)
            print('Playing song')


"""IMPORT PACKAGES"""

print("Importing packages...")

#Let the user know that importlib is being imported, and then import it
imp('importlib',real=False)
#Actually imports it
import importlib

#Used for checking if a file exists
os=imp('os')

print("Current dir is", os.getcwd())

leds=imp('aiy.leds')
#Initalize button light to let the user know the program is loading
Color=leds.Color
lights.init()

tts=imp('pyttsx3')
sr=imp('speech_recognition')
argparse=imp('argparse')
time=imp('time')
random=imp('random')
snowboy=imp('snowboy.snowboydecoder')
threading=imp('threading')
subprocess=imp('subprocess') #Used for checking IP address and changing/getting volume

aiy_board=imp('aiy.board')

audio=imp('aiy.voice.audio')
AudioFormat=audio.AudioFormat
record_file=audio.record_file
del audio
#TODO: Implement aiy.voice.audio.play_wav in the future


#logging=imp('logging')
#TODO: Is this necessary?

#Import for playing songs:
vlc=imp('vlc')
string=imp('string')
sys=imp('sys')
ast=imp('ast')
youtube_dl=imp('youtube_dl')
#logging.basicConfig(
#    level=logging.INFO,
#    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
#)

print('Packages imported. Initalizing...')


#Initalizes and then runs main thread

if __name__=='__main__':
    try:
        main_thread.init()
        print('Done initalizing. Running...')
        main_thread.run()
    except KeyboardInterrupt:
        print("\nKeyboard interruption detected")
    except:
        print("Unexpected error")
        raise
    finally:
        lights.reset_led()
else:
    print('Done initalizing.')
