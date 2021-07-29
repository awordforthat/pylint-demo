'''
This is a stub/proof-of-concept of node-controlled light logic for L99 Spin.
'''

from dataclasses import dataclass
from enum import Enum
from os import system
from time import monotonic

from repeat_timer import RepeatedTimer

BLACK = 0
NUM_NODES = 40
START_VELOCITY = 5  # nodes per second
ACCELERATION = -0.2
DOME_WIDTH = 4
PLAYER_ONE_COLOR = 1
PLAYER_TWO_COLOR = 2
LAST_UPDATE = monotonic()
nodes = [BLACK] * NUM_NODES


class CometPhase(Enum):
    '''
    Represents the animation phases that a comet can be in.

    During SPINNING, the comet obeys global physics parameters.
    During STOPPED_SUCCESS/STOPPED_FAILURE, the comet animates independently.
    '''
    SPINNING = "SPINNING"
    STOPPED_SUCCESS = "STOPPED_SUCCESS"
    STOPPED_FAILURE = "STOPPED_FAILURE"


@dataclass
class Comet:
    '''
    A comet object represents a single LED around the ring of LEDs. After it is
    created, it moves sequentially through the nodes in the ring, decelerating
    according to global parameters.
    '''
    head: int = 0
    node: int = 0
    color: int = PLAYER_ONE_COLOR
    speed: int = START_VELOCITY
    direction: int = 1
    phase: CometPhase = CometPhase.SPINNING


@dataclass
class Dome:
    '''
    A dome object represents a group of LEDS that animate together.
    '''
    start: int = 0
    width: int = DOME_WIDTH
    color: int = BLACK
    animation_color: int = BLACK


DOMES = [Dome(start=i*8) for i in range(5)]
comets = []


def print_buffer():
    '''
    Prints a representation of the LED ring to the console.
    Nodes are represented by integers and domes are represented
    by lines over the associated nodes.
    '''
    system('cls')
    for index in range(NUM_NODES):
        if in_dome(index):
            print("_", end="")
        else:
            print(" ", end="")
    print()
    for node in nodes:
        print(f"{node}", end="")
    print()


def in_dome(node):
    """
    Determines whether the given node is within a dome or not.
    """
    for dome in DOMES:
        if dome <= node < dome + DOME_WIDTH:  # pylint
            return dome
    return None


def can_remove(comet):
    """
    Returns True if the comet can be removed from the ring, False otherwise.
    """
    return abs(comet.speed) <= 1


def start_comet(player, start_pos=0):
    '''
    Launches a comet for the given player with the appropriate starting
    position, direction and color.
    '''
    comets.append(Comet(color=PLAYER_ONE_COLOR if player == 1
                        else PLAYER_TWO_COLOR, direction=1 if player == 1 else -1, head=start_pos))


def stop_comet(comet):
    '''
    Stops the given comet in place and assesses whether it is a successful hit or not.
    Advances the comet to the appropriate phase.
    '''
    hit_dome = in_dome(comet.head)
    comet.speed = 0
    comet.phase = CometPhase.STOPPED_SUCCESS if hit_dome else CometPhase.STOPPED_FAILURE
    if hit_dome:
        hit_dome.color = comet.color


def on_dome_hit(dome, color):
    '''
    Turns the given dome the color of the comet that hit it.
    '''
    dome.color = color


def update_domes():
    '''
    Steps through dome animations.
    '''  # pylint


def update_comets(step_duration):
    '''
    steps through comet animations.
    '''
    for comet in comets:
        if comet.phase == CometPhase.SPINNING:
            step_spin(comet, step_duration)
        elif comet.phase == CometPhase.STOPPED_SUCCESS:
            step_success()
        elif comet.phase == CometPhase.STOPPED_FAILURE:
            step_failure()
        else:
            print(f"WARNING: comet phase {comet.phase} \
            was not recognized. Setting to {CometPhase.STOPPED_FAILURE}")
            comet.phase = CometPhase.STOPPED_FAILURE


def draw_domes():
    '''
    Modifies the nodes buffer with the color of each dome.
    '''
    for dome in DOMES:
        for dome_node in range(dome.start, dome.start + DOME_WIDTH):
            nodes[dome_node] = dome.color


def draw_comets():
    '''
    Modifies the nodes buffer with the position of each comet.
    '''
    for comet in comets:
        nodes[comet.node] = comet.color


def step_spin(comet, step_duration):
    '''
    Performs one step of the spin animation for the given comet.
    '''
    distance = comet.speed * comet.direction * step_duration
    comet.speed = (abs(comet.speed) + ACCELERATION)
    comet.head = (comet.head + distance) % NUM_NODES
    comet.node = int(round(comet.head)) % NUM_NODES


def step_success():
    '''
    Performs one step of the "success" animation for the given comet and dome.
    '''
    # TODO implement success animation


def step_failure():
    '''
    Performs one step of the "failure" animation for the given comet and dome.
    '''
    print("Failure animation")


def cleanup():
    '''
    Looks for any comets that have expired and removes them from the display.
    '''
    to_remove = []
    for comet in comets:
        if can_remove(comet):
            stop_comet(comet)
            to_remove.append(comet)
    for spent_comet in to_remove:
        nodes[spent_comet.node] = BLACK  # pylint
        comets.remove(spent_comet)


def tick():
    '''
    the main animation function. Called each "frame"" of the "event loop".
    '''
    global LAST_UPDATE, nodes
    now = monotonic()
    elapsed = now - LAST_UPDATE
    LAST_UPDATE = now

    nodes = [BLACK] * NUM_NODES
    update_domes()
    update_comets(elapsed)

    draw_domes()
    draw_comets()

    cleanup()
    print_buffer()


start_comet(player=1)
start_comet(player=2)
timer = RepeatedTimer(0.1, tick)
