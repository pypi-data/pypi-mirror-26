# ---------------------------------------------------
# timeline elements in SVG
# ---------------------------------------------------
class Root:
    def __init__(self, theme, body, maxLengthPx, maxHeightPx, scale):
        self.node = theme.root % (maxLengthPx * scale, maxHeightPx * scale, maxLengthPx, maxHeightPx, body)
        self.theme = theme
        
class Axis:
    def __init__(self, theme, startXOffset, endXOffset):
        self.endXOffset = endXOffset
        self.startXOffset = startXOffset
        self.theme = theme

    def getShape(self):
        y = 0
        t = self.theme.Arrow(-25, y, self.startXOffset, self.endXOffset)
        return t.node
    
    def getHeight(self):
        return 20


class Marble:
    def __init__(self, theme, xOffset, y, text, coloring):
        self.theme = theme
        self.xOffset = xOffset
        self.color = coloring.getColorFor(text)
        self.text = text
        self.y = y

    def getShape(self):
        c = self.theme.Circle(self.xOffset, self.y, self.text, self.color)
        return c.node
    
    def getHeight(self):
        return 50

class Struct:
    def __init__(self, theme, xOffset, text, coloring, width, subitems, stepWidth):
        self.theme = theme
        self.xOffset = xOffset
        self.color = coloring.getColorFor(text)
        self.text = text
        self.width = width
        self.subitems = subitems
        self.stepWidth = stepWidth
        self.coloring = coloring
        self.height = self.stepWidth * len(self.subitems)
        self.shape = self.createShape()

    def createShape(self):
        y = 0
        c = self.theme.BlockWithText(self.xOffset, y, self.text, self.color, self.stepWidth, self.height)
        xOffset = self.xOffset
        yOffset = 3
        svg = ""
        for m in self.subitems:
            m = Marble(self.theme, xOffset, yOffset, m, self.coloring)
            svg += m.getShape()
            yOffset += self.stepWidth
        return c.node + svg
    
    def getShape(self):
        return self.shape
    
    def getHeight(self):
        return self.height

class Terminate:
    def __init__(self, theme, xOffset):
        self.theme = theme
        self.xOffset = xOffset

    def getShape(self):
        y = 0
        e = self.theme.End(self.xOffset, y)
        return e.node
    
    def getHeight(self):
        return 50

class Error:
    def __init__(self, theme, xOffset):
        self.theme = theme
        self.xOffset = xOffset

    def getShape(self):
        y = 0
        e = self.theme.Err(self.xOffset, y)
        return e.node

    def getHeight(self):
        return 50

class OperatorBox:
    def __init__(self, theme, maxLengthPx, height, text):
        self.theme = theme
        self.maxLengthPx = maxLengthPx
        self.height = height
        self.text = text

    def getShape(self):
        margin = 2
        y = 0
        box = self.theme.Block(0 + margin, y, self.maxLengthPx - 2 * margin, self.height, self.text, "white");
#         return self.theme.block % (0+margin,y,self.maxLengthPx-2*margin,self.height, self.maxLengthPx/2.0, y+self.height/2+5, self.text)
        return box.node

    def getHeight(self):
        return 70
