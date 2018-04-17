#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
from lxml import html
import requests
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os
import sys
#import urlparse
from urllib.parse import urljoin
import emoji

from flask import Flask
from flask import request, render_template
from flask import make_response


# Flask should start in global layout
context = Flask(__name__)
# Facbook Access Token
ACCESS_TOKEN = "EAADSsDjm6gIBANlzUbBmbFLGpNvZBhnZCEw71BSMvwQZCK8n9KjaY5Pf8P5ZAZBlt9mKcLHe2AmU5hgq7XZAc4vedP5ISpyuRIBKuWMvYx6YI6976r5qpZBsI8vSoU4pmqvVqffjNVJuvCttk7EykTb9tUfHWCnjfivwKUZAA1S4WQZDZD"

#************************************************************************************#
#                                                                                    #
#    All Webhook requests lands within the method --webhook                          #
#                                                                                    #
#************************************************************************************#
reqContext = None
# Webhook requests are coming to this method
@context.route('/webhook', methods=['POST'])
def webhook():
    global reqContext
    reqContext = request.get_json(silent=True, force=True)
    #print(json.dumps(reqContext, indent=4))
    print("webhook---->" + reqContext.get("result").get("action"))
    print ("webhook is been hit ONCE ONLY")
    if reqContext.get("result").get("action") == "input.welcome":
       return welcome()
    elif reqContext.get("result").get("action") == "asktheuser":
       return asktheuser(reqContext)
    elif reqContext.get("result").get("action") == "nationality":
       return userNationality(reqContext)
    elif reqContext.get("result").get("action") == "nationalityrecheck":
       return userNationalityRecheck()
    elif reqContext.get("result").get("action") == "startover":
       return startOver()
    elif reqContext.get("result").get("action") == "destinationcountry":
       print ("User Input-->Citizenship -->" + reqContext.get("result").get("resolvedQuery"))
       return userDestinationCountry(reqContext)
    elif reqContext.get("result").get("action") == "wikipediasearch":
       print ("User Input-->Country Name -->" + reqContext.get("result").get("resolvedQuery"))
       return wikipedia_search(reqContext)
    elif reqContext.get("result").get("action") == "nothanks":
       return noThanks()
    elif reqContext.get("result").get("action") == "morebots":
       return moreBots()
    else:
       print("Good Bye")

 
#************************************************************************************#
#                                                                                    #
#   This method is to get the Facebook User Deatails via graph.facebook.com/v2.6     #
#                                                                                    #
#************************************************************************************#
nationality = "False"
destinationcountry = "False"
def welcome():
    data = request.json
    print (data)
    if data is None:
        return {}
    #entry = data.get('originalRequest')
    platform = data.get('originalRequest').get('source')
    print ("PLATFORM -->" + platform)

    if platform == "facebook":
       id = data.get('originalRequest').get('data').get('sender').get('id')
       print ("id :" + id)
       fb_info = "https://graph.facebook.com/v2.6/" + id + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN
       print (fb_info)
       result = urllib.request.urlopen(fb_info).read()
       print (result)
       data = json.loads(result)
       first_name = data.get('first_name')
       print ("FACEBOOK: First Name -->" + first_name)
    elif platform == "telegram":
       first_name = data.get('originalRequest').get('data').get('message').get('chat').get('first_name')
       print ("TELEGRAM: First Name -->" + first_name)
    elif platform == "skype":
       first_name = "to Visa CheckBot"
       print ("SKYPE: Within Python")
    elif platform == "slack":
       first_name = "to Visa CheckBot"
       print ("SKYPE: Within Python")
       
    speech1 = "Visa CheckBot - your one stop solution for visa related enquiry. "
    res = {
          "speech": speech1,
          "displayText": speech1,
           "data" : {
             "facebook" : [
                   {
                    "sender_action": "typing_on"
                  },
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Welcome " + first_name + "! ",
                                   "image_url" : "http://kredist.ru/wp-content/uploads/2014/10/%D0%B2%D1%8B%D0%B5%D0%B7%D0%B4-%D0%B7%D0%B0-%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%83-%D1%81-%D0%B4%D0%BE%D0%BB%D0%B3%D0%B0%D0%BC%D0%B8.jpg",
                                 } 
                           ]
                       } 
                   }
                },
                 {
                    "sender_action": "typing_on"
                  },
                 {
                 "text": speech1
                  },
                 {
                  "text": "So, let's start. Shall we?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Yeah Sure",
                  "payload": "Yeah Sure",
                  "image_url": "http://gdurl.com/eNYq"
                 },
                 {
                  "content_type": "text",
                  "title": "No Thanks",
                  "payload": "No Thanks",
                  "image_url": "http://gdurl.com/uViQ"
                   }
                  ]
                 }
                ],
            "telegram": {
                 "text": "Welcome in Telegram -->" + first_name + "! " + speech1 + "So let's start, shall we?",
                 "photo": "http://kredist.ru/wp-content/uploads/2014/10/%D0%B2%D1%8B%D0%B5%D0%B7%D0%B4-%D0%B7%D0%B0-%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%83-%D1%81-%D0%B4%D0%BE%D0%BB%D0%B3%D0%B0%D0%BC%D0%B8.jpg",
                 "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "callback_data": "Yeah Sure", "text": "Yeah Sure" }], 
                        [{ "callback_data": "No Thanks", "text": "No Thanks" }] 
                       ] 
                },
               },
            "slack": {
                 "text": speech1,
                 "attachments": [
                   {
                     "text": "So, let's start. Shall we?",
                    "fallback": "You are unable to proceed",
                    "callback_id": "intro_block",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                         {
                            "name": "response",
                            "text": "Yeah Sure",
                            "type": "button",
                            "value": "Yeah Sure"
                         },
                         {
                            "name": "response",
                            "text": "No Thanks",
                            "type": "button",
                            "value": "No Thanks"
                         }
                     ]
                  }
                ]
              }
            },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": "",
              "attachments": [
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "title": "Welcome to Visa CheckBot",
                    "subtitle": "Your one stop solution for Visa check",
                    "images": [
                      {
                        "url": "http://kredist.ru/wp-content/uploads/2014/10/%D0%B2%D1%8B%D0%B5%D0%B7%D0%B4-%D0%B7%D0%B0-%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%83-%D1%81-%D0%B4%D0%BE%D0%BB%D0%B3%D0%B0%D0%BC%D0%B8.jpg"
                      }
                    ],
                    "buttons": [
                      {
                        "type": "imBack",
                        "title": "Yeah Sure",
                        "postback": "Yeah Sure"
                      },
                      {
                        "type": "imBack",
                        "title": "No Thanks",
                        "postback": "No Thanks"
                      }
                    ]
                  }
                }
              ]
            }
          }
        }
       ],
     };
    print (res)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print (r)
    return r

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    print ("Data.........")
    print (data)
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

#************************************************************************************#
#                                                                                    #
#   Tell USER about Visa Check Bot - ASK TWO QUESTIONS                               #
#                                                                                    #
#************************************************************************************#
def asktheuser(reqContext):
    print (reqContext.get("result").get("action"))
    option = reqContext.get("result").get("action")
    res = {
        "speech": "Great! I'll ask two questions only",
        "displayText": "Great! I'll ask two questions only",
        "data" : {
        "facebook" : [
               {
                "text": "Great! I'll ask two questions only."
               },
              {
                    "sender_action": "typing_on"
              },
              {
                 "text": "Then only I can precisely tell whether you need a VISA or NOT to travel your destination country."
              },
              {
                    "sender_action": "typing_on"
              },
              {
                  "text": "Ready?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "I'm Ready",
                  "payload": "I'm Ready",
                 },
                 {
                  "content_type": "text",
                  "title": "No Thanks",
                  "payload": "No Thanks",
                  }
                  ]
                 }
             ],
        "telegram": {
                 "text": "Great! I'll ask two questions only. Then only I can precisely tell whether you need a VISA or NOT to travel your destination country.",
                 "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "callback_data": "I'm Ready", "text": "I'm Ready" }], 
                        [{ "callback_data": "No Thanks", "text": "No Thanks" }] 
                       ] 
                },
              },
        "slack": {
                 "text": "Great! I'll ask two questions only. Then only I can precisely tell whether you need a VISA or NOT to travel your destination country.",
                 "attachment_type": "default",
                    "actions": [
                         {
                            "name": "response",
                            "text": "I'm Ready",
                            "type": "button",
                            "value": "I'm Ready"
                         },
                         {
                            "name": "response",
                            "text": "No Thanks",
                            "type": "button",
                            "value": "No Thanks"
                         }
                     ]
            }
           }, 
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": "Great! I'll ask two questions only. Then only I can precisely tell whether you need a VISA or NOT to travel your destination country.",
              "attachments": [
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "buttons": [
                      {
                        "type": "imBack",
                        "title": "Ready",
                        "postback": "Ready"
                      },
                      {
                        "type": "imBack",
                        "title": "No Thanks",
                        "postback": "No Thanks"
                      }
                    ]
                  }
                }
              ]
            }
          }
        }
       ]
     };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   Asking the USER the FIRST QUESTION - What's Your Nationality?                    #
#                                                                                    #
#************************************************************************************#
data = None
def userNationality(reqContext):
    nationality = "False"
    destinationcountry = "False"
    print (reqContext.get("result").get("action"))
    res = {
        "speech": "What is your nationality?",
        "displayText": "What is your nationality?",
        "data" : {
        "facebook" : [
              {
                 "text": "What is your nationality?"
              }
             ],
        "telegram": {
                 "text": "What is your nationality?"
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": "What is your nationality?"
            }
          }
        }
       ]   
     };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

###     START AGAIN       ###
def userNationalityRecheck():
    print ("******userNationalityRecheck********")
    nationality = ""
    destinationcountry = ""
    res = {
        "speech": "Which country do you want to travel?",
        "displayText": "Which country do you want to travel?",
        "data" : {
        "facebook" : [
              {
                 "text": "Which country do you want to travel?"
              }
             ],
        "telegram": {
                 "text": "Which country do you want to travel?"
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": "Which country do you want to travel?"
            }
          }
        }
       ]   
      };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

###   Start Over        ###
def startOver():
    print ("*********startOver*************")
    global nationality
    global destinationcountry
    nationality = ""
    destinationcountry = ""
    res = {
        "speech": "What is your nationality?",
        "displayText": "What is your nationality?",
        "data" : {
        "facebook" : [
              {
                 "text": "What is your nationality?"
              }
             ],
        "telegram": {
                 "text": "What is your nationality?"
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": "What is your nationality?"
            }
          }
        }
       ]   
      };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


#************************************************************************************#
#                                                                                    #
#   Asking the USER the SECOND QUESTION - What's Your Destination Country?           #
#                                                                                    #
#************************************************************************************#

def userDestinationCountry(reqContext):
    correct_nationality = ""
    print ("Within userDestinationCountry METHOD")
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    
    # Loading nationality input
    global nationality
    nationality = ""
    nationality = str(resolvedQuery).title()
    
    # Loading Nationality List into Array to validate against the user nationality input
    file_path = '/app/country_name_JSON.txt'
    with open(file_path) as f:
       data = json.loads(f.read())
       print("First Element from Nationality_List -->" + data[0]['nationality'])

    # Loading the Nationality list to validate nationality input:
    for data_item in data:
        str_nationality = str(data_item['nationality'])
        #print (str_nationality)
        if str_nationality == nationality:
           correct_nationality = nationality
           print ("This is the CORRECT nationality--->" + nationality)
           break
        
        
    if correct_nationality:
        print ("Which country do you want to travel?")
        speech = "Which country do you want to travel?"
        
    else:
        speech = "This is not a valid citizenship. Please enter a valid citizenship"
        print ("This is not a valid citizenship. Please enter a valid citizenship")
        userNationalityRecheck()
        

    print ("userDestinationCountry Method nationality --> " + nationality)
    res = {
        "speech": "Second Question",
        "displayText": speech,
        "data" : {
        "facebook" : [
              {
                 "text": speech
              }
             ],
        "telegram": {
                 "text": speech
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": speech
            }
          }
        }
       ]    
      };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   This method is to get the Wikipedia Information via Google API                   #
#                                                                                    #
#************************************************************************************#

def wikipedia_search(reqContext):
    print ("***Nationality has the latest input-->" + nationality)
    resolvedQuery_wiki = reqContext.get("result").get("resolvedQuery")
    global nationalityNEW
    #To capitalize the first letter
    global destinationcountry
    destinationcountry = ""
    destinationcountry = str(resolvedQuery_wiki).title() 
    
    if destinationcountry == nationality:
        destinationcountry = ""
        print ("destinationcountry: " + destinationcountry)
    else:
        print ("destinationcountry: " + destinationcountry) 

    
    # Check if the country name is abbreviated, put the correct names:
    if "Uae" in destinationcountry:
        destinationcountry = "United Arab Emirates"
    elif "Usa" in destinationcountry or "Us" in destinationcountry and "Russia" not in destinationcountry and "Mauritius" not in destinationcountry and "Cyprus" not in destinationcountry and "Australia" not in destinationcountry and "Austria" not in destinationcountry and "Belarus" not in destinationcountry:
        destinationcountry = "United States"
    elif "Uk" in destinationcountry or "England" in  destinationcountry and "Ukraine" not in destinationcountry:
        destinationcountry =  "United Kingdom"
            
    
    # Loading Nationality List into Array to validate against the user nationality input
    file_path = '/app/country_name_JSON.txt'
    with open(file_path) as f:
       data = json.loads(f.read())
       print("First Element from Nationality_List -->" + data[0]['nationality'])

    # Loading the Nationality list to validate nationality input:
    for data_item in data:
        str_destinationcountry = str(data_item['country_name'])
        if str_destinationcountry == destinationcountry:
           correct_str_destinationcountry = destinationcountry
           print ("This is the CORRECT destinationcountry--->" + destinationcountry)
           break
        

    print ("wikipedia_search Method nationality --> " + nationality)
    nationalityNEW = nationality
    jsoncountryappendage = "}}"
    destinationcountry1 = str(destinationcountry + jsoncountryappendage)
    print ("destinationcountry1--------->" + destinationcountry1)
    google_query = ''
    if nationalityNEW:
       google_query = str("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&&titles=Visa_requirements_for_" + nationalityNEW + "_citizens")
       nationalityNEW = ''
    else:   
       print ("Nationality value NULL, hence NO API Calling...!!!")
    ###########################################################

    if google_query is None:
        return {}
    print("google_query::::"+google_query)
    if google_query:
       result = urllib.request.urlopen(google_query).read()
    #print (result)
    data1 = json.loads(result)
    infotoStringFinal = "0"
    #data1 = str(data1)
    wikidata = str(data1).split("{{flag|")
    for info in wikidata:
        #print ("info within FOR Loop--->" + info)
        if destinationcountry1 in info and "}}." not in info and "{{flagicon|" not in info:
           print ("I'm in IF loop, therefore I'm already in FOR loop")
           #infotoString = str(info)
           infotoStringFinal = str(info)
           print (infotoStringFinal)
           break
        elif destinationcountry in info and "|state<!" in info:
           print ("Exception handling for Peru, Belgium and Costa Rica")
           infotoStringFinal = info.split("|state<!")[0]
           print ("Country name: -->" + infotoStringFinal)
        else:
           continue
    print ("NECESSARY STRING -->")
    # Check all artifacts which are to be removed to get the VISA INFORMATION
    print (infotoStringFinal)
    #print ("Section splitlines -->" + infotoStringFinal.splitlines()

    if "Visa" in infotoStringFinal or "movement" in infotoStringFinal:
        #visa_status_primary = infotoStringFinal.split("\n| {{",1)[1]
        visa_status_primary = infotoStringFinal.split("}}<ref>")
        print ("After splitting }}<ref>, here is the 2nd part -->" + visa_status_primary[0])
        
        # Checking for the 1st && 3rd CATEGORY, like --> Denmark}} \n| {{no|Visa required OR Thailand}} \n| {{yes|Visa not required  Germany}}\n| {{free|{{sort|EU|Visa not required}}
        if "|{{" in visa_status_primary[0]:
           print ("3rd Category -> 1st clause of |{{ --> " + visa_status_primary[0])
           # Germany}}\n| {{free|{{sort|EU|Visa not required}}
           visa_status = visa_status_primary[0].split("{{")[2].split("}}")[0].split("|")[2].split("}}")[0]
           print ("3rd category: FINAL visa_status -->" + visa_status)
        
        elif "{{" in visa_status_primary[0]:
           visa_status_temp_1 = visa_status_primary[0].split("{{")
           print ("Splitting the {{ from the string and select LAST PART-->" + visa_status_temp_1[1])
           
           # Checking for the 1st CATEGORY, like --> Denmark}} \n| {{no|Visa required OR Thailand}} \n| {{yes|Visa not required
           if "|" in visa_status_temp_1[1]:
               visa_status_almst_fnl = visa_status_primary[0].split("{{")[1].split("|")[1]
               #visa_status = visa_status_temp_2[1]
               print ("1st category: FINAL visa_status -->" + visa_status_almst_fnl)
               if "}}" in visa_status_almst_fnl:
                   visa_status = visa_status_almst_fnl.split("}}")[0]
                   print ("If visa_status holds }} then split it -->" + visa_status)
               else:
                   visa_status = visa_status_almst_fnl
        
        # Checking for the 2nd CATEGORY, like --> Malaysia}} (e-Visa required)\n* 
        elif "(" in visa_status_primary[0]:
           visa_status_temp_1 = visa_status_primary[0].split("(")
           print ("Splitting the ( from the string and select LAST PART-->" + visa_status_temp_1[1])
           if ")" in visa_status_temp_1[1]:
               visa_status = visa_status_temp_1[1].split(")")[0]
               #visa_status = visa_status_temp_2[0]
               print ("2nd CATEGORY: FINAL visa_status -->" + visa_status_temp_1[1].split(")")[0])
        else:
           #visa_status = visa_status_primary[0]
           print ("ELSE: No exception found, so assigning same variable to visa_status_temp_1-->")
           
           # 5th CATEGORY like, Thailand}}\n| Visa on arrival\n| e-Visa for 60 Days\n|-\n|
           if "Visa" in visa_status_primary[0]:
               if "}}" in visa_status_primary[0]:
                   visa_status = visa_status_primary[0].split("|")[1].split("\n")[0]
                   print ("5th CATEGORY --->" + visa_status)
           elif "Visitor" in visa_status_primary[0]:
                if "}}" in visa_status_primary[0]:
                   visa_status = visa_status_primary[0].split("|")[1].splitlines()
                   print ("5th CATEGORY --->" + visa_status)
    else:
        visa_status = infotoStringFinal 
        print ("No change in VISA Status -->" + visa_status)
        # 4th CATEGORY like, Australia}}\n| {{yes|[[eVisitor]]}}<ref>{{Timatic|nationality=DK|destination=AU}}
        if "]]" in infotoStringFinal:
            print ("Check 4th Category-->" + infotoStringFinal.split("]]")[0].split("[[")[1])
            visa_status = infotoStringFinal.split("]]")[0].split("[[")[1]

    #########################################################################
    subtitle = "You need " + visa_status + " for " + destinationcountry
    #########################################################################
    if visa_status == "Visa required":
        image_url_final = str("https://www.iconsdb.com/icons/preview/red/visa-xxl.png")
    elif visa_status == "Visa not required" or visa_status == "Freedom of movement":
        image_url_final = str("https://www.iconsdb.com/icons/preview/green/visa-xxl.png")
    elif visa_status == "e-Visa required" or visa_status == "eVisa" or visa_status == "Visa on arrival" or visa_status == "eVisa / Visa on arrival":
        image_url_final = str("http://www.iconsplace.com/icons/preview/yellow/visa-256.png")
    elif visa_status == "0":
        image_url_final = "https://previews.123rf.com/images/lkeskinen/lkeskinen1707/lkeskinen170701095/81349455-no-information-rubber-stamp.jpg"
        visa_status = "Hmm, No VISA details found"
        subtitle = "Please check the spelling or see if it's a valid country name"
    else:
        image_url_final = str("http://www.iconsplace.com/icons/preview/yellow/visa-256.png")
############################################################
#    
############################################################
    res = {
          "speech": "Visa Status",
          "displayText": visa_status,
           "data" : {
              "facebook" : [
                  {
                    "sender_action": "typing_on"
                  },
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : visa_status,
                                   "image_url" : image_url_final,
                                   "subtitle" : subtitle,
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://en.wikipedia.org/wiki/Visa_requirements_for_" + nationality + "_citizens",
                                        "title": "More info"
                                    },
                                    {
                                        "type": "element_share"
                                    }]
                                 } 
                           ]
                       } 
                   }
                },
                 {
                  "text": "Write another country name to continue checking VISA requirement",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Restart",
                  "payload": "startover",
                  },
                 {
                  "content_type": "text",
                  "title": "No",
                  "payload": "No",
                  }
                  ]
                 }
               ],
            "telegram": {
                 "photo": image_url_final,
                 "text": subtitle + ". Write another country name to continue checking VISA requirement",
                 "reply_markup": { 
                   "inline_keyboard": [ 
                        [{ "callback_data": "startover", "text": "Restart" }], 
                        [{ "callback_data": "No", "text": "No" }] 
                       ] 
                },
             }
           },
         "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": subtitle + ". Write another country name to continue checking VISA requirement",
              "attachments": [
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "buttons": [
                      {
                        "type": "imBack",
                        "title": "Restart",
                        "postback": "startover"
                      },
                      {
                        "type": "imBack",
                        "title": "No",
                        "postback": "No"
                      }
                    ]
                  }
                }
              ]
            }
          }
        }
       ]   
      };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


###   No Thanks        ###
def noThanks():
    print ("*********No Thanks*************")
    statement = "I'm sorry to hear that. But you can always click on menu to start again."
    res = {
        "speech": statement,
        "displayText": statement,
        "data" : {
        "facebook" : [
              {
                 "text": statement
              }
             ],
        "telegram": {
                 "text": statement
             }
           },
        "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "text": statement
            }
          }
        }
       ]   
      };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   Help Information Providing                                                       #
#                                                                                    #
#************************************************************************************#
def help():
    speech = "Write Hi to start or you can choose option from menu."
    res = {
        "speech": speech,
        "displayText": speech,
        "data" : {
        "facebook" : [
               {
                "text": speech
               }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#   Displaying ALL CHATBOTS - For Sale                                               #
#                                                                                    #
#************************************************************************************#
def moreBots():
    print ("Within forsale method")
    speech = "This bot is been created by marvin.ai. \nDo you like it?"
    res = {
        "speech": speech,
        "displayText": speech,
        "data" : {
        "facebook" : [
               {
                    "sender_action": "typing_on"
               },
                {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "You like Visa CheckBot?",
                                   "image_url" : "http://kredist.ru/wp-content/uploads/2014/10/%D0%B2%D1%8B%D0%B5%D0%B7%D0%B4-%D0%B7%D0%B0-%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D1%83-%D1%81-%D0%B4%D0%BE%D0%BB%D0%B3%D0%B0%D0%BC%D0%B8.jpg",
                                   "subtitle" : "Get customized virtual assistant for your organization today",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "Buy Template"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://www.facebook.com/marvinai.live",
                                        "title": "Facebook Page"
                                    },
                                    {
                                        "type": "element_share"
                                   }]
                                 },
                                 {
                                   "title" : "Travel Agency Bot Template",
                                   "image_url" : "http://www.sunsail.eu/files/Destinations/Mediteranean/Greece/Athens/thira.jpg",
                                   "subtitle" : "Get customized virtual assistant for your Restaurant today",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "Buy Template"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://m.me/926146750885580",
                                        "title": "Chat"
                                    },
                                    {
                                        "type": "element_share"
                                   }]
                                 },
                                 {
                                   "title" : "Real Estate Bot Template",
                                   "image_url" : "https://husvild-static.s3.eu-central-1.amazonaws.com/images/files/000/280/915/large/3674bd34e6c1bc42b690adeacfe9c778507f261a?1516032863",
                                   "subtitle" : "Get qualified buyer and seller leads automatically delivered to your inbox!",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "Buy Template"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://m.me/realestatebotai",
                                        "title": "Chat"
                                    },
                                    {
                                        "type": "element_share"
                                   }]
                                 },
                                 {
                                   "title" : "Restaurant Bot Template",
                                   "image_url" : "https://www.outlookhindi.com/public/uploads/article/gallery/6eb226c14abd79a801172ab8d473e6d2_342_660.jpg",
                                   "subtitle" : "Perfectly crafted bot from assisting online customers to handle orders",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "Buy Template"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://m.me/730273667158154",
                                        "title": "Chat"
                                    },
                                    {
                                        "type": "element_share"
                                   }]
                                 },
                                 {
                                   "title" : "Coffee Shop Bot Template",
                                   "image_url" : "https://images-na.ssl-images-amazon.com/images/I/71Crz9MYPPL._SY355_.jpg",
                                   "subtitle" : "Your bot can deal with online customers, take orders and many more ",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "Buy Template"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://m.me/200138490717876",
                                        "title": "Chat"
                                    },
                                    {
                                        "type": "element_share"
                                   }]
                                 },
                                 {
                                   "title" : "Gym & Fitness Bot",
                                   "image_url" : "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxITEhUTExMWFhUXGBgaFxgYGBoXFxsXHRoaHhoYHhgbHSggGBolHRgeIjEiJSkrLi4uGB8zODMtNygtLisBCgoKDg0OGhAQGi0lHSUtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAKQBMwMBIgACEQEDEQH/xAAcAAACAwEBAQEAAAAAAAAAAAAEBQADBgIBBwj/xABAEAABAgMFBQYEBAUDBAMAAAABAhEAAyEEEjFBUQUGYXGBEyKRobHwMsHR4UJScvEHFCMzYiSCskNzkqIVNET/xAAZAQADAQEBAAAAAAAAAAAAAAAAAQIDBAX/xAAjEQACAgICAQUBAQAAAAAAAAAAAQIRAyESMUEEEyJRYTLB/9oADAMBAAIRAxEAPwD4bEiRIAJEiRIAJEiRBABI9gk7OmgXjLWBWpSQKY5RyLJMci4pxUi6XA4hqQwKRHQEeNFiRDQiJEWXY8SIvQjhFpCbKrsWiS8XIRFiRDolsH7IxaizcWi6aqlPrHPbN44QxWz2VYDUv4fOCP5e6nl9oJsynEeTBVvfv6w0iGygyicOHp6R2U1r79tFkoKLU5+MeqAzw4QxWLbQhySBFKJRwLvSGMyWH4uC2I/aLFWWpejchX384VFchWuUOR0jzsqCGsqy1wp01Mers4Hv3rBQchLMQ1Dj7oYoWiG8+TniTjAps+TV4YesJopSFhTHjQZOkmBlpiHEtOzlo5Ijto8IiRnEeR0Y8MAzyPI9iQgPIkSJCAkSJEgAkSJEgAkSJEgAkSJEgAkMNl2wyXmJA7TBBIe7qoccnyhfBU4sAOAhoB2jbM+etMszFJvEMauAly9K5eUX7V2qgSrklai5ZSlOVKFavkDm2NKxnZK2WCQ4FDywPLGDZNjM+Z2csByaEuPrSHYkregBJvFiWORghVmUn4h1y4dDF0zY81E3sykEj8pcYkFjwUkjmDGrsG7aloN4qAAIrriHELmltlrHKTpIxoTXnBcuXSOZiCCzVBIPDXwgmzp8dI1Rg2cFBjtCM46nFg8dSFEu7Vxxy4RRJwiSTkK0j0WAqct9DhBaV1YN4ZR2meUA0erjq1G04wCslkspALjPlBCpb6CK7OpVLxAdyNScwBlB8uTxy0fnlDECplhhgesQySxf2Hjm0OgjvAA5kVx9+MeJW54+Qw88TAIFmBqAVjgkhwCK4DPGCZ6FKZgKevAD54NEVIYVZxixrV6HTDPUwAUSppdvX3wi60rYe8acI5s8slYAI84JtMo3cWpqBRxXD3SABRPXhlz0gVV9qUGcGWyzqIBPyY8axWqiSCMKVA+pYQi0LpyznFLQRaK0f3844ly8Afl4RBojyXJeuXn0i7swKN9eR1wiyaCkYvhgCAKUHEtjHIlrzBD5mIbLSOCjO6OoECz0MSwYZCHNnkua1PjBdpsAPdzbDmImyuJlSI8MWzUMSNKRXFEnMSPYkIDyJEiQgJEiRIAJEiRIAJEiRIAJDK3Ss8qeYhemG1r/ALQ1CU+hikAHIA7yjlGg3SnCXPQpSTdcHu1wINeBZjzgDZNlDKUsfhcdcI0+6dkKQpSKqZYS+RYt6xnNqjTFF8kONqSilEgqWkqCVOU1BClqUC7klwbxqakwbMtIl2YOhR7VTBaSABQly4IyzpCDc+UmZdlqPdADDnGx21Llolos7KKauzAd6l0kmgN5uojB6dHbHcbR8mWby1KpVRPjXPnF8mV5x6uRcUpOJCiHxBYs/lBKAc/L3zj0Ujx2DTJSTQ6v74xfLkU1xrlz44x2ZOYF48KmDbHZy1cMDkeLenWAkFkoBKmZ6CvLywjtNlclWmXHnh7EHKsQpiFHkwwp4RVLUQRRm8D/AJY8fOGIoRY61emL5Drw0eGCbKQDU4U4DPHIP5xdZ5oUQ9WLs2bFgA4f92ekFyZFFKLupgBdILacamABbMs1HWkmn5CwD0D5FvXhFfYAHSrHKtB9oYolrFKEjAKelH10PPwi1SEO5Ds9XbIVGD/cwCA0WIABRzJrQsAcvxZQDLsKbxUQdTUjvajTx0h5aZBX3AqgyGlXrllFh2akB6jEgByW9SYAEkuQFYACnm7/AGjmbI/CaCpOmOev2hyNnrUqrs3xFgxOTPjA1tlXfhDvn+8AGctId7uuBAbh75QDOCh8QYjhoNNKw+RZlZBq45e+HCArWhIxerPi/pQ084BpiGZLOmXlFKgoM7dRRuWcM5sgFu9U4DTDP6RXabMrLEZlxR+TNWJo0UjebnbDs82zduUhcy67H4RU32HADOMxt61mZiKurDJzhwg7dPeZVms85PZBV1nd3uLWApmPxAqBFavwjzauxJqXnFCky1E3VKADvUZnWOVqpbO5O46EAVdusHJIAAzL/eNJNsS1pJllCykNNCFAmXlUcxiHDjGOdhWOVNUoKYEpupBFHLd7mGhpuZYeytlokzCSrvguGBr+E4qSfiNGe7jWE5DUfs+ZbSk3ZikwK0a3fnYnZLvpcpNDw0+nhGUIjWLtWc84uLo4jwx1HhhiOYkSJCAkSJEhASJEiQASJEhpsbYM60uZYAQkspaiyQdHzPAQXXY0m9IWRsNjbCVaFArBTJBDk0vNkBmNT84fbvbMsFi/qzFdvODMSnuJxqlJxOFT0aC9tW3tLOJ0u6h1KvByPxGoYHw4wm218SklGVSM1thIMxaUkgAsCMGEH7tW3s1EY3gRStWoYK3dX2irqJYJZ1zFUSBSoGeePAsRB0zallCikKuh6KuBSlcWBAQNHflmqXHVMpSp3Eze7tuuWhJUGDgKGaekG707XMyaqWgulJYqcm82FHoxJEFW9EicB/UJbAkAKHWEczZZT8LEecOChythN5OHFFcpODfWCUhjz99IkpDDBq/OLgK4e/l946zhYTIkAHX6deMWz5gSA5FS2PD60jiRMrr1bDN+A9IYWSy5kuQMcs8B4QCKbGsKLn4cnf4i+L4QXOsQVU0ya8QW6eNNIvRZCHL45Dyi7sFJIoSDk+fLHFs6PAB5YZTIAQ7AsHNWzqRw44mGEqUQAVUpUcXoxamBgQSw6TLKndzmGwwGZIh3IlDEmuLegEAGaMhdVIcDJsiaVvY69TDKVs26l7pmLwLkBnOLYYAuelYbqsiWPdfMjFz86CLrPIIBvDk1e6TTKmPlAFCZFjUO8aUACWc0xLjOCFWdLXmw5Up9IaTpdMD0fLygG0SLwI1NQxqdOTDzgAUzZ4u0NMKOdcICnIUrBBIAo2BLe/CHplJBcpH5U4nPSor8orqJYKhXhm5x8DjAIzE66EUBLd00bn56QimSFLUzOH7xI7rZUNTrlhG1TJScQHZtaPjwrlCza7KQUhmwVhQaNABmpdgKXWcRR8DyKcAM4AKhWj6BiG1DnNoe2S2XgkU0JpgAznjA20JLqABFP3gHYLKno7KchQIKgkJbBwpKj6HwjT2q1TJlgky5q0KmIxANTLAaWS1CbucY6fK1Sxy/eDdk2u4FCaFtdUJd1QF1TvWlUqcxjlhe0dWHKlphGyQUzkkZHPSHdu20k7VkqR8KUIlrL4lT/WEatnT1I7QXU3qhDm9df4m0dh1gex2ciVOUS6gUq49018owOqzZb0JSCuXMDivg/pGAtW7yH/pzGGhD+cONs7xqmtRyQHgFHaKFRd01+kEU0KTUmIrRsWYkEgpUBoawNL2fNVgk9aRspOzQ19dTE7ZCSGQG1GPhhD5ke2jE2qxzJfxpIfA5eOEDx9Ms6ETiZa0gpUmo468NXjE7y7FVZZ5lmoIvJP8AideIwhqd6Jnj4q0KYkSJFGZIkSJAAVsyxKnTUy04qOOgzPQRt5p7O5JlhkpFBpqeZzMLd2JXYWWbavxrPZyjoBVSvFh0hywI/mW7kxKSOBIDjoXHSM5bN4Kl+/4JtpT/AOqiX+bunmcPNoYSpZXKQg/CO82pLY8Iz0437UnS+kngAXJ6AE9I08kskatXnGsejCbth1kUwEhOMy8pfFIAfoSUpbQkRntsoCZ1xOOKjxh/u6f9ab2AkEjkFV82jMbRtP8AqJimxNIhv5GsUlBHtntab114fbKsl9adAXPKMdKsyhfWcAR5lvnH0HcW0JUbp0MRk6NcO5bA9sWS5N7uY9+scSJT4+3fhhjB+8KWWn3++MDSUg15NlSOjA7gjj9UksrIJABNCX5v5QwsyQME4PhXOKS6u6B1bxMMbHZlYl6san7fM5xsc4Qllpugn7tz5wTLkJNWbL1HjFa0XUlTgMHJODfXnw5R5ZrWpQvgCWj88w1ILl7uT41IPCENJsKTYi7hh7NIZy5NHrz5/PjwhbZtppIAdKw7ukv0IBL0D4w6sxJYj4W+dDjh9oLCqLJKcyl/COuyJ9+9YKkofHLF4uXJyzyhWOhXbVhCCtbJSPDVow9t/iBKCiEyipNakirYEJ0POLf4sbYUgS7Mg/ECpbZofup5Egk/pGRj55ZrIqYhc5SrktFCsgkFZwlgasXOgyLgHOU3ejaOJVbPpGw96ZVpVcI7OYxugkKCuALULDBvGHdpRVyKadfPlwj5FYLWhF57x0LDxYl+MfQ91t5k2gCWp+2DVJ/uADH9WohxnemTPHW0GWh7tcXwdycx5wtn2dyXzL4Zty1fwh7PQKku4pl7+ULJycnxD+njX1EamIim2RIqwcOMPJ+MJbWs3hyZvfhGnnJxcYVhVY9nhc0EnupqQ+Iy8frClKlbHGLk0kKJtn7t4pcY1DQuTtDs1BkBTYAuQ/IYxqNtC+WThwzhVKsaRl9Y5vdb7O5YIro7O05xX2rhzdcMwDVCeQjsWpCrUFJSyF0WKt3gyubQbI7FOICjpjAU23qQpmF0mtAze9IzNjzZ+x0ywVTACpzc/SMD1g2TNBDFL9YdbySASi6m6i6GhKtIRhCHVdA1rQsfACxGEKbNPImXVhtQdIbC3EquiNBv5YJcnZ0iZcT2pUO8fiZVGB0wPSGn4Jf2U2fZnZTZei2unVNG/wCRH+2Cf4lbBTabPJnpooApB1UCxB5tGY2Vtxc25LmKa5RP6Sa+BY8ngja+2J6btmmGkoktxVUmFTsNNfh86nSlJUUqBBGIMSPqVnnIWkKKUudQIkV7n4T7H6fKokSHm5lgE61y73wIeYv9KKt1LDrGjMErdD/eOV2MmRZ85csXm/Oaq8yY83VtwXZZ1lV8STel6sfiHz6wt3gtpmTFrOZLQBsa0mVNB/N6CElouU6ehzs7ZhSpSzUmj5AaDnmemZhpdaDZVoM1FxISnNxiYHMpSS7nnFmJ1ZrSlKgXuqAUEk6KDFJ1B8iAYz21bOTMe6eLV8xDO1AM7hT5Y1zplFVjW5wLDi7eL/KFQ1JrQFtWcgSEywe8taQeQL+sPdxktMA0LRldrzP9Qh2YFPPGNLu5PuWgj/KMsiqJ0YZXNMb7x/3BoM4Dsq8AG5jXw9tDXeSWxJyJBEJ7Knk2XzrGvpncDH1say39oOkqYuT1fxPJhBFl2kg94qN38KU0Uol6k4gZsK6kB4UbemNZpigcm6EsR1jJyNp4PwbXpxw8I2kzngr2bW3WlU20WezgkIUVLWLxVRAJAUHIxHiOEHWq2uZq1IWvs1AS0D4S7gkcABeJyA0EZaVbCi1WVcwXL94KGBAW6Uk5iqn6dIL29s2eZndUpKyVS2SWUqWukxL0BBSo4muEQna0atUbDeHZsmV3l2mWZiijsQg3Z5KmAPZYooRRWINcSIe7GMxCuwnNeZzdIKTxB0LGmRDRkdnbvbPlomlSe2tCVYzu0TKU5/uIlqAvUejlj0hlu/api50xalKWq9iSSaJSDXAgVHBsIasUujek6DR/ekWkFswT1/aBbPMfKvI9aty84MRxhmR8h/jNs5aLRKngEoXL7McFpJLcCb5b9J0hB/EO3pTaP5RACJNkAlpQnAzLo7WZxUVOHNe6+JMfdNrbPlWiWqTOSFy1AOM3GBBFQoHAgx8R/iFYgm1z5d26uYszb6qhSVOWSWpVw+oOGeco1s3jK1RnbBJJV3iAkju0Up1fldILEYkaQ6nyeyKCk3Zia0IUlwXCgRiDiDpCzY9oQggTQq6EsFBryC7pmJ0UMDqOVbJkxdpnJSkDtFAJLEFJIxVTAAVOjdImi0z6vYJhmSkTGHeSFkZEqALOT58YrnyqmnDDIVHhF9is6ZcpEtIIZIT4JbDpA9sIILGvOkdCORiy1S3VSlS/Lrz8uECr7oUaAEa51+sWWq1pCgl8Xx09+kZbeDbLkpSYwyyv4o6cEK+bOZe1mmGWoiuBj1a7ymyjK2hV4vDjd633lBK/iyOv3iHGkbqdujTypSUJwhNtaYMhUQ2nqoag6tGW2hPdV3WIii5OkfTNqkLlIWMLqfBoxm0bVlGisM1I2eHW5CQ3QtT3lGFtCypRrBFBKWh5utZTNnJGpht/Gq2l5FnT8KBeP6mYepirdGemzd5RDlroxLjQRV/EMBaErfvZh3I5nUwJ/ITXxMPZbUQUrTRSSD1+kaeepNokqnIPfQO+n8QTrxHGMVeul4KkWoj4SQ9C2LGhB4GNXEyjOjT2FAUhKgpny6xIEs1tMtIQ+H1iRnTNU9GSja7oyhLsNpnfjmKEpP6QLyz5p8IxUfR7ZIFlkyrMKzDLTe/xv95Z5l25NFMyxryZi3SqCEyp/fChkQ3IQ73pmhN1A0rGeikTLs3WwrXkMxTKhyoH84PRNU7MB4xj9izy6G/CoUyYnTxhhvpIEuawo+MO90Tx1Y12qk0p76vHNjSpIcJ8G+Qi7fuSlFy6ADcRhT8IindwlQa8R1IieerL9p8qM7t/+4CNPecNbLav6oUMwIB3rsykTM2jixukSzwEEtoIXGVH0WYvt5V38SQ46Qqsb0YEjKnv2Ir3e2h3y8NzZJSboE1kpFYwhkljtI68mGOapMUbWKloWgoPfSRhmcD0hbs3ZRlC+mUCR+OZXwEbVFrsUuoCpquVPGFO10qnsAvs2NAACnkR+IciDGsZTyeDnlHFh87EKNh/zBUqZMCbz98tiBpkBDzZe3LoTLth7OYgXUT/APpzAMHUQz6vjQ4wdspJQAFIlOfxh3fW6QSD/uhjJQ6gVm/jQgYYmhyz+sdEY0c0siZwtYUoIM6XdIa9LDrOHdS5Iwzq8PtkWQJAcAJAupBxAJdy9XNDrrjQawzJaHIQiW2LAJpTFuflBkmeVuxYM+qi9enryaKozc7HdnIA4Vzi1E3Ic6UGPswtQtQGPDTWnlBMleDH0HWAQase9PfzhFvFu/Z7Wm7NS6g9xaSAtJzZWh0L4QzVOINFdIpXNegOrmFQXR85n/w0SFf/AGVXXr/TBVyBv1oNIUzrELAsoKHSp7s3NQBwf8BGgj6bPnmpBL5U4461hPtOyImSyhYvAtRs2xc4FszETx2tG2LLT2YlW0CSwmrbmVJ6pLgcxBg2zOQKpTMS2VPHH0hVvBsNdmIKCVIJpqOcD2Dabu5YjB/SMk5LpnS4wl2gXam0Zi1doQEs4pgBlCVRKq5Q62ioLDnF6EQpmKbiYaZLVFU1IApHU+yqlpQsUOeoVj006cYvkyKuo1FQNOf0i6dNJdJL6xrGOjCc96Gez5kyYnuMbzXsq8YO2lsWVZQJkwlcxQcJNAOcLd3pxlhTKZiCxzb94fb3yV3EzZy3Kk9waCOd6dHWqcbB1lK7DLmgNcXMQoJozlx0Ywik2eUo91RCuMEbAUVJXKHwrSXH+QDjrjC+SgJWzsXh1QrujTbCs6bNOlqn1BqHq4hTvZaVC8KATCVMMg9BBO1lkdmSoLISwGcZ7bFpUtQBLn3SCKt2E3SoUTo7sMormISMyPvHlqHeI0p4feGm6skGYqYcJaCr5fWLfRglboKnHvKGiiPOJHOLk5knxLxIRqLt3bH21qkSvzzEA8rwfyeNjt+0CZbpy8gogchh5Qh/h6P9dLV+RM1fhLU3m0WWy0MVq1Jg8kx6E22p16aTAQj2atyTBeyNmrtEwS0BziTonMxXSI7Y03UszzElsVj/ANT9Yb712f8AmLfLkoD3lJSedLx9fCH+7FkRZ5wBTQJICjgCBQwvkWZaZxmj4gSxzrnGfLZsoaoXb8WrtLQsJ+FJujkkMPSBthWooIeC7VsmatRLdYGTYlpLNBqqDalZod4tkidJEwVpGWkS2Fw5BgeIEbjZ00/y5SoGMjbS01TcPSDA7uLD1K41NDLZa5aEEq+LhnxiFd4nIBoWJmEHLwgqzzMmjZYYp2znl6mbVLSD5KtCC3zyOsHyFampPljj7xhTZ7Q37e9YYpUCKdBhGxzjWU2BHTFvKCpcxGYBavM5ecZ2zW9SfibDryOsFWfaAOD8R+3U+EAh1KsILFQBU+JTTpT7w/lzGByz0yw9Yz1ltoUzU0zwxOr1Axj0zzeBJZg5IJA6gYitPrABokTgqmWOlK54vnF6JtGfrhrCizTgrDClcPefDCC1TSwc09lvWAYcpf7faBps0Jrm3B+Af58IoM9wwfHgG4+/nAtrtAuk4BjgMtfWADlE66GIq5PlSOLRaLorjgHNMicHfLxhci2FV66wbDUl6kgt7EcWlYZSXbEXnAJ4dDAIutykTEkLAwc1qDxGJ+UYy37ukkqlF8KGmOhwOGsaKfdF4ywTTHFROjmp5PlC6dbDdJwUCxcFmqNM4hwTLjklHRlZdinXig4u1ddBr0g6ZssIReBvLq5+gy+4gy0JSSFXXXwxc+jA44wLbjU6gVc5UOWfOBQSHLI5ClLqJdtS+ObZRJiqxTMNbxerZ8I5WrCuUUTQ4sMoqlKYd5wUnliCPeENNvrmKkyzMHdAZJqcMmiyxoZCEgUoSeDBvnBapjSVpofyuxY5sI4nK3Z6UY1GjM7FUtMy8hKiwIwbEEZ84EMiYFEsx4nCG0+cUyyCpRWcycBoAKCEcw8TUtFoh6O5C1XiSXyeBkn+peOCXPhWC5xCaDAQvnK7qzyHj9gYaIYvUXxh3sJP9Ka9ApSE+F4kQkjWbBsouBJDhKTNmAYsSlKQD+bvJLZh4chQWwQWdaqhKumESPodk2FLShKZiJipgDLKCAm9mkfpPd6RIz5m3tnz7cVTTpytLPN82HzhdtOe9IZ7pS2k2ya9UykpH+9Tn/hCZUhcxRCEqUrQAkt0jRGD/lAUafZVom2aWRLXcK2KjdF7CiXIoA/nCazWFYmpStBTWoUCKCpx4Qw2ja8YpL7Iuuj2ftW0E1nzP/Ij0iqXbLRlPmf+avrCqZNJMHCa0sN1h0gt/YT/APJ2kf8A6FnnX1iyTtyek1KV8x8w0KRNj29C4r6GpSXk3Nh31lFFybKUj/JJvJ6ihHR4Q7Vmjt1XVOmjEZi6Dj1aE8o1gwpZoIY1F2hzyylGmGy5gZoJlrZuH3cwula5Z89YMkl/fvSNjmaGktVKc4KkzvPXCEabUnHTLM144ikWG2E0ujqTTwq7/KGKhxMSDzy5j2I5sk4dqxZ2ryL4Uph7aAJE4jBm94Hl6wXJnBasweWXPDTzgEN7LOHxalT6+DZ/LrF5toBDjQBhXhwwDwtkNRIIBOA4Z5YR2iSStyQz1yPPhn7xANPZ5rOAPvn5x2i0Pnq3j78TAMibn6xTOW4IBI4jhXqDh4wAN0T+Ibz+2HOsCzp1NOOufvnlFImAD6++EcItDgvnw9tr1gACS9/8PAs5bJiB7aJbFlIcAEg1qACM6t4xLRbJaS1XLU1BcDpR+kLrTbCpNAAkfDe+J8ia+p9YAKbVtBw4UwxuhQxGVM66wGicTVq50qH4jMkRXOuJOD11oOOQ08Y7lTRm2Pk1KvXGAARZ/CbxJ9MwX6eEUrmfh0b2+ce2lZ8sA4px5wGZ5MIpFdpVA6qvEmqepNfbx6PhES3ouKNDs/e26kJmynb8cuhamKDTzEMk7cs8zBaRmyxdJPXT5xhTUnkI5UIw4I6VlkaXaJBVQhsoW2NCXK11CQS2qshCe60QqMPiJzHNnsUy0KUXugVUo0SkfXhBe0N2LRKs5mNflEjvgEAHJwQ4fWNZuVskTLAg3wjvKmN+ZV4pvKOYCUgDIGusbzdTatiXZ5litUxCZk1K1qCjdT2QNxJdTXFUe4plAk0oYBM/P2zrC6wZgZKTUGjtly4xud05YImTlMpiFMdHLH9N4dPCJtnd0SkyjLUV3zMQcDUF0MzhQUl6/wCPQMp8tMnZM0sylIXXmUpYeA8ImRpBVsx20dsdrMWsWiYgEsALzMnuhWGKgLx4qMSM3LwiRfFGfJmhXNl2eTPs91V+YuWp6XbqL1MdVekC7A2gJM6+SwIKSWBYEirHlBO89plzkS5iMQAFe+fqYSyrNgL1TU0JowPU1whvTJTtGy3iTNUvu35hShjcQTQlwVBOdDXnGJtl4FlAg8QQfOPqm5a1yrHOUt75UxvYhISLo4Ur1jF7YtxWovC526L9ukmZaD7LZZkxLIQpTYsKDmcBFdoQDgG5Rot07aOzVJJar+MF0So2xFL2XOOCPNP1i07Knj/pL6C96QytM0ypjZQ7sFvpjEubRcccX2YpctSD3klP6gR6wWJlAdI+nbLmpmi6oAvCDevYstEtakoCVCvdDO1cM8IUc+6aLn6ZpWmY4rcV9/WC5M6FqZjUiyRQs75V0jos42gi0KKcffWLbE9KFg75D6wLMmFq1HJxy4xzJnFKWfo3PwgvYVodiWkHGlX6tn1gqyWhCfhN5TZUHE++EZ4zyRUnjWDbNgAT4ajjFWQ0O0hzeqAHDvlq558cINs852Ka1z5UjPWedzd8cWekNLIu6BUHiSK++EMkfInc8vfvWOJs+rE0Z3yhZ2xGbe8+EcrtTu1fbwANZU4EB/p7oIFtk2gAwqM9dIGE3DTLDGtAOmmUVTJ/Coy4+eucAFC099zTHUuGYj7xxaE01OubR5Nn4lvHDo1XaK5loSQXoOPywpABSpLkE5Vxo/H7x6CQHcEeAy4QOVMlyWBwx8cKe9YpEx+VT9+EIqiy0zur6eWMBrml2y9KccYsmHKuXv3rAypjlz9gOXKEykiubN8/GLZxYcoHcEjnHdqOA1MQzRFaR3hxHzisqon3pFuaTzgdZ8okZ3MNWhlu9tOXZ1rXMlCY8tSUAtRZIZT4igIcVrCqYe9Hi4APoWxbErap/uGSASgS5dACxIKlKUSQWz0MF7i7sWNdsXLnm/cCyxWq7NcJKAFgpYoxVQuSWoHjE7s7cmWSYVJqlabixmU6jRQy+8NZm3ZSCFy1KUoVAukMeJPyhbK0aPefeyXZZipVnSkdlPmXQU3kJYKTTvOSk4E/vlNt75TZ9n/lriRL7tW75u1PAOtz1aM9bLQpaiVFy5J4klyeZMUgwqQ+T6CkopEjhNsWKBvARIqyBrKlj+RUpq3jXqmGm7lmQESZrd8lYdzk9WyLUiRIpCHOzZ6v5e0f95UYu2q7xiRIxXbN5fygFajHEmcpJvJLERIkWZD62G/JStXxEPSKdmz1YPEiQvBfk2O7kw9onnDjelNWyIiRI5pdndD+T4/eYCLUrINIkSO08wvX6B48KBQ8vSJEiiTolh71guViBr9WiRIZDO0LIPh5w1s4BZ6s+PSJEiiX2WTlXsdflFdklhQc5NTKp0iRIBEtyiAWONThwpq0LplrWEJZR7yq9OXOJEhFIMtJ7r9OlPCAJkwhxl4xIkMSOJyjXkTFJWQSH0+cSJEllNqUXitZ7sSJCLRxJ+IdfSPZx7yesSJEMpHKzA4+USJCGeqxiKiRIBHqYsT84kSAAcx5EiRIyRIkSAD/2Q==",
                                   "subtitle" : "Get your gym & fitness bot today",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "Buy Template"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://m.me/566837733658925",
                                        "title": "Chat"
                                    },
                                    {
                                        "type": "element_share"
                                   }]
                                 }
                           ]
                       } 
                   }
                }
           ]
    } 
   };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting APPLICATION on port %d" % port)
    context.run(debug=True, port=port, host='0.0.0.0')