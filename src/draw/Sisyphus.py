from math import sin, cos, radians, sqrt
from Sand import *
from dialog import *
from Chains import *
import logging

class Sander( Sandable ):
    """
### Draw Sisyphus tracks

#### Hints

Download tracks from [Dropbox](https://www.dropbox.com/sh/n2l29huvdrjalyx/AAA69jTy1aDobkR_wKog1Ewka?dl=0)

#### Parameters

* **File Name** - name of the file to be drawn.  Files use a rudimentary file browser that supports
  directories.  Search through the directories to find interesting things to draw.
"""

    def __init__( self, width, length ):
        self.multiplier = min(width, length) / 2.
        self.xc, self.yc = width / 2, length / 2
        self.fullRadius = sqrt(max(width,length)**2)
        
        self.backgrounds = ['None','Spiral',"Full Spiral"]

        self.editor = [
            DialogFile(  "filename",            "File Name",                default = CLIPART_PATH, filter = '.thr'),
            DialogFloat( "rotation",            "Rotation",                 units = 'Degrees', default = 0, min = -360., max = 360.),
            DialogList(  "background",          "Background",               default = 'None', list = self.backgrounds),
        ]

    def generate( self, params ):
        chain = []
        background = []
        filename = params.filename
        multiplier = self.multiplier
        xc, yc = self.xc, self.yc
        aplus = radians(params.rotation)
        if filename.endswith( '.thr'):
            with open(filename, 'r') as f:
                while True:
                    line = f.readline().strip()
                    if len(line) == 0:
                        break
                    if line.startswith('#'):
                        continue
                    parts = line.split(' ')
                    angle, radius = float(parts[0])+aplus, float(parts[1])
                    x, y = xc + sin(angle) * radius * multiplier, yc + cos(angle) * radius * multiplier
                    chain += [ (x, y) ]

            if params.background == 'Spiral':
                background = Chains.spiral(xc,yc,self.multiplier,linesPerInch=2.,angleRate=7.,radiusEnd=0.)
            elif params.background == 'Full Spiral':
                background = Chains.spiral(xc,yc,self.fullRadius,linesPerInch=2.,angleRate=7.,radiusEnd=0.)

        return [ background, chain ]

