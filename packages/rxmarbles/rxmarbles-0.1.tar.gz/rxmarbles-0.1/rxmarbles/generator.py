from __future__ import print_function
from pyparsing import *
from .svgshapes import *
import sys
import argparse
import math
import importlib

start = Suppress("+")
tickCharacter = '-'
terminateCharacter = "|"
errorCharacter = "#"
infinity = ">"

colon = Suppress(":")
comment_start = "//"
empty_tick = Word(tickCharacter, exact=1)
# our marble can be either single alphanumeric character, or mutiple characters surrounded by ()
marble_text = alphanums + "'\""

simpleMarble = Word(marble_text, exact=1)
brackedMarble = Suppress("(") + Word(alphanums + "'\".") + Suppress(")")
grouppedMarble = Combine("{" + Word(marble_text + ",") + "}")
marble = Or([simpleMarble, brackedMarble , grouppedMarble])
end = Or([terminateCharacter, errorCharacter, infinity]).setResultsName('end')
item = Word(alphanums)
source_name = Word(alphanums + "{}(),><=!+-'/\"").setResultsName('name')
source_keyword = "source"
operator_keyword = "operator"
tick = Or([empty_tick, marble])
ticks = Group(ZeroOrMore(tick)).setResultsName('ticks')
padding = Optional(Word('.')).setResultsName('padding')
timeline = Group(padding + start + ticks + end).setResultsName('timeline', True)
skewed_group = Suppress("{") + OneOrMore(timeline) + Suppress("}")
type = Or([source_keyword, operator_keyword]).setResultsName('type')
source_or_operator = Group(type + source_name + colon + Or([timeline, skewed_group]))

marble_diagram_keyword = "marble"
marble_diagram_body = OneOrMore(source_or_operator)
marble_diagram_name = Word(alphanums + "_").setResultsName("diagram_name")
marble_diagram = Group(Suppress(marble_diagram_keyword) + marble_diagram_name + Suppress("{") + marble_diagram_body + Suppress("}"))
marble_diagrams = OneOrMore(marble_diagram)
marble_diagrams.ignore(comment_start + restOfLine)

class Timeline:
    def __init__(self, parsedlist, theme):
        self.theme = theme
        self.type = parsedlist.type
        self.name = parsedlist.name
        self.timelines = parsedlist.timeline
        self.rotation = 0
        if len(self.timelines) > 1:
            self.rotation = 15
        maxIndex = max(map(lambda x: 2 + len(x.ticks) + len(x.padding), self.timelines))
        # this is used as distance on flat axis between two time ticks
        self.baseThickWidth = 50.0
        # this is used as distance on skewed between two time ticks
        self.tickWidth = self.baseThickWidth / math.cos(self.rotation * math.pi / 180.0)
        
        self.width = self.tickWidth * maxIndex
        self.topMargin = 30
        self.totalHeight = 0
        
    def createGrouppedSymbol(self, o, xOffset, coloring):
        # Sub-parsing groupped marble
        ungrouppedMarble = Suppress("{") + Word(marble_text) + ZeroOrMore(Suppress(",") + Word(marble_text)) + Suppress("}")
        subitems = ungrouppedMarble.parseString(o)
        stepWidth = 1.0 * self.baseThickWidth
        body = ", ".join(map(lambda x: str(x), subitems))
        width = stepWidth * len(subitems)
        grouppedSymbol = Struct(self.theme, xOffset, body, coloring, width, subitems, stepWidth)
        return grouppedSymbol
        
    def __getTimelineShapes(self, coloring, timelineItems):
        # adding ticks
        theme = self.theme
        self.end = timelineItems.end
        xOffset = 0
        global parseString
        for o in timelineItems.ticks:
            if o.startswith('{') and o.endswith('}'):
                grouppedSymbol = self.createGrouppedSymbol(o, xOffset, coloring)
                self.symbols.append(grouppedSymbol)
            else:
                if o != tickCharacter:
                    self.symbols.append(Marble(theme, xOffset, 0, o, coloring))
            xOffset += self.tickWidth

        # adding completion, error or infinity symbol to the axis 
        if self.end == terminateCharacter:
            self.symbols.append(Terminate(theme, xOffset))
        elif self.end == errorCharacter:
            self.symbols.append(Error(theme, xOffset))

        # adding time axis
        self.symbols.insert(0, Axis(theme, 0, xOffset + 2 * self.baseThickWidth))

    def getSvg(self, y, coloring, maxLength):
        svg = ""
        yy = y + self.topMargin
        for timelineItems in self.timelines: 
            self.symbols = []
            self.__getTimelineShapes(coloring, timelineItems)
            xOffset = self.baseThickWidth * len(timelineItems.padding)
            g_id = self.type + "_" + self.name
            rotYY = yy
            svg += '<g id="%s" transform="rotate(%s %s %s) translate(%s,%s)">' % (g_id, self.rotation, xOffset, rotYY , xOffset, yy)
            for obj in self.symbols:
                svg += obj.getShape()
                h = obj.getHeight()
                if self.totalHeight < h + self.topMargin :
                    self.totalHeight = h + self.topMargin 
            svg += '</g>'
            
        # and finally - inserting an extra axis - only when we are in the skewed block mode
        if len(self.timelines) > 1:
            maxPadding = max(map(lambda x: len(x.padding), self.timelines))
            a = Axis(self.theme, 0, self.baseThickWidth * (4 + maxPadding))
            axisSvg = '<g id="skew" transform="translate(0 %s)">%s</g>' % (yy, a.getShape())
            svg = axisSvg + svg
        return svg

    def height(self):
        "returns height in pixels. This must be called after getSvg()"
        
        # let's calculate all bounding boxes
        maxHeight = 0
        for timeline in self.timelines:
            timelineWidth = self.baseThickWidth * (1 + len(timeline.ticks))
            timelineHeight = self.totalHeight
            bb = (timelineWidth, timelineHeight)
            # width of the diagonal
            diag = math.sqrt(bb[0] * bb[0] + bb[1] * bb[1])
            alphaRad = math.atan2(bb[1], bb[0])
            alphaDeg = alphaRad * 180.0 / math.pi
            # after rotation
            betaDeg = alphaDeg + self.rotation
            betaRad = betaDeg * math.pi / 180.0 
            height = diag * math.sin(betaRad)
            if maxHeight < height:
                maxHeight = height 
        return maxHeight

class Source(Timeline):
    def __init__(self, parsedList, theme):
        Timeline.__init__(self, parsedList, theme)

class Operator:
    def __init__(self, parsedList, theme):
        self.theme = theme
        self.timeline = Timeline(parsedList, theme)
        self.name = parsedList.name
        self.width = self.timeline.width
        self.boxHeight = 80
        self.topMargin = 10

    def height(self):
        "height in pixels"
        return self.boxHeight + self.timeline.height() + 2 * self.topMargin

    def getSvg(self, y, coloring, maxLength):
        theme = self.theme
        boxY = y + self.topMargin
        box = OperatorBox(theme, maxLength, self.boxHeight, self.name)
        svg = '<g transform="translate(0 %s)">' % boxY
        svg += box.getShape() + self.timeline.getSvg(0 + self.boxHeight + self.topMargin, coloring, maxLength)
        svg += '</g>'
        return svg

# ---------------------------------------------------
# timeline elements
# ---------------------------------------------------

def getObjects(parseResult, theme):
    global source_keyword
    global operator_keyword
    result = []
    for line in parseResult:
        type = line[0]
        if type == operator_keyword:
            t = Operator(line, theme)
        if type == source_keyword:
            t = Source(line, theme)
        result.append(t)
    return result

default = ["#ffcc00", "#48b3cd", "#ffaacc", "#e5ff7c", "#ececec", "#a4ecff", "#ff6600", "#a0c800", "#ff3a3a", "#afafe9", "#db7c7c", "#80ffe6"]

palettes = {'default':default}

class Coloring:
    'This object is stateful color provider for each of the marble'
    
    def __init__(self, paletteName='default'):
        global palettes
        self.colorPalette = palettes[paletteName]
        self.colormap = {}
        self.index = 0

    def getColorFor(self, marbleId):
        if not marbleId in self.colormap:
            self.colormap[marbleId] = self.colorPalette[self.index]
            self.index += 1
            if self.index >= len(self.colorPalette):
                self.index = 0
        return self.colormap[marbleId]

class SvgDocument:
    def __init__(self, rowObjects, theme, scale):
        self.theme = theme
        self.scale = scale
        self.coloring = Coloring()
        self.rowObjects = rowObjects
        # in pixels
        self.maxRowWidth = max(map(lambda row: row.width, self.rowObjects))

    def getDocument(self):
        theme = self.theme
        scale = self.scale
        body = ""
        y = 0
        for row in self.rowObjects:
            body += row.getSvg(y, self.coloring, self.maxRowWidth)
            y = y + row.height()

        r = Root(theme, body, self.maxRowWidth, y, scale / 100.0)
        return r.node
    
