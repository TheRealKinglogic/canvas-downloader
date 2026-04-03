from playwright.sync_api import sync_playwright
import os
import re
import time

#Change to URL of course you want to download
URL = "https://bruinlearn.ucla.edu/courses/YOUR_COURSE_ID/modules"

def clean_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        storage_state="state.json",
        accept_downloads=True
    )
    page = context.new_page()

    page.goto(URL)
    page.wait_for_selector(".context_module")

    buttons = page.query_selector_all("button")
    for b in buttons:
        try:
            if b.get_attribute("aria-expanded") == "false":
                b.click()
        except:
            pass

    time.sleep(2)

    modules = page.query_selector_all(".context_module")
    print(f"Found {len(modules)} modules")

    for m_idx in range(len(modules)):

        modules = page.query_selector_all(".context_module")
        module = modules[m_idx]

        title_el = module.query_selector(".context_module_title")
        if title_el:
            module_name = clean_name(title_el.inner_text().strip())
        else:
            module_name = f"Module_{m_idx+1}"

        if not module_name:
            module_name = f"Module_{m_idx+1}"

        log(f"\n=== Module {m_idx+1}: {module_name} ===")

        os.makedirs(module_name, exist_ok=True)

        items = module.query_selector_all("a.ig-title")
        log(f"\n=== Module {m_idx+1}: {module_name} ===")

        for i in range(len(items)):
            try:
                start_time = time.time()

                modules = page.query_selector_all(".context_module")
                module = modules[m_idx]
                items = module.query_selector_all("a.ig-title")

                if i >= len(items):
                    continue

                item = items[i]
                href = item.get_attribute("href")
                name = clean_name(item.inner_text())

                log(f"  → Item {i + 1}/{len(items)}: {name}")
                log(f"    Opening: {href}")

                item.click()
                page.wait_for_load_state("networkidle")

                log("Page loaded")

                download_btn = page.query_selector("a[download]")

                if download_btn:
                    log("Found download button")

                    with page.expect_download(timeout=15000) as download_info:
                        download_btn.click()

                    download = download_info.value
                    filename = clean_name(download.suggested_filename)

                    save_path = os.path.join(module_name, filename)
                    download.save_as(save_path)

                    elapsed = time.time() - start_time
                    log(f"Downloaded: {filename} ({elapsed:.2f}s)")

                else:
                    log("Not a downloadable file")

                page.goto(URL)
                page.wait_for_selector(".context_module")

            except Exception as e:
                log(f"ERROR on item {i + 1}: {e}")
                page.goto(URL)
                page.wait_for_selector(".context_module")

    browser.close()