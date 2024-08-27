# %%

# The markers "# %%" separate code blocks for execution (cells) 
# Press shift-enter to exectute a cell and move to next cell
# Press ctrl-enter to exectute a cell and keep cursor at the position
# For more details, see https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter

# %%

from build123d import *
from ocp_vscode import *
import copy

# %%

def in_to_mm(li):
    return tuple([25.4 * i for i in li])

boss_locations = (in_to_mm([0.10, 0.60]),
                  in_to_mm([0.70, 2.60]),
                  in_to_mm([1.80, 2.60]),
                  in_to_mm([2.00, 0.55]))

cube_locations = (in_to_mm([0.10-(2/25.4), 0.60         ]),
                  in_to_mm([0.70         , 2.60+(2/25.4)]),
                  in_to_mm([1.80         , 2.60+(2/25.4)]),
                  in_to_mm([2.00+(2/25.4), 0.55         ]))

with BuildSketch(Location(in_to_mm([-2.10/2, -2.70/2]))) as board_base:
    with BuildLine() as board_outline:
        l1 = Line(in_to_mm([0.00, 0.00]), in_to_mm([0.00, 2.60]))
        l3 = Line(in_to_mm([0.00, 2.60]), in_to_mm([0.51, 2.60]))
        l4 = Line(in_to_mm([0.51, 2.60]), in_to_mm([0.61, 2.70]))
        l5 = Line(in_to_mm([0.61, 2.70]), in_to_mm([1.90, 2.70]))
        l6 = Line(in_to_mm([1.90, 2.70]), in_to_mm([2.00, 2.60]))
        l7 = Line(in_to_mm([2.00, 2.60]), in_to_mm([2.10, 2.60]))
        l8 = Line(in_to_mm([2.10, 2.60]), in_to_mm([2.10, 0.00]))
        l9 = Line(in_to_mm([2.10, 0.00]), in_to_mm([0.00, 0.00]))

    make_face()

breadboard_frame_width = 61.5
arduino_board_width = 25.4*2.10
arduino_board_buffer = arduino_board_width + 1.0

arduino_board_offset = (breadboard_frame_width - arduino_board_width)/2
arduino_board_inset = (breadboard_frame_width - arduino_board_buffer)/2


with BuildSketch() as board_frame:
    offset(board_base.sketch, amount= (arduino_board_offset), kind=Kind.INTERSECTION)
    offset(amount= -arduino_board_inset, kind=Kind.INTERSECTION, mode=Mode.SUBTRACT)

with BuildSketch() as board_hex:

    offset(board_base.sketch, amount= 0.50, kind=Kind.INTERSECTION)

    with HexLocations(5, 7, 8, [Align.CENTER, Align.CENTER]):
         RegularPolygon(4.5,6, mode=Mode.SUBTRACT)

with BuildSketch() as board_border:
    offset(board_base.sketch, amount= 0.50, kind=Kind.INTERSECTION)
    offset(amount=-2.00, kind=Kind.INTERSECTION, mode=Mode.SUBTRACT)

with BuildSketch(Location(in_to_mm([-2.10/2, -2.70/2]))) as boss_base:
    with Locations(*cube_locations):
        Rectangle(4,4, mode=Mode.ADD)

    with Locations(*boss_locations):
        Circle(radius=4.00, mode=Mode.ADD)

with BuildSketch(Location(in_to_mm([-2.10/2, -2.70/2]))) as bosses:
    with Locations(*cube_locations):
        Rectangle(5,5, mode=Mode.ADD)

    with Locations(*boss_locations):
        Circle(radius=2.50, mode=Mode.ADD)

with BuildPart() as arduino_uno_board:
     extrude(board_frame.sketch, amount=7)
     extrude(board_hex.sketch, amount=1.50)
     extrude(board_border.sketch, amount=1.50)
     extrude(boss_base.sketch, amount=1.50)
     extrude(bosses.sketch, amount=5.50)

     with Locations((0.00,-25.40*(2.70/2)-2.00,1.5)):
         Box(50,2.20,7.00,align=(Align.CENTER, Align.MAX, Align.MIN), mode=Mode.SUBTRACT)

     with Locations((0.00,-25.40*(2.70/2)-0.50,5.5)):
         Box(50,2.00,2.00,align=(Align.CENTER, Align.MAX, Align.MIN), mode=Mode.SUBTRACT)

     hole_locations = tuple(Location(loc) for loc in boss_locations)

     for loc in hole_locations:
         loc.position -= in_to_mm([2.10/2, 2.70/2])

     with Locations(*hole_locations):
         holes = Hole(radius=1.25)
 
with BuildSketch(Location((-54.5/2, -83.0/2,0))) as bread_base:
    with BuildLine() as bread_outline:
        l1 = Line(( 0.00,  0.00), ( 0.00, 83.00))
        l1 = Line(( 0.00, 83.00), (54.50, 83.00))
        l1 = Line((54.50, 83.00), (54.50,  0.00))
        l1 = Line((54.50,  0.00), ( 0.00,  0.00))
    
    make_face()

with BuildSketch() as bread_hex:
    offset(bread_base.sketch, amount= 0.50, kind=Kind.INTERSECTION)

    with HexLocations(5, 7, 10, [Align.CENTER, Align.CENTER]):
         RegularPolygon(4.5,6, mode=Mode.SUBTRACT)

with BuildSketch(Location((0,0,1.0))) as bread_over:
    offset(bread_base.sketch, amount= 0.50, kind=Kind.INTERSECTION)

with BuildSketch() as bread_frame:
    offset(bread_base.sketch, amount= 3.50, kind=Kind.INTERSECTION)
    offset(amount= -3.00, kind=Kind.INTERSECTION, mode=Mode.SUBTRACT)

with BuildPart() as bread_board:
     extrude(bread_frame.sketch, amount=7.00)
     extrude(bread_hex.sketch, amount=1.00)
     extrude(bread_over.sketch, amount=0.50)

     box_locations = tuple(Location(loc) for loc in ((4.70, 0.0,1.50),(27.10, 0.0,1.50),(49.70, 0.0,1.50)))
     for loc in box_locations:
         loc.position -= (54.5/2.0, 83.0/2.0)

     with Locations(*box_locations):
         Box(4.30,1.60,10.00,align=(Align.CENTER, Align.MAX, Align.MIN), mode=Mode.SUBTRACT)

     box_locations = tuple(Location(loc) for loc in ((0.0,14.00,1.50),(0.0, 68.60,1.50)))
     for loc in box_locations:
         loc.position -= (54.5/2.0, 83.0/2.0)

     with Locations(*box_locations):
         Box(1.60,4.30,10.00,align=(Align.MAX, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

box_assembly = Compound(label="assembly", children=[Location((0, -((25.4*2.70)/2.0)-3.5, 0))*arduino_uno_board.part,
                                                    Location((0,  (83/2.00)+3.5,0))*bread_board.part])

show(box_assembly,axes=True, axes0=True, grid=(True, True, True), transparent=True)

box_assembly.export_stl("box_assembly.stl")
# %%
