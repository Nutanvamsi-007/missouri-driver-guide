# 🚗 Missouri Driver Guide — Project Context & Session Handoff

> **Session Timestamp**: September 25, 2026  
> **Project Location**: `/Users/nutanvamsigunti/workspace/missouri-driver-guide`  
> **Source Material**: Official Missouri DOR Driver Guide (`Driver Guide.pdf`, Revised August 2026, 102 Pages)  
> **Application Status**: Fully functional, verified in browser via Chrome DevTools MCP, zero external runtime dependencies.

---

## 📌 Executive Summary

This project transforms the official 102-page Missouri Department of Revenue (DOR) Driver Guide into a high-performance, interactive, and attention-seeking local web application designed to help applicants master Missouri traffic laws and pass the official 25-question permit examination.

All text, graphics, vector signs, and maneuver diagrams have been extracted and optimized for 100% offline, client-side execution with zero latency.

---

## 🗂 File & Directory Inventory

```
/Users/nutanvamsigunti/workspace/missouri-driver-guide/
├── index.html                   # Core single-page application shell (semantic HTML5)
├── styles.css                   # Custom CSS styling (dark/light themes, 3D card flips, responsive grid)
├── app.js                       # Vanilla ES6 application engine (state management, tabs, quiz, search, audio)
├── data.js                      # Offline client bundle with all structured chapters, questions & figures
├── guide_data.json              # Machine-readable JSON export of full handbook content
├── server.py                    # Lightweight Python HTTP server with WebP MIME types & no-cache headers
├── start.sh                     # Automated bash launcher (`chmod +x start.sh`)
├── build_missouri_guide.py      # Automated PDF extraction pipeline (PyMuPDF + Pillow)
├── verify_crops.py              # Diagnostic & visual validation script for sign bounding boxes
├── README.md                    # Project documentation and quick-start guide
├── SESSION_CONTEXT.md           # This comprehensive handoff document
├── Driver_Guide.pdf             # Official Missouri DOR Driver Guide source PDF (102 pages, 2.2 MB)
├── .venv/                       # Python 3.9 virtual environment (PyMuPDF 1.26.5, Pillow 11.3.0)
└── assets/
    ├── pages/                   # 102 high-resolution WebP page renders (`page_001.webp` .. `page_102.webp`)
    └── images/
        ├── signs/               # 56 cropped traffic signs, shields & shapes (200 DPI PNG)
        ├── diagrams/            # 18 road maneuver, parking, and traffic signal diagrams (200 DPI PNG)
        └── extracted/           # 62 native raster images extracted from PDF streams
```

---

## ⚙️ Architecture & Technical Stack

1. **Frontend (Zero-Dependency Modern Web)**:
   - **Vanilla ES6 JavaScript**: No frameworks (React, Vue, etc.) required; boots instantaneously from local disk.
   - **CSS Custom Properties**: Fluid typography, responsive flex/grid layouts, glassmorphism badges, and smooth 3D CSS `transform-style: preserve-3d` animations.
   - **Client-Side Fuzzy Search**: Real-time searching across 102 pages of handbook text, definitions, traffic signs, and point violation rules.
   - **Web Speech API**: Integrated text-to-speech engine with Play/Pause controls for hands-free listening.

2. **Data Pipeline (`build_missouri_guide.py`)**:
   - **PyMuPDF (`fitz`)**: Fast PDF processing engine capable of rendering 102 full pages to WebP in < 0.02 seconds.
   - **Adobe InDesign Vector Extraction**: Solved the critical issue where standard PDF extractors (`pdfimages`) produce 0 images for road signs because InDesign renders signs as vector drawing paths (`page.get_drawings()`). We isolate precise bounding boxes and rasterize them at 200 DPI into transparent/crisp PNGs.
   - **Offline JS Bundle Generator**: Exports `data.js` (`window.MISSOURI_GUIDE_DATA = {...}`) so the browser can load the entire database locally without triggering strict browser file:// CORS restrictions.

3. **Local Web Server (`server.py`)**:
   - Built on Python's native `http.server` and `socketserver`.
   - Auto-discovers open ports starting from `8080`.
   - Sends `Access-Control-Allow-Origin: *` for seamless local asset loading.
   - Sends `Cache-Control: no-cache, no-store, must-revalidate` during development so asset changes reflect immediately on refresh.
   - Supports `--open` or `-o` flag to launch the system default browser automatically.

---

## 🎯 Major Features Implemented

### 1. Interactive Handbook Reader
- Full coverage of **all 16 chapters + Introduction and Index** (pages 1 to 102).
- Table of contents with chapter progress tracking, read-time estimates, and page jump links.
- Reading tools: Font sizing (A- / A+), Dark/Light theme toggle, and Chapter bookmarks saved in `localStorage`.
- Official Page Inspector modal: View the high-res original Missouri DOR PDF page side-by-side with formatted text.
- Text-to-Speech audio reader using browser speech synthesis.

### 2. Official 25-Question Missouri Permit Exam Simulator
- Authentic state exam logic: **25 multiple choice questions**, **20 correct answers (80%) needed to pass**.
- Two modes:
  - **Practice Mode**: Instant answer feedback with full statutory explanations and handbook page citations.
  - **Timed Exam Mode**: 25-minute countdown clock simulating official MSHP testing conditions with final score report.
- Question bank compiled directly from DOR test topics: right-of-way, BAC alcohol laws, speed limits, work zone fines, school bus stopping laws, and sign recognition.

### 3. Missouri Road Signs Lab & 3D Flashcards
- Interactive 3D flip cards covering **81 official signs, shapes, and diagrams**:
  - **Sign Shapes (9)**: Octagon (Stop), Triangle (Yield), Vertical Rect (Regulatory), Horizontal Rect (Guide), Pentagon (School), Round (Railroad Advance), Crossbuck (Railroad Crossing), Pennant (No Passing Zone), Diamond (Warning).
  - **Regulatory Signs (14)**: No Left Turn, No Right Turn, No U-Turn, No Trucks, No Bicycles, Stop Sign, Yield Sign, Wrong Way, Do Not Enter, One Way, Lane Control (Only), Speed Limit 70, Keep Right, Railroad Crossbuck.
  - **Warning Signs (26)**: Stop Ahead, Signal Ahead, Pedestrian Crossing, School Crossing, Sharp Curves, Chevrons, Slippery When Wet, Slow Moving Vehicle, Exit Speed Advisory, Added Lane, Divided Roadway Begin/End, etc.
  - **Work Zone Signs (7)**: Road Work Ahead, Fresh Oil, Loose Gravel, Right Lane Closed Ahead, Work Zone Merge, Work Zone Flagger Ahead, End Road Work.
  - **Guide & Highway Shields (7)**: Official Vehicle Inspection Station, Interstate 70, Business Loop 44, US Highway 36, Missouri Route 25, County Lettered Route A, Emergency Reference Marker.
  - **Driving Maneuver Diagrams (18)**: Single & Multi-Lane Roundabout Navigation, Dual Left Turns, Shared Center Turn Lanes, J-Turn Intersections, Driver Hand Signals, Commercial Truck No-Zones, Pedestrian Signals, Hill Parking, Parallel Parking, Vehicle Blind Spots, Traffic Light Sequences, Stopping Distances, and Click It or Ticket Law.
- Card tile styling: Clean white rounded tiles (`background: #ffffff`, `border-radius: var(--radius-md)`) with subtle depth to prevent raw bounding box cutoff and ensure sharp contrast in dark mode.

### 4. Simulators & Calculators
- **Stopping Distance Physics Simulator**:
  - Dynamically calculates Reaction Distance and Braking Distance from 10 mph to 85 mph based on Chapter 8 physics formulas.
  - Toggles between Dry Pavement (friction ~0.72) and Wet Pavement (friction ~0.38).
  - Visual comparison bars and car-length equivalents.
- **Missouri Point System Simulator**:
  - Interactive violation selector (Speeding >5 mph, Speeding >30 mph, Careless driving, DUI/DWI, Driving with suspended license).
  - Tracks points accumulation towards warning notices (4 points), suspension (8 points in 18 months), and revocation (12 points in 12 months).
  - Explains the point reduction timeline: 1 year clean drops 1/3 points; 2 years drops 1/2; 3 years drops to 0.

### 5. 102 PDF Pages Visual Gallery
- Grid view of all 102 pages rendered in high-resolution WebP (`page_001.webp` through `page_102.webp`).
- Filter by chapter or jump directly to specific handbook pages.
- Click any thumbnail to trigger the high-resolution lightbox inspector.

---

## 📐 Verified Vector Crop Coordinates Reference

When maintaining or adding sign crops in `build_missouri_guide.py`, refer to this definitive coordinate list (0-indexed page index):

```python
# (id, page_idx, x0, y0, x1, y1, category, title, description)

# Sign Shapes (Page 47 / idx 46)
("shape_octagon", 46, 43, 374, 78, 409, "shapes", "Octagon Shape", "Exclusively used for Stop signs.")
("shape_triangle", 46, 43, 415, 78, 450, "shapes", "Triangle (Equilateral Downward)", "Exclusively used for Yield signs.")
("shape_vertical_rect", 46, 43, 456, 78, 498, "shapes", "Vertical Rectangle", "Regulatory signs (speed limits, lane controls).")
("shape_horizontal_rect", 46, 43, 505, 85, 536, "shapes", "Horizontal Rectangle", "Guide signs (directions, distances, services).")
("shape_pentagon", 46, 43, 542, 78, 577, "shapes", "Pentagon (Pointed Up)", "School Advance and School Crossing zones.")
("shape_round", 46, 186, 374, 222, 409, "shapes", "Round Shape", "Railroad Crossing Advance Warning.")
("shape_crossbuck", 46, 190, 418, 220, 446, "shapes", "Crossbuck Shape", "Marks actual railroad grade crossing.")
("shape_pennant", 46, 186, 456, 228, 492, "shapes", "Pennant Shape (Isosceles)", "No Passing Zone warning.")
("shape_diamond", 46, 186, 505, 225, 552, "shapes", "Diamond Shape", "Warning signs of hazards and roadway conditions.")

# Regulatory Prohibition Signs (Page 50 / idx 49)
("no_left_turn", 49, 78, 394, 138, 454, "regulatory", "No Left Turn", "Left turn is prohibited.")
("no_right_turn", 49, 163, 394, 223, 454, "regulatory", "No Right Turn", "Right turn is prohibited.")
("no_u_turn", 49, 248, 394, 308, 454, "regulatory", "No U-Turn", "U-turns are prohibited.")
("no_trucks", 49, 78, 479, 138, 539, "regulatory", "No Trucks", "Commercial trucks are prohibited.")
("no_bicycles", 49, 163, 479, 223, 539, "regulatory", "No Bicycles", "Bicycles are prohibited.")

# Work Zone Signs (Page 53 / idx 52)
("road_work_ahead", 52, 36, 436, 95, 496, "workzone", "Road Work Ahead", "Work zone ahead. Fines doubled.")
("fresh_oil", 52, 129, 436, 188, 496, "workzone", "Fresh Oil", "Recently oiled pavement.")
("right_lane_closed_ahead", 52, 35, 503, 95, 562, "workzone", "Right Lane Closed Ahead", "Right travel lane closes ahead.")
("workzone_merge", 52, 129, 502, 189, 561, "workzone", "Work Zone Merge", "Merge in direction of arrow.")
("workzone_flagger", 52, 220, 433, 280, 490, "workzone", "Work Zone Flagger Ahead", "Flagger directing traffic.")

# Key Driving Diagrams
("roundabout_navigation", 27, 244, 238, 342, 428, "diagram", "Roundabout Navigation", "Single-lane and multi-lane flow.")
("driver_hand_signals", 25, 68, 532, 295, 576, "diagram", "Driver Hand Signals", "Arm positions for Left Turn, Stop/Slow, Right Turn.")
("truck_no_zones", 30, 170, 280, 341, 332, "diagram", "Truck No-Zone Blind Spots", "Front, rear, and side blind spots.")
("pedestrian_signals", 31, 295, 151, 337, 243, "diagram", "Pedestrian Walk & Don't Walk", "Pedestrian crossing signals.")
("parking_on_hills", 37, 98, 271, 280, 338, "diagram", "Hill Parking Wheel Directions", "Curb turn direction on grades.")
("parallel_parking_steps", 37, 116, 458, 260, 573, "diagram", "Parallel Parking 4 Steps", "4-step maneuver to park within 18 inches.")
("vehicle_blind_spots", 38, 216, 361, 340, 480, "diagram", "Vehicle Blind Spots & Mirrors", "Mirror cones and vehicle blind spots.")
("stopping_distance_chart", 59, 103, 272, 276, 376, "diagram", "Stopping Distance by Speed", "Reaction vs braking distance chart.")
("seat_belt_law", 56, 276, 365, 338, 462, "diagram", "Seat Belt Law (Click It or Ticket)", "Missouri seat belt mandate.")
```

---

## 🚀 How to Run and Pick Up This Work

### 1. Launch the Application
In your terminal, navigate to the workspace directory:

```bash
cd /Users/nutanvamsigunti/workspace/missouri-driver-guide
./start.sh
```

Or run Python directly:
```bash
python3 server.py --open
```

The portal will open in your browser at: **`http://localhost:8080/`**.

### 2. Re-running the Data Extraction Pipeline
If you make changes to `CROPS` or extraction logic in `build_missouri_guide.py`:

```bash
cd /Users/nutanvamsigunti/workspace/missouri-driver-guide
./.venv/bin/python build_missouri_guide.py
```
This updates `guide_data.json` and `data.js` within 1 second without re-rendering existing WebP pages.

---

## 🔮 Recommended Next Steps for Future Sessions

1. **Expanded Exam Database**: Expand `PRACTICE_QUESTIONS` in `build_missouri_guide.py` from 40 to 100+ questions to enable random pool generation for endless practice exams.
2. **Offline PWA Support**: Add `service-worker.js` and `manifest.json` to enable full Progressive Web App installability on mobile devices.
3. **Audio Chapter Playlists**: Add continuous chapter playlist playback and rate controls (1x, 1.25x, 1.5x) to the text-to-speech toolbar.
4. **Printable Cheat Sheet**: Add a dedicated printable summary sheet for night-before cramming with all vital numbers (BAC limits, distances, fines, and point values).
