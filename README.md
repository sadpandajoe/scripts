# Scripts

Repository of scripts to help with Git operations, debugging issues during release cutting, cherry-picking, and other development workflows.

This repository contains utility scripts designed to streamline various development tasks and troubleshoot common issues that arise during software release cycles, Git operations, and development workflows.

## Setup

### Virtual Environment

It's recommended to use a virtual environment to isolate dependencies:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Making Scripts Executable

To make the scripts executable:

```bash
# Give execution permission to all Python scripts
chmod +x *.py

# Alternatively, make a specific script executable
# chmod +x script_name.py
```

## Requirements

To run these scripts, you'll need:

- Python 3.6+
- Dependencies listed in `requirements.txt`

## Available Scripts

### git_diff_files.py

This script compares and lists files changed between two Git references.

#### Usage

```bash
./git_diff_files.py <base_ref> <head_ref> [OPTIONS]
```

**Options:**

- `--pattern` / `-p`: File pattern to filter results (e.g., "\*.py")
- `--output` / `-o`: Output file path for the list of changes

**Example:**

```bash
./git_diff_files.py main feature-branch --pattern "*.py" --output changes.txt
```
