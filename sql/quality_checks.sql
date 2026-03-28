-- Prescription Data Quality Checks
-- SQL validation queries for a synthetic community pharmacy dataset
-- This file focuses on duplicate patterns, missing links, reimbursement gaps,
-- and refill-timing inconsistencies in prescription-related workflows.

-- =========================================================
-- CHECK 1: Duplicate patient-drug records within a short refill window
-- Purpose:
-- Identify cases where the same patient receives the same active ingredient
-- again within a short number of days, which may suggest duplicate supply,
-- early refill, or workflow inconsistency.
-- =========================================================

SELECT
    p1.prescription_id AS prescription_id_1,
    p2.prescription_id AS prescription_id_2,
    p1.patient_id,
    p1.active_ingredient,
    p1.issue_date AS issue_date_1,
    p2.issue_date AS issue_date_2,
    p1.refill_window_days
FROM prescriptions p1
JOIN prescriptions p2
    ON p1.patient_id = p2.patient_id
    AND p1.active_ingredient = p2.active_ingredient
    AND p1.prescription_id < p2.prescription_id
WHERE
    julianday(p2.issue_date) - julianday(p1.issue_date) < p1.refill_window_days;

-- =========================================================
-- CHECK 2: Same active ingredient in overlapping prescription records
-- Purpose:
-- Identify cases where treatment periods for the same patient and active
-- ingredient appear to overlap, which may suggest duplicate or excessive supply.
-- Approximate end date is calculated as issue_date + duration_days.
-- =========================================================

SELECT
    p1.prescription_id AS prescription_id_1,
    p2.prescription_id AS prescription_id_2,
    p1.patient_id,
    p1.active_ingredient,
    p1.issue_date AS issue_date_1,
    p1.duration_days AS duration_days_1,
    p2.issue_date AS issue_date_2,
    p2.duration_days AS duration_days_2
FROM prescriptions p1
JOIN prescriptions p2
    ON p1.patient_id = p2.patient_id
    AND p1.active_ingredient = p2.active_ingredient
    AND p1.prescription_id < p2.prescription_id
WHERE
    julianday(p2.issue_date) <= julianday(p1.issue_date) + p1.duration_days;

-- =========================================================
-- CHECK 3: Missing patient link
-- Purpose:
-- Identify prescription records that do not match a valid patient record
-- in the Patients table.
-- =========================================================

SELECT
    pr.prescription_id,
    pr.patient_id,
    pr.drug_name,
    pr.active_ingredient
FROM prescriptions pr
LEFT JOIN patients pa
    ON pr.patient_id = pa.patient_id
WHERE
    pa.patient_id IS NULL;

-- =========================================================
-- CHECK 4: Missing reimbursement flag
-- Purpose:
-- Identify prescription rows where the reimbursement status is missing,
-- blank, or not documented.
-- =========================================================

SELECT
    prescription_id,
    patient_id,
    drug_name,
    active_ingredient,
    reimbursement_flag
FROM prescriptions
WHERE
    reimbursement_flag IS NULL
    OR TRIM(reimbursement_flag) = '';

-- =========================================================
-- CHECK 5: Repeat or chronic prescription issued too early
-- Purpose:
-- Identify repeat or chronic prescriptions where a new issue date appears
-- earlier than expected based on the refill window.
-- =========================================================

SELECT
    p1.prescription_id AS previous_prescription_id,
    p2.prescription_id AS current_prescription_id,
    p1.patient_id,
    p1.active_ingredient,
    p1.prescription_type,
    p1.issue_date AS previous_issue_date,
    p2.issue_date AS current_issue_date,
    p1.refill_window_days
FROM prescriptions p1
JOIN prescriptions p2
    ON p1.patient_id = p2.patient_id
    AND p1.active_ingredient = p2.active_ingredient
    AND p1.prescription_id < p2.prescription_id
WHERE
    p1.prescription_type IN ('Repeat', 'Chronic')
    AND julianday(p2.issue_date) - julianday(p1.issue_date) < p1.refill_window_days;
