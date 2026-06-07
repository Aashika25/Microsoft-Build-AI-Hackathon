import requests
from bs4 import BeautifulSoup
import time
import os
from urllib.parse import urljoin, urlparse

seed_urls = [
    "https://handbook.gitlab.com/handbook/people-group/general-onboarding/",
    "https://handbook.gitlab.com/handbook/engineering/",
    "https://handbook.gitlab.com/handbook/people-group/",
    "https://handbook.gitlab.com/handbook/communication/",
    "https://handbook.gitlab.com/handbook/people-policies/",
    "https://handbook.gitlab.com/handbook/business-technology/"
]
    
BASE_DOMAIN = "handbook.gitlab.com"
BASE_OUTPUT_DIR = "gitlab_handbook_data"
visited = set()

def get_page_name(url):
    parsed = urlparse(url)
    name = parsed.path.strip('/').split('/')[-1]
    return name if name else "index"

def is_seed_url(url):
    for seed in seed_urls:
        if url.rstrip('/') == seed.rstrip('/'):
            return True
    return False

def get_links_from_content(content_div, current_url):
    """Extract links only from td-content div"""
    links = []
    for a in content_div.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(current_url, href)
        parsed = urlparse(full_url)

        if parsed.netloc == BASE_DOMAIN and '/handbook/' in parsed.path:
            clean_url = parsed.scheme + "://" + parsed.netloc + parsed.path
            links.append(clean_url)
    return links

def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"    ⚠️ Non-200 status ({response.status_code}) for: {url}")
            return None, []

        soup = BeautifulSoup(response.text, 'html.parser')
        main = soup.find('div', class_=lambda c: c and 'td-content' in c)

        if not main:
            print(f"    ⚠️ td-content not found on: {url}")
            return None, []

        # Extract links from td-content BEFORE decomposing tags
        links = get_links_from_content(main, url)

        # Clean noise
        for tag in main.find_all(['script', 'style', 'button', 'form']):
            tag.decompose()

        text = main.get_text(separator='\n', strip=True)
        lines = [line for line in text.splitlines() if line.strip()]
        cleaned = '\n'.join(lines)

        return cleaned, links

    except requests.exceptions.Timeout:
        print(f"    ❌ Timeout on: {url}")
        return None, []
    except requests.exceptions.ConnectionError:
        print(f"    ❌ Connection error on: {url}")
        return None, []
    except Exception as e:
        print(f"    ❌ Unexpected error on {url}: {e}")
        return None, []

def save_content(url, text, parent_url=None):
    if is_seed_url(url):
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        folder = os.path.join(BASE_OUTPUT_DIR, *path_parts)
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, "content.txt")
    else:
        if parent_url:
            parsed_parent = urlparse(parent_url)
            parent_parts = parsed_parent.path.strip('/').split('/')
            folder = os.path.join(BASE_OUTPUT_DIR, *parent_parts)
        else:
            folder = BASE_OUTPUT_DIR

        os.makedirs(folder, exist_ok=True)
        page_name = get_page_name(url)
        filepath = os.path.join(folder, f"{page_name}.txt")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"SOURCE: {url}\n")
        f.write("=" * 60 + "\n\n")
        f.write(text)

    return filepath

# ── Level 0: Scrape seed pages first ──────────────────────
print(f"🚀 Starting crawl — 1 level deep only")
print(f"📁 Output: {BASE_OUTPUT_DIR}/\n")

child_queue = []  # collect child links from seed pages

for url in seed_urls:
    if url in visited:
        continue

    visited.add(url)
    print(f"[SEED] Scraping: {url}")

    text, links = scrape_page(url)

    if text and len(text) > 200:
        filepath = save_content(url, text)
        print(f"    ✅ Saved → {filepath} ({len(text)} chars)")
        print(f"    🔗 Found {len(links)} child links")

        # Add child links with their parent
        for link in links:
            if link not in visited:
                child_queue.append((link, url))
    else:
        print(f"    ⚠️ Skipped — empty content")

    time.sleep(0.5)

# ── Level 1: Scrape child pages only ──────────────────────
print(f"\n📄 Scraping {len(child_queue)} child pages...\n")

for url, parent_url in child_queue:
    if url in visited:
        continue

    visited.add(url)
    print(f"[CHILD] Scraping: {url}")

    text, _ = scrape_page(url)  # ignore links — no deeper crawling

    if text and len(text) > 200:
        filepath = save_content(url, text, parent_url)
        print(f"    ✅ Saved → {filepath} ({len(text)} chars)")
    else:
        print(f"    ⚠️ Skipped — empty content")

    time.sleep(0.5)

# ── Summary ────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"✅ Done!")
print(f"📄 Total pages scraped : {len(visited)}")
print(f"📁 Data saved in       : {BASE_OUTPUT_DIR}/")
print(f"{'='*50}")