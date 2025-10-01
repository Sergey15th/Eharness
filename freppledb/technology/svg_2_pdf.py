import os
import reportlab
reportlab.rl_config.renderPMBackend = 'rlPIL' # pyright: ignore[reportAttributeAccessIssue]
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
drawing = svg2rlg('РМ1.svg')
renderPDF.drawToFile(drawing, 'РМ1.pdf')