# Active Walk Model

This is an interactive warehouse engineering analytics application for evaluating
walking-time standards associated with order-picking operations. Speicifically warehouses operating under manhattan active systems. 

This project demonstrates the modernization of a legacy analytical workflow
into a Python-based processing pipeline with an interactive Streamlit user
interface.

> **Portfolio Demo**
>
> This repository uses synthetic demonstration data only.
> No proprietary operational data, credentials, production database
> connections, or confidential company information are included.

---

## Problem

Warehouse order-picking involves a significant amount of operator travel.

Existing engineered standards may not always reflect changes in:

- facility layout
- location configuration
- transaction sequences
- pick density
- walking distance
- operating patterns

The Active Walk Model analyzes these factors and estimates a proposed walking
standard that can be compared against the current standard.

---

## Application Workflow

```text
Facility Layout
      ↓
Location Model
      ↓
Pick Transactions
      ↓
Location Matching
      ↓
Walk Components
      ↓
Regression
      ↓
Proposed Standard
      ↓
Impact Analysis