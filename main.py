#Other import statements at bottom of file
import logging

def imp(package_name):
    
    log.debug("Importing {0}...".format(package_name))
    return importlib.import_module(package_name)

class log:
    
    COLOR_SEQ = "\033[1;%dm"
    RESET_SEQ = "\033[0m"
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    COLORS = {
        'WARNING': YELLOW,
        'INFO': WHITE,
        'DEBUG': BLUE,
        'CRITICAL': YELLOW,
        'ERROR': RED
    }

    @classmethod
    def init(cls):
        files.write_file("log","",False)
        cls.rootLogger = logging.getLogger(__name__)
        cls.rootLogger.setLevel(logging.NOTSET)
        
        cls.console = logging.StreamHandler()#sys.stdout)
        cls.fileHandler = logging.FileHandler("log.txt")
        
        #console accepts logs at least as severe as INFO
        #log file accepts logs at least as severe as DEBUG
        cls.console.setLevel(logging.INFO)
        cls.fileHandler.setLevel(logging.DEBUG)
        
        #Set formatting of logs
        cls.format = logging.Formatter('%(levelname)s:%(message)s')
        cls.console.setFormatter(log_formatter())
        cls.fileHandler.setFormatter(log_formatter())
        
        cls.rootLogger.addHandler(cls.console)
        cls.rootLogger.addHandler(cls.fileHandler)
        
        cls.logger = cls.rootLogger
        cls.logger.propagate = False
        
    @classmethod
    def _make_record(cls,msg,lvl):
        
        #Build the log
        log_dict={
            "msg": cls._format_str(msg),
            #"exc_info": exc_info,
            "levelno": lvl,
            "levelname": logging.getLevelName(lvl)
        }
        
        if lvl!=logging.DEBUG and lvl!=logging.INFO:
            
            #get info about the method that called the log
            callerframerecord = inspect.stack()[2]
            frame = callerframerecord[0]
            info = inspect.getframeinfo(frame)
            try:
                filename=info.filename
                function=info.function
                line=info.lineno
            finally:
                del info
                del frame
            
            #Set levelname
        
            #Build the log
            more_info={
                "lineno": line,
                "funcName": function,
            }
            log_dict.update(more_info)
        
        #Log the event
        record = logging.makeLogRecord(log_dict)
        cls.logger.handle(record)
        
    @classmethod
    def _format_str(cls,text):
        build=""
        first=True
        for obj in text:
            if not first:
                build+=" "
            else:
                first=False
            build+=str(obj)
        return build
    
    @classmethod
    def debug(cls,*text):
        cls._make_record(text,logging.DEBUG)
    
    @classmethod
    def info(cls,*text):
        cls._make_record(text,logging.INFO)
    
    @classmethod
    def warning(cls,*text):
        cls._make_record(text,logging.WARNING)
    
    @classmethod
    def error(cls,*text):
        cls._make_record(text,logging.ERROR)
    
    @classmethod
    def critical(cls,*text):
        cls._make_record(text,logging.CRITICAL)
    
class log_formatter(logging.Formatter):

    def format(self, record):

        if record.levelno == logging.INFO:
            self._style._fmt = "%(msg)s"
        elif record.levelno == logging.DEBUG:
            self._style._fmt = "%(levelname)s: %(msg)s"
        else:
            self._style._fmt = "%(levelname)s: ln %(lineno)d in %(funcName)s: %(msg)s"
            
        levelname = record.levelname
        if levelname in log.COLORS:
            levelname_color = log.COLOR_SEQ % (30 + log.COLORS[levelname]) + levelname + log.RESET_SEQ
            record.levelname = levelname_color
            
        return super().format(record)
    
class speak:
    @classmethod
    def init(cls):
        log.debug('Initalizing voice...')
        cls.engine = tts.init()
        
        #Should customize voice properties
        
    @classmethod
    def say(cls, *args):
        build=''
        for text in args:
            if not len(build)==0:
                build+=' '
            build+=str(text)
        log.debug('Speaking "'+build+'"...')
        log.info(build)
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
            log.warning("Error: couldn't initalize leds")
    
    @classmethod
    def init(cls):
        #Have to set this after importing aiy.leds, cannot go in class body
        cls.colors=['off', leds.Color.CYAN, leds.Color.WHITE, leds.Color.PURPLE, leds.Color.YELLOW, leds.Color.BLUE, leds.Color.GREEN, Color.RED]
        cls.names=['off', 'cyan', 'white', 'purple', 'yellow', 'blue', 'green', 'red']
        
        log.debug('Initalizing status light...')
        #cls.status_ui=aiy.voicehat.get_status_ui()
        #TODO: keep or remove?
        log.debug('Initalizing leds...')
        cls._get_led_inst()
        log.debug('Setting LED...')
        cls.button_change('purple')
    
    @classmethod
    def status_change(cls, info):
        log.debug('Status light=', info)
        cls.status_ui.status(info)
    
    @classmethod
    def button_change(cls, c):
        #Try to initalize if instance doesn't exist
        if cls.led_inst is None:
            log.debug("Trying to create an LED instance")
            cls._get_led_inst()
        
        #If instance exists
        if cls.led_inst is not None:
            log.debug('Changing LED color to', c)
            color=cls.colors[cls.names.index(c)]
            
            if color==cls.current_color:
                log.debug("led is already set to", color)
            elif color=='off':
                cls.led_inst.update(leds.Leds.rgb_off())
            else:
                cls.led_inst.update(leds.Leds.rgb_on(color))
            cls.current_color=color
        else:
            log.error("Cannot change led color: Leds() not yet initalized.")
        
    @classmethod
    def reset_led(cls):
        #Turn off leds before the program exits so they are not left on
        if not cls.led_inst is None:
            log.debug('Resetting led')
            try:
                cls.button_change('off')
                #Delete the associated variables for Leds() instance and aiy.leds package respectively
                #IDK if this actually helps anything
                del cls.led_inst
                #This throws error for some reason
                #del leds
            except:
                log.critical("When resetting led, another error ocurred:")
                raise

class files:
    
    #This is relative to the path that is changed at the beginning of the program
    data_loc='data/'
    
    @classmethod
    def init(cls):
        log.debug('Initalizing files...')
        log.debug('Loading playlist...')
        cls.playlist=cls.load_file('playlist', '')
        if type(cls.playlist)!=list:
            cls.playlist=[]
        log.debug('Playlist has '+str(len(cls.playlist))+' items.')
        log.debug('Loading name...')
        cls.name=cls.load_file('name', 'human')
        log.debug('Name is '+str(cls.name))
        log.debug('Loading location...')
        cls.location=cls.load_file('location', 'Null Island')
        log.debug('Location is '+cls.location)
    
    @classmethod
    def _nofile(cls, file, contents, use_default=True):
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        log.info('Data file', loc+file+'.txt', 'missing, creating...')
        cls.write_file(file, contents, use_default)
    
    @classmethod
    def write_file(cls, file, info, use_default=True):
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        with open(loc+file+'.txt', "w+") as data:
            data.write(info)
            log.debug('Wrote "'+str(info)+'" to', loc+file+'.txt')
    
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
                        log.exception("ValueError")
                        pass
        except IOError:
            cls._nofile(file, not_found, use_default)
            contents=not_found
        if len(contents)==1:
            contents=contents[0]
        log.debug("Retrieved", contents, "from", loc+file+'.txt')
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
                log.debug('Appended "'+str(info)+'" to', loc+file+'.txt')
        except IOError:
            cls._nofile(file, info, use_default)

    @classmethod
    def item_exists(cls, name, use_default=True):
        #returns true if a file or directory with the given name exists
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        res=os.path.exists(loc+name)
        log.debug("Path",loc+name,"exists:",res)
        return res
        
    @classmethod
    def file_exists(cls, name, use_default=True):
        if not cls.item_exists(name, use_default):
            log.debug("Path",loc+name,"does not exist, file cannot exist")
            return False
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        res=os.path.isfile(loc+name)
        log.debug("File",loc+name,"exists:",res)
        return res
        
    @classmethod
    def dir_exists(cls, name, use_default=True):
        if not cls.item_exists(name, use_default):
            log.debug("Path",loc+name,"does not exist, dir cannot exist")
            return False
        if use_default:
            loc=cls.data_loc
        else:
            loc=""
        res=os.path.isdir(loc+name)
        log.debug("Dir",loc+name,"exists:",res)
        return res

class volume:
    @classmethod
    def init(cls):
        log.debug('Loading volume...')
        log.debug('Getting current volume...')
        cls.volume=cls._get_volume()
        volume.update()
        log.debug('Volume is set to '+str(cls.volume))
    
    @classmethod
    def update(cls):
        log.debug("Volume updated")
        subprocess.call('amixer -q set Master %d%%' % cls.volume, shell=True)
    
    @classmethod
    def change(cls, vol):
        cls.volume=vol
        log.debug('Volume: ', vol)
        cls.update()
        speak.say('Volume set to', str(vol))
    
    @classmethod
    def _get_volume(cls):
        res=subprocess.check_output(r'amixer get Master | grep "Front Left:" | sed "s/.*\[\([0-9]\+\)%\].*/\1/"', shell=True).strip()
        return int(res)
    
    @classmethod
    def move(cls, amount):
        #raise or lower the volume by the given ammount
        log.debug("Changing volume by",amount)
        cls.change(cls.volume+amount)

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
        log.debug('Loading music...')
        
        log.debug('Loading Youtube_DL')
        #Set Youtube DL options
        cls.ydl_opts={
            'default_search': 'ytsearch1:',
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': False, #Quiet is false, should show info when loading songs
            'ignore-errors': False,
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
        
        log.debug('Loading VLC...')
        cls.vlc_instance=vlc.get_default_instance()
        
        #create a playlist?
        #cls.vlc_playlist=cls.vlc.media_list_new()
        #cls.vlc_player=cls.vlc_instance.media_list_player_new()
        
        cls.vlc_player=cls.vlc_instance.media_player_new()
        
        cls.vlc_event_manager=cls.vlc_player.event_manager()
        cls.vlc_event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, cls._song_finished, 1)
    
    @classmethod
    def find_music(cls,search_term):
        try:
            can_play=True
            log.debug("Checking if search term is already indexed")
            song_id=cls._get_id_from_term(search_term)
            
            if song_id is None:
                log.debug("Song not found in index, searching Youtube...")
                speak.say("Searching for "+search_term)
                #Song isn't indexed, search YT
                try:
                    with youtube_dl.YoutubeDL(cls.ydl_opts) as ydl:
                        meta=ydl.extract_info(search_term, download=False)
                        
                except KeyboardInterrupt:
                    log.info("KeyboardInterrupt")
                    raise
                    
                except Exception:
                    #Error when song doesn't exist
                    log.warning("Exception ocurred when searching for song:",Exception)
                    meta=None
                    
                if meta is None:
                    #Song doesn't exist
                    log.info("Song does not exist")
                    can_play=False
                    
                else:
                    meta=meta['entries'][0]
                    #Song exists but search term not known
                    song_id=meta["id"]
                    song_url = meta["url"]
                    song_title= meta["title"]
                    log.info("Found song:", song_title)
                    
                    title=cls._get_title_from_id(song_id)
                    
                    if title is None or not files.file_exists('music/'+song_id+'.mp3',False):
                        #Song exists but is not saved locally
                        if cls.save_files:
                            log.debug("Song not downloaded, downloading...")
                            speak.say("Downloading "+cls.cleanup_title(song_title))
                            try:
                                cls.download_music(song_url,song_id)
                            except KeyboardInterrupt:
                                log.debug("KeyboardInterrupt when downloading song")
                                raise
                            log.info("Finished downloading.")
                            #Index title
                            title=song_title
                            cls.song_ids[song_id]=song_title
    
                        else:
                            log.debug("Song not downloaded, save_files is set to False")
                            log.info("Streaming song...")
                            cls._stream_music(song_url)
                    
                    log.debug("Indexing search term")
                    #Index the search term
                    cls.song_terms[search_term]=song_id
                    #Save dicts to file
                    cls._save_dicts()
                    
            else:
                title=cls._get_title_from_id(song_id)
                log.info("Found song:", title)
                log.debug("id:", song_id)
                
            if can_play:
                log.debug("Playing song...")
                cls.playing=True
                cls.has_music=True
                build_song=' '.join(['Playing', cls.cleanup_title(title)])
                log.debug(build_song)
                cls.last_song=search_term
                speak.say(build_song)
                try:
                    cls._play_from_file(song_id)
                    cls.vlc_player.play()
                
                except KeyboardInterrupt:
                    log.info("KeyboardInterrupt when playing song")
                    raise
                
                except:
                    log.error("Error playing song:",sys.exc_info()[0])
                    speak.say('Sorry, there was an error')
                    cls.has_music=False
                    cls.playing=False
                
            else:
                log.debug("Can't find", search_term)
                speak.say("Sorry, I can't find", search_term)
                
        except KeyboardInterrupt:
            log.warning("KeyboardInterrupt detected, song operation canceled.")
        
    @classmethod
    def _get_id_from_term(cls, term):
        return cls.song_terms.get(term)
        
    @classmethod
    def _get_title_from_id(cls, song_id):
        return cls.song_ids.get(song_id)
        
    @classmethod
    def _save_dicts(cls):
        log.debug("Saving song info dictionaries...")
        files.write_file('song_ids',str(cls.song_ids))
        files.write_file('song_terms',str(cls.song_terms))
        
    @classmethod
    def _load_dicts(cls):
        error=False
        log.debug("Loading song info dictionaries...")
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
            log.info("Error loading dictionaries, saving default values")
            cls._save_dicts()
        
    @classmethod
    def download_music(cls, url, song_name):
        opts=cls.ydl_opts
        opts['outtmpl']='music/{0}.%(ext)s'.format(song_name)
        #download with output as the id
        try:
            with youtube_dl.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except KeyboardInterrupt:
            log.info("KeyboardInterrupt while downloading")
            raise
        except:
          log.error("Error downloading song:", sys.exc_info()[0])
        
    @classmethod
    def _stream_music(cls, url):
        #todo: implement this
        log.debug("Streaming music from url",url)
        cls.vlc_player.set_media(cls.vlc_instance.media_new(url))
    
    @classmethod
    def _play_from_file(cls, music_file):
        #todo: check if this works
        log.debug("Playing music from file",music_file)
        cls.vlc_player.set_media(cls.vlc_instance.media_new("music/"+music_file+".mp3"))
        
    @classmethod
    def cleanup_title(cls,title):
        build=''
        for character in title:
            if character in cls.title_chars:
                build+=character
        res=build.replace("  "," ")
        log.debug("Cleaned up song title",'"'+title+'"',"to make",'"'+res+'"')
        return res
    
    @classmethod
    def play_multiple(cls, reset=False):
        log.info('Loading the song')
        if reset:
            log.debug("Starting playlist over")
            cls.playlist_item=0
            cls.is_playlist=True
        else:
            cls.playlist_item+=1
            
        next_song=files.playlist[cls.playlist_item]
        log.info('Next song is', next_song)
        time.sleep(2)
        cls.find_music(next_song)
    
    @classmethod
    def _song_finished(cls, *args, **kwargs):
        log.info('Song finished')
        log.debug('Playlist:', cls.is_playlist)
        if cls.is_playlist==True:
            if cls.playlist_item==len(playlist):
                log.debug('Playlist done')
            else:
                log.debug('Song done, continuing playlist')
                cls.play_multiple()
    
    @classmethod
    def pause(cls, paused=True):
        log.debug("Paued:",paused)
        cls.vlc_player.set_pause(paused)
    
class btn:
    
    @classmethod
    def init(cls):
        log.debug('Initalizing button...')
        cls.board=aiy_board.Board()
        cls.event_was_set=False
    
    @classmethod
    def wait(cls):
        log.debug("Waiting for button press")
        cls.board.button.wait_for_press()
        
    @classmethod
    def set_event(cls):
        cls.done = threading.Event()
        cls.board.button.when_pressed=cls.done.set
        cls.event_was_set=True
        log.debug("Set up button pressed event")
        
    @classmethod
    def was_pressed(cls):
        assert cls.event_was_set
        return cls.done.is_set()
   
class record:

    callback=None

    @classmethod
    def init(cls,fname='recording.wav'):
        cls.filename=fname
        log.debug("Setting up recording args...")
        parser = argparse.ArgumentParser()
        parser.add_argument('--filename', '-f', default=cls.filename)
        cls.args = parser.parse_args()
    
    @classmethod
    def new(cls):
        btn.set_event()
        log.info("Recording audio...")
        try:
            record_file(AudioFormat.CD, filename=cls.args.filename, wait=cls.interval, filetype='wav')
        except KeyboardInterrupt:
            log.info("KeyboardInterrupt whle recording audio")
        log.info("Recording stopped")
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
        hotword.resetSpeaking()
        while not finished:
            duration = time.monotonic() - start
            if btn.was_pressed() or (hotword.doneSpeaking() and duration > 1):
                finished=True
            elif duration > 5 and hotword.speaking==0:
                log.debug("Stopped recording because user did not speak")
                finished=True
            else:
                log.debug('Recording: %.02f seconds.' % duration, "speaking:", hotword.isSpeaking())
                time.sleep(0.5)

class recognize:
    
    #Speech-to-text
    
    @classmethod
    def init(cls,fname='houndify'):
        log.debug('Loading Houndify credentials from file...')
        file_data=files.load_file(fname, '') #credential location, should be stored as 2 lines: client ID and client key
        assert file_data!='' #Credentials file is missing or empty
        cls.HOUNDIFY_CLIENT_ID = file_data[0].replace("\n","") # Houndify client IDs are Base64-encoded strings
        cls.HOUNDIFY_CLIENT_KEY = file_data[1].replace("\n","") # Houndify client keys are Base64-encoded strings
        
    
    @classmethod
    def main(cls):
        
        #Record what the user said
        file_name=record.new()
        if files.file_exists(file_name,False):
            lights.button_change('cyan')
            log.info("Interpreting speech...")
            
            #Get path to the audio file and load it
            audio=cls.parse_audio(file_name)
            
            #Send the audio file to Houndify for recognition, return text
            text=cls.get_text(audio)
            
            #return the text that the user said so it can be interpreted
            return text
        else:
            log.warning("Recording file does not exist")
            return None
    
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
            log.debug("Result: client said", resp)
            
        except sr.UnknownValueError:
            log.error("Houndify could not understand audio")
            speak.say("Sorry, I cannot understand what you just said")
            
        except sr.RequestError as e:
            speak.say("Sorry, I cannot connect to the speech recognition service. Please try again later.")
            log.warning("Could not request results from Houndify service; {0}".format(e))
        return resp

class hotword:
    
    started=False
    detected=False
    
    @classmethod
    def init(cls):
        log.debug("Starting detector thread...")
        cls.detector_thread = threading.Thread(target=cls.start, daemon=True)
        cls.detector_thread.start()
        
    @classmethod
    def start(cls):
        cls.started=True
        log.debug("Starting detector")
        cls.detector = snowboy.HotwordDetector(files.load_file('path_to_voice_model', './model.pmdl'), sensitivity=0.4, audio_gain=1)
        try:
            cls.detector.start(cls.detected_callback)
            log.debug("Detector running")
        except:
            log.critical('Error starting detector')
            raise

    @classmethod
    def reset_detector(cls):
        log.debug("Detector trigger has been reset")
        cls.detected=False

    @classmethod
    def detected_callback(cls):
        log.debug("Hotword detected")
        cls.detected=True
        
    @classmethod
    def was_said(cls):
        return cls.detected
        
    @classmethod
    def doneSpeaking(cls):
        sp=cls.isSpeaking()
        if sp:
            cls.speaking=1
        elif cls.speaking > 0:
            cls.speaking+=1
        
        #User spoke then was silent for 4 checks
        if cls.speaking > 4:
            log.debug("User stopped speaking")
            return True
        else:
            return False
        
    @classmethod
    def resetSpeaking(cls):
        cls.speaking=0
        
    @classmethod
    def isSpeaking(cls):
        return cls.detector.vad_status >= 0
    
class trigger:
    
    #Waits for a trigger from the user
    #Stops when the user presses the button or speaks the hotword

    @classmethod
    def init(cls):
        cls.commands=[]
        log.debug("Starting trigger thread")
        cls.input_thread = threading.Thread(target=cls.getConsoleInput, daemon=True)
        cls.input_thread.start()
    
    @classmethod
    def wait(cls):
        hotword.reset_detector()
        btn.set_event()
        
        looping=True
        log.debug('Waiting for wakeup. Hotword detection started:',hotword.started)
        
        while looping:
            if hotword.was_said() or btn.was_pressed() or cls.hasCommands():
                log.debug('Wakeup triggered, exiting wait loop')
                looping=False
            else:
                time.sleep(0.5)
    
    @classmethod
    def getConsoleInput(cls):
        try:
            while True:
                log.debug("Accepting keyboard input")
                inp=input("")
                cls.commands.append(inp)
                log.debug("User entered",inp)
        except KeyboardInterrupt:
            log.debug("KeyboardInterrupt while waiting for input, raising interrupt...")
            raise
    
    @classmethod
    def getNextCommand(cls):
        if cls.hasCommands():
            first=cls.commands[0]
            cls.commands.pop(0)
            return first
        else:
            return None
            
            
    @classmethod
    def hasCommands(cls):
        has_command=len(cls.commands)!=0
        return has_command

class main_thread:
    
    initialized=False
    keep_running=True
    
    @classmethod
    def init(cls):
        
        log.debug('Initalizing main...')
        
        #Set class variables that will be used to recognize the intent of a speaker
        
        cls.greeting=['good morning', 'hello', 'good afternoon', 'hi', 'hey', 'hey there', 'hi there', 'hello there']
        cls.replay=['replay', 'start over', 'restart the song', 'start the song over']
        cls.names=['one hundred', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'teen', 'thirty', 'fourty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        cls.numbers=[100, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 10, 30, 40, 50, 60, 70, 80, 90, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        cls.current_weather=['sunny', 'cloudy', 'stormy', 'foggy', 'snowing', 'sleeting', 'hailing', 'windy', 'humid']
        cls.future_weather=['rain', 'thunder and lightning', 'clouds', 'increased humidity', 'high winds', 'fog', 'storms', 'hail', 'sleet', 'tornado', 'snow', 'solar flare', 'tsunami', 'zombie apocalypse', 'raining tacos', 'wildfire', 'avalanche', 'sand storms', 'drought']
        
        #Initalize packages that have been imported
        log.debug("Initalizing other classes")
        #lights.init() #This is called right after importing leds
        speak.init()
        files.init()
        volume.init()
        music.init()
        btn.init()
        recognize.init()
        record.init()
        hotword.init()
        trigger.init()
        
        #Set initialized flag, allowing main.run() to be called without error
        cls.initialized=True
        
        
    @classmethod
    def run(cls):
        
        #Packages must have been imported and initalized before use, return an error otherwise
        assert cls.initialized
        
        lights.button_change('green')
        speak.say('Hello')
        log.info('Program loaded.\nPress the button, say the hotword, or enter a command on the console.')
        #separate function/class?
        while cls.keep_running:
            lights.button_change('green')
            
            if not trigger.hasCommands():
                
                trigger.wait()
            
            command=trigger.getNextCommand()
            if command is None:
            
                if music.playing:
                    log.debug('Pausing song')
                    music.pause()
                
                lights.button_change('yellow')
                log.debug('Listening...')
                
                text=recognize.main()
                
            else:
                text=command
            
            lights.button_change('blue')
            
            if text is None:
                log.debug("Nothing to recognize")
            elif len(str(text))==0:
                #Nothing was heard
                speak.say("Sorry, I didn't hear you.")
                log.debug("I didn't hear you. Please press the button and try again.")
            else:
                log.debug('You said "'+str(text)+'".')
                main_thread.recognize(str(text).lower())
    
    @classmethod
    def starts(cls, text, beginning):
        return text.startswith(beginning)
    
    @classmethod
    def recognize(cls, text):
        #Interpret what the person said
        
        if text=='power off' or text=='shut down':
            speak.say('Good bye!')
            lights.reset_led()
            subprocess.call('sudo shutdown now', shell=True)
        
        elif text=='reboot' or text=='restart':
            speak.say('See you in a bit!')
            lights.reset_led()
            subprocess.call('sudo reboot', shell=True)
            
        elif text=='close program' or text=='stop program' or text=='stop recongizer' or text=='stop recognizer' or text=='exit':
            speak.say('Goodbye for now.')
            log.debug("Closing program...")
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
            if music.has_music:
                if music.last_song=='':
                    speak.say('You have not played a song recently')
                else:
                    log.info('Replaying the song')
                    music.find_music(music.last_song)
                
            else:
                log.debug('No song is currently playing.')
                speak.say('No song is playing.')
        
        elif text=='shuffle my playlist':
            if files.playlist==[]:
                speak.say("You don't have any songs on your playlist yet.")
            else:
                log.error("Can't play playlists yet!")
                #TODO
                music.find_music(random.choice(files.playlist))
        
        elif text=='pause' or text=='stop':
            if music.has_music==True and music.playing==True:
                #pause song in case command was given on the console
                music.playing=False
                music.pause(True)
                speak.say('Song paused')
        
        elif text=='resume' or text=='play' or text=='resume the song':
            if music.has_music==True and music.playing==False:
                music.playing=True
                speak.say('Okay')
        
        #Here, recognition of the string based on text.startswith('x') is allowed.
        
        elif cls.starts(text, 'simon says '):
            speak.say(text.replace('simon says ', ''))
        
        elif cls.starts(text, 'play '):
            if text=='play my playlist' or text=='play playlist':
                if files.playlist==[]:
                    speak.say("You don't have any songs on your playlist yet.")
                else:
                    log.error("Can't play playlists yet!")
                    speak.say('Playing your playlist')
                    music.play_multiple(True)
            else:
                music.has_music=False
                music.playing=False
                music.find_music(text.replace('play ', '', 1))
        
        elif cls.starts(text, 'volume'):
            if text=='volume':
                speak.say('Volume is set to', str(volume.volume))
            else:
                text=text.replace('volume ', '').replace('volume','') #In case the user says something like "volumes"
                if text=='up':
                    volume.move(+10)
                elif text=='down':
                    volume.move(-10)
                else:
                    try:
                        vol=text
                        for index, item in enumerate(cls.names):
                            vol=vol.replace(item, str(cls.numbers[index]))
                        total=0
                        for num in vol.split():
                            if num!='':
                                total+=int(num)
                        vol=total
                        if vol >=1 and vol <=100:
                            volume.change(vol)
                        else:
                            speak.say('Please give a number from one to one hundred.')
                    except ValueError:
                        log.debug("ValueError converting volume query to an int")
                        speak.say('You can say volume up, volume down, or volume followed by a number from one to one hundred.')
                    
        elif cls.starts(text, 'call me'):
            if text=='call me':
                build_name='Your name is '+files.name+'. You can change it by saying call me, followed by your name.'
                speak.say(build_name)
            else:
                text=text.replace('call me ', '')
                files.write_file('name', text)
                files.name=text
                log.debug('Name changed to', text)
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
            speak.say("Sorry, I don't know what you just said.")
            files.append_file("unknown_responses", text)
            
        #Unpause music
        if music.playing==True and music.has_music==True and cls.keep_running:
            music.pause(False)
            log.debug('Finished responding to query. Playing song...')


"""IMPORT PACKAGES"""


#Initalize logging
import inspect
log.init()

log.debug("Logging started")
log.info("Importing packages...")

log.debug("Importing importlib...")
import importlib

leds=imp('aiy.leds')
#Initalize button light to let the user know the program is loading
Color=leds.Color
lights.init()

#Used for checking if a file exists
os=imp('os')
log.debug("Current dir is", os.getcwd())

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

#Import for playing songs:
vlc=imp('vlc')
string=imp('string')
sys=imp('sys')
ast=imp('ast')
youtube_dl=imp('youtube_dl')

log.info('Packages imported. Initalizing...')


#Initalizes and then runs main thread

if __name__=='__main__':
    try:
        main_thread.init()
        log.info('Done initalizing. Running...')
        main_thread.run()
    except KeyboardInterrupt:
        log.info("Keyboard interrupt detected")
    except:
        log.critical("Unexpected error")
        raise
    finally:
        lights.reset_led()
else:
    log.debug('Done initalizing.')
