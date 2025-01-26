import pickle
import pygame
import pyperclip
import random
import threading
import time
import webbrowser

from Button import Button
from TextLabel import TextLabel
from Tray import *
from Canvas import *
from PopupWindow import PopupWindow
from Stats import *
import CanvasFinalGrds

pygame.init()
pygame.mixer.init()
sunshine = pygame.mixer.Sound("pet_assets/sunshine.mp3")
darkness =pygame.mixer.Sound("pet_assets/darkness.mp3")
clock = pygame.time.Clock()

# Keep happiness between 0 and avg final course grade
# If token does not exist, then assume average scores are 100
avgScores = 100
mood_state="happy"

# Create list of currently enrolled courses
courseLst = []
tkn = Canvas.get_saved_token()
if (Canvas.check_valid_token(tkn)):
    scoreDict = CanvasFinalGrds.finalGradesDict(tkn)
    # Accumulator to count number of courses with final grds
    totalGrds = 0
    numOfGrds = 0
    for score in scoreDict.values():
        if (score != None):
            totalGrds += score
            numOfGrds += 1
    if (numOfGrds != 0):
        avgScores = int(totalGrds / numOfGrds)

    # Get dictionary of all courses the student has taken before
    courseDict = CanvasFinalGrds.matchCourseNameID(tkn)
    
    # Traverse through scoreDict to see currently enrolled coursesID
    for courseID in scoreDict:
        # Since courseID is key for courseDict, can easily find
        # course name through key value pairs
        courseName = courseDict.get(courseID, -1)
        if courseName != -1:
            score = scoreDict[courseID]
            courseLst += [courseName + " " + str(score)]


# Check to see if the user has already logged in 
token = get_saved_token()

def random_target():
    x = random.randint(0, 300)
    y = random.randint(0, 300)
    return [x, y]

def move_towards_target():
    global pet_pos, last_image_switch_time, walk1_left_img, walk2_left_img, walk1_right_img, walk2_right_img
    target_x, target_y = target_pos
    direction_x = target_x - pet_pos[0]
    direction_y = target_y - pet_pos[1]
    distance = (direction_x**2 + direction_y**2) ** 0.5
    if distance > 0:
        direction_x /= distance
        direction_y /= distance
    pet_pos[0] += direction_x * pet_speed
    pet_pos[1] += direction_y * pet_speed
    if direction_x < 0:
        if time.time() - last_image_switch_time > image_switch_delay:
            walk1_left_img, walk2_left_img = walk2_left_img, walk1_left_img
            last_image_switch_time = time.time()
    elif direction_x > 0:
        if time.time() - last_image_switch_time > image_switch_delay:
            walk1_right_img, walk2_right_img = walk2_right_img, walk1_right_img
            last_image_switch_time = time.time()

def resize(img, width, height):
    img_rect = img.get_rect()
    aspect_ratio = img_rect.width / img_rect.height
    if img_rect.width > img_rect.height:
        new_width = width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = height
        new_width = int(new_height * aspect_ratio)
    return pygame.transform.scale(img, (new_width, new_height))



screen_width, screen_height = 400, 400
screen = pygame.display.set_mode((screen_width, screen_height), pygame. NOFRAME)
pygame.display.set_caption("Tamagotchi Anteater")
image_width, image_height = int(screen_width * 0.25), int(screen_height * 0.25)

stand_img = pygame.image.load("pet_assets/stand.png")
walk1_left_img = pygame.image.load("pet_assets/walk1_left.png")
walk2_left_img = pygame.image.load("pet_assets/walk2_left.png")
walk1_right_img = pygame.image.load("pet_assets/walk1_right.png")
walk2_right_img = pygame.image.load("pet_assets/walk2_right.png")
stand_img = resize(stand_img, image_width, image_height)
walk1_left_img = resize(walk1_left_img, image_width, image_height)
walk2_left_img = resize(walk2_left_img, image_width, image_height)
walk1_right_img = resize(walk1_right_img, image_width, image_height)
walk2_right_img = resize(walk2_right_img, image_width, image_height)

def switch_mood(stand, left1, left2, right1, right2):
    global stand_img, walk1_left_img, walk2_left_img,walk1_right_img, walk2_right_img
    stand_img = pygame.image.load(stand)
    walk1_left_img = pygame.image.load(left1)
    walk2_left_img = pygame.image.load(left2)
    walk1_right_img = pygame.image.load(right1)
    walk2_right_img = pygame.image.load(right2)
    stand_img = resize(stand_img, image_width, image_height)
    walk1_left_img = resize(walk1_left_img, image_width, image_height)
    walk2_left_img = resize(walk2_left_img, image_width, image_height)
    walk1_right_img = resize(walk1_right_img, image_width, image_height)
    walk2_right_img = resize(walk2_right_img, image_width, image_height)

#switch_mood("pet_assets/stand.png", "pet_assets/walk1_left.png", "pet_assets/walk2_left.png", "pet_assets/walk1_right.png", "pet_assets/walk2_right.png")


running = True
minimized = False
anteater_color = (150, 75, 0)
pet_pos = [150, 150]
pet_speed = 1

move_counter = 0
window_pos = [500, 500]
target_pos = [150, 150]
target_reach_threshold = 5
move_delay = random.randint(2, 5)
last_move_time = time.time()
image_switch_delay = 0.4
last_image_switch_time = time.time()

buttons = [] 

texts = []
popups = []

canvas_button = Button("Connect to Canvas", 200, 50, (screen_width // 2 - 200 // 2, screen_height // 2 - 50 // 2 - 100), 5, pygame.font.Font("PressStart2p.ttf", 8))
courses_button = Button("Courses", 50, 50, (screen_width - 110, 10), 5, pygame.font.Font("PressStart2p.ttf", 6))
todo_button = Button("To-Do", 50, 50, (screen_width - 50, 10), 5, pygame.font.Font("PressStart2p.ttf", 8))
exit_button = Button("Exit", 50, 50, (5, 10), 5, pygame.font.Font("PressStart2p.ttf", 8))
def start_game(): 
    login_message = TextLabel(f"Logged in as: {get_username(token)}", pygame.font.Font("PressStart2p.ttf", 8), '#FFFFFF', (10, screen_height - 20))
    buttons.append(todo_button)
    buttons.append(exit_button)
    buttons.append(courses_button)
    texts.append(login_message)

if token == "":
    buttons.append(canvas_button)
else: 
    start_game()
       
# Main Game Loop
while running:
    # Handling Keyboard Events 
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                if mood_state=="happy":
                    switch_mood("pet_assets/lebronhappy.png", "pet_assets/lebronhappy.png", "pet_assets/lebronhappy.png", "pet_assets/lebronhappy.png", "pet_assets/lebronhappy.png")
                    sunshine.play()
                elif mood_state=="sad":
                    switch_mood("pet_assets\evillebron.webp", "pet_assets\evillebron.webp", "pet_assets\evillebron.webp", "pet_assets\evillebron.webp", "pet_assets\evillebron.webp")
                    darkness.play()
            if event.key == pygame.K_n:
                switch_mood("pet_assets/stand.png", "pet_assets/walk1_left.png", "pet_assets/walk2_left.png", "pet_assets/walk1_right.png", "pet_assets/walk2_right.png")
            if event.key == pygame.K_0:
                avgScores+=10
            if event.key == pygame.K_MINUS:
                avgScores-=10
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: 
                print("Happiness increased!")
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in buttons:
                button.check_click()
            
        if canvas_button.pressed:
            if check_valid_token(token):
                print("Token found. Proceeding with the game...")
            else: 
                print("Connecting to Canvas...")
                webbrowser.open(api_token_url)
                token = pyperclip.paste()
                while not check_valid_token(token):
                    token = pyperclip.paste()
                write_token(token)
                buttons.clear()
                start_game()
                print(f"Token received: {token}")
        
        if todo_button.pressed:
            loadingText = TextLabel("Loading...", pygame.font.Font("PressStart2p.ttf", 12), "#FFFFFF", (150, screen_height / 8))
            loadingText.draw(screen)
            pygame.display.flip()
            todo = get_to_do_list(token)
            todo_popup = PopupWindow("Canvas Todo List", todo)
            found = False
            loadingText.update_text("")
            pygame.display.flip()
            index = 0 
            for popup in popups:
                if popup.title == "Canvas Todo List":
                    found = True
                    index = popups.index(popup)
            if found:
                popups.pop(index) 
            else:
                popups.append(todo_popup)

        if courses_button.pressed:
            todo_popup = PopupWindow("Canvas Course List", courseLst)
            found = False
            index = 0 
            for popup in popups:
                if popup.title == "Canvas Course List":
                    found = True
                    index = popups.index(popup)
            if found:
                popups.pop(index) 
            else:
                popups.append(todo_popup)
            
        if exit_button.pressed:
            running = False

    if time.time() - last_move_time > move_delay:
        move_towards_target()
        target_x, target_y = target_pos
        if abs(pet_pos[0] - target_x) < target_reach_threshold and abs(pet_pos[1] - target_y) < target_reach_threshold:
            target_pos = random_target()
            last_move_time = time.time()
            move_delay = random.randint(2, 5)
    update_happiness(avgScores)
    if avgScores<30 and mood_state=="happy":
        mood_state="sad"
        switch_mood("pet_assets/idle.png","pet_assets/sadwl1.png","pet_assets/sadwl2.png","pet_assets/sadwr1.png","pet_assets/sadwr2.png")
    if avgScores>30 and mood_state=="sad":
        mood_state="happy"
        switch_mood("pet_assets/stand.png", "pet_assets/walk1_left.png", "pet_assets/walk2_left.png", "pet_assets/walk1_right.png", "pet_assets/walk2_right.png")
    if not minimized:
        screen.fill((0, 0, 0))
        draw_happiness_meter(screen, screen_width, screen_height)
        if pet_pos[0] > target_pos[0]:
            screen.blit(walk1_left_img, (pet_pos[0], pet_pos[1]))
        elif pet_pos[0] < target_pos[0]:
            screen.blit(walk1_right_img, (pet_pos[0], pet_pos[1]))
        else:
            screen.blit(stand_img, (pet_pos[0], pet_pos[1]))
        
        for button in buttons:
            button.draw(screen)
            button.pressed=False
            
        for text in texts:
            text.draw(screen)  
            
        for popup in popups:
            popup.draw(screen)
            
        pygame.display.flip()

    clock.tick(90)

pygame.quit()
