from build123d import *
from ocp_vscode import *

import copy

def in_to_mm(li):
    return tuple([25.4 * i for i in li])

boss_locations_scaled = (in_to_mm([0.10, 0.60, 0.00]),
                         in_to_mm([0.70, 2.60, 0.00]),
                         in_to_mm([1.80, 2.60, 0.00]),
                         in_to_mm([2.00, 0.55, 0.00]))

boss_locations = ([Pos(0.10, 0.60, 0.00),Rot(0, 0,  90,)],
                  [Pos(0.70, 2.60, 0.00),Rot(0, 0,   0,)],
                  [Pos(1.80, 2.60, 0.00),Rot(0, 0,   0,)],
                  [Pos(2.00, 0.55, 0.00),Rot(0, 0, 270,)],)

class Boss():
    def __init__(self):
        pass

    def boss(self, diameter, height, hole=None, depth=None, box=None):
        b = Cylinder(diameter/2, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
        
        if box:
            b += Box(box[0], box[1], box[2], align=(Align.CENTER, Align.MIN, Align.MIN))
        if hole:
            b -= Pos(0,0,height) * Cylinder(hole/2, depth, align=(Align.CENTER, Align.CENTER, Align.MAX))

        return b

# print(boss_locations_scaled)
# print(boss_locations)

# boss_base = Rectangle(4,4) \
#          + Pos(2,0,0) * Circle(radius=2)

# boss = extrude(boss_base, 5) - Pos(2,0,4) * Cylinder(1,6)

# board_outline = make_face(Polyline(*board_corners))
# with BuildSketch(Location(in_to_mm([-2.10/2, -2.70/2]))) as boss_base:
#     with Locations(*cube_locations):
#         Rectangle(4,4, mode=Mode.ADD)
# 
#     with Locations(*boss_locations):
#         Circle(radius=4.00, mode=Mode.ADD)
# 
# with BuildSketch(Location(in_to_mm([-2.10/2, -2.70/2]))) as bosses:
#     with Locations(*cube_locations):
#         Rectangle(5,5, mode=Mode.ADD)
# 
#     with Locations(*boss_locations):
#         Circle(radius=2.50, mode=Mode.ADD)

# cube_locations = (in_to_mm([0.10-(2/25.4), 0.60         ]),
#                   in_to_mm([0.70         , 2.60+(2/25.4)]),
#                   in_to_mm([1.80         , 2.60+(2/25.4)]),
#                   in_to_mm([2.00+(2/25.4), 0.55         ]))

board_corners = [
        (0.00, 0.00, 0.00),
        (0.00, 2.60, 0.00),
        (0.51, 2.60, 0.00),
        (0.61, 2.70, 0.00),
        (1.90, 2.70, 0.00),
        (2.00, 2.60, 0.00),
        (2.10, 2.60, 0.00),
        (2.10, 0.00, 0.00),
        (0.00, 0.00, 0.00),
]

board_outline = make_face(Polyline(*board_corners),Align)
board = extrude(board_outline, .0625)
bb = board.bounding_box().max
board.label = "board"
board.color = Color(0,1,0)

scale_outline = ((2.40 / bb.X),  
                 (3.00 / bb.Y),
                 (0.25 / bb.Z))
outline = scale(board, scale_outline)
bo = outline.bounding_box().max
outline.label = "outline"

scale_inside  = ((2.20  / bb.X),  
                 (2.80  / bb.Y),
                 (0.125 / bb.Z))
inside = scale(copy.copy(board), scale_inside)
bi = inside.bounding_box().max
inside.label = "inside"

# b = Box(1, 2, 3)
# c = Cylinder(0.2, 5)

# locs = HexLocations(5, 7, 7).local_locations

# foo = [copy.copy(b+c).locate(loc) for loc in locs]
# reference_assembly = Compound(children=foo)

# b = Boss()
#

# part = Solid()

# for pos in boss_locations:
#    part += pos[0] * pos[1] * b.boss(0.25,0.20,0.1,0.125,(0.25,0.20,0.20))

# part += Pos(0,0,.25) * board

# part = outline - inside

board = Pos(-bb.X/2, -bb.Y/2, 0) * board
outline = Pos(-bo.X/2, -bo.Y/2, 0) * outline
inside = Pos(-bi.X/2, -bi.Y/2, 0) * inside

assembly = Compound(label="assembly", children=[outline-inside, board])

print(assembly.show_topology())
# board = Pos(0,0,1) * board

# show(Pos(0,-2.5,0) * reference_assembly, axes=True, axes0=True, grid=(True, True, True), transparent=True)
# show(Pos(-2.1/2, -2.7/2,0) * board, axes=True, axes0=True, grid=(True, True, True), transparent=True)
# show(Rot(0,0,0) * Pos(0,0,0) * b.boss(6,4,2,3,(6,3,4)), axes=True, axes0=True, grid=(True, True, True), transparent=True)
show(assembly, axes=True, axes0=True, grid=(True, True, True), transparent=True)
