# 🚗 Missouri Driver Guide — Interactive Study Portal & Exam Simulator

A high-performance, attention-seeking local web application containing **all 102 pages, 16 chapters, and 73+ traffic signs and road diagrams** from the official Missouri Department of Revenue (DOR) Driver Guide (`Driver Guide.pdf`, Revised August 2026).

---

## ⚡ Quick Start

Run the automated launcher script to start the local web server and launch the application in your browser:

```bash
cd /Users/nutanvamsigunti/workspace/missouri-driver-guide
./start.sh
```

Or run directly with Python:

```bash
python3 server.py --open
```

The web server will automatically boot at: **`http://localhost:8080`** (or next available port).

---

## 🔍 The Best & Most Efficient Way to Copy PDF Text & Pictures

Extracting content from Adobe InDesign-generated state manuals presents unique technical challenges. Here is how our dual-pipeline extraction engine solves them:

### 1. Vector Signs vs. Raster Images Challenge
* **The Problem**: In the Missouri Driver Guide, standard road signs (Stop, Yield, Speed Limits, Regulatory, Warning, Work Zone, Interstate shields) and lane lines are rendered in Adobe InDesign as **vector paths (`drawings`)**, NOT embedded raster images. Standard PDF extractors (like `pdfimages`) yield **0 images** on key sign pages (pages 48–56).
* **The Solution**: 
  1. **Native Raster Image Stream Extraction**: We extract all 62 authentic photographs and composite diagrams using PyMuPDF (`fitz.extract_image(xref)`) directly without re-compression loss.
  2. **High-DPI Vector Bounding-Box Cropping**: We isolate and render every individual traffic sign and road diagram at **200 DPI** into crisp, transparent PNGs (`assets/images/signs/` and `assets/images/diagrams/`).
  3. **Retina Page Rendering**: Every one of the **102 pages** is rendered at **140 DPI into modern WebP format** (`assets/pages/page_001.webp` through `page_102.webp`), totaling only ~12 MB for the entire handbook. This powers the interactive side-by-side **"Official PDF Mirror"** view.

### 2. High-Fidelity Structured Text Extraction
* PyMuPDF block parsing captures the full text hierarchy:
  * 16 Official Chapters + Introduction + Complete Index.
  * Headings, subheadings, bullet points, statutory citations (RSMo), and fee schedules.
  * Identification of **💡 Examiner Tips**, **⚠️ Legal Warnings & Penalties**, and **ℹ️ Important Notes**.
  * Complete full-text search indexing across all 102 pages.

---

## 🌟 Interactive Features

### 1. 📖 Full Handbook Reader
* **Sticky Table of Contents**: Navigate effortlessly through all 16 chapters with estimated reading times and completion checkmarks.
* **Original PDF Mirror**: Click *"View Official PDF Page"* on any section to instantly compare the interactive text with the original high-resolution printed page.
* **Audio Narration (Text-to-Speech)**: Integrated Web Speech API (`speechSynthesis`) lets you listen to any chapter read aloud with play/pause controls.
* **Reading Customization**: Dynamic font scaler (`A-` / `A+`) and dark/light theme switching with preference persistence in `localStorage`.
* **Study Bookmarks**: Star any tricky chapter to save for quick review.

### 2. 📝 Missouri Permit Exam Simulator
* Modeled directly after the real Missouri State Highway Patrol written test.
* **25 Randomized Questions**: Passing score requires **80% (20 of 25 correct)**.
* **Two Modes**:
  * **Practice Mode**: Immediate feedback on every selection with detailed statutory explanations and Driver Guide page references.
  * **Timed Exam Mode**: 25-minute test countdown, simulating real exam conditions.
* Complete performance breakdown with question-by-question review.

### 3. 🛑 3D Road Sign Lab & Flashcards
* Interactive 3D flip cards with realistic perspective physics.
* 73+ signs and diagrams categorized by **Regulatory**, **Warning**, **Work Zone**, **Guide & Services**, **Sign Shapes**, and **Road Maneuvers**.
* Flip to test recognition: front reveals the graphic; back reveals the official rule, name, and handbook page citation.

### 4. 🧮 Interactive Rules & Safety Simulators
* **Speed & Stopping Distance Calculator**: Interactive slider (20 to 75 mph) with dry vs. wet road friction toggles. Displays reaction distance, braking distance, and total stopping distance in feet and car lengths.
* **Missouri Point System Penalty Tracker**: Interactive violation checklist (Careless driving, Speeding 5–29 mph, Speeding 30+ mph, DUI, Suspended license). Displays license standing: Safe, 4-Point Warning Letter, 8-Point Suspension (30–90 days), or 12-Point Revocation (1 year).
* **Blood Alcohol Concentration (BAC) Gauge**: Visual breakdown of Zero Tolerance (.02% for under 21), Commercial (.04%), and Adult Intoxication (.08%), along with the Implied Consent Law penalty (immediate 1-year revocation for refusal).
* **Siddens Bening Hands-Free Law (SB 398)**: Interactive prohibited vs. permitted phone uses guide.

### 5. 🔍 Instant Global Full-Text Search (`⌘K` or `/`)
* Client-side fuzzy search across all 102 pages, definitions, and signs.
* Instant `<mark>` keyword highlighting with direct jump to sections.

### 6. 🖼 102 PDF Pages Mirror Grid
* Visual gallery of all 102 official state pages.
* Click any thumbnail to open the high-res zoom lightbox.

---

## 📁 Project Structure

```
missouri-driver-guide/
├── Driver_Guide.pdf           # Original Missouri DOR PDF (2.2 MB)
├── index.html                 # Main interactive single-page application
├── styles.css                 # Custom glassmorphic CSS (Dark/Light mode)
├── app.js                     # Application engine (Reader, Exam, Flashcards, Search)
├── data.js                    # Pre-packaged JS data bundle (zero CORS restrictions)
├── guide_data.json            # Structured JSON database of the manual
├── server.py                  # Custom Python HTTP server with WebP MIME support
├── start.sh                   # Executable one-click launcher
├── build_missouri_guide.py    # Python extraction pipeline script
└── assets/
    ├── pages/                 # 102 high-resolution WebP page renders
    └── images/
        ├── signs/             # 58 cropped traffic signs & shields (PNG)
        ├── diagrams/          # 15 road maneuver & parking diagrams (PNG)
        └── extracted/         # 62 native raster images from PDF
```

---

## 🛠 Re-running the Extraction Pipeline

If you ever wish to re-extract the PDF or adjust image DPI settings:

```bash
cd /Users/nutanvamsigunti/workspace/missouri-driver-guide
./.venv/bin/python build_missouri_guide.py
```

---

## 🌐 Public Web Hosting & Deployment Guide

This project is engineered as a **100% static, zero-dependency Progressive Web Application (PWA)**. It requires no backend runtime, database, or server-side computation. It can be hosted free of charge on any modern edge CDN or static hosting provider.

### Option 1: GitHub Pages (Recommended — Automated)

The repository includes a ready-to-use GitHub Actions workflow (`.github/workflows/deploy.yml`) and `.nojekyll` configuration:

1. **Create a remote repository** on GitHub (e.g. `missouri-driver-guide`).
2. **Push your code**:
   ```bash
   git remote add origin https://github.com/<your-username>/missouri-driver-guide.git
   git push -u origin main
   ```
3. **Enable GitHub Pages**:
   - Navigate to **Settings > Pages** on your GitHub repository.
   - Under **Build and deployment > Source**, select **GitHub Actions**.
   - Your site will automatically build and publish to `https://<your-username>.github.io/missouri-driver-guide/`.

*(Note: If hosting on a GitHub project subpath, all asset links are strictly relative, so everything works out of the box without broken links!)*

---

### Option 2: Cloudflare Pages (Ultra-Fast Global Edge)

Cloudflare Pages provides global anycast edge caching with unlimited bandwidth:

1. Log into your [Cloudflare Dashboard](https://dash.cloudflare.com/) and go to **Workers & Pages > Create application > Pages > Connect to Git**.
2. Select your repository.
3. Configure build settings:
   - **Framework preset**: None
   - **Build command**: *(leave blank)*
   - **Build output directory**: `.`
4. Click **Save and Deploy**. Cloudflare automatically respects the included `_headers` and `_redirects` configuration files for security and long-term asset caching.

---

### Option 3: Vercel / Netlify

1. Import the repository in [Vercel](https://vercel.com/) or [Netlify](https://netlify.com/).
2. Leave the build command empty and set the publish directory to `.`.
3. The included `vercel.json` (for Vercel) and `_headers` / `_redirects` (for Netlify) provide instant routing, cache control, and PWA manifest headers.

---

## 📱 Progressive Web App (PWA) Offline Capabilities

* **Installable on Mobile & Desktop**: Users can tap **"Add to Home Screen"** on iOS Safari or Chrome on Android/Desktop to install the app like a native app.
* **Service Worker (`sw.js`)**: Implements `NetworkFirst` for HTML updates and `CacheFirst` for static assets (CSS, JS, 102 WebP pages, and sign PNGs), providing uninterrupted studying even in airplane mode.
* **Web App Manifest (`manifest.webmanifest`)**: Defines standalone display mode, high-res icons (192px & 512px), and deep-link shortcuts to the Exam Simulator and Signs Lab.
* **Deep Linking**: Direct navigation via URL hashes (e.g. `#exam`, `#signs`, `#calculators`, `#pdf-mirror`, `#reader`).

---

## 🔍 SEO & Social Sharing (OpenGraph)

* **Social Preview Image**: 1200x630 pixel-perfect `og-image.png` included for link previews on Twitter/X, Discord, Slack, iMessage, and LinkedIn.
* **Structured Data**: Schema.org `WebApplication` and `LearningResource` JSON-LD markup embedded for Google rich results.
* **Search Engine Files**: Included `robots.txt` and `sitemap.xml` for crawler indexing.
