Scripts to perform OCR and to detect lines in cards
Right now, main does nothing. 
My intention is to turn main into a comprehensive OCR script which will use different methods on different card types.
Both "OCR" and "layoutDetection" are set up as modules. Their functions should be imported into other scripts for use.

"OCR" directory contains functions for general preprocessing as well as OCR.
"layoutDetection" contains functions designed to detect lines on type 2 cards(cards like 310-0000).