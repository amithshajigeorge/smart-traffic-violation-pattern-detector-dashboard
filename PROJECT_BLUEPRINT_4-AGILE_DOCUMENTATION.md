# 📘 PROJECT_BLUEPRINT_3.md: Agile Project Documentation

**Project Name:** Smart Traffic Violation Pattern Detector Dashboard  
**Platform Name:** Collision X  
**Role:** Agile Project Manager & Technical Team Lead  
**Team Size:** 13 Developers (Interns)  
**Duration:** 2 Months (4 Sprints of 2 Weeks each)  
**Tools:** Python, Streamlit, Pandas, Matplotlib, Folium  

---

## 1. 📋 Product Backlog

This backlog represents the complete scope of work prioritized for the 2-month internship.

| Planned Sprint | Actual Sprint | US ID | User Story Description | MOSCOW | Dependency | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Sprint 1 | Sprint 1 | US-01 | As a lead, I want to **initialize the project structure** and repo so the team can collaborate. | Must Have | None | Sami (Lead) | Done |
| Sprint 1 | Sprint 1 | US-02 | As a user, I want a **Data Upload Page** to load traffic CSVs. | Must Have | US-01 | Divija | Done |
| Sprint 1 | Sprint 1 | US-03 | As a system, I need **robust git conflict handling** to merge 13 members' code. | Must Have | None | Anshu | Done |
| Sprint 2 | Sprint 2 | US-04 | As a user, I want distinct **Visualization Pages** for different insights. | Must Have | US-02 | Ishwari | Done |
| Sprint 2 | Sprint 2 | US-05 | As a user, I want **Visual Plots** (Bar/Pie) for traffic trends. | Must Have | US-04 | Harika | Done |
| Sprint 3 | Sprint 3 | US-06 | As a brand, I want a custom **Logo and Platform Identity (Collision X)**. | Should Have | None | Mrunalini | Done |
| Sprint 3 | Sprint 3 | US-07 | As a user, I want a **Map Visualization** using specific GeoJSONs for accurate regions. | Must Have | US-02 | Amith | Done |
| Sprint 4 | Sprint 4 | US-08 | As a user, I want **AI-assisted analysis** (Claude/Gemini) insights generated for complex data. | Should Have | US-05 | Sami | In Progress |

---

## 2. 🏃 Sprint Backlog (Sprint 1: Foundation & Data)

**Sprint Goal:** Establish "Collision X" platform base, handle data uploads, and sort out huge git merge conflicts.

| US ID | Task ID | Task Description | Team Member | Status | Est. Effort (Hrs) | Day 1-7 | Day 8-14 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| US-01 | T-101 | Initialize Repo & Core Architecture (app.py) | Sami | Done | 10 | 10 | 0 |
| US-03 | T-102 | Resolve Merge Conflicts (13 branches) | Anshu | Done | 15 | 8 | 7 |
| US-02 | T-103 | Build `09_Upload_Dataset.py` Page | Divija | Done | 8 | 5 | 3 |
| US-04 | T-104 | Develop `01_Numerical_Analysis.py` Page | Mrunalini | Done | 8 | 4 | 4 |
| US-04 | T-105 | Develop `11_About_Page.py` structure | Harika | Done | 6 | 0 | 6 |
| US-07 | T-106 | Research & Find Open Source GeoJSON Maps | Amith | Done | 12 | 2 | 10 |
| US-05 | T-107 | Implement Basic Visual Plots (Matplotlib) | Sanjana | Done | 8 | 0 | 8 |

---

## 3. 🗣️ Stand-up Meeting Log

Daily syncing, focusing on "Collision X" platform blockers.

| Sprint | Day | Date | Impediments / Blockers | Action Taken |
| :--- | :--- | :--- | :--- | :--- |
| **Sp 1** | Day 3 | Nov 03 | **Blocker:** Anshu reported massive merge conflicts due to 13 people pushing to `main`. | **Action:** Sami enforced "Pull Rebase" policy; Anshu took ownership of all complex merges. |
| **Sp 2** | Day 5 | Nov 15 | **Issue:** Ishwari & Harika flagged HTML rendering issues in Streamlit tables. | **Action:** **Mrunalini & Ishwari** wrote custom CSS variables to fix the layout colors and spacing. |
| **Sp 3** | Day 2 | Dec 02 | **Blocker:** Map plotting failing. Standard maps don't match our data regions. | **Action:** Amith spent 2 days finding the correct Open Source **GeoJSON** files from the internet. |
| **Sp 3** | Day 4 | Dec 04 | **Task:** Need a unique identity. | **Action:** Mrunalini designed the **"Collision X"** logo and theme assets. |

---

## 4. 🔄 Retrospection

Reflecting on the "Collision X" team performance.

| SL # | Sprint # | Team Member | Start Doing | Stop Doing | Continue Doing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Sprint 1 | Anshu | Review large PRs in pairs. | Trying to merge everything on Friday evening. | effectively communicating conflict resolutions. |
| 2 | Sprint 2 | Sami | Leveraging **Gemini/Claude** for tricky Pandas debugging. | Writing custom CSS without checking Streamlit support. | guiding the team on architecture. |
| 3 | Sprint 2 | Mrunalini | Creating assets (Logo) earlier in the sprint. | Using hardcoded paths. | improving UI aesthetics. |
| 4 | Sprint 3 | Amith | Validating GeoJSON files before implementation. | Ignoring projection errors. | searching for open-source resources. |
| 5 | Sprint 3 | All | Using standard Variable names (Data Variables). | Hardcoding column names in pages. | collaborating on plotting logic. |

---

## 5. 🐛 Defect Tracker

| Sl No | Description | Detected Sprint | Assigned To | Type | Action Taken | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| BUG-01 | **Map Visibility:** Map not loading for certain States. | Sprint 3 | Amith | Data | Swapped broken GeoJSON with valid Open Source files found online. | Closed |
| BUG-02 | **Merge Conflict:** `app.py` overwritten by accident. | Sprint 1 | Anshu | Process | Reverted commit; established strict merge order. | Closed |
| BUG-03 | **Visuals:** Bar charts overlapping on mobile. | Sprint 2 | Sanjana | UI | Adjusted figure size and rotation using Matplotlib params. | Closed |
| BUG-04 | **Analysis:** Complex filters causing slow load. | Sprint 4 | Darsana | Perf | Optimization assistance from AI tools (Claude). | Closed |

---

## 6. 🧪 Unit Test Plan

| Sl No | Test Case Name | Test Procedure | Condition to be Tested | Expected Result | Actual Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-01 | **GeoJSON Validity** | Load map with new GeoJSON file. | `map_plot.py` check. | Map renders without polygon errors. | Matches Expected |
| TC-02 | **Logo Rendering** | Check Sidebar logo display. | `sidebar.py` render. | "Collision X" logo appears correctly. | Matches Expected |
| TC-03 | **Git Merge** | Merge Feature Branch to Main. | Conflict resolution. | No code loss; history preserved. | Matches Expected |
| TC-04 | **Variable Consistency** | Check column names across pages. | `data_variables.py` usage. | All pages use unified constants. | Matches Expected |

---

## 7. 👥 Authors / Team Collision X

The dedicated team behind the **Smart Traffic Violation Pattern Detector Dashboard**.

| Team Member | Role / Key Contribution |
| :--- | :--- |
| **Saidul Ali Mallick (Sami)** | **Team Lead & Lead Developer**. Initialized project, handled overall architecture, AI integrations, and core logic. |
| **Anshu Gupta** | **Git Specialist**. Managed merge conflicts, repository health, and version control for 13 members. |
| **Mrunalini M** | **UI/UX & Branding**. Created "Collision X" platform identity, Logo, and core UI pages. |
| **Ishwari Deshmukh** | **Frontend Developer**. Built visualization pages and handled Streamlit layout components. |
| **Harika Sayani** | **Frontend Developer**. Contributed to page structure, HTML representation, and About page. |
| **Divija V** | **Frontend Developer**. Implemented Data Upload and file handling logic. |
| **Amith Shaji George** | **Map Specialist**. Solved complex GeoJSON visualization issues using open-source resources. |
| **Sanjana Gowrishetty** | **Data Analyst**. Contributed to visual representation and plotting logic. |
| **Darsana R** | **Developer**. Contributed to plotting modules and dashboard integration. |
| **Poojitha Borra** | **Developer**. Assisted with page routing and debugging. |
| **Saniya Mahek** | **Developer**. Worked on data validation and filters. |
| **Vijay G** | **Developer**. Contributed to backend utility functions. |
| **Rakshitha P** | **Developer**. Assisted with testing and documentation. |

> **Acknowledgment:** We leveraged AI tools (Claude & Gemini) primarily for **complex debugging** where Sami & Anshu led the analysis to resolve deep technical issues.
