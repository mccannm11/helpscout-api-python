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
Example Usage: API
---------------------
<pre><code>
import ApiClient

client = ApiClient.ApiClient()
client.API_KEY = "your-api-key-here"

mailboxes = client.mailboxes()
folders = mailboxes.folders
for f in folders:
    #do things here


customer = client.customer(customer-id-here)
if customers.socialProfiles != None:
    for s in customers.socialProfiles:
         #do things

</code></pre>


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
* conversations_for_folder(int mailbox_id, int folder_id)
* conversations_for_mailbox(int mailbox_id)
* conversations_for_customerByMailbox(int mailbox_id, int customer_id)
* conversation(Integer conversation_id)

### Attachments
* attachment_data(int attachment_id)

### Customers
* customers()
* customer(int customer_id)

### Users
* users()
* users_for_mailbox(int mailbox_id)
* user(int user_id)

