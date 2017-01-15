import os
import sys
import json
import config
import random
import requests

from mapping_folder import mapping
from random import randint
from datetime import datetime
from flask import Flask, request
from bs4 import BeautifulSoup

random.seed(datetime.now())

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            os.pardir
        )
    )
    import apiai

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', config.VERIFY_TOKEN)
CLIENT_ACCESS_TOKEN = os.environ.get('CLIENT_ACCESS_TOKEN', config.CLIENT_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    try:
       if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200

    except Exception as e:
        print ("Error : ", str(e))

    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():

    try:
        data = request.get_json()

        if data["object"] == "page":

            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:

                    if messaging_event.get("message"):  # someone sent us a message

                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                        if "text" in messaging_event["message"]:
                            message_text = messaging_event["message"]["text"]   # the message's text
                            postback_text = messaging_event["message"]["text"]

                        elif "sticker_id" in messaging_event["message"]:
                            if messaging_event["message"]["sticker_id"] == 369239263222822:     #thumbs_up_sticker
                                attachment_message = "Thanks for the thumbs up! Please tell all your friends - I'd love to meet them too. ^_^"
                            else:
                                attachment_message = "Thanks! Once I know you better, I will start reading anything that you share and your mind too. :P Till then, I can give you relevant information about the books present in the KGP Central Library. Just type HELP to get a list of the allowed inputs."

                            send_message_text(sender_id, attachment_message)
                            return "ok", 200

                        elif "attachments" in messaging_event["message"] :
                            attachment_message = "Thanks! Once I know you better, I will start reading anything that you share and your mind too. :P Till then, I can give you relevant information about the books present in the KGP Central Library. Just type HELP to get a list of the allowed inputs."
                            send_message_text(sender_id, attachment_message)
                            return "ok", 200

                        else:
                            send_message_text(sender_id, "Uh oh! I didn't quite get what you said. But, I can give you relevant information about the books present in the KGP Central Library. Just type HELP to get a list of the allowed inputs.")
                            return "ok",200

                        if postback_text == "Yes":
                            postback_payload = messaging_event["message"]["quick_reply"]["payload"]
                            if postback_payload == "yes_interested":
                                bot_response = "That's great! Please tell me book details."
                                send_message_text(sender_id, bot_response)
                                return "ok", 200

                        elif postback_text == "No":
                            postback_payload = messaging_event["message"]["quick_reply"]["payload"]
                            if postback_payload == "no_interested":
                                bot_response = "Alright :) You can type HELP any time to get a complete list of the inputs allowed."
                                send_message_text(sender_id, bot_response)
                                return "ok", 200

                        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

                        request_api = ai.text_request()
                        request_api.query = postback_text.lower()

                        response = json.loads(request_api.getresponse().read())     #this response is generated automatically by API.AI based on the training given earlier

                        result = response['result']
                        action = result['action']

                        # print "Action  : " + str(action)

                        if action == "hi_greeting_action":
                            send_message_quick_reply_about(sender_id)

                        elif action == "help_action":
                            bot_response = "1. find the book <book_name> written by <author_name>\n2. check books on <subject_name>\n3. check the book with ISBN <isbn_value>"
                            send_message_text(sender_id, bot_response)

                        elif action == "ask_name_action":
                            bot_response = "My name is KitabiKeeda. I am your personal assistant to help you browse through books in IIT Kharagpur Central Library. ^_^"
                            send_message_text(sender_id, bot_response)

                        elif action == "ask_job_action":
                            bot_response = "You can tell me the subject, author or book that you are interested in and I'll show you the relevant information right away!"
                            send_message_text(sender_id, bot_response)
                            send_message_quick_reply_yes_no_interested_now(sender_id)

                        elif action == "get_book_details_action":
                            book_title_value = response['result']['parameters']['book_title']
                            book_author_value = response['result']['parameters']['book_author']
                            fb_data = scrape_acc_to_title_and_author(book_title_value, book_author_value)
                            # print ("fb_data -> ", fb_data)
                            # print ("API response ->", response)
                            send_message_carousel(sender_id, fb_data)

                        elif action == "find_book_by_isbn_action":
                            isbn_value = response['result']['parameters']['book_isbn']
                            fb_data = scrape_acc_to_isbn(isbn_value)
                            send_message_carousel(sender_id, fb_data)

                        elif action == "get_books_by_subject_action":
                            subject_value = response['result']['parameters']['book_subject']
                            fb_data = scrape_acc_to_subject(subject_value)
                            send_message_carousel(sender_id, fb_data)

                        elif action == "bye_action":
                            bot_response = "See you later! Please tell your friends that I'd like to meet them too! ^_^"
                            send_message_text(sender_id, bot_response)

                        elif action == "fallback_action":
                            # print ("API response ->", response)
                            bot_response = "Sorry, I didn't get that! :("
                            send_message_text(sender_id, bot_response)

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        sender_id = messaging_event["sender"]["id"]
                        payload_value =  messaging_event["postback"]["payload"]

                        if payload_value != "USER_DEFINED_PAYLOAD":
                            book_avail_details = check_available(payload_value)
                            if book_avail_details[2] == 0:
                                bot_response = "Oops! All copies of the books are already issued! :( May be you should try later."
                                send_message_text(sender_id, bot_response)
                            elif book_avail_details[2] >= 0:
                                bot_response = "Awesome! I found " + str(book_avail_details[2]) + " copies of the book on the shelf right now."
                                num1 = get_shelf_by_id(payload_value)
                                mapping.main_function(num1)
                                send_message_text(sender_id, bot_response)
                                send_message_download_button(sender_id)
                            else:
                                bot_response = "Oops! Book details not found in database! :("
                                send_message_text(sender_id, bot_response)
                            return "ok", 200

                        # r = requests.get("https://graph.facebook.com/v2.6/" + str(sender_id) + "?fields=first_name,last_name,locale,gender,timezone,profile_pic&access_token=" + str(ACCESS_TOKEN))
                        # object_json = r.json()
                        # greeting = "Hi " + str(object_json["first_name"]) +" "+ str(object_json["last_name"]) + "! :) \nNice to meet you. My name is KitabiKeeda. I'm your personal assistant to help you to browse through the books in the KGP Central Library. ^_^ I'll provide you all the relevant information about the books that you might be interested in."
                        greeting = "Hi! :) \nNice to meet you. My name is KitabiKeeda. I'm your personal assistant to help you to browse through the books in the KGP Central Library. ^_^ I'll provide you all the relevant information about the books that you might be interested in."
                        # gender_val = 1
                        # if str(object_json["gender"]) == "female":
                        #     gender_val = 2
                        send_message_text(sender_id, greeting)

    except Exception as e:
        print ("Error : ", str(e))

    return "ok", 200

def send_message_quick_reply_about(recipient_id):
    try:
        text_to_show = "Hi!"
        params = {
            "access_token": ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": text_to_show,
                "quick_replies":[
                  {
                    "content_type":"text",
                    "title":"What's your name?",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                  },
                  {
                    "content_type":"text",
                    "title":"What can you do?",
                    "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                  }
                ]
            }
          })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    except Exception as e:
        print ("Error : ", str(e))

def send_message_text(recipient_id, message_text):
    try:
        params = {
            "access_token": ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
          })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    except Exception as e:
        print ("Error : ", str(e))

def send_message_download_button(recipient_id):
    try:
        params = {
        "access_token": ACCESS_TOKEN
        }
        headers = {
        "Content-Type": "application/json"
        }

        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message":{
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"button",
                    "text" : "I have retreieved the exact location of the book that you are looking for. :)",
                    "buttons":[
                     {
                        "type":"web_url",
                        "url":"http://localhost/mapping_folder/untitled.html",
                        "title":"Go to book location"
                     }
                    ]
                }
            }
        }
        })

        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    except Exception as e:
        print ("Error : ", str(e))

def send_message_quick_reply_yes_no_interested_now(recipient_id):
    try:
        params = {
            "access_token": ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Are you looking for a book right now?",
                "quick_replies":[
                  {
                    "content_type":"text",
                    "title":"Yes",
                    "payload":"yes_interested",
                    "image_url": "http://emojipedia-us.s3.amazonaws.com/cache/8b/ad/8bad3f664912bfd74b20bd9e2c279a19.png"
                  },
                  {
                    "content_type":"text",
                    "title":"No",
                    "payload":"no_interested",
                    "image_url": "http://emojipedia-us.s3.amazonaws.com/cache/57/7a/577af039fd5a68d6e5ee1986342fe21d.png"
                  }
                ]
            }
          })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    except Exception as e:
        print ("Error : ", str(e))

def check_available(id_):
    try:
        url = "http://10.17.32.5:8380/opac/myaccount/copyDetail.jsp"
        params = {
            "tid": id_
        }
        page = requests.get(url, params=params)
        soup = BeautifulSoup(page.text, "lxml")

        copies = int(soup.find_all("p", id="lblCopyNumVal")[0].text.strip())
        issued =  int(soup.find_all("p", id="lblCopyIssueVal")[0].text.strip())
        ref =  int(soup.find_all("p", id="lblCopyRefVal")[0].text.strip())
        shelf =  int(soup.find_all("p", id="lblCopyShelfVal")[0].text.strip())

        return (copies, issued, shelf)

        # print(copies, issued, ref, shelf)

        # statuses = soup.find_all("ul", id="itrCpyInner")[0].find_all("li")

        # for status in statuses:

        #     status_ = status.find_all("p", id="lblStatVal")[0].text.strip()
        #     detail = status.find_all("p", id="lblItmDtlVal")[0].text.strip()
        #     location = status.find_all("p", id="lblLocVal")[0].text.strip()
        #     rack = status.find_all("p", id="lblReckVal")[0].text.strip()
        #     shelf = status.find_all("p", id="lblShelfVal")[0].text.strip()
        #     floor = status.find_all("p", id="lblFlrVal")[0].text.strip()
        #     due_date = status.find_all("p", id="lblDateVal")[0].text.strip()
        #     category = status.find_all("p", id="lblCatVal")[0].text.strip()

        #     print(status_, detail, location, rack, shelf, floor, due_date, category)

    except Exception as e:
        print ("Error : ", str(e))

def scrape_acc_to_subject(subject_name):
    try:
        searchurl = "http://10.17.32.5:8380/opac/search/searchResult.html"

        params = {
            "searchdata": subject_name,
            "qcon1": 1,
            "cat1": 0,
            "docType": "BK",
            "sortBy": -1,
            "db": 8,
            "search_selectedSites": 1
        }

        r = requests.post(searchurl, params=params)
        page = r.text
        soup = BeautifulSoup(page, "lxml")
        searchresult = soup.find_all("ul", id="searchItr")[0]
        all_suggestions = searchresult.find_all("li", class_="floatedLeft")

        books_retrieved = list()

        books_count = 0

        for result in all_suggestions:
            is_available = result.find_all("div", class_="pnlIsAvailable")[0]
            is_available = is_available.find_all("img")[0]['src']
            if(is_available=="null"):
                continue
            image_url = result.find_all('div', class_="resultImgDiv")[0].img['src']
            if image_url.strip() == "/opac/images/blankBookSmall.png":
                image_url = "http://globedia.com/imagenes/noticias/2012/5/20/historial-error-404_1_1222509.jpg"
            else :
                image_url = image_url[0:len(image_url)-18] + str("250_SCLZZZZZZZ_.jpg")
            label = result.find_all('p', class_="resultsMainLbl")[0].text
            sublabel = result.find_all('p', class_="resultsSubLbl")[0].text
            sublabel2 = result.find_all('p', class_="resultsSubLbl2")[0].text
            info = result.find_all('div', class_="recordObjectDiv")[0]
            id_ = info['titleobjectinfo']
            isbn =  info['isbn']

            book_summary = str(get_book_details(id_))
            book_summary_1 = "Author : " + str(sublabel.strip()) +str(". ") + book_summary

            books_retrieved.insert(0, {"title":str(label.strip()),
                            "image_url":image_url.strip(),
                            "subtitle": (book_summary_1[:70] + "..") if len(book_summary_1)>70 else book_summary_1,
                            "buttons":[
                              {
                                "type":"postback",
                                "title":"Check availaibility",
                                "payload": id_
                              }
                            ]
                      })
            books_count = books_count + 1
            if books_count >= 10:
                break
            # print(image_url.strip())
            # print(label.strip())
            # print(sublabel.strip())
            # print(sublabel2.strip())
            # print(id_)
            # print(isbn)

        facebook_data = {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements": books_retrieved
                  }
                }
            }
        return facebook_data

    except Exception as e:
        print ("Error : ", str(e))

def get_shelf_by_id(id_):
    try:
        details_url = "http://10.17.32.5:8380/opac/detailsPage/detailsPage.jsp?"
        params = {
            "tid":id_,
            "typeOfData":"",
            "_rqst": "undefined",
            "numOfRecords":3,
            "copyDetailJson":""
        }

        headers = {
            "referer": "http://10.17.32.5:8380/opac/search/searchResult.html"
        }

        r = requests.post(details_url, params=params, headers=headers)
        page = r.text
        soup = BeautifulSoup(page, "lxml")
        attrs = soup.find_all("ul", id="dataItr_0")[0].find_all('li', class_="floatedLeft")
        for attr in attrs:
            name = attr.find_all('p', class_="detailsName")[0].text.strip()
            value = attr.find_all('p', class_="detailsValue")[0].text.strip()
            if name == "Call No.":
                return float((value.split(" "))[0])

    except Exception as e:
        print ("Error : ", str(e))


def scrape_acc_to_isbn(subject_name):
    try:
        searchurl = "http://10.17.32.5:8380/opac/search/searchResult.html"
        params = {
            "searchdata": subject_name,
            "qcon1": 1,
            "cat1": 7,
            "docType": "BK",
            "sortBy": -1,
            "db": 8,
            "search_selectedSites": 1
        }

        r = requests.post(searchurl, params=params)
        page = r.text
        soup = BeautifulSoup(page, "lxml")
        searchresult = soup.find_all("ul", id="searchItr")[0]
        all_suggestions = searchresult.find_all("li", class_="floatedLeft")

        books_retrieved = list()
        books_count = 0

        for result in all_suggestions:
            is_available = result.find_all("div", class_="pnlIsAvailable")[0]
            is_available = is_available.find_all("img")[0]['src']
            if(is_available=="null"):
                continue
            image_url = result.find_all('div', class_="resultImgDiv")[0].img['src']
            if image_url.strip() == "/opac/images/blankBookSmall.png":
                image_url = "http://globedia.com/imagenes/noticias/2012/5/20/historial-error-404_1_1222509.jpg"
            else :
                image_url = image_url[0:len(image_url)-18] + str("250_SCLZZZZZZZ_.jpg")
            label = result.find_all('p', class_="resultsMainLbl")[0].text
            sublabel = result.find_all('p', class_="resultsSubLbl")[0].text
            sublabel2 = result.find_all('p', class_="resultsSubLbl2")[0].text
            info = result.find_all('div', class_="recordObjectDiv")[0]
            id_ = info['titleobjectinfo']
            isbn =  info['isbn']

            book_summary = str(get_book_details(id_))
            book_summary_1 = "Author : " + str(sublabel.strip()) +str(". ") + book_summary
            books_retrieved.insert(0, {"title":str(label.strip()),
                            "image_url":image_url.strip(),
                            "subtitle": (book_summary_1[:70] + "..") if len(book_summary_1)>70 else book_summary_1,
                            "buttons":[
                              {
                                "type":"postback",
                                "title":"Check availaibility",
                                "payload": id_
                              }
                            ]
                      })
            books_count = books_count + 1
            if books_count >= 10:
                break
            # print(image_url.strip())
            # print(label.strip())
            # print(sublabel.strip())
            # print(sublabel2.strip())
            # print(id_)
            # print(isbn)

        facebook_data = {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements": books_retrieved
                  }
                }
            }
        return facebook_data

    except Exception as e:
        print ("Error : ", str(e))

def scrape_acc_to_title_and_author(title_name, author_name):
    try:
        searchurl = "http://10.17.32.5:8380/opac/search/searchResult.html"
        params = {
            "searchdata": title_name,
            "qcon1": 1,
            "cat1": 2,
            "con1":0,
            "searchdata2": author_name,
            "qcon2": 1,
            "cat2": 1,
            "docType": "BK",
            "sortBy": -1,
            "db": 8,
            "search_selectedSites": 1
        }

        r = requests.post(searchurl, params=params)
        page = r.text
        soup = BeautifulSoup(page, "lxml")
        searchresult = soup.find_all("ul", id="searchItr")
        if(len(searchresult) == 0):
            books_retrieved = list()
            facebook_data = {
                    "attachment":{
                      "type":"template",
                      "payload":{
                        "template_type":"generic",
                        "elements": books_retrieved
                      }
                    }
                }
            return facebook_data

        all_suggestions = searchresult.find_all("li", class_="floatedLeft")

        books_retrieved = list()
        books_count = 0

        for result in all_suggestions:
            is_available = result.find_all("div", class_="pnlIsAvailable")[0]
            is_available = is_available.find_all("img")[0]['src']
            if(is_available=="null"):
                continue
            image_url = result.find_all('div', class_="resultImgDiv")[0].img['src']
            if image_url.strip() == "/opac/images/blankBookSmall.png":
                image_url = "http://globedia.com/imagenes/noticias/2012/5/20/historial-error-404_1_1222509.jpg"
            else :
                image_url = image_url[0:len(image_url)-18] + str("250_SCLZZZZZZZ_.jpg")
            label = result.find_all('p', class_="resultsMainLbl")[0].text
            sublabel = result.find_all('p', class_="resultsSubLbl")[0].text
            sublabel2 = result.find_all('p', class_="resultsSubLbl2")[0].text
            info = result.find_all('div', class_="recordObjectDiv")[0]
            id_ = info['titleobjectinfo']
            isbn =  info['isbn']

            book_summary = str(get_book_details(id_))
            book_summary_1 = "Author : " + str(sublabel.strip()) +str(". ") + book_summary

            books_retrieved.insert(0, {"title":str(label.strip()),
                            "image_url":image_url.strip(),
                            "subtitle": (book_summary_1[:70] + "..") if len(book_summary_1)>70 else book_summary_1,
                            "buttons":[
                              {
                                "type":"postback",
                                "title":"Check availaibility",
                                "payload": id_
                              }
                            ]
                      })
            books_count = books_count + 1
            if books_count >= 10:
                break

            # print(image_url.strip())
            # print(label.strip())
            # print(sublabel.strip())
            # print(sublabel2.strip())
            # print(id_)
            # print(isbn)

        facebook_data = {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements": books_retrieved
                  }
                }
            }
        return facebook_data

    except Exception as e:
        print ("Error : ", str(e))

def get_book_details(id_):
    try:
        details_url = "http://10.17.32.5:8380/opac/detailsPage/detailsPage.jsp?"
        params = {
            "tid":id_,
            "typeOfData":"",
            "_rqst": "undefined",
            "numOfRecords":3,
            "copyDetailJson":""
        }

        headers = {
            "referer": "http://10.17.32.5:8380/opac/search/searchResult.html"
        }
        r = requests.post(details_url, params=params, headers=headers)
        page = r.text
        soup = BeautifulSoup(page, "lxml")
        attrs = soup.find_all("ul", id="dataItr_0")[0].find_all('li', class_="floatedLeft")
        for attr in attrs:
            name = attr.find_all('p', class_="detailsName")[0].text.strip()
            value = attr.find_all('p', class_="detailsValue")[0].text.strip()
            if name == "Libsys Abstract Data":
                return value

    except Exception as e:
        print ("Error : ", str(e))

def send_message_carousel(recipient_id, data_to_send):
    try:
        params = {
            "access_token": ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }

        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": data_to_send
          })

        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    except Exception as e:
        print ("Error : ", str(e))

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False, port=7010, host='127.0.0.1')
