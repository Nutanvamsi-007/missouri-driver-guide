#!/usr/bin/env python3
"""
Generate sample high-quality AI narration audio clips using Microsoft Neural Voices (edge-tts).
Produces both comprehensive chapter narration and high-yield 3-minute exam cram podcasts.
"""

import os
import asyncio
import edge_tts

OUTPUT_DIR = "/Users/nutanvamsigunti/workspace/missouri-driver-guide/assets/audio/samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Curated Narration Script for Chapter 1 (Curated for natural speech & listener attention)
CHAPTER_1_NARRATION = """
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

# High-Yield 3-Minute Exam Cram Podcast Script
EXAM_CRAM_SCRIPT = """
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
"""

async def generate_samples():
    print("Generating sample AI neural audio files...")

    # Sample 1: Andrew (Warm, conversational male educator)
    file1 = os.path.join(OUTPUT_DIR, "chapter1_narration_andrew.mp3")
    print(f"Creating {file1} (en-US-AndrewNeural)...")
    comm1 = edge_tts.Communicate(CHAPTER_1_NARRATION.strip(), "en-US-AndrewNeural", rate="+3%", pitch="+0Hz")
    await comm1.save(file1)

    # Sample 2: Jenny (Clear, engaging female educator)
    file2 = os.path.join(OUTPUT_DIR, "chapter1_narration_jenny.mp3")
    print(f"Creating {file2} (en-US-JennyNeural)...")
    comm2 = edge_tts.Communicate(CHAPTER_1_NARRATION.strip(), "en-US-JennyNeural", rate="+2%", pitch="+1Hz")
    await comm2.save(file2)

    # Sample 3: High-Yield Exam Cram Podcast (Guy - confident broadcast quality)
    file3 = os.path.join(OUTPUT_DIR, "chapter1_cram_podcast_guy.mp3")
    print(f"Creating {file3} (en-US-GuyNeural)...")
    comm3 = edge_tts.Communicate(EXAM_CRAM_SCRIPT.strip(), "en-US-GuyNeural", rate="+5%", pitch="+0Hz")
    await comm3.save(file3)

    print("\nAll audio samples generated successfully!")
    for f in [file1, file2, file3]:
        size_kb = os.path.getsize(f) / 1024
        print(f"  • {os.path.basename(f)}: {size_kb:.1f} KB")

if __name__ == "__main__":
    asyncio.run(generate_samples())
