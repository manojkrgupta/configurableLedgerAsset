#### Issue Flow
* Issuer gets to decide the name, transferable or not, expiry or not, redeemable or not, and can add multiple/additional attributes (HashMap) on the same State/Asset.
* Applications like Government Bond, will be transferable, with maturity(some expiry), and redeemable (cash the principal on maturity), with additional attribute of coupon payment dates.
* Applications like College University Degree, will not be transferable, no expiry, and not redeemable. Will have additional attributes like Collage Name, University Name, Education Stream etc etc along with Issuer and Owner(Holder).
* Applications like Limited Edition Sovereign, will be transferable, no expiry but will be redeemable directly with Issuer.

---

#### Transfer Flow
* Not all instruments are transferable.
* If transferable -- will work on the basic nature of the instrument decided right from the issue point(by the issuer).
* Check = not expired apart from being owned. 

---

#### Flow Redeem/Settle/Expire/Mature/Consume/Spend
* Not all instruments will have expiry/maturity.
* Redeem can be executed by either the owner (holder of the asset) or also by the issuer of the asset (present design, can be controlled)
* If permitted, it will work on the basic nature of the instrument decided right from the issue point(by the issuer).

---

#### Verify Flow
* Every asset can be verified for
* Present Owner (default, public)
* Issuer (default, public)
* Transferable if permitted (default, public)
* Expiry/Maturity if any (default, public)
* And other attributes (private data)

---

#### ListInstrument Flow

---

#### Flow Exchange/Trade (Transfer version 2) – Future Release

