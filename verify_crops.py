#!/usr/bin/env python3
"""
Inspect, precisely calibrate, and extract all Missouri Driver Guide road signs,
shapes, work zone signs, and driving diagrams.
"""

import os
import fitz
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Driver_Guide.pdf")
SIGNS_DIR = os.path.join(BASE_DIR, "assets", "images", "signs")
DIAGRAMS_DIR = os.path.join(BASE_DIR, "assets", "images", "diagrams")
EXTRACTED_DIR = os.path.join(BASE_DIR, "assets", "images", "extracted")

os.makedirs(SIGNS_DIR, exist_ok=True)
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

doc = fitz.open(PDF_PATH)

# Definitive, verified coordinates list:
# (id, page_idx, x0, y0, x1, y1, category, title, description)
SIGNS_CONFIG = [
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
    ("rest_area", 55, 227, 99, 271, 133, "guide", "Rest Area", "Highway rest area facilities ahead."),
    ("interstate_shield", 55, 58, 450, 93, 485, "guide", "Interstate Route Shield (I-70)", "Red, white, and blue shield indicating Interstate highway."),
    ("business_loop", 55, 98, 450, 133, 485, "guide", "Business Loop Shield (Loop 44)", "Green shield for business loop through commercial area."),
    ("us_route_shield", 55, 138, 450, 173, 485, "guide", "US Highway Shield (US-36)", "Black and white shield indicating Federal US Highway."),
    ("missouri_route_shield", 55, 178, 450, 213, 485, "guide", "Missouri State Route (Route 5)", "Missouri state route highway marker."),
    ("county_road", 55, 218, 450, 253, 485, "guide", "County Lettered Road (Route A)", "Missouri secondary lettered highway."),
    ("emergency_marker", 55, 280, 485, 345, 575, "guide", "Emergency Reference Marker", "Provides route, direction, and milepost for dispatchers."),

    # -------------------------------------------------------------
    # Maneuver & Driving Diagrams (Various Pages)
    # -------------------------------------------------------------
    ("school_bus_stopping", 25, 212, 36, 344, 98, "diagram", "School Bus Stop Law", "When to stop on 2-lane vs 4-lane divided roads."),
    ("turn_right_diagram", 26, 233, 102, 338, 226, "diagram", "Right Turn Position", "Approach and complete turns close to the right curb."),
    ("turn_left_2way_diagram", 26, 232, 225, 341, 351, "diagram", "Left Turn: 2-Way to 2-Way", "Turn before the center of the intersection into left lane."),
    ("turn_left_1way_diagram", 26, 232, 363, 339, 474, "diagram", "Left Turn: 2-Way to 1-Way", "Turn from nearest left lane into nearest left lane of 1-way."),
    ("roundabout_navigation", 27, 203, 158, 337, 214, "diagram", "Roundabout Flow", "Yield to traffic already in roundabout; circulate counter-clockwise."),
    ("driver_hand_signals", 28, 197, 333, 344, 381, "diagram", "Driver Hand Signals", "Arm positions for Left Turn, Right Turn, and Slow/Stop."),
    ("bicycle_hand_signals", 30, 169, 279, 342, 333, "diagram", "Bicycle Hand Signals", "Standard signaling conventions for cyclists."),
    ("truck_no_zones", 31, 294, 151, 338, 244, "diagram", "Truck No-Zone Blind Spots", "Front, rear, and wide side blind spots of semi-trucks."),
    ("parallel_parking_steps", 37, 98, 271, 280, 338, "diagram", "Parallel Parking 3 Steps", "Reverse angle, straighten, and center inside 18 inches."),
    ("parking_on_hills", 37, 116, 458, 260, 573, "diagram", "Hill Parking Wheel Directions", "Turn wheels toward curb downhill, away from curb uphill."),
    ("highway_acceleration_lane", 38, 216, 361, 340, 480, "diagram", "Entering Freeway via Acceleration Lane", "Match highway speed and merge smoothly."),
    ("traffic_light_signals", 45, 303, 73, 338, 437, "diagram", "Traffic Light Sequences", "Solid red, yellow, green, and flashing left turn phases."),
    ("child_safety_seats", 59, 103, 272, 276, 376, "diagram", "Child Passenger Restraints", "Rear-facing infant seat, booster seat, and seat belt guidelines.")
]

print(f"Beginning calibrated extraction of {len(SIGNS_CONFIG)} signs and diagrams...")

output_catalog = []
for name, pno, x0, y0, x1, y1, cat, title, desc in SIGNS_CONFIG:
    target_dir = SIGNS_DIR if cat in ["shapes", "warning", "regulatory", "workzone", "guide"] else DIAGRAMS_DIR
    out_file = os.path.join(target_dir, f"{name}.png")
    page = doc[pno]
    rect = fitz.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(clip=rect, dpi=200)
    pix.save(out_file)

    # Validate image quality
    im = Image.open(out_file).convert("RGB")
    pixels = list(im.getdata())
    non_white = sum(1 for p in pixels if not (p[0] > 240 and p[1] > 240 and p[2] > 240))
    pct = (non_white / len(pixels)) * 100

    if pct < 5.0:
        print(f"⚠️  WARNING: {name} might be blank! ({pct:.1f}% non-white)")
    else:
        print(f"✓  {name} ({pix.width}x{pix.height}, {pct:.1f}% visual content)")

    rel_path = os.path.relpath(out_file, BASE_DIR)
    output_catalog.append({
        "id": name,
        "title": title,
        "description": desc,
        "category": cat,
        "page": pno + 1,
        "image": rel_path,
        "width": pix.width,
        "height": pix.height
    })

print(f"\nAll {len(output_catalog)} images processed and verified.")
