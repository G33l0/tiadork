<div align="center">

```
  ████████╗██╗ █████╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗
  ╚══██╔══╝██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝
    ██║   ██║███████║██║  ██║██║   ██║██████╔╝█████╔╝
    ██║   ██║██╔══██║██║  ██║██║   ██║██╔══██╗██╔═██╗
     ██║   ██║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██╗
     ╚═╝   ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
```

**Google Dork Combiner — Built for Pentesters & Bug Bounty Hunters**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-red?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)

**Author:** [g33l0](https://t.me/x0x0h33l0) &nbsp;|&nbsp; **Telegram:** [@x0x0h33l0](https://t.me/x0x0h33l0)

</div>

---

## What is TiaDork?

**TiaDork** is an interactive command-line wizard that combines a curated list of dork templates with your own keyword list to mass-generate targeted Google search dorks for use in reconnaissance and penetration testing engagements.

Instead of writing dorks one by one, you feed in a keywords file (domains, paths, targets) and TiaDork generates every combination automatically — saving hours of manual work.

---

## Features

| Feature | Description |
|---|---|
| **Interactive wizard** | 9-step guided flow with confirmation before generating |
| **Input validation feedback** | Shows first 3 lines of your keyword file for visual confirmation before proceeding |
| **51 built-in WordPress templates** | Covers login pages, exposed configs, sensitive paths, API endpoints, and more |
| **Custom template files** | Load your own `.txt` template file for any target technology |
| **Progress bar** | tqdm progress bar auto-activates when keyword count ≥ 100 (requires `pip install tqdm`) |
| **Split output** | Optionally chunk output into N-dork-per-file sets for manageable manual testing |
| **Timestamped output** | Every run gets a unique filename — never overwrites a previous result |
| **Duplicate removal** | Deduplicates both keywords and generated dorks |
| **Safe error handling** | Specific messages for FileNotFoundError, PermissionError, UnicodeDecodeError, OSError |
| **Ctrl+C safe** | Clean exit with goodbye message on interrupt |
| **Cross-platform** | Windows, Linux, macOS (colorama handles ANSI colour on all platforms) |

---

## Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.9+ | Required |
| colorama | 0.4.6+ | Required |
| tqdm | 4.64.0+ | Optional — progress bar for large keyword lists |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/g33l0/tiadork.git
cd tiadork
```

### 2. Create a virtual environment (recommended)

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
# Installs colorama (required) + tqdm (optional progress bar)
pip install -r requirements.txt
```

> To install only the required dependency: `pip install colorama`

---

## Usage

### Run the interactive wizard

```bash
python3 Dork_Combiners.py
```

### Check version

```bash
python3 Dork_Combiners.py --version
```

---

## Wizard Walkthrough

The wizard guides you through **9 steps**:

```
  [1] Select keyword input file
      Path to keywords file: keywords_example.txt
      ──────────────────────────────────────────────────
        Keyword file contents (first 3 lines):
        1. site:example.com
        2. inurl:admin
        3. filetype:sql
        ... +11 more
      ──────────────────────────────────────────────────
      Is this the correct file? [Y/n]: y

  [2] Loading keywords
      [+] Loaded 14 unique keyword(s)

  [3] Select template source
        [1] Built-in WordPress templates (51 templates)
        [2] Load custom template file
      Choose source [1/2]: 1
      [+] Using built-in WordPress templates (51 templates)

  [4] Set output filename
      Output filename [Dorks_20250618_142301.txt]:

  [5] Generating dork combinations
      [*] Combining templates with keywords...
      [+] 700 dork combination(s) generated

  [6] Preview
      ────────────────────────────────────────────────────
       1. ("wp-login.php")site:example.com
       2. ("wp-login.php")inurl:admin
       ...

  [7] Split output into chunks?
      [*] Total dorks to write: 700
      Split into multiple files? [y/N]: y
      Dorks per chunk [500]: 500
      [+] Will split into 2 file(s) of up to 500 dorks each.

  [8] Review & confirm
      ──────────────────────────────────────────────────────
        Input file  : /home/user/tiadork/keywords_example.txt
        Templates   : built-in (51 templates)
        Output file : Dorks_20250618_142301.txt
        Keywords    : 14
        Est. dorks  : 700
        Split into  : 2 file(s) × 500 dorks
      ──────────────────────────────────────────────────────
      Proceed? [Y/n]: y

  [9] Writing output file(s)
      [+] Dorks_20250618_142301_part1.txt  (500 dorks)
      [+] Dorks_20250618_142301_part2.txt  (200 dorks)

  [✓] Done! 700 dorks split across 2 file(s).
```

---

## File Formats

### Keyword file

One keyword per line. Lines starting with `#` are comments and are ignored.

```text
# My target keywords
site:example.com
inurl:admin
filetype:sql
filetype:env
```

See `keywords_example.txt` for a ready-to-use starting point.

### Custom template file

Same format as a keyword file — one template per line, `#` for comments.

```text
# Apache templates
intitle:"Apache Status"
Index of /
intitle:"phpinfo()"
inurl:config.php
```

See `templates_example.txt` for a categorised example file covering Apache, PHP, login panels, exposed files, and multiple CMS targets.

---

## Output Format

Each generated dork follows the pattern:

```
("TEMPLATE")KEYWORD
```

**Example output:**

```
("wp-login.php")site:example.com
("wp-admin")inurl:admin
("index of /wp-content/")filetype:sql
("wp-config.php.bak")site:*.gov
```

These are ready to paste directly into Google, Bing, DuckDuckGo, or any search engine that supports advanced operators.

---

## Split Output

When splitting is enabled, files are named using zero-padded part numbers:

| Total chunks | Example filenames |
|---|---|
| 1–9 | `Dorks_..._part1.txt`, `Dorks_..._part9.txt` |
| 10–99 | `Dorks_..._part01.txt`, `Dorks_..._part99.txt` |
| 100+ | `Dorks_..._part001.txt`, `Dorks_..._part999.txt` |

---

## Project Structure

```
tiadork/
├── Dork_Combiners.py       # Main tool
├── keywords_example.txt    # Sample keyword input file
├── templates_example.txt   # Sample custom template file
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── CHANGELOG.md            # Release history
├── LICENSE                 # MIT license
└── README.md               # This file
```

---

## Legal Disclaimer

> TiaDork is intended **strictly for authorized security testing, bug bounty programs, and educational purposes**.
> Use of this tool against systems without **explicit written permission** is illegal and unethical.
> The author holds **no responsibility** for misuse or damage caused by this tool.
> Always operate within the scope of your engagement.

---

## Contact

| Platform | Handle |
|---|---|
| Telegram | [@x0x0h33l0](https://t.me/x0x0h33l0) |
| GitHub | [g33l0](https://github.com/g33l0/IamG2) |

---

<div align="center">
  <sub>Built with ❤️ for the offensive security community</sub>
</div>
