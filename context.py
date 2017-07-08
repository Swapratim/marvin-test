#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os
import psycopg2
import urlparse

from flask import Flask
from flask import request, render_template
from flask import make_response


# Flask should start in global layout
context = Flask(__name__)
# Facbook Access Token
#ACCESS_TOKEN = "EAAXRzkKCxVQBAImZBQo8kEpHVn0YDSVxRcadEHiMlZAcqSpu5pV7wAkZBKUs0eIZBcX1RmZCEV6cxJzuZAp5NO5ZCcJgZBJu4OPrFpKiAPJ5Hxlve2vrSthfMSZC3GqLnzwwRENQSzZAMyBXFCi1LtLWm9PhYucY88zPT4KEwcZCmhLYAZDZD"
ACCESS_TOKEN = "EAADCpnCTbUoBAMlgDxoEVTifvyD80zCxvfakHu6m3VjYVdS5VnbIdDnZCxxonXJTK2LBMFemzYo2a4DGrz0SxNJIFkMAsU8WBfRS7IRrZAaHRrXEMBEL5wmdUvzawASQWtZAMNBr90Gattw3IGzeJ7pZBBUthMewXDvnmBELCgZDZD"
# Google Access Token
Google_Acces_Toekn = "key=AIzaSyDNYsLn4JGIR4UaZMFTAgDB9gKN3rty2aM&cx=003066316917117435589%3Avcms6hy5lxs&q="
# NewsAPI Access Token
newspai_access_token = "505c1506aeb94ba69b72a4dbdce31996"
# Weather Update API KeyError
weather_update_key = "747d84ccfe063ba9"

#************************************************************************************#
#                                                                                    #
#    All Webhook requests lands within the method --webhook                          #
#                                                                                    #
#************************************************************************************#
# Webhook requests are coming to this method
@context.route('/webhook', methods=['POST'])
def webhook():
    reqContext = request.get_json(silent=True, force=True)
    #print(json.dumps(reqContext, indent=4))
    print(reqContext.get("result").get("action"))
    print ("webhook is been hit ONCE ONLY")
    if reqContext.get("result").get("action") == "input.welcome":
       return welcome()
    elif reqContext.get("result").get("action") == "weather":
       return weather(reqContext)
    elif reqContext.get("result").get("action") == "yahooWeatherForecast":
       return weatherhook(reqContext)
    elif reqContext.get("result").get("action") == "wikipedia":
       return wikipedia_search(reqContext)
    elif reqContext.get("result").get("action") == "GoogleSearch":
       return searchhook(reqContext)
    elif reqContext.get("result").get("action") == "wikipediaInformationSearch":
       return wikipediaInformationSearch(reqContext)
    elif reqContext.get("result").get("action") == "news.category":
       return newsCategory(reqContext)
    elif reqContext.get("result").get("action") == "topnews":
       return news_category_topnews(reqContext)
    elif reqContext.get("result").get("action") == "topfournewsarticle":
       return topFourNewsArticle(reqContext)
    else:
       print("Good Bye")

 
#************************************************************************************#
#                                                                                    #
#   This method is to get the Facebook User Deatails via graph.facebook.com/v2.6     #
#                                                                                    #
#************************************************************************************#
def welcome():
    print ("within welcome method")
    data = request.json
    print (data)
    if data is None:
        return {}
    entry = data.get('originalRequest')
    dataall = entry.get('data')
    sender = dataall.get('sender')
    id = sender.get('id')
    print ("id :" + id)
    fb_info = "https://graph.facebook.com/v2.6/" + id + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN
    print (fb_info)
    result = urllib.request.urlopen(fb_info).read()
    print (result)
    data = json.loads(result)
    first_name = data.get('first_name')
    print (first_name)
    speech = "I can provide News, Weather Report or Information search from Wikipedia"
    res = {
          "speech": speech,
          "displayText": speech,
           "data" : {
              "facebook" : [
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Hi " + first_name + "! I am Marvin",
                                   "image_url" : "https://pbs.twimg.com/profile_images/717482045019136001/aYzlNG5L.jpg",
                                 } 
                           ]
                       } 
                   }
                },
                 {
                 "text": speech
                  },
                 {
                  "text": "Click your choice:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "news",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   }
                  ]
                 }
                ]
               }
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
#   This method is to get the Facebook User Deatails via graph.facebook.com/v2.6     #
#                                                                                    #
#************************************************************************************#
def quickReply():
    res = {
          "speech": speech,
          "displayText": speech,
           "data" : {
              "facebook" : [
                  {
                  "text": "Click your choice:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "news",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   }
                  ]
                 }
                ]
               }
            };
    print (res)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print (r)
    return r

#************************************************************************************#
#                                                                                    #
#   Below method is to get the Facebook Quick Reply Webhook Handling - Weather       #
#                                                                                    #
#************************************************************************************#
def weather(reqContext):
    print (reqContext.get("result").get("action"))
    option = reqContext.get("result").get("action")
    res = {
        "speech": "Please provide the city name",
        "displayText": "Please provide the city name",
        "data" : {
        "facebook" : [
               {
                "text": "Please provide the city name"
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
#   Below 3 methods are to get the Yahoo Weather Report for a location via API       #
#                                                                                    #
#************************************************************************************#
def weatherhook(reqContext):
   #req = request.get_json(silent=True, force=True)
   result = reqContext.get("result")
   parameters = result.get("parameters")
   city = parameters.get("geo-city")
   if not parameters.get("geo-city"):
      city = parameters.get("geo-city-dk")
      #return 

   ###########################################################
   data = yahoo_weatherapi(city)
   #print (data)
   ############################################################
   query = data.get('query')
   if query is None:
       return {}

   result = query.get('results')
   if result is None:
       return {}

   channel = result.get('channel')
   if channel is None:
       return {}

   item = channel.get('item')
   location = channel.get('location')
   units = channel.get('units')
   if (location is None) or (item is None) or (units is None):
       return {}

   condition = item.get('condition')
   if condition is None:
       return {}

   #description = item.get('description')
   #if description is None:
   #    return {}
    
   #print ("URL Link and Condition code should be printed afterwards")
   link = item.get('link')
   link_forecast = link.split("*",1)[1]
   #print (link_forecast)
   #print ("<<<<<>>>>")
   #print (condition.get('code')) 
   condition_get_code = condition.get('code')
   condition_code = weather_code(condition_get_code)
   image_url = "http://gdurl.com/" + condition_code

   #if condition.get('code') != condition_code:
   #   image_url = "http://l.yimg.com/a/i/us/we/" + condition.get('code') + "/14.gif"
   #print (image_url) 
    
   speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
            ", the temperature is " + condition.get('temp') + " " + units.get('temperature')
   #print ("City - Country: " +location.get('city') + "-" + location.get('country'))
   #print ("image url: " + image_url)
   #print ("forecast link: " + link_forecast)
   #print("speech: " + speech)
   ##############################################################
   #res = {"speech": speech,
   #       "displayText": speech,
   #       "source": "apiai-weather-webhook-sample"}
   res = {
         "speech": speech,
         "displayText": speech,
          "data" : {
             "facebook" : [
                 {
                "text": speech
                 },
                 {
                "attachment" : {
                  "type" : "template",
                    "payload" : {
                     "template_type" : "generic",
                      "elements" : [ 
                                {
                                  "title" : location.get('city') + "-" + location.get('country'),
                                  "image_url" : image_url,
                                  "subtitle" : "",
                                  "buttons": [{
                                       "type": "web_url",
                                       "url": link_forecast,
                                       "title": "Weather Forecast"
                                   }]
                                 } 
                          ]
                      } 
                  }
                }
              ]
            } 
        };
   print (res)
   res = json.dumps(res, indent=4)
   r = make_response(res)
   r.headers['Content-Type'] = 'application/json'
   print ("City - Country: " +location.get('city') + "-" + location.get('country'))
   return r

def yahoo_weatherapi(city):

    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "') and u='c'"
    if yql_query is None:
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_url = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
    #print (yql_url)
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    return data

def weather_code(condition_get_code):
# Below block of code is to check for weather condition code and map corresponding http://gdurl.com/#### permalink context

    if condition_get_code == "0":
       condition_code = "EmPG"
    elif condition_get_code == "1":
       condition_code = "mh7N"
    elif condition_get_code == "2":
       condition_code = "jENO"
    elif condition_get_code == "3":
       condition_code = "BTT7"
    elif condition_get_code == "4":
       condition_code = "kTWn"
    elif condition_get_code == "5":
       condition_code = "vBIX"
    elif condition_get_code == "6":
       condition_code = "zuxw"
    elif condition_get_code == "7":
       condition_code = "Vy9A"
    elif condition_get_code == "8":
       condition_code = "cT-0"
    elif condition_get_code == "9":
       condition_code = "M4nr"
    elif condition_get_code == "10":
       condition_code = "8-OZ"
    elif condition_get_code == "11":
       condition_code = "4sN0"
    elif condition_get_code == "12":
       condition_code = "SrHt"
    elif condition_get_code == "13":
       condition_code = "i925"
    elif condition_get_code == "14":
       condition_code = "9WKu"
    elif condition_get_code == "15":
       condition_code = "YjI9B"
    elif condition_get_code == "16":
       condition_code = "Lqmw"
    elif condition_get_code == "17":
       condition_code = "8wXj"
    elif condition_get_code == "18":
       condition_code = "AHL1"
    elif condition_get_code == "19":
       condition_code = "pSfX"
    elif condition_get_code == "20":
       condition_code = "ugKj"
    elif condition_get_code == "21":
       condition_code = "eFL0"
    elif condition_get_code == "22":
       condition_code = "Co_g" 
    elif condition_get_code == "23":
       condition_code = "h8uM"
    elif condition_get_code == "24":
       condition_code = "HBlw"
    elif condition_get_code == "25":
       condition_code = "QHzi"
    elif condition_get_code == "26":
       condition_code = "3IaA"
    elif condition_get_code == "27":
       condition_code = "i-dK"
    elif condition_get_code == "28":
       condition_code = "aIAw"
    elif condition_get_code == "29":
       condition_code = "6z8CS"
    elif condition_get_code == "30":
       condition_code = "xt2C"
    elif condition_get_code == "31":
       condition_code = "3Utr"
    elif condition_get_code == "32":
       condition_code = "YHpS"
    elif condition_get_code == "33":
       condition_code = "Hr4W"
    elif condition_get_code == "34":
       condition_code = "84WQ"
    elif condition_get_code == "35":
       condition_code = "3BH6"
    elif condition_get_code == "36":
       condition_code = "vjLN"
    elif condition_get_code == "37":
       condition_code = "41rl"
    elif condition_get_code == "38":
       condition_code = "8Ibx" 
    elif condition_get_code == "39":
       condition_code = "lIee"
    elif condition_get_code == "40":
       condition_code = "9GNz"
    elif condition_get_code == "41":
       condition_code = "uy77"
    elif condition_get_code == "42":
       condition_code = "15Ou"
    elif condition_get_code == "43":
       condition_code = "P_Jg"
    elif condition_get_code == "45":
       condition_code = "wF0D"
    elif condition_get_code == "46":
       condition_code = "1huQ"
    elif condition_get_code == "47":
       condition_code = "MlO5"
    elif condition_get_code == "3200":
       condition_code = "mgzs"
    else: 
       print ("Condition code did not match the sequence")

    return condition_code

#************************************************************************************#
#                                                                                    #
#   Below method is to get the Facebook Quick Reply Webhook Handling - Wikipedia     #
#                                                                                    #
#************************************************************************************#
def wikipedia_search(reqContext):
    print (reqContext.get("result").get("action"))
    option = reqContext.get("result").get("action")
    res = {
        "speech": "Please provide the topic you want to search in Wikipedia",
        "displayText": "Please provide the topic you want to search in Wikipedia",
        "data" : {
        "facebook" : [
               {
                "text": "Please ask a question you want to search in Wikipedia"
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
#   This method is to get the Wikipedia Information via Google API                   #
#                                                                                    #
#************************************************************************************#
# Searchhook is for searching for Wkipedia information via Google API
def searchhook(reqContext):
    req = request.get_json(silent=True, force=True)
    print("Within Search function......!!")
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    print ("resolvedQuery: " + resolvedQuery)
    true_false = True
    baseurl = "https://www.googleapis.com/customsearch/v1?"
###########################################################
    result = req.get("result")
    parameters = result.get("parameters")
    search_list0 = parameters.get("any")
    #print ("search_list0" + search_list0)
    search_u_string_removed = [str(i) for i in search_list0]
    search_list1 = str(search_u_string_removed)
    #print ("search_list1" + search_list1)
    cumulative_string = search_list1.strip('[]')
    search_string = cumulative_string.replace(" ", "%20")
    print(search_string)
    search_string_ascii = search_string.encode('ascii')
    if search_string_ascii is None:
        return None
    google_query = "key=AIzaSyDNYsLn4JGIR4UaZMFTAgDB9gKN3rty2aM&cx=003066316917117435589%3Avcms6hy5lxs&q=" + search_string_ascii + "&num=1"
###########################################################
    if google_query is None:
        return {}
    #google_url = baseurl + urllib.parse.urlencode({google_query})
    google_url = baseurl + google_query
    print("google_url::::"+google_url)
    result = urllib.request.urlopen(google_url).read()
    #print (result)
    data = json.loads(result)
    print ("data = json.loads(result)")
############################################################
    speech = data['items'][0]['snippet'].encode('utf-8').strip()
    for data_item in data['items']:
        link = data_item['link'],

    for data_item in data['items']:
        pagemap = data_item['pagemap'],

    cse_thumbnail_u_string_removed = [str(i) for i in pagemap]
    cse_thumbnail_u_removed = str(cse_thumbnail_u_string_removed)
    cse_thumbnail_brace_removed_1 = cse_thumbnail_u_removed.strip('[')
    cse_thumbnail_brace_removed_2 = cse_thumbnail_brace_removed_1.strip(']')
    cse_thumbnail_brace_removed_final =  cse_thumbnail_brace_removed_2.strip("'")
    print (cse_thumbnail_brace_removed_final)
    keys = ('cse_thumbnail', 'metatags', 'cse_image')
    for key in keys:
        # print(key in cse_thumbnail_brace_removed_final)
        print ('cse_thumbnail' in cse_thumbnail_brace_removed_final)
        true_false = 'cse_thumbnail' in cse_thumbnail_brace_removed_final
        if true_false == True:
            print ('Condition matched -- Within IF block')
            for key in pagemap:
                cse_thumbnail = key['cse_thumbnail']
                print ('Within the For loop -- cse_thumbnail is been assigned')
                for image_data in cse_thumbnail:
                    raw_str = image_data['src']
                    print ('raw_str::: ' + raw_str)
                    print ('***TRUE***')
                    break
        else:
            raw_str = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwdc3ra_4N2X5G06Rr5-L0QY8Gi6SuhUb3DiSN_M-C_nalZnVA"
            print ('***FALSE***') 
    
    
    src_brace_removed_final = raw_str
    # Remove junk charaters from URL
    link_u_removal =  [str(i) for i in link]
    link_u_removed = str(link_u_removal)
    link_brace_removed_1 = link_u_removed.strip('[')
    link_brace_removed_2 = link_brace_removed_1.strip(']')
    link_final =  link_brace_removed_2.strip("'")
    # Remove junk character from search item
    search_string_final = cumulative_string.strip("'")
    print ("Image::::::::")
    print (src_brace_removed_final)
    print ("link_final....")
    print (link_final)
    print("Response:")
    print(speech)
############################################################
    res = {
          "speech": speech,
          "displayText": speech,
           "data" : {
              "facebook" : [
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : search_string_final,
                                   "image_url" : src_brace_removed_final,
                                   "subtitle" : "",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": link_final,
                                        "title": "More info"
                                    }]
                                 } 
                           ]
                       } 
                   }
                },
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
#   This method is to get the Wikipedia Information via Google API                   #
#                                                                                    #
#************************************************************************************#
# Searchhook is for searching for Wkipedia information via Google API
def wikipediaInformationSearch(reqContext):
    req = request.get_json(silent=True, force=True)
    print("Within Search function......!!")
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    print ("resolvedQuery: " + resolvedQuery)
    true_false = True
    baseurl = "https://www.googleapis.com/customsearch/v1?"
    resolvedQueryFinal = resolvedQuery.replace(" ", "%20")
    print(resolvedQueryFinal)
    search_string_ascii = resolvedQueryFinal.encode('ascii')
    if search_string_ascii is None:
        return None
    google_query = "key=AIzaSyDNYsLn4JGIR4UaZMFTAgDB9gKN3rty2aM&cx=003066316917117435589%3Avcms6hy5lxs&q=" + search_string_ascii + "&num=1"
###########################################################
    if google_query is None:
        return {}
    google_url = baseurl + google_query
    print("google_url::::"+google_url)
    result = urllib.request.urlopen(google_url).read()
    data = json.loads(result)
    print ("data = json.loads(result)")
############################################################
    speech = data['items'][0]['snippet'].encode('utf-8').strip()
    for data_item in data['items']:
        link = data_item['link'],

    for data_item in data['items']:
        pagemap = data_item['pagemap'],

    cse_thumbnail_u_string_removed = [str(i) for i in pagemap]
    cse_thumbnail_u_removed = str(cse_thumbnail_u_string_removed)
    cse_thumbnail_brace_removed_1 = cse_thumbnail_u_removed.strip('[')
    cse_thumbnail_brace_removed_2 = cse_thumbnail_brace_removed_1.strip(']')
    cse_thumbnail_brace_removed_final =  cse_thumbnail_brace_removed_2.strip("'")
    print (cse_thumbnail_brace_removed_final)
    keys = ('cse_thumbnail', 'metatags', 'cse_image')
    for key in keys:
        # print(key in cse_thumbnail_brace_removed_final)
        print ('cse_thumbnail' in cse_thumbnail_brace_removed_final)
        true_false = 'cse_thumbnail' in cse_thumbnail_brace_removed_final
        if true_false == True:
            print ('Condition matched -- Within IF block')
            for key in pagemap:
                cse_thumbnail = key['cse_thumbnail']
                print ('Within the For loop -- cse_thumbnail is been assigned')
                for image_data in cse_thumbnail:
                    raw_str = image_data['src']
                    print ('raw_str::: ' + raw_str)
                    print ('***TRUE***')
                    break
        else:
            raw_str = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwdc3ra_4N2X5G06Rr5-L0QY8Gi6SuhUb3DiSN_M-C_nalZnVA"
            print ('***FALSE***') 
    
    
    src_brace_removed_final = raw_str
    # Remove junk charaters from URL
    link_u_removal =  [str(i) for i in link]
    link_u_removed = str(link_u_removal)
    link_brace_removed_1 = link_u_removed.strip('[')
    link_brace_removed_2 = link_brace_removed_1.strip(']')
    link_final =  link_brace_removed_2.strip("'")
    # Remove junk character from search item
    search_string_final = cumulative_string.strip("'")
    print ("Image::::::::")
    print (src_brace_removed_final)
    print ("link_final....")
    print (link_final)
    print("Response:")
    print(speech)
############################################################
    res = {
          "speech": speech,
          "displayText": speech,
           "data" : {
              "facebook" : [
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : search_string_final,
                                   "image_url" : src_brace_removed_final,
                                   "subtitle" : "",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": link_final,
                                        "title": "More info"
                                    }]
                                 } 
                           ]
                       } 
                   }
                },
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
#   Below method is to get the Facebook Quick Reply Webhook Handling - NEWS          #
#                                                                                    #
#************************************************************************************#
def newsCategory(reqContext):
    print (reqContext.get("result").get("action"))
    #option = reqContext.get("result").get("action")
    res = {
            "speech": "Please select the category",
            "displayText": "Please select the category",
            "data" : {
            "facebook" : [
                 {
                  "text": "Select your choice:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Top News",
                  "payload": "topnews",
                  "image_url": "https://previews.123rf.com/images/alexwhite/alexwhite1209/alexwhite120900529/15471651-news-icon-Stock-Photo-icons.jpg"
                  },
                 {
                  "content_type": "text",
                  "title": "Sports",
                  "payload": "sports",
                  "image_url": "http://thebridgeconference.com/wp-content/uploads/2014/05/main_paragraph_icon.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Finance",
                  "payload": "business",
                  "image_url": "http://www.22traders.com/wp-content/uploads/2014/09/statistics-market-icon11.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Technology",
                  "payload": "technology",
                  "image_url": "https://cdn.pixabay.com/photo/2015/12/04/22/20/gear-1077550_640.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Entertainment",
                  "payload": "entertainment",
                  "image_url": "https://userscontent2.emaze.com/images/2afc7b67-eba3-41c8-adce-b1e2b1c34b02/99782968e977045b1f88f94d0c4e00cf.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Science & Nature",
                  "payload": "science",
                  "image_url": "https://previews.123rf.com/images/sasigallery/sasigallery1510/sasigallery151000046/46507337-Atom-with-nature-Science-Environmental-Protection-Icon-symbol-design-Vector-illustration--Stock-Vector.jpg"
                  }
                  ]
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
#   Below method is to get the provide News Category Quick Replies - Top News        #
#                                                                                    #
#************************************************************************************#
def news_category_topnews(reqContext):
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    print ("resolvedQuery: " + resolvedQuery)
    if resolvedQuery == "topnews":
        res = {
            "speech": "Please select the Newspaper",
            "displayText": "Please select the Newspaper",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please Select Newspaper:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "The Times Of India",
                  "payload": "the-times-of-india",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGUM0uhwsV3vp9ZzMEnjJo4MDZRSC3cgp32qH64zZlWFsAiGNv"
                  },
                 {
                  "content_type": "text",
                  "title": "BBC News",
                  "payload": "bbc-news",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWrLeudSaMDHDclbCjfvVoOdIK9q3XKqbWG5G1aDJzO3z6YZUP"
                  },
                  {
                  "content_type": "text",
                  "title": "CNN",
                  "payload": "cnn",
                  "image_url": "https://qph.ec.quoracdn.net/main-qimg-583846beabeef96102a6f18fc2096a82-c"
                  },
                  {
                  "content_type": "text",
                  "title": "Time",
                  "payload": "time",
                  "image_url": "https://s0.wp.com/wp-content/themes/vip/time2014/img/time-touch_icon_152.png"
                  },
                  {
                  "content_type": "text",
                  "title": "USA Today",
                  "payload": "usa-today",
                  "image_url": "http://www.gmkfreelogos.com/logos/U/img/U_Bahn.gif"
                  },
                  {
                  "content_type": "text",
                  "title": "The Telegraph",
                  "payload": "the-telegraph",
                  "image_url": "https://media.glassdoor.com/sqll/700053/the-telegraph-calcutta-squarelogo-1475068747795.png"
                  },
                  {
                  "content_type": "text",
                  "title": "The Washington Post",
                  "payload": "the-washington-post",
                  "image_url": "https://static1.squarespace.com/static/58505df4579fb348904cdf5f/t/58ab141b20099e74879fe27f/1487606851497/wp.jog"
                  },
                  {
                  "content_type": "text",
                  "title": "The Guardian (UK)",
                  "payload": "the-guardian-uk",
                  "image_url": "http://a2.mzstatic.com/eu/r30/Purple62/v4/0b/a9/56/0ba956de-3621-3585-285e-1141b53d4d51/icon175x175.png"
                  },
                  {
                  "content_type": "text",
                  "title": "The Guardian (AU)",
                  "payload": "the-guardian-au",
                  "image_url": "http://a2.mzstatic.com/eu/r30/Purple62/v4/0b/a9/56/0ba956de-3621-3585-285e-1141b53d4d51/icon175x175.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Reuters",
                  "payload": "reuters",
                  "image_url": "http://www.adweek.com/wp-content/uploads/sites/9/2013/09/reuters-logo.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "The Hindu",
                  "payload": "the-hindu",
                  "image_url": "https://lh4.ggpht.com/_wAwneNQFfcruC-YiUpWKPtBTpzfdqLVTIArJyYRt52xGm4ABVQKT5eeLb_rl6em42kO=w300"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "sports":
        res = {
            "speech": "Please select the Newspaper",
            "displayText": "Please select the Newspaper",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please Select Newspaper:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "ESPN",
                  "payload": "espn",
                  "image_url": "https://www.brandsoftheworld.com/sites/default/files/styles/logo-thumbnail/public/052016/untitled-1_242.png?itok=vy3l2HxD"
                  },
                 {
                  "content_type": "text",
                  "title": "ESPN Cric Info",
                  "payload": "espn-cric-info",
                  "image_url": "http://topnews.ae/images/ESPNcricinfo.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "BBC Sport",
                  "payload": "bbc-sport",
                  "image_url": "http://yellingperformance.com/wp-content/uploads/2014/08/bbc-sport.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Fox Sports",
                  "payload": "fox-sports",
                  "image_url": "data:image/jpeg;base64,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"
                  },
                  {
                  "content_type": "text",
                  "title": "The Sport Bible",
                  "payload": "the-sport-bible",
                  "image_url": "https://pbs.twimg.com/profile_images/528682495923859456/yuXwYzR4.png"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "business":
        res = {
            "speech": "Please select the Newspaper",
            "displayText": "Please select the Newspaper",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please Select Newspaper:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "The Economist",
                  "payload": "the-economist",
                  "image_url": "https://gs-img.112.ua/original/2016/04/01/221445.jpg"
                  },
                 {
                  "content_type": "text",
                  "title": "Financial Times",
                  "payload": "financial-times",
                  "image_url": "http://www.adweek.com/wp-content/uploads/sites/10/2014/03/financial_times_logo304x200.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "CNBC",
                  "payload": "cnbc",
                  "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/CNBC_logo.svg/961px-CNBC_logo.svg.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Business Insider",
                  "payload": "business-insider",
                  "image_url": "https://pbs.twimg.com/profile_images/661313209605976064/EjEK7KeO.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "Fortune",
                  "payload": "fortune",
                  "image_url": "https://fortunedotcom.files.wordpress.com/2014/05/f_icon_orange_1.png"
                  },
                  {
                  "content_type": "text",
                  "title": "The Wall Street Journal",
                  "payload": "the-wall-street-journal",
                  "image_url": "https://www.wsj.com/apple-touch-icon.png"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "technology":
        res = {
            "speech": "Please select the Newspaper",
            "displayText": "Please select the Newspaper",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please Select Newspaper:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "TechRadar",
                  "payload": "techradar",
                  "image_url": "http://www.ittiam.com/vividhdr/img/techradar.jpg"
                  },
                 {
                  "content_type": "text",
                  "title": "TechCrunch",
                  "payload": "techcrunch",
                  "image_url": "https://tctechcrunch2011.files.wordpress.com/2014/04/tc-logo.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "T3N",
                  "payload": "t3n",
                  "image_url": "https://pbs.twimg.com/profile_images/2267864145/8oalkkbzq6davn5snoi4.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Hacker News",
                  "payload": "hacker-news",
                  "image_url": "https://pbs.twimg.com/profile_images/659012257985097728/AXXMa-X2.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Buzzfeed",
                  "payload": "buzzfeed",
                  "image_url": "https://static-s.aa-cdn.net/img/ios/352969997/d5f0fe265f21af1cffd41964bc7b46ab"
                  },
                  {
                  "content_type": "text",
                  "title": "Recode",
                  "payload": "recode",
                  "image_url": "https://cdn.vox-cdn.com/uploads/hub/sbnu_logo/633/large_mark.64395.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Reddit",
                  "payload": "reddit",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCOC1gOn12VNBdquLlqxTCt9XGF_vWiF3Y3gjfnCxCBIN_FXdZ"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "entertainment":
        res = {
            "speech": "Please select the Newspaper",
            "displayText": "Please select the Newspaper",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please Select Newspaper:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Entertainment Weekly",
                  "payload": "entertainment-weekly",
                  "image_url": "https://i.redd.it/ndughnbltu2z.png"
                  },
                 {
                  "content_type": "text",
                  "title": "MTV News",
                  "payload": "mtv-news",
                  "image_url": "http://imagesmtv-a.akamaihd.net/uri/mgid:file:http:shared:mtv.com/news/wp-content/uploads/2016/07/staff-author-250-1468362828.png?format=jpg&quality=.8"
                  },
                  {
                  "content_type": "text",
                  "title": "MTV News (UK)",
                  "payload": "mtv-news-uk",
                  "image_url": "http://imagesmtv-a.akamaihd.net/uri/mgid:file:http:shared:mtv.com/news/wp-content/uploads/2016/07/staff-author-250-1468362828.png?format=jpg&quality=.8"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "science":
        res = {
            "speech": "Please select the Newspaper",
            "displayText": "Please select the Newspaper",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please Select Newspaper:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "National Geographic",
                  "payload": "national-geographic",
                  "image_url": "https://pbs.twimg.com/profile_images/798181194202566656/U8QbCBdH_400x400.jpg"
                  },
                 {
                  "content_type": "text",
                  "title": "New Scientist",
                  "payload": "new-scientist",
                  "image_url": "http://www.peteraldhous.com/Images/ns.jpg"
                  }
                  ]
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
#   Below method is to get the News Details in JSON Format and put as List Template  #
#                                                                                    #
#************************************************************************************#
newspaper_url = ''
data = ''
def topFourNewsArticle(reqContext):
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    print ("resolvedQuery: " + resolvedQuery)
    newsAPI = "https://newsapi.org/v1/articles?source=" + resolvedQuery + "&sortBy=top&apiKey=" + newspai_access_token
    result = urllib.request.urlopen(newsAPI).read()
    data = json.loads(result)
    newspaper_url = newsWebsiteIdentification(resolvedQuery)
    print ("newspaper_url finally: " + newspaper_url)
    res = {
            "speech": "Please select the Newspaper",
            "displayText": "Please select the Newspaper",
            "data" : {
            "facebook" : [
                 {
                "attachment" : {
                  "type" : "template",
                    "payload" : {
                     "template_type" : "list",
                     "elements" : [ 
                        {
                            "title": data['articles'][0]['title'],
                            "image_url": data['articles'][0]['urlToImage'],
                            "default_action": {
                               "type": "web_url",
                               "url": data['articles'][0]['url'],
                                "webview_height_ratio": "tall",
                                },
                            "buttons": [
                            {
                               "title": "Read Article",
                               "type": "web_url",
                               "url": data['articles'][0]['url'],
                               "webview_height_ratio": "tall",
                            }
                          ]
                        },
                        {
                            "title": data['articles'][1]['title'],
                            "image_url": data['articles'][1]['urlToImage'],
                            "subtitle": data['articles'][1]['description'],
                            "default_action": 
                                {
                                    "type": "web_url",
                                    "url": data['articles'][1]['url'],
                                    "webview_height_ratio": "tall"
                                },
                                "buttons": [
                                {
                                     "title": "Read Article",
                                     "type": "web_url",
                                     "url": data['articles'][1]['url'],
                                     "webview_height_ratio": "tall"
                                }
                               ]
                        },
                        {
                            "title": data['articles'][2]['title'],
                            "image_url": data['articles'][2]['urlToImage'],
                            "subtitle": data['articles'][2]['description'],
                            "default_action": 
                               {
                                   "type": "web_url",
                                   "url": data['articles'][2]['url'],
                                   "webview_height_ratio": "tall"
                                },
                                "buttons": [
                                {
                                   "title": "Read Article",
                                   "type": "web_url",
                                   "url": data['articles'][2]['url'],
                                   "webview_height_ratio": "tall"
                                }
                              ]
                       },
                       {
                            "title": data['articles'][3]['title'],
                            "image_url": data['articles'][3]['urlToImage'],
                            "subtitle": data['articles'][3]['description'],
                            "default_action": 
                            {
                                "type": "web_url",
                                "url": data['articles'][3]['url'],
                                "webview_height_ratio": "tall"
                            },
                            "buttons": [
                            {
                                "title": "Read Article",
                                "type": "web_url",
                                "url": data['articles'][3]['url'],
                                "webview_height_ratio": "tall"
                            }
                           ]
                        }
                        ],
                        "buttons": [
                         {
                            "title": "View Site",
                            "type": "web_url",
                            "url": newspaper_url
                        }
                       ]  
                     } 
                   }
                 }
               ]
             } 
           };
    #print (res)
    res = json.dumps(res, indent=4)
    print (res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


#************************************************************************************#
#                                                                                    #
#   Identifying Newspaper Website                                                    #
#                                                                                    #
#************************************************************************************#
def newsWebsiteIdentification(resolvedQuery):

    if resolvedQuery == "the-times-of-india":
       newspaper_url = "http://timesofindia.indiatimes.com"
    elif resolvedQuery == "bbc-news":
       newspaper_url = "http://www.bbc.com/news"
    elif resolvedQuery == "cnn":
       newspaper_url = "http://edition.cnn.com"
    elif resolvedQuery == "time":
       newspaper_url = "http://time.com"
    elif resolvedQuery == "usa-today":
       newspaper_url = "https://www.usatoday.com"
    elif resolvedQuery == "the-telegraph":
       newspaper_url = "http://www.telegraph.co.uk"
    elif resolvedQuery == "the-washington-post":
       newspaper_url = "https://www.washingtonpost.com"
    elif resolvedQuery == "the-guardian-uk":
       newspaper_url = "https://www.theguardian.com/uk"
    elif resolvedQuery == "the-guardian-au":
       newspaper_url = "https://www.theguardian.com/au"
    elif resolvedQuery == "reuters":
       newspaper_url = "http://www.reuters.com"
    elif resolvedQuery == "the-hindu":
       newspaper_url = "http://www.thehindu.com"
    elif resolvedQuery == "espn":
       newspaper_url = "http://espn.go.com"
    elif resolvedQuery == "espn-cric-info":
       newspaper_url = "http://www.espncricinfo.com"
    elif resolvedQuery == "bbc-sport":
       newspaper_url = "http://www.bbc.com/sport"
    elif resolvedQuery == "fox-sports":
       newspaper_url = "http://www.foxsports.com"
    elif resolvedQuery == "the-sport-bible":
       newspaper_url = "http://www.sportbible.com"
    elif resolvedQuery == "the-economist":
       newspaper_url = "https://www.economist.com"
    elif resolvedQuery == "financial-times":
       newspaper_url = "https://www.ft.com"
    elif resolvedQuery == "cnbc":
       newspaper_url = "http://www.cnbc.com"
    elif resolvedQuery == "business-insider":
       newspaper_url = "http://nordic.businessinsider.com"
    elif resolvedQuery == "fortune":
       newspaper_url = "http://fortune.com"
    elif resolvedQuery == "the-wall-street-journal":
       newspaper_url = "https://www.wsj.com"
    elif resolvedQuery == "techradar":
       newspaper_url = "http://www.techradar.com"
    elif resolvedQuery == "techcrunch":
       newspaper_url = "https://techcrunch.com"
    elif resolvedQuery == "t3n":
       newspaper_url = "http://t3n.de"
    elif resolvedQuery == "hacker-news":
       newspaper_url = "http://thehackernews.com"
    elif resolvedQuery == "buzzfeed":
       newspaper_url = "https://www.buzzfeed.com"
    elif resolvedQuery == "entertainment-weekly":
       newspaper_url = "http://ew.com"
    elif resolvedQuery == "mtv-news":
       newspaper_url = "http://www.mtv.com"
    elif resolvedQuery == "mtv-news-uk":
       newspaper_url = "http://www.mtv.co.uk/news"
    elif resolvedQuery == "national-geographic":
       newspaper_url = "http://www.nationalgeographic.com"
    elif resolvedQuery == "new-scientist":
       newspaper_url = "https://www.newscientist.com"
    else: 
       print ("Newspaper name did not match the input")

    print ("Within newsWebsiteIdentification Method, the newspaper_url is: " + newspaper_url)
    return newspaper_url  
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting APPLICATION on port %d" % port)
    context.run(debug=True, port=port, host='0.0.0.0')