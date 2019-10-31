import speech_recognition as sr
import pyttsx3
import time
import fnmatch
import linecache

import ply.lex as lex
import ply.yacc as yacc
import os
import subprocess

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pygame import mixer


options = Options()
options.add_argument('--headless')

# open
# search

# pyaudio/ speech recognition initiation

r = sr.Recognizer()
botReply = pyttsx3.init()
bot_text = "BOT : "
user_text = "USER : "
ok_text = "OK, "
repeat = "Can you repeat ?"
welcome = "Welcome, please tell me what to do"
write_conf = "Is that all?"

def find(pattern, path):
    found=False
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                found=True
                return os.path.join(root, name)
    if found==False:
        print("Not found")

def property_setting(r,v):
    botReply.getProperty('volume')
    botReply.getProperty('rate')
    botReply.setProperty('rate',r)
    botReply.setProperty('volume',v)


def write_file(source):
    lists = []
    bool = True
    while bool:
        print("What do you want to be written?")
        text = None
        try:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            text = r.recognize_google(audio)
        except:
            print("WHAT?!?!?!!?")
        lists.append(text)

        # confirmation
        print("Is that all?")
        try:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            text = r.recognize_google(audio)
        except:
            print("WHAT?!?!?!!?")

        if text == "yes":
            bool = False
            break
        elif text == "restart":
            print("restarting")
            lists.pop()
            break
        elif text == "no":
            print("Your note will continue on the next line")

    bools = True
    title = None
    while bools:
        print("Title of note?")
        text = None
        try:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            time.sleep(1)
            text = r.recognize_google(audio)
        except:
            print("WHAT?!?!?!!?")

        texts = None
        print("Is " + text + " the title?")
        try:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            texts = r.recognize_google(audio)
        except:
            print("WHAT?!?!?!!?")

        if texts == "yes":
            bools = False
            title = text
            break

    name = title + ".txt"
    f = open(name, "w+")
    for i in lists:
        f.write(i + "\n")
    print("Your file is saved with name " + name)
    f.close()

tokens = [
    'SEARCH',
    'OPEN',
    'WORD',
    'PLAY',
    'THANKS',
    'WRITE',
    'STOP',
    'AND'
]

t_ignore = r' '

def t_OPEN(t):
    r'open|OPEN'
    t.type = 'OPEN'
    return t

def t_SEARCH(t):
    r'search|SEARCH'
    t.type = 'SEARCH'
    return t

def t_AND(t):
    r'and|AND|then|THEN'
    t.type = 'AND'
    return t

def t_WORD(t):
    r'[a-zA-z_][a-zA-z_0-9]*'
    t.type = 'WORD'
    return t

def t_error(t):
    print("Illegal characters.")
    t.lexer.skip(1)

lexer = lex.lex()

command = []
def p_searching(p):
    '''
    searching : expression
                | empty

    '''
    run(p[1])

def p_expression(p):
    '''
    expression : expression expression
    '''
    p[0] = (p[1],p[2])

def p_expression_type(p):
    '''
    expression : SEARCH
                | OPEN
                | WORD
                | AND
    '''
    p[0] = p[1]
    command.append(p[0])


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    print("Syntax error")

parser = yacc.yacc()
app = []
at_index = []

def app_open():
    word = []

    for i in range(1, len(command)):
        word.append(command[i])

    cwd = os.getcwd()
    file = open("directories.txt", "r+")

    for line in enumerate(file):
        x = (line[1].partition(" - "))
        if x[0] == word[0].lower():
            try:
                y = x[2].rstrip('\n')
                subprocess.call(y)
                break
            except OSError:
                print("Error reading command.\n")

    if word[0].lower() not in app:
        try:
            os.chdir("C:\\")
            a = "dir /s /b "
            b = word[0] + ".exe"
            c = a + b
            x = (os.popen(c).read()).rstrip('\n')
            os.chdir(cwd)
            file.write("\n" + word[0] + " - " + x)
            subprocess.call(x)

        except OSError:
            print("Application does not exist.")

def chrome_search():
    word = []
    for i in range(1, len(command)):
        if ((command[i] == 'and') and (command[i + 1] == 'open')) or (command[i] == 'then') and (
                command[i + 1] == 'open'):
            break
        word.append(command[i])
    browser = webdriver.Chrome('/Users/Ikhsan M/Downloads/chromedriver')
    browser.maximize_window()
    browser.get('https://www.google.com')
    search = browser.find_element_by_name("q")
    search.send_keys(" ".join(word))
    search.send_keys(Keys.RETURN)


def run(p):
    if type(p) == tuple:
        with open("directories.txt", "r+") as file:
            for line in enumerate(file):
                x = (line[1].partition(" - "))
                app.append(x[0])
        if p[0].lower() == 'search':
            chrome_search()
            index = []
            if ('and') or ('then') in command:
                for i in range(0, len(command)):
                    if (command[i] == 'and') or (command[i] == 'then'):
                        index.append(i)
                for j in index:
                    if command[j + 1] == 'search':
                        word = []
                        for i in range(j + 2, len(command)):
                            if ((command[i] == 'and') and (command[i + 1] == 'open')) or (command[i] == 'then') and (
                                    command[i + 1] == 'open'):
                                break
                            word.append(command[i])
                        browser = webdriver.Chrome('/Users/Ikhsan M/Downloads/chromedriver')
                        browser.maximize_window()
                        browser.get('https://www.google.com')
                        search = browser.find_element_by_name("q")
                        search.send_keys(" ".join(word))
                        search.send_keys(Keys.RETURN)
                    elif command[j + 1] == 'open':
                        for i in range(0, len(app)):
                            if app[i] == command[j + 2].lower():
                                x = linecache.getline('directories.txt', i + 1).partition(" - ")
                                try:
                                    y = x[2].rstrip('\n')
                                    subprocess.call(y)

                                except OSError:
                                    print("Error reading command.\n")
            command.clear()

        elif p[0].lower() == 'play':
            name = []
            for i in range(1, len(command)):
                name.append(command[i])
            z = " ".join(name)
            command.clear()
            z = z + '.mp3'
            z = z.lower()
            song = find(z.lower(), 'C:/Users/Ikhsan M/Documents/my_music')
            mixer.init()
            mixer.music.load(song)
            mixer.music.play()

        elif p[0].lower() == 'write':
            write_file(audio)

        elif  p[0].lower() == 'stop':
            mixer.music.stop()

        elif p[0].lower() == 'open':
            app_open()
            index = []
            if ('and') or ('then') in command:
                for i in range(0, len(command)):
                    if (command[i] == 'and') or (command[i] == 'then'):
                        index.append(i)
                for j in index:
                    if command[j + 1].lower() == 'open':
                        for i in range(0, len(app)):
                            if app[i] == command[j + 2].lower():
                                x = linecache.getline('directories.txt', i + 1).partition(" - ")
                                try:
                                    y = x[2].rstrip('\n')
                                    subprocess.call(y)

                                except OSError:
                                    print("Error reading command.\n")
                    elif (command[j + 1].lower() != 'open') and (command[j + 1].lower() != 'search'):
                        for i in range(0, len(app)):
                            if app[i] == command[j + 1].lower():
                                x = linecache.getline('directories.txt', i + 1).partition(" - ")
                                try:
                                    y = x[2].rstrip('\n')
                                    subprocess.call(y)

                                except OSError:
                                    print("Error reading command.\n")
                    elif command[j + 1] == 'search':
                        word = []
                        for i in range(j + 2, len(command)):
                            if ((command[i] == 'and') and (command[i + 1] == 'open')) or ((command[i] == 'then') and (
                                    command[i + 1] == 'open')):
                                break
                            word.append(command[i])
                        browser = webdriver.Chrome('/Users/Ikhsan M/Downloads/chromedriver')
                        browser.maximize_window()
                        browser.get('https://www.google.com')
                        search = browser.find_element_by_name("q")
                        search.send_keys(" ".join(word))
                        search.send_keys(Keys.RETURN)

            command.clear()

        else:
            print("Error reading command")
            command.clear()
    else:
        return p


with sr.Microphone() as source:
    bools = True
    while bools:
        try:
            bool = True
            print("Speak anything: ")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio=r.listen(source)
            text = r.recognize_google(audio)
            print("You said: {}".format(text))
            if text == "OK Google":
                print("YES")
                print(bot_text + welcome)
                property_setting(140,1)
                botReply.say(welcome)
                botReply.runAndWait()
                print("Your command : ")
                while bool:
                    with sr.Microphone() as audio:
                        cmd = r.listen(audio)
                        try:
                            stt = r.recognize_google(cmd)
                            if stt == 'thank you':
                                property_setting(130,1)
                                print(user_text + stt)
                                print(bot_text + "Your Welcome")
                                botReply.say("Your Welcome")
                                botReply.runAndWait()
                                bool = False
                                bools = False
                                break
                            print(user_text + stt)
                            time.sleep(1)
                            print(bot_text + ok_text + stt)
                            print("\n")
                            property_setting(130, 1)
                            botReply.say(ok_text + stt)
                            botReply.runAndWait()
                            stt.lower()

                            #parsing
                            parser.parse(stt)
                            time.sleep(1)
                            print("Speak Anything :")

                        except:
                            print(bot_text + repeat)
                            property_setting(130, 1)
                            botReply.say(repeat)
                            botReply.runAndWait()
                            time.sleep(1)
                            stt = " "
                            print("Speak Anything :")
        except:
            print(bot_text + repeat)
            property_setting(130, 1)
            botReply.say(repeat)
            botReply.runAndWait()

