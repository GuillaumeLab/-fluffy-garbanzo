# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:41:07 2019

@author: Hugh

A super simple program which makes an HTML document with a graph.
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
#import cv2

df = pd.read_csv("Position_Salaries.csv")
fig, ax = plt.subplots()
ax = sns.barplot(df["Position"], df["Salary"])
fig.savefig("barplot1.png")

html = """
<!DOCTYPE html>
<head>
<title>A title of joy</title>
</head>
<body>
A body of joy... Here comes the science: <br/>
    
<img src="barplot1.png" alt="salary_graph">
</body>
"""

latex = """
\\documentclass[]{article}

\\addtolength{\\oddsidemargin}{-0.75in}
\\addtolength{\\textwidth}{1.5in}
\\addtolength{\\topmargin}{-0.75in}
\\addtolength{\\textheight}{1.5in}

\\usepackage{amsfonts}
\\usepackage{amsmath}
\\usepackage{amsthm}
\\usepackage{txfonts} \\usepackage{pxfonts}
\\usepackage{graphicx}

\\title{This is a Test Heckle}
\\author{Team Elephant in the Living Room}

\\begin{document}

\\maketitle

\\begin{abstract}
We're going to do some crazy shit!
\\end{abstract}

\\section{The Science}

Look at this science!
\\includegraphics{barplot1.png}

\\end{document}
"""

f = open("test_heckle.html","w")
f.write(html)
f.close()

g = open("test_heckle.tex","w")
g.write(latex)
g.close()

#subprocess.check_call(['pdflatex', 'test_heckle.tex'])
os.system("pdflatex test_heckle.tex")