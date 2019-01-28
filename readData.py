import json
import csv
from pprint import pprint
#When I get the errror: 
#UnicodeEncodeError: 'charmap' codec can't encode characters in position 52-54: character maps to <undefined>
# use the command "chcp 65001"
with open('return.txt') as f:
    data = json.load(f)
    print(len(data))

with open('dataFile.csv', 'w', newline='', encoding='utf-8') as file:
    thewriter = csv.writer(file)
    thewriter.writerow(['ID','Screen_name','Tweet', 'Age', 'Gender'])
    for d in data:
        if (len(d['faceFeature']) > 0):
            thewriter.writerow([d['id'],d['screen_name'],d['twitterData'],d['faceFeature'][0]['attributes']['age']['value'],d['faceFeature'][0]['attributes']['gender']['value']])


