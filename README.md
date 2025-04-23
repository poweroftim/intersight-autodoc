# intersight-autodoc
From API get requests, dynamically create tables in a Word Doc for easy documentation.


## Prerequisites

Ensure you have the following installed:
- **Python**: Version 3.8 or higher
- **pip**: Python package manager
- **Git**: For cloning the repository (optional)

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

### 4. Define Environment Variables

Create a v2 API Key within Intersight. 
<img width="465" alt="Screenshot 2025-04-23 at 10 39 45 AM" src="https://github.com/user-attachments/assets/7b4bed64-89c3-4d24-b44a-f4206452da00" />

Create an .env file in the intersight-autodoc directory with the following values:
```bash
SECRET_KEY_PATH=./NAME_OF_SECRET_API_KEY.txt
API_KEY_ID=<API_KEY>
```


### 5. Create Configuration Files

Create the necessary configuration files in the root directory. 


Config.yaml - If using an Intersight appliance, an update to the base_url will be required. Otherwise, the config.yaml is ready to use. 


```bash
# Config.yaml
directories:
  output: "./output"
  flattened_output: "./flattened_output"
  excel_output: "./excel_output"
word_template_path: "./template.docx"
base_url: "https://www.intersight.com/api/v1"
```

Operations.yaml - Review the operations.yaml file for correct syntax. 

For help learning which $select and $expand queries to use, the [Intersight API REST Client](https://us-east-1.intersight.com/apidocs/apirefs/All/api/v1) is helpful. 


```bash
# Operations.yaml
OPERATIONS:
  - request_method: "GET"
    resource_path: "/resource/path" 
    select: "?$select=field1,field2" # Copy and paste the $select query from the API client
    expand: "&$expand=relatedResource" # Copy and paste the $expand query from the API client. 
    filter: "field1,field2" # This is a filter for JSON output, not the $filter for the Intersight API. 
    request_process: true
    table_name: "Name of table in Word Doc" 
    column_names: "Rename columns from filter list" #The order of the filter and column names fields must match. 
    placeholder: "{{placeholder_name}}" #Insert placeholders in your document to control the order in which the tables appear. 
```



### 6. Run the script

Execute the script:

```bash
python intersight_autodoc.py
```

Example Output:
<br>
<img width="669" alt="Screenshot 2025-04-22 at 2 57 36 PM" src="https://github.com/user-attachments/assets/7f6cea8b-eeeb-4ab4-8ca9-adf11342423d" />


## Notes
- **Authentication**: Ensure the secret_key_path and api_key_id in the .env file are valid for accessing the Intersight API. See operations.yaml for examples of use.
- **Word Template**: Use the Word Doc template provided in the repository.
- **Filtering**: The filter key in operations.yaml specifies which fields to include in the filtered JSON output. It is not same as the $filter query used in the Intersight API REST Client. 

## Troubleshooting
- **Missing Dependencies**: Run pip install -r requirements.txt to ensure all dependencies are installed.
- **Directory Errors**: Verify that the directories specified in config.yaml exist.
- **API Errors**: Check your api_key_id and secret_key_path for validity.


## Feature Requests/Issues
Please use the Issues Tab for any feature requests, issues, etc. Thanks!
