import os
import re
from pathlib import Path

JOB_ROOT = Path(r"G:\Manufacturing\JOB FOLDERS\2024 Orders")


def normalize_job_number(job_number: str) -> str:
    if not job_number or not str(job_number).strip():
        raise ValueError("Job number is blank.")

    job_number = str(job_number).strip().upper()
    job_number = re.sub(r"\s+", " ", job_number)
    return job_number


def extract_core_job(job_number: str) -> str:
    cleaned = normalize_job_number(job_number)

    match = re.match(r"^([A-Z])\s*(\d+)", cleaned)
    if not match:
        raise ValueError("Format must look like D24836 or D24836 FAI")

    prefix = match.group(1)
    num = match.group(2)
    return f"{prefix}{num}"


def build_job_folder_path(job_number: str) -> Path:
    core_job = extract_core_job(job_number)
    return JOB_ROOT / core_job


def find_matching_job_folders(job_number: str):
    core_job = extract_core_job(job_number)

    if not JOB_ROOT.exists():
        raise FileNotFoundError(f"Job root not found: {JOB_ROOT}")

    matches = []
    core_upper = core_job.upper()

    for item in JOB_ROOT.iterdir():
        if item.is_dir() and item.name.upper().startswith(core_upper):
            matches.append(item)

    matches.sort(key=lambda p: p.name.upper())

    if not matches:
        raise FileNotFoundError(
            f"No matching folder found.\n"
            f"Searched in:\n{JOB_ROOT}\n\n"
            f"Looking for folders starting with:\n{core_job}"
        )

    return matches


def open_job_folder(job_number: str):
    try:
        matches = find_matching_job_folders(job_number)
        folder_path = matches[0]
        os.startfile(str(folder_path))

        if len(matches) == 1:
            return True, f"✅ Opened:\n{folder_path}"

        match_list = "\n".join(str(p.name) for p in matches[:10])
        extra_note = ""
        if len(matches) > 10:
            extra_note = f"\n...and {len(matches) - 10} more"

        return True, (
            f"✅ Opened:\n{folder_path}\n\n"
            f"Other matches found:\n{match_list}{extra_note}"
        )

    except Exception as e:
        return False, f"❌ Error: {str(e)}"