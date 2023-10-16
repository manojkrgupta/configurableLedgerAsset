### Story 4(Use case 4) : Graduation certificate
* Quantifiable=False (quantity=None)
* Transferable=False (transferable=False)
* Expiry=No          (expiry=None)
* Verifiable=True    (verifiable=True)

---

### General Information
* Any node can issue a instrument to any other node
* Based on whether transferable(or not), the owning node can transfer the asset(instrument) to any other node.
* Based on whether quantifiable(or not), the asset(instrument) can be transferred(or consumed) in portion or as a whole.
 * Quantifiable as a flag(control) is decided at the time of the issue of the instrument, by setting a value to quantity. No value for attribute=quantity, makes it non-quantifiable.

---

### Step 1: Issue (Expected Success)
* Node=Authority(University in this case) is issuing/vouch for/certifying/granting instrument='Graduation certificate' to node=Charlie
* Flow=Issue
 * Issuer gets to decide the name, transferable or not, expiry or not, redeemable or not, and can add multiple/additional attributes (HashMap) on the same State/Asset.
 * Applications like Government Bond, will be transferable, with maturity(some expiry), and redeemable (cash the principal on maturity), with additional attribute of coupon payment dates.
 * Applications like College University Degree, will not be transferable, no expiry, and not redeemable. Will have additional attributes like Collage Name, University Name, Education Stream etc etc along with Issuer and Owner(Holder).
 * Applications like Limited Edition Sovereign, will be transferable, no expiry but will be redeemable directly with Issuer.

#### Issue. Python3/Jupyter call:
```
h.message("Graduation certificate")
(req_id, response, uuid_cert) = h.issue('Authority', 'Charlie', 'BE Computer Engineering', quantity=None, transferable=False, expiry=None, verifiable=True,
        attributes={
            'university': 'University of Mumbai', 
            'year': '2023',
            'score': '450/500',
            'major subject': "['Robotics', 'AI', 'DSP']"})
```

#### Issue. Postman request from node=Authority(can a University or any certifying Institute):
```
{'clientRequestId': '36552.1696498008.9060092', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'BE Computer Engineering', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'false', 'verifiable': 'true', 'attributes': {'university': 'University of Mumbai', 'year': '2023', 'score': '450/500', 'major subject': "['Robotics', 'AI', 'DSP']"}}}
```

---

### Step 2: Transfer (Expected Failure)
* The owning node=Charlie, is now attempting to transfer the certificate to node=Charlie, but this should fail, since its a non-transaferable instrument.
* Flow=Transfer
 * Not all instruments are transferable.
 * If transferable -- will work on the basic nature of the instrument decided right from the issue point(by the issuer).
 * Check = not expired apart from being owned. 

#### Transfer. Python3/Jupyter call:
```
h.message("Transfer of Graduation certificate (expected failure)")
(req_id, response, uuid_new) = h.transfer(uuid_cert, 'Charlie', 'Alice')
```

#### Transfer. Postman request from node=Charlie:
```
{'clientRequestId': '36552.1696498294.601697', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': '28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'}}
```

---

### Step 3: Redeem(Consume). Expected Failure
* Flow=Redeem/Settle/Expire/Mature/Consume/Spend
 * Not all instruments will have expiry/maturity.
 * Redeem can be executed by either the owner (holder of the asset) or also by the issuer of the asset (present design, can be controlled)
 * If permitted, it will work on the basic nature of the instrument decided right from the issue point(by the issuer).

#### Redeem. Python3/Jupyter call:
```
h.message("Redeeming 'BE Computer Engineering' (expected failure)")
h.redeem(uuid_cert, 'Charlie')
```

#### Redeem. Postman request from node=Alice:
```
{'clientRequestId': '36552.1696498351.415508', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': 'd0f0dc0e-b67c-4d27-b335-a091a5ed7c7d', 'quantity': 1}}
```

---

### Issue logs
```
 05-10 14:56:48 | I | Issuing instrument='BE Computer Engineering' to 'Charlie'
 05-10 14:56:48 | I | Running action 'Issue' on 'Authority/9FA89008DEEE/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 05-10 14:56:48 | D | Request type=post to url='https://localhost:8888/api/v1/flow/9FA89008DEEE'
 05-10 14:56:48 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Issue', 'requestBody': {'name': 'BE Computer Engineering', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'false', 'verifiable': 'true', 'attributes': {'university': 'University of Mumbai', 'year': '2023', 'score': '450/500', 'major subject': "['Robotics', 'AI', 'DSP']"}}}
 05-10 14:56:48 | D | {'clientRequestId': '36552.1696498008.9060092', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'BE Computer Engineering', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'false', 'verifiable': 'true', 'attributes': {'university': 'University of Mumbai', 'year': '2023', 'score': '450/500', 'major subject': "['Robotics', 'AI', 'DSP']"}}}
 05-10 14:56:48 | D | After filling values = {'clientRequestId': '36552.1696498008.9060092', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'BE Computer Engineering', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'false', 'verifiable': 'true', 'attributes': {'university': 'University of Mumbai', 'year': '2023', 'score': '450/500', 'major subject': "['Robotics', 'AI', 'DSP']"}}}
 05-10 14:56:48 | D | 202
 05-10 14:56:48 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696498008.9060092', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:48.929Z'}
 05-10 14:56:52 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696498008.9060092'
 05-10 14:56:52 | D | 200
 05-10 14:56:52 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696498008.9060092', 'flowId': '1033f8ad-81bd-42db-a2b9-af1ecc02b9ae', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:49.258Z'}
 05-10 14:56:56 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696498008.9060092'
 05-10 14:56:57 | D | 200
 05-10 14:56:57 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696498008.9060092', 'flowId': '1033f8ad-81bd-42db-a2b9-af1ecc02b9ae', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:49.258Z'}
 05-10 14:57:01 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696498008.9060092'
 05-10 14:57:01 | D | 200
 05-10 14:57:01 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696498008.9060092', 'flowId': '1033f8ad-81bd-42db-a2b9-af1ecc02b9ae', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:49.258Z'}
 05-10 14:57:05 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696498008.9060092'
 05-10 14:57:05 | D | 200
 05-10 14:57:05 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696498008.9060092', 'flowId': '1033f8ad-81bd-42db-a2b9-af1ecc02b9ae', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:49.258Z'}
 05-10 14:57:09 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696498008.9060092'
 05-10 14:57:09 | D | 200
 05-10 14:57:09 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696498008.9060092', 'flowId': '1033f8ad-81bd-42db-a2b9-af1ecc02b9ae', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:49.258Z'}
 05-10 14:57:13 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696498008.9060092'
 05-10 14:57:13 | D | 200
 05-10 14:57:13 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696498008.9060092', 'flowId': '1033f8ad-81bd-42db-a2b9-af1ecc02b9ae', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:49.258Z'}
 05-10 14:57:17 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696498008.9060092'
 05-10 14:57:17 | D | 200
 05-10 14:57:17 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696498008.9060092', 'flowId': '1033f8ad-81bd-42db-a2b9-af1ecc02b9ae', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:49.258Z'}
 05-10 14:57:21 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696498008.9060092'
 05-10 14:57:21 | D | 200
 05-10 14:57:21 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696498008.9060092', 'flowId': '1033f8ad-81bd-42db-a2b9-af1ecc02b9ae', 'flowStatus': 'COMPLETED', 'flowResult': '9eaa5900-59f8-40d7-a25c-c89d146b15f9', 'flowError': None, 'timestamp': '2023-10-05T09:27:20.609Z'}
 05-10 14:57:21 | I | 9eaa5900-59f8-40d7-a25c-c89d146b15f9
```

### Transfer logs
```
 05-10 15:02:23 | I | Tranfering instrument id '9eaa5900-59f8-40d7-a25c-c89d146b15f9' to 'Alice'
 05-10 15:02:23 | I | Running action 'Transfer' on 'Charlie/0AA37CC89C79/CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'
 05-10 15:02:23 | D | Request type=post to url='https://localhost:8888/api/v1/flow/0AA37CC89C79'
 05-10 15:02:23 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Transfer', 'requestBody': {'id': '__TRANSFER_ASSET_ID__', 'to': '__TRANSFER_TO__'}}
 05-10 15:02:23 | D | {'clientRequestId': '36552.1696498343.2683609', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': '9eaa5900-59f8-40d7-a25c-c89d146b15f9', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'}}
 05-10 15:02:23 | D | After filling values = {'clientRequestId': '36552.1696498343.2683609', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': '9eaa5900-59f8-40d7-a25c-c89d146b15f9', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'}}
 05-10 15:02:23 | D | 202
 05-10 15:02:23 | D | {'holdingIdentityShortHash': '0AA37CC89C79', 'clientRequestId': '36552.1696498343.2683609', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:23.296Z'}
 05-10 15:02:27 | D | Request type=get to url='https://localhost:8888/api/v1/flow/0AA37CC89C79/36552.1696498343.2683609'
 05-10 15:02:27 | D | 200
 05-10 15:02:27 | D | {'holdingIdentityShortHash': '0AA37CC89C79', 'clientRequestId': '36552.1696498343.2683609', 'flowId': 'ef796277-431a-42b9-8a7b-14c5ef39774b', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:23.581Z'}
 05-10 15:02:31 | D | Request type=get to url='https://localhost:8888/api/v1/flow/0AA37CC89C79/36552.1696498343.2683609'
 05-10 15:02:31 | D | 200
 05-10 15:02:31 | D | {'holdingIdentityShortHash': '0AA37CC89C79', 'clientRequestId': '36552.1696498343.2683609', 'flowId': 'ef796277-431a-42b9-8a7b-14c5ef39774b', 'flowStatus': 'FAILED', 'flowResult': None, 'flowError': {'type': 'FLOW_FAILED', 'message': 'net.corda.v5.ledger.utxo.ContractVerificationException: Verification of ledger transaction with ID SHA-256D:18F7EA6D657B5A3BC9EE0A61CD7D15DFDED46CBBC1A8E0515E7EBFB974A666DD failed: net.corda.v5.ledger.utxo.ContractVerificationException: Ledger transaction contract verification failed for the specified transaction: SHA-256D:18F7EA6D657B5A3BC9EE0A61CD7D15DFDED46CBBC1A8E0515E7EBFB974A666DD.\nThe following contract verification requirements were not met:\ncom.r3.developers.configurableInstrument.contracts.InstrumentContract: Failed requirement: Instrument is not transferable.\n'}, 'timestamp': '2023-10-05T09:32:27.611Z'}
 05-10 15:02:31 | I | {'type': 'FLOW_FAILED', 'message': 'net.corda.v5.ledger.utxo.ContractVerificationException: Verification of ledger transaction with ID SHA-256D:18F7EA6D657B5A3BC9EE0A61CD7D15DFDED46CBBC1A8E0515E7EBFB974A666DD failed: net.corda.v5.ledger.utxo.ContractVerificationException: Ledger transaction contract verification failed for the specified transaction: SHA-256D:18F7EA6D657B5A3BC9EE0A61CD7D15DFDED46CBBC1A8E0515E7EBFB974A666DD.\nThe following contract verification requirements were not met:\ncom.r3.developers.configurableInstrument.contracts.InstrumentContract: Failed requirement: Instrument is not transferable.\n'}
 05-10 15:02:31 | I | Time taken = 0:00:08.136343
```

### Redeem logs
```
 05-10 15:03:40 | I | Redeeming instrument id '0fb152f0-805c-4d63-a889-3485c92df378' quantity '1'
 05-10 15:03:40 | I | Running action 'Redeem' on 'Alice/BAA7F076B971/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 05-10 15:03:40 | D | Request type=post to url='https://localhost:8888/api/v1/flow/BAA7F076B971'
 05-10 15:03:40 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Redeem', 'requestBody': {'id': '__REDEEM_ASSET_ID__', 'quantity': 1}}
 05-10 15:03:40 | D | {'clientRequestId': '36552.1696498420.089261', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': '0fb152f0-805c-4d63-a889-3485c92df378', 'quantity': 1}}
 05-10 15:03:40 | D | After filling values = {'clientRequestId': '36552.1696498420.089261', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': '0fb152f0-805c-4d63-a889-3485c92df378', 'quantity': 1}}
 05-10 15:03:40 | D | 202
 05-10 15:03:40 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498420.089261', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:33:40.108Z'}
 05-10 15:03:44 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498420.089261'
 05-10 15:03:44 | D | 200
 05-10 15:03:44 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498420.089261', 'flowId': '7ee180c7-d010-47ee-96c6-d69cf2c358da', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:33:40.432Z'}
 05-10 15:03:48 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498420.089261'
 05-10 15:03:48 | D | 200
 05-10 15:03:48 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498420.089261', 'flowId': '7ee180c7-d010-47ee-96c6-d69cf2c358da', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:33:40.432Z'}
 05-10 15:03:52 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498420.089261'
 05-10 15:03:52 | D | 200
 05-10 15:03:52 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498420.089261', 'flowId': '7ee180c7-d010-47ee-96c6-d69cf2c358da', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:33:40.432Z'}
 05-10 15:03:56 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498420.089261'
 05-10 15:03:56 | D | 200
 05-10 15:03:56 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498420.089261', 'flowId': '7ee180c7-d010-47ee-96c6-d69cf2c358da', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:33:40.432Z'}
 05-10 15:04:00 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498420.089261'
 05-10 15:04:00 | D | 200
 05-10 15:04:00 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498420.089261', 'flowId': '7ee180c7-d010-47ee-96c6-d69cf2c358da', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:33:40.432Z'}
 05-10 15:04:04 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498420.089261'
 05-10 15:04:04 | D | 200
 05-10 15:04:04 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498420.089261', 'flowId': '7ee180c7-d010-47ee-96c6-d69cf2c358da', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:33:40.432Z'}
 05-10 15:04:08 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498420.089261'
 05-10 15:04:08 | D | 200
 05-10 15:04:08 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498420.089261', 'flowId': '7ee180c7-d010-47ee-96c6-d69cf2c358da', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:33:40.432Z'}
 05-10 15:04:12 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498420.089261'
 05-10 15:04:12 | D | 200
 05-10 15:04:12 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498420.089261', 'flowId': '7ee180c7-d010-47ee-96c6-d69cf2c358da', 'flowStatus': 'COMPLETED', 'flowResult': 'net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@7ebb6a72', 'flowError': None, 'timestamp': '2023-10-05T09:34:09.520Z'}
 05-10 15:04:12 | I | net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@7ebb6a72
```


### Error, when node is not owning the asset
```
 05-10 18:17:43 | I | Redeeming instrument id '36e7e531-51ea-48a7-af6c-8e624f7e780a' quantity 'None'
 05-10 18:17:43 | I | Running action 'Redeem' on 'Alice/BAA7F076B971/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 05-10 18:17:43 | D | Request type=post to url='https://localhost:8888/api/v1/flow/BAA7F076B971'
 05-10 18:17:43 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Redeem', 'requestBody': {'id': '__REDEEM_ASSET_ID__'}}
 05-10 18:17:43 | D | {'clientRequestId': '51973.1696510063.204709', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': '36e7e531-51ea-48a7-af6c-8e624f7e780a'}}
 05-10 18:17:43 | D | After filling values = {'clientRequestId': '51973.1696510063.204709', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': '36e7e531-51ea-48a7-af6c-8e624f7e780a'}}
 05-10 18:17:43 | D | 202
 05-10 18:17:43 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '51973.1696510063.204709', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T12:47:43.232Z'}
 05-10 18:17:47 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/51973.1696510063.204709'
 05-10 18:17:47 | D | 200
 05-10 18:17:47 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '51973.1696510063.204709', 'flowId': 'a9589ef5-b4d0-4f91-8770-c9a073cfabaa', 'flowStatus': 'FAILED', 'flowResult': None, 'flowError': {'type': 'FLOW_FAILED', 'message': 'Not able to find a owning state with id 36e7e531-51ea-48a7-af6c-8e624f7e780a'}, 'timestamp': '2023-10-05T12:47:44.927Z'}
 05-10 18:17:47 | I | {'type': 'FLOW_FAILED', 'message': 'Not able to find a owning state with id 36e7e531-51ea-48a7-af6c-8e624f7e780a'}

('51973.1696510063.204709',
 <Response [200]>,
 {'type': 'FLOW_FAILED',
  'message': 'Not able to find a owning state with id 36e7e531-51ea-48a7-af6c-8e624f7e780a'})
```
