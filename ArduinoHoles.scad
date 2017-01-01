//---------------------------------------------------------------
//-- Openscad Arduino Holes module
//-- (C) Juan Pedro López (jotape)
//-- May-2013
//---------------------------------------------------------------
//-- Released under the GPL license
//---------------------------------------------------------------

//------------------------------------------------------------------
//-- Draw the Arduino holes so you can mount your
//-- Arduino board anywhere.
//--
//-- Parameters:
//--  board: name of the board you want to draw.
//--  height: height of the drawn cylinders.
//------------------------------------------------------------------

module arduinoHoles(board="UNO", height = 5) {
	if (board=="UNO") {
		// Draw the holes
		translate(v = [15, 50.5, 0]) {
			cylinder(h = height, r = 1.6, center = true, $fn=36);
		}

		translate(v = [65.5, 7, 0]) {
			cylinder(h = height, r = 1.6, center = true, $fn=36);
		}

		translate(v = [65.5, 35, 0]) {
			cylinder(h = height, r = 1.6, center = true, $fn=36);
		}
	}
	else {
		echo("Board ", board, " is not supported yet.");
	}
}
