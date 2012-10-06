
class Attachment:
    def __init__(self):
        self._id = None
        self._mimeType = None
        self._fileName = None
        self._size = None
        self._width = None
        self._height = None
        self._url = None

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


