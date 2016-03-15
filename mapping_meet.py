# CSE 160
# Sidney Sullivan & Naomi Provost
# Final Project cont.

import csv
from bs4 import BeautifulSoup

#used the website: http://flowingdata.com/2009/11/12/how-to-make-a-us-county-thematic-map-using-free-tools/

information = "May_2013_Online_Dating_CSV.csv"
csv_file = csv.DictReader(open(information, 'rb'), delimiter=',', quotechar='"')

fips_dict = {}
fips_lst = []

# Loop through the csv_file lines and append to the list. This looks at if the
# responder thinks it's easy or difficult to meet people in their area.
for line in csv_file:
    fips_lst.append([line['fips'], line['meet']])
    
# Loop through fips_lst and create dict with fips as keys.
for row in fips_lst:
    try:
        fips = row[0]
        response = int(row[1])
        fips_dict[fips] = response
    except:
        pass

# Load the SVG map
svg = open('USA_Counties.svg', 'r').read()

# Load into Beautiful Soup
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])

# Find counties
paths = soup.findAll('path')

# Map colors
colors = ["#0000FF", "#FF6347", "#ADD8E6"]

# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1; stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt; marker-start:none;stroke-linejoin:bevel;fill:'
# Color the counties based on answer to question
for p in paths:
     
    if p['id'] not in ["State_Lines", "separator"]:
        # pass
        try:
            response = fips_dict[p['id']]
        except:
            continue
             
        if response == 1:
            color_class = 0
        elif response == 2:
            color_class = 1
        else:
            color_class = 2
 
        color = colors[color_class]
        p['style'] = path_style + color

# Output map
print soup.prettify()
