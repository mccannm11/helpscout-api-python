import requests
import json
import base64
import models


class ApiClient(object):
    BASE_URL = "https://api.helpscout.net/v1/"
    API_KEY = ""
    
    def mailbox(self, mailbox_id, fields=None):
        url = add_fields("mailboxes/" + str(mailbox_id) + ".json", fields)
        return self.item(url, "Mailbox", 200)

    def mailboxes(self, fields=None):
        url = add_fields("mailboxes.json", fields)
        return self.page(url,"Mailbox", 200)

    def folders(self, mailbox_id, fields=None):
        url = add_fields("mailboxes/" + str(mailbox_id) + "/folders.json", fields)
        return self.page(url, "Folder", 200)

    def conversations_for_folders(self, mailbox_id, folder_id, fields=None):
        url = "mailboxes/" + str(mailbox_id) + "/folders/" + str(folder_id) + "/conversations.json"
        url = add_fields(url, fields)
        return self.page(url, "Conversation", 200)

    def conversations_for_mailbox(self, mailbox_id, fields=None):
        url = add_fields("mailbox/" + str(mailbox_id) + "/conversations.json", fields)
        return self.page(url)

    def conversation_for_customer_by_mailbox(self, mailbox_id, customer_id, fields=None):
        url = "mailboxes/" + str(mailbox_id) + "/customers/" + str(customer_id) + "/conversations.json"
        url = add_fields(url, fields)
        return self.page(url, "Conversation", 200)

    def conversation(self, conversation_id, fields=None):
        url = add_fields("conversations/" + str(conversation_id) + ".json", fields)
        return self.item(url, "Conversation", 200)

    def attachment_data(self, attachment_id):
        url = "attachments/" + str(attachment_id) + "/data.json" 
        json_string = self.call_server(url, 200)
        json_obj = json.loads(json_string)
        item = json_obj["item"]
        return item["data"]

    def customers(self, fields=None):
        url = add_fields("customers.json", fields)
        return self.page(url, "Customer", 200)

    def customer(self, customer_id, fields=None):
        url = add_fields("customers/" + str(customer_id) + ".json", fields)
        return self.page(url, "Customer", 200)

    def user(self, user_id, fields=None):
        url = add_fields("users/" + str(user_id) + ".json", fields)
        return self.item(url, "User", 200)

    def users(self, fields=None):
        url = add_fields("users.json", fields)
        return self.page(url, "User", 200)

    def users_for_mailbox(self, mailbox_id, fields=None):
        url = add_fields("mailboxes/" + str(mailbox_id) + "users.json", fields)
        return self.page(url, "User", 200)

    def call_server(self, url, expected_code):
        auth =  "Basic " + self.encoded() 
        headers = {'Content-Type': 'application-json'
                  , 'Accept' : 'application-json'
                  , 'Authorization' : str(auth)
                  , 'Accept-Encoding' : 'gzip, deflate'
                  }
        r = requests.get(self.BASE_URL + url, headers=headers)
        check_status_code(r.status_code, expected_code)
        return r.text

    def item(self, url, clazz, expected_code):
        string_json = self.call_server( url, expected_code )
        return Parser.parse(json.loads(string_json)["item"], clazz)
        
    def page(self, url, clazz, expected_code):
        string_json = self.call_server(url, expected_code)
        json_obj = json.loads(string_json)
        p = Page()
        for key, value in json_obj.iteritems():
            setattr(p, key, value)
        p.items = parse_list(p.items, clazz)
        return p
    
    def encoded(self):
        raw = str(self.API_KEY) + ":x"
        return base64.b64encode(raw)

    def decoded(val):
        return base64.b64decode(val)


def check_status_code(code, expected):
    if code == expected:
        return
    default_status = "Invalid API Key"
    status = status_codes[str(code)]
    if status != None:
        raise ApiException(status)
    else:
        raise ApiException(default_status)

def add_fields(url, fields):
    final_str = url
    if fields != None and len(fields) > 0 :
        final_str += "?fields="
        sep = ""
        for key,value in fields:
            final_str += sep + value
            sep = ","
    return final_str

def parse(json, clazz):
    c = getattr(models, clazz)()
    for key, value in json.items():
        setattr(c, key, value)
    return c

def parse_list(lizt, clazz):
    for i in range (len(lizt)):
        lizt[i] = parse(lizt[i], clazz)

    return lizt

status_codes = {
    '400': 'The request was not formatted correctly',
    '401': 'Invalid API Key',
    '402': 'API Key Suspended',
    '403': 'Access Denied',
    '404': 'Resource Not Found',
    '405': 'Invalid Method Type',
    '429': 'Throttle Limit Reached. Too many requests',
    '500': 'Application Error or Server Error',
    '503': 'Service Temporarily Unavailable'
    }

class Page:
    def __init__(self):
        self.page = None
        self.pages = None
        self.count = None
        self.items = None


class ApiException(Exception):
    def __init__(self, message):
        Exception.__init__(self,message)




