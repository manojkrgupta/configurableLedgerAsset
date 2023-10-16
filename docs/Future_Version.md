#### Feature 1 : Allow parties not in the network – Like students holding university degree don’t need to be on network.
* People holding eRupee, Digital Currency etc don’t need to be on network.
* At the time of issue, transfer, redeem, they’ll be authenticated with Peoples Registry and will progress ahead with updates happening directly in the issuer ledger.

---

#### Feature 2 : Next version of Transfer – Exchange (Allow trading of assets on ledger)
* Two ledger instruments can be swapped/traded with network entities, based on exchange rate, agreed upon, negotiation.
* Examples:
```python
# Tradable/Exchangable with any item
h.issue('Dave', 'Alice', 'eRupee',
        quantity=100001, transferable=True, expiry=None, verifiable=True,
        exchange={'with': None, 'rate': None} // Tradable/Exchangeable with any item 
       )

# Tradable/Exchangable with eRupee in the ratio given
h.issue('Dave', 'Alice', 'Digital Currency INR 500 Note',
        quantity=None, transferable=True, expiry=None, verifiable=True,
        exchange={'with': 'eRupee', 'rate': '1:500', 'fraction': False}
        attributes={'number': 'OMV 336048', 'year': '1981'}
       )

# Tradable/Exchangable with eRupee at the rate defined 100000
h.issue('Dave', 'Alice', 'Limited edition watch',
        quantity=1, transferable=True, expiry=None, verifiable=True,
        exchange={'with': 'eRupee', 'rate': 100000}
        attributes={'model': ‘Apple 007', 'year': '2000'}
       )
```

---

#### Feature 3: Allow conditions (lambda) – per instruments – which can be triggered upon any defined action – transfer, redeem, print etc.
* This can add loopholes and has to be thought upon well before implementing.

---

#### Feature 4: End of the day Aggregator based on instrument
* Fungible Instruments, with a defined quantity can be aggregated at the end of the day.
* If lets says, Alice has received 100 Apples(instrument=Apple) from me and another 50Apples from you, this can be aggregated to 150Apples, by this end of the batch.
* This will optimise the ledger, and will also make future transactions faster.


---

#### Feature n
