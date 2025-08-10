# Lithopane 3mf Generator

This python scripts will read an image and covert it into a 3mf file, which can be used to 3D print a lithopane.


## Setup

This script was written using Python 3.11.2. Earlier version should work, however you will likely need to install a different version of PIL in that case.

If you are using Python 3.11.2+, then install dependencies using: `py -m pip install -r requirements.txt`

Otherwise, install using `py -m pip install pillow`



## Usage

Once installed, script can be run using `py generate.py {path to image}`.

You can specify in mm how large the longest side of the image should be by using the `-d` flag. Example: `py generate.py test.png -d 200` to generate a lithopane where the longest side is 200mm. Otherwise, defaults to 50mm.



## Printing

Please ensure that sparse infill is set to `100%`