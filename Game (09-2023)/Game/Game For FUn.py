import sys
import os
import pickle

#Base Player
class Player:
    def __init__(self, Health, Attack, Defense, MP):
        self.Health = 10
        self.Attack = 2
        self.Defense = 1
        self.MP = 10


#Game Variables
Run = True
User_Input = ''

#File Management
def Making_Files(File_Name):
    with open(f'{File_Name}.dat', 'w') as f:
        Name = ' '
        Player = Player()



if os.path.isfile('J:\CSCI125\Practice\Game\File_1.dat') == False:
    Files = ['File_1', 'File_2', 'File_3']
    for File_Name in Files:
        Making_Files(File_Name)
else:
    pass



#Game

while Run:
    os.system('cls')
    print("Welcome to the game! \n Start Game \n Quit Game")
    User_Input = input("What would you like to do: ")

    if User_Input.lower() == 'quit game':
        sys.exit()
    elif User_Input.lower() == 'start game':
        os.system('cls')
        User_Input = input("Choose your file: ")
        print('File 1 \n File 2 \n File 3')
        if User_Input.lower() == 'File 1':
            #######################################

    else:
        print('Error Invalid Response!')
        