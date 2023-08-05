


CONFIG_TEXT = """
# For help and detailed explanations of parameters see:
# https://github.com/jasonhamilton/hotwing-cli/blob/master/config-options.md

[Project]
Units = inches

[RootChord]
Profile = http://m-selig.ae.illinois.edu/ads/coord/ag04.dat
Width = 10
LeadingEdgeOffset = 0
Rotation = 0
RotationPosition = 0.5

[TipChord]
Profile = http://m-selig.ae.illinois.edu/ads/coord/ag09.dat
Width = 8
LeadingEdgeOffset = 2
Rotation = 0
RotationPosition = 0.5

[Panel]
Width = 24
StockLeadingEdge = 0
StockTrailingEdge = 0
SheetingTop = 0.0625
SheetingBottom = 0.0625

[Machine]
Width = 30
FoamHeight = 2
SafeHeight = 4
Feedrate = 5
Kerf = 0.075
"""

def generate_config(filename):
	with open(filename,"w") as f:
		f.write(CONFIG_TEXT)