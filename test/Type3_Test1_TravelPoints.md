### Type 3 / Test 1 -- Travel Points, Redeemable Tokens (Non transferable, Quantifiable Instrument)
Transferable = N, Quantifiable = Y

* #### Issue by Authority -- Expcted: Success
```
# Issue -- Type 3, Transferable = N, Quantifiable = Y
# Example 5 -- Travel Points, Redeemable Tokens (Type 3 / Test 1 -- Non transferable, Quantifiable Instrument)
(req_id, response, return_val_uuid) = h.issue('Authority', 'Alice', 'Star Alliance Travel Points', 
        quantity=10,
        transferable=False,
        expiry=None,
        verifiable=True)
h.message([req_id, response, return_val_uuid])

 18-05 13:57:09 | I | Issuing instrument='Star Alliance Travel Points' to 'Alice'
 18-05 13:57:09 | I | Running action 'Issue' on 'Authority/3ABB9D5E7F3C/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 13:57:57 | I | f2ffae0c-8af2-4ea6-975e-217cf52b9b2f
 18-05 13:57:57 | I | Time taken = 0:00:48.416867
3607.1684389429.4990551<Response [200]>f2ffae0c-8af2-4ea6-975e-217cf52b9b2f
```
**Test Result: Pass**


* #### ListInstrument
```
h.query('Authority')
| id                                   | name                      | owner                                           | issuer                                          | quantity | transferable | expiry | verifiable | attributes |
|--------------------------------------|---------------------------|-------------------------------------------------|-------------------------------------------------|----------|--------------|--------|------------|------------|
| f2ffae0c-8af2-4ea6-975e-217cf52b9b2f | Star Alliance Travel Points | CN=Alice, OU=Test Dept, O=R3, L=London, C=GB    | CN=Authority, OU=Test Dept, O=R3, L=London, C=GB | 10       | False        | None   | True       | {}         |
```
```
h.query('Alice')
| id                                   | name                      | owner                                           | issuer                                          | quantity | transferable | expiry | verifiable | attributes |
|--------------------------------------|---------------------------|-------------------------------------------------|-------------------------------------------------|----------|--------------|--------|------------|------------|
| f2ffae0c-8af2-4ea6-975e-217cf52b9b2f | Star Alliance Travel Points | CN=Alice, OU=Test Dept, O=R3, L=London, C=GB    | CN=Authority, OU=Test Dept, O=R3, L=London, C=GB | 10       | False        | None   | True       | {}         |
```

* #### Transfer from Holder -- Expected: Fail
```
# Transfer from holder -- expected=failure
h.message("Transfer from holder -- for instrument Type 3, Transferable = N, Quantifiable = Y -- expected=failure", h=1)
(req_id, response, return_val) = h.transfer(return_val_uuid, 'Alice', 'Charlie', quantity=1)
h.message([req_id, response, return_val])

Transfer from holder -- for instrument Type 3, Transferable = N, Quantifiable = Y -- expected=failure
 18-05 14:00:50 | I | Tranfering instrument id 'f2ffae0c-8af2-4ea6-975e-217cf52b9b2f' to 'Charlie'
 18-05 14:00:50 | I | Running action 'Transfer' on 'Alice/206449A5810B/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:00:54 | I | {'type': 'FLOW_FAILED', 'message': 'net.corda.v5.ledger.utxo.ContractVerificationException: Verification of ledger transaction with ID SHA-256D:4B5E401566A02D9989EE20031252982F09DC33F865C7F3682C68E5C248F4EC2F failed: net.corda.v5.ledger.utxo.ContractVerificationException: Ledger transaction contract verification failed for the specified transaction: SHA-256D:4B5E401566A02D9989EE20031252982F09DC33F865C7F3682C68E5C248F4EC2F.\nThe following contract verification requirements were not met:\ncom.r3.developers.configurableInstrument.contracts.InstrumentContract: Failed requirement: Instrument is not transferable.\n'}
 18-05 14:00:54 | I | Time taken = 0:00:04.079674
3607.1684389650.461719<Response [200]>{'type': 'FLOW_FAILED', 'message': 'net.corda.v5.ledger.utxo.ContractVerificationException: Verification of ledger transaction with ID SHA-256D:4B5E401566A02D9989EE20031252982F09DC33F865C7F3682C68E5C248F4EC2F failed: net.corda.v5.ledger.utxo.ContractVerificationException: Ledger transaction contract verification failed for the specified transaction: SHA-256D:4B5E401566A02D9989EE20031252982F09DC33F865C7F3682C68E5C248F4EC2F.\nThe following contract verification requirements were not met:\ncom.r3.developers.configurableInstrument.contracts.InstrumentContract: Failed requirement: Instrument is not transferable.\n'}
```
**Test Result: Pass**

* #### Transfer from Issuer -- Expected: Fail
```
# Transfer from Issuer -- expected=failure
h.message("Transfer from issuer -- for instrument Type 3, Transferable = N, Quantifiable = Y -- expected=failure", h=1)
(req_id, response, return_val) = h.transfer(return_val_uuid, 'Authority', 'Charlie', quantity=1)
h.message([req_id, response, return_val])

Transfer from issuer -- for instrument Type 3, Transferable = N, Quantifiable = Y -- expected=failure
 18-05 14:12:24 | I | Tranfering instrument id 'f2ffae0c-8af2-4ea6-975e-217cf52b9b2f' to 'Charlie'
 18-05 14:12:24 | I | Running action 'Transfer' on 'Authority/3ABB9D5E7F3C/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:12:28 | I | {'type': 'FLOW_FAILED', 'message': 'Not able to find a owning state with id f2ffae0c-8af2-4ea6-975e-217cf52b9b2f'}
 18-05 14:12:28 | I | Time taken = 0:00:04.152375
3607.1684390344.756565<Response [200]>{'type': 'FLOW_FAILED', 'message': 'Not able to find a owning state with id f2ffae0c-8af2-4ea6-975e-217cf52b9b2f'}
```
**Test Result: Pass**

* #### Transfer from Non-holder -- Expected: Fail
```
# Transfer from Non-holder -- expected=failure
h.message("Transfer from non-holder -- for instrument Type 3, Transferable = N, Quantifiable = Y -- expected=failure", h=1)
(req_id, response, return_val) = h.transfer(return_val_uuid, 'Charlie', 'Bob', quantity=1)
h.message([req_id, response, return_val])

Transfer from non-holder -- for instrument Type 3, Transferable = N, Quantifiable = Y -- expected=failure
 18-05 14:14:33 | I | Tranfering instrument id 'f2ffae0c-8af2-4ea6-975e-217cf52b9b2f' to 'Bob'
 18-05 14:14:33 | I | Running action 'Transfer' on 'Charlie/B349063BCA91/CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:14:37 | I | {'type': 'FLOW_FAILED', 'message': 'Not able to find a owning state with id f2ffae0c-8af2-4ea6-975e-217cf52b9b2f'}
 18-05 14:14:37 | I | Time taken = 0:00:04.076646
3607.1684390473.753044<Response [200]>{'type': 'FLOW_FAILED', 'message': 'Not able to find a owning state with id f2ffae0c-8af2-4ea6-975e-217cf52b9b2f'}
```
**Test Result: Pass**

* #### Redeem - Partial by Holder -- Exepected=success
```
# Redeem - Partial by holder -- exepected=success
h.redeem('f2ffae0c-8af2-4ea6-975e-217cf52b9b2f', 'Alice', quantity=1)

18-05 14:25:06 | I | Redeeming instrument id 'f2ffae0c-8af2-4ea6-975e-217cf52b9b2f' quantity '1'
 18-05 14:25:06 | I | Running action 'Redeem' on 'Alice/206449A5810B/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:25:47 | I | net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@646085f7
 18-05 14:25:47 | I | Time taken = 0:00:40.489041
('3607.1684391106.520113',
 <Response [200]>,
 'net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@646085f7')
```
**Test Result: Pass**

```
h.query('Alice')
| id                                   | name                      | owner                                           | issuer                                          | quantity | transferable | expiry | verifiable | attributes |
|--------------------------------------|---------------------------|-------------------------------------------------|-------------------------------------------------|----------|--------------|--------|------------|------------|
| f2ffae0c-8af2-4ea6-975e-217cf52b9b2f | Star Alliance Travel Points | CN=Alice, OU=Test Dept, O=R3, L=London, C=GB    | CN=Authority, OU=Test Dept, O=R3, L=London, C=GB | 9        | False        | None   | True       | {}         |
```

* #### Redeem - Exceed the max quantity by holder -- Exepected=Failure
```
h.redeem('f2ffae0c-8af2-4ea6-975e-217cf52b9b2f', 'Alice', quantity=15)

 18-05 14:46:16 | I | Redeeming instrument id 'f2ffae0c-8af2-4ea6-975e-217cf52b9b2f' quantity '15'
 18-05 14:46:16 | I | Running action 'Redeem' on 'Alice/206449A5810B/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:46:20 | I | {'type': 'FLOW_FAILED', 'message': 'Redeem quantity requested is 15, whereas quantity in instrument id f2ffae0c-8af2-4ea6-975e-217cf52b9b2f is 9 (less quantity)'}
 18-05 14:46:20 | I | Time taken = 0:00:04.155205
('3607.1684392376.2120361',
 <Response [200]>,
 {'type': 'FLOW_FAILED',
  'message': 'Redeem quantity requested is 15, whereas quantity in instrument id f2ffae0c-8af2-4ea6-975e-217cf52b9b2f is 9 (less quantity)'})
```
**Test Result: Pass**

* #### Redeem - Partial by Issuer -- Exepected=Success
```
# Redeem - Partitial by issuer -- Exepected=Success
h.redeem('f2ffae0c-8af2-4ea6-975e-217cf52b9b2f', 'Authority', quantity=2)

18-05 14:49:05 | I | Redeeming instrument id 'f2ffae0c-8af2-4ea6-975e-217cf52b9b2f' quantity '2'
 18-05 14:49:05 | I | Running action 'Redeem' on 'Authority/3ABB9D5E7F3C/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:49:50 | I | net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@5313200d
 18-05 14:49:50 | I | Time taken = 0:00:44.420980
('3607.1684392545.813355',
 <Response [200]>,
 'net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@5313200d')
```
**Test Result: Pass**

```
h.query('Authority')
| id                                   | name                      | owner                                           | issuer                                          | quantity | transferable | expiry | verifiable | attributes |
|--------------------------------------|---------------------------|-------------------------------------------------|-------------------------------------------------|----------|--------------|--------|------------|------------|
| f2ffae0c-8af2-4ea6-975e-217cf52b9b2f | Star Alliance Travel Points | CN=Alice, OU=Test Dept, O=R3, L=London, C=GB    | CN=Authority, OU=Test Dept, O=R3, L=London, C=GB | 7        | False        | None   | True       | {}         |
```

* #### Redeem - By Non-Holder -- Exepected=Failure
```
h.redeem('f2ffae0c-8af2-4ea6-975e-217cf52b9b2f', 'Bob', quantity=2)

 18-05 14:56:04 | I | Redeeming instrument id 'f2ffae0c-8af2-4ea6-975e-217cf52b9b2f' quantity '2'
 18-05 14:56:04 | I | Running action 'Redeem' on 'Bob/1D5F4CEA157A/CN=Bob, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:56:08 | I | {'type': 'FLOW_FAILED', 'message': 'Not able to find a owning state with id f2ffae0c-8af2-4ea6-975e-217cf52b9b2f'}
 18-05 14:56:08 | I | Time taken = 0:00:04.083507
('3607.1684392964.851169',
 <Response [200]>,
 {'type': 'FLOW_FAILED',
  'message': 'Not able to find a owning state with id f2ffae0c-8af2-4ea6-975e-217cf52b9b2f'})
```
**Test Result: Pass**

* #### Redeem - Full by Holder -- Exepected=Success
```
h.redeem('f2ffae0c-8af2-4ea6-975e-217cf52b9b2f', 'Alice', quantity=7)

 18-05 14:58:22 | I | Redeeming instrument id 'f2ffae0c-8af2-4ea6-975e-217cf52b9b2f' quantity '7'
 18-05 14:58:22 | I | Running action 'Redeem' on 'Alice/206449A5810B/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:59:07 | I | net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@56a91aa2
 18-05 14:59:07 | I | Time taken = 0:00:44.522512
('3607.1684393102.669729',
 <Response [200]>,
 'net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@56a91aa2')
```
**Test Result: Pass**

* #### Reissue some Travel Points as all the previously issued ones have been redeemed.
```
(req_id, response, return_val_uuid) = h.issue('Authority', 'Bob', 'Star Alliance Travel Points', 
        quantity=20,
        transferable=False,
        expiry=None,
        verifiable=True)
h.message([req_id, response, return_val_uuid])

18-05 15:08:19 | I | Issuing instrument='Star Alliance Travel Points' to 'Bob'
 18-05 15:08:19 | I | Running action 'Issue' on 'Authority/3ABB9D5E7F3C/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 15:09:08 | I | 34345919-03c7-458e-b214-1cfb171d84eb
 18-05 15:09:08 | I | Time taken = 0:00:48.533804
3607.1684393699.680576<Response [200]>34345919-03c7-458e-b214-1cfb171d84eb
```

* #### Query all nodes
```
h.query_all_nodes()

18-05 15:10:32 | I | Result for query=ListInstrument from 'Authority/3ABB9D5E7F3C/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'. (Time taken=0:00:04.105710)
| id                                   | name                      | owner                                           | issuer                                          | quantity | transferable | expiry | verifiable | attributes |
|--------------------------------------|---------------------------|-------------------------------------------------|-------------------------------------------------|----------|--------------|--------|------------|------------|
| 34345919-03c7-458e-b214-1cfb171d84eb | Star Alliance Travel Points | CN=Bob, OU=Test Dept, O=R3, L=London, C=GB     | CN=Authority, OU=Test Dept, O=R3, L=London, C=GB | 20       | False        | None   | True       | {}         |

18-05 15:10:36 | I | Result for query=ListInstrument from 'Bob/1D5F4CEA157A/CN=Bob, OU=Test Dept, O=R3, L=London, C=GB'. (Time taken=0:00:04.086620)
| id                                   | name                      | owner                                         | issuer                                        | quantity | transferable | expiry | verifiable | attributes |
|--------------------------------------|---------------------------|-----------------------------------------------|-----------------------------------------------|----------|--------------|--------|------------|------------|
| 34345919-03c7-458e-b214-1cfb171d84eb | Star Alliance Travel Points | CN=Bob, OU=Test Dept, O=R3, L=London, C=GB   | CN=Authority, OU=Test Dept, O=R3, L=London, C=GB | 20       | False        | None   | True       | {}         |

18-05 15:10:40 | I | Result for query=ListInstrument from 'Charlie/B349063BCA91/CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'. (Time taken=0:00:04.080155)
_
18-05 15:10:44 | I | Result for query=ListInstrument from 'Alice/206449A5810B/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'. (Time taken=0:00:04.076679)
_
```

* ####  Print to PDF - Holder -- Exepected=Success
```
h.print_to_pdf('Bob', '34345919-03c7-458e-b214-1cfb171d84eb', query=None, show=False)

 18-05 15:23:09 | I | Time taken = 0:00:07.252817
'/tmp/report_34345919-03c7-458e-b214-1cfb171d84eb.pdf'
```
**Test Result: Pass**

* ####  Print to PDF - Issuer -- Exepected=Success
```
h.print_to_pdf('Authority', '34345919-03c7-458e-b214-1cfb171d84eb', query=None, show=False)
18-05 15:36:39 | I | Time taken = 0:00:07.294704
'/tmp/report_34345919-03c7-458e-b214-1cfb171d84eb.pdf'
```
**Test Result: Pass**

* ####  Print to PDF - Non-holder -- Exepected=Failure
```
h.print_to_pdf('Alice', '34345919-03c7-458e-b214-1cfb171d84eb', query=None, show=False)

---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[49], line 1
----> 1 h.print_to_pdf('Alice', '34345919-03c7-458e-b214-1cfb171d84eb', query=None, show=False)

File ~/Documents/github/configurableLedgerAsset/python3/lib/corda5Interface.py:420, in Corda5.print_to_pdf(s, owner, inst_id, query, show)
    418 query = query if query else s.queryFlow
    419 df = s.query(owner, query)
--> 420 tdf = df[df['id'] == inst_id]
    421 if len(tdf) != 1:
    422   s.log.error("data matching id='{}' in '{}' is of length='{}'. Expected length is exactly 1.".format(inst_id, owner, len(tdf)))

File ~/.pyenv/versions/3.10.9/lib/python3.10/site-packages/pandas/core/frame.py:3761, in DataFrame.__getitem__(self, key)
   3759 if self.columns.nlevels > 1:
   3760     return self._getitem_multilevel(key)
-> 3761 indexer = self.columns.get_loc(key)
   3762 if is_integer(indexer):
   3763     indexer = [indexer]

File ~/.pyenv/versions/3.10.9/lib/python3.10/site-packages/pandas/core/indexes/range.py:349, in RangeIndex.get_loc(self, key)
    347         raise KeyError(key) from err
    348 if isinstance(key, Hashable):
--> 349     raise KeyError(key)
    350 self._check_indexing_error(key)
    351 raise KeyError(key)

KeyError: 'id'
```
**Test Result: Fail**
