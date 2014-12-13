/*
 * Makerbeam Foam Cutter
 * It requires: http://www.thingiverse.com/thing:590893
 *
 *  Created on: Dec 13, 2014
 *      Author: jotape
 */

include <simplified_parametric_makerbeam.scad>;

show_foam = 0;
show_nichrome_wire = 1;

module nichrome_wire (length, x, y, z) {
	color ("black") translate(v=[x, y, z]) cube (size=[1, 1, length]);
}

makerbeam_x(200, 10, 0, 0, 0);
makerbeam_x(200, 10, 0, 160, 0);
makerbeam_x(200, 10, 10, 125, 60);

makerbeam_y(150, 10, 0, 10, 0);
makerbeam_y(150, 10, 0, 10, 10);
makerbeam_y(150, 10, 150, 10, 0);
makerbeam_y(150, 10, 30, 10, 0);
makerbeam_y(150, 10, 0, 10, 60);

makerbeam_z(60, 10, 0, 0, 10);
makerbeam_z(60, 10, 0, 160, 10);

if (show_foam) {
    color ("orange") {
        translate(v=[10, -(22+125)+($t*100), 10]) cube (size=[210, 297, 30]);
    }
    
    color ("red") {
        translate(v=[10, 125-125+($t*100), 10]) cube (size=[150, 150, 31]);
    }
}

if (show_nichrome_wire) {
    nichrome_wire (60, 160, 125-1, 5);
}
