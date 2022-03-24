import pygame, random, sys
from pygame.locals import *
from PyDictionary import PyDictionary
import datetime, hashlib
import webbrowser

# Retrieves array of possible answers to select random word from.
from ansDict import possAnswers

#######   == WORDLE in pygame ==  ########
#######   == by Ben Alderton  ==  ########


# Initialise pygame
pygame.init()

# Colour/Font definitions

(width, height) = (500, 600)
screen = pygame.display.set_mode((width, height))

purewhite = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 183, 55)
grey = (180, 180, 180)
darkgrey = (100, 100, 100)
black = (0, 0, 0)
green = (60, 205, 48)
lime = (153, 255, 204)

tinyFont = pygame.font.SysFont("Arial", 13)
smallFont = pygame.font.SysFont("Helvetica neue", 15)
font = pygame.font.SysFont("Helvetica neue", 40)
font4 = pygame.font.SysFont("Proxima Nova", 40)
font2 = pygame.font.SysFont("Arial", 40, bold=True)
font3 = pygame.font.SysFont("Arial", 32, bold=True)
bigFont = pygame.font.SysFont("Arial", 65, bold=True)

youWin = bigFont.render("You win!", True, black)
youLose = bigFont.render("You lose!", True, black)
playAgain = bigFont.render("Play Again!", True, black)

dictionary = PyDictionary()

homeIcon = pygame.image.load('home.png')
homeIcon = pygame.transform.scale(homeIcon, (32, 30))
allowedChars = "qwertyuiopasdfghjklzxcvbnm"
alphabetIndex = [grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey,grey]

# ========== Gameplay ===========

def halveRow(num, range):
    if num >= range/2:
        num = num-range/2
    return num

def renderAlphabet():

    darkfile = open('darkmodevar.txt', 'r')
    darkmode = str(darkfile.read())

    darkfile.close()

    if darkmode == 'True':
        bg = pygame.image.load('Word-Art-2-Dark.png')
        modecolour = (122, 122, 122)
        modecolourrev = (255, 255, 255)
    else:
        bg = pygame.image.load('Word Art-2.png')
        modecolour = (255, 255, 255)
        modecolourrev = (0, 0, 0)

    coords = (0, 50 * 7.5, width / 6.5, height / 1)
    txt = tinyFont.render(f"Return", True, modecolourrev)
    screen.fill(grey, coords)
    screen.blit(txt, (coords[0] + width / 52 + 6, coords[1] + height / 52 + 6))
    pygame.draw.rect(screen, purewhite, pygame.Rect(coords[0], coords[1], width / 6.5, height/10), 1)
    coords = (width - width / 6.5, 50 * 7.5, width / 6.5, height / 10)
    screen.fill(grey, coords)
    txt = tinyFont.render(f"Backspace", True, modecolourrev)
    screen.blit(txt, (coords[0] - 3 + width / 52, coords[1] + height / 52 + 6))
    pygame.draw.rect(screen, purewhite, pygame.Rect(coords[0], coords[1], width / 6.5, height / 10),1)
    for letter in allowedChars:
        index = allowedChars.index(letter)
        thecolour = alphabetIndex[index]
        txt = smallFont.render(f"{letter.upper()}", True, modecolourrev)
        colour = black
        if thecolour == yellow:
            colour = yellow
        elif thecolour == green:
            colour = green
        elif thecolour == grey:
            colour = grey
        elif thecolour == darkgrey:
            colour = darkgrey
        h=0
        if index >= 13:
            h = width/13
        index = halveRow(index, 26)
        coords = (index * (width / 13), 50 * 8.5+h, width / 13, height/13)
        screen.fill(colour, coords)
        screen.blit(txt, (coords[0]+width/52, coords[1]+height/52))
        pygame.draw.rect(screen, purewhite, pygame.Rect(coords[0], coords[1], width/13, width/13), 1)

# Function 1

def checkGuess(turns, word, userGuess, window, duplicateArray):
    darkfile = open('darkmodevar.txt', 'r')
    darkmode = str(darkfile.read())

    darkfile.close()

    if darkmode == 'True':
        bg = pygame.image.load('Word-Art-2-Dark.png')
        modecolour = (122, 122, 122)
        modecolourrev = (255, 255, 255)
    else:
        bg = pygame.image.load('Word Art-2.png')
        modecolour = (255, 255, 255)
        modecolourrev = (0, 0, 0)
    gameList = ["", "", "", "", ""]
    used = []
    spacing = 0  # How far apart boxes are going to render
    guessColour = [grey, grey, grey, grey, grey]
    duplicatedAccountedFor = False

    for i in range(0, 5):  # Checking each letter of the player's guess

        if word[i] == userGuess[i]:  # If the letter is the exact same as the one in the word, it is green
            guessColour[i] = green
            used.append(userGuess[i])
            for letter in allowedChars:
                if letter.upper() == userGuess[i]:
                    index = allowedChars.index(letter)
                    alphabetIndex[index] = green

    for i in range(0, 5):  # Checking each letter of the player's guess

        if userGuess[i] in word and userGuess[i] != word[i]: # If the letter is in the word, it will primarily turn yellow

            if userGuess[i] not in used:
                guessColour[i] = yellow
                used.append(userGuess[i])
                for letter in allowedChars:
                    if letter.upper() == userGuess[i]:
                        index = allowedChars.index(letter)
                        if alphabetIndex[index] != green:
                            alphabetIndex[index] = yellow

            if userGuess[i] in used and userGuess[i] in duplicateArray and not duplicatedAccountedFor:
                guessColour[i] = yellow
                duplicatedAccountedFor = True

                for letter in allowedChars:
                    if letter.upper() == userGuess[i]:
                        index = allowedChars.index(letter)
                        if alphabetIndex[index] != green:
                            alphabetIndex[index] = yellow

    for i in range(0,5):

        if userGuess[i] not in word:
            for letter in allowedChars:
                if letter.upper() == userGuess[i]:
                    index = allowedChars.index(letter)
                    alphabetIndex[index] = darkgrey


    list(userGuess)

    for i in range(0, 5):

        gameList[i] = font4.render(userGuess[i], True, modecolour)

        # Drawing  Boxes
        #
        # "pygame.Rect(60+spacing)" gives first rectangle 60 pixels from the edge + the spacing value.
        #
        # "50+(turns*80)" puts the first row of boxes 50 down from border and then 80 more for
        # each extra guess to make rows.f

        pygame.draw.rect(window, guessColour[i], pygame.Rect(110 + spacing, 47 + (turns * 60), 45, 45))
        pygame.draw.rect(window, modecolourrev, pygame.Rect(110 + spacing, 47 + (turns * 60), 45, 45), 3)

        # Drawing Letters
        # Same as previous but adjusted values to align correctly

        window.blit(gameList[i], (121 + spacing, 58 + (turns * 60)))

        spacing += 60  # Stops all letters/boxes from being placed on the first column


    renderAlphabet()

    if guessColour == [green, green, green, green, green]:
        return True


# Function 2 [Copied as this seems to be the only way to do this, and I am too dumb to write myself]
# Code from top answer on https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame


def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


# Function 3


def define(word):  # Defining the word using PyDictionary

    definition = str(dictionary.meaning(word, True))  # Getting original definition w/out formatting
    alChar = "abcdefghijklmnopqrstuvwxyz:, ".upper()  # The characters that are allowed in definition

    for i in range(len(definition)):
        if definition[i].upper() not in alChar:
            definition = definition.replace(definition[i], " ") # Replace illegal characters in string

    definition = " ".join(definition.split())

    if definition == 'None':
        definition = 'No Definition Found'

    blit_text(screen, definition, (10, 510), tinyFont)
    print(definition)


# Function 4

def saveState(window):

    pygame.image.save(window, "screenSave.jpg")

def saveDaily(window):

    pygame.image.save(window, "dailySave.jpg")


def check_mouse_click(image, window):
    darkfile = open('darkmodevar.txt', 'r')
    darkmode = str(darkfile.read())

    darkfile.close()

    if darkmode == 'True':
        bg = pygame.image.load('Word-Art-2-Dark.png')
        modecolour = (122, 122, 122)
        modecolourrev = (255, 255, 255)
    else:
        bg = pygame.image.load('Word Art-2.png')
        modecolour = (255, 255, 255)
        modecolourrev = (0, 0, 0)
    FPS = 60
    clock = pygame.time.Clock()

    width = screen.get_width()

    pygame.draw.rect(window, modecolour, pygame.Rect(180, 26, 140, 60))
    pygame.draw.rect(window, black, pygame.Rect(180, 26, 140, 60), 7)

    playGame = smallFont.render('View Game', True, black)
    window.blit(playGame, (212, 46))

    loop = True

    while loop == True:

        for ev in pygame.event.get():

            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                mouse = pygame.mouse.get_pos()

                if width / 2 - 70 <= mouse[0] <= width / 2 + 70 and 26 <= mouse[1] <= 86:

                    image2 = pygame.image.load(image)
                    window.blit(image2, (0, 0))
                    returnToRestart = font.render('Press Return To Restart', True, modecolour)
                    window.blit(returnToRestart, (35, 530))
                    loop2 = True
                    while loop2 == True:

                        for ev in pygame.event.get():

                            if ev.type == pygame.KEYDOWN:
                                if ev.key == pygame.K_RETURN:
                                    loop = False
                                    loop2 = False
                                    main(False)

                            if ev.type == pygame.MOUSEBUTTONDOWN:

                                mouse = pygame.mouse.get_pos()

                                if 3 <= mouse[0] <= 35 and 3 <= mouse[1] <= 33:
                                    loop2 = False
                                    loop = False
                                    start_menu()

                        pygame.display.update()
                        clock.tick(FPS)



            if ev.type == pygame.KEYDOWN:
                if ev.key == K_RETURN:

                    loop = False

            if ev.type == pygame.MOUSEBUTTONDOWN:

                mouse = pygame.mouse.get_pos()

                if 3 <= mouse[0] <= 35 and 3 <= mouse[1] <= 33:
                    loop = False
                    start_menu()


        pygame.display.update()
        clock.tick(FPS)

    main(False)


# Function 5

def help_menu():

    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption('Wordle')

    darkfile = open('darkmodevar.txt', 'r')
    darkmode = str(darkfile.read())

    darkfile.close()

    if darkmode == 'True':
        bg = pygame.image.load('Word-Art-2-Dark.png')
        modecolour = (122, 122, 122)
        modecolourrev = (255, 255, 255)
    else:
        bg = pygame.image.load('Word Art-2.png')
        modecolour = (255, 255, 255)
        modecolourrev = (0, 0, 0)

    screen.blit(bg, (-100, -40))


    if darkmode == 'False':
        desc = pygame.image.load('desc.png')
    else:
        desc = pygame.image.load('descDark.png')
    screen.blit(desc, (0, 0))

    screen.blit(homeIcon, (3, 3))

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # Quits game effectively

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse = pygame.mouse.get_pos()

                if 3 <= mouse[0] <= 35  and 3 <= mouse[1] <= 33:
                    start_menu()

        pygame.display.update()

        clock.tick(FPS)

def options_sidebar():
    darkfile = open('darkmodevar.txt', 'r')
    darkmode = str(darkfile.read())

    darkfile.close()

    if darkmode == 'True':
        bg = pygame.image.load('Word-Art-2-Dark.png')
        modecolour = (122, 122, 122)
        modecolourrev = (255, 255, 255)
    else:
        bg = pygame.image.load('Word Art-2.png')
        modecolour = (255, 255, 255)
        modecolourrev = (0, 0, 0)

    FPS = 100
    clock = pygame.time.Clock()
    button = ''

    optionsIcon = pygame.image.load('options.png')
    optionsIcon = pygame.transform.scale(optionsIcon, (51.4, 39.4))
    speed = 6
    startMenu = pygame.image.load('startMenu.jpg')
    startMenuDark = pygame.image.load('startMenuDark.jpg')

    darkButtonOn = pygame.image.load('dmodebuttonon.png')
    darkButtonOff = pygame.image.load('dmodebuttonoff.png')
    darkModeCurrentRect = ''

    if darkmode == 'True':
        darkModeCurrent = darkButtonOn
        darkModeCurrent = pygame.transform.scale(darkModeCurrent, (160, 160))

    else:
        darkModeCurrent = darkButtonOff
        darkModeCurrent = pygame.transform.scale(darkModeCurrent, (160, 160))

    for i in range(35):

        pygame.draw.rect(screen, modecolour, pygame.Rect(500 - (speed * i), 0, 210, 600))

        pygame.draw.rect(screen, black, pygame.Rect(500 - (speed*i), 0, 6, 600))

        button = screen.blit(optionsIcon, (510-(speed*i), 5))

        darkModeCurrentRect = screen.blit(darkModeCurrent, (528 - (speed * i), 80))

        pygame.display.update()

        clock.tick(FPS)

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # Quits game effectively

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse = pygame.mouse.get_pos()

                if button.collidepoint(mouse):

                    for i in range(35):

                        if darkmode:

                            screen.blit(startMenuDark, (0, 0))

                        else:

                            screen.blit(startMenu, (0, 0))

                        pygame.draw.rect(screen, modecolour, pygame.Rect(291 + (speed * i), 0, 300, 600))
                        pygame.draw.rect(screen, black, pygame.Rect(291 + (speed * i), 0, 6, 600))
                        button = screen.blit(optionsIcon, (301 + (speed * i), 5))
                        darkModeCurrentRect = screen.blit(darkModeCurrent, (337 + (speed * i), 80))


                        pygame.display.update()

                        clock.tick(FPS)

                    start_menu()

                if 0 <= mouse[0] <= 289 and 0 <= mouse[1] <= 600:

                    for i in range(35):

                        if darkmode:

                            screen.blit(startMenuDark, (0, 0))

                        else:

                            screen.blit(startMenu, (0, 0))

                        pygame.draw.rect(screen, modecolour, pygame.Rect(291 + (speed * i), 0, 300, 600))
                        pygame.draw.rect(screen, black, pygame.Rect(291 + (speed * i), 0, 6, 600))
                        button = screen.blit(optionsIcon, (301 + (speed * i), 5))
                        darkModeCurrentRect = screen.blit(darkModeCurrent, (337 + (speed * i), 80))

                        pygame.display.update()

                        clock.tick(FPS)

                    start_menu()

                if darkModeCurrentRect.collidepoint(mouse):

                    darkfile = open('darkmodevar.txt', 'r')
                    darkmode = str(darkfile.read())
                    darkfile.close()

                    if darkmode == 'True':
                        darkfile = open('darkmodevar.txt', 'w')
                        darkfile.write('False')
                        darkfile.close()

                    if darkmode == 'False':
                        darkfile = open('darkmodevar.txt', 'w')
                        darkfile.write('True')
                        darkfile.close()

                    start_menu()

        pygame.display.update()

        clock.tick(FPS)

def start_menu():

    darkfile = open('darkmodevar.txt', 'r')
    darkmode = str(darkfile.read())

    darkfile.close()

    if darkmode == 'True':
        bg = pygame.image.load('Word-Art-2-Dark.png')
        modecolour = (122, 122, 122)
        modecolourrev = (255, 255, 255)
    else:
        bg = pygame.image.load('Word Art-2.png')
        modecolour = (255, 255, 255)
        modecolourrev = (0, 0, 0)

    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption('Wordle')

    screen.blit(bg, (-100, -40))

    pygame.draw.rect(screen, modecolour, pygame.Rect(100, 150, 300, 80))
    pygame.draw.rect(screen, black, pygame.Rect(100, 150, 300, 80), 7)

    playText = font.render('Play', True, black)
    screen.blit(playText, (210, 165))

    pygame.draw.rect(screen, modecolour, pygame.Rect(100, 250, 300, 80))
    pygame.draw.rect(screen, black, pygame.Rect(100, 250, 300, 80), 7)

    dailyText = font.render('Daily', True, black)
    screen.blit(dailyText, (204, 265))

    pygame.draw.rect(screen, modecolour, pygame.Rect(100, 350, 300, 80))
    pygame.draw.rect(screen, black, pygame.Rect(100, 350, 300, 80), 7)

    helpText = font.render('Help', True, black)
    screen.blit(helpText, (210, 365))

    optionsIcon = pygame.image.load('options.png')
    optionsIcon = pygame.transform.scale(optionsIcon, (51.4, 39.4))
    optionsIcon = screen.blit(optionsIcon, (445, 5))

    if darkmode:
        pygame.image.save(screen, "startMenuDark.jpg")
    if not darkmode:
        pygame.image.save(screen, "startMenu.jpg")

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # Quits game effectively

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse = pygame.mouse.get_pos()

                if optionsIcon.collidepoint(mouse):
                    options_sidebar()

                if 100 <= mouse[0] <= 400  and 150 <= mouse[1] <= 230:
                    main(False)

                if 100 <= mouse[0] <= 400  and 250 <= mouse[1] <= 330:

                    current_date = datetime.datetime.now().date()
                    current_date = int(current_date.strftime("%Y%m%d"))
                    streakdatefile = open('streakdate.txt', 'r')
                    streakdate = int(streakdatefile.read())
                    streakdatefile.close()

                    if streakdate == current_date:
                        dailySave = pygame.image.load('dailySave.jpg')
                        screen.blit(dailySave, (0, 0))

                        streakfile = open('streak.txt', 'r')
                        streak = str(streakfile.read())
                        streakint = int(streak)
                        colour = modecolour
                        streakText = font3.render("STREAK :", True, modecolour)

                        if streakint <= 4:
                            colour = red
                        elif 4 < streakint <= 10:
                            colour = yellow
                        elif streakint > 10:
                            colour = green

                        streakText2 = font2.render(streak, True, colour)
                        screen.blit(streakText, (160, 535))
                        screen.blit(streakText2, (320, 530))

                        while True:

                            for event in pygame.event.get():

                                if event.type == pygame.QUIT:  # Quits game effectively

                                    pygame.quit()
                                    sys.exit()

                                if event.type == pygame.MOUSEBUTTONDOWN:

                                    mouse = pygame.mouse.get_pos()

                                    if 3 <= mouse[0] <= 35 and 3 <= mouse[1] <= 33:
                                        start_menu()

                            pygame.display.update()
                            clock.tick(FPS)

                    if streakdate != current_date:
                        main(True)

                if 100 <= mouse[0] <= 400  and 350 <= mouse[1] <= 430:
                    help_menu()

        pygame.display.update()

        clock.tick(FPS)

def get_daily_word(): # Code from Robert

    current_date = datetime.datetime.now().date()
    current_date = str(int(current_date.strftime("%Y%m%d")))

    seed = int(hashlib.sha256(str(current_date).encode('utf-8')).hexdigest(), 16)
    while seed >= len(possAnswers): seed /= 10
    return int(seed)

def write_date():

    current_date = datetime.datetime.now().date()
    current_date = int(current_date.strftime("%Y%m%d"))

    streakdate = open('streakdate.txt', 'w')
    streakdate.write('')
    streakdate.write(str(current_date))

def check_daily(daily, win):

    streakdate = open('streakdate.txt', 'r')
    streakfileread = open('streak.txt', 'r')


    if daily:

        current_date = datetime.datetime.now().date()
        current_date = int(current_date.strftime("%Y%m%d"))
        streakdate2 = int(streakdate.read())

        if streakdate2 < current_date:

            if streakdate2 + 1 < current_date:
                streak = 0
                streakfileread.close()
                streakfilewrite = open('streak.txt', 'w')
                streakfilewrite.write(str(streak))
                streakfilewrite.close()

            if win == True:
                print('2')
                streakfileread =  open('streak.txt', 'r')
                streak = int(streakfileread.read())
                streakfileread.close()
                streak += 1
                streakfilewrite = open('streak.txt', 'w')
                streakfilewrite.write(str(streak))
                streakfilewrite.close()
                write_date()

            elif win == False:
                streakfileread = open('streak.txt', 'r')
                streak = 0
                streakfileread.close()
                streakfilewrite = open('streak.txt', 'w')
                streakfilewrite.write(str(streak))
                streakfilewrite.close()
                write_date()

            streakfileread = open('streak.txt', 'r')
            streak = int(streakfileread.read())
            return streak

        else:
            streak = int(streakfileread.read())
            return streak




# Function 6

def main(daily):

    global alphabetIndex
    alphabetIndex = [grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey,
                     grey, grey, grey, grey, grey, grey, grey, grey, grey,grey]

    darkfile = open('darkmodevar.txt', 'r')
    darkmode = str(darkfile.read())

    darkfile.close()

    if darkmode == 'True':
        bg = pygame.image.load('Word-Art-2-Dark.png')
        modecolour = (122, 122, 122)
        modecolourrev = (255, 255, 255)
    else:
        bg = pygame.image.load('Word Art-2.png')
        modecolour = (255, 255, 255)
        modecolourrev = (0, 0, 0)

    if daily:
        ans = possAnswers[get_daily_word()].upper()

    else:
        ans = random.choice(possAnswers).upper()  # Answer selection from ansDict.py

    # Window properties
    FPS = 60
    clock = pygame.time.Clock()

    pygame.display.set_caption('Wordle')

    screen.blit(bg, (-100, -40))

    guess = ""


    print(ans)

    for i in range(0, 5):
        for j in range(0, 6):
            # Drawing grid
            pygame.draw.rect(screen, modecolourrev, pygame.Rect(110 + (i * 60), 47 + (j * 60), 45, 45), 3)

    # Reset Variables
    turns = 0
    win = False
    endgame = False
    lose = False

    zebra = True
    rickroll = ['NEVER', 'GONNA']

    # Guess List
    file = open('gsDict.txt')
    file2 = file.read()

    if daily:
        dailyChallenge = smallFont.render('DAILY CHALLENGE', True, modecolourrev)
        screen.blit(dailyChallenge, (180, 11))

    else:
        unlimitedMode = smallFont.render('UNLIMITED MODE', True, modecolourrev)
        screen.blit(unlimitedMode, (183, 11))


    screen.blit(homeIcon, (3, 3))

    duplicates = []

    for i in range(0, len(ans)):
        for j in range(i + 1, len(ans)):
            if (ans[i] == ans[j]):
                duplicates.append(ans[i])

    renderAlphabet()
    # Event Controller
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # Quits game effectively

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse = pygame.mouse.get_pos()

                if 3 <= mouse[0] <= 35  and 3 <= mouse[1] <= 33:
                    start_menu()

            if event.type == pygame.KEYDOWN:  # Implementing typing

                if event.unicode in allowedChars and not endgame:
                    guess += event.unicode.upper()

                if event.key == K_RETURN and endgame:  # If win is already true, then restart main on enter
                    main(False)

                if event.key == K_RETURN and turns == 6:  # If they have lost then restart main on enter
                    main(False)

                if event.key == K_BACKSPACE and not endgame: # Delete a letter when backspace is pressed
                    guess = guess[:-1]

                if len(guess) > 5 and not endgame:  # Delete a letter if word is too long
                    guess = guess[:-1]

                if event.key == K_RETURN and len(guess) > 4 and guess.lower() in file2 and not endgame:  # On enter if letter is 5 letters, call checkGuess

                    win = checkGuess(turns, ans, guess, screen, duplicates)
                    if guess in rickroll:
                        webbrowser.open('https://www.youtube.com/watch?v=xvFZjo5PgG0')
                    turns += 1
                    guess = ""
                    screen.fill(black, (0, 500, 500, 200))


        if zebra:
            screen.fill(black, (0, 500, 500, 200))  # Cover up text at bottom
        screen.fill(modecolour, (0, 500, 500, 5))  # white border for writing box
        screen.fill(black, (0, 500, 500, 1))  # white border for writing box

        renderGuess = font2.render(guess, True, grey)  # Pre-render text as image to be instantiated on screen
        screen.blit(renderGuess, (180, 530))  # Instantiation of image at the bottom

        if win and not endgame:  # Instantiation of win, loss and play again text

            saveState(screen)

            streak = check_daily(daily, win)
            streakfont = str(streak)

            if daily:
                saveDaily(screen)

            pygame.draw.rect(screen, black, pygame.Rect(40, 50, 420, 400))
            pygame.draw.rect(screen, modecolour, pygame.Rect(50, 60, 400, 380))

            screen.blit(youWin, (117, 160))

            if daily:

                print('Streak: ' + str(streak))
                streakText = font3.render("STREAK :", True, black)

                streakText2 = font2.render(streakfont, True, black)
                screen.blit(streakText, (160, 260))
                screen.blit(streakText2, (320, 255))

            else:
                screen.blit(playAgain, (74, 243))


            yourWordWas = smallFont.render("THE WORD WAS " + ans, True, green)
            screen.blit(yourWordWas, (164, 110))
            again = smallFont.render("PRESS RETURN TO RESTART", True, black)
            screen.blit(again, (145, 365))
            zebra = False

            define(ans)

            endgame = True  # Needed to stop this if statement from looping
            win = False

            saved = 'screenSave.jpg'

            alphabetIndex = [grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey,
                             grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey]

            check_mouse_click(saved, screen)



        elif turns == 6 and not win and not lose and not endgame:

            saveState(screen)
            streak = check_daily(daily, win)
            streakfont = str(streak)

            if daily:
                saveDaily(screen)

            pygame.draw.rect(screen, black, pygame.Rect(40, 50, 420, 400))
            pygame.draw.rect(screen, modecolour, pygame.Rect(50, 60, 400, 380))
            screen.blit(youLose, (110, 160))

            if daily:

                print('Streak: ' + str(streak))
                streakText = font3.render("STREAK :", True, black)


                streakText2 = font2.render(streakfont, True, black)
                screen.blit(streakText, (160, 260))
                screen.blit(streakText2, (320, 255))

            else:
                screen.blit(playAgain, (74, 243))

            yourWordWas = smallFont.render("THE WORD WAS " + ans, True, red)
            screen.blit(yourWordWas, (164, 110))
            again = smallFont.render("PRESS RETURN TO RESTART", True, black)
            screen.blit(again, (145, 365))
            zebra = False

            define(ans)

            endgame = True
            lose = True

            saved = 'screenSave.jpg'

            alphabetIndex = [grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey,
                             grey, grey, grey, grey, grey, grey, grey, grey, grey, grey, grey]

            check_mouse_click(saved, screen)

        pygame.display.update()
        clock.tick(FPS)

start_menu()  # Start the game
