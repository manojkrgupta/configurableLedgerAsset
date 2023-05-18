

### Type 2) Transferable, non-Quantifiable Instrument. Example 1 – Unique artifacts on Ledger.

1. Issue command to be run:
```
h.issue('Authority', 'Alice', 'Unique artifact. The Mona Lisa', quantity=None, transferable=True, expiry=None, verifiable=True, 
attributes={'holding authority': 'The Louvre Museum, Paris'}) 
```
expected sample output:
```aidl
 18-05 14:20:05 | I | Issuing instrument='Unique artifact. The Mona Lisa' to 'Alice'
 18-05 14:20:05 | I | Running action 'Issue' on 'Authority/F7E16E10BD9A/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:20:50 | I | f350e8a9-8d62-4cf6-9bdd-31a3a415375f
 18-05 14:20:50 | I | Time taken = 0:00:44.538556
('2596.1684390805.556146',
 <Response [200]>,
 'f350e8a9-8d62-4cf6-9bdd-31a3a415375f')
```
*note: f350e8a9-8d62-4cf6-9bdd-31a3a415375f in output is the uuid of the transaction.
2. Query command to be run:
```
h.query('Alice')
```
expected sample output:
```aidl
	id	name	owner	issuer	quantity	transferable	expiry	verifiable	attributes
0	f350e8a9-8d62-4cf6-9bdd-31a3a415375f	Unique artifact. The Mona Lisa	CN=Alice, OU=Test Dept, O=R3, L=London, C=GB	CN=Authority, OU=Test Dept, O=R3, L=London, C=GB	None	True	None	True	{'holding authority': 'The Louvre Museum, Paris'}
```
*note: f350e8a9-8d62-4cf6-9bdd-31a3a415375f in output is the uuid of the transaction.
3. Transfer command to be run:
```aidl
h.transfer('f350e8a9-8d62-4cf6-9bdd-31a3a415375f', 'Alice', 'Charlie')
```
*note: transfer the ownership from Alice to Charlie
expected sample output:
```aidl
 18-05 14:32:14 | I | Tranfering instrument id 'f350e8a9-8d62-4cf6-9bdd-31a3a415375f' to 'Charlie'
 18-05 14:32:14 | I | Running action 'Transfer' on 'Alice/1029C3F8F875/CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:33:14 | I | net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@ffc727
 18-05 14:33:14 | I | Time taken = 0:01:00.449786
('2596.1684391534.491916',
 <Response [200]>,
 'net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@ffc727')
```
Now query on Alice, expected to see:
```aidl
h.query('Alice')
_ 
*note: return empty output 
```
and for Charlie:
```aidl
h.query('Charlie')
id	name	owner	issuer	quantity	transferable	expiry	verifiable	attributes
0	f350e8a9-8d62-4cf6-9bdd-31a3a415375f	Unique artifact. The Mona Lisa	CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB	CN=Authority, OU=Test Dept, O=R3, L=London, C=GB	None	True	None	True	{'holding authority': 'The Louvre Museum, Paris'}
```
ownership is now transferred from Alice to Charlie

4. Redeem command to be run:
```aidl
h.redeem('f350e8a9-8d62-4cf6-9bdd-31a3a415375f', 'Authority')
```
*note: the redeem can be called from either issuer ('Authroity' in this example) or current owner ('Charlier' in this example)
expected output:
```
 18-05 14:40:34 | I | Redeeming instrument id 'f350e8a9-8d62-4cf6-9bdd-31a3a415375f' quantity 'None'
 18-05 14:40:34 | I | Running action 'Redeem' on 'Authority/F7E16E10BD9A/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:41:18 | I | net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@62dfbf50
 18-05 14:41:18 | I | Time taken = 0:00:44.295710
('2596.1684392034.0885918',
 <Response [200]>,
 'net.corda.ledger.utxo.flow.impl.FinalizationResultImpl@62dfbf50')
 ```
now query result on both Authority and Charlie returns empty
```aidl
h.query('Authority')
_
h.query('Charlie')
_
```
5. PDF_report command to be run
just for demo purpose, re-run the issue command in step1 from Authority to Alice
```aidl
h.issue('Authority', 'Alice', 'Unique artifact. The Mona Lisa', quantity=None, transferable=True, expiry=None, verifiable=True, 
attributes={'holding authority': 'The Louvre Museum, Paris'}) 
 18-05 14:49:06 | I | Issuing instrument='Unique artifact. The Mona Lisa' to 'Alice'
 18-05 14:49:06 | I | Running action 'Issue' on 'Authority/F7E16E10BD9A/CN=Authority, OU=Test Dept, O=R3, L=London, C=GB'
 18-05 14:49:59 | I | e0e3c2de-6d35-4536-a36c-92bfd5576914
 18-05 14:49:59 | I | Time taken = 0:00:52.384526
('2596.1684392546.7109098',
 <Response [200]>,
 'e0e3c2de-6d35-4536-a36c-92bfd5576914')
 
 h.query('Alice')
 id	name	owner	issuer	quantity	transferable	expiry	verifiable	attributes
0	e0e3c2de-6d35-4536-a36c-92bfd5576914	Unique artifact. The Mona Lisa	CN=Alice, OU=Test Dept, O=R3, L=London, C=GB	CN=Authority, OU=Test Dept, O=R3, L=London, C=GB	None	True	None	True	{'holding authority': 'The Louvre Museum, Paris'}
```
*note: the uuid for the new transaction is now e0e3c2de-6d35-4536-a36c-92bfd5576914
the command to generate the pdf report will be:
```aidl
pdf_report = h.print_to_pdf('Alice', 'e0e3c2de-6d35-4536-a36c-92bfd5576914', show=False)
webbrowser.open("file:///{}".format(pdf_report))
```
and expected result is:
```aidl
[WDM] - Downloading: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8.81M/8.81M [00:00<00:00, 16.4MB/s]
 18-05 14:50:32 | I | Time taken = 0:00:08.905500
```
with a pdf file being saved locally

