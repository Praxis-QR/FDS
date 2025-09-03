from IPython.display import display, HTML
import time
import math
import re

# Created at: 23rd October 2018
#         by: Tolga Atam
# v2.1.0 Updated at: 15th March 2021
#         by: Tolga Atam

# Module for drawing classic Turtle figures on Google Colab notebooks.
# It uses html capabilites of IPython library to draw svg shapes inline.
# Looks of the figures are inspired from Blockly Games / Turtle (blockly-games.appspot.com/turtle)

DEFAULT_WINDOW_SIZE = (800, 500)
DEFAULT_SPEED = 4
DEFAULT_TURTLE_VISIBILITY = True
DEFAULT_PEN_COLOR = 'white'
DEFAULT_TURTLE_DEGREE = 270
DEFAULT_BACKGROUND_COLOR = 'black'
DEFAULT_IS_PEN_DOWN = True
DEFAULT_SVG_LINES_STRING = ""
DEFAULT_PEN_WIDTH = 4
# all 140 color names that modern browsers support. taken from https://www.w3schools.com/colors/colors_names.asp
VALID_COLORS = ('black', 'navy', 'darkblue', 'mediumblue', 'blue', 'darkgreen', 'green', 'teal', 'darkcyan', 'deepskyblue', 'darkturquoise', 'mediumspringgreen', 'lime', 'springgreen', 'aqua', 'cyan', 'midnightblue', 'dodgerblue', 'lightseagreen', 'forestgreen', 'seagreen', 'darkslategray', 'darkslategrey', 'limegreen', 'mediumseagreen', 'turquoise', 'royalblue', 'steelblue', 'darkslateblue', 'mediumturquoise', 'indigo', 'darkolivegreen', 'cadetblue', 'cornflowerblue', 'rebeccapurple', 'mediumaquamarine', 'dimgray', 'dimgrey', 'slateblue', 'olivedrab', 'slategray', 'slategrey', 'lightslategray', 'lightslategrey', 'mediumslateblue', 'lawngreen', 'chartreuse', 'aquamarine', 'maroon', 'purple', 'olive', 'gray', 'grey', 'skyblue', 'lightskyblue', 'blueviolet', 'darkred', 'darkmagenta', 'saddlebrown', 'darkseagreen', 'lightgreen', 'mediumpurple', 'darkviolet', 'palegreen', 'darkorchid', 'yellowgreen', 'sienna', 'brown', 'darkgray', 'darkgrey', 'lightblue', 'greenyellow', 'paleturquoise', 'lightsteelblue', 'powderblue', 'firebrick', 'darkgoldenrod', 'mediumorchid', 'rosybrown', 'darkkhaki', 'silver', 'mediumvioletred', 'indianred', 'peru', 'chocolate', 'tan', 'lightgray', 'lightgrey', 'thistle', 'orchid', 'goldenrod', 'palevioletred', 'crimson', 'gainsboro', 'plum', 'burlywood', 'lightcyan', 'lavender', 'darksalmon', 'violet', 'palegoldenrod', 'lightcoral', 'khaki', 'aliceblue', 'honeydew', 'azure', 'sandybrown', 'wheat', 'beige', 'whitesmoke', 'mintcream', 'ghostwhite', 'salmon', 'antiquewhite', 'linen', 'lightgoldenrodyellow', 'oldlace', 'red', 'fuchsia', 'magenta', 'deeppink', 'orangered', 'tomato', 'hotpink', 'coral', 'darkorange', 'lightsalmon', 'orange', 'lightpink', 'pink', 'gold', 'peachpuff', 'navajowhite', 'moccasin', 'bisque', 'mistyrose', 'blanchedalmond', 'papayawhip', 'lavenderblush', 'seashell', 'cornsilk', 'lemonchiffon', 'floralwhite', 'snow', 'yellow', 'lightyellow', 'ivory', 'white')
VALID_COLORS_SET = set(VALID_COLORS)
# 
# -------------------------new shapes added
# 
DEFAULT_TURTLE_SHAPE = 'turtle'
VALID_TURTLE_SHAPES = ('turtle', 'circle','arrow','car','f1','monkey','woman', 'sedan')
SVG_TEMPLATE = """
      <svg width="{window_width}" height="{window_height}">
        <rect width="100%" height="100%" fill="{background_color}"/>
        {lines}
        {turtle}
      </svg>
    """
TURTLE_TURTLE_SVG_TEMPLATE = """<g visibility={visibility} transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
<path style=" stroke:none;fill-rule:evenodd;fill:{turtle_color};fill-opacity:1;" d="M 18.214844 0.632812 C 16.109375 1.800781 15.011719 4.074219 15.074219 7.132812 L 15.085938 7.652344 L 14.785156 7.496094 C 13.476562 6.824219 11.957031 6.671875 10.40625 7.066406 C 8.46875 7.550781 6.515625 9.15625 4.394531 11.992188 C 3.0625 13.777344 2.679688 14.636719 3.042969 15.027344 L 3.15625 15.152344 L 3.519531 15.152344 C 4.238281 15.152344 4.828125 14.886719 8.1875 13.039062 C 9.386719 12.378906 10.371094 11.839844 10.378906 11.839844 C 10.386719 11.839844 10.355469 11.929688 10.304688 12.035156 C 9.832031 13.09375 9.257812 14.820312 8.96875 16.078125 C 7.914062 20.652344 8.617188 24.53125 11.070312 27.660156 C 11.351562 28.015625 11.363281 27.914062 10.972656 28.382812 C 8.925781 30.84375 7.945312 33.28125 8.238281 35.1875 C 8.289062 35.527344 8.28125 35.523438 8.917969 35.523438 C 10.941406 35.523438 13.074219 34.207031 15.136719 31.6875 C 15.359375 31.417969 15.328125 31.425781 15.5625 31.574219 C 16.292969 32.042969 18.023438 32.964844 18.175781 32.964844 C 18.335938 32.964844 19.941406 32.210938 20.828125 31.71875 C 20.996094 31.625 21.136719 31.554688 21.136719 31.558594 C 21.203125 31.664062 21.898438 32.414062 22.222656 32.730469 C 23.835938 34.300781 25.5625 35.132812 27.582031 35.300781 C 27.90625 35.328125 27.9375 35.308594 28.007812 34.984375 C 28.382812 33.242188 27.625 30.925781 25.863281 28.425781 L 25.542969 27.96875 L 25.699219 27.785156 C 28.945312 23.960938 29.132812 18.699219 26.257812 11.96875 L 26.207031 11.84375 L 27.945312 12.703125 C 31.53125 14.476562 32.316406 14.800781 33.03125 14.800781 C 33.976562 14.800781 33.78125 13.9375 32.472656 12.292969 C 28.519531 7.355469 25.394531 5.925781 21.921875 7.472656 L 21.558594 7.636719 L 21.578125 7.542969 C 21.699219 6.992188 21.761719 5.742188 21.699219 5.164062 C 21.496094 3.296875 20.664062 1.964844 19.003906 0.855469 C 18.480469 0.503906 18.457031 0.5 18.214844 0.632812"/>
</g>"""
TURTLE_CIRCLE_SVG_TEMPLATE = """
      <g visibility={visibility} transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
        <circle stroke="{turtle_color}" stroke-width="3" fill="transparent" r="12" cx="0" cy="0"/>
        <polygon points="0,19 3,16 -3,16" style="fill:{turtle_color};stroke:{turtle_color};stroke-width:2"/>
      </g>
    """
TURTLE_ARROW_SVG_TEMPLATE = """<g visibility={visibility} 
    transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
  <polygon points="0,-16 10,0 4,0 4,12 -4,12 -4,0 -10,0"
           style="fill:{turtle_color};stroke:{turtle_color};stroke-width:1"/>
</g>"""

TURTLE_CAR_SVG_TEMPLATE = """<g visibility={visibility} transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
  <!-- car body -->
  <rect x="-18" y="-12" rx="3" ry="3" width="36" height="14"
        style="fill:{turtle_color};stroke:#000;stroke-width:1"/>
  <!-- roof / cabin -->
  <path d="M -10 -12 L -4 -18 L 8 -18 L 14 -12 Z"
        style="fill:{turtle_color};stroke:#000;stroke-width:1"/>
  <!-- windows -->
  <rect x="-3.5" y="-16.5" width="4.5" height="5" rx="1"
        style="fill:rgba(255,255,255,0.9);stroke:none"/>
  <rect x="6" y="-16.5" width="4.5" height="5" rx="1"
        style="fill:rgba(255,255,255,0.9);stroke:none"/>
  <!-- bumpers / lower detail -->
  <rect x="-18" y="0" width="6" height="3" style="fill:#111;stroke:none"/>
  <rect x="12" y="0" width="6" height="3" style="fill:#111;stroke:none"/>
  <!-- wheels -->
  <g transform="translate(-8,10)">
    <circle cx="0" cy="0" r="4" style="fill:#222;stroke:#000;stroke-width:0.8"/>
    <circle cx="0" cy="0" r="1.4" style="fill:rgba(255,255,255,0.6);stroke:none"/>
  </g>
  <g transform="translate(10,10)">
    <circle cx="0" cy="0" r="4" style="fill:#222;stroke:#000;stroke-width:0.8"/>
    <circle cx="0" cy="0" r="1.4" style="fill:rgba(255,255,255,0.6);stroke:none"/>
  </g>
</g>"""

TURTLE_F1_SVG_TEMPLATE = """<g visibility={visibility} 
    transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">

  <!-- central body -->
  <rect x="-6" y="-22" width="12" height="44" 
        style="fill:{turtle_color};stroke:#000;stroke-width:1"/>

  <!-- front wing -->
  <rect x="-20" y="-24" width="40" height="4" 
        style="fill:#333;stroke:#000;stroke-width:0.5"/>

  <!-- rear wing -->
  <rect x="-16" y="20" width="32" height="4" 
        style="fill:#333;stroke:#000;stroke-width:0.5"/>

  <!-- cockpit -->
  <ellipse cx="0" cy="-5" rx="5" ry="7" 
           style="fill:rgba(255,255,255,0.8);stroke:#000;stroke-width:0.5"/>

  <!-- wheels -->
  <rect x="-18" y="-20" width="6" height="10" rx="2" 
        style="fill:#111;stroke:#000;stroke-width:0.5"/>
  <rect x="12"  y="-20" width="6" height="10" rx="2" 
        style="fill:#111;stroke:#000;stroke-width:0.5"/>

  <rect x="-18" y="10" width="6" height="10" rx="2" 
        style="fill:#111;stroke:#000;stroke-width:0.5"/>
  <rect x="12"  y="10" width="6" height="10" rx="2" 
        style="fill:#111;stroke:#000;stroke-width:0.5"/>

</g>"""

TURTLE_MONKEY_SVG_TEMPLATE = """
<g visibility={visibility}
   transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
  <!-- Hair (black, covering top and sides, NOT chin) -->
  <path d="M -16,-5 
           Q 0,-25 16,-5 
           Q 14,8 8,14 
           Q 0,20 -8,14 
           Q -14,8 -16,-5 Z"
        fill="black" stroke="black" stroke-width="1"/>

  <!-- Face -->
  <circle cx="0" cy="0" r="12" fill="#FFD1A9" stroke="{turtle_color}" stroke-width="2"/>

  <!-- Eyes -->
  <circle cx="-4" cy="-3" r="2" fill="black"/>
  <circle cx="4" cy="-3" r="2" fill="black"/>

  <!-- Smile -->
  <path d="M -5,4 Q 0,10 5,4" stroke="black" stroke-width="2" fill="none"/>
</g>
"""

TURTLE_WOMAN_SVG_TEMPLATE = """
<g visibility={visibility}
   transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
  <!-- Hair (changed to black) -->
  <path fill="black" d="M18 3c6 0 16 3 16 16s0 16-3 16-7-3-13-3-9.915 3-13 3c-3.343 0-3-12-3-16C2 6 12 3 18 3z"/>
  
  <!-- Face -->
  <path fill="#FFDC5D" d="M6 18.562c0-8.526 5.373-15.438 12-15.438s12 6.912 12 15.438S24.627 34 18 34 6 27.088 6 18.562z"/>
  
  <!-- Mouth -->
  <path fill="#DF1F32" d="M18 30c-2.347 0-3.575-1.16-3.707-1.293-.391-.391-.391-1.023 0-1.414.387-.387 1.013-.39 1.404-.01.051.047.806.717 2.303.717 1.519 0 2.273-.69 2.305-.719.398-.373 1.027-.362 1.408.029.379.393.38 1.011-.006 1.397C21.575 28.84 20.347 30 18 30z"/>
  
  <!-- Nose -->
  <path fill="#C1694F" d="M19 25h-2c-.552 0-1-.447-1-1s.448-1 1-1h2c.553 0 1 .447 1 1s-.447 1-1 1z"/>
  
  <!-- Hair top shading (changed to black) -->
  <path fill="black" d="M3.064 24c-.03-.325-.064-.647-.064-1 0-5 3 .562 3-3 0-3.563 2-4 4-6l3-3s5 3 9 3 8 2 8 6 3-2 3 3c0 .355-.033.673-.058 1h1.049C34 22.523 34 20.868 34 19 34 6 24 1 18 1S2 6 2 19c0 1.158-.028 2.986.012 5h1.052z"/>
  
  <!-- Eyes -->
  <path d="M13 22c-.552 0-1-.447-1-1v-2c0-.552.448-1 1-1s1 .448 1 1v2c0 .553-.448 1-1 1zm10 0c-.553 0-1-.447-1-1v-2c0-.552.447-1 1-1s1 .448 1 1v2c0 .553-.447 1-1 1z" fill="#662113"/>
</g>
"""

TURTLE_SEDAN_SVG_TEMPLATE = """
<g visibility={visibility}
   transform="rotate({degrees},{rotation_x},{rotation_y}) translate({turtle_x}, {turtle_y})">
   <!-- Sedan Top View -->
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 358.85 789.36" width="45" height="45">
     
     <!-- Wheels -->
     <rect fill="#60585a" x="16.287" y="623.04" width="27.775" height="78.696" rx="8.58" ry="8.58"/>
     <rect fill="#60585a" x="311.29" y="613.04" width="27.775" height="78.696" rx="8.58" ry="8.58"/>
     <rect fill="#60585a" x="318.79" y="98.038" width="27.775" height="78.696" rx="8.58" ry="8.58"/>
     <rect fill="#60585a" x="8.633"  y="101.12" width="27.775" height="78.696" rx="8.58" ry="8.58"/>

     <!-- Body (blue) -->
     <path d="M178.73 782.98c-113.07 2.362-130.4-17.92-147.11-21.261-16.705-38.776-19.877-365.73-9.855-392.46
              7.493-60.54-4.936-70.565-8.687-143.53-7.14-85.213 9.815-37.829-4.439-124.48
              21.658-90.216-19.136-92.053 168.52-100.63 172.21 2.401 147.96 10.415 169.61 100.63
              -14.254 86.652 2.701 39.268-4.439 124.48-3.751 72.961-16.18 82.986-8.687 143.53
              10.022 26.727 6.85 353.68-9.855 392.46-26.153 15.153-95.459 21.261-145.07 21.261z"
           fill="#1e3a8a" stroke="#000" stroke-width="1"/>

     <!-- Roof (orange) -->
     <path d="M37.198 44.521c-11.667 18.667-10.816 196.22 7.851 210.22
              18.03-14.851 122.48-28.646 142.34-27.364
              20.288-1.492 99.694 8.055 124.09 22.697
              6.577 2.13 19.727-205.55 1.059-219.55
              -58.34-16.344-252.01-16.344-275.34 13.99z"
           fill="#f97316" stroke="#000" stroke-width="1"/>

     <!-- Glass areas -->
     <!-- Front windshield -->
     <rect x="90" y="70" width="180" height="80"
           fill="#93c5fd" fill-opacity="0.7" stroke="black" stroke-width="0.5" rx="10" ry="10"/>
     <!-- Rear windshield -->
     <rect x="100" y="640" width="160" height="70"
           fill="#93c5fd" fill-opacity="0.7" stroke="black" stroke-width="0.5" rx="10" ry="10"/>
     <!-- Left side windows -->
     <rect x="55" y="200" width="40" height="300"
           fill="#93c5fd" fill-opacity="0.7" stroke="black" stroke-width="0.5" rx="6" ry="6"/>
     <!-- Right side windows -->
     <rect x="265" y="200" width="40" height="300"
           fill="#93c5fd" fill-opacity="0.7" stroke="black" stroke-width="0.5" rx="6" ry="6"/>

   </svg>
</g>
"""


# 
# -------------------------new shapes end 
# 

SPEED_TO_SEC_MAP = {1: 1.5, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.3, 6: 0.18, 7: 0.12, 8: 0.06, 9: 0.04, 10: 0.02, 11: 0.01, 12: 0.001, 13: 0.0001}


# helper function that maps [1,13] speed values to ms delays
def _speedToSec(speed):
    return SPEED_TO_SEC_MAP[speed]


turtle_speed = DEFAULT_SPEED

is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
pen_color = DEFAULT_PEN_COLOR
window_size = DEFAULT_WINDOW_SIZE
turtle_pos = (DEFAULT_WINDOW_SIZE[0] // 2, DEFAULT_WINDOW_SIZE[1] // 2)
turtle_degree = DEFAULT_TURTLE_DEGREE
background_color = DEFAULT_BACKGROUND_COLOR
is_pen_down = DEFAULT_IS_PEN_DOWN
svg_lines_string = DEFAULT_SVG_LINES_STRING
pen_width = DEFAULT_PEN_WIDTH
turtle_shape = DEFAULT_TURTLE_SHAPE

drawing_window = None


# construct the display for turtle
def initializeTurtle(initial_speed=DEFAULT_SPEED, initial_window_size=DEFAULT_WINDOW_SIZE):
    global window_size
    global drawing_window
    global turtle_speed
    global is_turtle_visible
    global pen_color
    global turtle_pos
    global turtle_degree
    global background_color
    global is_pen_down
    global svg_lines_string
    global pen_width
    global turtle_shape

    if isinstance(initial_speed,int) == False or initial_speed not in range(1, 14):
        raise ValueError('initial_speed must be an integer in interval [1,13]')
    turtle_speed = initial_speed

    if not (isinstance(initial_window_size, tuple) and len(initial_window_size) == 2 and isinstance(
            initial_window_size[0], int) and isinstance(initial_window_size[1], int)):
        raise ValueError('window_size must be a tuple of 2 integers')

    window_size = initial_window_size

    is_turtle_visible = DEFAULT_TURTLE_VISIBILITY
    pen_color = DEFAULT_PEN_COLOR
    turtle_pos = (window_size[0] // 2, window_size[1] // 2)
    turtle_degree = DEFAULT_TURTLE_DEGREE
    background_color = DEFAULT_BACKGROUND_COLOR
    is_pen_down = DEFAULT_IS_PEN_DOWN
    svg_lines_string = DEFAULT_SVG_LINES_STRING
    pen_width = DEFAULT_PEN_WIDTH
    turtle_shape = DEFAULT_TURTLE_SHAPE

    drawing_window = display(HTML(_generateSvgDrawing()), display_id=True)


# helper function for generating svg string of the turtle
def _generateTurtleSvgDrawing():
    if is_turtle_visible:
        vis = 'visible'
    else:
        vis = 'hidden'

    turtle_x = turtle_pos[0]
    turtle_y = turtle_pos[1]
    degrees = turtle_degree
    template = ''

    if turtle_shape == 'turtle':
        turtle_x -= 18
        turtle_y -= 18
        degrees += 90
        template = TURTLE_TURTLE_SVG_TEMPLATE

    elif turtle_shape == 'circle':
        degrees -= 90
        template = TURTLE_CIRCLE_SVG_TEMPLATE
# 
# -------------------------new shapes added
# 
    elif turtle_shape == 'arrow':
        degrees += 90
        template = TURTLE_ARROW_SVG_TEMPLATE
        
    elif turtle_shape == 'car':
        degrees += 90
        template = TURTLE_CAR_SVG_TEMPLATE
    elif turtle_shape == 'f1':
        degrees += 90
        template = TURTLE_F1_SVG_TEMPLATE
    elif turtle_shape == 'sedan':
        turtle_x -= 18
        turtle_y -= 18
        degrees += 90
        template = TURTLE_SEDAN_SVG_TEMPLATE
    elif turtle_shape == 'monkey':
        degrees += 90
        template = TURTLE_MONKEY_SVG_TEMPLATE
    elif turtle_shape == 'woman':
        turtle_x -= 18
        turtle_y -= 18
        degrees += 90
        template = TURTLE_WOMAN_SVG_TEMPLATE
# 
# -------------------------new shapes end
# 
    else:
        # fallback in case of typo or unsupported shape
        degrees -= 90
        template = TURTLE_CIRCLE_SVG_TEMPLATE

    return template.format(turtle_color=pen_color, turtle_x=turtle_x, turtle_y=turtle_y, \
                                      visibility=vis, degrees=degrees, rotation_x=turtle_pos[0], rotation_y=turtle_pos[1])


# helper function for generating the whole svg string
def _generateSvgDrawing():
    return SVG_TEMPLATE.format(window_width=window_size[0], window_height=window_size[1],
                               background_color=background_color, lines=svg_lines_string,
                               turtle=_generateTurtleSvgDrawing())


# helper functions for updating the screen using the latest positions/angles/lines etc.
def _updateDrawing():
    if drawing_window == None:
        raise AttributeError("Display has not been initialized yet. Call initializeTurtle() before using.")
    time.sleep(_speedToSec(turtle_speed))
    drawing_window.update(HTML(_generateSvgDrawing()))


# helper function for managing any kind of move to a given 'new_pos' and draw lines if pen is down
def _moveToNewPosition(new_pos):
    global turtle_pos
    global svg_lines_string

    # rounding the new_pos to eliminate floating point errors.
    new_pos = ( round(new_pos[0],3), round(new_pos[1],3) )

    start_pos = turtle_pos
    if is_pen_down:
        svg_lines_string += """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-linecap="round" style="stroke:{pen_color};stroke-width:{pen_width}"/>""".format(
            x1=start_pos[0], y1=start_pos[1], x2=new_pos[0], y2=new_pos[1], pen_color=pen_color, pen_width=pen_width)

    turtle_pos = new_pos
    _updateDrawing()


# makes the turtle move forward by 'units' units
def forward(units):
    if not isinstance(units, (int,float)):
        raise ValueError('units must be a number.')

    alpha = math.radians(turtle_degree)
    ending_point = (turtle_pos[0] + units * math.cos(alpha), turtle_pos[1] + units * math.sin(alpha))

    _moveToNewPosition(ending_point)

fd = forward # alias

# makes the turtle move backward by 'units' units
def backward(units):
    if not isinstance(units, (int,float)):
        raise ValueError('units must be a number.')
    forward(-1 * units)

bk = backward # alias
back = backward # alias


# makes the turtle move right by 'degrees' degrees (NOT radians)
def right(degrees):
    global turtle_degree

    if not isinstance(degrees, (int,float)):
        raise ValueError('degrees must be a number.')

    turtle_degree = (turtle_degree + degrees) % 360
    _updateDrawing()

rt = right # alias

# makes the turtle face a given direction
def face(degrees):
    global turtle_degree

    if not isinstance(degrees, (int,float)):
        raise ValueError('degrees must be a number.')

    turtle_degree = degrees % 360
    _updateDrawing()

setheading = face # alias
seth = face # alias

# makes the turtle move right by 'degrees' degrees (NOT radians, this library does not support radians right now)
def left(degrees):
    if not isinstance(degrees, (int,float)):
        raise ValueError('degrees must be a number.')
    right(-1 * degrees)

lt = left

# raises the pen such that following turtle moves will not cause any drawings
def penup():
    global is_pen_down

    is_pen_down = False
    # TODO: decide if we should put the timout after lifting the pen
    # _updateDrawing()

pu = penup # alias
up = penup # alias

# lowers the pen such that following turtle moves will now cause drawings
def pendown():
    global is_pen_down

    is_pen_down = True
    # TODO: decide if we should put the timout after releasing the pen
    # _updateDrawing()

pd = pendown # alias
down = pendown # alias

def isdown():
    return is_pen_down

# update the speed of the moves, [1,13]
# if argument is omitted, it returns the speed.
def speed(speed = None):
    global turtle_speed

    if speed is None:
        return turtle_speed

    if isinstance(speed,int) == False or speed not in range(1, 14):
        raise ValueError('speed must be an integer in the interval [1,13].')
    turtle_speed = speed
    # TODO: decide if we should put the timout after changing the speed
    # _updateDrawing()


# move the turtle to a designated 'x' x-coordinate, y-coordinate stays the same
def setx(x):
    if not isinstance(x, (int,float)):
        raise ValueError('new x position must be a number.')
    if x < 0:
        raise ValueError('new x position must be non-negative.')
    _moveToNewPosition((x, turtle_pos[1]))


# move the turtle to a designated 'y' y-coordinate, x-coordinate stays the same
def sety(y):
    if not isinstance(y, (int,float)):
        raise ValueError('new y position must be a number.')
    if y < 0:
        raise ValueError('new y position must be non-negative.')
    _moveToNewPosition((turtle_pos[0], y))


def home():
    global turtle_degree

    turtle_degree = DEFAULT_TURTLE_DEGREE
    _moveToNewPosition( (window_size[0] // 2, window_size[1] // 2) ) # this will handle updating the drawing.

# retrieve the turtle's currrent 'x' x-coordinate
def getx():
    return(turtle_pos[0])

xcor = getx # alias

# retrieve the turtle's currrent 'y' y-coordinate
def gety():
    return(turtle_pos[1])

ycor = gety # alias

# retrieve the turtle's current position as a (x,y) tuple vector
def position():
    return turtle_pos

pos = position # alias

# retrieve the turtle's current angle
def getheading():
    return turtle_degree

heading = getheading # alias

# move the turtle to a designated 'x'-'y' coordinate
def goto(x, y=None):
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('the tuple argument must be of length 2.')

        y = x[1]
        x = x[0]

    if not isinstance(x, (int,float)):
        raise ValueError('new x position must be a number.')
    if x < 0:
        raise ValueError('new x position must be non-negative')
    if not isinstance(y, (int,float)):
        raise ValueError('new y position must be a number.')
    if y < 0:
        raise ValueError('new y position must be non-negative.')
    _moveToNewPosition((x, y))

setpos = goto # alias
setposition = goto # alias

# switch turtle visibility to ON
def showturtle():
    global is_turtle_visible

    is_turtle_visible = True
    _updateDrawing()

st = showturtle # alias

# switch turtle visibility to OFF
def hideturtle():
    global is_turtle_visible

    is_turtle_visible = False
    _updateDrawing()

ht = hideturtle # alias

def isvisible():
    return is_turtle_visible

def _validateColorString(color):
    if color in VALID_COLORS_SET: # 140 predefined html color names
        return True
    if re.search("^#(?:[0-9a-fA-F]{3}){1,2}$", color): # 3 or 6 digit hex color code
        return True
    if re.search("rgb\(\s*(?:(?:\d{1,2}|1\d\d|2(?:[0-4]\d|5[0-5]))\s*,?){3}\)$", color): # rgb color code
        return True
    return False

def _validateColorTuple(color):
    if len(color) != 3:
        return False
    if not isinstance(color[0], int) or not isinstance(color[1], int) or not isinstance(color[2], int):
        return False
    if not 0 <= color[0] <= 255 or not 0 <= color[1] <= 255 or not 0 <= color[2] <= 255:
        return False
    return True

def _processColor(color):
    if isinstance(color, str):
        color = color.lower()
        if not _validateColorString(color):
            raise ValueError('color is invalid. it can be a known html color name, 3-6 digit hex string or rgb string.')
        return color
    elif isinstance(color, tuple):
        if not _validateColorTuple(color):
            raise ValueError('color tuple is invalid. it must be a tuple of three integers, which are in the interval [0,255]')
        return 'rgb(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
    else:
        raise ValueError('the first parameter must be a color string or a tuple')

# change the background color of the drawing area
# if no params, return the current background color
def bgcolor(color = None, c2 = None, c3 = None):
    global background_color

    if color is None:
        return background_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('if the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    background_color = _processColor(color)
    _updateDrawing()


# change the color of the pen
# if no params, return the current pen color
def color(color = None, c2 = None, c3 = None):
    global pen_color

    if color is None:
        return pen_color
    elif c2 is not None:
        if c3 is None:
            raise ValueError('if the second argument is set, the third arguments must be set as well to complete the rgb set.')
        color = (color, c2, c3)

    pen_color = _processColor(color)
    _updateDrawing()

pencolor = color

# change the width of the lines drawn by the turtle, in pixels
# if the function is called without arguments, it returns the current width
def width(width = None):
    global pen_width

    if width is None:
        return pen_width
    else:
        if not isinstance(width, int):
            raise ValueError('new width position must be an integer.')
        if not width > 0:
            raise ValueError('new width position must be positive.')

        pen_width = width
        # TODO: decide if we should put the timout after changing the pen_width
        # _updateDrawing()

pensize = width

# calculate the distance between the turtle and a given point
def distance(x, y=None):
    if isinstance(x, tuple) and y is None:
        if len(x) != 2:
            raise ValueError('the tuple argument must be of length 2.')

        y = x[1]
        x = x[0]

    if not isinstance(x, (int,float)):
        raise ValueError('new x position must be a number.')
    if x < 0:
        raise ValueError('new x position must be non-negative')
    if not isinstance(y, (int,float)):
        raise ValueError('new y position must be a number.')
    if not y < 0:
        raise ValueError('new y position must be non-negative.')

    if not isinstance(point, tuple) or len(point) != 2 or (not isinstance(point[0], int) and not isinstance(point[0], float)) or (not isinstance(point[1], int) and not isinstance(point[1], float)):
        raise ValueError('the vector given for the point must be a tuple with 2 numbers.')

    return round(math.sqrt( (turtle_pos[0] - x) ** 2 + (turtle_pos[1] - y) ** 2 ), 4)

# clear any text or drawing on the screen
def clear():
    global svg_lines_string

    svg_lines_string = ""
    _updateDrawing()

def write(obj, **kwargs):
    global svg_lines_string
    global turtle_pos
    text = str(obj)
    font_size = 12
    font_family = 'Arial'
    font_type = 'normal'
    align = 'start'

    if 'align' in kwargs and kwargs['align'] in ('left', 'center', 'right'):
        if kwargs['align'] == 'left':
            align = 'start'
        elif kwargs['align'] == 'center':
            align = 'middle'
        else:
            align = 'end'

    if "font" in kwargs:
        font = kwargs["font"]
        if len(font) != 3 or isinstance(font[0], int) == False or isinstance(font[1], str) == False or font[2] not in {'bold','italic','underline','normal'}:
            raise ValueError('font parameter must be a triplet consisting of font size (int), font family (str) and font type. font type can be one of {bold, italic, underline, normal}')
        font_size = font[0]
        font_family = font[1]
        font_type = font[2]
        
    style_string = ""
    style_string += "font-size:" + str(font_size) + "px;"
    style_string += "font-family:'" + font_family + "';"

    if font_type == 'bold':
        style_string += "font-weight:bold;"
    elif font_type == 'italic':
        style_string += "font-style:italic;"
    elif font_type == 'underline':
        style_string += "text-decoration: underline;"

    
    svg_lines_string += """<text x="{x}" y="{y}" fill="{fill_color}" text-anchor="{align}" style="{style}">{text}</text>""".format(x=turtle_pos[0], y=turtle_pos[1], text=text, fill_color=pen_color, align=align, style=style_string)
    
    _updateDrawing()

def shape(shape=None):
    global turtle_shape
    if shape is None:
        return turtle_shape
    elif shape not in VALID_TURTLE_SHAPES:
        raise ValueError('shape is invalid. valid options are: ' + str(VALID_TURTLE_SHAPES))
    
    turtle_shape = shape
    _updateDrawing()

# return turtle window width
def window_width():
    return window_size[0]

# return turtle window height
def window_height():
    return window_size[1]
