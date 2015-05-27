import requests
import json
import base64
from . import models
import inspect

class Client(object):
    def __init__(self):
        self.BASE_URL = "https://api.helpscout.net/v1/"
        self.API_KEY = ""
        self.pagestate = {}

    def mailbox(self, mailbox_id, fields=None):
        url = add_fields("mailboxes/{}.json".format(mailbox_id), fields)
        return self.item(url, "Mailbox", 200)

    def mailboxes(self, fields=None):
        url = add_fields("mailboxes.json", fields)
        return self.page(url,"Mailbox", 200)

    def folders(self, mailbox_id, fields=None):
        url = add_fields("mailboxes/{}/folders.json".format(mailbox_id), fields)
        return self.page(url, "Folder", 200)

    def conversations_for_folders(self, mailbox_id, folder_id, fields=None):
        url = "mailboxes/{}/folders/{}/converstations.json".format(mailbox_id, folder_id)
        url = add_fields(url, fields)
        return self.page(url, "Conversation", 200)

    def conversations_for_mailbox(self, mailbox_id, fields=None):
        url = add_fields("mailboxes/{}/conversations.json".format(mailbox_id), fields)
        return self.page(url, "Conversation", 200)

    def conversation_for_customer_by_mailbox(self, mailbox_id, customer_id, fields=None):
        url = "mailboxes/{}/customers/{}/conversations.json".format(mailbox_id, customer_id)
        url = add_fields(url, fields)
        return self.page(url, "Conversation", 200)

    def conversation(self, conversation_id, fields=None):
        url = add_fields("conversations/{}.json".format(conversation_id), fields)
        return self.item(url, "Conversation", 200)

    def attachment_data(self, attachment_id):
        url = "attachments/{}/data.json".format(attachment_id)
        json_string = self.call_server(url, 200)
        json_obj = json.loads(json_string)
        item = json_obj["item"]
        return item["data"]

    def customers(self, fields=None):
        url = add_fields("customers.json", fields)
        return self.page(url, "Customer", 200)

    def customer(self, customer_id, fields=None):
        url = add_fields("customers/{}.json".format(customer_id), fields)
        return self.page(url, "Customer", 200)

    def user(self, user_id, fields=None):
        url = add_fields("users/{}.json".format(user_id), fields)
        return self.item(url, "User", 200)

    def users(self, fields=None):
        url = add_fields("users.json", fields)
        return self.page(url, "User", 200)

    def users_for_mailbox(self, mailbox_id, fields=None):
        url = add_fields("mailboxes/{}/users.json".format(mailbox_id), fields)
        return self.page(url, "User", 200)

    def call_server(self, url, expected_code, page=None):
        headers = {'Content-Type': 'application-json'
                  , 'Accept' : 'application-json'
                  , 'Accept-Encoding' : 'gzip, deflate'
                  }
        qsp = {}
        if page:
            qsp = {'page': page}
        r = requests.get(self.BASE_URL + url, headers=headers, auth=(self.API_KEY, 'x'), params=qsp)
        check_status_code(r.status_code, expected_code)
        return r.text

    def item(self, url, clazz, expected_code):
        string_json = self.call_server( url, expected_code )
        return Parser.parse(json.loads(string_json)["item"], clazz)

    def page(self, url, clazz, expected_code):
        # support calling many times to get subsequent pages
        caller = inspect.stack()[1][3]
        if caller in self.pagestate:
            curpage = self.pagestate[url].page
            maxpage = self.pagestate[url].pages
            if curpage < maxpage:
                page = curpage + 1
            elif curpage == maxpage:
                return None
        else:
            page = 1

        string_json = self.call_server(url, expected_code, page)
        json_obj = json.loads(string_json)
        p = Page()
        for key, value in json_obj.items():
            setattr(p, key, value)
        p.items = parse_list(p.items, clazz)

        # update state cache with response details
        self.pagestate[caller] = {'page': p.page, 'pages': p.pages}

        return p

    def setpage(self, function, page=2):
        '''Set a specific page number to start at when fetching paginated data'''
        if self.pagestate.get(function, None):
            self.pagestate[function]['page'] = int(page) - 1
            # this will be updated to be valid on the next call to "function"
            self.pagestate[function]['pages'] = int(page)

    def reset(self, function=None):
        '''Clear the function state tracking, optionally taking a specific function to clear
           Usage:
             client.reset()
             client.reset('users_for_mailbox')
        '''
        if function:
            if self.pagestate.pop(function, None) == None:
                return False
        else:
            self.pagestate = {}
        return True

def check_status_code(code, expected):
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
    for key, value in list(json.items()):
        setattr(c, key, value)
    return c

def parse_list(lizt, clazz):
    for i in range (len(lizt)):
        lizt[i] = parse(lizt[i], clazz)
    return lizt

class Page:
    def __init__(self):
        self.page = None
        self.pages = None
        self.count = None
        self.items = None

class ApiException(Exception):
    def __init__(self, message):
        Exception.__init__(self,message)
