# finops-intelligence-model

A FinOps intelligence model that connects infrastructure cost to workload behavior and business value to support commitment strategy, optimization priorities, and engineering decisions.

## Why this project exists

Traditional FinOps dashboards are very good at showing **what changed**:
- spend increased
- an anomaly occurred
- a savings opportunity exists

But strong FinOps decision-making also requires understanding **why cost changed** and whether that change reflects:
- healthy growth
- architecture inefficiency
- workload drift
- commitment coverage risk

This project is designed to bridge that gap by connecting:

**Infrastructure Cost → Workload Behavior → Business Value → FinOps Decision**

## Core idea

The model helps answer questions such as:

1. Did cost increase because demand increased, or because the system became less efficient?
2. What workload behavior is driving cloud cost?
3. Is this cost aligned with business value?
4. Which portion of usage is stable enough for Savings Plans or Reserved Instance strategy?
5. Which anomalies should be routed to engineering, finance, or product teams?

## What this project models

This repository starts with a simple API-driven workload example and builds four connected layers:

### 1. Infrastructure cost layer
Models cloud cost using workload drivers such as:
- API calls
- duration
- memory
- request pricing
- compute pricing

### 2. Workload behavior layer
Translates technical activity into behavior metrics such as:
- API calls per customer
- API calls per transaction
- baseline vs variable demand

### 3. Business value layer
Connects cost to value using metrics such as:
- transactions
- contribution margin per transaction
- cost per transaction

### 4. FinOps decision layer
Generates insights to support:
- anomaly interpretation
- optimization prioritization
- commitment strategy
- engineering decision support

## Example outputs

This model produces outputs such as:
- total infrastructure cost
- API calls per customer
- API calls per transaction
- cost per transaction
- growth vs inefficiency classification
- stable baseline usage estimate
- commitment candidate usage

## Example use cases

### Use case 1: Explain a cost increase
A rise in cost may be caused by:
- more customers and more transactions, which may be healthy growth
- more API calls per transaction, which may indicate inefficiency

This model helps distinguish between the two.

### Use case 2: Support commitment strategy
Savings Plans and Reserved Instances should generally align to stable baseline demand, not volatile demand.

This model helps estimate:
- stable usage
- variable usage
- commitment candidate usage
- on-demand exposure risk

### Use case 3: Improve engineering conversations
Instead of saying:
> “Cloud cost increased”

the model supports a more useful explanation:
> “API calls per transaction increased, which raised cost per transaction without increasing value.”

## MVP scope

Version 1 focuses on one story:

**API workload → cloud cost → customer value → commitment insight**

### MVP inputs
- monthly API calls
- average duration (ms)
- memory (MB)
- cost per 1M requests
- cost per GB-second
- customers
- transactions per customer
- contribution margin per transaction

### MVP outputs
- total cost
- request cost
- compute cost
- API calls per customer
- total transactions
- API calls per transaction
- cost per transaction
- growth vs inefficiency interpretation
- baseline demand estimate for commitment decisions

  ## How to run

Install dependencies:

```bash
pip install -r requirements.txt

## Repository structure

```text
finops-intelligence-model/
├── README.md
├── data/
│   ├── raw/
│   └── sample/
├── notebooks/
│   ├── 01_cost_normalization.ipynb
│   ├── 02_workload_behavior.ipynb
│   ├── 03_unit_economics.ipynb
│   └── 04_commitment_intelligence.ipynb
├── src/
│   ├── ingest/
│   ├── models/
│   ├── metrics/
│   ├── commitments/
│   └── reporting/
├── docs/
│   ├── architecture.md
│   ├── metrics.md
│   └── use_cases.md
├── outputs/
│   ├── charts/
│   └── tables/
└── requirements.txt
