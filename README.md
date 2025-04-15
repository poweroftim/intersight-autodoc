# intersight-autodoc
Using API get requests, create tables in a Word Doc for easy documentation. 

---
## Prerequisites

Ensure you have the following installed:
- **Python**: Version 3.8 or higher
- **pip**: Python package manager
- **Git**: For cloning the repository (optional)

---

## Setup Instructions

### 1. Clone the Repository
If the project is hosted on GitHub, clone it using:
```bash
git clone https://github.com/poweroftim/intersight-autodoc.git
cd intersight-autodoc
```
### 2. Create a Virtual Environment

Set up a virtual environment to isolate dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 4. Create Configuration Files

Create the necessary configuration files in the root directory:

config.yaml
```bash
directories:
  input: "input"
  output: "output"
  excel_output: "excel_output"
word_template_path: "template.docx"
secret_key_path: "path/to/secret_key.txt"
api_key_id: "your_api_key_id"
base_url: "https://www.intersight.com/api/v1"
```

operations.yaml
```bash
OPERATIONS:
  - request_method: "GET"
    resource_path: "/resource/path"
    select: "?$select=field1,field2"
    expand: "&$expand=relatedResource" 
    filter: "field1,field2" # This is a filter for JSON output, not the same filter for the Intersight API. 
    request_process: true
    table_name: "Name of table in Word Doc"
    column_names: "Rename columns from filter list. Retain the order."
```

### 5. Prepare Input and Output Directories

Ensure the directories specified in config.yaml exist:

- **input**: Place input files here.
- **output**: Processed JSON files will be saved here.
- **excel_output**: Excel files will be saved here.

### 6. Run the script

Execute the script:

```bash
python intersight_ops.py
```


## Notes

- **Authentication**: Ensure the secret_key_path and api_key_id in config.yaml are valid for accessing the Intersight API.
- **Word Template**: The word_template_path should point to a valid .docx file if Word document generation is required.
- **Filtering**: The filter key in operations.yaml specifies which fields to include in the filtered JSON output.


## Troubleshooting
- **Missing Dependencies**: Run pip install -r requirements.txt to ensure all dependencies are installed.
- **Directory Errors**: Verify that the directories specified in config.yaml exist.
- **API Errors**: Check your api_key_id and secret_key_path for validity.
