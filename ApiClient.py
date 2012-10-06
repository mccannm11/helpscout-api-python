import requests
import json
import base64
import models


class ApiClient:
    BASE_URL = "https://api.helpscout.net/v1/"
    apiKey = ""
    
    def getMailbox(self, mailbox_id, fields=None):
        url = "mailboxes/" + str(mailbox_id) + ".json"
        if fields != None:      
            url = self.setFields(url, fields)
        return self.getItem(url, "Mailbox", 200)

    def getMailboxes(self, fields=None):
        url = "mailboxes.json"
        if fields != None:
            url = self.setFields(url, fields)
        return self.getPage(url,"Mailbox", fields)

    def getFolders(self, mailbox_id, fields=None):
        url = "mailboxes/" + str(mailbox_id) + "/folders.json"
        if fields != None:    
            url = self.setFields(url, fields)
        return self.getPage(url, "Folder", 200)

    def getConverstationsForFolders(self, mailbox_id, folder_id, fields=None):
        url = "mailboxes/" + str(mailbox_id) + "/folder/" + str(folder_id) + "conversations.json"
        if fields != None:     
            url = self.setFields(url, fields)
        return self.getPage(url, "Conversation", 200)

    def getConversationsForMailbox(self, mailbox_id, fields=None):
        url = "mailbox/" + str(mailbox_id) + "/conversations.json"
        if fields != None :
            url = self.setFields(url, fields)
        return self.getPage(url)

    def getConversationForCustomerByMailbox(self, mailbox_id, customer_id, fields=None):
        url = "mailboxes/" + str(mailbox_id) + "/customers/" + str(customer_id) + "/conversations.json"
        if fields != None:
            url = self.setFields(url, fields)
        return self.getPage(url, "Conversation", 200)

    def getConversation(self, conversation_id, fields=None):
        url = "conversations/" + str(conversation_id) + ".json"
        if fields != None:
            url = self.setFields(url, fields)
        return self.getItem(url, "Conversation", 200)

    def getAttachmentData(self, attachment_id):
        url = "attachments/" + str(attachment_id) + "/data.json" 
        json_string = self.callServer(url, 200)
        json_obj = json.loads(json_string)
        item = json_obj["item"]
        return item["data"]

    def getCustomers(self, fields=None):
        url = "customers.json"
        if fields != None:
            url = self.setFields(url, fields)
        return self.getPage(url, "Customer", 200)

    def getCustomer(self, customer_id, fields=None):
        url = "customers/" + str(customer_id) + ".json"
        if fields != None:
            url = self.setFields(url, fields)
        return self.getPage(url, "Customer", 200)

    def getUser(self, user_id, fields=None):
        url = "users/" + str(user_id) + ".json"
        if fields != None:
            url = self.setFields(url, fields)
        return self.getItem(url, "User", 200)

    def getUsers(self, fields=None):
        url = "users.json"
        if fields != None:
            url = self.setFields(url, fields)
        return self.getPage(url, "User", 200)

    def getUsersForMailbox(self, mailbox_id, fields=None):
        url = "mailboxes/" + str(mailbox_id) + "users.json"
        if fields != None:
            url = self.setFields(url, fields)
        return getPage(url, "User", 200)

    def callServer(self, url, expected_code):
        auth =  "Basic " + self.getEncoded() 
        headers= {'Content-Type': 'application-json'
                  , 'Accept' : 'application-json'
                  , 'Authorization' : str(auth)
                  , 'Accept-Encoding' : 'gzip, deflate'
                  }
        r = requests.get(self.BASE_URL + url, headers=headers)
        self.checkStatusCode(r.status_code, expected_code)
        return r.text

    def getItem(self, url, clazz, expected_code):
        string_json = self.callServer( url, expected_code )
        return Parser.parse(json.loads(string_json)["item"], clazz)
        
    def getPage(self, url, clazz, expected_code):
        string_json = self.callServer(url, expected_code)
        json_obj = json.loads(string_json)
        p = Page()

        for i in json_obj:
            setattr(p, i, json_obj[i])
        return p
    
    def getEncoded(self):
        raw = str(self.apiKey) + ":x"
        return base64.b64encode(raw)

    def getDecoded(val):
        return base64.b64decode(val)

    def setFields(self, url, fields):
        final_str = url + "?fields="
        if (fields != None and len(fields) > 0 ):
            sep = ""
            for i in fields:
                final_str += sep + fields[i]
                sep = ","

        return final_str
    
    def checkStatusCode(self, code, expected):
        if code == expected:
            return
        """ @todo gotta be a better way to do this """
        if (code == 400):
            raise Exception("The request was not formatted correctly")
        elif(code == 401):
            raise Exception("Invalid Api Key")
        elif(code == 402):
            raise Exception("API Key Suspended")
        elif (code == 403):
            raise Exception("Access Denied")
        elif (code == 404):
            raise Exception("Resource Not Found")
        elif (code == 405):
            raise Exception("Invalid method Type")
        elif(code == 429):
            raise Exception("Throttle Limit Reached. Too Many requests")
        elif(code == 500):
            raise Exception("Application Error or server error")
        elif(code == 503):
            raise Exception("Service Temporarily Unavailable")
        else:
            raise Exception("API Key Suspended")
            

class Page:
    def __init__(self):
        self.page = None
        self.pages = None
        self.count = None
        self.items = None

class ApiException(Exception):
    def __init__(self, message):
        Exception.__init__(self,message)


class Parser:
    @staticmethod
    def parse(json, clazz):
        c = getattr(globals()["models"], clazz)()
        for i in json:
            setattr(c, i, json[i])
        return c 



