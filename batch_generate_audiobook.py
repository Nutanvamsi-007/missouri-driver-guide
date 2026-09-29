#!/usr/bin/env python3
"""
Batch Audio Studio Generator for Missouri Driver Guide.
Generates studio-grade AI neural audio for all handbook chapters:
1. High-Yield Exam Cram Podcast (Guy Neural - broadcast exam cram)
2. Comprehensive Chapter Narration (Jenny Neural - articulate educator)
"""

import os
import asyncio
import edge_tts

OUTPUT_DIR = "/Users/nutanvamsigunti/workspace/missouri-driver-guide/assets/audio/chapters"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHAPTERS = {
    "intro": {
        "title": "Welcome & Missouri Driver Examination Overview",
        "cram": """
Welcome to the Missouri Driver Guide Exam Cram Overview. Here is what you need to know about the official examination before you begin studying.

Number one: The Examination Structure.
The Missouri written driver examination consists of 25 multiple-choice questions. To pass, you must correctly answer at least 20 questions, which is an 80 percent passing score. Every question is taken directly from the Missouri Driver Guide. There are no trick questions.

Number two: The Four-Part Driver Examination.
New drivers must pass four distinct tests:
First: The Vision Test, requiring at least 20/40 visual acuity.
Second: The Road Sign Recognition Test, identifying signs by shape, color, and symbol without words.
Third: The Written Knowledge Test of 25 questions.
And fourth: The Driving Skills Road Test, conducted by a Missouri State Highway Patrol examiner.

Number three: Key Test Mindset.
Your driving examiner rides with you only to evaluate vehicle control and compliance with Missouri traffic laws. They will never ask you to do anything illegal or unsafe. Relax, scan your mirrors constantly, use turn signals 100 feet before turns, and make complete stops at every stop sign. Let's begin Chapter 1!
""",
        "narration": """
Welcome to the Missouri Driver Guide, published by the Missouri Department of Revenue. This guide is your complete roadmap to understanding Missouri motor vehicle laws, safe driving practices, and licensing requirements.

Whether you are a first-time teen driver earning your instruction permit, a new resident transferring your license to Missouri, or an experienced driver brushing up on current statutes, this portal provides interactive study tools, flashcards, audio narration, and realistic exam simulators.

To earn your Missouri driver license, you will take a 25-question written exam administered by the Missouri State Highway Patrol. You must score 80 percent, or 20 correct answers out of 25, to pass. All questions are derived directly from the chapters in this guide.

Studying this material carefully will build your driving confidence, protect lives on Missouri highways, and ensure you pass your licensing exam on your very first attempt. Let's explore the rules of the road together.
"""
    },
    "chapter-1": {
        "title": "The Missouri Driver License",
        "cram": """
Welcome to the Missouri Driver Guide High-Yield Cram Session for Chapter 1: The Missouri Driver License. Here are the top tested facts, ages, and rules you must know to pass your 25-question permit exam.

Rule number one: The Instruction Permit age.
You are eligible for an Instruction Permit at age 15. You must pass the vision, road sign, and written tests. While holding this permit, you must complete at least 40 hours of supervised driving practice, with at least 10 hours completed at night.

Rule number two: Moving to the Intermediate License.
You are eligible at age 16. But here are the test conditions: You must have held your instruction permit for a minimum of six months, or 182 days. You must have had no alcohol-related convictions in the last twelve months, and no traffic convictions in the last six months. Then, you must pass the on-the-road driving skills test.

Rule number three: Intermediate License Restrictions. Pay close attention here, as this is on almost every state exam.
First, the Nighttime Curfew: You cannot drive between 1:00 AM and 5:00 AM unless accompanied by a licensed adult age 21 or older, or if you are driving directly to or from school, work, or in an emergency.
Second, the Passenger Rule: For the first six months, you may carry only one passenger under age 19 who is not an immediate family member. After the first six months, you may carry up to three passengers under age 19.
Third, Seatbelts: Seatbelts are mandatory for everyone in the vehicle under Missouri's Click It or Ticket law.

Rule number four: Full Under-21 Driver License.
At age 18, you may apply for a full Class F driver license. All under-21 licenses in Missouri are issued with a vertical format to immediately identify minors.

Finally, Rule number five: REAL ID Requirements.
When applying for a REAL ID-compliant license, you must present four things: Proof of identity and lawful status, proof of your Social Security Number, and two separate documents verifying your Missouri residential address.

Master these numbers: Age 15 for permit, 40 hours total with 10 hours at night, 6 months minimum hold time, Age 16 for intermediate, and the 1:00 AM to 5:00 AM curfew. You are now prepared for Chapter 1 exam questions!
""",
        "narration": """
Welcome to Chapter 1 of the official Missouri Driver Guide: The Missouri Driver License.

In this chapter, you will learn who needs a Missouri driver license, how the Graduated Driver License program works for new drivers, and the exact documents required at the license office.

First, let's look at who must have a Missouri driver license.
Anyone who operates a motor vehicle on public roads in Missouri is required by law to have a valid driver license. You must obtain a Missouri license if:
Number one: You live in Missouri, are 16 years of age or older, and plan to drive.
Number two: You are a new resident of Missouri, even if you already hold a valid license from another state.
And number three: You are an out-of-state commercial driver moving to Missouri.

You do not need a Missouri license if you are an active-duty member of the armed forces with a valid home-state license, or a full-time student temporarily attending school in Missouri.

Now, let's examine the Graduated Driver License program. This is one of the most frequently tested topics on the Missouri permit exam.

Step One is the Instruction Permit, available at age 15.
To receive an instruction permit, you must pass the vision test, the road sign recognition test, and the written knowledge examination.
When driving with an instruction permit, you cannot drive alone. You must always be accompanied by a licensed parent, grandparent, legal guardian, or a qualified driving instructor. You may also drive with another licensed driver who is at least 25 years old and has held a valid license for at least three years, provided you have written permission from your parent or guardian.

Before you can advance to the next step, Missouri law requires you to complete at least 40 hours of supervised driving instruction. And remember this for your exam: at least 10 of those 40 hours must be completed at night, between sunset and sunrise.
"""
    },
    "chapter-2": {
        "title": "The Driver Examination",
        "cram": """
Welcome to the High-Yield Exam Cram for Chapter 2: The Driver Examination. Here are the core numbers and failure conditions tested on the permit exam.

Fact number one: Vision Requirements.
To qualify for an unrestricted driver license in Missouri, you must demonstrate a visual acuity of at least 20/40 with either eye or both eyes combined. If your vision is between 20/41 and 20/70, you may be restricted to daylight driving only or referred to a vision specialist.

Fact number two: Road Sign and Written Passing Scores.
The written knowledge test has 25 multiple-choice questions. You must score at least 80 percent, which means answering 20 questions correctly. The road sign test evaluates your ability to recognize traffic signs by their shape and color alone without reading text.

Fact number three: Vehicle Inspection Before Skills Test.
Before your road test begins, the Highway Patrol examiner inspects your test vehicle. Your vehicle must have a valid license plate, proof of financial responsibility insurance, functioning headlights, brake lights, turn signals, horn, clean windshield with wipers, rearview mirror, and working seatbelts. If any of these fail, your test will be canceled.

Fact number four: Automatic Driving Test Failures.
You will immediately fail the road test if you commit any of the following four critical errors:
1. Being involved in any preventable traffic accident.
2. Committing any dangerous action that causes the examiner to take control of the wheel or brake.
3. Violating any Missouri traffic law, such as running a red light, speeding, or failing to stop at a stop sign.
4. Refusing to follow the examiner's instructions.

Remember: 20/40 vision, 20 out of 25 on the written test, and zero traffic violations during your skills exam!
""",
        "narration": """
Chapter 2 covers the Missouri Driver Examination process administered by the Missouri State Highway Patrol. The examination ensures that every licensed driver possesses the vision, knowledge, and physical skill required to operate safely on public highways.

The examination consists of four distinct components:
First is the Vision Screening. You will look through an optical device to measure your visual sharpness and peripheral field of vision. Missouri standards require 20/40 vision or better for an unrestricted license. If you require corrective lenses to meet this standard, your license will carry a restriction code requiring glasses or contact lenses whenever you drive.

Second is the Highway Road Sign Test. You must identify traffic regulatory, warning, and guide signs by recognizing their geometric shapes and background colors.

Third is the Written Knowledge Test. This computer-based exam contains 25 questions testing your knowledge of Missouri traffic laws, safe following distances, point penalties, and right-of-way rules. You must answer at least 20 questions correctly to pass.

The fourth component is the Driving Skills Road Test. You must provide a properly insured, registered, and safe vehicle. During the road test, the examiner will observe your starting, backing, parallel parking, intersection control, speed management, and adherence to traffic signals.
"""
    },
    "chapter-3": {
        "title": "Rules of the Road",
        "cram": """
Welcome to the Chapter 3 Cram Session: Rules of the Road. This chapter has the highest number of questions on the Missouri exam. Pay close attention to these statutory speeds and right-of-way rules!

Rule number one: Statutory Speed Limits. Memorize these exact numbers:
- Rural Interstates and Freeways: 70 miles per hour.
- Rural Expressways: 65 miles per hour.
- Urban Interstates, Freeways, and Expressways: 60 miles per hour.
- State-divided highways: 60 miles per hour.
- Undivided state highways: 55 miles per hour.
- County lettered roads: 45 miles per hour, unless posted otherwise.

Rule number two: Four-Way Stop Intersections.
Who goes first?
First rule: The first vehicle to reach the intersection and come to a complete stop has the right-of-way.
Second rule: If two vehicles arrive at the exact same time, the driver on the left must yield to the driver on the right.
Third rule: If two vehicles arrive opposite each other, a driver turning left must yield to oncoming traffic going straight.

Rule number three: School Buses. This is a guaranteed test question!
When a school bus stops and displays flashing red lights and an extended stop arm:
On a two-lane road or undivided highway: Drivers traveling in BOTH directions must come to a complete stop at least 20 feet from the bus.
On a divided highway with a physical median, barrier, or unpaved space: ONLY drivers traveling in the SAME direction as the bus must stop. Drivers traveling in the opposite direction on the other side of the median may proceed.

Rule number four: Emergency Vehicles and the Move Over Law.
When an emergency vehicle approaches with sirens or flashing lights, immediately pull over to the right edge of the road and stop.
When passing a stationary emergency vehicle or maintenance vehicle on the shoulder, Missouri's Move Over Law requires you to move over into an adjacent lane if safe to do so. If you cannot change lanes, you must slow down and proceed with caution.

Remember: 70 on rural interstates, yield to the right at four-way stops, both directions stop for school buses unless physically divided, and move over for emergency vehicles!
""",
        "narration": """
Chapter 3 outlines the fundamental Rules of the Road in Missouri. Traffic laws are designed to create orderly, predictable vehicle movement and protect all highway users.

Missouri's Basic Speed Law requires you to operate at a careful and prudent speed, taking into account traffic density, road surface conditions, weather, and visibility. Even if the posted speed limit is 60 miles per hour, driving at 60 during a heavy rainstorm or dense snow may be cited as careless and imprudent driving.

Understanding Right-of-Way is essential. Right-of-way is something you give to others to avoid collisions; no law grants you absolute right-of-way. At uncontrolled intersections, yield to vehicles already in the intersection and to drivers on your right. When entering a traffic roundabout, always yield to traffic circulating counter-clockwise inside the circle.

When signaling turns, Missouri law requires you to activate your turn signal at least 100 feet before making a turn or changing lanes. If your electric turn signals fail, use hand signals: arm extended straight out for a left turn, arm bent upward at the elbow for a right turn, and arm pointed down toward the ground for slowing down or stopping.
"""
    },
    "chapter-4": {
        "title": "Sharing the Road",
        "cram": """
Welcome to the Chapter 4 Cram Session: Sharing the Road with commercial trucks, motorcycles, bicycles, and trains.

Topic number one: Commercial Truck 'No-Zones'.
Large commercial trucks have massive blind spots known as the No-Zone:
- In front of the truck: Up to 20 feet.
- Behind the truck: Up to 200 feet.
- Along both sides: Especially the right side, which extends across multiple lanes.
Memorize this golden rule for your test: If you cannot see the truck driver's face in their side mirror, the truck driver cannot see you! Also, never squeeze between a turning truck and the curb, because trucks must swing wide to make right turns.

Topic number two: Bicycles.
Under Missouri law, bicycles are legal vehicles with full rights to use public roadways. When passing a bicyclist traveling in the same direction, you must give them at least 3 feet of safe clearance.

Topic number three: Railroad Crossings.
When red warning lights are flashing, bells are clanging, or crossbuck signals indicate an approaching train, Missouri law requires you to stop between 15 feet and 50 feet from the nearest rail. Never stop on the tracks, never drive around lowered crossing gates, and remember that trains cannot stop quickly.

Topic number four: Pedestrians.
Always yield to pedestrians crossing at marked or unmarked crosswalks. When you see a pedestrian carrying a white cane or accompanied by a guide dog, they are visually impaired; you must come to a complete stop and yield the right-of-way immediately.

Remember: 3 feet clearance for bicycles, 15 to 50 feet stop at railroad tracks, avoid truck No-Zones, and stop completely for white canes!
""",
        "narration": """
Chapter 4 emphasizes the vital responsibility of sharing Missouri roadways safely with commercial trucks, buses, motorcyclists, bicyclists, and pedestrians.

Commercial motor vehicles require significantly greater stopping distances than passenger cars. A fully loaded tractor-trailer traveling at 55 miles per hour takes nearly 300 feet to stop, which is the length of an entire football field. Always maintain a generous four-second following cushion behind large trucks, and never cut abruptly in front of a truck when passing.

Motorcyclists have the same rights and privileges as other motorists, but their smaller size makes them harder to see and judge for speed and distance. Always check your mirrors and turn your head to scan your blind spots before changing lanes, especially at intersections where half of all motorcycle-car collisions occur.

Bicyclists are legally entitled to use Missouri roads and must obey the same traffic signals and signs as motor vehicles. When passing a bicycle, provide a minimum clearance cushion of 3 feet, and reduce your speed to prevent wind turbulence from destabilizing the rider.
"""
    },
    "chapter-5": {
        "title": "Parking",
        "cram": """
Welcome to the Chapter 5 Cram Session: Parking Rules and Hill Parking. Hill parking directions are among the most frequently missed questions on the Missouri exam!

Rule number one: Parking on Hills. Memorize these exact wheel directions:
- Downhill with a curb: Turn your front wheels TOWARD the curb, to the right.
- Uphill with a curb: Turn your front wheels AWAY from the curb, to the left. That way, if your brakes fail, your front tire rolls into and blocks against the curb.
- Uphill or Downhill WITHOUT a curb: Turn your front wheels TOWARD the edge of the road, to the right.
A great memory trick: The ONLY time you turn your wheels away from the curb to the left is Uphill with a Curb! Every other hill condition, turn to the right!

Rule number two: Prohibited Parking Distances. Memorize these distances:
- 15 feet: Do not park within 15 feet of a fire hydrant.
- 20 feet: Do not park within 20 feet of a crosswalk at an intersection.
- 30 feet: Do not park within 30 feet of any stop sign, yield sign, or traffic control signal.
- 50 feet: Do not park within 50 feet of the nearest rail of a railroad crossing.

Rule number three: Parallel Parking.
When parallel parking along a curb, your vehicle must be parked parallel to and within 12 inches of the curb.

Remember: Wheels to the left ONLY uphill with curb; 15 feet from hydrants, 20 feet from crosswalks, 30 feet from stop signs, and 12 inches from the curb!
""",
        "narration": """
Chapter 5 covers parking regulations, hill parking safety, and parallel parking procedures. Proper parking prevents runaway vehicles, maintains clear visibility at intersections, and preserves pedestrian walkways.

When parking on hills, always set your emergency parking brake firmly and place your transmission in Park, or in Reverse if driving a manual transmission. Your front wheels must be angled so that if the brake fails, the vehicle will roll away from traffic lanes:
When parking facing downhill with a curb, turn wheels toward the curb.
When parking facing uphill with a curb, turn wheels away from the curb to the left, allowing the back of your front tire to brace against the concrete curb.
If parking on any hill without a curb, always angle your wheels toward the shoulder to the right.

Missouri law prohibits parking where your vehicle obstructs emergency services or blocks sightlines: keep 15 feet clear of fire hydrants, 20 feet from crosswalks, and 30 feet from stop signs and signals. When parallel parking on city streets, ensure your vehicle is within 12 inches of the curb.
"""
    },
    "chapter-6": {
        "title": "Highway Driving",
        "cram": """
Welcome to the Chapter 6 Cram Session: Interstate and Highway Driving.

Concept number one: Entering the Highway.
When entering an interstate via an on-ramp, use the acceleration lane to match your speed to the flow of highway traffic before merging smoothly into an open gap. Never stop on an acceleration lane unless traffic is so heavy there is physically no space to enter.

Concept number two: Exiting the Highway.
Never slow down on the main highway lanes. Signal early, move into the deceleration lane at full speed, and then brake smoothly within the deceleration ramp to reach the posted exit advisory speed limit.

Concept number three: Velocitizing.
Velocitizing is a dangerous optical and sensory illusion that occurs after driving at high speeds for prolonged periods. When exiting the freeway onto city streets, you will feel like you are traveling much slower than you actually are. Always check your speedometer when exiting to verify your true speed.

Concept number four: Highway Hypnosis.
Highway hypnosis is a trance-like state of drowsiness caused by staring at monotonous, unchanging pavement for hours. To prevent highway hypnosis, avoid staring straight ahead; keep your eyes moving, scan mirrors every 5 to 10 seconds, open windows for fresh air, and stop to stretch and rest at least every 100 miles or two hours.

Concept number five: Highway Emergencies.
If your vehicle breaks down on an interstate, pull completely off the travel lanes onto the right shoulder. Turn on your four-way hazard flashers and tie a white cloth to your driver's side door handle or antenna to signal for help.

Remember: Match highway speed in the acceleration lane, watch for velocitizing at exits, scan eyes to fight highway hypnosis, and stay buckled on the shoulder!
""",
        "narration": """
Chapter 6 focuses on high-speed expressway and interstate driving. Multi-lane highways are mathematically the safest roads per mile driven, but their high operating speeds make split-second decisions critical.

Entering an interstate requires using the full length of the acceleration lane to match the speed of oncoming expressway traffic. Signal your intention, check your rearview and side mirrors, glance over your shoulder to verify your blind spot, and merge seamlessly into the flow.

On highways with three or more lanes traveling in the same direction, the right lane is for slower traffic, entering, and exiting. The middle lane is for general through-travel, and the far left lane is reserved for passing and higher-speed travel. Never cruise indefinitely in the left lane if you are obstructing faster traffic.

Long-distance highway travel introduces physical fatigue and sensory dulness, commonly called Highway Hypnosis. Protect yourself by shifting your visual focus, taking active breaks every two hours, and recognizing that exit ramps demand immediate speed reductions.
"""
    },
    "chapter-7": {
        "title": "Pavement Markings, Traffic Signs, and Signals",
        "cram": """
Welcome to the Chapter 7 Cram Session: Traffic Signs, Shapes, Colors, and Pavement Markings. This is the largest visual section of the Missouri permit exam!

Part one: Sign Colors and Their Meanings.
- Red: Stop, yield, or prohibited action.
- Yellow: General warning of road hazards ahead.
- White and Black: Regulatory laws and speed limits.
- Orange: Highway construction and maintenance work zones.
- Green: Directional guidance and highway mileage.
- Blue: Motorist services such as food, fuel, lodging, and hospitals.
- Brown: Public recreation areas and state parks.
- Fluorescent Yellow-Green: School zones, school crossings, and pedestrian areas.

Part two: Sign Shapes. Memorize these shapes without words:
- Octagon: Stop.
- Equilateral Triangle: Yield.
- Round Circle: Railroad crossing advance warning.
- Diamond: Warning of physical road conditions ahead.
- Pentagon: School zone or school crossing.
- Pennant: No Passing Zone, posted on the left side of the road facing oncoming drivers.
- Vertical Rectangle: Regulatory rule, such as speed limit.

Part three: Pavement Markings.
- Yellow lines: Separate traffic traveling in OPPOSITE directions.
- White lines: Separate lanes of traffic traveling in the SAME direction.
- Broken lines: Passing or lane changing is permitted when safe.
- Solid lines: Passing is prohibited or lane changing is discouraged.
- Double solid yellow lines: Passing is strictly prohibited in BOTH directions.
- Reversible center turn lanes: Solid yellow exterior line with broken yellow interior line on both sides; used strictly for making left turns, never for passing or driving down.

Part four: Traffic Signals.
A flashing red light means the exact same thing as a stop sign: come to a complete stop, yield to cross traffic, and proceed when clear. A flashing yellow light means slow down, proceed with caution, and be prepared to stop.

Remember: Pennant means No Passing on the left; yellow separates opposite traffic, white separates same direction; and flashing red equals a stop sign!
""",
        "narration": """
Chapter 7 is your definitive guide to Missouri's road sign catalog, traffic light sequences, and pavement striping standards. Uniform traffic control devices provide consistent visual instructions across the United States.

Traffic signs are categorized into three primary classes:
Regulatory Signs enforce legal requirements, such as speed limits, stop signs, yield controls, and one-way directives. Ignoring a regulatory sign is a moving violation subject to fines and driving record points.
Warning Signs alert drivers to physical roadway features, upcoming curves, intersections, lane merges, and steep grades. They are diamond-shaped with bold black symbols on yellow or fluorescent backgrounds.
Guide Signs convey information regarding routes, exits, destinations, rest areas, and hospital facilities.

Pavement markings guide lane positioning. Always remember that yellow lines divide opposing streams of traffic. If a broken yellow line is on your side of the lane, you may cross it to pass slower vehicles when the oncoming lane is clear. A solid yellow line on your side indicates that sightlines are restricted, and passing is strictly forbidden by Missouri law.
"""
    },
    "chapter-8": {
        "title": "Safe Driving Tips For Everyday Driving",
        "cram": """
Welcome to the Chapter 8 Cram Session: Safe Driving Tips and Essential Equipment Rules.

Fact number one: Missouri Seatbelt Laws.
Under Missouri's Click It or Ticket law, seatbelts are mandatory for all front-seat occupants and all passengers between 8 and 16 years of age anywhere in the vehicle.
Child Restraint Law:
- Children under age 4, or weighing under 40 pounds, must be secured in an approved, crash-tested child safety seat.
- Children age 4 through 7, who weigh at least 40 pounds but less than 80 pounds, and are under 4 feet 9 inches tall, must be secured in a booster seat.

Fact number two: The 3-Second Following Distance Rule.
Under normal dry conditions, maintain at least a 3-second following distance behind the vehicle in front of you. Pick a fixed marker like an overhead sign. When the rear bumper of the car ahead passes the marker, count: one-thousand-one, one-thousand-two, one-thousand-three. If your front bumper passes before you finish counting, you are tailgating! Increase this distance to 4 or 5 seconds in rain, fog, or snow.

Fact number three: Headlight Laws.
Missouri law requires your headlights to be turned on:
1. From one-half hour after sunset until one-half hour before sunrise.
2. Any time weather conditions require continuous operation of your windshield wipers.
Remember: Wipers on, lights on!

Fact number four: Dimming High Beams.
You must dim your high-beam headlights to low beams:
- Within 500 feet of any approaching oncoming vehicle.
- Within 300 feet when following behind another vehicle.

Remember: 3-second rule for following, wipers on equals lights on, dim high beams at 500 feet oncoming and 300 feet following, booster seats under 8 years and 80 pounds!
""",
        "narration": """
Chapter 8 provides practical defensive driving strategies, stopping distance calculations, and occupant restraint laws. Defensive driving means anticipating hazards, maintaining visual cushions, and compensating for the mistakes of other drivers.

Proper safety belt usage reduces the risk of fatal injury by 45 percent. In a collision, your seatbelt keeps you positioned behind the steering controls, prevents you from being thrown into other passengers or against the vehicle frame, and stops ejection through windshields or doors.

Vehicle stopping distance is the sum of two factors: Reaction Distance and Braking Distance. At 55 miles per hour, your vehicle travels approximately 60 feet during the three-quarters of a second it takes your brain to recognize a hazard and move your foot to the brake pedal. It then takes another 140 feet of braking on dry pavement to stop completely, for a total stopping distance of over 200 feet.

To maintain a safe stopping buffer, use the 3-Second Following Rule under ideal driving conditions. In poor weather, at night, or when following motorcycles and large trucks, double your following margin to ensure you always have an escape path.
"""
    },
    "chapter-9": {
        "title": "Safe Driving Tips For Special Driving Conditions",
        "cram": """
Welcome to the Chapter 9 Cram Session: Special Driving Conditions, Hydroplaning, and Emergency Recoveries.

Topic number one: Hydroplaning.
Hydroplaning occurs when water on the roadway accumulates in front of your tires faster than your tire treads can channel it away, causing your vehicle to ride on a thin film of water with zero traction.
- It can begin at speeds as low as 35 miles per hour and becomes severe above 55 miles per hour.
- If your vehicle hydroplanes: Take your foot off the gas pedal immediately. Do NOT slam on your brakes, and do NOT turn your steering wheel violently. Hold the wheel straight and let the vehicle decelerate until tire grip returns.

Topic number two: Winter Driving.
- Bridges and overpasses freeze before ordinary roadway surfaces because cold air circulates both above and underneath the bridge deck.
- Never use cruise control on wet, icy, or snow-covered roads.

Topic number three: Fog.
Always drive with your LOW-beam headlights or fog lights in dense fog. Never use your high beams; high beams reflect off water droplets in the fog, creating a blinding wall of glare that eliminates forward visibility.

Topic number four: Tire Blowout Recovery.
If a tire suddenly bursts:
1. Grip the steering wheel firmly with both hands.
2. Keep the vehicle traveling straight.
3. Gently ease your foot off the accelerator.
4. Do NOT brake immediately. Wait until your speed drops below 30 miles per hour, then brake gently and pull safely off the roadway.

Topic number five: Brake Failure.
If your brake pedal drops straight to the floor:
1. Rapidly pump the brake pedal to build up hydraulic pressure.
2. Shift your transmission into a lower gear.
3. Gently apply your emergency parking brake while holding the release lever.

Remember: Hydroplaning starts at 35 miles per hour; never brake during a skid or blowout; use low beams in fog; and bridges freeze first!
""",
        "narration": """
Chapter 9 addresses challenging environmental conditions and mechanical vehicle emergencies. Adverse weather requires reduced speed, increased following buffers, and heightened visual awareness.

Rain dramatically decreases road friction, especially during the first 10 to 15 minutes of a downpour, when rainwater mixes with accumulated roadway oil, grease, and rubber residue to form a slick emulsified film. As speeds increase, tires can hydroplane completely off the road surface.

Winter driving demands gentle, progressive control inputs. Accelerate smoothly, avoid sudden steering transitions, and brake well in advance of turns. Black ice is an invisible, transparent coating of ice on asphalt that creates extreme skidding hazards, particularly on shaded road segments and elevated bridge structures.

If your vehicle begins to skid, remain calm: release the accelerator and brake pedals, and steer smoothly in the direction you want the front of the vehicle to travel. Avoid over-correcting, which can trigger an uncontrollable secondary fishtail skid.
"""
    },
    "chapter-10": {
        "title": "Alcohol, Drugs, and Driving",
        "cram": """
Welcome to the Chapter 10 Cram Session: Alcohol, Drugs, and Driving. This chapter contains strict statutory penalties that are heavily tested on the Missouri exam.

Rule number one: Legal Blood Alcohol Concentration Limits. Memorize these three BAC thresholds:
1. Adult Drivers age 21 and older: 0.08 percent.
2. Commercial Drivers holding a CDL: 0.04 percent.
3. Minor Drivers under age 21: 0.02 percent, under Missouri's Zero Tolerance and Abuse and Lose laws.

Rule number two: Missouri's Implied Consent Law.
By driving a motor vehicle on public roads in Missouri, you are legally deemed to have given your consent to submit to chemical tests of your breath, blood, or urine if an officer suspects you of impaired driving.
If you refuse to take a chemical test:
- Your driver license will be revoked immediately for one full year.
- Evidence of your refusal can be used against you in a criminal court.

Rule number three: First Offense DWI Penalties.
A first-offense conviction for Driving While Intoxicated is a Class B misdemeanor:
- Up to 6 months in county jail.
- Fines up to 1,000 dollars.
- 8 points assessed against your driving record, resulting in an automatic 30-day suspension followed by a 60-day restricted driving period.
- Mandatory installation of an Ignition Interlock Device on your vehicle.

Rule number four: Minor Abuse and Lose Law.
If you are under 21 and convicted of possessing or consuming alcohol or drugs, even if you were not operating a motor vehicle at the time, your driving privileges will be suspended for 90 days for a first offense and revoked for one full year for a second offense.

Remember: 0.08 for adults, 0.04 for commercial, 0.02 for minors; refusing chemical test equals 1-year revocation; first DWI adds 8 points!
""",
        "narration": """
Chapter 10 details Missouri's comprehensive statutory framework regarding driving under the influence of alcohol, illicit drugs, and impairing prescription medications. Impaired driving remains the leading contributing factor in severe and fatal highway crashes.

Alcohol is a central nervous system depressant that degrades driving performance long before obvious physical intoxication appears. It reduces peripheral vision, slows reaction timing, distorts distance perception, and impairs rational decision-making and hazard evaluation.

Missouri law enforces strict chemical testing through the Implied Consent doctrine. Law enforcement officers equipped with reasonable grounds may request a chemical breath or blood test. Refusal results in an immediate administrative one-year license revocation regardless of whether you are subsequently convicted in court.

Operating a vehicle with a Blood Alcohol Concentration of 0.08 percent or higher constitutes an automatic violation. Commercial operators face disqualification at 0.04 percent, while young drivers under 21 face automatic suspension at 0.02 percent under Missouri's Zero Tolerance statute.
"""
    },
    "chapter-11": {
        "title": "The Point System",
        "cram": """
Welcome to the Chapter 11 Cram Session: The Missouri Point System. These numbers are tested frequently on license renewal and permit exams!

Milestone number one: 4 Points in 12 Months.
When you accumulate 4 points on your driving record within a 12-month period, the Department of Revenue sends you an advisory Warning Letter urging you to improve your driving habits before losing your license.

Milestone number two: 8 Points in 18 Months = Suspension.
If you accumulate 8 or more points within an 18-month period, your driver license is automatically suspended:
- First suspension: 30 days.
- Second suspension: 60 days.
- Third or subsequent suspension: 90 days.

Milestone number three: 12 Points = 1-Year Revocation.
Your driver license will be revoked for one full calendar year if you accumulate:
- 12 or more points in 12 months,
- 18 or more points in 24 months, or
- 24 or more points in 36 months.

Milestone number four: How Points are Reduced.
If you drive without committing any moving violations:
- After 1 full year of clean driving: Your points are reduced by one-third.
- After 2 consecutive full years: Your remaining points are reduced by one-half.
- After 3 consecutive full years: Your point total drops completely to zero!

Common point assessments: Speeding in state court adds 3 points; Careless and imprudent driving adds 4 points; Driving under the influence or failure to maintain insurance adds 4 to 8 points.

Remember: Warning letter at 4 points, suspension at 8 points, one-year revocation at 12 points, and three clean years drops your record to zero!
""",
        "narration": """
Chapter 11 explains the Missouri Point System administered by the Driver License Bureau of the Department of Revenue. The point system identifies chronic traffic offenders, enforces progressive disciplinary actions, and encourages compliant driving.

Points are assessed against your official state driving record upon conviction for traffic violations in municipal or state circuit courts. Minor infractions carry lower point values, while dangerous offenses, hit-and-run crashes, and substance impairment incur immediate suspensions.

The Department monitors accumulated points on a rolling timeline:
An accumulation of 4 points within 12 months prompts an official warning notice.
Reaching 8 points within 18 months triggers mandatory driving privilege suspension, progressing from 30 days for a first occurrence up to 90 days for repeated violations.
Reaching 12 points within 12 months results in a complete one-year revocation, requiring full re-examination, reinstatement fees, and proof of SR-22 insurance.

Points decrease over time through clean driving: your point total reduces by one-third after one violation-free year, drops by half after two years, and resets entirely to zero after three consecutive years.
"""
    },
    "chapter-12": {
        "title": "Vehicle Titling and Registration",
        "cram": """
Welcome to the Chapter 12 Cram Session: Vehicle Titling, Registration, and License Plates.

Rule number one: 30-Day Titling Window.
When you purchase a new or used motor vehicle in Missouri, you must apply for a Certificate of Title within 30 days of the date of purchase. If you fail to title your vehicle within 30 days, you will be charged a penalty fee of 25 dollars for each 30 days late, up to a maximum penalty of 200 dollars.

Rule number two: Required Documents for Titling and Registration.
When you visit the license office to title and license a vehicle, you must present:
1. The Certificate of Title or Manufacturer's Statement of Origin, properly assigned to you.
2. An approved Missouri Vehicle Safety Inspection certificate, not more than 60 days old.
3. An emissions inspection certificate, if you reside in the St. Louis area.
4. Your personal property tax receipt or non-assessment waiver for the previous tax year.
5. Current proof of financial responsibility vehicle insurance.

Rule number three: License Plate Renewals.
Missouri offers biennial, or two-year, registrations. Vehicle model years correspond to renewal years: even-year model vehicles renew in even-numbered years, and odd-year model vehicles renew in odd-numbered years.

Rule number four: Disability Parking Placards.
Disability parking placards may only be displayed when the vehicle is actively transporting the disabled individual. Remember this key law: You must remove the hanging placard from your rearview mirror while driving; hanging placards can obstruct forward vision and constitute a moving violation.

Remember: Title within 30 days or pay late fees; keep safety inspection under 60 days; and always remove disability placards from the rearview mirror while driving!
""",
        "narration": """
Chapter 12 governs the titling, registration, and license plate requirements for motor vehicles operating on Missouri highways. The Department of Revenue administers vehicle documentation to verify legal ownership and roadworthiness.

Upon purchasing or acquiring a motor vehicle, Missouri law requires you to submit an application for title within 30 days. Operating an untitled or unregistered vehicle is a misdemeanor offense subject to progressive late fees and moving citations.

To register a vehicle and obtain license plates, you must demonstrate compliance with state emissions and safety mandates, provide receipts confirming payment of county personal property taxes, and show valid proof of vehicle liability insurance.

License plates must be securely attached to both the front and rear bumpers of passenger vehicles, kept clean, illuminated by a white rear license plate lamp, and completely free of obstructing frames or tinted plastic covers that obscure registration tags.
"""
    },
    "chapter-13": {
        "title": "Mandatory Insurance",
        "cram": """
Welcome to the Chapter 13 Cram Session: Mandatory Insurance and Financial Responsibility. This chapter covers the exact dollar amounts required by Missouri law!

Fact number one: Missouri's 25/50/25 Minimum Liability Limits.
Memorize these three numbers for your permit test:
- 25,000 dollars for bodily injury or death of one person in any one accident.
- 50,000 dollars for bodily injury or death of two or more persons in any one accident.
- 25,000 dollars for injury to or destruction of property of others in any one accident.
Together, this is legally known as 25/50/25 liability coverage.

Fact number two: Proof of Insurance.
You must maintain valid proof of financial responsibility in your motor vehicle at all times, or be able to show digital electronic proof on your smartphone. You must present this proof when registering your vehicle, when renewing license plates, and anytime requested by a law enforcement officer or accident investigator.

Fact number three: Penalties for Uninsured Driving.
If you are caught driving without insurance:
- 4 points will be assessed against your Missouri driving record.
- Your driver license and vehicle plates will be suspended.
- You must pay reinstatement fees starting at 20 dollars and climbing to 400 dollars for repeat offenses.
- You will be required to file and maintain an SR-22 proof of financial responsibility insurance policy with the state for three full consecutive years.

Remember: 25 thousand per person, 50 thousand per crash, 25 thousand property damage; uninsured driving adds 4 points and requires a 3-year SR-22 filing!
""",
        "narration": """
Chapter 13 details Missouri's Motor Vehicle Financial Responsibility Law. Operating a motor vehicle is a privilege that carries substantial financial responsibility for any personal injury or property damage you may cause to others.

Every motor vehicle operated on Missouri public roads must be covered by a valid liability insurance policy issued by an authorized insurance provider. State law establishes minimum mandatory liability limits of 25 thousand dollars for bodily injury to one person, 50 thousand dollars for total bodily injury per collision, and 25 thousand dollars for property damage.

Drivers must present proof of valid insurance during annual registration, following traffic accidents, and upon lawful request by law enforcement officers.

Failure to maintain insurance results in automatic administrative suspensions, assessment of 4 points against your driving record, and mandatory filing of an SR-22 certificate of future financial responsibility for a continuous period of three years.
"""
    },
    "chapter-14": {
        "title": "Safety and Emissions Inspections & Required Equipment",
        "cram": """
Welcome to the Chapter 14 Cram Session: Vehicle Safety Inspections, Emissions, and Required Equipment.

Part one: Biennial Safety Inspections.
In Missouri, a motor vehicle safety inspection is required every two years for vehicles that are over 10 model years old or have an odometer reading over 150,000 miles. Safety inspection certificates are valid for 60 days from the date of inspection.

Part two: Gateway Emissions Testing.
Emissions testing is required for motor vehicles registered in five specific jurisdictions:
1. St. Louis City.
2. St. Louis County.
3. St. Charles County.
4. Jefferson County.
5. Franklin County.

Part three: Required Vehicle Equipment.
Your vehicle must be equipped with all of the following in good working order:
- Headlights: At least two white headlights that illuminate persons and vehicles at least 500 feet ahead on high beam.
- Taillights: Red taillights visible from a distance of 500 feet, along with a white license plate illumination lamp visible from 50 feet.
- Horn: An audible horn capable of being heard from a distance of at least 200 feet. Sirens, whistles, and bells are prohibited on non-emergency passenger vehicles.
- Muffler: An adequate muffler in constant operation to prevent excessive or unusual noise. Muffler cutouts, bypasses, or straight pipes are strictly illegal in Missouri.
- Mirror: At least one rearview mirror providing a view of the highway for at least 200 feet to the rear.

Remember: Safety inspection valid for 60 days; horn must be heard from 200 feet; headlights illuminate 500 feet; and muffler cutouts are illegal!
""",
        "narration": """
Chapter 14 establishes vehicle safety standards, mandatory equipment specifications, and regional emissions compliance mandates. Keeping your motor vehicle in proper mechanical condition is essential for highway safety and clean air quality.

Missouri requires biennial safety inspections for vehicles exceeding 10 model years or 150,000 miles. Certified inspection stations evaluate steering mechanisms, braking performance, tire tread depth, suspension components, lighting systems, and window glazing.

In the metropolitan St. Louis region, including St. Louis City, St. Louis County, St. Charles, Jefferson, and Franklin counties, vehicles must also satisfy On-Board Diagnostic emissions standards under the Gateway Clean Air Program.

All vehicles operated on public highways must maintain functioning safety equipment: two white headlights, red taillights, rear reflectors, turn signals, windshield wipers, a rearview mirror with 200 feet rearward visibility, and a horn audible from at least 200 feet.
"""
    },
    "chapter-15": {
        "title": "Commercial Vehicles",
        "cram": """
Welcome to the Chapter 15 Cram Session: Commercial Vehicles and the Class E For-Hire License. If you are taking the Class E written test, this chapter is your primary focus!

Rule number one: Who Needs a Class E For-Hire License?
You must obtain a Class E license if:
1. You receive pay for driving a motor vehicle carrying 14 or fewer passengers, such as a daycare van driver.
2. You transport property for pay or as part of your job, such as a florist or parcel delivery driver.
3. You operate an employer-owned motor vehicle designed to carry freight with a Gross Vehicle Weight Rating of 26,000 pounds or less.
Exemptions: Uber, Lyft, and taxicab drivers operating vehicles under 12,000 pounds, and restaurant prepared-food delivery drivers do not need a Class E license.

Rule number two: Class E Eligibility.
You must be at least 18 years old to obtain a Class E license. If you already hold a valid Class F operator license, a driving skills road test is not required; you only need to pass the Class E written test and vision screening.

Rule number three: Emergency Safety Equipment for Commercial Vehicles.
Commercial motor vehicles must carry:
- Three emergency reflective triangles, flares, or electric lanterns.
- At least one approved fire extinguisher properly charged and mounted.

Rule number four: Commercial Vehicle Dimensions.
- Maximum vehicle width: 8 feet 6 inches, or 102 inches.
- Maximum height: 13 feet 6 inches to 14 feet, depending on the roadway classification.

Remember: Class E at age 18, applies to transporting passengers or goods for pay under 26,000 pounds; must carry 3 reflective triangles and a fire extinguisher!
""",
        "narration": """
Chapter 15 details regulations governing commercial motor vehicles and the requirements for earning a Missouri Class E For-Hire license.

A Class E license is required when an individual is employed for the principal purpose of operating a motor vehicle, transports 14 or fewer passengers for compensation, or drives a commercial freight delivery vehicle rated at 26,000 pounds or less Gross Vehicle Weight Rating. Drivers operating vehicles exceeding 26,000 pounds, transporting hazardous materials, or carrying 16 or more passengers require a Commercial Driver License, or CDL.

Commercial vehicles are subject to rigorous safety rules. Operators must ensure their vehicle is equipped with side clearance lights, mud flaps that prevent tires from throwing rocks and debris, an approved and charged fire extinguisher, and three portable emergency reflective warning triangles.

Before operating any commercial vehicle, drivers must conduct a thorough pre-trip inspection of tires, coupling devices, steering components, and air brake systems to guarantee safe transit.
"""
    },
    "chapter-16": {
        "title": "Distracted Driving & Electronic Communication Devices",
        "cram": """
Welcome to the Chapter 16 Cram Session: Missouri's Siddens Bening Hands-Free Law, Senate Bill 398. This is Missouri's newest traffic statute and is tested on all recent exams!

Rule number one: The Universal Hands-Free Prohibition.
Under Missouri law, ALL drivers, regardless of age, are strictly prohibited from physically holding or supporting a cell phone or electronic wireless communication device with any part of their body while driving on public highways.

Rule number two: Specifically Prohibited Actions.
While operating a motor vehicle, you cannot:
- Physically hold your phone in your hand or rest it on your lap.
- Read, write, or send text messages, emails, or instant messages.
- Manually enter letters, numbers, or symbols.
- Watch movies, videos, streaming broadcasts, or social media feeds.
- Record, broadcast, or transmit video.

Rule number three: What IS Permitted?
You may use your phone ONLY in hands-free mode:
- Voice-operated features and voice-to-text dictation.
- Hands-free Bluetooth telephone calls through your vehicle speakers or a single-ear headset.
- GPS navigation apps, provided the phone is secured in a dashboard or windshield mount and requires only a single touch or swipe to activate.

Rule number four: Exceptions and Penalties.
You are permitted to hold your phone only to make an emergency call to 911, the police, fire department, or emergency medical personnel to report a crime, fire, or road hazard. Violations carry fines up to 150 dollars for a first offense, with enhanced penalties in designated school zones and active highway work zones.

Remember: Never hold your phone while driving; use mounted hands-free navigation; emergency 911 is the only exception; keep both hands on the wheel!
""",
        "narration": """
Chapter 16 covers Missouri's landmark distracted driving statute, known as the Siddens Bening Hands-Free Law, enacted under Senate Bill 398. Distracted driving is a primary catalyst for highway collisions, pedestrian injuries, and avoidable fatalities.

The law establishes a clear, statewide standard: no driver may physically hold, grip, or support any wireless communication device with their hand, arm, or lap while operating a motor vehicle on public roads.

Drivers are encouraged to configure navigation routes and music playlists before shifting into gear. Handheld typing, texting, internet browsing, and video streaming are strictly outlawed. Drivers may utilize integrated voice-activation features, Bluetooth hands-free systems, and dashboard-mounted devices accessible via simple single-tap controls.

Focusing completely on the road, scanning mirrors regularly, and eliminating electronic distractions ensures that every driver returns home safely. Drive safe, Missouri!
"""
    }
}

async def generate_chapter(ch_id, data):
    print(f"\n==========================================")
    print(f"Generating Audio for {ch_id}: {data['title']}")
    print(f"==========================================")

    # 1. Cram Podcast (Guy Neural)
    cram_file = os.path.join(OUTPUT_DIR, f"{ch_id}_cram.mp3")
    print(f"  • Generating Cram Podcast -> {os.path.basename(cram_file)} (en-US-GuyNeural)...")
    comm_cram = edge_tts.Communicate(data["cram"].strip(), "en-US-GuyNeural", rate="+4%", pitch="+0Hz")
    await comm_cram.save(cram_file)
    cram_kb = os.path.getsize(cram_file) / 1024
    print(f"    [Done] Size: {cram_kb:.1f} KB")

    # 2. Comprehensive Narration (Jenny Neural)
    narration_file = os.path.join(OUTPUT_DIR, f"{ch_id}_narration.mp3")
    print(f"  • Generating Chapter Narration -> {os.path.basename(narration_file)} (en-US-JennyNeural)...")
    comm_narr = edge_tts.Communicate(data["narration"].strip(), "en-US-JennyNeural", rate="+2%", pitch="+1Hz")
    await comm_narr.save(narration_file)
    narr_kb = os.path.getsize(narration_file) / 1024
    print(f"    [Done] Size: {narr_kb:.1f} KB")

async def main():
    print("Starting Studio Audio Generation for 17 Chapters (Intro + 1 to 16)...")
    total_files = len(CHAPTERS) * 2
    print(f"Total MP3 files to generate: {total_files}")
    
    # Process sequentially or in small batches of 2-3 to avoid rate limits
    for ch_id, ch_data in CHAPTERS.items():
        await generate_chapter(ch_id, ch_data)
        await asyncio.sleep(0.5)

    print("\n==========================================")
    print("ALL 34 AUDIOBOOK & CRAM TRACKS GENERATED!")
    print("==========================================")

if __name__ == "__main__":
    asyncio.run(main())
