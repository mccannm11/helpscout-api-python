import requests
import json
import base64

class Attachment:
    def __init__(self):
        self.id = None
        self.mimeType = None
        self.fileName = None
        self.size = None
        self.width = None
        self.height = None
        self.url = None

    def isImage(self):
        return self.mimeType != NULL and mimeType.substring(0, 4) == "image"
        
class Conversation:
    def __init__(self):
        self.id = None
        self.folderId = None
        self.isDraft = None
        self.number = None
        self.source = None
        self.owner = None
        self.mailbox = None
        self.customer = None
        self.threadCount = None
        self.status = None
        self.subject = None
        self.preview = None
        self.createdAt = None
        self.modifiedAt = None
        self.closedAt = None
        self.closedBy = None
        self.createdBy = None
        self.ccList = None
        self.bccList = None
        self.tags = None

        def isCreatedByCustomer(self):
            return self.createdBy != None and isinstance(self.createdBy, CustomerRef)

        def hasCcList(self):
            return self.ccList != None and len(self.ccList) > 0

        def hasBccList(self):
            return self.bccList != None and len(self.bccList) > 0

        def hasTags(self):
            return self.tags != None and len(self.tags) > 0
        
class Customer:
    def __init__(self):
        self.id = None
        self.firstName = None
        self.lastName = None
        self.gender = None
        self.age = None
        self.jobLocation = None
        self.location = None
        self.organization = None
        self.photoUrl = None
        self.photoType = None
        self.createdAt = None
        self.modifiedAt = None
        self.background = None
        self.address = None 
        self.socialProfiles = None
        self.emails = None
        self.phones = None
        self.chats = None
        self.websites = None

        def hasBackground(self):
            return self.background != None

        def hasAddress(self):
            return self.address != None

        def hasSocialProfiles(self):
            return self.socialProfiles != None and len(self.socialProfiles) > 0

        def hasEmails(self):
            return self.emails != None

        def hasPhones(self):
            return self.phones != None and len(self.phones) > 0

        def hasChats(self):
            return self.chats != None and len(self.chats) > 0

        def hasWebsites(self):
            return self.websites != None and len(self.websites) > 0 

        
class Folder:
    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.userId = None
        self.totalCount = None
        self.activeCount = None
        self.modifiedAt = None

        
class Mailbox:
    def __init__(self):
        self.id = None
        self.name = None
        self.slug = None
        self.email = None
        self.createdAt = None
        self.modifiedAt = None

        
class Source:
    def __init__(self):
        self.type = None
        self.via = None

    def isViaCustomer(self):
        return self.via != None and "customer" == self.via

    
class User:
    def __init__(self):
        self.id = None
        self.firstName = None
        self.email = None
        self.role = None
        self.timezone = None
        self.photoUrl = None
        self.createdAt = None
        self.modifiedAt = None



class Address:
    def __init__(self):
        self.id = None
        self.lines = None
        self.city = None
        self.state = None
        self.postalCode = None
        self.country = None
        self.createdAt = None
        self.modifiedAt = None


class CustomerEntry:
    def __init__(self):
        self.id = None
        self.value = None
        self.type = None
        self.location = None


class EmailEntry(CustomerEntry):
    def __init__(self):
        pass


class ChatEntry(CustomerEntry):
    def __init__(self):
        pass


class PhoneEntry(CustomerEntry):
    def __init__(self):
        pass


class SocialProfileEntry(CustomerEntry):
    def __init__(self):
        pass

class WebsiteEntry(CustomerEntry):
    def __init__(self):
        pass


class MailboxRef:
    def __init__(self):
        self.id = None
        self.name = None


class AbstractRef:
    def __init__(self):
        self.id = None
        self.firstName = None
        self.lastName = None
        self.email = None


class UserRef(AbstractRef):
    def __init__(self):
        pass


class CustomerRef(AbstractRef):
    def __init__(self):
        pass


class AbstractThread:
    def __init__(self):
        self.id = None
        self.state = None
        self.body = None
        self.toList = None
        self.ccList = None
        self.bccList = None
        self.attachments  = None

        def isPublished(self):
            return self.state == "published" ##hmmm these are not right

        def isDraft(self):
            return self.state == "draft"

        def isHeldForReview(self):
            return self.state == "underreview"

        def hasAttachments(self):
            return self.attachemnts != None and len(self.attachments) > 0


class Customer(AbstractRef):
    def __init__(self):
        pass


class ForwardChild(AbstractRef):
    def __init(self):
        pass


class Note(AbstractRef):
    def __init__(self):
        pass


class Message(AbstractRef):
    def __init__(self):
        pass


class ForwardParent(AbstractRef):
    def __init__(self):
        pass



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
        c = globals()["User"]()
        for i in json:
            setattr(c, i, json[i])
        return c 



