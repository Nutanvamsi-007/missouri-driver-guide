import fitz  # PyMuPDF
import json

doc = fitz.open("Driver_Guide.pdf")
print(f"Total Pages: {len(doc)}")
print(f"Metadata: {json.dumps(doc.metadata, indent=2)}")

toc = doc.get_toc()
print(f"Table of Contents entries: {len(toc)}")
for item in toc[:40]:
    print(f"  Level {item[0]}: {item[1]} (Page {item[2]})")

# Check images across first 10 pages and total images
total_images = 0
for pno in range(len(doc)):
    page = doc[pno]
    imgs = page.get_images(full=True)
    total_images += len(imgs)
    if pno < 8 and imgs:
        print(f"Page {pno+1} has {len(imgs)} images")

print(f"Total images found across document: {total_images}")
