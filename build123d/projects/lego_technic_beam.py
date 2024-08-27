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
# Algebra mode

technic_holes = 7

technic_x = 8
technic_y = 7.4
technic_z = 7.9

technic_hole_diameter = 4.8 + 0.2
technic_flange_diameter = 6.2 + 0.1
technic_flange_depth = 1

technic_beam_face = SlotCenterToCenter(technic_x * (technic_holes-1), technic_z)

pin_locations = GridLocations(technic_x, technic_y, technic_holes, 1)

flange_references = [Circle((technic_flange_diameter+0/20)/2).locate(loc) for i, loc in enumerate(pin_locations)]
pin_flanges = Compound(children=flange_references)

hole_references = [Circle((technic_hole_diameter+0/20)/2).locate(loc) for i, loc in enumerate(pin_locations)]
pin_holes = Compound(children=hole_references)

#hole_references = [copy.copy(technic_hole).locate(loc) for loc in pin_locations]
#pin_holes = Compound(children=hole_references)

#lc = Pos(0,lego_grid/4,lego_grid/2)  * Rot(0,0,180)     * Cylinder(lego_grid/2, lego_grid, 180)
#rc = Pos(0,(lego_grid*holes)-lego_grid/4,lego_grid/2)   * Rot(0,0,0  ) * Cylinder(lego_grid/2, lego_grid, 180)
#b =  Pos(0,lego_grid*(holes-1)-lego_grid/2,lego_grid/2) * Box(lego_grid, lego_grid*(holes-1), lego_grid) 

#pin = Cylinder(technic_hole/2, lego_grid).scale(0.5)

#pins = Pos(0,lego_grid/2,lego_grid/2) *  pin

#for i in range(1, holes):
#    pins += Pos(0,lego_grid/2+i*lego_grid,lego_grid/2) * pin

#
#r = b - c
# lc + rc + b -
#r =  lc + rc + b - pins

beam_face = technic_beam_face
for flange in pin_flanges.children:
    beam_face -= flange
beam_face = extrude(beam_face,technic_flange_depth,[0,0,1])
beam_face = mirror(beam_face, Plane.XY.move(Pos(0,0,technic_z/2))) + beam_face

beam_body = technic_beam_face 
for hole in pin_holes.children:
    beam_body -= hole
beam_body = extrude(beam_body,technic_z - 2*technic_flange_depth,[0,0,1])
beam_body = Pos(0, 0, technic_flange_depth) * beam_body

beam = beam_face + beam_body

beam.export_stl("calibration_beam.stl")

show(beam, axes=True, axes0=True, grid=(True, True, True), transparent=True)

# %%

