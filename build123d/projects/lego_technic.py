from build123d import *
from ocp_vscode import *

import copy

# Technic, Liftarm 5 x 7 Open Center Thick
# 
#     Height = 7.86mm
#     Width = 39.80mm
#     Length = 55.85mm
#     Opening width = 24.08mm
#     Opening length = 40.20mm
# 
# Technic, Liftarm 1 x 9 Thick (oriented as shown on Bricklink image):
# 
#     Height = 7.86mm
#     Width = 7.44mm
#     Length = 71.36mm


class Technic:
    # Class variables got here

    lego_xy_grid = 8
    pin_hole_radius = 4.8/2
    pin_flange_radius = 6.2/2
    pin_flange_depth = 0.9
    beam_width = 7.8
    beam_width_grid_z_minus = (lego_xy_grid - beam_width) / 2 
    beam_height = 7.4 + 0.4
    beam_radius = beam_height/2
    align_top =     (Align.CENTER, Align.CENTER, Align.MIN)
    align_center =  (Align.CENTER, Align.CENTER, Align.CENTER)
    align_bottom =  (Align.CENTER, Align.CENTER, Align.MAX)
    
    beam_box = Box(lego_xy_grid, beam_height, beam_width,align=(Align.MIN, Align.CENTER, Align.MIN))

    def __init__(self):
        pass

    def PinHole(self, s=(1.0,1.0,1.0)):
        p  = Pos(0,0,-Technic.beam_width_grid_z_minus) * Cylinder(Technic.pin_hole_radius, Technic.lego_xy_grid, align=(Align.CENTER, Align.CENTER, Align.MIN))
        p += Pos(0,0,0)                                * Cylinder(Technic.pin_flange_radius, Technic.pin_flange_depth, align=(Align.CENTER, Align.CENTER, Align.MIN))
        p += Pos(0,0, Technic.beam_width            )  * Cylinder(Technic.pin_flange_radius, Technic.pin_flange_depth, align=(Align.CENTER, Align.CENTER, Align.MAX))
        return scale(p, s)
    
    def Beam(self,l=1, s=(1.0,1.0,1.0)):
        b  = Pos(0,                      0, 0) * Cylinder(Technic.beam_radius, Technic.beam_width, align=(Align.CENTER, Align.CENTER, Align.MIN))
        
        if l>1:
            b += Pos((l-1)*Technic.lego_xy_grid, 0, 0) * Cylinder(Technic.beam_radius, Technic.beam_width, align=(Align.CENTER, Align.CENTER, Align.MIN))
            b +=                                         scale(Technic.beam_box,((l-1),1,1))
        
        return scale(b, s)
                    
t = Technic()

p = t.PinHole()

beam_length = 20

locs = GridLocations(Technic.lego_xy_grid, Technic.lego_xy_grid, beam_length, 1).local_locations

# c = [Pos(((beam_length-1)*Technic.lego_xy_grid)/2,0,0) * copy.copy(p).locate(loc) for loc in locs]
# holes = Pos(((beam_length-1)*Technic.lego_xy_grid)/2,0,0) * Compound(children=c)
# holes = Compound(children=c)

# part = t.Beam(beam_length) - holes
part = t.Beam(beam_length)

for i in range(beam_length):
    part -= Pos(i * Technic.lego_xy_grid, 0, 0) * scale(p,(1+(.02*i), 1+(.02*i), 1))   

# holes = c

# part = holes

# show(Pos(0,-2.5,0) * reference_assembly, axes=True, axes0=True, grid=(True, True, True), transparent=True)
# show(Pos(-2.1/2, -2.7/2,0) * board, axes=True, axes0=True, grid=(True, True, True), transparent=True)
show(Pos(0,0,0) * part, axes=True, axes0=True, grid=(True, True, True), transparent=True)
export_stl(part,"technic_beam_5_scale.stl")