#!/usr/bin/env python3
"""
Full Unabridged Audiobook Generator for Missouri Driver Guide.
Generates complete, unabridged narrations for all chapters using Jenny Neural.
Every section, rule, and paragraph from the official handbook is narrated.
"""

import os
import re
import json
import time
import asyncio
import edge_tts

OUTPUT_DIR = "/Users/nutanvamsigunti/workspace/missouri-driver-guide/assets/audio/chapters"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text_for_audio(raw_text):
    text = raw_text
    
    # Strip raw PDF page numbers and dot leaders
    text = re.sub(r'Page\s+\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\.\s*\.\s*\.\s*\.\s*\.', '', text)
    text = re.sub(r'[•\x07*\t]', ' ', text)
    
    # Expand abbreviations for natural speech
    replacements = [
        (r'\bRSMo\b', 'Revised Statutes of Missouri'),
        (r'\bGDL\b', 'Graduated Driver License'),
        (r'\bBAC\b', 'Blood Alcohol Concentration'),
        (r'\bCDL\b', 'Commercial Driver License'),
        (r'\bGVWR\b', 'Gross Vehicle Weight Rating'),
        (r'\bMSHP\b', 'Missouri State Highway Patrol'),
        (r'\bDOR\b', 'Department of Revenue'),
        (r'\bDOT\b', 'Department of Transportation'),
        (r'\bmph\b', 'miles per hour'),
        (r'\bDUI\b', 'Driving Under the Influence'),
        (r'\bDWI\b', 'Driving While Intoxicated'),
        (r'(\d+)\s*ft\.?', r'\1 feet'),
        (r'(\d+)\s*in\.?', r'\1 inches'),
        (r'(\d+)\s*lbs\.?', r'\1 pounds'),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
        
    # Merge wrapped lines into complete sentences
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    merged = []
    for line in lines:
        if merged and not merged[-1].endswith(('.', ':', '!', '?', ';')):
            merged[-1] += ' ' + line
        else:
            merged.append(line)
            
    clean = ' '.join(merged)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def chunk_text(text, max_chars=3200):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = []
    current_len = 0
    for s in sentences:
        if current_len + len(s) > max_chars and current:
            chunks.append(' '.join(current))
            current = [s]
            current_len = len(s)
        else:
            current.append(s)
            current_len += len(s)
    if current:
        chunks.append(' '.join(current))
    return chunks

async def generate_chapter_narration(ch):
    ch_id = ch['id']
    title = ch['title']
    output_file = os.path.join(OUTPUT_DIR, f"{ch_id}_narration.mp3")
    
    print(f"\n=======================================================")
    print(f"Generating Full Unabridged Narration: {ch_id} - {title}")
    print(f"=======================================================")
    
    raw_text = ch.get('full_text', '')
    if not raw_text:
        print(f"  [Warning] No full_text for {ch_id}, skipping.")
        return
        
    cleaned = clean_text_for_audio(raw_text)
    intro_prefix = f"Chapter {ch['number']}: {title}. " if ch['number'] > 0 else f"{title}. "
    full_script = intro_prefix + cleaned
    
    chunks = chunk_text(full_script)
    words = len(full_script.split())
    print(f"  • Total Words: {words} | Characters: {len(full_script)} | Chunks: {len(chunks)}")
    
    t0 = time.time()
    temp_output = output_file + ".tmp"
    with open(temp_output, 'wb') as outfile:
        for idx, chunk in enumerate(chunks):
            # print(f"    - Processing Chunk {idx+1}/{len(chunks)} ({len(chunk)} chars)...")
            comm = edge_tts.Communicate(chunk, "en-US-JennyNeural", rate="+2%", pitch="+1Hz")
            async for item in comm.stream():
                if item["type"] == "audio":
                    outfile.write(item["data"])
                    
    # Atomic rename upon successful completion
    os.replace(temp_output, output_file)
    elapsed = time.time() - t0
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"  ✅ Completed in {elapsed:.1f}s | Size: {file_size_mb:.2f} MB -> {os.path.basename(output_file)}")

async def main():
    print("Loading handbook data from data.js...")
    with open('data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    data = json.loads(content[content.index('{'):content.rindex('}')+1])
    
    chapters_to_process = [ch for ch in data['chapters'] if ch['number'] <= 16]
    print(f"Found {len(chapters_to_process)} chapters to synthesize.")
    
    t_start = time.time()
    for ch in chapters_to_process:
        await generate_chapter_narration(ch)
        await asyncio.sleep(0.5)
        
    total_time = time.time() - t_start
    print(f"\n🎉 ALL {len(chapters_to_process)} UNABRIDGED CHAPTER AUDIOBOOKS GENERATED IN {total_time/60:.1f} MINUTES!")

if __name__ == "__main__":
    asyncio.run(main())
