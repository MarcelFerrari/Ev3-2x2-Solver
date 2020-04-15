# Cube Layout

"""
- -   A B   - -   - -
- -   C D   - -   - -

E F   G H   I J   K L
M N   O P   Q R   S T

- -   U V   - -   - -
- -   W X   - -   - -
"""

import sys
import rpyc
from time import sleep
conn = rpyc.classic.connect('10.42.0.3') # host name or IP address of the EV3
ev3_motor = conn.modules['ev3dev2.motor']
ev3_sensor = conn.modules['ev3dev2.sensor']
ev3_sound = conn.modules['ev3dev2.sound']
ev3_button = conn.modules['ev3dev2.button']

# Going forward enginesda
flip_motor = ev3_motor.MoveTank(ev3_motor.OUTPUT_B, ev3_motor.OUTPUT_C)
turn_motor = ev3_motor.MediumMotor(ev3_motor.OUTPUT_A)
# Def variables
RATIO_ROTATE = 2.3333
# Define basic functions
def flip(n):
    for l in range(n):
        flip_motor.on_for_degrees(ev3_motor.SpeedPercent(70),ev3_motor.SpeedPercent(70), 360, brake=True)
        sleep(0.15)


def turn(k):
    k = k * RATIO_ROTATE * 90
    if k > 0:
        c = 30
    else:
        c = - 30
    turn_motor.on_for_degrees(ev3_motor.SpeedPercent(-35), k + c, brake = True)
    turn_motor.on_for_degrees(ev3_motor.SpeedPercent(-35), - c, brake = True)

# Define basic moves
# Right
def r(n):

    turn(-1)
    flip(2)
    turn(1)
    flip(3)

    turn(n)

    flip(3)
    turn(1)
    flip(2)
    turn(-1)

    flip(2)
# Left
def l(n):

    turn(1)
    flip(2)
    turn(-1)
    flip(3)

    turn( -n)

    flip(3)
    turn(-1)
    flip(2)
    turn(1)

    flip(2)

 # Upper
def u(n):
     flip(2)

     turn(-n)

     flip(2)
# Under
def d(n):
    turn(n)

# Front
def f(n):
    flip(1)

    turn(n)

    flip(3)

# Back
def b(n):
    flip(3)

    turn(n)

    flip(1)

#define permutations for R,U,F
permutation = [[0,7,2,15,4,5,6,21,16,8,3,11,12,13,14,23,17,9,1,19,20,18,22,10],
            [2,0,3,1,6,7,8,9,10,11,4,5,12,13,14,15,16,17,18,19,20,21,22,23],
            [0,1,13,5,4,20,14,6,2,9,10,11,12,21,15,7,3,17,18,19,16,8,22,23]]

def applyMove(state, move):
    return ''.join([state[i] for i in permutation[move]])

def get_solution(scramble):
    #remove up,front,rigth colors
    scramble = ''.join([(' ', x)[x in scramble[12]+scramble[19]+scramble[22]] for x in scramble])
    solved = ' '*4+scramble[12]*2+' '*4+scramble[19]*2+scramble[12]*2+' '*4+scramble[19]*2+scramble[22]*4

    dict1 = {scramble: ''} #stores states with dist 0,1,2,... from the scramble
    dict2 = {solved: ''} #stores states with dist 0,1,2,... from the solved state

    moveName = 'RUF'
    turnName = " 2'"

    for i in range(6):
        tmp = {}
        for state in dict1:
            if state in dict2:
                #solution found
                return dict1[state] + dict2[state]
                exit()
            moveString = dict1[state]
            #do all 9 moves
            for move in range(3):
                for turn in range(3):
                    state = applyMove(state, move)
                    tmp[state] = moveString + moveName[move] + turnName[turn]
                state = applyMove(state, move)
        dict1 = tmp
        tmp = {}
        for state in dict2:
            if state in dict1:
                #solution found
                return dict1[state] + dict2[state]
                exit()
            moveString = dict2[state]
            #do all 9 moves
            for move in range(3):
                for turn in range(3):
                    state = applyMove(state, move)
                    tmp[state] = moveName[move] + turnName[2 - turn] + moveString
                state = applyMove(state, move)
        dict2 = tmp

def solve(scramble):
    print(scramble)
    # Moves list formatting
    raw_moves = []
    moves = []
    # Get solved state
    solved_cube = str(get_solution(scramble)).replace(" ","")
    # Separate each move
    iterator = iter(range(len(solved_cube)))
    print(solved_cube)
    # Loop through each char
    for i in iterator:
        first_index = i
        tmp = solved_cube
        try:
            counter = 1
            while True:
                if solved_cube[i + counter].isalpha():
                    break
                else:
                    counter = counter + 1
                    next(iterator)
            raw_moves.append(tmp[first_index:first_index+counter])
        except:
            raw_moves.append(tmp[first_index:])
    # Reformat output for eval() function
    for i in raw_moves:
        command = ""
        # get move
        if i[0] == "R":
            command = command + "r("
        elif i[0]== "L":
            command = command + "l("
        elif i[0]== "U":
            command = command + "u("
        elif i[0]== "D":
            command = command + "d("
        elif i[0]== "F":
            command = command + "f("
        elif i[0]== "B":
            command = command + "b("
        # Check if inverse
        try:
            if i[1] == "'":
                command = command + "-"
        except:
            pass

        # Add numbers if necessary
        try:
            if i[1] != "'":
                    command = command + i[1:]
            else:
                command = command + i[2:]
                if i[2:] == "":
                    command = command + "1"
        except:
            command = command + "1"
        # Add last )
        command = command + ")"
        moves.append(command)

    print(raw_moves)
    print(moves)
    return moves

if __name__ == "__main__":
    scramble = sys.argv[1]
    solution = solve(scramble)
    for i in solution:
        eval(i)
