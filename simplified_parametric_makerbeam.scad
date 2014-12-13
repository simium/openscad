/*
 * Simplified version of Makerbeam
 * parametric by Meir Michanie (https://www.thingiverse.com/meirm)
 *
 *  Created on: Dec 13, 2014
 *      Author: jotape
 */

file_dxf="MakerBeam.dxf";

demo = 0;
enable_colors = 1;

if (demo) {
    demo();
}

module tslot(model="tslot2", h=10, w=10) {
    scale([0.1*w,0.1*w,1])
       linear_extrude(height=h)import( file=file_dxf, layer=model, $fn=60);
}

module makerbeam_x(h=10, w=10, x=0, y=0, z=0) {
    if (enable_colors) color("red")
    translate([x, y, w+z]) rotate(a=[0, 90, 0]) tslot(h=h, w=w);
}

module makerbeam_y(h=10, w=10, x=0, y=0, z=0){
    if (enable_colors) color("green")
    translate([x, y, w+z]) rotate(a=[-90, 0, 0]) tslot(h=h, w=w);
}

module makerbeam_z(h=10, w=10, x=0, y=0, z=0){
    if (enable_colors) color("blue")
    translate ([x, y, z]) tslot(h=h, w=w);
}


module demo() {
    makerbeam_x(100, 10, 10, 0, 0);
    makerbeam_x(100, 10, 10, 110, 0);
    makerbeam_x(100, 10, 10, 110, 90);
    makerbeam_x(100, 10, 10, 0, 90);

    makerbeam_y(100, 10, 110, 10, 0);
    makerbeam_y(100, 10, 110, 10, 90);
    makerbeam_y(100, 10, 0, 10, 0);
    makerbeam_y(100, 10, 0, 10, 90);

    makerbeam_z(100, 10, 0, 0, 0);
    makerbeam_z(100, 10, 0, 110, 0);
    makerbeam_z(100, 10, 110, 110, 0);
    makerbeam_z(100, 10, 110, 0, 0);
}