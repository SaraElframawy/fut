from report_parser_using_selenium import parse_html_file
import requests
import json
from pathlib import Path

# Xray API configuration
xray_api_key = "<YOUR_XRAY_API_KEY>"  # Replace with your Xray API key
jira_base_url = "https://msab.atlassian.net/"  # Replace with your Jira domain

headers = {
    "Authorization": f"Bearer {xray_api_key}",
    "Content-Type": "application/json"
}
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to import execution results to Xray
def import_execution_results(execution_data):
    import_results_url = f"{jira_base_url}/rest/raven/2.0/import/execution"
    response = requests.post(import_results_url, headers=headers, json=execution_data)
    if response.status_code == 200:
        print("Execution results imported successfully.")
        return response.json()
    else:
        print(f"Failed to import execution results: {response.status_code}")
        print(response.text)
        exit()

# Function to upload attachments to an issue
def upload_attachment(issue_key, file_path):
    attachment_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}/attachments"
    with open(file_path, 'rb') as file:
        files = {
            'file': (file_path, file, 'application/octet-stream')
        }
        response = requests.post(attachment_url, headers={
            "Authorization": headers["Authorization"],
            "X-Atlassian-Token": "no-check"
        }, files=files)
        if response.status_code == 200:
            print(f"Attachment {file_path} uploaded successfully.")
        else:
            print(f"Failed to upload attachment {file_path}: {response.status_code}")
            print(response.text)
def create_test_result_with_attachments(test_execution_key, test_key, status, comment, image_paths, html_file_path=None):
    execution_data = {
        "testExecutionKey": test_execution_key,
        "tests": [
            {
                "testKey": test_key,
                "status": status,
                "comment": comment
            }
        ]
    }

    # Import execution results
    import_results_url = f"{jira_base_url}/rest/raven/2.0/import/execution"
    response = requests.post(import_results_url, headers=headers, json=execution_data)
    if response.status_code == 200:
        print("Execution results imported successfully.")
        execution_result = response.json()

        # Attach additional files (images, HTML reports, etc.)
        for image_path in image_paths:
            upload_attachment(test_execution_key, image_path)
        if html_file_path:
            upload_attachment(test_execution_key, html_file_path)

        return execution_result
    else:
        print(f"Failed to import execution results: {response.status_code}")
        print(response.text)
        return None

# Main logic
test_execution_key = "<TEST_EXECUTION_KEY>"  # Replace with your test execution key
html_report = fr"{Path.home()}\OneDrive - Micro systemation AB\Desktop\Test_cases_TestRail_xam\tests\html_reports\test_Right_hand_hide.html"

# Default status to "PASS"
status = "PASS"

try:
    test_names, durations, results = parse_html_file(html_report)
    for result in results:
        if result == "Failed":
            status = "FAIL"
        elif result == "Error":
            status = "FAIL"
        elif result == "Retest":
            status = "TODO"
        elif result == "Blocked":
            status = "ABORTED"
except Exception as e:
    print("Maybe the HTML file needs to be produced by running pytest with --html.")
    exit()

execution_data = {
    "testExecutionKey": test_execution_key,
    "tests": [
        {
            "testKey": "<TEST_KEY>",  # If Xray is integrated with Jira,
            # each test case created in Xray will have a Jira issue key (e.g., TEST-123).
            "status": status,
            "comment": "Automated test result imported from script."
        }
    ]
}

# Import execution results
import_execution_results(execution_data)

# Attach additional files (HTML report, images, etc.)
image_paths = [
    "../Test/Right_hand_side_VN/version.png",
]
for image_path in image_paths:
    upload_attachment(test_execution_key, image_path)
upload_attachment(test_execution_key, html_report)
# Main logic
test_key = "<TEST_KEY>"  # Replace with your test case key
text_file_path = "../Test/Right_hand_side_VN/Right_hand_version_number.txt"

# Read the comment from a text file
comment = read_file(text_file_path)

# Define image paths
image_paths = [
    "../Test/Right_hand_side_VN/version.png"
]

create_test_result_with_attachments(test_execution_key, test_key, status, comment, image_paths, html_report)