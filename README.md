
# Canvas Module Downloader (UCLA )

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Playwright](https://img.shields.io/badge/Automation-Playwright-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A lightweight Python tool that downloads files from **Bruin Learn (Canvas)** course modules using browser automation.
Designed for UCLA students where Canvas API access is restricted. This tool can be adapted for other Canvas instances and institutions, but 
current implementation (including URLs and selectors) is specifically configured for UCLA Bruin Learn.

If used with other campuses, URLs, login, and file structure may/will be different.
---

## Features

* No API token required (works with student accounts)
* Automated module expansion and navigation
* Downloads all direct file attachments
* Organizes files by module
* Simple, transparent, and customizable

---

## How It Works

Because student Canvas accounts have limited API access, this tool simulates a real browser session:

1. Log in once and save session (`state.json`)
2. Open the Modules page
3. Expand all modules
4. Visit each item
5. Download files when available

---

## Project Structure

```
Canvas-Downloader/
├── Login_Script.py
├── Auto_Download.py
├── state.json          (Generated after login)
└── README.md
```

---

## Requirements

* Python 3.9 or higher
* Playwright

Install dependencies:

```bash
pip install playwright
playwright install
```

---

## Setup

### 1. Authenticate (First-Time Only)

```bash
python Login_Script.py
```

* A browser window will open
* Log in at: [https://bruinlearn.ucla.edu](https://bruinlearn.ucla.edu)
* Return to terminal and press **Enter**

This creates `state.json` (your saved login session).

> `state.json` grants access to your account. Do not share.

---

### 2. Set Course URL

Edit `Auto_Download.py`:

```python
URL = "https://bruinlearn.ucla.edu/courses/YOUR_COURSE_ID/modules"
```

Replace `YOUR_COURSE_ID` with your actual course ID.

---

## Usage

```bash
python Auto_Download.py
```

The script will:

* Open the modules page
* Expand all modules
* Iterate through items
* Download files automatically

A browser window is shown (`headless=False`) so you can monitor progress.

---

## Output

Files are saved into folders named after each module:

```
Canvas-Downloader/
├── Week 1 - Introduction/
│   ├── syllabus.pdf
│   └── lecture_slides.pdf
├── Week 2 - Chapter 1/
│   ├── lecture_slides.pdf
│   └── notes.pdf
│   └── assignment.docx
```

---

## Limitations

* Only supports **direct downloads** (PDF, DOCX, ZIP, etc.)
* Does not support:

  * Google Drive links
  * Embedded videos (YouTube, Kaltura)
  * External tools
* Skips non-file items (quizzes, discussions, pages)
* No resume functionality
* May break if Canvas UI changes
* Default timeout: 15 seconds

---

## Troubleshooting

| Problem              | Solution                      |
| -------------------- | ----------------------------- |
| `state.json` missing | Run login script again        |
| No files downloaded  | Item may not be a direct file |
| Timeout errors       | Increase timeout value        |
| Wrong course         | Check URL                     |
| Playwright issues    | Reinstall dependencies        |

---

## Customization

* **Run in background**

```python
headless=True
```

* **Change download directory**

```python
os.makedirs(os.path.join("downloads", module_name), exist_ok=True)
```

* **Skip existing files**

```python
if os.path.exists(path):
    continue
```

* **Increase timeout**

```python
timeout=30000
```

---

## Responsible Use

This tool is intended for **personal academic use only**.

Users must:

* Follow UCLA policies
* Respect copyright
* Avoid redistribution of protected content

---

## License

This project is licensed under the **MIT License**.

---

## Contributing

Contributions are welcome. If Canvas updates break selectors, update elements such as:

```python
a[download]
```

Feel free to submit improvements or fixes.

---

## Disclaimer

This project is not affiliated with UCLA or Canvas.
Use at your own risk.

---

