import sys, os

# Suppress comtypes/pyttsx3 callback errors in console
sys.stderr = open(os.devnull, 'w')

import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit
import webbrowser
import subprocess
import random



engine=pyttsx3.init()

# If female voice needed, use these 3 lines
# voices=engine.getProperty("voices")
# for i, v in enumerate(voices):
#     print(i, v.id, v.name)

engine.setProperty("rate",200)
engine.setProperty("volume",1.0)
# engine.setProperty("voice", voices[1].id) (code for female voice)




def speak(text):
  # Speaks the given text loud
  engine.say(text)
  engine.runAndWait()

def take_command():
  # Listens and coverts to text
  r=sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening...")
    r.adjust_for_ambient_noise(source, duration=0.7)
    r.pause_threshold=1
    audio=r.listen(source)


    try:
      print("Recognizing...")
      query=r.recognize_google(audio, language="en-in")
      print(f"You said: {query}")
    except sr.UnknownValueError:
      print("Sorry, I did not understand.")
      return "None"
    except sr.RequestError as e:
      print(f"Could not request results; check your internet")
      return "None"

  return query.lower()


def tell_time():
  # It will tell you the cureent time
  now=datetime.datetime.now().strftime("%I:%M:%p")   #12 hours format
  speak(f"The time is {now}")
  return now

def open_website(site_name):
  # Opens the weebsite by name
  # You can add more websites in your dict
  sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "linkedin": "https://www.linkedin.com"
    }
  site_key = site_name.lower().strip()
  url = sites.get(site_key)
  if url:
        speak(f"Opening {site_key}")
        webbrowser.open(url)
  else:
        # Try to open the raw text as a URL or search term
    if site_key.startswith("http"):
      webbrowser.open(site_key)
    else:
      speak(f"Opening {site_key}")
      webbrowser.open(f"https://{site_key}")


def search_web(query):
    # Search the web for the given query using Google.
    if not query:
        speak("What should I search for?")
        return
    speak(f"Searching for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")


def play_music(song_name):
   if not song_name:
      speak("Please tell me the song name to play.")
      return
   speak(f"Playing {song_name} on YouTube")
   pywhatkit.playonyt(song_name)

   listening=False
   speak("Iam now paused. Say 'Jarvis listen when you want me to listen again")



apps = {
        "notepad": "notepad.exe",
        "chrome": "chrome.exe",
        "vscode": "code",   # VS Code (if installed and in PATH)
        "calculator": "calc.exe"
    }

def open_app(app_name):
  
    app_key = app_name.lower().strip()
    path = apps.get(app_key)

    if path:
        speak(f"Opening {app_key}")
        try:
            os.system(path)
        except Exception as e:
            speak("Sorry, I couldn't open the app.")
            print(e)
    else:
        speak(f"App {app_key} is not configured yet.")




if __name__=="__main__":
  speak("Hello Sujal, Iam Jarvis.")

  listening=True

  while True:
    command=take_command()

    if command=="None":
      continue
    command=command.lower().strip()
    speak(f"You said {command}")

    if "jarvis listen" in command:
      
       speak("I am listening now")
       continue
    
    if listening:
      if "time" in command:
        tell_time()

      elif "open" in command:
        item=command.replace("open ", "", 1).strip().lower()

        if item in apps:
            open_app(item)
        else:
            open_website(item)
      
      elif "search" in command:
                # remove word 'search' and possible word 'for'
                query = command.replace("search", "").replace("for", "").strip()
                search_web(query)

      elif "play music" in command or "play song" in command or "play some music" in command or "play" in command:
        song=command.replace("play", "", 1).strip()
        play_music(song)

      elif any(word in command for word in ["exit", "quit", "bye", "stop","shutdown"]):
        speak("Jarvis shutting down.")
        break

      else:
        speak("Sorry i cant do that yet")
        
     
