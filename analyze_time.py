import warnings
warnings.filterwarnings("ignore")

import datetime
import subprocess
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.csv import partition_csv
from pathlib import Path

# Setup dates
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

date_fmt = "%Y-%m-%d"
today_str = today.strftime(date_fmt)
yesterday_str = yesterday.strftime(date_fmt)

# Define file locations
download_dir = Path.home() / "Downloads"
file_base_today = f"Toggl_Track_summary_report_{today_str}_{today_str}"
file_base_yesterday = f"Toggl_Track_summary_report_{yesterday_str}_{yesterday_str}"

# Utility to find file
def find_file(file_base):
    for ext in ['csv', 'pdf']:
        path = download_dir / f"{file_base}.{ext}"
        if path.exists():
            return path, ext
    return None, None

# Find files
file_today, ext_today = find_file(file_base_today)
file_yesterday, ext_yesterday = find_file(file_base_yesterday)

if not file_today:
    print(f"❌ No file found for today ({today_str})")
    exit(1)
else:
    print(f"✅ Found today's file: {file_today}")

if not file_yesterday:
    print(f"⚠️ No file found for yesterday ({yesterday_str}) — continuing with just today's data")
else:
    print(f"✅ Found yesterday's file: {file_yesterday}")

# Extract structured data using Unstructured
def extract_text(file_path, file_type):
    if file_type == "pdf":
        elements = partition_pdf(filename=str(file_path), strategy="hi_res",extract_images_in_pdf=True)
    elif file_type == "csv":
        elements = partition_csv(filename=str(file_path))
    else:
        return ""
    return "\n".join([el.text for el in elements if el.text])

text_today = extract_text(file_today, ext_today)
text_yesterday = extract_text(file_yesterday, ext_yesterday) if file_yesterday else ""

# Prepare prompt for LLM
prompt = f"""
You are my productivity coach. You will receive structured time tracking data for TODAY and YESTERDAY as plain text.

### TODAY ({today_str})
{text_today}

### YESTERDAY ({yesterday_str})
{text_yesterday}

Your task is to:
- Compare the time and projects between TODAY and YESTERDAY.
- ONLY use the entries listed under each specific date — never infer or carry over tasks between days.
- Do not assume any project happened on both days unless it appears in both TODAY and YESTERDAY sections.
- Assign a productivity score for TODAY (0–100), based on time usage, task quality, and inclusion of rest or walking breaks.
- Suggest 2–4 improvements to my time usage. Breaks and walking are considered positive.
- Your output should be in clean markdown
- Focus only on the "TIME ENTRY" and "DURATION" sections of the pdf files and don't look at other sections.
- Focus only on the "Description" and "Duration" columns of the csv files and don't look at other columns.
- Make the output specific to the data provided, and do not include any generic advice or suggestions. 
- Display the report with TODAY time and projects, YESTERDAY time and projects,  the productivity score, and recommendations for improvement. 
- Important: Do NOT hallucinate or infer data. ONLY use the fields explicitly provided under each date.
"""

# Call LLM using Ollama
print("🧠 Running analysis with local LLM...")
ollama_command = ["ollama", "run", "llama3.2"]
result = subprocess.run(ollama_command, input=prompt.encode(), capture_output=True)
output_text = result.stdout.decode()

# Save result
output_file = Path("time_analyze.md")
output_file.write_text(output_text)
print(f"✅ Analysis saved to: {output_file.resolve()}")

