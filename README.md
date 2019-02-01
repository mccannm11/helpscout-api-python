helpscout-api-python
====================

Python wrapper for the Help Scout API 

## Installation:
`git clone git@github.com/mccannm11/helpscout-api-python`
`cd helpscout-api-python && python setup.py install`

Example Usage: API
---------------------

```
import helpscout

client = helpscout.Client()
client.api_key = "your-api-key-here"

mailboxes = client.mailboxes()
folders = client.folders(mailboxes.items[0].id)
for f in folders:
    #do things here


customer = client.customer(customer-id-here)
if customers.socialProfiles != None:
    for s in customers.socialProfiles:
         #do things

```


Field Selectors
---------------------
Field selectors are given as a list of Strings. When field selectors are used, the appropriate object is created with the fields provided.

ApiClient Methods
--------------------
Each method can accept a field selector as an addition parameter.

### Mailboxes
* mailboxes()
* mailbox(int mailbox_id)

### Folders
* folders(int mailbox_id)

### Conversations
* conversations_for_folders(int mailbox_id, int folder_id)
* conversations_for_mailbox(int mailbox_id)
* conversations_for_customerByMailbox(int mailbox_id, int customer_id)
* conversation(int conversation_id)

### Attachments
* attachment_data(int attachment_id)

### Customers
* customers()
* customer(int customer_id)

### Users
* users()
* users_for_mailbox(int mailbox_id)
* user(int user_id)

### Search
* search()
* search(query="subject:foo")
* search(query="subject:foo", sort_by="number", sort_order="asc")

See full syntax for query parameter here:
http://developer.helpscout.net/help-desk-api/search/conversations/

### Pagination
Multiple calls to the above calls that support pagination will return subsequent pages.  
* clearstate() - to clear the pagination couters and start from page 1 again.
* clearstate(str 'function') - to clear the pagination couter for a given function, e.g. "folders"
You could set the starting page by passing in page=N as a keyword arg.
