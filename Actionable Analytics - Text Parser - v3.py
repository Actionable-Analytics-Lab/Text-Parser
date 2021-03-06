# -*- coding: utf-8 -*-
"""
Version 3

Updated by: Hamza Amjad

Features:
    -Included usage of pandas library to create DataFrame structure for data
    -Utilize pandas library to output data to csv format
    -Removed unnecessary print statements
    -Added additional tags to cleanHTML function
        -Included Special Entities from http://www.htmlhelp.com/reference/html40/entities/special.html
        
To-Do:
    -Add additional data fields [date, ?]
    -Extend functionality of cleanHTML
    -Explicity cast data types in DataFrame
    -Add connection to Database (once Database is set up)
"""

################################################################################################
#Packages used in code
################################################################################################
import re
import os
import pandas as pd

################################################################################################
#Created functions used in code
################################################################################################
def cleanHTML(html):
    htmltaglist = [r'<p.*?>',r'</p>',r'<div.*?>',r'</div>',r'<u>',r'</u>',r'<b>',r'</b>',r'<i>','r</i>',r'<h1.*?>',r'</h1>',r'<h2.*?>',r'</h2>',r'<h3.*?>',r'</h3>',r'<h4.*?>',r'</h4>',r'<h5.*?>',r'</h5>',r'<h6.*?>',r'</h6>']
    for tag in htmltaglist:
        html = re.sub(tag, '', html)
        
    html = re.sub(r'<br.*?>',r'\n', html)
    
    
    specialEntities = {'r&quot;': r'"',r'&amp;': r'&',r'&lt;': r'<',r'&gt;': r'>',r'&OElig;': r'Œ',r'&oelig;': r'œ',r'&Scaron;': r'Š',r'&scaron;': r'š',r'&Yuml;': r'Ÿ',r'&circ;': r'ˆ',r'&tilde;': r'˜',r'&ensp;': r' ',r'&emsp;': r' ',r'&thinsp;': r' ',r'&zwnj;': r'‌',r'&zwj;': r'‍',r'&lrm;': r'‎',r'&rlm;': r'‏',r'&ndash;': r'–',r'&mdash;': r'—',r'&lsquo;': r'‘',r'&rsquo;': r'’',r'&sbquo;': r'‚',r'&ldquo;': r'“',r'&rdquo;': r'”',r'&bdquo;': r'„',r'&dagger;': r'†',r'&Dagger;': r'‡',r'&permil;': r'‰',r'&lsaquo;': r'‹',r'&rsaquo;': r'›',r'&euro;': r'€'}
    for key, value in specialEntities.items():
        html = re.sub(key,value, html)
        return html

################################################################################################
#Create an empty DataFrame which will be used to store the data pulled from files
################################################################################################
columns = ['Item', 'Listing Price', 'Vendor Name', 'Description']
structuredData = pd.DataFrame(columns=columns)



################################################################################################
#Start For Loop. Fan through every file in certain directory. Rewrite file path to folder that
#contains your html files.
################################################################################################
for path, subdirs, files in os.walk(os.getcwd()+r'\HansaMarketHTMLFiles'):
    for filename in files:
        fileName = os.path.join(path, filename)
        

################################################################################################
#Reading the data from raw HANSA file, rewrite file path as needed
################################################################################################
        with open(fileName, encoding='utf-8') as input:
            raw = input.read()
    
################################################################################################
#Removing line breaks, tabs and other white space characters, except for single spaces, from string
################################################################################################
        onlySpaces = re.sub(r'\s+', ' ', raw)

################################################################################################
#Pull desired values out of cleaned string
################################################################################################
        item = re.search(r'<h2.*?>(.*?)</h2>',onlySpaces).group(1)

        listingPrice = re.search(r'<div.*?> <strong>(.*?)</strong>',onlySpaces).group(1)
        listingPrice = float(re.sub(r'USD\s', '', listingPrice))

        vendorName = re.search(r'<td>Vendor</td> <td><a.*?>(.*?)</a>',onlySpaces).group(1)

        description = cleanHTML(re.search(r'<h3><u>Listing Details</u></h3>(.*)<footer>',onlySpaces).group(1))

################################################################################################
#Append values to dataframe
################################################################################################
        structuredData = structuredData.append({columns[0]: item, columns[1]: listingPrice, columns[2]: vendorName, columns[3]: description}, ignore_index=True) 

structuredData.to_csv(os.getcwd()+r'\Structured Data.csv', index=False)