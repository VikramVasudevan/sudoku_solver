import os

# Import the gTTS module for text  
# to speech conversion  
from gtts import gTTS  
  
# This module is imported so that we can  
# play the converted audio  
  
from playsound import playsound  
from pathlib import Path

import config

def play(text_val, prefix):
    print(text_val)
    if(config.DISABLE_AUDIO):
        return
    # Here are converting in English Language  
    language = 'en'  
    
    # Passing the text and language to the engine,  
    # here we have assign slow=False. Which denotes  
    # the module that the transformed audio should  
    # have a high speed  
    obj = gTTS(text=text_val, lang=language, slow=False)  
    
    #Here we are saving the transformed audio in a mp3 file named  
    # exam.mp3  
    soundFileName = prefix + "_puzzle.mp3"
    outputDirectory = "./output"
    if(not os.path.exists(outputDirectory)):
       print("Creating directory ", outputDirectory)
       os.mkdir(outputDirectory)

    archiveFileName = Path().cwd() / outputDirectory / soundFileName
    obj.save(archiveFileName)
    playsound(str(archiveFileName)) 

def callOut(grid):
    text = ""
    for cell in grid:
        if(cell["col"]%9 ==0):
            if(text != ""):
                play(text,"_audio_row_" + str(cell["row"]))
            text = "row " + str(cell["row"]) + ": "
        text = text + (", " if cell["col"]!=0 else "") + str(cell["value"])            
    # Play the last row
    play(text,"_audio_row_" + "final")

def printGridToConsole(grid):
    text = ""
    for cell in grid:
        if(cell["col"]%9 ==0):
            if(text != ""):
                print(text)
            text = "row " + str(cell["row"]) + ": "
        text = text + (", " if cell["col"]!=0 else "") + str(cell["value"])            
    print(text)