#!/bin/bash

# Help menu
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  echo "🧠 Time Analyzer AI — Bash Script"
  echo
  echo "Usage:"
  echo "  ./analyze_time.sh"
  echo
  echo "Description:"
  echo "  Analyzes your daily time-tracking log using a local LLM for privacy to generate productivity insights."
  echo
  exit 0
fi

# Define the download folder
DOWNLOAD_DIR="$HOME/Downloads"

# Get today's and yesterday's dates in the format used in the filename
TODAY=$(date +"%Y-%m-%d")
YESTERDAY=$(date -v-1d +"%Y-%m-%d") # Use -v-1d for macOS to get yesterday's date
# Expected filename bases
FILENAME_BASE_TODAY="Toggl_Track_summary_report_${TODAY}_${TODAY}"
FILENAME_BASE_YESTERDAY="Toggl_Track_summary_report_${YESTERDAY}_${YESTERDAY}"

# Try to find today's and yesterday's files
if [ -f "$DOWNLOAD_DIR/${FILENAME_BASE_TODAY}.csv" ]; then
    FILE_PATH_TODAY="$DOWNLOAD_DIR/${FILENAME_BASE_TODAY}.csv"
    FILE_TYPE_TODAY="csv"
elif [ -f "$DOWNLOAD_DIR/${FILENAME_BASE_TODAY}.pdf" ]; then
    FILE_PATH_TODAY="$DOWNLOAD_DIR/${FILENAME_BASE_TODAY}.pdf"
    FILE_TYPE_TODAY="pdf"
else
    echo "No Toggl Track summary report found for today ($TODAY) in Downloads."
    exit 1
fi

if [ -f "$DOWNLOAD_DIR/${FILENAME_BASE_YESTERDAY}.csv" ]; then
    FILE_PATH_YESTERDAY="$DOWNLOAD_DIR/${FILENAME_BASE_YESTERDAY}.csv"
    FILE_TYPE_YESTERDAY="csv"
elif [ -f "$DOWNLOAD_DIR/${FILENAME_BASE_YESTERDAY}.pdf" ]; then
    FILE_PATH_YESTERDAY="$DOWNLOAD_DIR/${FILENAME_BASE_YESTERDAY}.pdf"
    FILE_TYPE_YESTERDAY="pdf"
else
    echo "No Toggl Track summary report found for yesterday ($YESTERDAY) in Downloads."
fi

echo "Processing files: $FILE_PATH_TODAY and $FILE_PATH_YESTERDAY"

# Extract text based on file type
if [[ "$FILE_TYPE_TODAY" == "pdf" ]]; then
    if ! command -v pdftotext &> /dev/null; then
        echo "Error: pdftotext is not installed. Please install it with 'brew install poppler'"
        exit 1
    fi
    TEXT_TODAY=$(pdftotext "$FILE_PATH_TODAY" -)
elif [[ "$FILE_TYPE_TODAY" == "csv" ]]; then
    TEXT_TODAY=$(cat "$FILE_PATH_TODAY")
else
    echo "No Data for yesterday."
fi

if [[ "$FILE_TYPE_YESTERDAY" == "pdf" ]]; then
    if ! command -v pdftotext &> /dev/null; then
        echo "Error: pdftotext is not installed. Please install it with 'brew install poppler'"
        exit 1
    fi
    TEXT_YESTERDAY=$(pdftotext "$FILE_PATH_YESTERDAY" -)
elif [[ "$FILE_TYPE_YESTERDAY" == "csv" ]]; then
    TEXT_YESTERDAY=$(cat "$FILE_PATH_YESTERDAY")
else
    echo "No Data for yesterday."
fi

# Send the extracted text to the local LLM for analysis and comparison
OUTPUT_FILE="time_analyze.md"

# Send the extracted text to the local LLM for analysis and comparison
echo "# $TODAY" >> "$OUTPUT_FILE"

# Updated and clarified prompt
echo "$TEXT_TODAY" | ollama run llama3.2 "You are my productivity coach. You will receive structured time tracking data for TODAY and YESTERDAY as JSON.

Your task is to:
- Compare the time and projects between TODAY and YESTERDAY.
- ONLY use the entries listed under each specific date — never infer or carry over tasks between days.
- Do not assume any project happened on both days unless it appears in both TODAY and YESTERDAY sections.
- Assign a productivity score for TODAY (0–100), based on time usage, task quality, and inclusion of rest or walking breaks.
- Suggest 2–3 improvements to my time usage. Breaks and walking are considered positive.
- Your output should be in clean markdown.

Important: Do NOT hallucinate or infer data. ONLY use the fields explicitly provided under each date.
" >> "$OUTPUT_FILE"

echo "Analysis saved to $OUTPUT_FILE"