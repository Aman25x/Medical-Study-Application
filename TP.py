from cmu_112_graphics import *
#copied from: https://www.cs.cmu.edu/~112/notes/hw7.html
from tkinter import *
from tkinter import messagebox #desktop messages
import cv2 as cv #used for image segmentation and canny edge detection
import math
import matplotlib.pyplot as plt
import numpy as np

from pygame import mixer #used for sound effects
import webbrowser #used for hyperlinking 

#import numpy as np
#import os
#import sys
#from matplotlib import pyplot as plt
''' All sound files that were used were found from 
https://freesound.org/ '''

''' image citations:
brain background image - https://hominidpost.com/cool-facts-about-the-human-brain-you-might-not-know/
brain image - https://aroundwellington.com/brainy-days-2019/
skull image - https://www.thinglink.com/scene/862729415476379648
ankle image - https://teachmeanatomy.info/lower-limb/joints/ankle-joint/
ribs image -  https://teachmeanatomy.info/thorax/bones/ribcage/
hand image - https://geekymedics.com/bones-of-the-hand/
'''

#beginning screen
class SplashScreenMode(Mode):
    def appStarted(mode):
        #loading background brain image
        mode.greyRaw = mode.loadImage('greys.jpg')
        mode.greyScaled = mode.scaleImage(mode.greyRaw,.4)

    def redrawAll(mode, canvas):
        #drawing all components of starting screen: buttons, text, etc
        mode.greyX, mode.greyY = mode.width/2,mode.height/2
        font = 'Arial 26 bold'
        canvas.create_rectangle(0,0,mode.width,mode.height,fill = 'yellow')
        canvas.create_image(mode.greyX, mode.greyY, 
            image=ImageTk.PhotoImage(mode.greyScaled))
        canvas.create_text(mode.width/2,200,text='Welcome to Greys101!!',\
            font=font)
        #drawing the Let's Study Button
        mode.goLX,mode.goRX = 50,200
        mode.goLY,mode.goRY = 300,350
        canvas.create_rectangle(mode.goLX,mode.goLY,mode.goRX,\
            mode.goRY,fill ='light green',outline = 'black',width = 3)
        #drawing the How does this work Button
        mode.hLX,mode.hRX = 300,450
        mode.hLY,mode.hRY = 300,350
        canvas.create_rectangle(mode.hLX,mode.hLY,mode.hRX,\
            mode.hRY,fill ='pink',outline='black',width = 3)
        canvas.create_text((mode.goRX+mode.goLX)/2,(mode.goRY+mode.goLY)/2\
            ,text = 'Lets Study', font = 'Arial 14 bold')
        canvas.create_text((mode.hRX+mode.hLX)/2,(mode.hRY+mode.hLY)/2\
            ,text = 'How does this work?', font = 'Arial 14 bold')
    
    def mousePressed(mode,event):
        if (mode.goLX<event.x<mode.goRX) and (mode.goLY<event.y<mode.goRY):
            #switch modes if the Lets Study button is clicked
            mode.app.setActiveMode(mode.app.gamePlayMode)
            #mixer is how the music is played
            mixer.init()
            mixer.music.load('begin.mp3')
            mixer.music.play()
        elif (mode.hLX<event.x<mode.hRX) and (mode.hLY<event.y<mode.hRY):
            #switch modes if the How does this work button is clicked
            mode.app.setActiveMode(mode.app.helpMode)

#Game Mode 1 Screen
class GamePlayMode(Mode):
    def redrawAll(mode,canvas):
        #background color
        canvas.create_rectangle(0,0,mode.width,mode.height,fill = 'light green')
        canvas.create_text(mode.width/2,25,text = 'Game Mode 1', font = 'Arial 18 bold')
        buttonFont = 'Arial 12 bold'
        canvas.create_text(mode.width/2,50,\
            text='Choose the anatomy that you would like to study',\
            font = 'Arial 18 bold')
        #dimensions for the left column of buttons
        mode.lRowX1, mode.lRowX2 = 50,200
        mode.c1LY,mode.c1RY = 100,150
        #creating the left column of buttons; each spaced by 100 vertically
        canvas.create_rectangle(mode.lRowX1,mode.c1LY,mode.lRowX2,mode.c1RY,\
            fill = 'light blue', outline = 'black', width = 3)
        canvas.create_rectangle(mode.lRowX1,mode.c1LY+100,mode.lRowX2,\
            mode.c1RY+100, fill = 'light blue',outline='black',width =3)
        canvas.create_rectangle(mode.lRowX1,mode.c1LY+200,mode.lRowX2,\
            mode.c1RY+200,fill = 'light blue', outline = 'black',width = 3)
        #dimensions for the right column of buttons
        mode.rRowX1,mode.rRowX2 = 300,450
        mode.c2LY,mode.c2RY = 100,150
        #creating the right column of buttons; each spaced by 100 vertically
        canvas.create_rectangle(mode.rRowX1,mode.c2LY,mode.rRowX2,mode.c2RY,\
            fill = 'light blue', outline = 'black', width = 3)
        canvas.create_rectangle(mode.rRowX1,mode.c2LY+100,mode.rRowX2,\
            mode.c2RY + 100,fill = 'light blue', outline = 'black', width = 3)
        canvas.create_rectangle(mode.rRowX1,mode.c2LY+200,mode.rRowX2,\
            mode.c2RY + 200,fill = 'light blue', outline = 'black', width = 3)
        #left column buttons text
        canvas.create_text((mode.lRowX1 + mode.lRowX2)/2,\
            (mode.c1LY+mode.c1RY)/2, text='Brain',font=buttonFont)
        canvas.create_text((mode.lRowX1 + mode.lRowX2)/2,\
            (mode.c1LY+100+mode.c1RY+100)/2,text='Hand',font=buttonFont)
        canvas.create_text((mode.lRowX1 + mode.lRowX2)/2,\
            (mode.c1LY+200+mode.c1RY+200)/2,text='Ankle',font=buttonFont)   
        #right column buttons text
        canvas.create_text((mode.rRowX1+mode.rRowX2)/2,\
            (mode.c2LY+mode.c2RY)/2,text='Spine',font=buttonFont)
        canvas.create_text((mode.rRowX1+mode.rRowX2)/2,\
            (mode.c2LY+100+mode.c2RY+100)/2,text='Skull',font=buttonFont)
        canvas.create_text((mode.rRowX1+mode.rRowX2)/2,\
            (mode.c2LY+200+mode.c2RY+200)/2,text='Ribs',font=buttonFont)
        #dimensions for the back button
        mode.bLX,mode.bRX = 175,300
        mode.bLY,mode.bRY = 425,475
        #creating the back buttons
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        #back button text
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
        #dimensions for the reverse button
        mode.cx,mode.cy = 400,450 
        mode.r = 38
        canvas.create_oval(mode.cx-mode.r,mode.cy-mode.r,mode.cx+mode.r,\
            mode.cy+mode.r,fill = 'yellow',outline = 'black',width =3)
        canvas.create_text(mode.cx,mode.cy,text = 'Reverse',\
            font = 'Arial 14 bold')

    def mousePressed(mode,event):
        #switch screen based off of the button(anatomy) that is selected
        if (mode.lRowX1<event.x<mode.lRowX2) and (mode.c1LY<event.y<mode.c1RY):
            mode.app.setActiveMode(mode.app.brainMode)
        elif(mode.rRowX1<event.x<mode.rRowX2) and (mode.c2LY<event.y<mode.c2RY):
            mode.app.setActiveMode(mode.app.spineMode)
        elif (mode.rRowX1<event.x<mode.rRowX2) and\
            (mode.c2LY+100<event.y<mode.c2RY+100):
            mode.app.setActiveMode(mode.app.skullMode)
        elif (mode.lRowX1<event.x<mode.lRowX2) and\
             (mode.c1LY+200<event.y<mode.c1RY+200):
            mode.app.setActiveMode(mode.app.ankleMode)
        elif (mode.lRowX1<event.x<mode.lRowX2) and\
            (mode.c1LY+100<event.y<mode.c1RY+100):
            mode.app.setActiveMode(mode.app.handMode)
        elif (mode.rRowX1<event.x<mode.rRowX2) and\
            (mode.c2LY+200<event.y<mode.c2RY+200):
            mode.app.setActiveMode(mode.app.ribsMode)
        elif (mode.bLX<event.x<mode.bRX) and (mode.bLY<event.y<mode.bRY):
            mode.app.setActiveMode(mode.app.splashScreenMode)
        elif (mode.cx-mode.r<event.x<mode.cx+mode.r) and (mode.cy-mode.r<\
            event.y<mode.cy+mode.r):
            mixer.init()
            mixer.music.load('plop.mp3')
            mixer.music.play()
            mode.app.setActiveMode(mode.app.reverseGamePlayMode)

#Game Mode 2 Screen
class ReverseGamePlayMode(Mode): 
    def redrawAll(mode,canvas):
        #background color
        canvas.create_rectangle(0,0,mode.width,mode.height,fill = 'light blue')
        canvas.create_text(mode.width/2,25,text = 'Game Mode 2', font = 'Arial 18 bold')
        buttonFont = 'Arial 12 bold'
        canvas.create_text(mode.width/2,50,\
            text='Choose the anatomy that you would like to study',\
            font = 'Arial 16 bold')
        #dimensions for the left column of buttons
        mode.lRowX1, mode.lRowX2 = 50,200
        mode.c1LY,mode.c1RY = 100,150
        #creating the left column of buttons; each spaced by 100 vertically
        canvas.create_rectangle(mode.lRowX1,mode.c1LY,mode.lRowX2,mode.c1RY,\
            fill = 'light green', outline = 'black', width = 3)
        canvas.create_rectangle(mode.lRowX1,mode.c1LY+100,mode.lRowX2,\
            mode.c1RY+100, fill = 'light green',outline='black',width =3)
        canvas.create_rectangle(mode.lRowX1,mode.c1LY+200,mode.lRowX2,\
            mode.c1RY+200,fill = 'light green', outline = 'black',width = 3)
        #dimensions for the right column of buttons
        mode.rRowX1,mode.rRowX2 = 300,450
        mode.c2LY,mode.c2RY = 100,150
        #creating the right column of buttons; each spaced by 100 vertically
        canvas.create_rectangle(mode.rRowX1,mode.c2LY,mode.rRowX2,mode.c2RY,\
            fill = 'light green', outline = 'black', width = 3)
        canvas.create_rectangle(mode.rRowX1,mode.c2LY+100,mode.rRowX2,\
            mode.c2RY + 100,fill = 'light green', outline = 'black', width = 3)
        canvas.create_rectangle(mode.rRowX1,mode.c2LY+200,mode.rRowX2,\
            mode.c2RY + 200,fill = 'light green', outline = 'black', width = 3)
        #left column buttons text
        canvas.create_text((mode.lRowX1 + mode.lRowX2)/2,\
            (mode.c1LY+mode.c1RY)/2, text='Brain',font=buttonFont)
        canvas.create_text((mode.lRowX1 + mode.lRowX2)/2,\
            (mode.c1LY+100+mode.c1RY+100)/2,text='Hand',font=buttonFont)
        canvas.create_text((mode.lRowX1 + mode.lRowX2)/2,\
            (mode.c1LY+200+mode.c1RY+200)/2,text='Ankle',font=buttonFont)   
        #right column buttons text
        canvas.create_text((mode.rRowX1+mode.rRowX2)/2,\
            (mode.c2LY+mode.c2RY)/2,text='Spine',font=buttonFont)
        canvas.create_text((mode.rRowX1+mode.rRowX2)/2,\
            (mode.c2LY+100+mode.c2RY+100)/2,text='Skull',font=buttonFont)
        canvas.create_text((mode.rRowX1+mode.rRowX2)/2,\
            (mode.c2LY+200+mode.c2RY+200)/2,text='Ribs',font=buttonFont)
        #dimensions for the back button
        mode.bLX,mode.bRX = 175,300
        mode.bLY,mode.bRY = 425,475
        #creating the back buttons
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        #back button text
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
        #dimensions for the unreverse button
        mode.cx,mode.cy = 400,450 
        mode.r = 38
        canvas.create_oval(mode.cx-mode.r,mode.cy-mode.r,mode.cx+mode.r,\
            mode.cy+mode.r,fill = 'yellow',outline = 'black',width =3)
        canvas.create_text(mode.cx,mode.cy,text = 'Unreverse',\
            font = 'Arial 14 bold')

    def mousePressed(mode,event):
        #switch screen based off of the button(anatomy) that is selected
        if (mode.lRowX1<event.x<mode.lRowX2) and (mode.c1LY<event.y<mode.c1RY):
            mode.app.setActiveMode(mode.app.reverseBrainMode)
        elif (mode.rRowX1<event.x<mode.rRowX2) and (mode.c2LY<event.y<mode.c2RY):
            mode.app.setActiveMode(mode.app.reverseSpineMode)
        elif (mode.rRowX1<event.x<mode.rRowX2) and\
            (mode.c2LY+100<event.y<mode.c2RY+100):
            mode.app.setActiveMode(mode.app.reverseSkullMode)
        elif (mode.lRowX1<event.x<mode.lRowX2) and\
             (mode.c1LY+200<event.y<mode.c1RY+200):
            mode.app.setActiveMode(mode.app.reverseAnkleMode)
        elif (mode.lRowX1<event.x<mode.lRowX2) and\
            (mode.c1LY+100<event.y<mode.c1RY+100):
            mode.app.setActiveMode(mode.app.reverseHandMode)
        elif (mode.rRowX1<event.x<mode.rRowX2) and\
            (mode.c2LY+200<event.y<mode.c2RY+200):
            mode.app.setActiveMode(mode.app.reverseRibsMode)
        elif (mode.bLX<event.x<mode.bRX) and (mode.bLY<event.y<mode.bRY):
            mode.app.setActiveMode(mode.app.splashScreenMode)
        elif (mode.cx-mode.r<event.x<mode.cx+mode.r) and (mode.cy-mode.r<\
            event.y<mode.cy+mode.r):
            mixer.init()
            mixer.music.load('plop.mp3')
            mixer.music.play()
            mode.app.setActiveMode(mode.app.gamePlayMode)

#screen for Brain Anatomy
class BrainMode(Mode):
    def appStarted(mode):
        #defining all booleans and parts
        mode.start = False
        mode.frontalLobe = 'Frontal Lobe'
        mode.occipitalLobe = 'Occipital Lobe'
        mode.parietalLobe = 'Parietal Lobe'
        mode.temporalLobe = 'Temporal Lobe'
        mode.found = False
        #list of parts
        mode.partList = ['Frontal Lobe','Occipital Lobe','Parietal Lobe',\
            'Temporal Lobe']
        mode.totalParts = len(mode.partList)
        #attempts will be used for accuracy score calculations
        mode.attempts = 0
        mode.currentPart = mode.partList[0]
        #loading and scaling brain image for the screen
        mode.brainRaw = mode.loadImage('brain.jpg')
        mode.brainScaled = mode.scaleImage(mode.brainRaw,1.2)
        #dimensions of the image
        mode.imageRows = 300
        mode.imageCols = 215
        #image location on screen
        mode.brainX, mode.brainY = mode.width/2, mode.height/2
        #OpenCV...reading the image
        mode.brainImage=cv.imread('/Users/vikasmalik/Desktop/TP/brain.jpg')
        mode.brainImage = cv.cvtColor(mode.brainImage, cv.COLOR_BGR2RGB)
        '''ColorSpace ImageSegmentation
            Learned from: https://realpython.com/python-opencv-color-spaces/
            This also where I was influenced to use snake_case for my code
            Here they taught the entire color segmentiation but also how to apply
            it on a larger scale
        '''
        light_front = (242,130,89)
        dark_front = (97,25,28)
        #The mask creates an array of 1's,0's. 1's representing when that 
        #the color in that range exists and 0's for when it doesn't
        mode.red_mask = cv.inRange(mode.brainImage, dark_front, light_front)
        light_occipital= (115,174,174)
        dark_occipital = (58,103,10)
        mode.green_mask = cv.inRange(mode.brainImage,dark_occipital,\
            light_occipital)
        light_temporal = (238,248,136)
        dark_temporal = (140,124,48)
        mode.yellow_mask=cv.inRange(mode.brainImage,dark_temporal,\
            light_temporal)
        light_parietal = (197,170,249)
        dark_parietal = (48,21,56)
        mode.purple_mask=cv.inRange(mode.brainImage,dark_parietal,\
            light_parietal)
        #Here we are combining the masks so that we can consider all the colors
        #that we care about
        final_mask=mode.purple_mask+ mode.green_mask+mode.yellow_mask+\
            mode.red_mask
        #this imposes the mask upon the original image
        #for every pixel, in the original image, that has a value of 1 that 
        #pixel is kept
        result = cv.bitwise_and(mode.brainImage,mode.brainImage,mask=final_mask)
        #using Canny Algorithm to get edges
        mode.brainEdges = cv.Canny(mode.brainImage,50,200)
    def redrawAll(mode,canvas):
        #drawing the image onto the canvas
        canvas.create_image(mode.brainX, mode.brainY, 
        image=ImageTk.PhotoImage(mode.brainScaled))
        canvas.create_text(mode.width/2,50,\
            text='How well do you know the brain?',font='Arial 16 bold')
        #creating start button
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
        #creating back button
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
    def mousePressed(mode,event):
        #switching screens if the back button selected
        if (mode.bLX<event.x<mode.bRX) and (mode.bLY<event.y<mode.bRY):
            mode.start = False
            mode.app.setActiveMode(mode.app.gamePlayMode)
        #Checks if the game has started
        elif mode.start == True:
            #checks what part the player was asked to find
            if mode.currentPart == mode.frontalLobe:
                #converting x,y for OpenCV form tkinter
                event.x = event.x - int((mode.width - mode.imageRows)//2) 
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                #checking 5 pixels around it in every direction
                for x in range(5):
                    for y in range(5):
                        #out of bounds check
                        if event.x+x > 300 or event.y+y > 215:
                            break
                        if 255 ==mode.red_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255== mode.red_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.red_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.red_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.occipitalLobe:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 300 or event.y+y > 215:
                            break
                        if 255 == mode.green_mask[event.y+y][event.x+x] :
                            mode.found = True
                        elif 255 == mode.green_mask[event.y+y][event.x-x] :
                            mode.found = True
                        elif 255 == mode.green_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.green_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.temporalLobe:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x >300 or event.y+y >215:
                            break
                        if 255 == mode.yellow_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.yellow_mask[event.y-y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.yellow_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.yellow_mask[event.y+y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.parietalLobe:
                event.x = event.x - int((mode.width - mode.imageRows)//2) 
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 300 or event.y+y > 215:
                            break
                        if 255 == mode.purple_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.purple_mask[event.y-y][event.x-x] :
                            mode.found = True
                        elif 255 == mode.purple_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.purple_mask[event.y+y][event.x-x]:
                            mode.found =  True
            #Checks if part was found
            if mode.found == False:
                mixer.init()
                mixer.music.load('incorrect.mp3')
                mixer.music.play()
                messagebox.showinfo('Wrong', 'Try Again')
                mode.attempts +=1
            else:
                mixer.init()
                mixer.music.load('correct.mp3')
                mixer.music.play()
                messagebox.showinfo('Correct','Found Part!')
                mode.attempts +=1
                mode.found = False
                mode.partList.pop(0)
                #Checks if the game is over
                if mode.partList != []:
                    mode.currentPart = mode.partList[0]
                    messagebox.showinfo('Message',\
                        f'Find the {mode.currentPart}')
                else:
                    mixer.init()
                    mixer.music.load('applause.mp3')
                    mixer.music.play()
                    messagebox.showinfo('Congratulations','Found all parts!')
                    #accuracy score
                    messagebox.showinfo('Accuracy Score',f'{(mode.totalParts/mode.attempts)*100}%')
                    mode.attempts = 0
                    #resets PartList if level is played again
                    mode.partList = ['Frontal Lobe','Occipital Lobe',\
                        'Parietal Lobe', 'Temporal Lobe']
                    mode.start = False
                    mode.app.setActiveMode(mode.app.gamePlayMode)
        #Checks if the player clicks the getStarted Button
        elif (mode.gsLX<event.x<mode.gsRX) and (mode.gsLY<event.y<mode.gsRY):
            #switches the boolean
            mode.start = True
            mode.currentPart = mode.partList[0]
            messagebox.showinfo('Message',f'Find the {mode.currentPart}')

#screen for Spine Anatomy
class SpineMode(Mode):
    def appStarted(mode):
        #loading and scaling spine image for the screen
        #https://www.innerbody.com/anatomy/skeletal/thoracic-vertebrae-lateral
        #(image citation)
        mode.spineRaw = mode.loadImage('spine.jpeg')
        mode.spineScaled = mode.scaleImage(mode.spineRaw,.5)
        #image location on screen
        mode.spineX = mode.width/2
        mode.spineY = mode.height/2
        #OpenCV...reading the image
        mode.spineImage = cv.imread('/Users/vikasmalik/Desktop/TP/spine.jpeg')
        mode.spineImage = cv.cvtColor(mode.spineImage, cv.COLOR_BGR2RGB)
        #Creating all masks for the image segmeentation
        light_cervical = (196,208,118)
        dark_cervical = (109,50,32)
        mode.cervical_mask = cv.inRange(mode.spineImage,dark_cervical,\
            light_cervical)
        light_thoracic = (128,126,210)
        dark_thoracic = (51,44,124)
        mode.thoracic_mask = cv.inRange(mode.spineImage,dark_thoracic,\
            light_thoracic)
        light_lumber = (237,231,153)
        dark_lumber = (171,166,59)
        mode.lumber_mask = cv.inRange(mode.spineImage,dark_lumber,light_lumber)
        light_sacrum = (124,197,124)
        dark_sacrum = (65,136,58)
        mode.sacrum_mask = cv.inRange(mode.spineImage,dark_sacrum,light_sacrum)
        light_coccyx = (211,139,210)
        dark_coccyx = (148,113,139)
        mode.coccyx_mask = cv.inRange(mode.spineImage,dark_coccyx,light_coccyx)
        #combining all masks
        final_mask = mode.cervical_mask+mode.coccyx_mask+mode.lumber_mask+\
            mode.thoracic_mask
        #overlaying the masks
        result = cv.bitwise_and(mode.spineImage,mode.spineImage,mask=final_mask)

        mode.imageRows = 393
        mode.imageCols = 708
        mode.start = False
        mode.lumber = 'Lumber'
        mode.cervical = 'Cervical'
        mode.thoracic = 'Thoracic'
        mode.coccyx = 'Coccyx'
        mode.sacrum = 'Sacrum'
        mode.partList = ['Lumber','Thoracic','Sacrum','Coccyx','Cervical']
        mode.totalParts = len(mode.partList)
        mode.attempts = 0
        mode.currentPart = mode.partList[0]
        mode.found = False
        plt.subplot(1, 2, 1)
        plt.imshow(mode.spineImage, cmap= 'gray')
        plt.subplot(1, 2, 2)
        plt.imshow(result)
        plt.show()


    def redrawAll(mode,canvas):
        #drawing the image onto the canvas
        canvas.create_image(mode.spineX,mode.spineY,
        image = ImageTk.PhotoImage(mode.spineScaled))
        canvas.create_text(mode.width/2,50,\
            text='Have you mastered the spine?',font='Arial 16 bold')
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')

    def mousePressed(mode,event):
        if (mode.bLX<event.x<mode.bRX) and (mode.bLY<event.y<mode.bRY):
            mode.app.setActiveMode(mode.app.gamePlayMode)
        #Checking the player has started the game
        elif mode.start == True:
            #Checking what part they player is asked about
            if mode.currentPart == mode.lumber:
                event.x = event.x - int((mode.width - mode.imageRows)//2 )
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                #checking if the pixels around the click are in the right part
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 393 or event.y+y > 708:
                            break
                        if 255 == mode.lumber_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.lumber_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.lumber_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.lumber_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.thoracic:
                event.x = event.x - int((mode.width - mode.imageRows)//2 )
                event.y = event.y - int((mode.height - mode.imageCols)//2) 
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 393 or event.y+y > 708:
                            break
                        if 255 == mode.thoracic_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.thoracic_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.thoracic_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.thoracic_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.coccyx:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 393 or event.y+y > 708:
                            break
                        if 255 == mode.coccyx_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.coccyx_mask[event.y-y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.coccyx_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.coccyx_mask[event.y+y][event.x-x] :
                            mode.found = True
            elif mode.currentPart == mode.cervical:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 393 or event.y+y > 708:
                            break
                        if 255 == mode.cervical_mask[event.y+y][event.x+x] :
                            mode.found = True
                        elif 255 == mode.cervical_mask[event.y-y][event.x-x] :
                            mode.found = True
                        elif 255 == mode.cervical_mask[event.y-y][event.x+x] :
                            mode.found = True
                        elif 255 == mode.cervical_mask[event.y+y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.sacrum:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 393 or event.y+y > 708:
                            break
                        if 255 == mode.sacrum_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.sacrum_mask[event.y-y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.sacrum_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.sacrum_mask[event.y+y][event.x-x]:
                            mode.found = True
            #Checks if the part was found or not
            if mode.found == False:
                mixer.init()
                mixer.music.load('incorrect.mp3')
                mixer.music.play()
                messagebox.showinfo('Wrong', 'Try Again')    
                mode.attempts +=1        
            else:
                mixer.init()
                mixer.music.load('correct.mp3')
                mixer.music.play()
                messagebox.showinfo('Correct','Found Part!')
                mode.attempts +=1
                mode.found = False
                mode.partList.pop(0)
                #Checks if the game is over or not
                if mode.partList != []:
                    mode.currentPart = mode.partList[0]
                    messagebox.showinfo('Message',\
                        f'Find the {mode.currentPart}')
                #resets partList if the level is played again
                else:
                    mixer.init()
                    mixer.music.load('applause.mp3')
                    mixer.music.play()
                    messagebox.showinfo('Congratulations','Found all parts!')
                    messagebox.showinfo('Accuracy Score',f'{(mode.totalParts/mode.attempts)*100}%')
                    mode.attempts = 0
                    mode.start = False
                    mode.partList = ['Lumber','Cervical','Thoracic','Coccyx',\
                        'Sacrum']
                    mode.app.setActiveMode(mode.app.gamePlayMode)
        #Checking if the player clicks the getStarted Button
        elif(mode.gsLX<event.x<mode.gsRX) and (mode.gsLY<event.y<mode.gsRY):
            #switching boolean
            mode.start = True
            mode.currentPart = mode.partList[0]
            messagebox.showinfo('Message',f'Find the {mode.currentPart}')

#screen for Skull Anatomy
class SkullMode(Mode):
    def appStarted(mode):
        #https://www.innerbody.com/image/skel16.html (image citation)
        mode.skullRaw = mode.loadImage('skull.png')
        mode.skullScaled = mode.scaleImage(mode.skullRaw,.8)
        mode.skullX=mode.width/2
        mode.skullY=mode.height/2
        mode.skullImage = cv.imread('/Users/vikasmalik/Desktop/TP/skull.png')
        mode.skullEdges = cv.Canny(mode.skullImage,50,200)
        mode.skullImage = cv.cvtColor(mode.skullImage, cv.COLOR_BGR2RGB)
        mode.attempts = 0
        #print(hsv_skull)
        #print(mode.skullImage)
        light_sphenoid = (195,189,93)
        dark_sphenoid =  (152,46,50)
        mode.sphenoid_mask = cv.inRange(mode.skullImage,dark_sphenoid,\
            light_sphenoid)
        light_frontal = (249,173,151)
        dark_frontal = (147,72,56)
        mode.frontal_mask = cv.inRange(mode.skullImage,dark_frontal,\
            light_frontal)
        light_maxilla = (189,141,183)
        dark_maxilla = (106,58,100)
        mode.maxilla_mask = cv.inRange(mode.skullImage,dark_maxilla,\
            light_maxilla)
        light_zygomatic = (121,167,200)
        dark_zygomatic = (35,81,114)
        mode.zygomatic_mask = cv.inRange(mode.skullImage,dark_zygomatic,\
            light_zygomatic)
        final_mask = mode.maxilla_mask+mode.zygomatic_mask+mode.frontal_mask
        result =cv.bitwise_and(mode.skullImage,mode.skullImage,mask=final_mask)
        mode.start = False
        mode.frontalBone = 'Frontal Bone'
        mode.sphenoidBone = 'Sphenoid Bone'
        mode.maxillaBone = 'Maxilla Bone'
        mode.zygomaticBone = 'Zygomatic Bone'
        mode.partList = ['Zygomatic Bone','Maxilla Bone','Sphenoid Bone',\
            'Frontal Bone']
        mode.totalParts = len(mode.partList)
        mode.currentPart = mode.partList[0]
        mode.found = False
        #plt.subplot(1, 2, 1)
        #plt.imshow(mode.skullImage, cmap= 'gray')
        #plt.subplot(1, 2, 2)
        #plt.imshow(result)
        #plt.show()
        mode.imageRows = 398
        mode.imageCols = 490


    def redrawAll(mode,canvas):
        #drawing the image onto the screen
        canvas.create_image(mode.skullX,mode.skullY,
        image = ImageTk.PhotoImage(mode.skullScaled))
        canvas.create_text(mode.width/2,50,\
            text='Lets see if you skulld to study?',font='Arial 16 bold')
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')

    def mousePressed(mode,event):
        if (mode.bLX<event.x<mode.bRX) and (mode.bLY<event.y<mode.bRY):
            mode.app.setActiveMode(mode.app.gamePlayMode)
        #once the player has started the game
        elif mode.start == True:
            #checking what part they were asked about
            if mode.currentPart == mode.frontalBone:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2) 
                #checking around the pixel that they clicked on
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 398 or event.y+y > 490:
                            break
                        if 255 == mode.frontal_mask[event.y+y][event.x+x] :
                            mode.found = True
                        elif 255 == mode.frontal_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.frontal_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.frontal_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.maxillaBone:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 398 or event.y+y > 490:
                            break
                        if 255 == mode.maxilla_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.maxilla_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.maxilla_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.maxilla_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.sphenoidBone:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 398 or event.y+y > 490:
                            break
                        if 255 == mode.sphenoid_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.sphenoid_mask[event.y-y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.sphenoid_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.sphenoid_mask[event.y+y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.zygomaticBone:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 398 or event.y+y > 490:
                            break
                        if 255 == mode.zygomatic_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.zygomatic_mask[event.y-y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.zygomatic_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.zygomatic_mask[event.y+y][event.x-x]:
                            mode.found = True
            #based off of if a part was found or not
            if mode.found == False:
                mixer.init()
                mixer.music.load('incorrect.mp3')
                mixer.music.play()
                messagebox.showinfo('Wrong', 'Try Again') 
                mode.attempts +=1
            else:
                mixer.init()
                mixer.music.load('correct.mp3')
                mixer.music.play()
                messagebox.showinfo('Correct','Found Part!')
                mode.attempts +=1
                mode.found = False
                mode.partList.pop(0)
                #Checking if the level was complete or not
                if mode.partList != []:
                    mode.currentPart = mode.partList[0]
                    messagebox.showinfo('Message',\
                        f'Find the {mode.currentPart}')
                else:
                    mixer.init()
                    mixer.music.load('applause.mp3')
                    mixer.music.play()
                    messagebox.showinfo('Congratulations','Found all parts!')
                    messagebox.showinfo('Accuracy Score',f'{(mode.totalParts/mode.attempts)*100}%')
                    mode.attempts = 0
                    mode.start = False
                    #resetting partList if level is played again
                    mode.partList=['Frontal Bone','Sphenoid Bone',\
                        'Temporal Bone']
                    mode.app.setActiveMode(mode.app.gamePlayMode)
        #checking if the get started button was clicked
        elif(mode.gsLX<event.x<mode.gsRX) and (mode.gsLY<event.y<mode.gsRY):
            #switching the boolean
            mode.start = True
            mode.currentPart = mode.partList[0]
            messagebox.showinfo('Message',f'Find the {mode.currentPart}')

#screen for Forearm anatomy
class AnkleMode(Mode):
    def appStarted(mode):
        #https://www.kenhub.com/en/library/anatomy/arches-of-the-foot 
        #(image citation)
        mode.start = False
        mode.found = False
        mode.ankleRaw = mode.loadImage('ankle.jpg')
        mode.ankleScaled = mode.scaleImage(mode.ankleRaw,.8)
        mode.ankleX = mode.width/2
        mode.ankleY = mode.height/2
        mode.ankleImage= cv.imread('/Users/vikasmalik/Desktop/TP/ankle.jpg')
        mode.ankleImage = cv.cvtColor(mode.ankleImage, cv.COLOR_BGR2RGB)
        mode.ankleEdges = cv.Canny(mode.ankleImage,50,200)
        mode.partList = ['Talus','Tibia','Fibula','Calcaneus']
        mode.totalParts = len(mode.partList)
        mode.attempts = 0
        mode.talus = 'Talus'
        mode.tibia = 'Tibia'
        mode.fibula = 'Fibula'
        mode.calcaneus = 'Calcaneus'
        mode.imageRows = 200
        mode.imageCols = 452

        light_talus = (254,254,154)
        dark_talus = (147,148,46)
        mode.talus_mask = cv.inRange(mode.ankleImage,dark_talus,light_talus)

        light_tibia = (249,146,147)
        dark_tibia = (154,51,52)
        mode.tibia_mask = cv.inRange(mode.ankleImage,dark_tibia,light_tibia)

        light_fibula = (152,217,183)
        dark_fibula = (51,118,83)
        mode.fibula_mask = cv.inRange(mode.ankleImage,dark_fibula,light_fibula)

        light_calcaneus = (147,193,224)
        dark_calcaneus = (83,128,159)
        mode.calcaneus_mask = cv.inRange(mode.ankleImage,dark_calcaneus,light_calcaneus)

        final_mask = mode.talus_mask + mode.tibia_mask + mode.fibula_mask + mode.calcaneus_mask
        result =cv.bitwise_and(mode.ankleImage,mode.ankleImage,mask=final_mask)
        #plt.subplot(1, 2, 1)
        #plt.imshow(mode.ankleImage, cmap= 'gray')
        #plt.subplot(1, 2, 2)
        #plt.imshow(result)
        #plt.show()

    def redrawAll(mode,canvas):
        canvas.create_image(mode.ankleX,mode.ankleY,
        image = ImageTk.PhotoImage(mode.ankleScaled))
        canvas.create_text(mode.width/2,50,\
            text='Have you mastered the ankle?',font='Arial 16 bold')
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
        #creating back button
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')

    def mousePressed(mode,event):
        if (mode.bLX<event.x<mode.bRX) and (mode.bLY<event.y<mode.bRY):
            mode.app.setActiveMode(mode.app.gamePlayMode)
        elif mode.start == True:
            #checking what part they were asked about
            if mode.currentPart == mode.talus:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2) 
                #checking around the pixel that they clicked on
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 200 or event.y+y > 452:
                            break
                        if 255 == mode.talus_mask[event.y+y][event.x+x] :
                            mode.found = True
                        elif 255 == mode.talus_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.talus_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.talus_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.tibia:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 200 or event.y+y > 452:
                            break
                        if 255 == mode.tibia_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.tibia_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.tibia_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.tibia_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.fibula:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 200 or event.y+y > 452:
                            break
                        if 255 == mode.fibula_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.fibula_mask[event.y-y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.fibula_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.fibula_mask[event.y+y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.calcaneus:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 200 or event.y+y > 452:
                            break
                        if 255 == mode.calcaneus_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.calcaneus_mask[event.y-y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.calcaneus_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.calcaneus_mask[event.y+y][event.x-x]:
                            mode.found = True
            #based off of if a part was found or not
            if mode.found == False:
                mixer.init()
                mixer.music.load('incorrect.mp3')
                mixer.music.play()
                messagebox.showinfo('Wrong', 'Try Again') 
                mode.attempts +=1
            else:
                mixer.init()
                mixer.music.load('correct.mp3')
                mixer.music.play()
                messagebox.showinfo('Correct','Found Part!')
                mode.attempts +=1
                mode.found = False
                mode.partList.pop(0)
                #Checking if the level was complete or not
                if mode.partList != []:
                    mode.currentPart = mode.partList[0]
                    messagebox.showinfo('Message',\
                        f'Find the {mode.currentPart}')
                else:
                    mixer.init()
                    mixer.music.load('applause.mp3')
                    mixer.music.play()
                    messagebox.showinfo('Congratulations','Found all parts!')
                    messagebox.showinfo('Accuracy Score',f'{(mode.totalParts/mode.attempts)*100}%')
                    mode.attempts = 0
                    mode.start = False
                    #resetting partList if level is played again
                    mode.partList=['Talus','Tibia','Fibula','Calcaneus']
                    mode.app.setActiveMode(mode.app.gamePlayMode)
        #checking if the get started button was clicked
        elif(mode.gsLX<event.x<mode.gsRX) and (mode.gsLY<event.y<mode.gsRY):
            #switching the boolean
            mode.start = True
            mode.currentPart = mode.partList[0]
            messagebox.showinfo('Message',f'Find the {mode.currentPart}')
            
#screen for Hand Anatomy
class HandMode(Mode):
    def appStarted(mode):
        #https://www.innerbody.com/image/skel13.html(image citation)
        mode.handRaw = mode.loadImage('hand.jpg')
        mode.handScaled = mode.scaleImage(mode.handRaw,.9)
        mode.handX = mode.width/2
        mode.handY = mode.height/2
        mode.handImage = cv.imread('/Users/vikasmalik/Desktop/TP/hand.jpg')
        mode.handImage = cv.cvtColor(mode.handImage, cv.COLOR_BGR2RGB)
        mode.handEdges = cv.Canny(mode.handImage,50,200)
        mode.imageRows = 305
        mode.imageCols = 369

        mode.metacarple = 'Metacarple'
        mode.proximal = 'Proximal'
        mode.middle = 'Middle'
        mode.digital = 'Digital'
        mode.partList = ['Proximal','Middle','Digital','Metacarple']
        mode.totalParts = len(mode.partList)
        mode.attempts = 0
        mode.currentPart = mode.partList[0]
        mode.found = False
        mode.start = False

        light_metacarple = (247,217,150)
        dark_metacarple = (220,194,104)
        mode.metacarple_mask = cv.inRange(mode.handImage,dark_metacarple,\
            light_metacarple)

        light_proximal = (219,237,191)
        dark_proximal = (187,218,137)
        mode.proximal_mask = cv.inRange(mode.handImage,dark_proximal,\
            light_proximal)

        light_middle=(180,218,241)
        dark_middle= (118,181,222)
        mode.middle_mask = cv.inRange(mode.handImage,dark_middle,light_middle)

        light_digital = (255,205,177)
        dark_digital = (239,148,111)
        mode.digital_mask = cv.inRange(mode.handImage,dark_digital,\
            light_digital)
        
        final_mask = mode.digital_mask+mode.middle_mask+mode.proximal_mask

        result = cv.bitwise_and(mode.handImage,mode.handImage,mask=final_mask)

        #plt.subplot(1, 2, 1)
        #plt.imshow(mode.handImage, cmap= 'gray')
        #plt.subplot(1, 2, 2)
        #plt.imshow(result)
        #plt.show()

    def redrawAll(mode,canvas):
        canvas.create_image(mode.handX,mode.handY,
        image = ImageTk.PhotoImage(mode.handScaled))
        canvas.create_text(mode.width/2,50,\
            text='Can you hand-le this?',font='Arial 16 bold')
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
    def mousePressed(mode,event):
        if (mode.bLX<event.x<mode.bRX) and (mode.bLY<event.y<mode.bRY):
            mode.app.setActiveMode(mode.app.gamePlayMode)
        elif mode.start == True:
            if mode.currentPart == mode.digital:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 305 or event.y+y > 369:
                            break
                        if 255 == mode.digital_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.digital_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.digital_mask[event.y-y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.digital_mask[event.y-y][event.x+x]:
                            mode.found = True
            elif mode.currentPart == mode.middle:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 305 or event.y+y > 369:
                            break
                        if 255 == mode.middle_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.middle_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.middle_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.middle_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.metacarple:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(10):
                    for y in range(10):
                        if event.x+x > 305 or event.y+y > 369:
                            break
                        if 255 == mode.metacarple_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.metacarple_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.metacarple_mask[event.y-y][event.x+x]:
                            mode.found == True
                        elif 255 == mode.metacarple_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.proximal:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 305 or event.y+y > 369:
                            break
                        if 255 == mode.proximal_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.proximal_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.proximal_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.proximal_mask[event.y-y][event.x-x]:
                            mode.found = True
            if mode.found == False:
                mixer.init()
                mixer.music.load('incorrect.mp3')
                mixer.music.play()
                messagebox.showinfo('Wrong', 'Try Again') 
                mode.attempts +=1
            else:
                mixer.init()
                mixer.music.load('correct.mp3')
                mixer.music.play()
                messagebox.showinfo('Correct','Found Part!')
                mode.attempts +=1
                mode.found = False
                mode.partList.pop(0)
                #Checking if the level was complete or not
                if mode.partList != []:
                    mode.currentPart = mode.partList[0]
                    messagebox.showinfo('Message',\
                        f'Find the {mode.currentPart}')
                else:
                    mixer.init()
                    mixer.music.load('applause.mp3')
                    mixer.music.play()
                    messagebox.showinfo('Congratulations','Found all parts!')
                    messagebox.showinfo('Accuracy Score',f'{(mode.totalParts/mode.attempts)*100}%')
                    mode.attempts = 0
                    mode.start = False
                    #resetting partList if level is played again
                    mode.partList = ['Metacarple','Proximal','Middle','Digital']
                    mode.app.setActiveMode(mode.app.gamePlayMode)
            
                
        elif(mode.gsLX<event.x<mode.gsRX) and (mode.gsLY<event.y<mode.gsRY):
            #switching the boolean
            mode.start = True
            mode.currentPart = mode.partList[0]
            messagebox.showinfo('Message',f'Find the {mode.currentPart}')       
#screen for Ribs anatomy

class RibsMode(Mode):
    def appStarted(mode):
        #https://www.innerbody.com/image/skel14.html (image citation)
        mode.ribsRaw = mode.loadImage('ribs.jpg')
        mode.ribsScaled = mode.scaleImage(mode.ribsRaw,.5)
        mode.ribsX = mode.width/2
        mode.ribsY = mode.height/2
        mode.ribsImage = cv.imread('/Users/vikasmalik/Desktop/TP/ribs.jpg')
        mode.ribsImage = cv.cvtColor(mode.ribsImage, cv.COLOR_BGR2RGB)
        mode.ribsEdges = cv.Canny(mode.ribsImage,50,200)
        mode.imageRows = 427
        mode.imageCols = 594
        mode.found = False
        mode.start = False
        mode.ribs = 'Ribs'
        mode.costal = 'Costal'
        mode.sternum = 'Sternum'
        mode.partList = ['Ribs','Costal','Sternum']
        mode.totalParts = len(mode.partList)
        mode.attempts = 0
        mode.currentPart = mode.partList[0]

        light_ribs = (175,209,237)
        dark_ribs = (119,139,158)
        mode.ribs_mask = cv.inRange(mode.ribsImage,dark_ribs,light_ribs)

        light_costal = (241,234,118)
        dark_costal = (146,149,59)
        mode.costal_mask = cv.inRange(mode.ribsImage,dark_costal,light_costal)

        light_sternum = (166,218,169)
        dark_sternum = (65,119,70)
        mode.sternum_mask = cv.inRange(mode.ribsImage,dark_sternum,\
            light_sternum)
        
        final_mask = mode.costal_mask + mode.ribs_mask + mode.sternum_mask
        result = cv.bitwise_and(mode.ribsImage,mode.ribsImage,mask=final_mask)
        #plt.subplot(1, 2, 1)
        #plt.imshow(mode.ribsImage, cmap= 'gray')
        #plt.subplot(1, 2, 2)
        #plt.imshow(result)
        #plt.show()

    def redrawAll(mode,canvas):
        canvas.create_image(mode.ribsX,mode.ribsY,
        image = ImageTk.PhotoImage(mode.ribsScaled))
        canvas.create_text(mode.width/2,50,\
            text='How well do you know the Ribs?',font='Arial 16 bold')
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')

    def mousePressed(mode,event):
        if (mode.bLX<event.x<mode.bRX) and (mode.bLY<event.y<mode.bRY):
            mode.app.setActiveMode(mode.app.gamePlayMode)
        elif mode.start == True:
            if mode.currentPart == mode.costal:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 427 or event.y+y > 594:
                            break
                        if 255 == mode.costal_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.costal_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.costal_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.costal_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.sternum:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 427 or event.y+y > 594:
                            break
                        if 255 == mode.sternum_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.sternum_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.sternum_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.sternum_mask[event.y-y][event.x-x]:
                            mode.found = True
            elif mode.currentPart == mode.ribs:
                event.x = event.x - int((mode.width - mode.imageRows)//2)
                event.y = event.y - int((mode.height - mode.imageCols)//2)
                for x in range(5):
                    for y in range(5):
                        if event.x+x > 427 or event.y+y > 594:
                            break
                        if 255 == mode.ribs_mask[event.y+y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.ribs_mask[event.y+y][event.x-x]:
                            mode.found = True
                        elif 255 == mode.ribs_mask[event.y-y][event.x+x]:
                            mode.found = True
                        elif 255 == mode.ribs_mask[event.y-y][event.x-x]:
                            mode.found = True

            if mode.found == False :
                mixer.init()
                mixer.music.load('incorrect.mp3')
                mixer.music.play()
                messagebox.showinfo('Wrong', 'Try Again') 
                mode.attempts +=1
            else:
                mixer.init()
                mixer.music.load('correct.mp3')
                mixer.music.play()
                messagebox.showinfo('Correct','Found Part!')
                mode.attempts+=1
                mode.partList.pop(0)
                #Checking if the level was complete or not
                if mode.partList != []:
                    mode.currentPart = mode.partList[0]
                    messagebox.showinfo('Message',\
                        f'Find the {mode.currentPart}')
                else:
                    mixer.init()
                    mixer.music.load('applause.mp3')
                    mixer.music.play()
                    messagebox.showinfo('Congratulations','Found all parts!')
                    messagebox.showinfo('Accuracy Score',f'{(mode.totalParts/mode.attempts)*100}%')
                    mode.attempts = 0
                    mode.start = False
                    #resetting partList if level is played again
                    mode.partList = ['Ribs','Costal','Sternum']
                    mode.app.setActiveMode(mode.app.gamePlayMode)
            
        elif(mode.gsLX<event.x<mode.gsRX) and (mode.gsLY<event.y<mode.gsRY):
            #switching the boolean
            mode.start = True
            mode.currentPart = mode.partList[0]
            messagebox.showinfo('Message',f'Find the {mode.currentPart}')
            
class ReverseBrainMode(Mode):
    def appStarted(mode):
        mode.frontalLobe = 'Frontal Lobe'
        mode.occipitalLobe = 'Occipital Lobe'
        mode.parietalLobe = 'Parietal Lobe'
        mode.temporalLobe = 'Temporal Lobe'
        mode.partList = ['Frontal Lobe','Occipital Lobe','Parietal Lobe',\
            'Temporal Lobe']
        mode.part = mode.partList[0]
        mode.start = False
        mode.correct = False
        mode.brainRaw = mode.loadImage('brain.jpg')
        mode.brainScaled = mode.scaleImage(mode.brainRaw,1.2)
        mode.brainX, mode.brainY = mode.width/2, mode.height/2

    def redrawAll(mode,canvas):
        #drawing the image onto the canvas
        canvas.create_image(mode.brainX, mode.brainY, 
        image=ImageTk.PhotoImage(mode.brainScaled))
        canvas.create_text(mode.width/2,50,\
            text='How well do you know the brain?',font='Arial 16 bold')
        #creating start button
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
        #creating back button
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
            
    def mousePressed(mode,event):
        #checks if the back button is clicked
        if mode.bLX<event.x<mode.bRX and mode.bLY<event.y<mode.bRY:
            mode.start = False
            mode.app.setActiveMode(mode.app.reverseGamePlayMode)
        #checks if the game has started
        elif mode.gsLX<event.x<mode.gsRX and mode.gsLY<event.y<mode.gsRY:
            mode.start = True
            #as long as the parts of list haven't ran out
            while len(mode.partList) != 0:
                mode.part = mode.partList[0]
                #gets the user input
                mode.input = mode.getUserInput(f'What is the function of {mode.part}?').lower()
                #see what part the user was asked about
                if mode.part == mode.frontalLobe:
                    if ('cognitive' in mode.input) or ('memory' in mode.input)\
                        or ('emotion' in mode.input) or \
                        ('judgement' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes':
                            #if wrong give option to learn... use webbrowser to link
                            webbrowser.open('https://www.medicalnewstoday.com/articles/318139.php')
                elif mode.part == mode.occipitalLobe:
                    if ('vision' in mode.input) or ('depth perception' in \
                        mode.input) or ('facial recognition' in mode.input)or\
                        ('color determination' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.sciencedirect.com/topics/neuroscience/occipital-lobe')
                elif mode.part == mode.temporalLobe:
                    if ('hearing' in mode.input) or ('ears'in mode.input)\
                        or ('auditory input' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.neuroskills.com/brain-injury/temporal-lobes/')
                        
                elif mode.part == mode.parietalLobe:
                    if ('sensory' in mode.input) or ('sensation' in mode.input)\
                        or ('senses' in mode.input) or ('touch' in mode.input)\
                        or ('process sensory information' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Wrong','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.neuroskills.com/brain-injury/parietal-lobes/')

            #Checks if the game is over
            if len(mode.partList) == 0:
                messagebox.showinfo('Sweet','Congratulations! You answered every question right')
                #resets PartList if level is played again
                mode.partList = ['Frontal Lobe','Occipital Lobe',\
                    'Parietal Lobe', 'Temporal Lobe']
                mode.start = False
                mode.app.setActiveMode(mode.app.reverseGamePlayMode)
            
class ReverseSpineMode(Mode):
    def appStarted(mode):
        mode.spineRaw = mode.loadImage('spine.jpeg')
        mode.spineScaled = mode.scaleImage(mode.spineRaw,.5)
        mode.spineX = mode.width/2
        mode.spineY = mode.height/2
        mode.lumber = 'Lumber'
        mode.cervical = 'Cervical'
        mode.thoracic = 'Thoracic'
        mode.coccyx = 'Coccyx'
        mode.sacrum = 'Sacrum'
        mode.partList = ['Lumber','Thoracic','Sacrum','Coccyx','Cervical']
        mode.currentPart = mode.partList[0]
    
    def redrawAll(mode,canvas):
        canvas.create_image(mode.spineX, mode.spineY, 
        image=ImageTk.PhotoImage(mode.spineScaled))
        canvas.create_text(mode.width/2,50,\
            text='How well do you know the brain?',font='Arial 16 bold')
        #creating start button
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
        #creating back button
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
    
    def mousePressed(mode,event):
        if mode.bLX<event.x<mode.bRX and mode.bLY<event.y<mode.bRY:
            mode.start = False
            mode.app.setActiveMode(mode.app.reverseGamePlayMode)
        elif mode.gsLX<event.x<mode.gsRX and mode.gsLY<event.y<mode.gsRY:
            mode.start = True
            while len(mode.partList) != 0:
                mode.part = mode.partList[0]
                mode.input = mode.getUserInput(f'What is the function of {mode.part}?').lower()
                if mode.part == mode.lumber:
                    if ('lower back' in mode.input) or ('support' in mode.input)\
                        or ('support weight' in mode.input) or \
                        ('rotation' in mode.input) or ('protect' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://biologydictionary.net/lumbar-vertebrae/')
                        else:
                            pass
                elif mode.part == mode.cervical:
                    if ('mobility' in mode.input) or ('stability' in \
                        mode.input) or ('head rotation' in mode.input)or\
                        ('flexion' in mode.input) or ('extension' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.physio-pedia.com/Cervical_Vertebrae')
                        else:
                            pass
                elif mode.part == mode.thoracic:
                    if ('support the back' in mode.input) or ('support'in mode.input)\
                        or ('protective cage around ribs' in mode.input) or ('support lungs' in mode.input)\
                        or ('support the heart' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.kenhub.com/en/library/anatomy/thoracic-vertebrae') 
                        else:
                            pass
                elif mode.part == mode.coccyx:
                    if ('balance' in mode.input) or ('stability' in mode.input)\
                        or ('hip bone' in mode.input) or ('tailbone' in mode.input)\
                        or ('weight distribution' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Wrong','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://study.com/academy/lesson/coccyx-bone-definition-location-function.html')
                        else:
                            pass
                elif mode.part == mode.sacrum:
                    if ('secure pelvis' in mode.input) or ('support bladder' in mode.input)\
                        or ('sexual function' in mode.input) or ('support bowel' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Wrong','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.verywellhealth.com/sacral-vertebrae-anatomy-function-and-treatment-4769390')
                        else:
                            pass
                #Checks if the game is over
            if len(mode.partList) == 0:
                print('Congratulations! You answered every question right')
                #resets PartList if level is played again
                mode.partList = ['Lumber','Thoracic','Sacrum','Coccyx','Cervical']
                mode.start = False
                mode.app.setActiveMode(mode.app.reverseGamePlayMode)

class ReverseSkullMode(Mode):
    def appStarted(mode):
        mode.skullRaw = mode.loadImage('skull.png')
        mode.skullScaled = mode.scaleImage(mode.skullRaw,.8)
        mode.skullX=mode.width/2
        mode.skullY=mode.height/2
        mode.frontalBone = 'Frontal Bone'
        mode.sphenoidBone = 'Sphenoid Bone'
        mode.maxillaBone = 'Maxilla Bone'
        mode.zygomaticBone = 'Zygomatic Bone'
        mode.partList = ['Zygomatic Bone','Maxilla Bone','Sphenoid Bone',\
            'Frontal Bone']
        mode.currentPart = mode.partList[0]

    def redrawAll(mode,canvas):
        canvas.create_image(mode.skullX,mode.skullY,
        image = ImageTk.PhotoImage(mode.skullScaled))
        canvas.create_text(mode.width/2,50,\
            text='Lets see if you skulld to study?',font='Arial 16 bold')
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')

    def mousePressed(mode,event):
        if mode.bLX<event.x<mode.bRX and mode.bLY<event.y<mode.bRY:
            mode.start = False
            mode.app.setActiveMode(mode.app.reverseGamePlayMode)
        elif mode.gsLX<event.x<mode.gsRX and mode.gsLY<event.y<mode.gsRY:
            mode.start = True
            while len(mode.partList) != 0:
                mode.part = mode.partList[0]
                mode.input = mode.getUserInput(f'What is the function of {mode.part}?').lower()
                if mode.part == mode.zygomaticBone:
                    if ('protect arteries' in mode.input) or ('protect nerves' in mode.input)\
                        or ('protet organs' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.verywellhealth.com/zygomatic-bone-anatomy-4692051')
                        else:
                            pass
                elif mode.part == mode.sphenoidBone:
                    if ('create tunnels' in mode.input) or ('nerves' in \
                        mode.input) or ('holds everything together' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.visiblebody.com/blog/3d-skeletal-system-function-of-the-sphenoid')
                        else:
                            pass
                elif mode.part == mode.maxillaBone:
                    if ('protect the eyes' in mode.input) or ('protect the brain'in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.healthline.com/health/maxilla#function') 
                        else:
                            pass
                elif mode.part == mode.frontalBone:
                    if ('protect brain' in mode.input) or ('support head' in mode.input)\
                        or ('protext brain tissue' in mode.input) :
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Wrong','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.innerbody.com/image_skel01/skel40_new_skull.html')
                        else:
                            pass
                #Checks if the game is over
            if len(mode.partList) == 0:
                print('Congratulations! You answered every question right')
                #resets PartList if level is played again
                mode.partList = ['Zygomatic Bone','Maxilla Bone','Sphenoid Bone',\
                'Frontal Bone']
                mode.start = False
                mode.app.setActiveMode(mode.app.reverseGamePlayMode)
        
class ReverseAnkleMode(Mode):
    def appStarted(mode):
        mode.ankleRaw = mode.loadImage('ankle.jpg')
        mode.ankleScaled = mode.scaleImage(mode.ankleRaw,.8)
        mode.ankleX = mode.width/2
        mode.ankleY = mode.height/2
        mode.partList = ['Talus','Tibia','Fibula','Calcaneus']

    def redrawAll(mode,canvas):
        canvas.create_image(mode.ankleX,mode.ankleY,
        image = ImageTk.PhotoImage(mode.ankleScaled))
        canvas.create_text(mode.width/2,50,\
            text='Lets see if you skulld to study?',font='Arial 16 bold')
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')

    def mousePressed(mode,event):
        if mode.bLX<event.x<mode.bRX and mode.bLY<event.y<mode.bRY:
            mode.start = False
            mode.app.setActiveMode(mode.app.reverseGamePlayMode)
        elif mode.gsLX<event.x<mode.gsRX and mode.gsLY<event.y<mode.gsRY:
            mode.start = True
            while len(mode.partList) != 0:
                mode.part = mode.partList[0]
                mode.input = mode.getUserInput(f'What is the function of {mode.part}?').lower()
                if mode.part == mode.talus:
                    if ('connect the leg and the foot' in mode.input) or ('weight transfer' in mode.nput):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.healthline.com/human-body-maps/talus-bone')
                        else:
                            pass
                elif mode.part == mode.tibia:
                    if ('forms knee joint' in mode.input) or ('allows for movement' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.innerbody.com/image_skelfov/skel28_new.html')
                        else:
                            pass
                elif mode.part == mode.fibula:
                    if ('structural support' in mode.input) or ('minimize impact on tendons' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.healthline.com/human-body-maps/fibula-bone#1') 
                        else:
                            pass
                elif mode.part == mode.calcaneus:
                    if ('lever for calf muscles' in mode.input) or ('attachment for other lerg ligaments' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Wrong','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://study.com/academy/lesson/calcaneus-bone-definition-anatomy-function.html')
                        else:
                            pass
                #Checks if the game is over
            if len(mode.partList) == 0:
                print('Congratulations! You answered every question right')
                #resets PartList if level is played again
                mode.partList = ['Talus','Tibia','Fibula','Calcaneus']
                mode.start = False
                mode.app.setActiveMode(mode.app.reverseGamePlayMode)       

class ReverseHandMode(Mode):
    def appStarted(mode):
        mode.handRaw = mode.loadImage('hand.jpg')
        mode.handScaled = mode.scaleImage(mode.handRaw,.9)
        mode.handX = mode.width/2
        mode.handY = mode.height/2
        mode.metacarple = 'Metacarple'
        mode.proximal = 'Proximal'
        mode.middle = 'Middle'
        mode.digital = 'Digital'
        mode.partList = ['Proximal','Middle','Digital','Metacarple']
        mode.currentPart = mode.partList[0]

    def redrawAll(mode,canvas):
        canvas.create_image(mode.handX,mode.handY,
        image = ImageTk.PhotoImage(mode.handScaled))
        canvas.create_text(mode.width/2,50,\
            text='Can you hand-le this?',font='Arial 16 bold')
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')

    def mousePressed(mode,event):
        if mode.bLX<event.x<mode.bRX and mode.bLY<event.y<mode.bRY:
            mode.start = False
            mode.app.setActiveMode(mode.app.reverseGamePlayMode)
        elif mode.gsLX<event.x<mode.gsRX and mode.gsLY<event.y<mode.gsRY:
            mode.start = True
            while len(mode.partList) != 0:
                mode.part = mode.partList[0]
                mode.input = mode.getUserInput(f'What is the function of {mode.part}?').lower()
                if mode.part == mode.proximal:
                    if ('allow digital movement' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.healthline.com/human-body-maps/proximal-phalanges-hand#1')
                        else:
                            pass
                elif mode.part == mode.middle:
                    if ('allow finger bending' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.healthline.com/human-body-maps/middle-phalanges-hand')
                        else:
                            pass
                elif mode.part == mode.digital:
                    if ('allow for grabbing' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.healthline.com/human-body-maps/distal-phalanges-hand') 
                        else:
                            pass
                elif mode.part == mode.metacarple:
                    if ('bridge' in mode.input) or ('bridge between wrist and fingers' in mode.input)\
                        or ('allows hand function' in mode.input) :
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Wrong','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.theskeletalsystem.net/metacarpal-bones')
                        else:
                            pass
                #Checks if the game is over
            if len(mode.partList) == 0:
                print('Congratulations! You answered every question right')
                #resets PartList if level is played again
                mode.partList = mode.partList = ['Proximal','Middle','Digital','Metacarple']
                mode.start = False
                mode.app.setActiveMode(mode.app.reverseGamePlayMode)

class ReverseRibsMode(Mode):
    def appStarted(mode):
        mode.ribsRaw = mode.loadImage('ribs.jpg')
        mode.ribsScaled = mode.scaleImage(mode.ribsRaw,.5)
        mode.ribsX = mode.width/2
        mode.ribsY = mode.height/2
        mode.ribs = 'Ribs'
        mode.costal = 'Costal'
        mode.sternum = 'Sternum'
        mode.partList = ['Ribs','Costal','Sternum']
        mode.currentPart = mode.partList[0]

    def redrawAll(mode,canvas):
        canvas.create_image(mode.ribsX,mode.ribsY,\
            image = ImageTk.PhotoImage(mode.ribsScaled))
        canvas.create_text(mode.width/2,50,\
            text='How well do you know the Ribs?',font='Arial 16 bold')
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
        mode.gsLX,mode.gsRX = 50,200
        mode.gsLY,mode.gsRY = 425,475
        canvas.create_rectangle(mode.gsLX,mode.gsLY,mode.gsRX,mode.gsRY,\
            fill = 'light blue',outline = 'black', width = 3)
        canvas.create_text((mode.gsLX + mode.gsRX) /2,(mode.gsLY + mode.gsRY)/2\
            ,text = 'Get Started', font = 'Arial 17 bold')
    
    def mousePressed(mode,event):
        if mode.bLX<event.x<mode.bRX and mode.bLY<event.y<mode.bRY:
            mode.start = False
            mode.app.setActiveMode(mode.app.reverseGamePlayMode)
        elif mode.gsLX<event.x<mode.gsRX and mode.gsLY<event.y<mode.gsRY:
            mode.start = True
            while len(mode.partList) != 0:
                mode.part = mode.partList[0]
                mode.input = mode.getUserInput(f'What is the function of {mode.part}?').lower()
                if mode.part == mode.ribs:
                    if ('protect arteries' in mode.input) or ('protect nerves' in mode.input)\
                        or ('protet organs' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.verywellhealth.com/zygomatic-bone-anatomy-4692051')
                        else:
                            pass
                elif mode.part == mode.sternum:
                    if ('protect heart' in mode.input) or ('protect lungs' in \
                        mode.input) or ('protect blood vessels' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://courses.lumenlearning.com/boundless-ap/chapter/the-thorax/')
                        else:
                            pass
                elif mode.part == mode.costal:
                    if ('allow flexibility in ribs' in mode.input):
                        messagebox.showinfo('Correct','Correct')
                        mode.partList.pop(0)
                    else:
                        messagebox.showinfo('Incorrect','Try Again')
                        mode.learn = mode.getUserInput(f'Would you like to learn more about this part?').lower()
                        if mode.learn == 'yes' or mode.learn == 'Yes':
                            webbrowser.open('https://www.healthline.com/human-body-maps/costal-cartilage#1') 
                        else:
                            pass
                #Checks if the game is over
            if len(mode.partList) == 0:
                print('Congratulations! You answered every question right')
                #resets PartList if level is played again
                mode.partList = ['Ribs','Costal','Sternum']
                mode.start = False
                mode.app.setActiveMode(mode.app.reverseGamePlayMode)
        
#screen for Instructions
class HelpMode(Mode):
    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = 'light pink')
        canvas.create_text(mode.width/2,mode.height/2,text = 
        '''\tThis application will test your knowledge of anatomy in a
        variety of systems. In order to play first click on the Lets Study
        button. If you click the reverse button you will be taken to 
        Game Mode 2. 
        \tGame Mode 1:
            Choose the body system that you would like to study. 
        Once doing so you will see an image of the bodyparts. Then click 
        the get started button. You will then be prompted with messages, 
        asking you to click on the certain part that the question is asking 
        you to find. If correct you will be prompted with the next question. 
        If not you will get to try again. Once all parts are found then it 
        will take you back to the gamePlay screen.
        \tGame Mode 2:
            Choose the body system that you would like ot study. 
        Once doing so you will see an image of the bodyparts. Then click 
        the get started button. You will be prompted with input messages
        asking you to answer some quesitons. If you get them right then 
        you get the next question. If you get it wrong, you will be asked if 
        you would like to learn more. If you say yes you will be redirected
        to a url. If not then you can reattempt the question until you get it 
        right.Once all parts are found then it will take you back to the 
        gamePlay screen. ''', font = 'Arial 14 bold')
        mode.bLX,mode.bRX = 300,450
        mode.bLY,mode.bRY = 425,475
        canvas.create_rectangle(mode.bLX,mode.bLY,mode.bRX,mode.bRY,\
            fill='orange',outline='black',width = 3)
        canvas.create_text((mode.bLX+mode.bRX)/2,(mode.bLY+mode.bRY)/2,\
            text = 'Go back', font = 'Arial 18 bold')
    def mousePressed(mode,event):
        if mode.bLX<event.x<mode.bRX and mode.bLY<event.y<mode.bRY:
            mode.app.setActiveMode(mode.app.splashScreenMode)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gamePlayMode = GamePlayMode()
        app.reverseGamePlayMode = ReverseGamePlayMode()
        app.brainMode = BrainMode()
        app.spineMode = SpineMode()
        app.skullMode = SkullMode()
        app.ankleMode = AnkleMode()
        app.handMode = HandMode()
        app.ribsMode = RibsMode()
        app.reverseBrainMode = ReverseBrainMode()
        app.reverseSpineMode = ReverseSpineMode()
        app.reverseSkullMode = ReverseSkullMode()
        app.reverseAnkleMode = ReverseAnkleMode()
        app.reverseHandMode = ReverseHandMode()
        app.reverseRibsMode = ReverseRibsMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 300

def runGreys101():
    app = MyModalApp(width=500, height=500)

runGreys101()




