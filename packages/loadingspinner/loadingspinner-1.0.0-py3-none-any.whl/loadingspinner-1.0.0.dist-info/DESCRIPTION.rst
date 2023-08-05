loading-spinner

An incredibly simple "loading spinner" for python projects

Usage:

NOTE: Please do NOT import spinner. You MUST use loadingspinner.

import loadingspinner
loadingspinner.setText("Loading...")
loadingspinner.start()
<lines of code>
loadingspinner.stop()

Customizing the spinner:

Changing the spinner animation:
	loadingspinner.setFrames(<list of characters to display in order from left to right>)
	Ex. loadingspinner.setFrames(["|","/","-","\\"])
Changing the text color (requires Colorama to be installed):
	loadingspinner.setTextColor(color)
Changing the spinner color (Incomplete. Also requires Colorama):
	loadingspinner.setSpinnerColor(color)

