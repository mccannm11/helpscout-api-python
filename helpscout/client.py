import requests
import json
from . import models
import inspect

class Client(object):
    def __init__(self):
        self.base_url = "https://api.helpscout.net/v1/"
        self.api_key = ""
        self.pagestate = {}

    def mailbox(self, mailbox_id, fields=None):
        url = add_fields("mailboxes/{}.json".format(mailbox_id), fields)
        return self.item(url, "Mailbox", 200)

    def mailboxes(self, fields=None, **kwargs):
        url = add_fields("mailboxes.json", fields)
        return self.page(url, "Mailbox", 200, **kwargs)

    def folders(self, mailbox_id, fields=None, **kwargs):
        url = add_fields("mailboxes/{}/folders.json".format(mailbox_id), fields)
        return self.page(url, "Folder", 200, **kwargs)

    def conversations_for_folder(self, mailbox_id, folder_id, fields=None, **kwargs):
        url = "mailboxes/{}/folders/{}/converstations.json".format(mailbox_id, folder_id)
        url = add_fields(url, fields)
        return self.page(url, "Conversation", 200, **kwargs)

    def conversations_for_mailbox(self, mailbox_id, fields=None, **kwargs):
        url = add_fields("mailboxes/{}/conversations.json".format(mailbox_id), fields)
        return self.page(url, "Conversation", 200, **kwargs)

    def conversations_for_customer_by_mailbox(self, mailbox_id, customer_id, fields=None, **kwargs):
        url = "mailboxes/{}/customers/{}/conversations.json".format(mailbox_id, customer_id)
        url = add_fields(url, fields)
        return self.page(url, "Conversation", 200, **kwargs)

    def conversations_for_user_by_mailbox(self, mailbox_id, user_id, fields=None, **kwargs):
        url = "mailboxes/{}/customers/{}/conversations.json".format(mailbox_id, user_id)
        url = add_fields(url, fields)
        return self.page(url, "Conversation", 200, **kwargs)

    def conversation(self, conversation_id, fields=None):
        url = add_fields("conversations/{}.json".format(conversation_id), fields)
        return self.item(url, "Conversation", 200)

    def attachment_data(self, attachment_id):
        url = "attachments/{}/data.json".format(attachment_id)
        json_string = self.call_server(url, 200)
        json_obj = json.loads(json_string)
        item = json_obj["item"]
        return item["data"]

    def customers(self, fields=None, **kwargs):
        url = add_fields("customers.json", fields)
        return self.page(url, "Customer", 200, **kwargs)

    def customer(self, customer_id, fields=None, **kwargs):
        url = add_fields("customers/{}.json".format(customer_id), fields)
        return self.page(url, "Customer", 200, **kwargs)

    def user(self, user_id, fields=None):
        url = add_fields("users/{}.json".format(user_id), fields)
        return self.item(url, "User", 200)

    def users(self, fields=None, **kwargs):
        url = add_fields("users.json", fields)
        return self.page(url, "User", 200, **kwargs)

    def users_for_mailbox(self, mailbox_id, fields=None, **kwargs):
        url = add_fields("mailboxes/{}/users.json".format(mailbox_id), fields)
        return self.page(url, "User", 200, **kwargs)

    def search(self, query=None, sort_field="number", sort_order="asc", **kwargs):
        url = "search/conversations.json?query=({})&sort_field={}&sort_order={}".format(query, sort_field, sort_order)
        return self.page(url, "Search", 200, **kwargs)

    def call_server(self, url, expected_code, **params):
        headers = {'Content-Type': 'application-json',
                   'Accept' : 'application-json',
                   'Accept-Encoding' : 'gzip, deflate'
                  }
        req = requests.get('{}{}'.format(self.base_url, url),
                           headers=headers, auth=(self.api_key, 'x'), params=params)
        check_status_code(req.status_code, expected_code)
        return req.text

    def item(self, url, cls, expected_code):
        string_json = self.call_server(url, expected_code)
        return parse(json.loads(string_json)["item"], cls)

    def page(self, url, cls, expected_code, **kwargs):
        # support calling many times to get subsequent pages
        caller = inspect.stack()[1][3]
        if kwargs.get('page') is None:
            if caller in self.pagestate:
                (pcur, pmax) = [self.pagestate[caller].get(x) for x in ['page', 'pages']]
                if all((pcur, pmax)) and pcur < pmax:
                    kwargs['page'] = pcur + 1
                elif pcur == pmax:
                    return None

        string_json = self.call_server(url, expected_code, **kwargs)
        json_obj = json.loads(string_json)
        page = Page()
        for key, value in json_obj.items():
            setattr(page, key, value)
        page.items = parse_list(page.items, cls)

        # update state cache with response details
        self.pagestate[caller] = {'page': page.page, 'pages': page.pages}

        return page

    def clearstate(self, function=None):
        '''Clear the function state tracking, optionally taking a specific function to clear
           Usage:
             client.reset()
             client.reset('users_for_mailbox')
        '''
        if function:
            if self.pagestate.pop(function, None) is None:
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
    if fields != None and len(fields) > 0:
        final_str = "{}?fields={}".format(url, ','.join(fields))
    return final_str

def parse(json_obj, cls):
    obj = getattr(models, cls)()
    for key, value in list(json_obj.items()):
        setattr(obj, key.lower(), value)
    return obj

def parse_list(lst, cls):
    for i in range(len(lst)):
        lst[i] = parse(lst[i], cls)
    return lst

class Page:
    def __init__(self):
        self.page = None
        self.pages = None
        self.count = None
        self.items = None
    def __getitem__(self, index):
        return self.items[index]

    
class ApiException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
