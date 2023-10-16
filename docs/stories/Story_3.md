### Story 3(Use case 3) : Amazon Vouchers
* Quantifiable=True  (quantity=200)
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

### Step 1: Issue
* Node=Authority is issuing 200 instrument='Amazon Voucher' to node=Alice
* Flow=Issue
 * Issuer gets to decide the name, transferable or not, expiry or not, redeemable or not, and can add multiple/additional attributes (HashMap) on the same State/Asset.
 * Applications like Government Bond, will be transferable, with maturity(some expiry), and redeemable (cash the principal on maturity), with additional attribute of coupon payment dates.
 * Applications like College University Degree, will not be transferable, no expiry, and not redeemable. Will have additional attributes like Collage Name, University Name, Education Stream etc etc along with Issuer and Owner(Holder).
 * Applications like Limited Edition Sovereign, will be transferable, no expiry but will be redeemable directly with Issuer.

#### Issue. Python3/Jupyter call:
```
h.message("Amazon Vouchers")
(req_id, response, uuid_amazon) = h.issue('Authority', 'Alice', 'Amazon Voucher', 
        quantity=200,
        transferable=False,
        expiry=None,
        verifiable=True,
        attributes={'currency': 'INR'})
```

#### Issue. Postman request from node=Authority:
```
{'clientRequestId': '36552.1696497976.524884', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'Amazon Voucher', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'false', 'verifiable': 'true', 'quantity': 200, 'attributes': {'currency': 'INR'}}}
```
---

### Step 2: Transfer (Expected Failure)
* The owning node=Alice, is now attempting to transfer four Amazon Voucher to node=Charlie, but this should fail, since its a non-transaferable instrument.
* Flow=Transfer
 * Not all instruments are transferable.
 * If transferable -- will work on the basic nature of the instrument decided right from the issue point(by the issuer).
 * Check = not expired apart from being owned. 

#### Transfer. Python3/Jupyter call:
```
h.message("Transfer of Amazon Voucher (expected failure)")
(req_id, response, uuid_new) = h.transfer(uuid_amazon, 'Alice', 'Charlie', quantity=4)
```

#### Transfer. Postman request from node=Alice:
```
{'clientRequestId': '36552.1696498294.601697', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': '28f10fb0-9e2b-4ab0-9fdb-1573565cb3c7', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'}}
```

---

### Step 3: Redeem(Consume)
* Flow=Redeem/Settle/Expire/Mature/Consume/Spend
 * Not all instruments will have expiry/maturity.
 * Redeem can be executed by either the owner (holder of the asset) or also by the issuer of the asset (present design, can be controlled)
 * If permitted, it will work on the basic nature of the instrument decided right from the issue point(by the issuer).

#### Redeem. Python3/Jupyter call:
```
h.message("Redeem of Amazon Voucher (expected success)")
h.redeem(uuid_amazon, 'Alice', quantity=1)
```

#### Redeem. Postman request from node=Alice:
```
{'clientRequestId': '36552.1696498351.415508', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Redeem', 'requestBody': {'id': 'd0f0dc0e-b67c-4d27-b335-a091a5ed7c7d', 'quantity': 1}}
```

---

### Issue logs
```
 05-10 14:56:16 | I | Issuing instrument='Amazon Voucher' to 'Alice'
 05-10 14:56:16 | I | Running action 'Issue' on 'Authority/9FA89008DEEE/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 05-10 14:56:16 | D | Request type=post to url='https://localhost:8888/api/v1/flow/9FA89008DEEE'
 05-10 14:56:16 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Issue', 'requestBody': {'name': 'Amazon Voucher', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'false', 'verifiable': 'true', 'quantity': 200, 'attributes': {'currency': 'INR'}}}
 05-10 14:56:16 | D | {'clientRequestId': '36552.1696497976.524884', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'Amazon Voucher', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'false', 'verifiable': 'true', 'quantity': 200, 'attributes': {'currency': 'INR'}}}
 05-10 14:56:16 | D | After filling values = {'clientRequestId': '36552.1696497976.524884', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Issue', 'requestBody': {'name': 'Amazon Voucher', 'to': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB', 'transferable': 'false', 'verifiable': 'true', 'quantity': 200, 'attributes': {'currency': 'INR'}}}
 05-10 14:56:16 | D | 202
 05-10 14:56:16 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497976.524884', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:16.545Z'}
 05-10 14:56:20 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497976.524884'
 05-10 14:56:20 | D | 200
 05-10 14:56:20 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497976.524884', 'flowId': '776f4778-29bf-4e66-8706-ab2789ccabd3', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:16.903Z'}
 05-10 14:56:24 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497976.524884'
 05-10 14:56:24 | D | 200
 05-10 14:56:24 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497976.524884', 'flowId': '776f4778-29bf-4e66-8706-ab2789ccabd3', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:16.903Z'}
 05-10 14:56:28 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497976.524884'
 05-10 14:56:28 | D | 200
 05-10 14:56:28 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497976.524884', 'flowId': '776f4778-29bf-4e66-8706-ab2789ccabd3', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:16.903Z'}
 05-10 14:56:32 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497976.524884'
 05-10 14:56:32 | D | 200
 05-10 14:56:32 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497976.524884', 'flowId': '776f4778-29bf-4e66-8706-ab2789ccabd3', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:16.903Z'}
 05-10 14:56:36 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497976.524884'
 05-10 14:56:36 | D | 200
 05-10 14:56:36 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497976.524884', 'flowId': '776f4778-29bf-4e66-8706-ab2789ccabd3', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:16.903Z'}
 05-10 14:56:40 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497976.524884'
 05-10 14:56:40 | D | 200
 05-10 14:56:40 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497976.524884', 'flowId': '776f4778-29bf-4e66-8706-ab2789ccabd3', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:16.903Z'}
 05-10 14:56:44 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497976.524884'
 05-10 14:56:44 | D | 200
 05-10 14:56:44 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497976.524884', 'flowId': '776f4778-29bf-4e66-8706-ab2789ccabd3', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:26:16.903Z'}
 05-10 14:56:48 | D | Request type=get to url='https://localhost:8888/api/v1/flow/9FA89008DEEE/36552.1696497976.524884'
 05-10 14:56:48 | D | 200
 05-10 14:56:48 | D | {'holdingIdentityShortHash': '9FA89008DEEE', 'clientRequestId': '36552.1696497976.524884', 'flowId': '776f4778-29bf-4e66-8706-ab2789ccabd3', 'flowStatus': 'COMPLETED', 'flowResult': '0fb152f0-805c-4d63-a889-3485c92df378', 'flowError': None, 'timestamp': '2023-10-05T09:26:45.069Z'}
 05-10 14:56:48 | I | 0fb152f0-805c-4d63-a889-3485c92df378
```

### Transfer logs
```
 05-10 15:02:15 | I | Tranfering instrument id '0fb152f0-805c-4d63-a889-3485c92df378' to 'Charlie'
 05-10 15:02:15 | I | Running action 'Transfer' on 'Alice/BAA7F076B971/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 05-10 15:02:15 | D | Request type=post to url='https://localhost:8888/api/v1/flow/BAA7F076B971'
 05-10 15:02:15 | D | Original Request = {'clientRequestId': '__REQUEST_NUMBER__', 'flowClassName': '__PACKAGE__.workflows.Transfer', 'requestBody': {'id': '__TRANSFER_ASSET_ID__', 'to': '__TRANSFER_TO__', 'quantity': 4}}
 05-10 15:02:15 | D | {'clientRequestId': '36552.1696498335.108681', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': '0fb152f0-805c-4d63-a889-3485c92df378', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB', 'quantity': 4}}
 05-10 15:02:15 | D | After filling values = {'clientRequestId': '36552.1696498335.108681', 'flowClassName': 'com.r3.developers.configurableInstrument.workflows.Transfer', 'requestBody': {'id': '0fb152f0-805c-4d63-a889-3485c92df378', 'to': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB', 'quantity': 4}}
 05-10 15:02:15 | D | 202
 05-10 15:02:15 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498335.108681', 'flowId': None, 'flowStatus': 'START_REQUESTED', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:15.134Z'}
 05-10 15:02:19 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498335.108681'
 05-10 15:02:19 | D | 200
 05-10 15:02:19 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498335.108681', 'flowId': '0eee4ebc-1b7d-4281-bf5d-593c42463725', 'flowStatus': 'RUNNING', 'flowResult': None, 'flowError': None, 'timestamp': '2023-10-05T09:32:15.374Z'}
 05-10 15:02:23 | D | Request type=get to url='https://localhost:8888/api/v1/flow/BAA7F076B971/36552.1696498335.108681'
 05-10 15:02:23 | D | 200
 05-10 15:02:23 | D | {'holdingIdentityShortHash': 'BAA7F076B971', 'clientRequestId': '36552.1696498335.108681', 'flowId': '0eee4ebc-1b7d-4281-bf5d-593c42463725', 'flowStatus': 'FAILED', 'flowResult': None, 'flowError': {'type': 'FLOW_FAILED', 'message': 'net.corda.v5.ledger.utxo.ContractVerificationException: Verification of ledger transaction with ID SHA-256D:6A6D36117B6E2993067AB875F0E93B8DEF6B3B7BFC401507C30FA872ED5CAFE0 failed: net.corda.v5.ledger.utxo.ContractVerificationException: Ledger transaction contract verification failed for the specified transaction: SHA-256D:6A6D36117B6E2993067AB875F0E93B8DEF6B3B7BFC401507C30FA872ED5CAFE0.\nThe following contract verification requirements were not met:\ncom.r3.developers.configurableInstrument.contracts.InstrumentContract: Failed requirement: Instrument is not transferable.\n'}, 'timestamp': '2023-10-05T09:32:18.618Z'}
 05-10 15:02:23 | I | {'type': 'FLOW_FAILED', 'message': 'net.corda.v5.ledger.utxo.ContractVerificationException: Verification of ledger transaction with ID SHA-256D:6A6D36117B6E2993067AB875F0E93B8DEF6B3B7BFC401507C30FA872ED5CAFE0 failed: net.corda.v5.ledger.utxo.ContractVerificationException: Ledger transaction contract verification failed for the specified transaction: SHA-256D:6A6D36117B6E2993067AB875F0E93B8DEF6B3B7BFC401507C30FA872ED5CAFE0.\nThe following contract verification requirements were not met:\ncom.r3.developers.configurableInstrument.contracts.InstrumentContract: Failed requirement: Instrument is not transferable.\n'}
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

