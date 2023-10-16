### Story 2(Use case 2) : Fiat currency with unique number in digital form.
* Quantifiable=False (quantity=None)
* Transferable=True  (transferable=True)
* Expiry=No          (expiry=None)
* Verifiable=True    (verifiable=True)

---

### General Information
* Any node can issue a instrument to any other node
* Based on whether transferable(or not), the owning node can transfer the asset(instrument) to any other node.
* Based on whether quantifiable(or not), the asset(instrument) can be transferred(or consumed) in portion or as a whole.
 * Quantifiable as a flag(control) is decided at the time of the issue of the instrument, by setting a value to quantity. No value for attribute=quantity, makes it non-quantifiable.
---
### Step 1: Issue
* Node=Authority is issuing instrument='Digital Currency INR 500 Note' to node=Alice
* Flow=Issue
 * Issuer gets to decide the name, transferable or not, expiry or not, redeemable or not, and can add multiple/additional attributes (HashMap) on the same State/Asset.
 * Applications like Government Bond, will be transferable, with maturity(some expiry), and redeemable (cash the principal on maturity), with additional attribute of coupon payment dates.
 * Applications like College University Degree, will not be transferable, no expiry, and not redeemable. Will have additional attributes like Collage Name, University Name, Education Stream etc etc along with Issuer and Owner(Holder).
 * Applications like Limited Edition Sovereign, will be transferable, no expiry but will be redeemable directly with Issuer.

#### Issue. Python3/Jupyter call:
```
h.message("Fiat currency with unique number in digital form.")
(req_id, response, uuid_fiat) = h.issue('Authority', 'Alice', 'Digital Currency INR 500 Note',
        quantity=None, 
        transferable=True, 
        expiry=None, 
        verifiable=True, 
        attributes={'number': 'OMV 336048', 'year': '1981'})
```

#### Issue. Postman request from node=Authority:
```
{'clientRequestId': '36552.1696497944.1001952', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'Digital Currency INR 500 Note', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'true', 'verifiable': 'true', 'attributes': {'number': 'OMV 336048', 'year': '1981'}}}
```

---

### Step 2: Transfer
* The owning node=Alice, is now going to transfer currency to node=Charlie
* Flow=Transfer
 * Not all instruments are transferable.
 * If transferable -- will work on the basic nature of the instrument decided right from the issue point(by the issuer).
 * Check = not expired apart from being owned. 

#### Transfer. Python3/Jupyter call:
```
h.message("Transfer of Fiat Currency (expected success)")
(req_id, response, uuid_new) = h.transfer(uuid_fiat, 'Alice', 'Charlie')
```

#### Transfer. Postman request from node=Alice:
```
{'clientRequestId': '36552.1696498294.601697', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': '28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'}}
```

#### Query Check. Python3/Jupyter call:
```
df_alice    = h.query('Alice')
df_charlie  = h.query('Charlie')
```

#### Query Check. Python3/Jupyter call:
```
{'clientRequestId': '37034.1692871571.1036139', 'flowClassName': 'com.r3.developers.configurableInstrument.query.ListInstrument', 'requestBody': {}}
```

#### Output
* The instrument should not be visible in output from Alice, but it should be visible in output from Charlie

---

### Step 3: Redeem(Consume)
* Flow=Redeem/Settle/Expire/Mature/Consume/Spend
 * Not all instruments will have expiry/maturity.
 * Redeem can be executed by either the owner (holder of the asset) or also by the issuer of the asset (present design, can be controlled)
 * If permitted, it will work on the basic nature of the instrument decided right from the issue point(by the issuer).

#### Redeem. Python3/Jupyter call:
```
h.message("Redeem of Fiat Currency (expected success)")
h.redeem(uuid_fiat, 'Charlie')
```

#### Redeem. Postman request from node=Alice:
```
{'clientRequestId': '36552.1696498351.415508', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': 'd0f0dc0e-b67c-4d27-b335-a091a5ed7c7d', 'quantity': 1}}
```

---
### Issue logs
```
 05-10 14:55:44 | I | Issuing instrument='Digital Currency INR 500 Note' to 'Alice'
 05-10 14:55:44 | I | Running action 'Issue' on 'Authority/9FA89008DEEE/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 05-10 14:55:44 | D | Request type=post to url='https://localhost:8888/api/v1/flow/9FA89008DEEE'
 05-10 14:55:44 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Issue', 'requestBody': {'name': 'Digital Currency INR 500 Note', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'true', 'verifiable': 'true', 'attributes': {'number': 'OMV 336048', 'year': '1981'}}}
 05-10 14:55:44 | D | {'clientRequestId': '36552.1696497944.1001952', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'Digital Currency INR 500 Note', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'true', 'verifiable': 'true', 'attributes': {'number': 'OMV 336048', 'year': '1981'}}}
 05-10 14:55:44 | D | After filling values = {'clientRequestId': '36552.1696497944.1001952', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'Digital Currency INR 500 Note', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'true', 'verifiable': 'true', 'attributes': {'number': 'OMV 336048', 'year': '1981'}}}
 05-10 14:55:44 | D | 202
 05-10 14:55:44 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497944.1001952', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:25:44.118Z'}
 05-10 14:55:48 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497944.1001952'
 05-10 14:55:48 | D | 200
 05-10 14:55:48 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497944.1001952', 'flowId': 'd835f426-21e4-42b5-b219-8405b3785318', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:25:44.556Z'}
 05-10 14:55:52 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497944.1001952'
 05-10 14:55:52 | D | 200
 05-10 14:55:52 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497944.1001952', 'flowId': 'd835f426-21e4-42b5-b219-8405b3785318', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:25:44.556Z'}
 05-10 14:55:56 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497944.1001952'
 05-10 14:55:56 | D | 200
 05-10 14:55:56 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497944.1001952', 'flowId': 'd835f426-21e4-42b5-b219-8405b3785318', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:25:44.556Z'}
 05-10 14:56:00 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497944.1001952'
 05-10 14:56:00 | D | 200
 05-10 14:56:00 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497944.1001952', 'flowId': 'd835f426-21e4-42b5-b219-8405b3785318', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:25:44.556Z'}
 05-10 14:56:04 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497944.1001952'
 05-10 14:56:04 | D | 200
 05-10 14:56:04 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497944.1001952', 'flowId': 'd835f426-21e4-42b5-b219-8405b3785318', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:25:44.556Z'}
 05-10 14:56:08 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497944.1001952'
 05-10 14:56:08 | D | 200
 05-10 14:56:08 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497944.1001952', 'flowId': 'd835f426-21e4-42b5-b219-8405b3785318', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:25:44.556Z'}
 05-10 14:56:12 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497944.1001952'
 05-10 14:56:12 | D | 200
 05-10 14:56:12 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497944.1001952', 'flowId': 'd835f426-21e4-42b5-b219-8405b3785318', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:25:44.556Z'}
 05-10 14:56:16 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497944.1001952'
 05-10 14:56:16 | D | 200
 05-10 14:56:16 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497944.1001952', 'flowId': 'd835f426-21e4-42b5-b219-8405b3785318', 'flowStatus': 'COMPLETED', 'flowResult': '28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7', 'flowError': None, 'timestamp': '2023-10-05T09:26:13.657Z'}
 05-10 14:56:16 | I | 28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7
```

### Transfer logs
```
 05-10 15:01:34 | I | Tranfering instrument id '28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7' to 'Charlie'
 05-10 15:01:34 | I | Running action 'Transfer' on 'Alice/BAA7F076B971/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 05-10 15:01:34 | D | Request type=post to url='https://localhost:8888/api/v1/flow/BAA7F076B971'
 05-10 15:01:34 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Transfer', 'requestBody': {'id': '__TRANSFER_ASSET_ID__', 'to': '__TRANSFER_TO__'}}
 05-10 15:01:34 | D | {'clientRequestId': '36552.1696498294.601697', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': '28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'}}
 05-10 15:01:34 | D | After filling values = {'clientRequestId': '36552.1696498294.601697', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': '28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'}}
 05-10 15:01:34 | D | 202
 05-10 15:01:34 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:34.622Z'}
 05-10 15:01:38 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:01:38 | D | 200
 05-10 15:01:38 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:35.056Z'}
 05-10 15:01:42 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:01:42 | D | 200
 05-10 15:01:42 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:35.056Z'}
 05-10 15:01:46 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:01:46 | D | 200
 05-10 15:01:46 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:35.056Z'}
 05-10 15:01:50 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:01:50 | D | 200
 05-10 15:01:50 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:35.056Z'}
 05-10 15:01:54 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:01:54 | D | 200
 05-10 15:01:54 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:35.056Z'}
 05-10 15:01:58 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:01:58 | D | 200
 05-10 15:01:58 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:35.056Z'}
 05-10 15:02:02 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:02:02 | D | 200
 05-10 15:02:02 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:35.056Z'}
 05-10 15:02:06 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:02:07 | D | 200
 05-10 15:02:07 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:35.056Z'}
 05-10 15:02:11 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:02:11 | D | 200
 05-10 15:02:11 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:31:35.056Z'}
 05-10 15:02:15 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498294.601697'
 05-10 15:02:15 | D | 200
 05-10 15:02:15 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498294.601697', 'flowId': 'aa4672f9-2c73-47e0-963f-5168c59ba2ef', 'flowStatus': 'COMPLETED', 'flowResult': '28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7', 'flowError': None, 'timestamp': '2023-10-05T09:32:12.884Z'}
 05-10 15:02:15 | I | 28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7
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

