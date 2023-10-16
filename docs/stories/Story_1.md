### Story 1(Use case 1) : Government Bond with defined coupon payments
* Quantifiable=True  (quantity=Integer)
* Transferable=True  (transferable=True)
* Expiry=Yes         (expiry=)
* Verifiable=True    (verifiable=True)

---

### General Information
* Any node can issue a instrument to any other node
* Based on whether transferable(or not), the owning node can transfer the asset(instrument) to any other node.
* Based on whether quantifiable(or not), the asset(instrument) can be transferred(or consumed) in portion or as a whole.
 * Quantifiable is a flag(control) which is decided at the time of the issue of the instrument, by setting a value to quantity. No value for attribute=quantity, makes it non-quantifiable.

---

### Step 1: Issue (Expected Success)
* Node=Authority is issuing ten instruments='Government Bond' to node=Alice
* Flow=Issue
 * Issuer gets to decide the name, transferable or not, expiry or not, redeemable or not, and can add multiple/additional attributes (HashMap) on the same State/Asset.
 * Applications like Government Bond, will be transferable, with maturity(some expiry), and redeemable (cash the principal on maturity), with additional attribute of coupon payment dates.
 * Applications like College University Degree, will not be transferable, no expiry, and not redeemable. Will have additional attributes like Collage Name, University Name, Education Stream etc etc along with Issuer and Owner(Holder).
 * Applications like Limited Edition Sovereign, will be transferable, no expiry but will be redeemable directly with Issuer.

#### Issue. Python3/Jupyter call:
```
h.message("Government Bond with defined coupon payments")
(req_id, response, uuid_bond) = h.issue('Authority', 'Alice', 'Government Bond 2024', 
        quantity=10,
        transferable=True,
        expiry=None,
        verifiable=True,
        attributes={'payments': "['10Jun2023', '10Sep2023', '10Dec2023', '10Mar2024']"})
```

#### Issue. Postman request from node=Authority:
```
{'clientRequestId': '37034.1692871320.855731', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'Government Bond 2024', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'true', 'verifiable': 'true', 'quantity': 10, 'attributes': {'payments': "['10Jun2026', '10Sep2026', '10Dec2026', '10Mar2027']"}}}
```

---

### Step 2: Transfer (Expected Success)
* The owning node=Alice, is now going to transfer four bonds (quantity=4) to node=Charlie
* Flow=Transfer
 * Not all instruments are transferable.
 * If transferable -- will work on the basic nature of the instrument decided right from the issue point(by the issuer).
 * Check = not expired apart from being owned. 

#### Transfer. Python3/Jupyter call:
```
h.message("Transfer of Bond (expected success)")
(req_id, response, uuid_new_bond) = h.transfer(uuid_bond, 'Alice', 'Charlie', quantity=4)
```

#### Transfer. Postman request from node=Alice:
```
{'clientRequestId': '37034.1692871472.970092', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': 'cf8cd64a-bb59-4efe-85c2-b7f4ec125c20', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB', 'quantity': 4}}
```

#### Query Check. Python3/Jupyter call:
```
df_alice  = h.query('Alice')
df_alice  = h.query('Charlie')
```

#### Query Check. Postman request:
```
{'clientRequestId': '37034.1692871571.1036139', 'flowClassName': 'com.r3.developers.configurableInstrument.query.ListInstrument', 'requestBody': {}}
```

#### Output from node=Alice
```
{'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871571.1036139', 'flowId': '286d0f7a-03ff-4b19-9662-955d9acff0ef', 'flowStatus': 'COMPLETED', 'flowResult': '[{"id":"cf8cd64a-bb59-4efe-85c2-b7f4ec125c20","name":"Government Bond 2024","owner":"CN=Alice, OU=Test Dept, O=R3, L=London, C=GB","issuer":"CN=Authority, OU=Test Dept, O=R3, L=London, C=GB","quantity":6,"transferable":true,"expiry":null,"verifiable":true,"attributes":{"payments":"[\'10Jun2023\', \'10Sep2023\', \'10Dec2023\', \'10Mar2024\']"}}]', 'flowError': None, 'timestamp': '2023-08-24T10:06:12.487Z'}
```

#### Formatted Output from node=Alice
```
name         : Government Bond 2024
owner        : CN=Alice, OU=Test Dept, O=R3, L=London, C=GB
issuer       : CN=Authority, OU=Test Dept, O=R3, L=London, C=GB
quantity     : 6
expiry       : null
transferable : true
verifiable   : true
attributes   : {"payments":"['10Jun2023', '10Sep2023', '10Dec2023', '10Mar2024']"}}
```

#### Formatted Output from node=Charlie
```
name         : Government Bond 2024
owner        : CN=Alice, OU=Test Dept, O=R3, L=London, C=GB
issuer       : CN=Authority, OU=Test Dept, O=R3, L=London, C=GB
quantity     : 4
expiry       : null
transferable : true
verifiable   : true
attributes   : {"payments":"['10Jun2023', '10Sep2023', '10Dec2023', '10Mar2024']"}}
```

---

### Step 3: Redeem(Consume)
* Flow=Redeem/Settle/Expire/Mature/Consume/Spend
 * Not all instruments will have expiry/maturity.
 * Redeem can be executed by either the owner (holder of the asset) or also by the issuer of the asset (present design, can be controlled)
 * If permitted, it will work on the basic nature of the instrument decided right from the issue point(by the issuer).

#### Redeem. Python3/Jupyter call:
```
h.message("Redeem of Bond (expected success)")
h.redeem(uuid_bond, 'Alice', quantity=1)
```

#### Redeem. Postman request from node=Alice:
```
{'clientRequestId': '36552.1696498351.415508', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': 'd0f0dc0e-b67c-4d27-b335-a091a5ed7c7d', 'quantity': 1}}
```

---

### Issue logs
```
 24-08 15:32:00 | I | Issuing instrument='Government Bond 2024' to 'Alice'
 24-08 15:32:00 | I | Running action 'Issue' on 'Authority/9FA89008DEEE/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 24-08 15:32:00 | D | Request type=post to url='https://localhost:8888/api/v1/flow/9FA89008DEEE'
 24-08 15:32:00 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Issue', 'requestBody': {'name': 'Government Bond 2024', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'true', 'verifiable': 'true', 'quantity': 10, 'attributes': {'payments': "['10Jun2023', '10Sep2023', '10Dec2023', '10Mar2024']"}}}
 24-08 15:32:00 | D | {'clientRequestId': '37034.1692871320.855731', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'Government Bond 2024', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'true', 'verifiable': 'true', 'quantity': 10, 'attributes': {'payments': "['10Jun2023', '10Sep2023', '10Dec2023', '10Mar2024']"}}}
 24-08 15:32:00 | D | After filling values = {'clientRequestId': '37034.1692871320.855731', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'Government Bond 2024', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'true', 'verifiable': 'true', 'quantity': 10, 'attributes': {'payments': "['10Jun2023', '10Sep2023', '10Dec2023', '10Mar2024']"}}}
 24-08 15:32:00 | D | 202
 24-08 15:32:00 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:00.915Z'}
 24-08 15:32:04 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:04 | D | 200
 24-08 15:32:04 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:01.250Z'}
 24-08 15:32:08 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:09 | D | 200
 24-08 15:32:09 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:01.250Z'}
 24-08 15:32:13 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:13 | D | 200
 24-08 15:32:13 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:01.250Z'}
 24-08 15:32:17 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:17 | D | 200
 24-08 15:32:17 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:01.250Z'}
 24-08 15:32:21 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:21 | D | 200
 24-08 15:32:21 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:01.250Z'}
 24-08 15:32:25 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:25 | D | 200
 24-08 15:32:25 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:01.250Z'}
 24-08 15:32:29 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:29 | D | 200
 24-08 15:32:29 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:01.250Z'}
 24-08 15:32:33 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:33 | D | 200
 24-08 15:32:33 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:01.250Z'}
 24-08 15:32:37 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:37 | D | 200
 24-08 15:32:37 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:02:01.250Z'}
 24-08 15:32:41 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/37034.1692871320.855731'
 24-08 15:32:41 | D | 200
 24-08 15:32:41 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '37034.1692871320.855731', 'flowId': '4d072066-034e-4123-aa54-bb4cd79b4a77', 'flowStatus': 'COMPLETED', 'flowResult': 'cf8cd64a-bb59-4efe-85c2-b7f4ec125c20', 'flowError': None, 'timestamp': '2023-08-24T10:02:41.185Z'}
 24-08 15:32:41 | I | cf8cd64a-bb59-4efe-85c2-b7f4ec125c20
```

### Transfer logs
```
 24-08 15:34:32 | I | Tranfering instrument id 'cf8cd64a-bb59-4efe-85c2-b7f4ec125c20' to 'Charlie'
 24-08 15:34:32 | I | Running action 'Transfer' on 'Alice/BAA7F076B971/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 24-08 15:34:32 | D | Request type=post to url='https://localhost:8888/api/v1/flow/BAA7F076B971'
 24-08 15:34:32 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Transfer', 'requestBody': {'id': '__TRANSFER_ASSET_ID__', 'to': '__TRANSFER_TO__', 'quantity': 4}}
 24-08 15:34:32 | D | {'clientRequestId': '37034.1692871472.970092', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': 'cf8cd64a-bb59-4efe-85c2-b7f4ec125c20', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB', 'quantity': 4}}
 24-08 15:34:32 | D | After filling values = {'clientRequestId': '37034.1692871472.970092', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': 'cf8cd64a-bb59-4efe-85c2-b7f4ec125c20', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB', 'quantity': 4}}
 24-08 15:34:33 | D | 202
 24-08 15:34:33 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.010Z'}
 24-08 15:34:37 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:34:37 | D | 200
 24-08 15:34:37 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:34:41 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:34:41 | D | 200
 24-08 15:34:41 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:34:45 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:34:45 | D | 200
 24-08 15:34:45 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:34:49 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:34:49 | D | 200
 24-08 15:34:49 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:34:53 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:34:53 | D | 200
 24-08 15:34:53 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:34:57 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:34:57 | D | 200
 24-08 15:34:57 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:35:01 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:35:01 | D | 200
 24-08 15:35:01 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:35:05 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:35:05 | D | 200
 24-08 15:35:05 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:35:09 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:35:09 | D | 200
 24-08 15:35:09 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:35:13 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:35:13 | D | 200
 24-08 15:35:13 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-08-24T10:04:33.271Z'}
 24-08 15:35:17 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/37034.1692871472.970092'
 24-08 15:35:17 | D | 200
 24-08 15:35:17 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '37034.1692871472.970092', 'flowId': 'ec41af79-49cf-47d1-969d-b4ed55878974', 'flowStatus': 'COMPLETED', 'flowResult': '464c6085-0dca-4c82-897c-02425d55aa9e', 'flowError': None, 'timestamp': '2023-08-24T10:05:14.485Z'}
 24-08 15:35:17 | I | 464c6085-0dca-4c82-897c-02425d55aa9e
```

### Redeem logs
```
 05-10 15:02:31 | I | Redeeming instrument id 'd0f0dc0e-b67c-4d27-b335-a091a5ed7c7d' quantity '1'
 05-10 15:02:31 | I | Running action 'Redeem' on 'Alice/BAA7F076B971/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 05-10 15:02:31 | D | Request type=post to url='https://localhost:8888/api/v1/flow/BAA7F076B971'
 05-10 15:02:31 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Redeem', 'requestBody': {'id': '__REDEEM_ASSET_ID__', 'quantity': 1}}
 05-10 15:02:31 | D | {'clientRequestId': '36552.1696498351.415508', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': 'd0f0dc0e-b67c-4d27-b335-a091a5ed7c7d', 'quantity': 1}}
 05-10 15:02:31 | D | After filling values = {'clientRequestId': '36552.1696498351.415508', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': 'd0f0dc0e-b67c-4d27-b335-a091a5ed7c7d', 'quantity': 1}}
 05-10 15:02:31 | D | 202
 05-10 15:02:31 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498351.415508', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:31.435Z'}
 05-10 15:02:35 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498351.415508'
 05-10 15:02:35 | D | 200
 05-10 15:02:35 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498351.415508', 'flowId': '2a8fc80f-9e66-4012-9bed-7c49d584283f', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:31.602Z'}
 05-10 15:02:39 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498351.415508'
 05-10 15:02:39 | D | 200
 05-10 15:02:39 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498351.415508', 'flowId': '2a8fc80f-9e66-4012-9bed-7c49d584283f', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:31.602Z'}
 05-10 15:02:43 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498351.415508'
 05-10 15:02:43 | D | 200
 05-10 15:02:43 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498351.415508', 'flowId': '2a8fc80f-9e66-4012-9bed-7c49d584283f', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:31.602Z'}
 05-10 15:02:47 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498351.415508'
 05-10 15:02:47 | D | 200
 05-10 15:02:47 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498351.415508', 'flowId': '2a8fc80f-9e66-4012-9bed-7c49d584283f', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:31.602Z'}
 05-10 15:02:51 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498351.415508'
 05-10 15:02:51 | D | 200
 05-10 15:02:51 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498351.415508', 'flowId': '2a8fc80f-9e66-4012-9bed-7c49d584283f', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:31.602Z'}
 05-10 15:02:55 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498351.415508'
 05-10 15:02:55 | D | 200
 05-10 15:02:55 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498351.415508', 'flowId': '2a8fc80f-9e66-4012-9bed-7c49d584283f', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:31.602Z'}
 05-10 15:02:59 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498351.415508'
 05-10 15:02:59 | D | 200
 05-10 15:02:59 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498351.415508', 'flowId': '2a8fc80f-9e66-4012-9bed-7c49d584283f', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:31.602Z'}
 05-10 15:03:03 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498351.415508'
 05-10 15:03:03 | D | 200
 05-10 15:03:03 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498351.415508', 'flowId': '2a8fc80f-9e66-4012-9bed-7c49d584283f', 'flowStatus': 'COMPLETED', 'flowResult': 'net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@106943aa', 'flowError': None, 'timestamp': '2023-10-05T09:33:01.643Z'}
 05-10 15:03:03 | I | net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@106943aa
```
