# Zapier Setup — Lead Capture → Contractor Routing

## Quick Setup (15 min)

### Zap 1: Formspree → Google Sheets (Lead Log)

**Trigger:** Formspree - New Email Submission
- Form ID: `xpwzgqkd` (service quotes form)
- Fields: name, email, phone, zip, service_details

**Action 1:** Google Sheets - Create Spreadsheet Row
- Spreadsheet: `QMA_Leads`
- Sheet: `Leads`
- Columns:
  - timestamp (from Formspree submission time)
  - name
  - email
  - phone
  - zip
  - service
  - status (default: "new")

**Action 2:** Gmail - Send Email
- To: `leads@quotemyanything.com`
- Subject: `[{service}] Lead from {zip} — {name}`
- Body:
```
Name: {name}
Email: {email}
Phone: {phone}
ZIP: {zip}
Service: {service}
Details: {service_details}

Dashboard: https://quotemyanything.com/for-pros.html
```

---

### Zap 2: Formspree → Google Sheets (Route by Service/ZIP)

**Same trigger + action 1 as above**

**Action 3:** Conditional Logic
- IF service = "roofing" AND zip contains "787"
  - THEN send SMS or email to assigned roofer(s)
  
Example contractor assignment:
- **Roofing + 78704**: Austin Roofing Pro (email: quotes@austinroofing.local)
- **HVAC + 78701**: AC Experts (email: quotes@acexperts.local)

**Action 4:** Google Sheets (Contractor Notification Log)
- Track: date, contractor, lead count

---

## Manual Workflow (if Zapier not ready)

1. New lead arrives → Formspree email
2. Copy lead data to `QMA_Leads` sheet
3. Match service + ZIP to contractor
4. Email contractor with lead details
5. Log in sheet, update status when quoted

---

## Contractor Database (Google Sheet)

Create sheet: `Contractors`

| Name | Service | ZIPs | Email | Plan | Active |
|------|---------|------|-------|------|--------|
| Austin Roofing Pro | Roofing | 78704,78703,78701 | quotes@austinroofing.local | per-lead | Yes |
| AC Experts Austin | HVAC | 78704,78702,78723 | quotes@acexperts.local | monthly | Yes |

---

## Revenue Tracking (Google Sheet)

Create sheet: `Revenue`

| Date | Contractor | Service | Type | Amount | Payment Status |
|------|-----------|---------|------|--------|-----------------|
| 2026-06-05 | Austin Roofing Pro | Roofing | per-lead | $25 | pending |
| 2026-06-05 | AC Experts | HVAC | monthly | $199 | paid |

Monthly MRR = SUM of all "monthly" rows

---

## Next Steps

1. Create three Google Sheets: `QMA_Leads`, `Contractors`, `Revenue`
2. Set up two Zapier zaps above (Formspree → Sheets → Email alerts)
3. Add first 5 contractors to `Contractors` sheet
4. Test: submit form, verify lead arrives in sheets + email alert sent
5. Route first 10 leads manually to contractors
6. Track quotes received + won status

**Success metric:** 80%+ of assigned leads get quoted within 48h
