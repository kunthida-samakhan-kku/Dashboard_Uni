# KKU Admission Dashboard — Handoff

> **Research scope:** วิเคราะห์เส้นทางจากนักเรียนมัธยมศึกษาตอนปลายเข้าสู่ระดับปริญญาตรีมหาวิทยาลัยขอนแก่น (KKU) โดยใช้ข้อมูลสาธารณะ/ Open Data ที่ตรวจสอบแหล่งที่มาได้
>
> **Critical data caveat:** จากการตรวจสอบแหล่งข้อมูลสาธารณะที่ค้นพบ ยังไม่พบ Structured Open Data จาก KKU ที่เผยแพร่เป็นตารางรวมว่า “นักศึกษาแรกเข้าแต่ละคน/แต่ละคณะ จบจากสายการเรียนใด” ดังนั้นห้ามสร้าง Cross-tab “สายการเรียนจริง × คณะ” จากข้อมูลจำนวนรับหรือเกณฑ์คุณสมบัติ เพราะสองอย่างนี้ไม่ใช่ข้อมูลภูมิหลังของผู้เข้าเรียนจริง

## 1. Project Overview

Dashboard มีเป้าหมายเพื่ออธิบายเส้นทางการศึกษาจากระดับมัธยมศึกษาตอนปลายไปสู่ระดับปริญญาตรีที่มหาวิทยาลัยขอนแก่น โดยเน้น 3 มิติหลัก:

1. Supply side — จำนวนนักเรียนระดับ ม.ปลาย/เทียบเท่า โดยเฉพาะจังหวัดขอนแก่น
2. Admission side — จำนวนรับ หลักสูตร/สาขา รอบการรับ และข้อมูลที่ KKU ประกาศ
3. Study-background side — ตรวจสอบว่ามีข้อมูลสาธารณะที่เชื่อม “แผนการเรียน/วุฒิเดิม → คณะ/สาขาที่เข้าเรียนจริง” หรือไม่

Dashboard ต้องแยกชัดเจนระหว่าง:
- **Actual observed data:** ข้อมูลนักเรียน/นักศึกษา/ผู้สมัครจริงที่มีตัวเลข
- **Admission criteria:** แผนการเรียนหรือวุฒิที่ “มีสิทธิ์สมัคร/ถูกกำหนดให้รับ”
- **Target but unavailable:** ข้อมูลที่ต้องการแต่ยังไม่พบใน Open Data

## 2. Main Research Question

> “นักเรียน ม.6 ที่เข้าศึกษาต่อระดับปริญญาตรีที่มหาวิทยาลัยขอนแก่น ส่วนใหญ่เลือกเรียนคณะอะไร และมาจากสายการเรียนไหน?”

### Interpretation rule

คำตอบ “คณะอะไร” สามารถวิเคราะห์ได้เมื่อมีจำนวนผู้สมัคร/ผู้ผ่าน/ผู้มีสิทธิ์/ผู้เข้าศึกษาจริงแยกคณะหรือสาขา

คำตอบ “มาจากสายการเรียนไหน” สามารถตอบเชิงจริงได้ **เฉพาะเมื่อพบข้อมูลภูมิหลังของผู้สมัคร/นักศึกษา** ที่มีตัวแปรสายการเรียน/แผนการเรียนหรือวุฒิเดิม

ประกาศรับสมัครที่ระบุว่า “รับเฉพาะวิทย์-คณิต” หรือ “รับวิทย์-คณิต/ศิลป์คำนวณ/ศิลป์ภาษา” ใช้ตอบได้เพียงว่า **คณะ/สาขานั้นเปิดรับสายใด** ไม่ใช่สัดส่วนสายการเรียนของผู้เข้าเรียนจริง

## 3. Business Questions

1. ในแต่ละปี KKU มีจำนวนรับระดับปริญญาตรีเท่าไร?
2. คณะ/สาขาใดมีจำนวนรับสูงที่สุด?
3. จำนวนรับของแต่ละคณะเปลี่ยนแปลงอย่างไรในแต่ละปี?
4. รอบ Portfolio / Quota / Admission / Direct มีจำนวนรับแตกต่างกันอย่างไร?
5. คณะใดเปิดรับนักเรียน ม.6 มากที่สุด?
6. คณะ/สาขาใดจำกัดแผนการเรียน เช่น วิทย์-คณิต?
7. สาขาใดเปิดรับหลายแผนการเรียน เช่น วิทย์-คณิต + ศิลป์คำนวณ + ศิลป์ภาษา?
8. จำนวนนักเรียน ม.ปลายในจังหวัดขอนแก่นมีแนวโน้มเพิ่มหรือลด?
9. สัดส่วน ม.4–ม.6 ต่อ ปวช. ในพื้นที่ที่มีข้อมูลเป็นอย่างไร?
10. จังหวัดขอนแก่นมีนักเรียน ม.ปลายและนักเรียนเทียบเท่าจำนวนเท่าไรในแต่ละปี?
11. คณะใดมีจำนวนรับสูงที่สุดในปีที่เลือก?
12. สาขาใดมีเกณฑ์รับที่เปิดกว้างที่สุดด้านแผนการเรียน?
13. มีข้อมูลจริงเพียงพอหรือไม่ที่จะสรุป “สายการเรียน → คณะ”?
14. หากมีข้อมูลสายการเรียนของนักศึกษา คณะใดมีสัดส่วนสายวิทย์-คณิตสูงที่สุด?
15. หากมีข้อมูลรายบุคคลแบบไม่เปิดเผยตัวตน สายการเรียนกับคณะที่เลือกมีความสัมพันธ์กันหรือไม่?

## 4. Data Sources

| Dataset | Description | Source Organization | Year | File Format | Download URL | License | Important Variables | Join Key | Usage |
|---|---|---|---|---|---|---|---|---|---|
| จำนวนนักเรียนระดับมัธยมศึกษาตอนปลาย จ.ขอนแก่น | จำนวนนักเรียน ม.ปลายของจังหวัดขอนแก่น | สำนักงานจังหวัดขอนแก่น / สำนักงานศึกษาธิการจังหวัดขอนแก่น | ข้อมูลรายปี; metadata ปรับปรุง 25 มิ.ย. 2568 | CSV, XLS/XLSX | https://data.go.th/th/dataset/dataset_20_446 | Open Data Common; เข้าถึงสาธารณะ ไม่มีเงื่อนไข | ปี, จังหวัด, จำนวน/หน่วย | ปีการศึกษา/ปี พ.ศ., จังหวัด | **Core** สำหรับแนวโน้ม supply นักเรียน ม.ปลายในขอนแก่น |
| จำนวนนักเรียนระดับมัธยมศึกษาตอนปลายหรือเทียบเท่า จ.ขอนแก่น | ม.ปลายสามัญ + อาชีวศึกษา | สำนักงานจังหวัดขอนแก่น / สำนักงานศึกษาธิการจังหวัดขอนแก่น | รายปี; metadata ปรับปรุง 25 มิ.ย. 2568 | CSV, XLS/XLSX | https://data.go.th/th/dataset/dataset_20_472 | Open Data Common; เข้าถึงสาธารณะ ไม่มีเงื่อนไข | ปี, จังหวัด, จำนวน ม.ปลาย/เทียบเท่า | ปี, จังหวัด | **Core** สำหรับภาพรวม ม.ปลาย + เทียบเท่า |
| จำนวนนักเรียนระดับ ปวช. จ.ขอนแก่น | จำนวนนักเรียน ปวช.1–3 | สำนักงานจังหวัดขอนแก่น / สำนักงานศึกษาธิการจังหวัดขอนแก่น | รายปี; metadata ปรับปรุง 25 มิ.ย. 2568 | CSV, XLS/XLSX | https://data.go.th/th/dataset/dataset_20_455 | Public; metadata ระบุระดับการเข้าถึงสาธารณะ | ปี, จังหวัด, จำนวน ปวช. | ปี, จังหวัด | Supporting สำหรับแยก “สามัญ vs อาชีวะ” |
| จำนวนห้องเรียนและนักเรียนระดับ ม.ต้น/ม.ปลายในระบบโรงเรียนประเทศไทย | จำนวนห้องเรียนและนักเรียนจำแนกสังกัด/ชั้น | สำนักงานปลัดกระทรวงศึกษาธิการ | 2564 ใน resource ที่ตรวจพบ | CSV, XLS/XLSX, PDF | https://data.go.th/th/dataset/gdpublish-dataset-15_17 | Open Data Common; สาธารณะ ไม่มีเงื่อนไข | ระดับชั้น, สังกัด, นักเรียน, ห้องเรียน | ปี/ระดับ/สังกัด | **Supporting** สำหรับ benchmark ระดับประเทศ |
| ข้อมูลนักเรียนในประเทศไทย | ข้อมูลนักเรียนระดับประถม/มัธยมในและนอกสังกัดกระทรวงศึกษาธิการ | ศูนย์เทคโนโลยีสารสนเทศและการสื่อสาร สป. กระทรวงศึกษาธิการ | หน้า catalog ปัจจุบัน | HTML / Micro Data API | https://www.catalog.moe.go.th/dataset/dataset-15_44 | ต้องตรวจเงื่อนไขของ API | ระดับการศึกษา/หน่วยงาน ฯลฯ | ปี/พื้นที่/ระดับ | **Supporting**; Micro Data API ต้องมี MOU/สิทธิ์ จึงไม่ควรใช้เป็น core ถ้าเข้าถึงไม่ได้ |
| จำนวนรับบุคคลเข้าศึกษา KKU รอบ 1 Portfolio | จำนวนรับแยกหลักสูตร/โครงการ และคุณสมบัติ/วุฒิ/แผนการเรียน | สำนักบริหารและพัฒนาวิชาการ/ระบบรับเข้าศึกษา KKU | 2569 | PDF | https://admissions.kku.ac.th/wp-content/uploads/2025/09/ed-port69.pdf | เอกสารเผยแพร่สาธารณะของ KKU; ตรวจเงื่อนไขการ reuse ก่อนเผยแพร่เชิงพาณิชย์ | คณะ, สาขา, โครงการ, วุฒิ, จำนวนรับ, แผนการเรียน, เกณฑ์ | ปีการศึกษา + รหัส/ชื่อสาขา + รอบ | **Core admission**; ใช้สร้าง faculty/major + seat + eligibility |
| จำนวนรับ KKU รอบ 1 Portfolio โครงการส่วนกลาง | จำนวนรับและคุณสมบัติบางโครงการ | KKU Admissions | 2569 | PDF | https://admissions.kku.ac.th/wp-content/uploads/2025/10/ph-port69.pdf | Public KKU document | คณะ/สาขา, จำนวนรับ, วุฒิ, แผนการเรียน, เกณฑ์ | ปี + สาขา + รอบ | Supporting / ตรวจสอบเงื่อนไข |
| KKU Admissions — หน้าคณะสาขา/โครงการ | หน้าระบบรับสมัครที่แสดงสาขาและจำนวนรับในโครงการ | KKU Admissions | 2568–2569 ตามหน้า | HTML | https://apps.admissions.kku.ac.th/web/Port/PortDetail/4731/18 | Public website | ชื่อหลักสูตร, จำนวนรับ, รอบ, เอกสารประกอบ | ปี + รอบ + หลักสูตร | ใช้ cross-check กับ PDF |
| รายงานวิจัย KKU: ปัจจัยการเลือกเข้าศึกษา รอบ 2 โควตาภาคตะวันออกเฉียงเหนือ | งานวิจัยเกี่ยวกับปัจจัย/แนวทางประชาสัมพันธ์ที่ส่งผลต่อการตัดสินใจเลือกเข้า KKU | สำนักบริหารและพัฒนาวิชาการ KKU | 2565 | Web page / research report | https://registrar.kku.ac.th/policy/?page_id=1280 | Public KKU research page | ปัจจัยการเลือก, ผู้สมัคร/การตัดสินใจ | ปี/รอบ | **Contextual / research**; ใช้ทำ interpretation ไม่ใช่ fact table ถ้าไม่พบ structured data |
| รายงานวิจัย: ปัจจัยแรกเข้าศึกษาและผลสัมฤทธิ์ นักศึกษาปริญญาตรี | งานวิจัยที่ KKU ระบุว่าศึกษาปัจจัยแรกเข้าและผลสัมฤทธิ์ ปี 2556–2565 | สำนักบริหารและพัฒนาวิชาการ KKU | 2556–2565 | Research listing / report availability ต้องตรวจไฟล์ | https://registrar.kku.ac.th/rs-baad | Public KKU research listing | ปัจจัยแรกเข้า, ผลสัมฤทธิ์ | ปีการศึกษา | **High-value lead**; ตรวจว่ารายงานมีตัวแปรแผนการเรียนหรือไม่ก่อนนำเข้า |
| ประกาศ KKU ที่มี “แผนการเรียน → จำนวนรับ” | ตัวอย่างตารางแผนการเรียนและจำนวนรับรายสาขา | KKU Registrar | 2564 | PDF | https://registrar.kku.ac.th/apply2/files/1421_1.pdf | Public KKU announcement | รหัสสาขา, แผนการเรียน, จำนวนรับ | ปี + รหัสสาขา | **Important proxy only**; ไม่ใช่ actual entrant background |

### Direct-download status

For the `data.go.th` resources above, the catalog exposes CSV/XLSX resources through its **Download** control, but the crawler did not expose the final binary URL. Do **not** invent a direct file URL. The dashboard agent should open the dataset page and use the current Download resource URL/API exposed by data.go.th.

For KKU PDFs, the URLs above are direct PDF URLs and can be downloaded programmatically.

## 5. Data Dictionary

### A. Khon Kaen upper-secondary dataset

Expected/verified metadata:
- `year` / ปี — Buddhist academic/calendar year
- `province` / จังหวัด — ขอนแก่น
- `student_count` / ค่าข้อมูล — number of students
- `unit` / หน่วย — คน/ราย as specified by resource

Use:
- Trend by year
- Upper-secondary supply
- Benchmark against KKU admission seats

### B. Khon Kaen upper-secondary-or-equivalent dataset

Concept:
- Upper-secondary general education
- Vocational education equivalent

Use:
- Compare general vs equivalent population
- Avoid treating “equivalent” as identical to M.6.

### C. KKU admission PDF

Important fields to extract from PDF tables:
- academic_year
- round
- faculty
- major/program
- project
- qualification_type
- eligible_education_type: ม.6 / international / vocational / กศน. / GED / child-siw
- seats_normal
- seats_special
- study_plan_eligibility
- selection_criteria
- tuition

**Important:** `study_plan_eligibility` is eligibility/requirement, not observed student background.

### D. Actual entrant-background dataset — target schema

If KKU or another authorized public source is found later, target:
- `academic_year`
- `application_round`
- `faculty_code`
- `faculty_name`
- `program_code`
- `program_name`
- `study_plan`
- `qualification_type`
- `province`
- `school_type`
- `school_province`
- `applicant_count`
- `selected_count`
- `confirmed_count`
- `enrolled_count`

If such data are only available internally or require restricted access, mark as **Unavailable for Open Data Dashboard**.

## 6. Data Cleaning

1. Convert Thai/Buddhist years consistently; retain `academic_year_be` and optionally `academic_year_ad`.
2. Standardize faculty names across years.
3. Standardize major/program names; keep original text in `*_raw`.
4. Normalize whitespace, line breaks and PDF-extraction artifacts.
5. Convert Thai numerals to Arabic numerals where necessary.
6. Convert numeric columns to numeric dtype.
7. Remove duplicated PDF rows caused by multi-page table extraction.
8. Do not infer missing values.
9. Treat “ไม่ระบุ”, blank, `-` as missing only when context confirms they mean unavailable.
10. Keep admission round as a categorical variable: Portfolio, Quota, Admission, Direct.
11. Keep `study_plan_eligibility` separate from `actual_study_plan`.
12. Validate totals against the source PDF/table where possible.
13. For province data, normalize province spelling to a controlled list.
14. Preserve source URL and source document name for every transformed dataset.
15. Do not ingest names, citizen IDs, addresses, phone numbers, or other personal identifiers.

## 7. Data Integration

### Integration that is valid now

```text
Khon Kaen upper-secondary students
        |
        | year
        v
Khon Kaen upper-secondary-or-equivalent
        |
        | year
        v
KKU admission seats / programs
        |
        | academic_year + faculty/program + round
        v
KKU Faculty / Major admission model
```

This supports:
- supply vs admission capacity
- trend
- faculty/program offering
- eligibility analysis

### Integration that is NOT currently valid

```text
Study plan of actual student
        X
Faculty actually entered
```

Reason: no verified public structured dataset was found containing both variables for actual KKU entrants.

### If actual entrant-background data becomes available

Preferred keys:

```text
academic_year
faculty_code
program_code
round_code
```

Optional geographic join:

```text
academic_year + province
```

Do not join using faculty names alone when codes exist.

## 8. Analysis Plan

### Descriptive

- Count
- Percentage
- Ranking
- Year-over-year change
- Seat share by faculty
- Seat share by round
- Eligibility share by study plan

### Admission competition

Only calculate:

`competition_ratio = applicants / seats`

when **actual applicant counts and seat counts refer to the same year, round, faculty/program and admission process**.

Do not calculate competition from a seat-only PDF.

### Cross-tabulation

If actual study-plan × faculty data become available:

```text
Rows = study_plan
Columns = faculty
Values = enrolled_count
```

Then calculate row percentages and column percentages.

### Chi-square test

Use only if:
- observations are actual student-level or valid aggregated counts,
- categories are mutually exclusive,
- expected frequencies are adequate,
- the sampling/observation design supports the test.

Do not use KKU “eligible study plans” as observed counts.

## 9. Dashboard Structure

### Page 1 — Overview

KPI cards:
- Applicants — only if actual data found
- Selected — only if actual data found
- Confirmed — only if actual data found
- Enrolled — only if actual data found
- Admission seats
- Top faculty by available actual metric

Visuals:
- KPI cards
- Year trend
- Top faculties

Add a visible data-status badge:
- `Actual`
- `Admission capacity`
- `Not available`

### Page 2 — Faculty & Major

Visuals:
- Bar chart: seats by faculty
- Top 10 majors by seats
- Treemap: faculty → major
- Filter: academic year / round / faculty

If applicant counts become available:
- applicant vs seats
- competition ratio

### Page 3 — Study Background

Preferred:
- Donut: actual study-plan distribution
- Heatmap: study_plan × faculty
- Row/column percentages
- Chi-square result

Current fallback:
- Show **“Study-plan eligibility by faculty”**
- Do not label it as student background.
- Example metric: number/share of programs that accept Science-Math, Arts-Math, Arts-Language.

### Page 4 — Trend

Visuals:
- Line: upper-secondary students in Khon Kaen
- Line: KKU admission seats
- Line: applicants/selected/enrolled if actual historical data become available
- Faculty trend ranking

### Page 5 — Geographic Analysis

Only build if actual student/applicant province data are available:
- Choropleth map
- Province ranking
- Region ranking

Current public-source fallback:
- Khon Kaen as source population context only.
- Do not claim that all KKU entrants come from Khon Kaen.

## 10. Expected Insights

Do **not** hard-code expected results.

The analysis should discover:
- Which faculty/program has the largest admission capacity
- Whether KKU admission capacity is changing over time
- Which study plans are most commonly accepted by programs
- Whether admission structures differ strongly by round
- Whether actual study-plan background is available
- Whether geographic origin data can support a KKU catchment analysis

Potential final insight format:

> “Among the years and admission rounds covered by the verified data, [faculty/program] had the highest [actual metric].”

Only populate `[faculty/program]` after calculation.

## 11. Technical Requirements

Recommended stack:

- Python 3.11+
- Pandas
- NumPy
- PyPDF / pdfplumber or Camelot/Tabula for PDF tables
- Plotly
- Streamlit
- DuckDB optional for local analytical warehouse
- GeoPandas optional for geographic analysis

Recommended project structure:

```text
kku-admission-dashboard/
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
├── notebooks/
├── src/
│   ├── ingest.py
│   ├── clean.py
│   ├── transform.py
│   └── analysis.py
├── app.py
├── requirements.txt
├── README.md
└── kku_admission_dashboard_handoff.md
```

Recommended data model:

```text
dim_year
dim_faculty
dim_program
dim_round
dim_study_plan
dim_province

fact_admission_capacity
fact_application        # only if actual data found
fact_selection          # only if actual data found
fact_enrollment         # only if actual data found
fact_student_background # only if actual study-plan data found
```

## 12. Data Limitations

### Limitation 1 — Actual study-plan background

This is the most important limitation.

Public KKU admission announcements often specify which study plans are **eligible**, but this does not reveal the study plan of the students who eventually enrolled.

Therefore:

> “รับเฉพาะวิทย์-คณิต” ≠ “นักศึกษาส่วนใหญ่เป็นวิทย์-คณิต”

### Limitation 2 — Applicant/selected/enrolled counts

The public pages and PDFs found during this research expose admission schedules, seats, eligibility and selection procedures, but a single complete, machine-readable historical applicant → selected → confirmed → enrolled dataset was not verified.

Do not manufacture these numbers.

### Limitation 3 — Faculty/program changes

Faculty and program structures can change over time. Historical names/codes should be retained rather than blindly mapping everything to the newest structure.

### Limitation 4 — Geographic analysis

Khon Kaen high-school counts are **source-population context**, not a count of KKU applicants or entrants.

### Limitation 5 — Personal data

Student-level names, IDs, addresses and other personal information must not be collected for this dashboard.

## 13. Source Verification

### Primary sources

- KKU Admissions: https://admissions.kku.ac.th/
- KKU Admissions application system: https://apps.admissions.kku.ac.th/
- KKU Registrar / Academic Administration: https://registrar.kku.ac.th/
- KKU Registrar research page: https://registrar.kku.ac.th/rs-baad
- data.go.th: https://data.go.th/
- Ministry of Education catalog: https://www.catalog.moe.go.th/
- Khon Kaen provincial datasets on data.go.th

### Verified source references

1. Khon Kaen upper-secondary students:
   https://data.go.th/th/dataset/dataset_20_446

2. Khon Kaen upper-secondary or equivalent:
   https://data.go.th/th/dataset/dataset_20_472

3. Khon Kaen vocational students:
   https://data.go.th/th/dataset/dataset_20_455

4. National lower/upper-secondary students and classrooms:
   https://data.go.th/th/dataset/gdpublish-dataset-15_17

5. KKU 2569 admission seats / Portfolio:
   https://admissions.kku.ac.th/wp-content/uploads/2025/09/ed-port69.pdf

6. KKU 2569 central Portfolio admission table:
   https://admissions.kku.ac.th/wp-content/uploads/2025/10/ph-port69.pdf

7. KKU research report — factors affecting decision to study, TCAS Round 2, 2565:
   https://registrar.kku.ac.th/policy/?page_id=1280

8. KKU research listing:
   https://registrar.kku.ac.th/rs-baad

9. Historical KKU admission announcement with study-plan eligibility and seats:
   https://registrar.kku.ac.th/apply2/files/1421_1.pdf

## 14. Next Steps

### Phase 1 — Data Download

1. Download the Khon Kaen upper-secondary CSV/XLSX.
2. Download upper-secondary-or-equivalent CSV/XLSX.
3. Download vocational CSV/XLSX if the dashboard compares general/vocational pathways.
4. Download KKU admission PDFs for all target years.
5. Download/inspect the KKU research report on first-entry factors.
6. Search the KKU Registrar/Admissions site for historical applicant/selected/enrolled statistics.

### Phase 2 — Extraction

1. Extract PDF tables.
2. Create `admission_capacity.csv`.
3. Extract:
   - year
   - round
   - faculty
   - program
   - seats
   - education type
   - study-plan eligibility
4. Preserve raw PDF text/table outputs.

### Phase 3 — Cleaning

1. Normalize Thai names.
2. Normalize year.
3. Normalize round.
4. Normalize faculty/program.
5. Validate totals against source PDFs.

### Phase 4 — EDA

Create:
- upper-secondary trend
- KKU seats trend
- faculty ranking
- major ranking
- study-plan eligibility matrix

### Phase 5 — Actual background-data investigation

Before building the “Study Background” page, verify whether KKU can publicly provide:
- study plan
- qualification
- faculty/program
- academic year
- enrolled/confirmed status

If unavailable, keep the page as “Eligibility Analysis” rather than “Actual Student Background”.

### Phase 6 — Dashboard

Build Streamlit pages:

```text
Overview
Faculty & Major
Study Background / Eligibility
Trend
Geographic Analysis
Data Sources
```

### Phase 7 — Deployment

Recommended:
- GitHub
- Streamlit Community Cloud

Add:
- source links
- data dictionary
- last-updated date
- data-status labels
- methodology notes

## Final Data-Availability Matrix

| Required Question | Verified public data? | Status |
|---|---:|---|
| จำนวน ม.4–ม.6 ในขอนแก่น | Yes | **Available** |
| Trend นักเรียน ม.ปลายในขอนแก่น | Yes | **Available** |
| ม.ปลาย + เทียบเท่าในขอนแก่น | Yes | **Available** |
| ปวช. ในขอนแก่น | Yes | **Available** |
| จำนวนรับ KKU แยกหลักสูตร/สาขา | Yes, via admission documents | **Available** |
| แผนการเรียนที่สาขารับ | Yes, for many admission documents | **Available as eligibility** |
| รายชื่อคณะ/สาขาที่เปิดรับ | Yes, via KKU Admissions | **Available** |
| จำนวนผู้สมัคร KKU แยกคณะ/สาขา/ปี | Not verified as complete structured Open Data | **Not sufficiently verified** |
| จำนวนผู้ผ่านคัดเลือกแยกคณะ/สาขา/ปี | Not verified as complete structured Open Data | **Not sufficiently verified** |
| จำนวนยืนยันสิทธิ์แยกคณะ/สาขา/ปี | Not verified as complete structured Open Data | **Not sufficiently verified** |
| จำนวนเข้าศึกษาจริงแยกคณะ/สาขา/ปี | Not verified as complete structured Open Data | **Not sufficiently verified** |
| สายการเรียนจริงของนักศึกษา KKU | Not found as verified structured Open Data | **Not found** |
| สายการเรียนจริง × คณะที่เข้า | Not found | **Not found** |
| จังหวัดโรงเรียนเดิมของนักศึกษา KKU | Not found as verified public aggregate dataset | **Not found** |
| โรงเรียนเดิม × คณะที่เข้า | Not found | **Not found** |
| Chi-square: study plan × faculty | Only if actual cross-tab data are obtained | **Conditional** |

## Important Implementation Rule

**Never substitute admission eligibility for actual student background.**

The dashboard should explicitly distinguish:

- `actual_student_background`
- `admission_eligibility`
- `admission_capacity`
- `applicant_count`
- `selected_count`
- `confirmed_count`
- `enrolled_count`

If a field is unavailable, show `N/A / Not publicly available` rather than estimating it.
