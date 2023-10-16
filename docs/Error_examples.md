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

### Error, when asset is not transferable
```
09-05 11:57:24 | I | Tranfering instrument id '6c764908-fdb0-40f3-af53-18f0159c6897' to 'Bob'
09-05 11:57:24 | I | Running action 'Transfer' on 'Charlie/D728EEE9116F/CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'
09-05 11:57:33 | I | {'type': 'FLOW_FAILED', 'message':
'net.corda.v5.ledger.utxo.ContractVerificationException: Verification of ledger transaction with ID SHA-256D:A2EBCEADF36EB733619F98987E3400B42E75CA93CE2998CF63FB2779D2A303BE failed: net.corda.v5.ledger.utxo.ContractVerificationException: Ledger transaction contract verification failed for the specified transaction: SHA-256D:A2EBCEADF36EB733619F98987E3400B42E75CA93CE2998CF63FB2779D2A303BE.\nThe following contract verification requirements were not met:\ncom.r3.developers.configurableInstrument.contracts.InstrumentContract: Failed requirement: Instrument is not transferable.\n'}

('57457.1683613644.99713',
 <Response [200]>,
 {'type': 'FLOW_FAILED',
  'message': 'net.corda.v5.ledger.utxo.ContractVerificationException:
Verification of ledger transaction with ID
SHA-256D:A2EBCEADF36EB733619F98987E3400B42E75CA93CE2998CF63FB2779D2A303BE
failed: net.corda.v5.ledger.utxo.ContractVerificationException: Ledger
transaction contract verification failed for the specified transaction:
SHA-256D:A2EBCEADF36EB733619F98987E3400B42E75CA93CE2998CF63FB2779D2A303BE.\nThe
following contract verification requirements were not
met:\ncom.r3.developers.configurableInstrument.contracts.InstrumentContract:
Failed requirement: Instrument is not transferable.\n'})
```
