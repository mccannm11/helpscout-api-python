helpscout-api-python
====================

Python wrapper for the Help Scout API 

Trying to get some python chops together. Criticism is much appreciated.
This is a pre aplha release and is still very much under construction.

<h5>
Dependencies
</h5>
<ul>
<li>
Python 2.7
</li>
<li>
requests
</li>
<li>
json
</li>
<li>
base64
</li>
</ul>

Field Selectors
---------------------
Field selectors are given as a list of Strings. When field selectors are used, the appropriate object is created with the fields provided.

ApiClient Methods
--------------------
Each method can accept a field selector as an addition parameter.

### Mailboxes
* getMailboxes()
* getMailbox(int mailbox_id)

### Folders
* getFolders(int mailbox_id)

### Conversations
* getConversationsForFolder(int mailbox_id, int folder_id)
* getConversationsForMailbox(int mailbox_id)
* getConversationsForCustomerByMailbox(int mailbox_id, int customer_id)
* getConversation(Integer conversation_id)

### Attachments
* getAttachmentData(int attachment_id)

### Customers
* getCustomers()
* getCustomer(int customer_id)

### Users
* getUsers()
* getUsersForMailbox(int mailbox_id)
* getUser(int user_id)

