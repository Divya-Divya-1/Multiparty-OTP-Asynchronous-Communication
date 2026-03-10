# Multiparty One-Time Pad Protocol for Asynchronous Communication

## Overview

This project implements a **multiparty one-time pad (OTP) communication protocol** designed for asynchronous message transmission while maintaining **perfect secrecy**.

The protocol minimizes wasted pads while ensuring that pads are **never reused across multiple communicating parties**.

The implementation supports communication scenarios involving **3, 4, or 5 parties**.

This project was developed as part of a cryptography course and includes both the **protocol implementation and simulation testing**.

---

## Problem

In asynchronous communication systems, multiple parties may send messages at unpredictable times.

This creates two main challenges:

1. Ensuring that **one-time pads are never reused**
2. Minimizing **wasted pads caused by conflicts between senders**

Traditional approaches such as splitting pads into equal sections can lead to **significant pad wastage and inefficient usage**.

The goal of this project is to design a protocol that:

- prevents pad reuse
- reduces wasted pads
- supports multiple communicating parties
- maintains perfect secrecy

---

## Protocol Design

Each party in the system is assigned:

- a **starting pad index**
- a **communication direction** (`forward` or `backward`)

Example for **3-party communication**:

```
Pad Sequence: 0 ------------------- n/2 ------------------- n-1

Party0 starts at 0   → forward
Party1 starts at n-1 → backward
Party2 starts at n/2 → forward
```

Each party maintains:

- last pad index used
- pads already used
- wasted pads due to conflicts

---

## d-Separation Rule

To prevent pad conflicts, the protocol introduces a **d-separation constraint**.

A party can only use a pad index if:

```
|current_index − other_party_last_index| ≥ d
```

If this condition is not satisfied:

- the pad is skipped
- the skipped pad is counted as **wasted**

This ensures pads used by different parties remain sufficiently separated.

---

## Security Guarantees

The protocol guarantees:

### Perfect Secrecy

- No pad is reused
- Each message uses a unique pad index

### Minimal Pad Waste

Worst-case wasted pads:

```
(m − 1) * n / m
```

Minimum expected wasted pads:

```
(m − 1) * d
```

Where:

- `m` = number of parties  
- `n` = pad length  
- `d` = minimum separation constraint

---

## Simulation Scenarios

The protocol was tested under three different communication scenarios.

### Scenario A – Single Sender

Only one party sends messages continuously.

Expected wasted pads:

```
0
```

Because there are no conflicts with other parties.

---

### Scenario B – Alternating Senders

Two parties alternate sending messages.

Expected wasted pads:

```
(m − 1) * d
```

Conflicts occur when parties approach each other's pad regions.

---

### Scenario C – Random Senders

All parties send messages with random probabilities.

Pad wastage varies depending on message timing but remains within protocol limits.

---

## Implementation

The project contains two main Python components.

### Protocol Implementation

File:

```
protocol/multiparty_otp_protocol.py
```

Implements:

- `Party` class
- `MultipartyOTPProtocol` class
- pad allocation algorithm
- d-separation enforcement
- pad usage tracking

---

### Simulation Testing

File:

```
simulation/multiparty_otp_testing.py
```

This program simulates protocol behavior and calculates the average number of wasted pads across multiple trials.

---

## How to Run

Run the simulation using Python:

```bash
python multiparty_otp_testing.py
```

Example parameters inside the script:

```python
m = 4      # number of parties
n = 100    # pad length
d = 2      # separation constraint
trials = 6000
```

Example output:

```
Scenario (a) Average Wasted Pads: X
Scenario (b) Average Wasted Pads: X
Scenario (c) Average Wasted Pads: X
```

---

## Technologies Used

- Python
- Cryptography concepts
- Simulation testing
- Algorithm design

---

## Learning Outcomes

This project demonstrates:

- cryptographic protocol design
- asynchronous secure communication
- simulation-based analysis
- algorithm design for resource efficiency
- secure pad allocation strategies

---


## Disclaimer

This project was developed for **academic purposes** as part of a cryptography course to explore secure communication protocol design.
