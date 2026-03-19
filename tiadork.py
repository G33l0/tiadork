#!/usr/bin/env python3
"""
TiaDork — Google Dork Combiner
Author  : g33l0
Telegram: https://t.me/x0x0h33l0
Requires: Python 3.9+, colorama, tqdm (optional)
"""

import os
import sys
import math
import argparse
from datetime import datetime
from typing import List, Optional, Tuple
from colorama import init, Fore, Style

# ── Python version guard ──────────────────────────────────────────────────────
if sys.version_info < (3, 9):
    sys.exit("[ERROR] TiaDork requires Python 3.9 or higher.")

init(autoreset=True)

# ── Optional tqdm import ──────────────────────────────────────────────────────
try:
    from tqdm import tqdm as _tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

__version__ = "1.0.0"

# Progress bar threshold: only show bar when keyword count >= this value
TQDM_THRESHOLD = 100

# Default chunk size for split output
DEFAULT_CHUNK_SIZE = 500

# ─────────────────────────────────────────────────────────────────────────────
# BUILT-IN WORDPRESS TEMPLATES
# ─────────────────────────────────────────────────────────────────────────────

BUILTIN_TEMPLATES: List[str] = [
    "Comentarios en Hello world!", "author/admin", "uncategorized/hello-world",
    "category/sin-categoria", "uncategorized", "non-classé",
    "Proudly powered by WordPress",
    "Welcome to WordPress. This is your first post.",
    "Just another WordPress site",
    "Mr WordPress on Hello world!", "/wp/hello-world/", "wp-content/uploads",
    "wp-includes/js", "wp-json/wp", "wp-login.php", "wp-admin",
    "powered by WordPress", "Leave a reply", "Posted in Uncategorized",
    "Sample Page", "Archives", "Hello world!", "meta/wp",
    "wp-content/plugins", "wp-content/themes",
    "Site is proudly powered by WordPress", "Log in to your site",
    "Edit or delete it, then start writing!", "You may delete this page.",
    "Search for:", "Nothing Found", "index of /wp-content/",
    "index of /wp-includes/", "inurl:/wp-content/plugins/",
    "inurl:/wp-content/themes/", "inurl:/wp-json/wp/v2/",
    "inurl:?s=", "inurl:tag/hello-world", "inurl:author=",
    "intitle:Hello world! site:wordpress.com", "intitle:Sample Page",
    "intitle:Welcome", "intitle:Index of /wp-admin",
    "intext:'This site uses Akismet to reduce spam'",
    "intext:'Powered by WordPress and the'",
    "intext:'You can log in using the admin area'",
    "inurl:/wp-comments-post.php", "inurl:/xmlrpc.php",
    "inurl:/wp-content/cache/", "inurl:/wp-content/backups/",
    "inurl:/wp-config.php.bak",
]

# ─────────────────────────────────────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────────────────────────────────────

def _box_row(content: str, inner: int) -> str:
    """Return a box content row padded to exactly `inner` chars between walls."""
    return "  \u2502" + content.ljust(inner) + "\u2502"


def display_banner() -> None:
    """
    ASCII art: TiaDork (7 letters, block-style box-drawing characters).
    The meta box is built programmatically — every line is mathematically
    guaranteed to be the same length regardless of version string length.
    """
    art = (
        "\n"
        "  \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2588\u2557  \u2588\u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2557  \u2588\u2588\u2557\n"
        "  \u255a\u2550\u2550\u2588\u2588\u2554\u2550\u2550\u255d\u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2554\u2550\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2551 \u2588\u2588\u2554\u255d\n"
        "     \u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2551\u2588\u2588\u2551  \u2588\u2588\u2551\u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u2588\u2588\u2588\u2588\u2588\u2554\u255d \n"
        "     \u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2551\u2588\u2588\u2551  \u2588\u2588\u2551\u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2554\u2550\u2588\u2588\u2557 \n"
        "     \u2588\u2588\u2551   \u2588\u2588\u2551\u2588\u2588\u2551  \u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u255a\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u2588\u2588\u2551  \u2588\u2588\u2551\u2588\u2588\u2551  \u2588\u2588\u2557\n"
        "     \u255a\u2550\u255d   \u255a\u2550\u255d\u255a\u2550\u255d  \u255a\u2550\u255d\u255a\u2550\u2550\u2550\u2550\u2550\u255d  \u255a\u2550\u2550\u2550\u2550\u2550\u255d \u255a\u2550\u255d  \u255a\u2550\u255d\u255a\u2550\u255d  \u255a\u2550\u255d\n"
    )

    # Box: 57 dashes → border len = 61, inner content width = 57
    N     = 57
    top   = "  \u250c" + "\u2500" * N + "\u2510"
    bot   = "  \u2514" + "\u2500" * N + "\u2518"
    inner = N

    meta = [
        top,
        _box_row(f"            TiaDork \u2014 Google Dork Combiner", inner),
        _box_row(f"                         g33l0", inner),
        _box_row(f"                 https://t.me/x0x0h33l0", inner),
        bot,
    ]

    print(Fore.RED + art + Style.RESET_ALL)
    for line in meta:
        print(Fore.RED + line + Style.RESET_ALL)
    print()


# ─────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _divider(width: int = 57) -> str:
    return Fore.RED + "\u2500" * width + Style.RESET_ALL

def _step(n: int, label: str) -> None:
    print(f"\n{Fore.RED}  [{n}]{Style.RESET_ALL} {Fore.WHITE}{label}{Style.RESET_ALL}")

def _ok(msg: str) -> None:
    print(f"{Fore.GREEN}      [+] {msg}{Style.RESET_ALL}")

def _info(msg: str) -> None:
    print(f"{Fore.BLUE}      [*] {msg}{Style.RESET_ALL}")

def _warn(msg: str) -> None:
    print(f"{Fore.YELLOW}      [!] {msg}{Style.RESET_ALL}")

def _err(msg: str) -> None:
    print(f"{Fore.RED}      [ERROR] {msg}{Style.RESET_ALL}")

def _prompt(label: str) -> str:
    """Display a labelled prompt and return the stripped user input."""
    print(f"      {Fore.WHITE}{label}: {Style.RESET_ALL}", end="", flush=True)
    return input().strip()


# ─────────────────────────────────────────────────────────────────────────────
# FILE I/O
# ─────────────────────────────────────────────────────────────────────────────

def read_file(filename: str) -> List[str]:
    """Return non-empty, non-comment lines from a UTF-8 text file."""
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            return [
                line.strip()
                for line in fh
                if line.strip() and not line.startswith("#")
            ]
    except FileNotFoundError:
        _err(f"File not found: {filename}")
        sys.exit(1)
    except PermissionError:
        _err(f"Permission denied: {filename}")
        sys.exit(1)
    except UnicodeDecodeError:
        _err(f"File is not valid UTF-8: {filename}")
        sys.exit(1)
    except OSError as exc:
        _err(f"Could not read '{filename}': {exc}")
        sys.exit(1)


def write_file(filename: str, lines: List[str]) -> None:
    """Write lines to a UTF-8 text file, one entry per line."""
    try:
        with open(filename, "w", encoding="utf-8") as fh:
            for line in lines:
                fh.write(line + "\n")
    except PermissionError:
        _err(f"Permission denied writing to: {filename}")
        sys.exit(1)
    except OSError as exc:
        _err(f"Write failed for '{filename}': {exc}")
        sys.exit(1)


def chunk_filename(base: str, part: int, total_parts: int) -> str:
    """
    Derive a zero-padded chunk filename from a base output name.

    Examples:
        Dorks_20250618.txt, part=2, total=3  →  Dorks_20250618_part2.txt
        MyDorks,            part=1, total=12 →  MyDorks_part01.txt
    """
    pad  = len(str(total_parts))
    stem, sep, ext = base.rpartition(".")
    if not stem:            # filename has no dot
        stem, ext = base, "txt"
    return f"{stem}_part{str(part).zfill(pad)}.{ext}"


def write_chunks(base: str, lines: List[str], size: int) -> List[str]:
    """
    Split `lines` into chunks of `size` and write each to its own file.
    Returns the list of filenames written.
    """
    total   = math.ceil(len(lines) / size)
    written = []
    for i in range(1, total + 1):
        chunk    = lines[(i - 1) * size : i * size]
        filename = chunk_filename(base, i, total)
        write_file(filename, chunk)
        written.append(filename)
    return written


# ─────────────────────────────────────────────────────────────────────────────
# CORE LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def remove_duplicates(items: List[str]) -> List[str]:
    """Return items in original order with all duplicates removed."""
    seen:   set       = set()
    result: List[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def generate_dork_combinations(
    templates: List[str],
    keywords:  List[str],
) -> List[str]:
    """
    Cross-join templates × keywords into ("template")keyword strings.

    When len(keywords) >= TQDM_THRESHOLD and tqdm is installed, a progress
    bar is shown over the template loop. Otherwise falls back to plain iteration.
    """
    results: List[str] = []

    use_bar = HAS_TQDM and len(keywords) >= TQDM_THRESHOLD
    iterator = (
        _tqdm(
            templates,
            desc="      Generating",
            unit=" tmpl",
            bar_format="{l_bar}{bar:28}{r_bar}",
            ncols=72,
            colour="red",
        )
        if use_bar
        else templates
    )

    for template in iterator:
        if not template:
            continue
        for keyword in keywords:
            if keyword:
                results.append(f'("{template}"){keyword}')

    return results


# ─────────────────────────────────────────────────────────────────────────────
# FILE PREVIEW HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _show_file_preview(lines: List[str], label: str = "Preview", n: int = 3) -> None:
    """Display the first `n` lines of a list inside a labelled preview box."""
    preview = lines[:n]
    border  = f"      {Fore.YELLOW}" + "\u2500" * 50 + Style.RESET_ALL
    print(border)
    print(f"      {Fore.YELLOW}  {label} (first {len(preview)} line{'s' if len(preview) != 1 else ''}):{Style.RESET_ALL}")
    for i, line in enumerate(preview, 1):
        print(f"      {Fore.CYAN}  {i}. {line}{Style.RESET_ALL}")
    if len(lines) > n:
        print(f"      {Fore.WHITE}     ... +{len(lines) - n} more{Style.RESET_ALL}")
    print(border)


# ─────────────────────────────────────────────────────────────────────────────
# WIZARD STEPS
# ─────────────────────────────────────────────────────────────────────────────

def wizard_input_file(step_n: int) -> str:
    """
    Step N — Loop until a valid keyword file is selected.
    After finding the file, shows a 3-line preview and asks for confirmation
    so the user can verify they selected the right file before continuing.
    """
    _step(step_n, "Select keyword input file")
    while True:
        path = _prompt("Path to keywords file")
        if not path:
            _warn("No path entered. Please try again.")
            continue
        if not os.path.isfile(path):
            _warn(f"File not found: '{path}'. Please try again.")
            continue

        _ok(f"Found: {os.path.abspath(path)}")

        # ── Input validation feedback: preview first 3 lines ─────────────────
        raw = read_file(path)
        if not raw:
            _warn("File appears empty (no valid lines found). Please choose another file.")
            continue

        _show_file_preview(raw, label="Keyword file contents")

        confirm = _prompt(
            f"Is this the correct file? [{Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}]"
        ).lower()
        if confirm in ("", "y", "yes"):
            return path
        _warn("Okay, let's pick a different file.")


def wizard_template_source(step_n: int) -> Tuple[List[str], str]:
    """
    Step N — Ask whether to use the built-in 51 WordPress templates or load
    a custom template file. Returns (template_list, source_label).
    """
    _step(step_n, "Select template source")
    print(f"      {Fore.WHITE}  [1] Built-in WordPress templates ({len(BUILTIN_TEMPLATES)} templates){Style.RESET_ALL}")
    print(f"      {Fore.WHITE}  [2] Load custom template file{Style.RESET_ALL}")
    print()

    while True:
        choice = _prompt(
            f"Choose source [{Fore.GREEN}1{Fore.WHITE}/{Fore.YELLOW}2{Fore.WHITE}]"
        ).strip()

        if choice in ("", "1"):
            _ok(f"Using built-in WordPress templates ({len(BUILTIN_TEMPLATES)} templates)")
            return BUILTIN_TEMPLATES, f"built-in ({len(BUILTIN_TEMPLATES)} templates)"

        if choice == "2":
            while True:
                tpl_path = _prompt("Path to custom templates file")
                if not tpl_path:
                    _warn("No path entered. Please try again.")
                    continue
                if not os.path.isfile(tpl_path):
                    _warn(f"File not found: '{tpl_path}'. Please try again.")
                    continue

                _ok(f"Found: {os.path.abspath(tpl_path)}")
                raw_tpl = read_file(tpl_path)
                if not raw_tpl:
                    _warn("Template file is empty. Please choose another file.")
                    continue

                unique_tpl = remove_duplicates(raw_tpl)
                removed    = len(raw_tpl) - len(unique_tpl)

                _ok(
                    f"Loaded {len(unique_tpl)} unique template(s)"
                    + (f"  (removed {removed} duplicate{'s' if removed != 1 else ''})"
                       if removed else "")
                )
                _show_file_preview(unique_tpl, label="Template file contents")

                confirm = _prompt(
                    f"Use this template file? [{Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}]"
                ).lower()
                if confirm in ("", "y", "yes"):
                    label = f"custom: {os.path.basename(tpl_path)} ({len(unique_tpl)} templates)"
                    return unique_tpl, label
                _warn("Okay, let's pick a different template file.")

        _warn("Please enter 1 or 2.")


def wizard_output_file(step_n: int) -> str:
    """Step N — Prompt for output filename; default to timestamped name."""
    _step(step_n, "Set output filename")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default   = f"Dorks_{timestamp}.txt"
    print(
        f"      {Fore.WHITE}Output filename "
        f"[{Fore.YELLOW}{default}{Fore.WHITE}]: {Style.RESET_ALL}",
        end="", flush=True,
    )
    name   = input().strip()
    chosen = name if name else default
    _ok(f"Output: {chosen}")
    return chosen


def wizard_split_output(step_n: int, total_dorks: int) -> Tuple[bool, int]:
    """
    Step N — Ask whether to split the output into chunks.
    Returns (do_split: bool, chunk_size: int).
    """
    _step(step_n, "Split output into chunks?")
    _info(f"Total dorks to write: {total_dorks}")
    print(
        f"      {Fore.WHITE}Split into multiple files? "
        f"[{Fore.GREEN}y{Fore.WHITE}/{Fore.RED}N{Fore.WHITE}]: {Style.RESET_ALL}",
        end="", flush=True,
    )
    ans = input().strip().lower()

    if ans not in ("y", "yes"):
        _info("Single-file output selected.")
        return False, 0

    # Prompt for chunk size
    while True:
        raw = _prompt(
            f"Dorks per chunk [{Fore.YELLOW}{DEFAULT_CHUNK_SIZE}{Fore.WHITE}]"
        )
        if not raw:
            size = DEFAULT_CHUNK_SIZE
            break
        if raw.isdigit() and int(raw) > 0:
            size = int(raw)
            break
        _warn("Please enter a positive integer.")

    total_chunks = math.ceil(total_dorks / size)
    _ok(f"Will split into {total_chunks} file(s) of up to {size} dorks each.")
    return True, size


def wizard_confirm(
    step_n:        int,
    input_file:    str,
    template_label: str,
    output_file:   str,
    keyword_count: int,
    template_count: int,
    do_split:      bool,
    chunk_size:    int,
) -> bool:
    """Step N — Display full settings summary and require explicit confirmation."""
    _step(step_n, "Review & confirm")
    border = f"      {Fore.BLUE}" + "\u2500" * 54 + Style.RESET_ALL
    est = keyword_count * template_count

    print(border)
    print(f"      {Fore.WHITE}  Input file  : {Fore.CYAN}{os.path.abspath(input_file)}{Style.RESET_ALL}")
    print(f"      {Fore.WHITE}  Templates   : {Fore.CYAN}{template_label}{Style.RESET_ALL}")
    print(f"      {Fore.WHITE}  Output file : {Fore.CYAN}{output_file}{Style.RESET_ALL}")
    print(f"      {Fore.WHITE}  Keywords    : {Fore.CYAN}{keyword_count}{Style.RESET_ALL}")
    print(f"      {Fore.WHITE}  Est. dorks  : {Fore.CYAN}{est}{Style.RESET_ALL}")
    if do_split:
        chunks = math.ceil(est / chunk_size)
        print(f"      {Fore.WHITE}  Split into  : {Fore.CYAN}{chunks} file(s) × {chunk_size} dorks{Style.RESET_ALL}")
    else:
        print(f"      {Fore.WHITE}  Output mode : {Fore.CYAN}single file{Style.RESET_ALL}")
    if not HAS_TQDM and keyword_count >= TQDM_THRESHOLD:
        print(
            f"      {Fore.YELLOW}  Note: install tqdm for a progress bar "
            f"(pip install tqdm){Style.RESET_ALL}"
        )
    print(border)
    print()

    while True:
        ans = _prompt(
            f"Proceed? [{Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}]"
        ).lower()
        if ans in ("", "y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        _warn("Please enter Y or N.")


def wizard_preview(step_n: int, dorks: List[str]) -> None:
    """Step N — Print a short preview of the generated dorks."""
    _step(step_n, "Preview")
    preview_count = min(8, len(dorks))
    border = f"      {Fore.YELLOW}" + "\u2500" * 52 + Style.RESET_ALL
    print(border)
    for i, dork in enumerate(dorks[:preview_count], 1):
        print(f"      {Fore.CYAN}{i:2d}. {dork}{Style.RESET_ALL}")
    if len(dorks) > preview_count:
        remaining = len(dorks) - preview_count
        print(f"      {Fore.WHITE}    ... +{remaining} more entries{Style.RESET_ALL}")
    print(border)


def wizard_run_again() -> bool:
    """Ask the user whether to start a new session."""
    print()
    ans = _prompt(
        f"Run again with a different file? [{Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}]"
    ).lower()
    return ans in ("y", "yes")


# ─────────────────────────────────────────────────────────────────────────────
# SESSION
# ─────────────────────────────────────────────────────────────────────────────

def run_session() -> None:
    """Execute one complete wizard session."""

    # ── Step 1: Select & validate keyword input file ─────────────────────────
    input_file = wizard_input_file(1)

    # ── Step 2: Load & deduplicate keywords ──────────────────────────────────
    _step(2, "Loading keywords")
    raw_keywords     = read_file(input_file)
    unique_keywords  = remove_duplicates(raw_keywords)
    removed_kw       = len(raw_keywords) - len(unique_keywords)
    _ok(
        f"Loaded {len(unique_keywords)} unique keyword(s)"
        + (f"  (removed {removed_kw} duplicate{'s' if removed_kw != 1 else ''})"
           if removed_kw else "")
    )

    # (read_file exits on empty; guard here is belt-and-braces)
    if not unique_keywords:
        _err("Keyword file is empty. Aborting.")
        return

    # ── Step 3: Choose template source (built-in or custom) ──────────────────
    active_templates, template_label = wizard_template_source(3)

    # ── Step 4: Choose output filename ───────────────────────────────────────
    output_file = wizard_output_file(4)

    # ── Step 5: Generate — needed before split dialog so we know total count ─
    _step(5, "Generating dork combinations")
    if not HAS_TQDM and len(unique_keywords) >= TQDM_THRESHOLD:
        _info(
            f"Tip: install tqdm for a progress bar  "
            f"(pip install tqdm)"
        )
    else:
        _info("Combining templates with keywords...")

    dork_combinations = generate_dork_combinations(active_templates, unique_keywords)
    _ok(f"{len(dork_combinations)} dork combination(s) generated")

    # ── Step 6: Preview ───────────────────────────────────────────────────────
    wizard_preview(6, dork_combinations)

    # ── Step 7: Split output? ─────────────────────────────────────────────────
    do_split, chunk_size = wizard_split_output(7, len(dork_combinations))

    # ── Step 8: Review & confirm ──────────────────────────────────────────────
    if not wizard_confirm(
        step_n         = 8,
        input_file     = input_file,
        template_label = template_label,
        output_file    = output_file,
        keyword_count  = len(unique_keywords),
        template_count = len(active_templates),
        do_split       = do_split,
        chunk_size     = chunk_size,
    ):
        _warn("Aborted by user.")
        return

    # ── Step 9: Write output file(s) ─────────────────────────────────────────
    _step(9, "Writing output file(s)")

    if do_split:
        written = write_chunks(output_file, dork_combinations, chunk_size)
        for fn in written:
            count = min(chunk_size, len(dork_combinations) - (written.index(fn) * chunk_size))
            _ok(f"  {fn}  ({count} dorks)  →  {os.path.abspath(fn)}")
        print(
            f"\n  {Fore.GREEN}[\u2713] Done! "
            f"{len(dork_combinations)} dorks split across {len(written)} file(s)."
            f"{Style.RESET_ALL}\n"
        )
    else:
        write_file(output_file, dork_combinations)
        _ok(f"Saved to: {os.path.abspath(output_file)}")
        print(
            f"\n  {Fore.GREEN}[\u2713] Done! "
            f"{len(dork_combinations)} dorks written to '{output_file}'"
            f"{Style.RESET_ALL}\n"
        )


# ─────────────────────────────────────────────────────────────────────────────
# ARGUMENT PARSING
# ─────────────────────────────────────────────────────────────────────────────

def parse_args() -> None:
    parser = argparse.ArgumentParser(
        prog="TiaDork",
        description="Google Dork Combiner — Built for Pentesters",
        epilog="Telegram: https://t.me/x0x0h33l0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"TiaDork v{__version__}",
    )
    parser.parse_args()


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parse_args()
    display_banner()

    print(_divider())
    print(f"{Fore.RED}  TiaDork Interactive Wizard{Style.RESET_ALL}")
    print(_divider())

    while True:
        run_session()
        if not wizard_run_again():
            break

    print(f"\n{Fore.RED}  Goodbye. Stay sharp.{Style.RESET_ALL}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}  [!] Interrupted by user. Goodbye.{Style.RESET_ALL}\n")
        sys.exit(0)