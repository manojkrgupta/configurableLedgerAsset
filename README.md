## References/Index
* [Install and Run](./docs/Install_and_Run.md)
* [Workflows List](./docs/Workflows.md)
* [Usecase, Example, Story 1](./docs/stories/Story_1.md)
* [Usecase, Example, Story 2](./docs/stories/Story_2.md)
* [Usecase, Example, Story 3](./docs/stories/Story_3.md)
* [Usecase, Example, Story 4](./docs/stories/Story_4.md)
* [Error Examples](./docs/Error_examples.md)
* [Future Versions, Features in pipe line](./docs/Future_Version.md)

## Multipurpose Configurable Ledger Asset
* Applications across industry – from CBDC to College University Degree to Limited Edition Sovereign ….. to many more

## Use case matrix
```
Type   Transferable   Quantifiable     Examples, Samples, Use Cases.
1         Y                Y           (1) Government Bond with defined coupon payments, (2) Digital currency (eRupee), (3) Limited Edition Sovereign
2         Y                N           (4) Unique artifacts on Ledger, (5) Fiat currency with unique number in digital form
3         N                Y           (6) Travel points, (7) Redeemable Tokens, (8) Amazon Vouchers
4         N                N           (9) Graduation certificate (10) Experience/Participation certificate (Credentials)
```


### Calls
```
Type 1) Transferable, Quantifiable Instrument. Example 1 – Government Bond with defined coupon payments.

h.issue('Dave', 'Alice', 'Government Bond 2024’, quantity=10, transferable=True, expiry=None, verifiable=True, 
attributes={'payments': "['10Jun2023', '10Sep2023', '10Dec2023', '10Mar2024']"})

Type 1) Transferable, Quantifiable Instrument. Example 2 – Digital currency (eRupee)

h.issue('Dave', 'Alice', 'eRupee’, quantity=100001, transferable=True, expiry=None,     verifiable=True )


Type 2) Transferable, non-Quantifiable Instrument. Example 1 – Unique artifacts on Ledger.

h.issue('Dave', 'Alice', 'Unique artifact. The Mona Lisa’, quantity=None, transferable=True, expiry=None, verifiable=True, 
attributes={'holding authority': 'The Louvre Museum, Paris'})

Type 2) Transferable, non-Quantifiable Instrument. Example 2 – Fiat currency with unique number in digital form.

h.issue('Dave', 'Alice', 'Digital Currency INR 500 Note’, quantity=None, transferable=True, expiry=None, verifiable=True, 
attributes={'number': 'OMV 336048', 'year': '1981’})


Type 3) non-Transferable, Quantifiable Instrument. Example 1 – Travel points.

h.issue('Dave', 'Alice', 'Star Alliance Travel Points’, quantity=100, transferable=False, expiry=None, verifiable=True)

Type 3) non-Transferable, Quantifiable Instrument. Example 2 – Amazon Vouchers

h.issue('Dave', 'Alice', ‘Amazon Voucher’, quantity=2000, transferable=False, expiry=None, verifiable=True, attributes={‘currency': ‘INR’})


Type 4) non-Transferable, non-Quantifiable Instrument. Example 1 – Graduation certificate

h.issue('Dave', 'Alice', 'BE Computer Engineering’, quantity=None, transferable=False, expiry=None, verifiable=True,
 attributes={'university': 'University of Mumbai', 'year': '2023’, 'score': '450/500’, 'subject’: "['Robotics', 'AI', 'DSP’]"})

Type 4) non-Transferable, non-Quantifiable Instrument. Example 2 – Experience/Participation certificate (Credentials)

h.issue('Dave', 'Alice', 'R3 Hackathon 2023’, quantity=None, transferable=False, expiry=None, verifiable=True, 
attributes={'Project': 'Corda 5', 'Year': '2023'})

```
