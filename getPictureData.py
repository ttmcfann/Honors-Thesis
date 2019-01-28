import sys, json 
import requests
from PIL import Image 
import os,time 
import os.path
file = open("test.json", "r")
listOfJsonObjects = []
location = 'C:/Users/Thomas McFann/Honors Thesis/Code/pictures'
loc = 'pictures'

#This function verifies that an image is valid for 
#the API 
def verify_image(img_file):
     #test image
     try:
        v_image = Image.open(img_file)
        v_image.verify()
        return True
        #is valid
        #print("valid file: "+img_file)
     except OSError:
        return False
#This line removes the space between each JSON object returned 
#from the API, so that an error will not be thrown        
for line in file:
    if line != "\n":
        listOfJsonObjects.append(line)

#This is a list that holds each Json object which 
#contains a tweet and the face++ api info
listOfAgeGenderTweet = []

#loop through every tweet returned from the API
# 
counter = 0  
for objects in listOfJsonObjects:
    struct = {} 
    try:
        #attempt to strip symbols from the JSON object 
        dataform = str(objects).strip("'<>() ")
        struct = json.loads(dataform, strict = False)
        print(struct)
        #This is the key of the Tweet API that holds 
        #the contents of the tweet 
        tweet = struct['text']
    
        id = struct['id']

        screen_name = struct['user']['screen_name']
        # capture picture url
        oldUrl = struct['user']['profile_image_url']
        #This line tells me whether a photo is jpg or png
        fileType = oldUrl[-3:]
        #makes each picture viewable in the browser 
        url = oldUrl.replace('_normal', '_400x400')
        # changes the name of the file based upon its picture type  
        if fileType == "jpg":
            nameOfFile = struct['user']['screen_name'] + '.jpg'
        if fileType == "png":
            nameOfFile = struct['user']['screen_name'] + '.png'


    
        # save file and store it in a file and make the username the filename
        #The result of this code stores the pictures in a folder that will be passed
        #to the API 
        completePath = os.path.join(location, nameOfFile)
        r = requests.get(url, allow_redirects=True)


    

        open(completePath, 'wb').write(r.content)
        #This code contains the parameters which will be passed to the 
        #Face ++ API 
        params = {

            'api_key': (None, 'aluEDiRbnvetp7TxiHjpD7uiwXU3iEfw'),

            'api_secret': (None, 'oAr7VWrwA7N0nJZ_F5aw8EubPH0tPtoY'),

            'image_file': (loc+ '/' + nameOfFile, open(loc+ '/' + nameOfFile, 'rb')),

            'return_landmark': (None, '0'),

            'return_attributes': (None, 'gender,age'),

        }
        response = requests.post('https://api-us.faceplusplus.com/facepp/v3/detect', files=params)
        # get the response json object d
        data = response.json()
        if ("faces" in data):
            print("in the if loop")
            face = data['faces']
            # print(face)
            print("made it past face")

            ##### I should rework this code to make the JSON code more workable
            # age = data["faces"][0][1]
            # print(age)
            # gender = data['faces']['gender']
            # print(gender)
            #####
            ageGenderTweet = {}
            print("created Json object")
            ageGenderTweet['twitterData'] = tweet
            ageGenderTweet['id'] = id
            ageGenderTweet['screen_name'] = screen_name
            ageGenderTweet['faceFeature']= face
            # ageGender.append(gender)
            # ageGender.append(age)
            #print(ageGender)

            print("opening file")  
            counter = counter + 1
            print(counter)
            listOfAgeGenderTweet.append(ageGenderTweet)
              
        else: 
            #error = data["error_message"]

            print("This picture is not good")
        # with open('data.txt', 'w') as outfile:
        #     json.dump(data, outfile)
        

    except: 
        #print(repr(objects))
        #print(sys.exc_info())
        print("error")
with open('return.txt', 'w') as outfile:
    json.dump(listOfAgeGenderTweet, outfile)
    print("dumped contents") 


    
    # struct = json.loads(dataform, strict = False)
    #     # capture picture
    #     oldUrl = struct['user']['profile_image_url']


    #jsonObjs = line.split()
    #print(jsonObjs[0])
    #for jsonObj in jsonObjs:
        #print json
        #tweet = jsonObj.split(',"text":"')[1].split('","source')[0]
        #picture = jsonObj.split(',"profile_image_url":"')[1].split('","profile_image_url_https')[0]
        #data = json.load(picture)
        #print(data)
    
