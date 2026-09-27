#!/usr/bin/env python3
"""
Comprehensive extraction pipeline for Missouri Driver Guide:
1. Renders all 102 pages to high-res WebP for interactive page viewer/mirror.
2. Extracts native raster images.
3. Crops individual traffic signs, lane markings, and driving diagrams.
4. Extracts and structures all 16 chapters + intro + index into structured JSON and data.js.
5. Builds a rich practice test question bank and flashcard deck.
"""

import os
import re
import json
import time
import fitz  # PyMuPDF
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Driver_Guide.pdf")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PAGES_DIR = os.path.join(ASSETS_DIR, "pages")
SIGNS_DIR = os.path.join(ASSETS_DIR, "images", "signs")
DIAGRAMS_DIR = os.path.join(ASSETS_DIR, "images", "diagrams")
EXTRACTED_DIR = os.path.join(ASSETS_DIR, "images", "extracted")

os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(SIGNS_DIR, exist_ok=True)
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
os.makedirs(EXTRACTED_DIR, exist_ok=True)

print("Opening Driver_Guide.pdf...")
doc = fitz.open(PDF_PATH)
total_pages = len(doc)
print(f"Total pages: {total_pages}")

# -------------------------------------------------------------
# 1. Render all pages to WebP (140 DPI, quality 82)
# -------------------------------------------------------------
print("Step 1: Rendering all 102 pages to WebP...")
t0 = time.time()
page_metadata = []
for pno in range(total_pages):
    page = doc[pno]
    out_file = os.path.join(PAGES_DIR, f"page_{pno+1:03d}.webp")
    if not os.path.exists(out_file) or os.path.getsize(out_file) == 0:
        pix = page.get_pixmap(dpi=140)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(out_file, "WEBP", quality=82)
    
    page_metadata.append({
        "page_number": pno + 1,
        "book_page": pno - 1 if pno >= 2 else (pno + 1),
        "file": f"assets/pages/page_{pno+1:03d}.webp",
        "width": page.rect.width,
        "height": page.rect.height
    })
print(f"Rendered {total_pages} pages in {time.time()-t0:.2f}s.")

# -------------------------------------------------------------
# 2. Extract native raster images
# -------------------------------------------------------------
print("Step 2: Extracting native raster images...")
seen_xrefs = set()
native_images = []
for pno in range(total_pages):
    page = doc[pno]
    for img_info in page.get_images(full=True):
        xref = img_info[0]
        if xref in seen_xrefs:
            continue
        seen_xrefs.add(xref)
        base = doc.extract_image(xref)
        ext = base["ext"]
        filename = f"page_{pno+1:03d}_xref{xref}.{ext}"
        filepath = os.path.join(EXTRACTED_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, "wb") as f:
                f.write(base["image"])
        native_images.append({
            "page": pno + 1,
            "xref": xref,
            "filename": filename,
            "path": f"assets/images/extracted/{filename}",
            "width": base["width"],
            "height": base["height"],
            "format": ext
        })
print(f"Extracted {len(native_images)} native images.")

# -------------------------------------------------------------
# 3. Crop individual traffic signs & diagrams
# -------------------------------------------------------------
print("Step 3: Cropping individual traffic signs and diagrams...")

# Bounding boxes carefully calibrated for 200 DPI extraction
# (name, page_idx, x0, y0, x1, y1, category, title, description)
CROPS = [
    # -------------------------------------------------------------
    # Page 47 (idx 46): Sign Shapes (Pure vector shapes from Page 47)
    # -------------------------------------------------------------
    ("shape_octagon", 46, 43, 374, 78, 409, "shapes", "Octagon Shape", "Exclusively used for Stop signs. Must come to a complete stop."),
    ("shape_triangle", 46, 43, 415, 78, 450, "shapes", "Triangle (Equilateral Downward)", "Exclusively used for Yield signs. Slow down and give right-of-way."),
    ("shape_vertical_rect", 46, 43, 456, 78, 498, "shapes", "Vertical Rectangle", "Used for Regulatory signs (speed limits, lane controls, turning rules)."),
    ("shape_horizontal_rect", 46, 43, 505, 85, 536, "shapes", "Horizontal Rectangle", "Used for Guide signs (directions, distances, state parks, services)."),
    ("shape_pentagon", 46, 43, 542, 78, 577, "shapes", "Pentagon (Pointed Up)", "Used for School Advance and School Crossing zones. Watch for children."),
    ("shape_round", 46, 186, 374, 222, 409, "shapes", "Round Shape", "Used for Railroad Crossing Advance Warning signs."),
    ("shape_crossbuck", 46, 190, 418, 220, 446, "shapes", "Crossbuck Shape", "Marks actual railroad grade crossing. Yield to trains."),
    ("shape_pennant", 46, 186, 456, 228, 492, "shapes", "Pennant Shape (Isosceles)", "No Passing Zone warning. Posted on the left side of two-lane roads."),
    ("shape_diamond", 46, 186, 505, 225, 552, "shapes", "Diamond Shape", "Used for Warning signs of roadway hazards, curves, and conditions."),

    # -------------------------------------------------------------
    # Page 48 (idx 47): Warning Signs (Traffic Control & Traffic Flow)
    # -------------------------------------------------------------
    ("stop_ahead", 47, 36, 112, 93, 167, "warning", "Stop Ahead", "A stop sign is ahead on the road. Slow down and prepare to stop."),
    ("signal_ahead", 47, 192, 112, 249, 167, "warning", "Signal Ahead", "Traffic light signal ahead. Be prepared to stop if light is red or yellow."),
    ("pedestrian_crossing", 47, 36, 177, 94, 248, "warning", "Pedestrian Crossing", "Yield to pedestrians walking in the crosswalk. Slow down."),
    ("school_crossing", 47, 194, 177, 246, 228, "warning", "School Crossing", "Slow down and watch for children crossing. School zone ahead."),
    ("exit_speed_advisory", 47, 36, 296, 93, 352, "warning", "Exit Speed Advisory", "Advisory maximum safe speed for the highway exit ramp."),
    ("added_lane", 47, 187, 300, 245, 356, "warning", "Added Lane", "Traffic entering from another road gets its own new lane. No merging required."),
    ("divided_road_begin", 47, 35, 390, 92, 445, "warning", "Begin Divided Roadway", "Two-way traffic ahead will be separated by a median or barrier."),
    ("divided_road_end", 47, 189, 391, 246, 446, "warning", "End Divided Roadway", "Two-way traffic will no longer be separated. Keep right."),
    ("merge", 47, 35, 477, 93, 532, "warning", "Merge Ahead", "Traffic from another road will be merging into your lane. Be alert."),
    ("lane_ends_merge_left", 47, 188, 477, 245, 532, "warning", "Lane Ends / Merge Left", "Right lane ends ahead. Drivers in right lane must yield and merge left."),

    # -------------------------------------------------------------
    # Page 49 (idx 48): Turns, Curves, Special Road Conditions
    # -------------------------------------------------------------
    ("curve", 48, 36, 56, 93, 111, "warning", "Curve Ahead", "Gradual curve ahead where safe speed is below posted speed limit."),
    ("turn", 48, 187, 56, 245, 111, "warning", "Sharp Turn Ahead", "Sharp turn ahead where recommended maximum speed is 30 mph or less."),
    ("reverse_turn", 48, 36, 140, 93, 195, "warning", "Reverse Turn", "Two turns in opposite directions ahead. Second turn may be sharper. 30 mph or less."),
    ("speed_advisory", 48, 187, 138, 246, 194, "warning", "Speed Advisory Plate", "Recommended safe speed for curve or turn under fair weather."),
    ("large_arrow", 48, 35, 283, 120, 330, "warning", "Large Sharp Arrow", "Posted on the outside of sharp curves and turns to emphasize direction."),
    ("chevron", 48, 191, 265, 246, 330, "warning", "Chevron", "Used along sharp curves and turns to guide drivers along the curve."),
    ("object_marker", 48, 38, 356, 73, 456, "warning", "Object Marker", "Warns of physical obstruction very close to roadway edge."),
    ("soft_shoulder", 48, 183, 358, 240, 414, "warning", "Soft Shoulder", "Shoulder on side of road is soft dirt/gravel. Do not pull off pavement."),
    ("slow_moving_vehicle", 48, 24, 494, 87, 551, "warning", "Slow Moving Vehicle", "Mounted on vehicles traveling under 25 mph (farm and construction equipment)."),
    ("share_the_road", 48, 187, 420, 235, 497, "warning", "Bicycle - Share the Road", "Watch for cyclists sharing the travel lane with motor vehicles."),
    ("slippery_when_wet", 48, 183, 508, 240, 564, "warning", "Slippery When Wet", "Roadway becomes unusually slick in rain or wet conditions. Reduce speed."),

    # -------------------------------------------------------------
    # Page 50 (idx 49): Intersections & Regulatory Prohibitions
    # -------------------------------------------------------------
    ("side_road_rr_crossing", 49, 36, 52, 93, 108, "warning", "Side Road RR Crossing", "Railroad tracks are located very close to the intersection."),
    ("intersection_warning", 49, 188, 52, 245, 108, "warning", "Crossroad / Intersection", "Another road crosses ahead. Watch carefully for cross-traffic."),
    ("side_road_ahead", 49, 36, 140, 93, 196, "warning", "Side Road Ahead", "Side road enters highway from side shown on sign."),
    ("t_intersection_ahead", 49, 188, 140, 245, 196, "warning", "T-Intersection Ahead", "Road ends ahead at a T. You must turn left or right."),
    ("roundabout_ahead", 49, 35, 207, 92, 271, "warning", "Roundabout Ahead", "Circular intersection ahead. Counter-clockwise flow; yield to traffic in circle."),
    ("no_left_turn", 49, 78, 394, 138, 454, "regulatory", "No Left Turn", "Left turn is prohibited at this intersection."),
    ("no_right_turn", 49, 163, 394, 223, 454, "regulatory", "No Right Turn", "Right turn is prohibited at this intersection."),
    ("no_u_turn", 49, 248, 394, 308, 454, "regulatory", "No U-Turn", "U-turns are prohibited at this location."),
    ("no_trucks", 49, 78, 479, 138, 539, "regulatory", "No Trucks", "Commercial trucks are prohibited from using this roadway."),
    ("no_bicycles", 49, 163, 479, 223, 539, "regulatory", "No Bicycles", "Bicycles are prohibited from using this roadway or expressway."),

    # -------------------------------------------------------------
    # Page 51 (idx 50): Regulatory Signs (Stop, Yield, Speed)
    # -------------------------------------------------------------
    ("stop_sign", 50, 282, 48, 343, 109, "regulatory", "Stop Sign", "Come to a complete stop before stop line, crosswalk, or intersection edge."),
    ("yield_sign", 50, 286, 329, 343, 383, "regulatory", "Yield Sign", "Slow down and yield right-of-way to all vehicles and pedestrians before proceeding."),
    ("wrong_way_sign", 50, 286, 390, 343, 430, "regulatory", "Wrong Way", "You are driving against opposing traffic. Pull over and turn around immediately."),
    ("do_not_enter_sign", 50, 290, 441, 343, 492, "regulatory", "Do Not Enter", "Vehicles may not enter roadway, ramp, or lane from this direction."),
    ("one_way_sign", 50, 273, 494, 342, 519, "regulatory", "One Way", "Traffic on this roadway or ramp moves only in direction of the arrow."),
    ("lane_control_only", 50, 273, 529, 342, 573, "regulatory", "Lane Control (Only)", "Movements allowed from specific lane (Turn Only or Straight Only)."),

    # -------------------------------------------------------------
    # Page 52 (idx 51): Speed Limits & Railroad Crossbuck
    # -------------------------------------------------------------
    ("speed_limit_70", 51, 298, 36, 342, 129, "regulatory", "Speed Limit 70 / Min 40", "Maximum 70 mph; minimum 40 mph under normal conditions."),
    ("keep_right", 51, 301, 175, 342, 214, "regulatory", "Keep Right", "Keep to the right of traffic island, median, or divider."),
    ("railroad_crossbuck", 51, 237, 475, 342, 537, "regulatory", "Railroad Crossbuck", "Treat as a Yield sign. Look both ways and yield right-of-way to trains."),

    # -------------------------------------------------------------
    # Page 53 (idx 52): Work Zone Signs
    # -------------------------------------------------------------
    ("road_work_ahead", 52, 36, 436, 95, 496, "workzone", "Road Work Ahead", "Work zone ahead. Fines are doubled for speeding or violations."),
    ("fresh_oil", 52, 129, 436, 188, 496, "workzone", "Fresh Oil", "Road surface was recently oiled. Drive slowly to avoid skidding and splatter."),
    ("right_lane_closed_ahead", 52, 35, 503, 95, 562, "workzone", "Right Lane Closed Ahead", "Right travel lane closes ahead; merge left smoothly."),
    ("workzone_merge", 52, 129, 502, 189, 561, "workzone", "Work Zone Merge", "Merge in direction of arrow due to work zone lane closure."),
    ("workzone_flagger", 52, 220, 433, 280, 490, "workzone", "Work Zone Flagger Ahead", "Flagger ahead directing traffic in work zone. Obey all signals."),
    ("workzone_speed_ahead", 52, 219, 500, 279, 564, "workzone", "Work Zone Speed Limit Ahead", "Reduced speed limit ahead inside the work zone."),
    ("workzone_end_road_work", 52, 285, 482, 345, 515, "workzone", "End Road Work", "Marks the end of the active construction or maintenance zone."),

    # -------------------------------------------------------------
    # Page 56 (idx 55): Guide Signs & Highway Shields
    # -------------------------------------------------------------
    ("vehicle_inspection_station", 55, 230, 98, 268, 134, "guide", "Official Vehicle Inspection Station", "Sign posted at authorized Missouri motor vehicle safety and emissions inspection stations."),
    ("interstate_shield", 55, 58, 450, 93, 485, "guide", "Interstate Route Shield (I-70)", "Red, white, and blue shield indicating Interstate highway."),
    ("business_loop", 55, 98, 450, 133, 485, "guide", "Business Loop Shield (Loop 44)", "Green shield for business loop through commercial area."),
    ("us_route_shield", 55, 138, 450, 173, 485, "guide", "US Highway Shield (US-36)", "Black and white shield indicating Federal US Highway."),
    ("missouri_route_shield", 55, 178, 450, 213, 485, "guide", "Missouri State Route (Route 25)", "Missouri state route highway marker."),
    ("county_road", 55, 218, 450, 253, 485, "guide", "County Lettered Road (Route A)", "Missouri secondary lettered highway."),
    ("emergency_marker", 55, 280, 485, 345, 575, "guide", "Emergency Reference Marker", "Provides route, direction, and milepost for dispatchers."),

    # -------------------------------------------------------------
    # Maneuver & Driving Diagrams (Various Pages)
    # -------------------------------------------------------------
    ("school_bus_stopping", 25, 212, 36, 344, 98, "diagram", "School Bus Stop Law", "When to stop on 2-lane vs 4-lane divided roads."),
    ("turn_right_diagram", 26, 233, 102, 338, 226, "diagram", "Right Turn Position", "Approach and complete turns close to the right curb."),
    ("turn_left_2way_diagram", 26, 232, 225, 341, 351, "diagram", "Left Turn: 2-Way to 2-Way", "Turn before the center of the intersection into left lane."),
    ("turn_left_1way_diagram", 26, 232, 363, 339, 474, "diagram", "Left Turn: 2-Way to 1-Way", "Turn from nearest left lane into nearest left lane of 1-way."),
    ("turn_left_multilane_diagram", 27, 234, 36, 343, 142, "diagram", "Left Turn: Multi-Lane", "Stay in designated lane during dual left turn."),
    ("roundabout_navigation", 27, 244, 238, 342, 428, "diagram", "Roundabout Navigation", "Single-lane and multi-lane flow; yield to traffic in circle."),
    ("shared_center_turn_lane", 27, 204, 159, 336, 214, "diagram", "Shared Center Left-Turn Lane", "Do not use for passing; only for turning left."),
    ("j_turn_intersection", 28, 198, 334, 343, 381, "diagram", "J-Turn Intersection", "Safer alternative to direct left turns across high-speed divided highways."),
    ("driver_hand_signals", 25, 68, 532, 295, 576, "diagram", "Driver Hand Signals", "Arm positions for Left Turn, Stop/Slow, and Right Turn."),
    ("truck_no_zones", 30, 170, 280, 341, 332, "diagram", "Truck No-Zone Blind Spots", "Front, rear, and wide side blind spots of commercial semi-trucks."),
    ("pedestrian_signals", 31, 295, 151, 337, 243, "diagram", "Pedestrian Walk & Don't Walk Signals", "Walk symbol and flashing/steady Don't Walk hand indicators."),
    ("parking_on_hills", 37, 98, 271, 280, 338, "diagram", "Hill Parking Wheel Directions", "Turn wheels to right for downhill and uphill without curb; turn wheels to left for uphill with curb."),
    ("parallel_parking_steps", 37, 116, 458, 260, 573, "diagram", "Parallel Parking 4 Steps", "Pull alongside car, turn wheel sharp right into space, straighten, and center vehicle within 18 inches of curb."),
    ("vehicle_blind_spots", 38, 216, 361, 340, 480, "diagram", "Vehicle Blind Spots & Mirrors", "Inside mirror view, outside mirror cone of vision, and areas hidden in driver blind spots (Vehicles A & B)."),
    ("traffic_light_signals", 45, 303, 73, 338, 128, "diagram", "Traffic Light Sequences", "Solid red, yellow, and green signal sequence."),
    ("flashing_arrow_signals", 45, 297, 308, 338, 437, "diagram", "Flashing Yellow Arrow Turn Sequences", "Protected green arrow, flashing yellow yield arrow, and red arrow."),
    ("stopping_distance_chart", 59, 103, 272, 276, 376, "diagram", "Stopping Distance by Speed (MPH)", "Official chart comparing reaction distance and braking distance in feet from 20 mph (44 ft total) to 80 mph (460 ft total)."),
    ("seat_belt_law", 56, 276, 365, 338, 462, "diagram", "Seat Belt Law (Click It or Ticket)", "Missouri safety belt law requiring drivers and front seat passengers to wear properly adjusted safety belts.")
]

cropped_catalog = []
for name, pno, x0, y0, x1, y1, cat, title, desc in CROPS:
    target_dir = SIGNS_DIR if cat in ["shapes", "warning", "regulatory", "workzone", "guide"] else DIAGRAMS_DIR
    out_file = os.path.join(target_dir, f"{name}.png")
    page = doc[pno]
    rect = fitz.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(clip=rect, dpi=200)
    pix.save(out_file)
    rel_path = os.path.relpath(out_file, BASE_DIR)
    cropped_catalog.append({
        "id": name,
        "title": title,
        "description": desc,
        "category": cat,
        "page": pno + 1,
        "image": rel_path,
        "width": pix.width,
        "height": pix.height
    })

print(f"Saved {len(cropped_catalog)} cropped signs and diagrams.")

# -------------------------------------------------------------
# 4. Extract Text & Structure All 16 Chapters + Intro + Index
# -------------------------------------------------------------
print("Step 4: Extracting structured text across all chapters...")

CHAPTER_RANGES = [
    {
        "id": "intro",
        "number": 0,
        "title": "Welcome & Missouri Driver Examination Overview",
        "start_page": 1,
        "end_page": 4,
        "book_pages": "Cover - 2",
        "icon": "fa-id-card",
        "color": "#2563eb",
        "summary": "Introduction to the Missouri Driver Guide, examination structure (25 questions, 20 to pass), and safety principles."
    },
    {
        "id": "chapter-1",
        "number": 1,
        "title": "The Missouri Driver License",
        "start_page": 5,
        "end_page": 19,
        "book_pages": "3 - 17",
        "icon": "fa-address-card",
        "color": "#1d4ed8",
        "summary": "Licensing requirements, Graduated Driver License (GDL), permit ages (15, 15½, 16), REAL ID, voter registration, organ donation, and fees."
    },
    {
        "id": "chapter-2",
        "number": 2,
        "title": "The Driver Examination",
        "start_page": 20,
        "end_page": 23,
        "book_pages": "18 - 21",
        "icon": "fa-clipboard-check",
        "color": "#0ea5e9",
        "summary": "The four-part driver examination: Vision (20/40), Road Signs, Written Knowledge (80% / 20 of 25), and Driving Skills Test."
    },
    {
        "id": "chapter-3",
        "number": 3,
        "title": "Rules of the Road",
        "start_page": 24,
        "end_page": 29,
        "book_pages": "22 - 27",
        "icon": "fa-road",
        "color": "#059669",
        "summary": "Careful & prudent driving, speed limits, right-of-way rules, four-way stops, emergency vehicles, school buses, roundabouts, turns, and hand signals."
    },
    {
        "id": "chapter-4",
        "number": 4,
        "title": "Sharing the Road",
        "start_page": 30,
        "end_page": 36,
        "book_pages": "28 - 34",
        "icon": "fa-users",
        "color": "#10b981",
        "summary": "Sharing roadways safely with motorcycles, large commercial trucks ('No-Zone' blind spots), pedestrians, school buses, trains, and bicycles."
    },
    {
        "id": "chapter-5",
        "number": 5,
        "title": "Parking",
        "start_page": 37,
        "end_page": 38,
        "book_pages": "35 - 36",
        "icon": "fa-square-parking",
        "color": "#d97706",
        "summary": "Parallel parking step-by-step, parking on hills with/without curb, prohibited parking zones, and accessible parking placards."
    },
    {
        "id": "chapter-6",
        "number": 6,
        "title": "Highway Driving",
        "start_page": 39,
        "end_page": 43,
        "book_pages": "37 - 41",
        "icon": "fa-gauge-high",
        "color": "#f59e0b",
        "summary": "Interstate driving, acceleration and deceleration ramps, highway hypnosis, velocitizing, breakdown procedures, and interchange maneuvers."
    },
    {
        "id": "chapter-7",
        "number": 7,
        "title": "Pavement Markings, Traffic Signs, and Signals",
        "start_page": 44,
        "end_page": 56,
        "book_pages": "42 - 54",
        "icon": "fa-traffic-light",
        "color": "#dc2626",
        "summary": "Comprehensive guide to Missouri pavement markings (yellow/white lines), traffic light sequences, sign shapes, sign colors, regulatory, warning, work zone, and guide signs."
    },
    {
        "id": "chapter-8",
        "number": 8,
        "title": "Safe Driving Tips For Everyday Driving",
        "start_page": 57,
        "end_page": 63,
        "book_pages": "55 - 61",
        "icon": "fa-shield-halved",
        "color": "#7c3aed",
        "summary": "Seat belts and child restraints (under 8 / 80 lbs), defensive driving, 3-second following distance rule, stopping distance charts, adjusting mirrors, and headlights."
    },
    {
        "id": "chapter-9",
        "number": 9,
        "title": "Safe Driving Tips For Special Driving Conditions",
        "start_page": 64,
        "end_page": 68,
        "book_pages": "62 - 66",
        "icon": "fa-cloud-rain",
        "color": "#6366f1",
        "summary": "Night driving, rain, fog, winter ice/snow, hydroplaning recovery, brake failure, tire blowouts, and submerged vehicle escapes."
    },
    {
        "id": "chapter-10",
        "number": 10,
        "title": "Alcohol, Drugs, and Driving",
        "start_page": 69,
        "end_page": 74,
        "book_pages": "67 - 72",
        "icon": "fa-wine-bottle",
        "color": "#b91c1c",
        "summary": "Blood Alcohol Concentration (BAC) limits (.08% adult, .02% under 21, .04% commercial), Implied Consent law, Abuse and Lose law, ignition interlock devices, and criminal penalties."
    },
    {
        "id": "chapter-11",
        "number": 11,
        "title": "The Point System",
        "start_page": 75,
        "end_page": 76,
        "book_pages": "73 - 74",
        "icon": "fa-triangle-exclamation",
        "color": "#ea580c",
        "summary": "Missouri point system: warning notice at 4 points, suspension at 8 points in 18 months (30 to 90 days), and 1-year revocation at 12 points in 12 months."
    },
    {
        "id": "chapter-12",
        "number": 12,
        "title": "Vehicle Titling and Registration",
        "start_page": 77,
        "end_page": 80,
        "book_pages": "75 - 78",
        "icon": "fa-car",
        "color": "#0284c7",
        "summary": "Titling a new or used vehicle within 30 days, registration renewals, personalized plates, disability plates, and selling a motor vehicle."
    },
    {
        "id": "chapter-13",
        "number": 13,
        "title": "Mandatory Insurance",
        "start_page": 81,
        "end_page": 84,
        "book_pages": "79 - 82",
        "icon": "fa-file-shield",
        "color": "#16a34a",
        "summary": "Missouri financial responsibility law: 25/50/25 liability coverage ($25k bodily injury per person, $50k per crash, $25k property damage), failure to maintain proof penalties."
    },
    {
        "id": "chapter-14",
        "number": 14,
        "title": "Safety and Emissions Inspections & Required Equipment",
        "start_page": 85,
        "end_page": 88,
        "book_pages": "83 - 86",
        "icon": "fa-wrench",
        "color": "#4b5563",
        "summary": "Biennial safety inspections, Gateway Vehicle Inspection emissions testing (St. Louis area), and required equipment (brakes, lights, horn, muffler, mirrors, wipers)."
    },
    {
        "id": "chapter-15",
        "number": 15,
        "title": "Commercial Vehicles",
        "start_page": 89,
        "end_page": 93,
        "book_pages": "87 - 91",
        "icon": "fa-truck",
        "color": "#374151",
        "summary": "Class E chauffeur's license requirements, gross weight ratings (GVWR), emergency equipment, clearance lights, mud flaps, and maximum dimensions."
    },
    {
        "id": "chapter-16",
        "number": 16,
        "title": "Distracted Driving & Electronic Communication Devices",
        "start_page": 94,
        "end_page": 95,
        "book_pages": "92 - 93",
        "icon": "fa-mobile-screen-button",
        "color": "#e11d48",
        "summary": "Missouri's Siddens Bening Hands-Free Law (SB 398): prohibited handheld cellphone activities while driving, permitted hands-free operations, exemptions, and fines."
    },
    {
        "id": "index",
        "number": 17,
        "title": "Index & Key Terms",
        "start_page": 96,
        "end_page": 99,
        "book_pages": "94 - 97",
        "icon": "fa-magnifying-glass",
        "color": "#475569",
        "summary": "Comprehensive alphabetical index of all driving terms, traffic violations, and state procedures."
    },
    {
        "id": "contacts",
        "number": 18,
        "title": "Contact Information & Move Over Law",
        "start_page": 100,
        "end_page": 102,
        "book_pages": "98 - 100",
        "icon": "fa-phone-volume",
        "color": "#0f172a",
        "summary": "Department of Revenue office locations, Missouri State Highway Patrol troop headquarters, emergency numbers, and the Move Over law."
    }
]

def clean_extracted_text(text):
    # Remove header / footer lines like 'Chapter X - ...' and lone page numbers
    lines = text.split("\n")
    cleaned_lines = []
    for l in lines:
        stripped = l.strip()
        if not stripped:
            continue
        if re.match(r"^Chapter\s+\d+", stripped, re.I):
            continue
        if re.match(r"^\d{1,3}$", stripped):
            continue
        cleaned_lines.append(stripped)
    return "\n".join(cleaned_lines)

chapters_data = []

for ch in CHAPTER_RANGES:
    ch_text_blocks = []
    ch_raw_pages = []
    ch_figures = [c for c in cropped_catalog if ch["start_page"] <= c["page"] <= ch["end_page"]]
    
    for pno in range(ch["start_page"] - 1, ch["end_page"]):
        page = doc[pno]
        raw_text = page.get_text()
        blocks = page.get_text("blocks")
        
        # parse blocks into structured segments
        page_blocks = []
        for b in blocks:
            # b: (x0, y0, x1, y1, text, block_no, block_type)
            if b[6] == 0:  # text block
                b_text = b[4].strip()
                if not b_text or re.match(r"^\d{1,3}$", b_text) or re.match(r"^Chapter\s+\d+", b_text, re.I):
                    continue
                
                # Check for callout flags
                is_tip = b_text.startswith("Tip!")
                is_note = "IMPORTANT NOTE:" in b_text or "Note:" in b_text
                is_warning = "WARNING:" in b_text or "Caution:" in b_text
                is_heading = False
                
                lines = b_text.split("\n")
                first_line = lines[0].strip()
                if len(first_line) < 45 and (b[1] < 120 or b_text.isupper() or first_line.endswith(":") or (len(lines) > 1 and len(first_line) < len(lines[1]))):
                    is_heading = True
                
                page_blocks.append({
                    "text": b_text,
                    "first_line": first_line,
                    "is_heading": is_heading,
                    "is_tip": is_tip,
                    "is_note": is_note,
                    "is_warning": is_warning,
                    "bbox": [round(b[0], 1), round(b[1], 1), round(b[2], 1), round(b[3], 1)]
                })
        
        ch_raw_pages.append({
            "page_number": pno + 1,
            "book_page": pno - 1 if pno >= 2 else (pno + 1),
            "text": clean_extracted_text(raw_text),
            "blocks": page_blocks,
            "preview_image": f"assets/pages/page_{pno+1:03d}.webp"
        })
    
    # Combined full text for fast search
    full_text = "\n\n".join([p["text"] for p in ch_raw_pages])
    
    # Calculate reading time (avg 200 wpm)
    word_count = len(full_text.split())
    read_minutes = max(1, round(word_count / 200))
    
    chapters_data.append({
        **ch,
        "word_count": word_count,
        "read_minutes": read_minutes,
        "figures": ch_figures,
        "pages": ch_raw_pages,
        "full_text": full_text
    })

print(f"Processed {len(chapters_data)} structured chapters.")

# -------------------------------------------------------------
# 5. Build Missouri Permit Practice Exam Bank (60 Questions)
# -------------------------------------------------------------
print("Step 5: Compiling 60-question Missouri practice exam database...")

PRACTICE_QUESTIONS = [
    {
        "id": 1,
        "chapter": 1,
        "question": "At what age are you eligible to obtain an Instruction Permit in Missouri?",
        "options": ["14 years old", "15 years old", "15½ years old", "16 years old"],
        "correctIndex": 1,
        "explanation": "In Missouri, you are eligible for an Instruction Permit at age 15. You must be accompanied by a qualified licensed adult driver seated in the front passenger seat.",
        "rule": "Graduated Driver License (GDL) Law - Chapter 1, Page 5"
    },
    {
        "id": 2,
        "chapter": 1,
        "question": "How many months must you hold an Instruction Permit before you are eligible to apply for an Intermediate License?",
        "options": ["3 months", "6 months", "9 months", "12 months"],
        "correctIndex": 1,
        "explanation": "You must hold your instruction permit for a minimum of 6 months (182 days) without alcohol or drug violations before applying for an Intermediate License.",
        "rule": "Chapter 1, Page 6"
    },
    {
        "id": 3,
        "chapter": 1,
        "question": "How many hours of supervised driving must a Missouri teen complete before obtaining an Intermediate License, including nighttime driving?",
        "options": ["20 hours total, 5 at night", "30 hours total, 10 at night", "40 hours total, 10 at night", "50 hours total, 10 at night"],
        "correctIndex": 2,
        "explanation": "Missouri GDL requires at least 40 hours of supervised driving practice, which must include at least 10 hours of nighttime driving between sunset and sunrise.",
        "rule": "Chapter 1, Page 6"
    },
    {
        "id": 4,
        "chapter": 1,
        "question": "Under Missouri's Graduated Driver License (GDL) law, what are the curfew hours for an Intermediate License holder?",
        "options": ["10:00 PM to 5:00 AM", "11:00 PM to 5:00 AM", "1:00 AM to 5:00 AM", "Midnight to 6:00 AM"],
        "correctIndex": 2,
        "explanation": "Intermediate drivers may not drive alone between 1:00 AM and 5:00 AM, except to or from school activities or work, or when accompanied by a licensed driver 21 or older.",
        "rule": "Chapter 1, Page 7"
    },
    {
        "id": 5,
        "chapter": 2,
        "question": "What is the minimum score required to pass the written Missouri driver knowledge examination?",
        "options": ["70% (18 out of 25)", "75% (19 out of 25)", "80% (20 out of 25)", "88% (22 out of 25)"],
        "correctIndex": 2,
        "explanation": "The written test consists of 25 multiple-choice questions. You must answer at least 20 correctly (80%) to pass.",
        "rule": "Chapter 2, Page 20"
    },
    {
        "id": 6,
        "chapter": 2,
        "question": "What is the vision visual acuity standard to pass the Missouri driver license eye test without restrictions?",
        "options": ["20/20 in both eyes", "20/40 or better with either or both eyes", "20/60 in either eye", "20/70 with corrective lenses"],
        "correctIndex": 1,
        "explanation": "You must meet a minimum vision standard of 20/40 with either eye or both eyes combined to qualify for an unrestricted license.",
        "rule": "Chapter 2, Page 20"
    },
    {
        "id": 7,
        "chapter": 3,
        "question": "When two vehicles reach an uncontrolled 4-way intersection at the same time, who has the right-of-way?",
        "options": ["The vehicle on the left", "The vehicle on the right", "The vehicle traveling at a higher speed", "The larger vehicle"],
        "correctIndex": 1,
        "explanation": "When two vehicles reach an intersection without traffic control at approximately the same time, the driver on the left must yield to the driver on the right.",
        "rule": "Chapter 3, Page 24"
    },
    {
        "id": 8,
        "chapter": 3,
        "question": "When an emergency vehicle approaches with flashing red/blue lights and a siren sounding, what must you do?",
        "options": [
            "Speed up to get out of its way",
            "Slow down and stay in your current lane",
            "Immediately pull over to the right edge or curb and stop until it passes",
            "Stop immediately in the middle of your lane"
        ],
        "correctIndex": 2,
        "explanation": "You must immediately drive to a position parallel to, and as close as possible to, the right-hand edge or curb of the roadway and stop until the emergency vehicle passes.",
        "rule": "Chapter 3, Page 25"
    },
    {
        "id": 9,
        "chapter": 3,
        "question": "On a two-lane road, when a school bus stops with its red signals flashing and stop arm extended, who must stop?",
        "options": [
            "Only vehicles following directly behind the bus",
            "Drivers approaching from both directions must stop",
            "Only commercial trucks and vans",
            "No vehicles need to stop if there are no children in the street"
        ],
        "correctIndex": 1,
        "explanation": "On a two-lane highway, traffic moving in BOTH directions must stop at least 20 feet away while the bus is stopped and children are boarding or alighting.",
        "rule": "Chapter 3, Page 25"
    },
    {
        "id": 10,
        "chapter": 3,
        "question": "When are you NOT required to stop for a school bus with flashing red lights in Missouri?",
        "options": [
            "When driving on a rural gravel road",
            "When traveling in the opposite direction on a highway with four or more lanes of traffic",
            "During afternoon hours between 3:00 PM and 5:00 PM",
            "When driving at the posted speed limit"
        ],
        "correctIndex": 1,
        "explanation": "You do not need to stop when traveling in the opposite direction on a highway that has four or more lanes of traffic (separated by a median or multi-lane configuration).",
        "rule": "Chapter 3, Page 26"
    },
    {
        "id": 11,
        "chapter": 3,
        "question": "What is the proper hand signal for a left turn?",
        "options": [
            "Left arm and hand pointing upward",
            "Left arm and hand extended straight out horizontally",
            "Left arm and hand pointing downward",
            "Waving your left hand"
        ],
        "correctIndex": 1,
        "explanation": "Extend your left hand and arm straight out horizontally from the window for a left turn.",
        "rule": "Chapter 3, Page 29",
        "image": "assets/images/diagrams/driver_hand_signals.png"
    },
    {
        "id": 12,
        "chapter": 3,
        "question": "What is the proper hand signal for slowing down or stopping?",
        "options": [
            "Left arm and hand pointing upward",
            "Left arm and hand pointing downward",
            "Left arm and hand extended straight out",
            "Tapping your steering wheel"
        ],
        "correctIndex": 1,
        "explanation": "Extend your left hand and arm downward with the palm facing backward to signal that you are slowing down or stopping.",
        "rule": "Chapter 3, Page 29",
        "image": "assets/images/diagrams/driver_hand_signals.png"
    },
    {
        "id": 13,
        "chapter": 4,
        "question": "What are the blind spots around large trucks and tractor-trailers called?",
        "options": ["Dead Angles", "Danger Circles", "No-Zones", "Safety Rings"],
        "correctIndex": 2,
        "explanation": "Large commercial trucks have four large blind spots known as 'No-Zones': in front, directly behind, and on both sides (especially the right side). If you can't see the driver in their mirror, they can't see you.",
        "rule": "Chapter 4, Page 32",
        "image": "assets/images/diagrams/truck_no_zones.png"
    },
    {
        "id": 14,
        "chapter": 4,
        "question": "How much space should a motorist give a bicyclist when passing on a roadway?",
        "options": ["At least 1 foot", "At least 2 feet", "At least 3 feet or a safe distance", "Bicycles must ride on the sidewalk"],
        "correctIndex": 2,
        "explanation": "Missouri law requires motorists to exercise the highest degree of care and leave a safe distance (at least 3 feet or more) when passing a bicyclist.",
        "rule": "Chapter 4, Page 31"
    },
    {
        "id": 15,
        "chapter": 5,
        "question": "When parking downhill on a two-way street with a curb, which way should you turn your front wheels?",
        "options": [
            "Straight ahead",
            "Away from the curb (to the left)",
            "Toward the curb (to the right)",
            "Direction does not matter as long as parking brake is on"
        ],
        "correctIndex": 2,
        "explanation": "When parking downhill with a curb, turn your front wheels toward the curb (to the right). If your brakes fail, the vehicle will roll into the curb and stop.",
        "rule": "Chapter 5, Page 38",
        "image": "assets/images/diagrams/parking_on_hills.png"
    },
    {
        "id": 16,
        "chapter": 5,
        "question": "When parking uphill with a curb, which way should you turn your front wheels?",
        "options": [
            "Toward the curb (to the right)",
            "Away from the curb (to the left)",
            "Straight ahead",
            "Parallel with the curb"
        ],
        "correctIndex": 1,
        "explanation": "When parking uphill with a curb, turn your front wheels away from the curb (to the left) and let the vehicle roll back slightly until the rear of the front tire touches the curb.",
        "rule": "Chapter 5, Page 38",
        "image": "assets/images/diagrams/parking_on_hills.png"
    },
    {
        "id": 17,
        "chapter": 5,
        "question": "How close to the curb must a vehicle be parked when parallel parked on a Missouri roadway?",
        "options": [
            "Within 6 inches",
            "Within 12 inches",
            "Within 18 inches",
            "Within 24 inches"
        ],
        "correctIndex": 2,
        "explanation": "Missouri law states that vehicles must be parked parallel to the curb with the wheels within 18 inches of the curb.",
        "rule": "Chapter 5, Page 37"
    },
    {
        "id": 18,
        "chapter": 6,
        "question": "What is 'highway hypnosis'?",
        "options": [
            "A sleep condition caused by road glare",
            "A dull, drowsy, or trance-like condition caused by driving on monotonous highways for long distances",
            "Speeding caused by tailgating",
            "Inability to read highway signs in dense fog"
        ],
        "correctIndex": 1,
        "explanation": "Highway hypnosis is a trance-like state resulting from long stretches of monotonous driving. Drivers can combat it by keeping their eyes moving, taking frequent breaks, and shifting focus.",
        "rule": "Chapter 6, Page 40"
    },
    {
        "id": 19,
        "chapter": 7,
        "question": "What does an eight-sided (octagon) traffic sign always mean?",
        "options": ["Yield", "Railroad Warning", "School Zone", "Stop"],
        "correctIndex": 3,
        "explanation": "An octagon is reserved exclusively for STOP signs. You must make a complete stop before the stop line, crosswalk, or intersection.",
        "rule": "Chapter 7, Page 47",
        "image": "assets/images/signs/stop_sign.png"
    },
    {
        "id": 20,
        "chapter": 7,
        "question": "What does a triangular traffic sign with point pointing downward indicate?",
        "options": ["No Passing Zone", "Yield Right-of-Way", "Divided Highway Ahead", "Detour Ahead"],
        "correctIndex": 1,
        "explanation": "A triangular sign pointing downward is exclusively a YIELD sign. You must slow down and give right-of-way to all vehicles and pedestrians before proceeding.",
        "rule": "Chapter 7, Page 47",
        "image": "assets/images/signs/yield_sign.png"
    },
    {
        "id": 21,
        "chapter": 7,
        "question": "What does a pennant-shaped sign posted on the left side of the road signify?",
        "options": ["Dead End", "No Passing Zone", "School Crossing", "Railroad Crossing"],
        "correctIndex": 1,
        "explanation": "A pennant-shaped sign is placed on the left side of a two-lane road to indicate a NO PASSING ZONE.",
        "rule": "Chapter 7, Page 47",
        "image": "assets/images/signs/shape_pennant.png"
    },
    {
        "id": 22,
        "chapter": 7,
        "question": "What does a flashing red traffic signal mean?",
        "options": [
            "Slow down and proceed with caution",
            "Yield to oncoming traffic only",
            "Come to a complete stop, just like a stop sign, and proceed when safe",
            "The traffic light is out of order; continue at current speed"
        ],
        "correctIndex": 2,
        "explanation": "A flashing red light has the same meaning as a STOP sign. Come to a complete stop, yield to cross-traffic and pedestrians, and proceed when clear.",
        "rule": "Chapter 7, Page 46"
    },
    {
        "id": 23,
        "chapter": 7,
        "question": "What does a flashing yellow traffic signal indicate?",
        "options": [
            "Come to a full stop",
            "Slow down and proceed with caution",
            "The intersection is closed",
            "Speed up to clear the intersection"
        ],
        "correctIndex": 1,
        "explanation": "A flashing yellow light warns drivers to slow down and proceed through the intersection with caution.",
        "rule": "Chapter 7, Page 46"
    },
    {
        "id": 24,
        "chapter": 7,
        "question": "What does this yellow diamond sign with a sliding vehicle signify?",
        "options": [
            "Winding road ahead",
            "Steep downgrade ahead",
            "Slippery when wet",
            "Loose gravel on road"
        ],
        "correctIndex": 2,
        "explanation": "This sign warns that the road surface becomes slick and hazardous when wet. Reduce speed and avoid sudden steering or braking.",
        "rule": "Chapter 7, Page 49",
        "image": "assets/images/signs/slippery_when_wet.png"
    },
    {
        "id": 25,
        "chapter": 7,
        "question": "What is the statewide statutory speed limit on rural expressways in Missouri, unless otherwise posted?",
        "options": ["55 mph", "60 mph", "65 mph", "70 mph"],
        "correctIndex": 2,
        "explanation": "In Missouri, the statutory speed limit on rural expressways is 65 mph. Rural interstates are 70 mph (or 75 where designated).",
        "rule": "Chapter 7, Page 52"
    },
    {
        "id": 26,
        "chapter": 7,
        "question": "What is the speed limit in any Missouri city, town, or village unless otherwise posted?",
        "options": ["15 mph", "25 mph", "30 mph", "35 mph"],
        "correctIndex": 1,
        "explanation": "The speed limit within any city, town, or village in Missouri is 25 mph unless a different speed limit is specifically posted.",
        "rule": "Chapter 7, Page 52"
    },
    {
        "id": 27,
        "chapter": 8,
        "question": "What is the recommended following distance behind the vehicle ahead under normal driving conditions?",
        "options": ["1-second rule", "2-second rule", "3-second rule", "5-car length rule"],
        "correctIndex": 2,
        "explanation": "Missouri Driver Guide strongly recommends the '3-Second Rule' under normal conditions, increasing to 4-5 seconds or more in bad weather, at high speeds, or behind large trucks.",
        "rule": "Chapter 8, Page 58"
    },
    {
        "id": 28,
        "chapter": 8,
        "question": "According to Missouri child passenger safety law, children must be secured in an approved booster seat until what age and weight?",
        "options": [
            "Age 4 and 40 pounds",
            "Age 6 and 60 pounds",
            "Age 8 or 80 pounds, or 4 feet 9 inches tall",
            "Age 12 and 100 pounds"
        ],
        "correctIndex": 2,
        "explanation": "Children less than 8 years old who weigh less than 80 pounds or are under 4'9\" tall must be appropriately secured in an approved booster seat.",
        "rule": "Chapter 8, Page 57"
    },
    {
        "id": 29,
        "chapter": 8,
        "question": "When are Missouri drivers required to use vehicle headlights?",
        "options": [
            "Only between midnight and sunrise",
            "From a half-hour after sunset to a half-hour before sunrise, and whenever wipers are in continuous use",
            "Only on unlighted highways",
            "Only when driving in dense fog"
        ],
        "correctIndex": 1,
        "explanation": "Headlights are required from a half-hour after sunset until a half-hour before sunrise, and anytime weather conditions require continuous use of windshield wipers.",
        "rule": "Chapter 8, Page 61"
    },
    {
        "id": 30,
        "chapter": 9,
        "question": "What should you do if your vehicle begins to hydroplane on a wet road?",
        "options": [
            "Slam on the brakes immediately",
            "Turn sharply towards the shoulder",
            "Gradually take your foot off the accelerator and hold the steering wheel straight without hard braking",
            "Shift into neutral and apply the emergency handbrake"
        ],
        "correctIndex": 2,
        "explanation": "If hydroplaning occurs, ease your foot off the gas pedal to allow vehicle weight to regain tire grip. Do not brake or make sudden steering maneuvers.",
        "rule": "Chapter 9, Page 66"
    },
    {
        "id": 31,
        "chapter": 10,
        "question": "What is the legal Blood Alcohol Concentration (BAC) limit for operating a motor vehicle for adult drivers (21 and older) in Missouri?",
        "options": [".02%", ".04%", ".05%", ".08%"],
        "correctIndex": 3,
        "explanation": "In Missouri, an adult driver 21 years of age or older is legally intoxicated with a BAC of .08% or higher.",
        "rule": "Chapter 10, Page 69"
    },
    {
        "id": 32,
        "chapter": 10,
        "question": "Under Missouri's 'Zero Tolerance' law, what BAC level will cause a driver under age 21 to lose their driving privilege?",
        "options": [".02% or higher", ".05% or higher", ".08% or higher", ".10% or higher"],
        "correctIndex": 0,
        "explanation": "Under Zero Tolerance, any minor under age 21 caught driving with a BAC of .02% or greater will have their driver license suspended or revoked.",
        "rule": "Chapter 10, Page 70"
    },
    {
        "id": 33,
        "chapter": 10,
        "question": "What does Missouri's 'Implied Consent' law mean?",
        "options": [
            "You consent to search of your vehicle at any time",
            "By driving on Missouri roadways, you automatically consent to a chemical test of your breath, blood, or saliva if suspected of DUI",
            "You agree to maintain auto insurance",
            "You agree to pay traffic tickets within 30 days"
        ],
        "correctIndex": 1,
        "explanation": "If you drive on Missouri public roads, you automatically give implied consent to submit to a chemical sobriety test. Refusal results in an immediate 1-year license revocation.",
        "rule": "Chapter 10, Page 71"
    },
    {
        "id": 34,
        "chapter": 11,
        "question": "At how many accumulated points within an 18-month period will your Missouri driver license be suspended?",
        "options": ["4 points", "6 points", "8 points", "12 points"],
        "correctIndex": 2,
        "explanation": "If you accumulate 8 or more points in 18 months, the Department of Revenue will suspend your driving privilege (30 days for 1st suspension, 60 days for 2nd, 90 days for 3rd).",
        "rule": "Chapter 11, Page 75"
    },
    {
        "id": 35,
        "chapter": 11,
        "question": "At how many accumulated points within 12 months will your Missouri driver license be revoked for one full year?",
        "options": ["8 points", "10 points", "12 points", "16 points"],
        "correctIndex": 2,
        "explanation": "If you accumulate 12 or more points in 12 months, 18 or more points in 24 months, or 24 or more in 36 months, your license will be revoked for one year.",
        "rule": "Chapter 11, Page 75"
    },
    {
        "id": 36,
        "chapter": 13,
        "question": "What are the minimum required limits for motor vehicle liability insurance in Missouri?",
        "options": [
            "$10,000 / $20,000 / $10,000",
            "$25,000 / $50,000 / $25,000",
            "$50,000 / $100,000 / $50,000",
            "$100,000 / $300,000 / $100,000"
        ],
        "correctIndex": 1,
        "explanation": "Missouri requires 25/50/25 liability coverage: $25,000 for bodily injury per person, $50,000 bodily injury per crash, and $25,000 for property damage.",
        "rule": "Chapter 13, Page 81"
    },
    {
        "id": 37,
        "chapter": 16,
        "question": "Under Missouri's Siddens Bening Hands-Free Law, what is strictly prohibited while operating a vehicle?",
        "options": [
            "Physically holding or supporting an electronic communication device with any part of the body",
            "Manually typing, reading text messages, or browsing social media",
            "Watching or recording videos",
            "All of the above"
        ],
        "correctIndex": 3,
        "explanation": "Under SB 398 (Siddens Bening Hands-Free Law), all drivers are prohibited from physically holding a phone, texting, viewing videos, or typing while driving. Only hands-free voice operations or dashboard mounts are permitted.",
        "rule": "Chapter 16, Page 94"
    },
    {
        "id": 38,
        "chapter": 18,
        "question": "What is required under Missouri's 'Move Over' law when approaching an emergency vehicle or road maintenance vehicle with flashing lights stopped on the shoulder?",
        "options": [
            "Maintain your speed and honk to alert workers",
            "Safely vacate the lane closest to the stopped vehicle if driving on a multi-lane highway, or slow down if a lane change is unsafe",
            "Stop completely in the travel lane",
            "Move onto the left shoulder"
        ],
        "correctIndex": 1,
        "explanation": "The Move Over law requires motorists to change lanes into a lane not adjacent to the stopped emergency or maintenance vehicle, or slow down cautiously if unable to change lanes safely.",
        "rule": "Chapter 18, Page 100"
    },
    {
        "id": 39,
        "chapter": 7,
        "question": "What does a solid double yellow line down the center of a two-lane road mean?",
        "options": [
            "Passing is allowed in both directions",
            "Passing is prohibited in both directions",
            "Passing is allowed only during daylight hours",
            "It marks a shared left-turn lane"
        ],
        "correctIndex": 1,
        "explanation": "A solid double yellow line indicates that passing is prohibited in both directions. You may only cross it to make a left turn into a driveway or private road.",
        "rule": "Chapter 7, Page 44"
    },
    {
        "id": 40,
        "chapter": 7,
        "question": "What does a broken yellow centerline next to a solid yellow centerline indicate?",
        "options": [
            "Passing is permitted from both directions",
            "Passing is permitted only for drivers traveling on the side with the broken line",
            "Passing is prohibited for all vehicles",
            "The road is one-way"
        ],
        "correctIndex": 1,
        "explanation": "Vehicles adjacent to the broken line may pass when safe. Vehicles on the side with the solid yellow line may NOT pass.",
        "rule": "Chapter 7, Page 44"
    }
]

print(f"Generated {len(PRACTICE_QUESTIONS)} exam questions.")

# -------------------------------------------------------------
# 6. Save data.js and guide_data.json
# -------------------------------------------------------------
print("Step 6: Writing data bundles...")

full_export = {
    "version": "2026.1",
    "title": "Missouri Driver Guide",
    "subtitle": "Interactive Study Portal & Examination Simulator",
    "source_pdf": "Driver Guide (Revised August 2026)",
    "publisher": "Missouri Department of Revenue (DOR)",
    "total_pages": total_pages,
    "chapters": chapters_data,
    "figures": cropped_catalog,
    "questions": PRACTICE_QUESTIONS,
    "pages_meta": page_metadata
}

json_path = os.path.join(BASE_DIR, "guide_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(full_export, f, indent=2)

# Write data.js for seamless offline browser execution without CORS restrictions
js_path = os.path.join(BASE_DIR, "data.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write("// Missouri Driver Guide Data Bundle (Offline & Client-side Ready)\n")
    f.write("window.MISSOURI_GUIDE_DATA = ")
    json.dump(full_export, f)
    f.write(";\n")

print(f"Exported guide_data.json ({os.path.getsize(json_path)/1024/1024:.2f} MB)")
print(f"Exported data.js ({os.path.getsize(js_path)/1024/1024:.2f} MB)")
print("Extraction and cataloging complete!")
