# Prescription Data Quality Checks: A Healthcare-Informed Mini Portfolio Project

## Executive Summary
This project is a small, rule-based data quality review exercise built with Python and SQL. It uses a fully synthetic prescription dataset inspired by community pharmacy workflows to identify and classify common data quality issues related to dosage, frequency, duplicate dispensing patterns, diagnosis alignment, documentation completeness, and refill timing.

The goal is to demonstrate a practical healthcare-informed QA mindset, not to simulate clinical decision-making.

---

## Why This Project Matters
In prescription-related workflows, poor data quality can create avoidable confusion, documentation ambiguity, duplication concerns, reimbursement friction, and medication-safety review flags.

This project focuses on the kinds of structured checks that help identify records needing closer review, especially when:
- dosage or frequency fields are incomplete or inconsistent,
- quantity does not plausibly match treatment duration,
- diagnosis coding and free-text documentation do not align,
- duplicate fills appear too early,
- or physician comments are too vague to support clear interpretation.

The project is inspired by real-world pharmacy-facing review logic, but all data is synthetic.

---

## Dataset & Privacy Note
All data used in this project is fully synthetic and created for portfolio purposes only.

It does **not** contain:
- real patient data,
- real prescriber identities,
- real reimbursement records,
- or any protected health information.

The project is designed to demonstrate realistic data quality review logic in a safe and clearly non-production context.

---

## Project Structure
This repository contains:

- a synthetic **Patients** table
- a synthetic **Prescriptions** table
- Python-based field and rule checks
- SQL-based relational and duplication checks
- a findings-oriented summary of flagged data quality issues

---

## Key Data Quality Checks
The project includes checks such as:

- missing dosage values
- inconsistent dosage unit formatting
- inconsistent frequency notation
- quantity vs duration/frequency mismatch
- dispense date earlier than issue date
- diagnosis code / diagnosis text mismatch
- duplicate patient-drug records within short refill windows
- repeat or chronic prescription issued too early
- missing or vague physician comments
- unexpected therapy switch without explanatory note

Flagged issues are grouped into practical categories such as:
- administrative / reimbursement-related
- documentation-quality
- safety-sensitive medication review flags

---

## Technology Used
- **Python**
- **Pandas**
- **SQL**
- **CSV / synthetic tabular data**
- **Markdown documentation**

---

## What This Project Demonstrates
This project demonstrates:

- healthcare-informed data quality awareness
- structured QA and documentation-review thinking
- practical Python and SQL use for rule-based validation
- the ability to distinguish between administrative, documentation, and safety-sensitive issues
- a realistic understanding of how small data inconsistencies can affect clarity, continuity, and workflow reliability in prescription-related contexts

---

## What This Project Does Not Claim
This project does **not** claim to:

- make clinical decisions
- evaluate treatment appropriateness
- recommend medication changes
- replace pharmacist or physician judgment
- model a full electronic prescribing system
- represent production-grade healthcare infrastructure
- use real patient data

It is a small portfolio project focused on structured data quality review.

---

## How to Run It
1. Load the synthetic dataset files
2. Run the Python notebook or script for field-level checks
3. Run the SQL queries for relational and duplication checks
4. Review the generated findings summary

---

## Suggested Next Improvements
Possible future extensions could include:
- terminology normalization checks
- structured instruction-text consistency checks
- second-stage review scoring
- a small dashboard summarizing issue frequency by category
