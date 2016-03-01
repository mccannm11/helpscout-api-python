import client

class Attachment:
    def __init__(self):
        self.id = None
        self.mimetype = None
        self.filename = None
        self.size = None
        self.width = None
        self.height = None
        self.url = None

    def isimage(self):
        return self.mimetype is not None and self.mimetype.startwith('image')

class Conversation(object):
    def __init__(self):
        self.id = None
        self.folderid = None
        self.isdraft = None
        self.number = None
        self.source = None
        self.owner = None
        self.mailbox = None
        self.customer = None
        self.threadcount = None
        self.status = None
        self.subject = None
        self.preview = None
        self.createdat = None
        self.modifiedat = None
        self.closedat = None
        self.closedby = None
        self.createdby = None
        self.cclist = None
        self.bcclist = None
        self.tags = None
        self._threads = None

    def iscreatedbycustomer(self):
        return self.createdby is not None and isinstance(self.createdby, CustomerRef)

    def hascclist(self):
        return self.cclist is not None and len(self.cclist) > 0

    def hasbcclist(self):
        return self.bcclist is not None and len(self.bcclist) > 0

    def hastags(self):
        return self.tags is not None and len(self.tags) > 0

    def hasthreads(self):
        return self._threads is not None and len(self._threads) > 0

    @property
    def threads(self):
        """threads"""
        return self._threads

    @threads.setter
    def threads(self, value):
        self._threads = client.parse_list(value, "Thread")


class Customer:
    def __init__(self):
        self.id = None
        self.firstname = None
        self.lastname = None
        self.gender = None
        self.age = None
        self.joblocation = None
        self.location = None
        self.organization = None
        self.photourl = None
        self.phototype = None
        self.createdat = None
        self.modifiedat = None
        self.background = None
        self.address = None
        self.socialprofiles = None
        self.emails = None
        self.phones = None
        self.chats = None
        self.websites = None

    def hasbackground(self):
        return self.background is not None

    def hasaddress(self):
        return self.address is not None

    def hassocialprofiles(self):
        return self.socialprofiles is not None and len(self.socialprofiles) > 0

    def hasemails(self):
        return self.emails is not None

    def hasphones(self):
        return self.phones is not None and len(self.phones) > 0

    def haschats(self):
        return self.chats is not None and len(self.chats) > 0

    def haswebsites(self):
        return self.websites is not None and len(self.websites) > 0

class Folder:
    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.userid = None
        self.totalcount = None
        self.activecount = None
        self.modifiedat = None


class Mailbox:
    def __init__(self):
        self.id = None
        self.name = None
        self.slug = None
        self.email = None
        self.createdat = None
        self.modifiedat = None


class Source:
    def __init__(self):
        self.type = None
        self.via = None

    def isviacustomer(self):
        return self.via is not None and "customer" == self.via


class User:
    def __init__(self):
        self.id = None
        self.firstname = None
        self.email = None
        self.role = None
        self.timezone = None
        self.photourl = None
        self.createdat = None
        self.modifiedat = None



class Address:
    def __init__(self):
        self.id = None
        self.lines = None
        self.city = None
        self.state = None
        self.postalcode = None
        self.country = None
        self.createdat = None
        self.modifiedat = None


class CustomerEntry:
    def __init__(self):
        self.id = None
        self.value = None
        self.type = None
        self.location = None


class EmailEntry(CustomerEntry):
    def __init__(self):
        super(EmailEntry, self).__init__()


class ChatEntry(CustomerEntry):
    def __init__(self):
        super(ChatEntry, self).__init__()


class PhoneEntry(CustomerEntry):
    def __init__(self):
        super(PhoneEntry, self).__init__()


class SocialProfileEntry(CustomerEntry):
    def __init__(self):
        super(SocialProfileEntry, self).__init__()

class WebsiteEntry(CustomerEntry):
    def __init__(self):
        super(WebsiteEntry, self).__init__()


class MailboxRef:
    def __init__(self):
        self.id = None
        self.name = None


class AbstractRef:
    def __init__(self):
        self.id = None
        self.firstname = None
        self.lastname = None
        self.email = None


class UserRef(AbstractRef):
    def __init__(self):
        super(UserRef, self).__init__()


class CustomerRef(AbstractRef):
    def __init__(self):
        super(CustomerRef, self).__init__()


class Thread(object):
    def __init__(self):
        self.id = None
        self.state = None
        self.body = None
        self.tolist = None
        self.cclist = None
        self.bcclist = None
        self.attachments = None

    def ispublished(self):
        return self.state == "published" ##hmmm these are not right

    def isdraft(self):
        return self.state == "draft"

    def isheldforreview(self):
        return self.state == "underreview"

    def hasattachments(self):
        return self.attachments is not None and len(self.attachments) > 0


class ForwardChild(AbstractRef):
    def __init__(self):
        super(ForwardChild, self).__init__()

class Note(AbstractRef):
    def __init__(self):
        super(Note, self).__init__()

class Message(AbstractRef):
    def __init__(self):
        super(Message, self).__init__()

class ForwardParent(AbstractRef):
    def __init__(self):
        super(ForwardParent, self).__init__()

class Search:
    def __init__(self):
        self.id = None
        self.number = None
        self.mailboxid = None
        self.subject = None
        self.status = None
        self.threadcount = None
        self.preview = None
        self.customerName = None
        self.customerEmail = None
        self.modifiedAt = None

