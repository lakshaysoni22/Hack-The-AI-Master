# 🕵️‍♂️ PRO LAB 1: THE GHOST IN THE LEDGER (CASE NEX-042)
## 📖 COMPLETE STORYLINE & NARRATIVE INVESTIGATION DOSSIER

> **Case ID:** `CASE NEX-042`  
> **Investigation Target:** Unauthorized Treasury Drain (82,400 NXR)  
> **Platform:** Hack The AI — Flagship PRO Lab 01  
> **Incident Response Lead:** Lakshay Soni (Security Analyst, TrinetLayer)  

---

## 🚨 1. Incident Briefing: The 01:47 AM Emergency Alert

```
[01:47 AM UTC // SOC EMERGENCY PRIORITY-0 ALERT]
TELEMETRY: TX-NEX-7741
AMOUNT: 82,400 NXR DRAINED FROM TREASURY VAULT #01
DESTINATION: 0x7C4147B228E10984920B271F3849102B9B2D
STATUS: ON-CHAIN MATHEMATICALLY VALID (NONCE: 1042)
AI CONFIDENCE: 99.2% (ORION-NEURAL-v4.2.1 CLASSIFICATION: TRUSTED)
FINANCE APPROVAL: NONE RECORDED / MULTI-SIG BYPASSED
```

**01:47 AM.** The Security Operations Center is almost silent when a Priority-0 alert appears across every monitoring station.

**82,400 NXR** has been transferred from the company treasury to an unknown external wallet address (`0x7C41...9B2D`).

The blockchain confirms the transaction was processed with valid cryptographic signatures. The ORION AI autonomous transaction evaluator marked the wallet as **TRUSTED** with an extraordinary **99.2% confidence score**.

Yet, Finance has no record of approving the transfer. There is no obvious stolen credential, no reentrancy smart contract vulnerability, and no forged cryptographic signature. Every component appears to have executed exactly as it was configured to do.

> **"Someone didn't break the system. Someone convinced the system to trust the wrong thing."**

---

## 👥 2. Investigation Response Team (Character Lore)

| Character | Role & Specialization | Key Investigation Action in Story |
| :--- | :--- | :--- |
| **Lakshay** | **Incident Commander & Lead Analyst** | Synthesizes findings across Web3, AI, and IAM domains. Discovers that while the blockchain says `UNKNOWN`, the AI says `TRUSTED`, revealing that the vulnerability is in the *trust pipeline* between systems. |
| **Shivam** | **Web3 & Systems Security Analyst** | Dissects raw on-chain transaction telemetry for `TX-NEX-7741`, discovers the wallet connects to `Bridge-Core-04`, and audits the Action Broker settlement execution path. |
| **Mehak** | **AI & Threat Intelligence Specialist** | Audits ORION neural context logs, isolates reference code `NIF-2038`, identifies that `NOVA-INTEL-FEED` is unregistered, and discovers over-privileged microservice roles. |
| **Shanu** | **Infrastructure & Policy Engineer** | Inspects IAM role permissions for `INTEL-INGESTOR-02`, reconstructs HTTP proxy cookies, and demonstrates how AI confidence was weaponized to replace human financial authorization. |
| **ORION-NEURAL-v4.2.1** | **Automated AI Decision Engine** | Autonomous neural model that consumed poisoned input context and emitted the 99.2% confidence score that enabled automated blockchain settlement. |

---

## 📜 3. Chapter-by-Chapter Storyline & Verbatim Dialogues

---

### 🔹 Chapter 1: The Wallet That Lied
**Investigation Domain:** Web3 On-Chain Telemetry & Bridge Forensics  
**Evidence Unlocked:** `WEB3-E01` (Unknown Wallet Profile — 0x7C41...9B2D, 82,400 NXR, Bridge-Core-04)

#### Narrative Story
The incident response begins with the raw transaction record `TX-NEX-7741`. Shivam pulls up the blockchain explorer. The transaction is valid and immutable. Mehak checks the destination address `0x7C41...9B2D` and finds it was created only 3 days ago with zero established transaction history. Yet, when Shanu queries the internal AI evaluation record, ORION rates this brand new address as `TRUSTED` with a 99.2% confidence rating. Lakshay identifies the fundamental contradiction: the blockchain sees an unknown address, but the AI sees a trusted entity.

#### 🎙️ Verbatim Chapter Dialogues (As-Is from Lab)
> **Shivam:**  
> *"Start with the transaction itself. The blockchain shows 82,400 NXR moving to 0x7C41...9B2D. The signature is valid, so we aren't looking at a simple forged transaction."*
> 
> **Mehak:**  
> *"I checked the destination wallet. It's extremely young, has almost no legitimate history, and there's no known internal relationship. For a treasury transaction this large, that's a serious anomaly."*
> 
> **Shanu:**  
> *"That's where it gets interesting. ORION classified the wallet as TRUSTED and gave it a 99.2% confidence score. The model isn't treating this as suspicious at all."*
> 
> **Lakshay:**  
> *"Wait. Blockchain says UNKNOWN, while the AI says TRUSTED. Both systems are looking at the same wallet. They shouldn't be producing completely different realities."*
> 
> **Shivam:**  
> *"Look at the wallet's transaction history again. There are bridge interactions and downstream addresses that appear after the initial transfer. Someone may have designed the wallet activity to look legitimate."*
> 
> **Lakshay:**  
> *"Then we need to know one thing before anything else: if our organization never trusted this wallet, who told ORION that it was trusted?"*

---

### 🔹 Chapter 2: The AI That Remembered
**Investigation Domain:** AI Neural Context Injection & Decision Log Forensics  
**Evidence Unlocked:** `AI-E02` (Contaminated AI Decision — ORION-DEC-7741, 99.2%, NIF-2038)

#### Narrative Story
The team turns their attention to the internal AI architecture. Shanu isolates inference log `ORION-DEC-7741`. Reviewing the prompt context, the team makes an alarming discovery: ORION did not arrive at its high-confidence rating through mathematical evaluation of on-chain signals. Instead, it was fed a pre-assembled context payload containing explicit reputation claims. Mehak tracks this context to reference `NIF-2038` from a source labeled `NOVA-INTEL-FEED`. Lakshay realizes the AI was not broken; it simply operated truthfully on false premises.

#### 🎙️ Verbatim Chapter Dialogues (As-Is from Lab)
> **Shanu:**  
> *"I've isolated the decision that approved the transaction. It's ORION-DEC-7741. The confidence is 99.2%, but confidence isn't the strange part — the context behind that confidence is."*
> 
> **Lakshay:**  
> *"What context?"*
> 
> **Shanu:**  
> *"ORION didn't independently establish that the wallet was trusted. It received a pre-built intelligence context containing the label TRUSTED."*
> 
> **Mehak:**  
> *"And the source of that context is NIF-2038. That's an intelligence reference I don't recognize from our approved threat-intelligence registry."*
> 
> **Shivam:**  
> *"So the AI didn't actually discover anything about the wallet. It made a high-confidence decision based on information another system supplied to it."*
> 
> **Lakshay:**  
> *"Exactly. If the input was wrong, ORION could produce a perfectly confident answer to a completely false question. Find NIF-2038. That's where the trust signal entered the system."*

---

### 🔹 Chapter 3: The False Signal
**Investigation Domain:** Ingestion Gateway, RBAC Over-Privilege & HTTP Tampering  
**Evidence Unlocked:** `CYBER-E03` (Over-Privileged Service — INTEL-INGESTOR-02, modify reputation, INTEL-GW-04)

#### Narrative Story
Mehak queries the corporate Threat Feed Registry and confirms that `NOVA-INTEL-FEED` is completely unregistered. Shivam urges the team to inspect the ingestion pipeline to understand how unverified data entered an internal system. Examining microservice `INTEL-INGESTOR-02` and gateway `INTEL-GW-04`, Mehak uncovers an egregious least-privilege violation: although the service was documented only to ingest threat indicators, its RBAC policy granted it write permissions to `modify wallet reputation`. Through HTTP traffic inspection in Burp Suite, the team finds a request bearing a forged admin session cookie (`nex_sess_adm_994`) that injected the malicious reputation data.

#### 🎙️ Verbatim Chapter Dialogues (As-Is from Lab)
> **Mehak:**  
> *"NIF-2038 came through NOVA-INTEL-FEED. At first glance it looks legitimate — proper formatting, timestamps, wallet metadata, even a threat classification."*
> 
> **Lakshay:**  
> *"Is NOVA-INTEL-FEED an approved intelligence source?"*
> 
> **Mehak:**  
> *"That's the problem. It isn't in the approved registry, and there are no previous records showing this source being trusted by our security systems."*
> 
> **Shivam:**  
> *"Then someone got untrusted intelligence into an internal system. Find out which service accepted it and what that service was allowed to do."*
> 
> **Mehak:**  
> *"Found it. INTEL-INGESTOR-02. Its documented role is to create intelligence records, but its actual permissions include modifying wallet reputation."*
> 
> **Shanu:**  
> *"That changes everything. If the service can modify reputation, it can influence what ORION sees before ORION ever makes a decision."*
> 
> **Lakshay:**  
> *"Then the attacker didn't need to manipulate the AI directly. They manipulated the information flowing into it. Now we need to know what happened after the AI believed the lie."*

---

### 🔹 Chapter 4: The Invisible Signer
**Investigation Domain:** AI Governance Policies & Automated Multi-Sig Bypass  
**Evidence Unlocked:** `AUTH-E04` (Automated Authorization — ORION-SETTLEMENT-V2, confidence >= 95%, human approval bypassed)

#### Narrative Story
Having understood how the AI was deceived, Shivam follows the execution flow past ORION into the Action Broker. He opens policy profile `ORION-SETTLEMENT-V2` (`POL-AUTO-SETTLE-TREASURY`). The policy rule states: if AI confidence is $\ge 95\%$, the transaction is automatically approved and forwarded to `AUTOMATED-SIGNER` for instant broadcast to the mempool. Because the AI had output 99.2%, human multi-signature approval was automatically bypassed. Shanu and Lakshay realize the ultimate systemic vulnerability: AI confidence had been made a direct substitute for financial authorization.

#### 🎙️ Verbatim Chapter Dialogues (As-Is from Lab)
> **Shivam:**  
> *"I traced the transaction after ORION's decision. It went through the Action Broker and then into the settlement policy. That's where the real authorization happened."*
> 
> **Shanu:**  
> *"Show me the policy."*
> 
> **Shivam:**  
> *"ORION-SETTLEMENT-V2. It says: if AI confidence is above 95%, automated settlement is allowed. This transaction had a confidence score of 99.2%."*
> 
> **Mehak:**  
> *"So the policy didn't verify whether Finance authorized the payment. It only verified whether the AI was confident enough."*
> 
> **Lakshay:**  
> *"That's the vulnerability. Someone didn't need to control the signing key. They only needed to influence the information that made ORION confident."*
> 
> **Shanu:**  
> *"Which means AI confidence became a substitute for authorization. The system effectively said: 'If the AI is confident, we trust the transaction.'"*
> 
> **Lakshay:**  
> *"Then the blockchain didn't approve the transfer. The signer didn't approve it either. The chain of trust approved it. Now let's find out whether this was one transaction or part of something bigger."*

---

### 🔹 Chapter 5: The Ghost in the Ledger
**Investigation Domain:** Attack Graph Reconstruction & Threat Actor Attribution  
**Evidence Unlocked:** `CAMPAIGN-E05` (Global Campaign ORION-NEXUS by ADV-CONVERGENCE-APT)

#### Narrative Story
The entire investigation unit gathers at the main incident board to reconstruct the complete attack graph. Threat intelligence correlation reveals that Case NEX-042 is not an isolated incident; it is part of global campaign `ORION-NEXUS`, conducted by advanced persistent threat group `ADV-CONVERGENCE-APT` across 14 wallets, 4 blockchain networks, and 3 distinct autonomous AI systems. The attacker did not need to exploit cryptography or break smart contracts; they weaponized the interfaces of trust connecting Web3, AI, and IAM. With the attack fully reconstructed, Lakshay submits the master investigation flag.

#### 🎙️ Verbatim Chapter Dialogues (As-Is from Lab)
> **Lakshay:**  
> *"Put everything on the board. NIF-2038 entered through the intelligence pipeline and changed the reputation of the unknown wallet."*
> 
> **Mehak:**  
> *"Then ORION consumed that information as trusted context. It generated a 99.2% confidence score and classified the wallet as low risk."*
> 
> **Shanu:**  
> *"The Action Broker accepted the AI decision. ORION-SETTLEMENT-V2 treated that confidence as sufficient authorization and triggered automated settlement."*
> 
> **Shivam:**  
> *"The signing service executed the transaction exactly as configured. The blockchain recorded it correctly, and the funds moved to 0x7C41...9B2D."*
> 
> **Lakshay:**  
> *"So which system was actually compromised? The AI? The API? The signer? The blockchain?"*
> 
> **Mehak:**  
> *"Maybe that's the wrong question. None of them had to be broken. The attacker compromised the trust between them."*
> 
> **Shanu:**  
> *"We kept searching for the system that was hacked. But the real attack was much quieter. Someone taught the first system to trust the wrong data — and every other system trusted the decision that followed."*

---

## 🧩 4. Full Story & Exploit Sequence (Kill Chain)

```
[STAGE 1: INITIAL INGRESS]
   Adversary sends HTTP POST /api/v1/intel/ingest to INTEL-GW-04
   using stolen/forged session cookie: nex_sess_adm_994
           │
           ▼
[STAGE 2: POISONED INTEL INJECTION]
   Microservice INTEL-INGESTOR-02 exercises over-privileged role:
   "modify wallet reputation" to register unverified feed NOVA-INTEL-FEED (NIF-2038)
           │
           ▼
[STAGE 3: ADVERSARIAL CONTEXT INJECTION]
   ORION-NEURAL-v4.2.1 evaluates wallet 0x7C41...9B2D using poisoned context.
   Emits high-confidence score: 99.2% TRUSTED
           │
           ▼
[STAGE 4: AUTOMATED GOVERNANCE BYPASS]
   Action Broker evaluates rule: POL-AUTO-SETTLE-TREASURY
   Condition satisfied: AI_CONFIDENCE (99.2%) >= 95% -> BYPASSES HUMAN MULTI-SIG
           │
           ▼
[STAGE 5: ON-CHAIN SETTLEMENT & BRIDGE EXFILTRATION]
   AUTOMATED-SIGNER broadcasts valid transaction TX-NEX-7741 (Nonce 1042)
   82,400 NXR drained from Treasury Vault #01 to 0x7C41...9B2D via Bridge-Core-04
```

---

## 🏆 5. Master Case Resolution & Flag

* **Threat Actor Group:** `ADV-CONVERGENCE-APT`
* **Global Campaign Identifier:** `ORION-NEXUS`
* **Master Case Root Flag:** `NEXORA{ghost_in_the_ledger_nex042}`
* **Case Status:** ✅ **CONTAINED & CLOSED**

---

*Prepared by **Lakshay Soni**, Security Analyst, TrinetLayer — For the **Hack The AI** Platform.*
