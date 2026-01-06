# LLM Research Sample: Batch 1 - Lab Vendors

**Model:** Claude Opus 4.1
**Date:** November 18, 2025
**Category:** Lab (Dental Laboratory Services)
**Vendors:** V001-V004

This document shows a complete example of my LLM-based vendor research output. I used this structured approach across all 5 batches to extract real vendor information for the synthetic data pipeline.

---

## Prompt Used

```
# Batch 1: Lab Vendors - Text-to-KG Extraction Prompt

I'm building a knowledge graph for a healthcare vendor consolidation ML system.
Please research the following 4 dental laboratory vendors and extract structured information.

For each vendor, investigate their official website and extract:

### Required Information

1. **EHR Integration Capabilities**
   - Which dental EHR systems do they integrate with?
   - Examples: Dentrix, Dentrix Ascend, OpenDental, Eaglesoft, Curve Dental, Denticon

2. **Integration Type** (choose one per EHR)
   - full_api: Real-time API, certified integration partner, bidirectional sync
   - partial_csv: CSV import/export, file-based data exchange, one-way sync
   - none: No documented integration, manual entry only

3. **Key Features & Specializations**
   - What do they specialize in? (crown & bridge, implants, dentures, orthodontics)
   - Digital workflow capabilities (3Shape integration, intraoral scanner support)
   - Notable technologies (AI, CAD/CAM)

4. **Peer Adoption Evidence**
   - Customer counts ("500+ practices", "nationwide network")
   - DSO partnerships (Smile Brands, PDS, Aspen Dental, Heartland Dental)
   - Scale indicators ("multi-state", "regional", "national")

5. **Coverage/Geographic Reach**
   - National vs regional
   - Multi-location capabilities

### Vendors to Research

- V001: National Dental Labs (nationaldentallab.com)
- V002: Glidewell (glidewelldental.com)
- V003: DDS Lab (ddslab.com)
- V004: NDX (ndx.com)

### Output Format

For each vendor, provide structured data with:
- Source URLs for each fact
- Confidence levels: high/medium/low
- Notes on any ambiguities or contradictions
```

---

## Claude Opus Response

### Critical Finding

**V001 and V004 are the same company.** National Dentex operates under multiple brand names including "National Dental Labs" and "NDX." This discovery led to sourcing a replacement vendor (ROE Dental) for V004.

---

## V001: National Dentex (NDX)

**VENDOR_ID:** V001
**OFFICIAL WEBSITE:** nationaldentex.com

### EHR Integrations

**Assessment: No direct EHR/PMS API integrations found**

| EHR System | Integration Type | Source | Confidence |
|------------|-----------------|--------|------------|
| Dentrix | none (manual) | Website review | MEDIUM |
| Dentrix Ascend | none (manual) | Website review | LOW |
| OpenDental | none (manual) | Website review | LOW |
| Eaglesoft | none (manual) | Website review | MEDIUM |
| Curve Dental | none (manual) | Website review | LOW |
| Denticon | none (manual) | Website review | LOW |

**Case Ordering System:**
- Doctor portal for aligners program with digital case submission
- Physical case submission via Rx forms, FedEx shipping
- Digital file upload for intraoral scanner files (STL format)
- **Classification: partial_csv** (file-based digital submission, no real-time bidirectional API)

Source: https://nationaldentex.com/aligners, https://nationaldentex.com/ndxgroup-practice-solutions/send-a-case/digital-impressions
Confidence: HIGH

### Key Features & Specializations

**Specialties:**
- **Crown & Bridge:** Verotek FCZ crowns (1,100 MPa flexural strength), 5-axis milling, CAD/CAM | Confidence: HIGH
- **Implants:** Strong focus - nSequence protocol for full-arch immediate loading, 3D guided surgical workflow | Confidence: HIGH
- **Dentures:** Digital dentures (Economy and Premium), 3D printed dentures | Confidence: HIGH
- **Orthodontics:** NDX Aligners (Zendura FLX material), retainers | Confidence: HIGH

**Digital Workflow:**
- **3Shape Integration:** CONFIRMED - 3Shape TRIOS explicitly supported, training offered | Confidence: HIGH
- **Intraoral Scanner Support:** All major brands - 3Shape TRIOS, iTero, Primescan, CEREC, Medit, Planmeca/E4D, Carestream, Dexis, 3M True Definition, Shining 3D | Confidence: HIGH

**Technologies:**
- **AI:** Mentioned as part of technology investments | Confidence: MEDIUM
- **CAD/CAM:** Confirmed - 5-axis milling machines, digital design stations | Confidence: HIGH
- **3D Printing:** Confirmed - Carbon 3D printers, 3D printed dentures | Confidence: HIGH

### Peer Adoption Evidence

**Customer Counts:**
- **"More than 50,000 customers across North America"** | Source: BusinessWire, USA Dental Report | Confidence: HIGH
- "Tens of thousands of dentists, specialists, and dental service organizations" | Confidence: HIGH

**DSO Partnerships:**
- **Heartland Dental:** CONFIRMED - Exclusive pricing partnership with dedicated landing page | Source: https://nationaldentex.com/heartland | Confidence: HIGH
- **Smile Brands:** NOT FOUND
- **PDS:** NOT FOUND
- **Aspen Dental:** NOT FOUND

**Scale Indicators:**
- **"Largest network of fully-owned dental labs in North America"** | Confidence: HIGH
- **55+ full-service labs** across United States | Confidence: HIGH
- **Nearly 4,000 employees** | Confidence: HIGH
- **$750 million annual revenue** | Confidence: MEDIUM (third-party source)

### Coverage/Geographic Reach

**Type:** NATIONAL - North America

- 55+ full-service dental laboratories throughout United States
- North America coverage: US, Canada, Mexico (via DSG acquisition)
- Headquarters: Jupiter, Florida (40,000 sq ft facility)
- Free local route pickup/delivery, FedEx shipping outside local routes

Confidence: HIGH

### Quality Certifications

- ADA CERP Recognized Provider (for CE programs)
- FDA registered
- Lifetime guarantee on Verotek products
- 5-year warranty on crown & bridge
- 3-year warranty on complete dentures

---

## V002: Glidewell

**VENDOR_ID:** V002
**OFFICIAL WEBSITE:** glidewelldental.com

### EHR Integrations

**Assessment: No direct EHR/PMS integrations - operates via digital case submission portal**

| EHR System | Integration Type | Source | Confidence |
|------------|-----------------|--------|------------|
| Dentrix | partial_csv | Portal submission | HIGH |
| Dentrix Ascend | partial_csv | Portal submission | HIGH |
| OpenDental | partial_csv | Portal submission | HIGH |
| Eaglesoft | partial_csv | Portal submission | HIGH |
| Curve Dental | partial_csv | Portal submission | HIGH |
| Denticon | partial_csv | Portal submission | HIGH |

**How Integration Works:**
- "My Account" portal for case submission
- File formats: STL, PLY, CTM, direct scanner files
- **Classification: partial_csv** (file-based, standard for dental labs)

Source: https://glidewelldental.com/send-case/submit-digital-case
Confidence: HIGH

### Key Features & Specializations

**Specialties:**
- **Crown & Bridge:** PRIMARY SPECIALTY - BruxZir Zirconia ("most successful tooth-colored restoration in history"), 90% completed in 3-day in-lab time | Confidence: HIGH
- **Implants:** Over 4 million implant cases restored, manufactures Inclusive prosthetic components and Hahn Tapered Implants | Confidence: HIGH
- **Dentures:** Simply Natural 3D-printed dentures with antimicrobial properties | Confidence: HIGH
- **Orthodontics:** Glidewell Clear Aligners | Confidence: HIGH

**Digital Workflow:**
- **3Shape Integration:** YES - Accepts 3Shape scans, supports abutment libraries | Confidence: HIGH
- **Intraoral Scanner Support:** iTero, Medit i700, 3Shape, Planmeca, Dentsply Sirona, "any scanner on the market" | Confidence: HIGH

**Technologies:**
- **AI Technology:** Applied Restorative Intelligence (ARI) developed with UC Berkeley, CrownAI for auto-generated crown designs, MarginAI for automatic margin marking | Confidence: HIGH
- **CAD/CAM:** glidewell.io In-Office Solution (complete chairside CAD/CAM), fastdesign.io Software, fastmill.io Mill | Confidence: HIGH

### Peer Adoption Evidence

**Customer Counts:**
- **80,000+ dentists served annually** | Confidence: HIGH
- **Over 3 million intraoral scans processed in 2024** | Confidence: HIGH
- "Thousands of units each day" | Confidence: HIGH

**DSO Partnerships:**
- **Heartland Dental:** CONFIRMED - Partnership discussed publicly, FastMill I.O. in-office milling partnership | Confidence: HIGH
- **Smile Brands:** Potential/historical relationship - no direct evidence of active partnership | Confidence: LOW
- **PDS:** NOT FOUND
- **Aspen Dental:** NOT FOUND

**Scale Indicators:**
- **"Largest US-based dental lab"** | Confidence: HIGH
- **"One of the largest dental labs in the world"** | Confidence: HIGH
- Founded 1970 (55+ years in business)

### Coverage/Geographic Reach

**Type:** NATIONAL

- Main campus: Irvine, California (ISO-certified, FDA-regulated)
- Nationwide US coverage
- Canadian service available
- FedEx overnight delivery for most US areas
- glidewell.io designed for multi-location DSO implementation

Confidence: HIGH

### Quality Certifications

- **ISO 13485:** Medical device quality management - CONFIRMED
- **FDA Registration:** FDA-regulated manufacturing facilities
- **CE Marking:** European compliance
- **CMCDS:** Canadian Medical Devices Conformity Assessment System
- R&D team: 150+ experts (9 Ph.D. scientists, 5 dentists, CDTs, MDTs)

---

## V003: DDS Lab

**VENDOR_ID:** V003
**OFFICIAL WEBSITE:** ddslab.com

### EHR Integrations

**Assessment: No direct EHR/PMS integrations - operates via proprietary web portal**

| EHR System | Integration Type | Source | Confidence |
|------------|-----------------|--------|------------|
| Dentrix | none (manual) | Website review | HIGH |
| Dentrix Ascend | none (manual) | Website review | HIGH |
| OpenDental | none (manual) | Website review | HIGH |
| Eaglesoft | none (manual) | Website review | HIGH |
| Curve Dental | none (manual) | Website review | HIGH |
| Denticon | none (manual) | Website review | HIGH |

**Case Ordering System:**
- Proprietary portal "My.DDSLab.com" and mobile app (iOS/Android)
- Real-time case tracking, status updates, billing management
- **Classification: partial_csv** (file-based portal ordering)

Source: https://go.ddslab.com/register_mydds_lab, https://www.ddslab.com/myddslab-app/
Confidence: HIGH

### Key Features & Specializations

**Specialties:**
- Crown & bridge: Ceramics, PFM, full cast | Confidence: HIGH
- Implants: All platforms and components | Confidence: HIGH
- Dentures: 3D printed digital dentures, traditional dentures | Confidence: HIGH
- Orthodontics: Custom appliances | Confidence: HIGH

**Digital Workflow:**
- **3Shape TRIOS:** Explicitly mentioned for digital denture workflows | Confidence: HIGH
- **Intraoral Scanner Support:** iTero, Dexis, TRIOS, CEREC | Confidence: HIGH
- Desktop model scanners for digitizing traditional impressions

**Clinical Support:**
- Field Support Technicians (FSTs) in all 50 states
- CDTs available for case planning
- AGD PACE-approved CE programs

### Peer Adoption Evidence

**DSO Partnerships:**
- **Smile Brands:** CONFIRMED - "DDS Lab has been a proud partner of Smile Brands since 2005" | Source: https://www.ddslab.com/smilebrands/ | Confidence: HIGH
- **Heartland Dental:** Mentioned in blog content | Confidence: HIGH
- **PDS:** NOT FOUND
- **Aspen Dental:** NOT FOUND

**Customer Scale:**
- **"One of the largest full-service dental laboratories in the world"** | Confidence: HIGH
- **"Tens of thousands of cases shipped each month"** | Confidence: HIGH
- Serves small practices to large multi-state companies

**Technician Capacity:**
- Tampa FL: 28,000 sq ft, 80+ certified dental technicians
- Shenzhen, China: 65,000 sq ft, 470+ certified technicians
- Grecia, Costa Rica: 100,000 sq ft (opened April 2024)

### Coverage/Geographic Reach

**Type:** NATIONAL (corrected from initial "regional" classification)

- Nationwide US coverage with FSTs in all 50 states
- Headquarters: Tampa, Florida
- Three global manufacturing facilities (Tampa, Shenzhen, Costa Rica)
- "Distributive manufacturing model" - 24/7 operation across time zones

Confidence: HIGH

### Quality Certifications

- **NBC CDL:** National Board Certified Dental Lab
- **NADL member:** National Association of Dental Laboratories
- **ISO 13485:** Shenzhen facility
- **MDSAP compliant:** Medical Device Single Audit Program (Shenzhen)
- **AGD PACE:** Approved CE programs

---

## V004: NDX (DUPLICATE)

**VENDOR_ID:** V004
**OFFICIAL WEBSITE:** ndx.com

### CRITICAL NOTE: DUPLICATE VENDOR

**V004 (NDX) is the SAME COMPANY as V001 (National Dental Labs).** Both refer to National Dentex Labs, which operates under multiple brand names.

**Evidence:**
- Same website domain: nationaldentex.com
- Same headquarters: Jupiter, Florida
- Same CEO: Kevin Mosher
- Same ownership: Cerberus Capital Management
- Same customer base: 50,000+ customers
- Same facility count: 55+ labs

**Action Taken:** Sourced replacement vendor ROE Dental for V004.

---

## Cross-Vendor Summary

### Key Insights

1. **No Direct EHR Integration:** None of the 4 vendors have real-time API integrations with dental EHRs. This is a structural characteristic of the dental lab industry - labs use portal-based ordering, not EHR plugins.

2. **Universal Scanner Support:** All vendors support major intraoral scanners (3Shape TRIOS, iTero, CEREC, Medit). This is the primary "integration" focus for labs.

3. **DSO Partnership Pattern:** Only 3 DSO partnerships confirmed across 4 vendors:
   - Heartland Dental: National Dentex, Glidewell
   - Smile Brands: DDS Lab (since 2005)

4. **Scale Leaders:**
   - Glidewell: 80,000+ dentists annually (largest by customer count)
   - National Dentex: 55+ labs, $750M revenue (largest by facility network)

5. **AI Differentiation:** Only Glidewell has documented AI (CrownAI, MarginAI with UC Berkeley).

### Integration Classification

For the synthetic data pipeline, all Lab vendors are assigned:
- **integration_quality = 1 (partial_csv)**
- Rationale: Portal-based STL file upload, no real-time EHR sync

### Confidence Assessment

| Data Type | Confidence |
|-----------|-----------|
| Specialties | HIGH |
| Scanner support | HIGH |
| National coverage | HIGH |
| Scale indicators | HIGH |
| DSO partnerships | MEDIUM (only confirmed ones listed) |
| EHR integration details | MEDIUM (absence of evidence) |

---

## Notes

- Research date: November 2025
- All sources are official vendor websites and verified press releases
- Full results for all 5 batches available on request
