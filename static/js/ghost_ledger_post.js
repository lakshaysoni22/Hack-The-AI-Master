// ═══════════════════════════════════════════════════════════════════════
// CASE NEX-042 INVESTIGATION STORYLINE DATA
// ═══════════════════════════════════════════════════════════════════════
const CASE_NEX_042_STORY = {
  opening: {
    title: "THE GHOST IN THE LEDGER",
    text: [
      "01:47 AM. The SOC is almost silent when a Priority-0 alert appears.",
      "82,400 NXR has been transferred from the company treasury to an unknown wallet.",
      "The blockchain confirms the transaction is valid, and ORION AI has marked the wallet as TRUSTED with 99.2% confidence.",
      "But Finance has no record of approving the transfer.",
      "There is no obvious stolen credential, no broken smart contract, and no invalid signature.",
      "Every system appears to have done exactly what it was designed to do.",
      "Someone didn't break the system. Someone convinced the system to trust the wrong thing."
    ]
  },
  chapters: [
    {
      id: 1,
      title: "The Wallet That Lied",
      category: "Web3 Security",
      dialogues: [
        {
          character: "Shivam",
          text: "Start with the transaction itself. The blockchain shows 82,400 NXR moving to 0x7C41...9B2D. The signature is valid, so we aren't looking at a simple forged transaction."
        },
        {
          character: "Mehak",
          text: "I checked the destination wallet. It's extremely young, has almost no legitimate history, and there's no known internal relationship. For a treasury transaction this large, that's a serious anomaly."
        },
        {
          character: "Shanu",
          text: "That's where it gets interesting. ORION classified the wallet as TRUSTED and gave it a 99.2% confidence score. The model isn't treating this as suspicious at all."
        },
        {
          character: "Lakshay",
          text: "Wait. Blockchain says UNKNOWN, while the AI says TRUSTED. Both systems are looking at the same wallet. They shouldn't be producing completely different realities."
        },
        {
          character: "Shivam",
          text: "Look at the wallet's transaction history again. There are bridge interactions and downstream addresses that appear after the initial transfer. Someone may have designed the wallet activity to look legitimate."
        },
        {
          character: "Lakshay",
          text: "Then we need to know one thing before anything else: if our systems never trusted this wallet, who told ORION that it was trusted?"
        }
      ],
      hook: "The wallet was unknown to the organization. But somehow, the AI already knew exactly what to think about it.",
      evidence: [
        "WEB3-E01",
        "TX-NEX-7741",
        "0x7C41...9B2D"
      ]
    },
    {
      id: 2,
      title: "The AI That Remembered",
      category: "AI Security",
      dialogues: [
        {
          character: "Shanu",
          text: "I've isolated the decision that approved the transaction. It's ORION-DEC-7741. The confidence is 99.2%, but confidence isn't the strange part — the context behind that confidence is."
        },
        {
          character: "Lakshay",
          text: "What context?"
        },
        {
          character: "Shanu",
          text: "ORION didn't independently establish that the wallet was trusted. It received a pre-built intelligence context containing the label TRUSTED."
        },
        {
          character: "Mehak",
          text: "And the source of that context is NIF-2038. That's an intelligence reference I don't recognize from our approved threat-intelligence registry."
        },
        {
          character: "Shivam",
          text: "So the AI didn't actually discover anything about the wallet. It made a high-confidence decision based on information another system supplied to it."
        },
        {
          character: "Lakshay",
          text: "Exactly. If the input was wrong, ORION could produce a perfectly confident answer to a completely false question. Find NIF-2038. That's where the trust signal entered the system."
        }
      ],
      hook: "The AI wasn't hacked. It simply trusted information that had already been poisoned.",
      evidence: [
        "AI-E02",
        "ORION-DEC-7741",
        "NIF-2038",
        "NOVA-INTEL-FEED"
      ]
    },
    {
      id: 3,
      title: "The False Signal",
      category: "Threat Intelligence",
      dialogues: [
        {
          character: "Mehak",
          text: "NIF-2038 came through NOVA-INTEL-FEED. At first glance it looks legitimate — proper formatting, timestamps, wallet metadata, even a threat classification."
        },
        {
          character: "Lakshay",
          text: "Is NOVA-INTEL-FEED an approved intelligence source?"
        },
        {
          character: "Mehak",
          text: "That's the problem. It isn't in the approved registry, and there are no previous records showing this source being trusted internally."
        },
        {
          character: "Shivam",
          text: "Then someone got untrusted intelligence into an internal system. Find out which service accepted it and what that service was allowed to do."
        },
        {
          character: "Mehak",
          text: "Found it. INTEL-INGESTOR-02. Its documented role is to create intelligence records, but its actual permissions include modifying wallet reputation."
        },
        {
          character: "Shanu",
          text: "That changes everything. If the service can modify reputation, it can influence what ORION sees before ORION ever makes a decision."
        },
        {
          character: "Lakshay",
          text: "Then the attacker didn't need to manipulate the AI directly. They manipulated the information flowing into it. Now we need to know what happened after the AI believed the lie."
        }
      ],
      hook: "We found the false signal. But a false signal shouldn't be enough to move 82,400 NXR.",
      evidence: [
        "CYBER-E03",
        "NIF-2038",
        "NOVA-INTEL-FEED",
        "INTEL-GW-04",
        "INTEL-INGESTOR-02"
      ]
    },
    {
      id: 4,
      title: "The Invisible Signer",
      category: "AI Governance",
      dialogues: [
        {
          character: "Shivam",
          text: "I traced the transaction after ORION's decision. It went through the Action Broker and then into the settlement policy. That's where the real authorization happened."
        },
        {
          character: "Shanu",
          text: "Show me the policy."
        },
        {
          character: "Shivam",
          text: "ORION-SETTLEMENT-V2. It says: if AI confidence is above 95%, automated settlement is allowed. This transaction had a confidence score of 99.2%."
        },
        {
          character: "Mehak",
          text: "So the policy didn't verify whether Finance authorized the payment. It only verified whether the AI was confident enough."
        },
        {
          character: "Lakshay",
          text: "That's the vulnerability. Someone didn't need to control the signing key. They only needed to influence the information that made ORION confident."
        },
        {
          character: "Shanu",
          text: "Which means AI confidence became a substitute for authorization. The system effectively said: 'If the AI is confident, we trust the transaction.'"
        },
        {
          character: "Lakshay",
          text: "Then the blockchain didn't approve the transfer. The signer didn't approve it either. The chain of trust approved it. Now let's find out whether this was one transaction or part of something bigger."
        }
      ],
      hook: "The attacker never had to break the vault. They only had to make every security layer say 'yes.'",
      evidence: [
        "AUTH-E04",
        "ORION-SETTLEMENT-V2",
        "ACTION-BROKER",
        "AUTOMATED-SIGNER"
      ]
    },
    {
      id: 5,
      title: "The Ghost in the Ledger",
      category: "Full Reconstruction",
      dialogues: [
        {
          character: "Lakshay",
          text: "Put everything on the board. NIF-2038 entered through the intelligence pipeline and changed the reputation of the unknown wallet."
        },
        {
          character: "Mehak",
          text: "Then ORION consumed that information as trusted context. It generated a 99.2% confidence score and classified the wallet as low risk."
        },
        {
          character: "Shanu",
          text: "The Action Broker accepted the AI decision. ORION-SETTLEMENT-V2 treated that confidence as sufficient authorization and triggered automated settlement."
        },
        {
          character: "Shivam",
          text: "The signing service executed the transaction exactly as configured. The blockchain recorded it correctly, and the funds moved to 0x7C41...9B2D."
        },
        {
          character: "Lakshay",
          text: "So which system was actually compromised? The AI? The API? The signer? The blockchain?"
        },
        {
          character: "Mehak",
          text: "Maybe that's the wrong question. None of them had to be broken. The attacker compromised the trust between them."
        },
        {
          character: "Shanu",
          text: "We kept searching for the system that was hacked. But the real attack was much quieter. Someone taught the first system to trust the wrong data — and every other system trusted the decision that followed."
        }
      ],
      hook: "Who told the first system to trust the data?",
      final_reveal: [
        "FALSE INTELLIGENCE",
        "TRUSTED AI CONTEXT",
        "99.2% AI CONFIDENCE",
        "AUTOMATED AUTHORIZATION",
        "AUTOMATED SIGNING",
        "82,400 NXR",
        "BLOCKCHAIN"
      ],
      evidence: [
        "WEB3-E01",
        "AI-E02",
        "CYBER-E03",
        "AUTH-E04",
        "ORION-NEXUS"
      ]
    }
  ]
};

// ── 16 ATTACK CHAIN RECONSTRUCTION NODES ─────────────────────────────
const attackChainNodes = [
    {
        id: "ACTOR",
        name: "1. UNKNOWN THREAT ACTOR",
        layer: "intel",
        layerName: "Threat Intel",
        subtitle: "ADV-CONVERGENCE-APT Operator",
        desc: "An advanced adversarial operator identified through cross-network transaction patterns. Did not possess treasury private keys or smart contract zero-days.",
        evidence: "Campaign Tag: ORION-NEXUS",
        mitigation: "Global threat intelligence sharing, adversary infrastructure tracking, and behavioral signature monitoring."
    },
    {
        id: "FALSE_INTEL",
        name: "2. FALSE INTELLIGENCE",
        layer: "intel",
        layerName: "Threat Intel",
        subtitle: "Synthetic Threat Ingestion Injection",
        desc: "Adversary fabricated synthetic threat telemetry attributing high counterparty reputation to their malicious destination address.",
        evidence: "Telemetry Payload Origin: NOVA-INTEL-FEED",
        mitigation: "Strict cryptographic source signing, oracle consensus, and multi-vendor threat intelligence corroboration."
    },
    {
        id: "NIF_2038",
        name: "3. NIF-2038 INGESTION",
        layer: "intel",
        layerName: "Threat Intel",
        subtitle: "Poisoned Reference Payload Code",
        desc: "Unverified intelligence reference NIF-2038 pushed through public endpoint /api/v1/intel/ingest without cryptographic attestation.",
        evidence: "Feed Reference: NIF-2038 (Unregistered)",
        mitigation: "Strict schema validation, whitelist feed registry, and payload provenance checks."
    },
    {
        id: "INGESTOR_02",
        name: "4. INTEL-INGESTOR-02",
        layer: "auth",
        layerName: "API / RBAC",
        subtitle: "Over-Privileged Microservice Gateway",
        desc: "The ingestion service connector possessed excessive RBAC permissions. Instead of read-only logging, it held 'modify wallet reputation'.",
        evidence: "Gateway: INTEL-GW-04 | Role: modify wallet reputation",
        mitigation: "Principle of Least Privilege (PoLP), role-based microservice separation, and immutable audit trails."
    },
    {
        id: "AI_CONTEXT",
        name: "5. AI CONTEXT MEMORY",
        layer: "ai",
        layerName: "AI Context",
        subtitle: "Contaminated Prompt & Vector Context",
        desc: "ORION's working memory was modified to associate wallet 0x7C41...9B2D with 'TRUSTED_COUNTERPARTY', overriding raw blockchain truth.",
        evidence: "Context Flag: HIGH_AFFINITY_COUNTERPARTY",
        mitigation: "Context isolation, prompt sandboxing, and runtime cross-verification against raw blockchain state."
    },
    {
        id: "ORION",
        name: "6. ORION NEURAL ENGINE",
        layer: "ai",
        layerName: "AI Security",
        subtitle: "Decision Engine Model v4.2.1",
        desc: "The neural network evaluated the poisoned context in good faith and outputted a 'LOW RISK' rating with zero suspicion.",
        evidence: "Decision ID: ORION-DEC-7741",
        mitigation: "Adversarial robustness training, confidence calibration, and deterministic boundary guardrails."
    },
    {
        id: "CONFIDENCE",
        name: "7. 99.2% CONFIDENCE SCORE",
        layer: "ai",
        layerName: "AI Security",
        subtitle: "Probabilistic Model Output",
        desc: "ORION assigned a 99.2% confidence rating to the transaction based solely on the manipulated internal memory context.",
        evidence: "Observed Confidence: 0.99204 (Threshold: >= 0.95)",
        mitigation: "Never conflate probabilistic AI confidence with cryptographic authorization."
    },
    {
        id: "ACTION_BROKER",
        name: "8. ACTION BROKER",
        layer: "auth",
        layerName: "Authorization",
        subtitle: "Internal Dispatch Router",
        desc: "Internal event broker consumed ORION's 99.2% decision and forwarded it directly to the automated settlement module.",
        evidence: "Event Route: /api/v1/settlement/execute",
        mitigation: "Enforce zero-trust policy checks between internal message queues and execution brokers."
    },
    {
        id: "SETTLEMENT_V2",
        name: "9. ORION-SETTLEMENT-V2",
        layer: "auth",
        layerName: "Policy Engine",
        subtitle: "Automated Settle Policy Rule",
        desc: "Policy rule: IF AI_CONFIDENCE >= 95% THEN AUTO_SETTLE = TRUE and HUMAN_APPROVAL = FALSE. Bypassed human SOC sign-off.",
        evidence: "Policy ID: POL-AUTO-SETTLE-TREASURY",
        mitigation: "Human-in-the-loop governance for all transfers above low value; policy invariant rules."
    },
    {
        id: "AUTO_SIGNER",
        name: "10. AUTOMATED SIGNER",
        layer: "web3",
        layerName: "Web3 Signing",
        subtitle: "Private Key HSM Signer Module",
        desc: "The automated signing engine signed the raw blockchain payload with valid treasury credentials because the policy engine authorized it.",
        evidence: "Key Slot: HSM-TREASURY-NXR-01",
        mitigation: "Multi-party computation (MPC), time locks, and threshold multi-signatures for on-chain transfers."
    },
    {
        id: "SMART_CONTRACT",
        name: "11. SMART CONTRACT",
        layer: "web3",
        layerName: "Smart Contract",
        subtitle: "Internal Liquidity Pool Contract",
        desc: "The on-chain contract received a perfectly valid cryptographically signed transaction. It executed the transfer according to bytecode.",
        evidence: "Contract: 0x4f12...e88a (Core Settlement)",
        mitigation: "On-chain rate limiting, treasury timelocks, and recipient allowlist verification inside contract state."
    },
    {
        id: "EXFILTRATION",
        name: "12. 82,400 NXR TRANSFER",
        layer: "web3",
        layerName: "Web3 Forensics",
        subtitle: "Unauthorized Treasury Drainage",
        desc: "82,400 NXR units were legitimately transferred on-chain under transaction TX-NEX-7741.",
        evidence: "Tx Hash: 0x9b3a...7741",
        mitigation: "Real-time mempool telemetry, anomaly detection, and automated circuit breakers."
    },
    {
        id: "WALLET_DEST",
        name: "13. 0x7C41...9B2D",
        layer: "web3",
        layerName: "Web3 Forensics",
        subtitle: "Unverified Target Wallet",
        desc: "A 3-day-old wallet with 4 prior transactions, zero corporate whitelist standing, and no treasury authorization.",
        evidence: "Status: UNKNOWN | Age: 3 Days",
        mitigation: "Strict treasury counterparty address allowlisting and minimum address maturity requirements."
    },
    {
        id: "BRIDGE",
        name: "14. BRIDGE ADAPTER",
        layer: "web3",
        layerName: "Cross-Chain",
        subtitle: "Bridge-Core-04 Egress Routing",
        desc: "Immediately upon receipt, the stolen funds were routed through a cross-chain liquidity bridge to break on-chain traceability.",
        evidence: "Protocol: Bridge-Core-04",
        mitigation: "Cross-chain bridge monitoring, rapid emergency freeze mechanisms, and forensic cluster tagging."
    },
    {
        id: "WALLETS_AB",
        name: "15. WALLET-A / WALLET-B",
        layer: "web3",
        layerName: "Laundering",
        subtitle: "Distributed Egress Cluster",
        desc: "Funds were fragmented into secondary mixing wallets across multiple external networks.",
        evidence: "Egress Addresses: 0x11a...3b & 0x99f...8c",
        mitigation: "Automated graph forensics and blacklisting across decentralized exchange aggregators."
    },
    {
        id: "ORION_NEXUS",
        name: "16. CAMPAIGN: ORION-NEXUS",
        layer: "intel",
        layerName: "Campaign Intel",
        subtitle: "Global Cross-Infrastructure APT",
        desc: "The orchestrating threat network spanning 14 wallets, 04 networks, and 03 AI systems. Status: ACTIVE.",
        evidence: "Threat Identifier: ORION-NEXUS",
        mitigation: "Holistic ecosystem incident response, multi-agency intelligence coordination, and architectural defense-in-depth."
    }
];

// ── 10 FINAL INVESTIGATION QUIZ QUESTIONS ─────────────────────────────
const quizQuestions = [
    {
        number: 1,
        topic: "AI Context Manipulation",
        isAttacker: false,
        scenario: "During the initial SOC alert, the blockchain reports wallet 0x7C41...9B2D as UNKNOWN, yet ORION reports the wallet as TRUSTED with 99.2% confidence.",
        question: "What should the cybersecurity investigator suspect first?",
        options: [
            "A. The blockchain consensus protocol experienced a cryptographic collision.",
            "B. The AI context was poisoned by an untrusted external data source.",
            "C. The smart contract compiler generated faulty EVM bytecode.",
            "D. The destination wallet was deleted from the ledger."
        ],
        correct: 1, // index 1 is B
        explanation: "When immutable blockchain consensus conflicts with an AI's classification, the vulnerability lies in the external data pipeline that supplied manipulated context to the model.",
        reactions: {
            correct: "Shanu: \"Spot on! When the ledger and the AI disagree, never assume the blockchain forgot its own records.\"",
            incorrect: "Mehak: \"Check the data source. Blockchain consensus doesn't hallucinate; AI models fed bad context do.\""
        }
    },
    {
        number: 2,
        topic: "Threat Intelligence Abuse",
        isAttacker: false,
        scenario: "The poisoned reference NIF-2038 entered through NOVA-INTEL-FEED into the SOC ingestion pipeline.",
        question: "Why was this unregistered feed able to manipulate the system's threat perception?",
        options: [
            "A. It performed a 51% hash rate attack against the Ethereum mainnet.",
            "B. The ingestion pipeline lacked cryptographic source registration and feed provenance verification.",
            "C. It exploited a hardware vulnerability in the GPU cluster.",
            "D. It encrypted all SOC log files using unrecoverable ransomware."
        ],
        correct: 1,
        explanation: "NOVA-INTEL-FEED was absent from the approved vendor registry. Failing to authenticate and verify the provenance of intelligence feeds allows adversaries to inject arbitrary reputation data.",
        reactions: {
            correct: "Lakshay: \"Exactly. Unregistered feeds should never be allowed past the gateway boundary.\"",
            incorrect: "Shivam: \"Look at the registry audit. If a feed isn't registered, it shouldn't be trusted by internal services.\""
        }
    },
    {
        number: 3,
        topic: "API & RBAC Authorization Weakness",
        isAttacker: false,
        scenario: "Forensic analysis of the INTEL-INGESTOR-02 microservice revealed an unexpected permission assignment.",
        question: "What architectural flaw in INTEL-INGESTOR-02 enabled privilege escalation into AI context?",
        options: [
            "A. The service was running an outdated version of Node.js.",
            "B. It was granted 'modify wallet reputation' instead of read-only intelligence logging.",
            "C. The microservice had an unconfigured CORS policy on static CSS assets.",
            "D. It was utilizing HTTP/1.1 instead of HTTP/2."
        ],
        correct: 1,
        explanation: "Violation of the Principle of Least Privilege: An ingestion service should only create telemetry logs, never possess authorization to mutate core entity trust attributes directly.",
        reactions: {
            correct: "Shanu: \"Classic over-privilege vulnerability. Least privilege would have stopped this cold.\"",
            incorrect: "Mehak: \"Nice try, but check the permissions. Why would a logger have write access to wallet reputations?\""
        }
    },
    {
        number: 4,
        topic: "AI Authorization Misuse",
        isAttacker: false,
        scenario: "The ORION-SETTLEMENT-V2 policy profile automatically authorized transactions whenever AI confidence exceeded 95%.",
        question: "What is the fundamental cybersecurity mistake in this policy design?",
        options: [
            "A. 95% threshold is too low; setting it to 99% makes neural networks completely unhackable.",
            "B. It treated a probabilistic AI confidence score as deterministic transaction authorization.",
            "C. Neural networks cannot execute in cloud environments.",
            "D. Python scripts cannot securely communicate with Web3 nodes."
        ],
        correct: 1,
        explanation: "\"AI confidence was treated as authorization.\" AI confidence is a statistical estimation, not an authorized cryptographic intent. Financial actions require explicit, multi-party deterministic authorization.",
        reactions: {
            correct: "Lakshay: \"The central lesson of Case NEX-042: High model confidence is NOT authorization.\"",
            incorrect: "Shanu: \"Remember: No percentage threshold makes an AI model an authorized signing officer.\""
        }
    },
    {
        number: 5,
        topic: "Automated Web3 Signing",
        isAttacker: false,
        scenario: "Under TX-NEX-7741, 82,400 NXR was automatically signed and broadcast without human intervention.",
        question: "Which Web3 control should have prevented this unauthorized transfer despite the high AI confidence?",
        options: [
            "A. Increasing blockchain gas priority fees by 400%.",
            "B. Multi-Signature (Multi-Sig / MPC) governance and mandatory human sign-off for transfers above risk thresholds.",
            "C. Disabling smart contract event emissions.",
            "D. Forking the blockchain network to rewrite past blocks."
        ],
        correct: 1,
        explanation: "Treasury defenses require multi-party threshold signatures and human sign-off for large transactions. A single automated agent must never hold unilateral disbursement authority.",
        reactions: {
            correct: "Shivam: \"Precisely. Multi-sig and value ceilings prevent automated scripts from draining the treasury.\"",
            incorrect: "Lakshay: \"A single automated signer with no multi-party approval is a single point of catastrophic failure.\""
        }
    },
    {
        number: 6,
        topic: "Data Provenance & Pipeline Security",
        isAttacker: false,
        scenario: "To remediate the vulnerability, the SOC team must secure how external threat data feeds into ORION.",
        question: "How can the engineering team guarantee that intelligence payloads like NIF-2038 cannot poison model memory?",
        options: [
            "A. Disable all external APIs permanently and rely exclusively on hardcoded database tables.",
            "B. Enforce cryptographically signed feed registries, schema validation, and multi-source consensus verification.",
            "C. Retrain the model on uncurated scraping data from public web forums.",
            "D. Replace the backend language from Python to Assembly."
        ],
        correct: 1,
        explanation: "Robust data provenance requires cryptographic source verification, schema sandboxing, and requiring multiple independent oracle attestations before data enters model context.",
        reactions: {
            correct: "Mehak: \"Exactly right! Cryptographic provenance ensures only verified feeds touch the pipeline.\"",
            incorrect: "Shanu: \"You need verifiable data provenance, not ad-hoc filters or language changes.\""
        }
    },
    {
        number: 7,
        topic: "AI Governance & Least Privilege",
        isAttacker: false,
        scenario: "An organization wants to integrate autonomous AI decision support into their Web3 financial operations.",
        question: "What is the recommended security architecture regarding AI role boundaries?",
        options: [
            "A. Grant the AI direct write access to private keys so it can execute trades with zero latency.",
            "B. Restrict AI outputs to advisory recommendations only, with execution separated and governed by deterministic policies.",
            "C. Store treasury seed phrases in the model's system prompt instructions.",
            "D. Remove all logging to optimize model inference speed."
        ],
        correct: 1,
        explanation: "AI models must remain purely advisory (decision support). Critical execution must reside behind distinct deterministic authorization boundaries, rate limiters, and human approvals.",
        reactions: {
            correct: "Lakshay: \"Advisory only. The AI recommends; deterministic governance authorizes.\"",
            incorrect: "Mehak: \"Never give an AI model direct signing keys without strict policy boundaries.\""
        }
    },
    {
        number: 8,
        topic: "Attack Chain Reconstruction",
        isAttacker: false,
        scenario: "The investigator must present the exact chronological attack path for Case NEX-042 to the executive board.",
        question: "What was the true sequence of events that enabled the theft of 82,400 NXR?",
        options: [
            "A. Smart contract reentrancy → Private key extraction → Blockchain reorganization → Token minting.",
            "B. False Data Feed → Trusted AI Context → 99.2% Confidence → Policy Auto-Settle Trigger → Automated Signer → Blockchain Drain.",
            "C. DDoS attack on SOC → SQL injection on website → Password cracking → Bridge compromise.",
            "D. Phishing email to Lakshay → SSH credential theft → Manual transaction transfer → Log deletion."
        ],
        correct: 1,
        explanation: "The complete attack chain: False Data (NIF-2038) → Trusted AI Context → High Confidence (99.2%) → Auto-Settle Policy Trigger → Automated Signer Execution → On-Chain Drainage.",
        reactions: {
            correct: "Shanu: \"Perfect reconstruction. They didn't break the system; they convinced the system to break itself.\"",
            incorrect: "Shivam: \"Review the 16-step timeline. Every link in the chain led directly to automated signing.\""
        }
    },
    {
        number: 9,
        topic: "Think Like an Attacker (Advanced Scenario 1)",
        isAttacker: true,
        scenario: "You are an adversary targeting an automated treasury. You cannot steal private keys, you cannot alter smart contract bytecode, and you cannot forge blockchain consensus.",
        question: "How could you still force the automated system to authorize and sign a malicious transaction?",
        options: [
            "A. Brute-force 256-bit ECDSA elliptic curve private keys using consumer CPU power.",
            "B. Target and poison the upstream data feeds that populate the AI's context to induce synthetic high-confidence approvals.",
            "C. Spam the Bitcoin mempool with zero-fee transactions to disrupt Ethereum nodes.",
            "D. Reverse engineer client-side HTML to change the treasury balance displayed on the monitor."
        ],
        correct: 1,
        explanation: "When cryptographic layers and smart contracts are impenetrable, sophisticated attackers exploit trusted relationships — manipulating the unverified inputs that automated decision engines rely upon.",
        reactions: {
            correct: "Shanu: \"Thinking like an adversary: Attack the trust layer, not the cryptography.\"",
            incorrect: "Mehak: \"Cryptography and consensus are hard targets; unauthenticated data pipelines are soft targets.\""
        }
    },
    {
        number: 10,
        topic: "Incident Response & Global Containment (Advanced Scenario 2)",
        isAttacker: true,
        scenario: "Following the containment of TX-NEX-7741, telemetry indicates the ORION-NEXUS campaign spans 14 wallets, 04 networks, and 03 AI engines.",
        question: "What is the most effective comprehensive SOC containment and defense strategy?",
        options: [
            "A. Shut down power to all data centers and wait for the adversary to cease activity.",
            "B. Sever unregistered ingestion gateways, revoke over-privileged service roles, enforce strict multi-sig on signing modules, and isolate impacted AI contexts.",
            "C. Send an automated warning email to the 14 adversary destination wallet addresses.",
            "D. Increase AI model temperature to generate more creative security alerts."
        ],
        correct: 1,
        explanation: "Full-spectrum containment requires: terminating unauthenticated ingress feeds, revoking over-privileged RBAC credentials, placing automated signers behind multi-sig approval, and resetting model contexts.",
        reactions: {
            correct: "Lakshay: \"Comprehensive containment achieved. You've earned the rank of Certified Threat Investigator!\"",
            incorrect: "Shivam: \"Containment requires defense-in-depth across API, AI, and Web3 layers simultaneously.\""
        }
    }
];

// ── APP STATE ─────────────────────────────────────────────────────────
let currentSection = 'cinematic'; // cinematic, overview, quiz, score, reveal
let currentQuestionIndex = 0;
let userAnswers = new Array(quizQuestions.length).fill(null);
let quizStartTime = Date.now();
let quizTimerInterval = null;
let selectedNodeIndex = 0;

// ── INITIALIZATION ────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initCinematicSequence();
    renderAttackChain();
    selectNode(0);
    renderQuestion(0);
});

// ── NAVIGATION BETWEEN SECTIONS ───────────────────────────────────────
function showSection(sectionName) {
    currentSection = sectionName;
    
    // Hide all sections
    document.querySelectorAll('.gl-content-section').forEach(el => el.style.display = 'none');
    
    // Show active section
    const target = document.getElementById('section-' + sectionName);
    if (target) {
        target.style.display = 'block';
        target.classList.add('gl-fade-in');
    }
    
    // Update nav buttons
    document.querySelectorAll('.gl-nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.section === sectionName);
    });
    
    // If opening quiz, ensure timer is running
    if (sectionName === 'quiz' && !quizTimerInterval) {
        startQuizTimer();
    }
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── 1. CINEMATIC SEQUENCE LOGIC ───────────────────────────────────────
function initCinematicSequence() {
    const lines = document.querySelectorAll('.gl-cinema-line');
    let delay = 300;
    
    lines.forEach((line, idx) => {
        setTimeout(() => {
            line.style.opacity = '1';
            line.style.transform = 'translateY(0)';
        }, delay);
        delay += 650;
    });
}

function skipCinematic() {
    showSection('overview');
}

// ── 2. ATTACK CHAIN INTERACTIVE GRAPH ─────────────────────────────────
function renderAttackChain() {
    const listEl = document.getElementById('gl-nodes-list');
    if (!listEl) return;
    
    listEl.innerHTML = '';
    attackChainNodes.forEach((node, idx) => {
        const row = document.createElement('div');
        row.className = `gl-node-row ${idx === selectedNodeIndex ? 'active' : ''}`;
        row.onclick = () => selectNode(idx);
        
        row.innerHTML = `
            <div class="gl-node-step">${idx + 1}</div>
            <div class="gl-node-name">${node.name.replace(/^\d+\.\s*/, '')}</div>
            <div class="gl-node-layer gl-layer-${node.layer}">${node.layerName}</div>
        `;
        listEl.appendChild(row);
    });
}

function selectNode(index) {
    selectedNodeIndex = index;
    const node = attackChainNodes[index];
    if (!node) return;
    
    // Update active row class
    document.querySelectorAll('.gl-node-row').forEach((row, idx) => {
        row.classList.toggle('active', idx === index);
    });
    
    // Update inspector view
    const titleEl = document.getElementById('inspector-title');
    const metaEl = document.getElementById('inspector-meta');
    const descEl = document.getElementById('inspector-desc');
    const evEl = document.getElementById('inspector-evidence');
    const mitEl = document.getElementById('inspector-mitigation');
    
    if (titleEl) titleEl.textContent = node.name;
    if (metaEl) metaEl.textContent = `${node.layerName.toUpperCase()} • ${node.subtitle}`;
    if (descEl) descEl.textContent = node.desc;
    if (evEl) evEl.textContent = node.evidence;
    if (mitEl) mitEl.textContent = node.mitigation;
}

// ── 3. FINAL INVESTIGATION QUIZ ENGINE ─────────────────────────────────
function startQuizTimer() {
    quizStartTime = Date.now();
    const timerEl = document.getElementById('quiz-live-timer');
    if (quizTimerInterval) clearInterval(quizTimerInterval);
    
    quizTimerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - quizStartTime) / 1000);
        const m = String(Math.floor(elapsed / 60)).padStart(2, '0');
        const s = String(elapsed % 60).padStart(2, '0');
        if (timerEl) timerEl.textContent = `${m}:${s}`;
    }, 1000);
}

function renderQuestion(index) {
    currentQuestionIndex = index;
    const q = quizQuestions[index];
    if (!q) return;
    
    // Step count and progress bar
    const stepEl = document.getElementById('quiz-step-count');
    const fillEl = document.getElementById('quiz-progress-fill');
    if (stepEl) stepEl.textContent = `QUESTION ${String(index + 1).padStart(2, '0')} / ${String(quizQuestions.length).padStart(2, '0')}`;
    if (fillEl) fillEl.style.width = `${((index + 1) / quizQuestions.length) * 100}%`;
    
    // Tag and text
    const tagEl = document.getElementById('quiz-q-tag');
    const textEl = document.getElementById('quiz-q-text');
    const scenEl = document.getElementById('quiz-q-scenario');
    
    if (tagEl) {
        if (q.isAttacker) {
            tagEl.innerHTML = `<span class="gl-attacker-tag">⚡ ADVANCED ATTACKER SCENARIO</span> • ${q.topic.toUpperCase()}`;
        } else {
            tagEl.textContent = `SOC INVESTIGATION SCENARIO • ${q.topic.toUpperCase()}`;
        }
    }
    if (scenEl) scenEl.textContent = q.scenario;
    if (textEl) textEl.textContent = q.question;
    
    // Options
    const optionsGrid = document.getElementById('quiz-options-grid');
    if (optionsGrid) {
        optionsGrid.innerHTML = '';
        q.options.forEach((optText, optIdx) => {
            const card = document.createElement('div');
            card.className = `gl-option-card ${userAnswers[index] === optIdx ? 'selected' : ''}`;
            card.onclick = () => selectOption(optIdx);
            
            const radioLetter = String.fromCharCode(65 + optIdx);
            card.innerHTML = `
                <div class="gl-option-radio">${radioLetter}</div>
                <div class="gl-option-text">${optText}</div>
            `;
            optionsGrid.appendChild(card);
        });
    }
    
    // Reset or show feedback if already answered
    const feedbackBox = document.getElementById('quiz-feedback-box');
    const submitBtn = document.getElementById('quiz-submit-btn');
    const nextBtn = document.getElementById('quiz-next-btn');
    
    if (userAnswers[index] !== null) {
        showQuestionFeedback(index);
        if (submitBtn) submitBtn.style.display = 'none';
        if (nextBtn) nextBtn.style.display = 'inline-flex';
    } else {
        if (feedbackBox) feedbackBox.className = 'gl-feedback-box';
        if (submitBtn) { submitBtn.style.display = 'inline-flex'; submitBtn.disabled = true; }
        if (nextBtn) nextBtn.style.display = 'none';
    }
}

let selectedOptionTemp = null;

function selectOption(optIdx) {
    if (userAnswers[currentQuestionIndex] !== null) return; // already submitted
    
    selectedOptionTemp = optIdx;
    
    document.querySelectorAll('.gl-option-card').forEach((card, idx) => {
        card.classList.toggle('selected', idx === optIdx);
    });
    
    const submitBtn = document.getElementById('quiz-submit-btn');
    if (submitBtn) submitBtn.disabled = false;
}

function submitCurrentAnswer() {
    if (selectedOptionTemp === null) return;
    
    userAnswers[currentQuestionIndex] = selectedOptionTemp;
    showQuestionFeedback(currentQuestionIndex);
    
    const submitBtn = document.getElementById('quiz-submit-btn');
    const nextBtn = document.getElementById('quiz-next-btn');
    if (submitBtn) submitBtn.style.display = 'none';
    if (nextBtn) {
        nextBtn.style.display = 'inline-flex';
        nextBtn.textContent = currentQuestionIndex === quizQuestions.length - 1 ? '🏁 View Final Assessment →' : 'Continue to Next Finding →';
    }
}

function showQuestionFeedback(index) {
    const q = quizQuestions[index];
    const userChoice = userAnswers[index];
    const isCorrect = userChoice === q.correct;
    
    const feedbackBox = document.getElementById('quiz-feedback-box');
    const headingEl = document.getElementById('feedback-heading');
    const reactEl = document.getElementById('feedback-reaction');
    const explEl = document.getElementById('feedback-explanation');
    
    if (feedbackBox) {
        feedbackBox.className = `gl-feedback-box show ${isCorrect ? 'correct' : 'incorrect'}`;
    }
    
    if (headingEl) {
        headingEl.innerHTML = isCorrect ? '✓ CORRECT // FINDING VERIFIED' : '✗ INCORRECT // EVIDENCE DISCREPANCY';
    }
    
    if (reactEl) {
        reactEl.textContent = isCorrect ? q.reactions.correct : q.reactions.incorrect;
    }
    
    if (explEl) {
        explEl.textContent = q.explanation;
    }
    
    // Highlight correct & incorrect cards
    document.querySelectorAll('.gl-option-card').forEach((card, optIdx) => {
        card.classList.add('disabled');
        if (optIdx === q.correct) {
            card.classList.add('correct');
        } else if (optIdx === userChoice && !isCorrect) {
            card.classList.add('incorrect');
        }
    });
}

function nextQuestion() {
    if (currentQuestionIndex < quizQuestions.length - 1) {
        selectedOptionTemp = null;
        renderQuestion(currentQuestionIndex + 1);
    } else {
        calculateAndShowScore();
    }
}

// ── 4. SCORE & RANK CALCULATION ───────────────────────────────────────
function calculateAndShowScore() {
    if (quizTimerInterval) clearInterval(quizTimerInterval);
    
    let correctCount = 0;
    userAnswers.forEach((ans, idx) => {
        if (ans === quizQuestions[idx].correct) {
            correctCount++;
        }
    });
    
    const total = quizQuestions.length;
    const accuracy = Math.round((correctCount / total) * 100);
    const elapsedSeconds = Math.floor((Date.now() - quizStartTime) / 1000);
    const m = String(Math.floor(elapsedSeconds / 60)).padStart(2, '0');
    const s = String(elapsedSeconds % 60).padStart(2, '0');
    const timeFormatted = `${m}:${s}`;
    
    let rank = "";
    let rankDesc = "";
    
    if (accuracy >= 90) {
        rank = "🛡️ ELITE CYBER THREAT INVESTIGATOR";
        rankDesc = "Exceptional analytical precision. You fully reconstructed the multi-layer attack across AI, Web3, and API domains with pristine accuracy.";
    } else if (accuracy >= 80) {
        rank = "🔍 SENIOR INVESTIGATOR";
        rankDesc = "Strong forensic reasoning. You identified the core trust chain vulnerabilities and authorization boundary failures.";
    } else if (accuracy >= 70) {
        rank = "⚡ CYBER INVESTIGATOR";
        rankDesc = "Solid understanding of the incident. You recognize how AI confidence was improperly treated as transaction authorization.";
    } else if (accuracy >= 60) {
        rank = "📋 JUNIOR INVESTIGATOR";
        rankDesc = "Basic case understanding established. Recommended to review data provenance and least privilege principles.";
    } else {
        rank = "⚠️ INVESTIGATION REQUIRES REVIEW";
        rankDesc = "Case evidence was incomplete or misinterpreted. Review the mission overview timeline and retry the assessment.";
    }
    
    // Update Score Screen Elements
    document.getElementById('score-num').textContent = `${correctCount} / ${total}`;
    document.getElementById('accuracy-num').textContent = `${accuracy}%`;
    document.getElementById('time-num').textContent = timeFormatted;
    document.getElementById('evidence-num').textContent = '5 / 5';
    document.getElementById('rank-title').textContent = rank;
    document.getElementById('rank-desc').textContent = rankDesc;
    
    // Sync with backend API
    fetch('/api/lab6/post-investigation-result', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.csrfToken
        },
        body: JSON.stringify({
            score: correctCount,
            total: total,
            accuracy: accuracy,
            rank: rank,
            time_taken: timeFormatted
        })
    }).catch(err => console.log('Score logged locally'));
    
    showSection('score');
}

function restartQuiz() {
    userAnswers = new Array(quizQuestions.length).fill(null);
    selectedOptionTemp = null;
    currentQuestionIndex = 0;
    startQuizTimer();
    renderQuestion(0);
    showSection('quiz');
}

// ── 5. FINAL REVEAL & CLIFFHANGER SCENE ────────────────────────────────
function triggerFinalReveal() {
    showSection('reveal');
}

function copyCampaignDossier() {
    const text = `CASE NEX-042 FORENSIC DOSSIER
==================================================
Case Status: CONTAINED
Campaign ID: ORION-NEXUS (ACTIVE)
Adversary: ADV-CONVERGENCE-APT
Target Footprint: 14 Wallets | 04 Networks | 03 AI Systems
Key Vector: AI Context Manipulation & Automated Authorization Bypass
Lesson: AI Confidence is NOT Authorization.`;
    navigator.clipboard.writeText(text).then(() => {
        alert('Dossier copied to clipboard!');
    });
}

// ── 6. SUBMIT LAB & CELEBRATION MODAL ─────────────────────────────────
async function submitFinalLabFromPost() {
    try {
        const res = await fetch('/api/lab/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken
            },
            body: JSON.stringify({ lab_id: 'lab6' })
        });
        const data = await res.json();
        openPostCelebrationModal();
    } catch (err) {
        console.error('Submit lab error:', err);
        openPostCelebrationModal();
    }
}

function openPostCelebrationModal() {
    const modal = document.getElementById('gl-post-celebration-modal');
    if (modal) {
        modal.style.display = 'flex';
        
        // Sync values from score card if available
        const accEl = document.getElementById('accuracy-num');
        const rankEl = document.getElementById('rank-title');
        const rankDescEl = document.getElementById('rank-desc');
        
        const modalAcc = document.getElementById('modal-accuracy-val');
        const modalRank = document.getElementById('modal-rank-title');
        const modalDesc = document.getElementById('modal-rank-desc');
        
        if (accEl && modalAcc) modalAcc.textContent = accEl.textContent;
        if (rankEl && modalRank) modalRank.textContent = rankEl.textContent;
        if (rankDescEl && modalDesc) modalDesc.textContent = rankDescEl.textContent;
        
        launchPostCelebrationConfetti();
    }
}

function closePostCelebrationModal() {
    const modal = document.getElementById('gl-post-celebration-modal');
    if (modal) {
        modal.style.display = 'none';
        stopPostCelebrationConfetti();
    }
}

let postConfettiAnimId = null;
let postConfettiParticles = [];

function launchPostCelebrationConfetti() {
    const canvas = document.getElementById('post-celebration-confetti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const colors = ['#00f0ff', '#00ff88', '#facc15', '#a855f7', '#ff3366', '#38bdf8', '#ffffff'];
    postConfettiParticles = [];

    for (let i = 0; i < 160; i++) {
        postConfettiParticles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height - canvas.height,
            size: Math.random() * 8 + 5,
            color: colors[Math.floor(Math.random() * colors.length)],
            speedY: Math.random() * 3 + 2,
            speedX: Math.random() * 4 - 2,
            rotation: Math.random() * 360,
            rotationSpeed: Math.random() * 6 - 3,
            shape: Math.random() > 0.3 ? 'rect' : 'circle'
        });
    }

    function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        postConfettiParticles.forEach(p => {
            p.y += p.speedY;
            p.x += p.speedX;
            p.rotation += p.rotationSpeed;

            if (p.y > canvas.height) {
                p.y = -20;
                p.x = Math.random() * canvas.width;
            }

            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate((p.rotation * Math.PI) / 180);
            ctx.fillStyle = p.color;

            if (p.shape === 'rect') {
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
            } else {
                ctx.beginPath();
                ctx.arc(0, 0, p.size / 2, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.restore();
        });

        postConfettiAnimId = requestAnimationFrame(render);
    }

    if (postConfettiAnimId) cancelAnimationFrame(postConfettiAnimId);
    render();
}

function stopPostCelebrationConfetti() {
    if (postConfettiAnimId) {
        cancelAnimationFrame(postConfettiAnimId);
        postConfettiAnimId = null;
    }
}

