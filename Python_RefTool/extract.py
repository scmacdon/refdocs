import requests
import re

# GitHub raw URL format
GITHUB_RAW_CODE_BASE_URL = "https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"

def fetch_code_from_github(owner: str, repo: str, branch: str, file_path: str) -> str:
    """
    Fetches a raw Kotlin code file from GitHub and returns its content as a string.
    """
    url = GITHUB_RAW_CODE_BASE_URL.format(owner=owner, repo=repo, branch=branch, file_path=file_path)
    response = requests.get(url)

    if response.status_code == 200:
        return response.text  # Return the raw Kotlin code as a string
    else:
        print(f"Failed to fetch Kotlin file: {url} (Status Code: {response.status_code})")
        return ""

def extract_snippet(code_content: str, snippet_name: str) -> str:
    """
    Extracts a Kotlin code snippet from the fetched content using snippet markers.
    """
    pattern = rf"// snippet-start:\[{re.escape(snippet_name)}\](.*?)// snippet-end:\[{re.escape(snippet_name)}\]"
    match = re.search(pattern, code_content, re.DOTALL)

    if match:
        return match.group(1).strip()  # Extract and return the snippet with preserved formatting
    else:
        print(f"Snippet '{snippet_name}' not found in the file.")
        return ""

if __name__ == "__main__":
    # GitHub details for the Kotlin CloudTrail example
    owner = "awsdocs"
    repo = "aws-doc-sdk-examples"
    branch = "main"
    file_path = "kotlin/services/cloudtrail/src/main/kotlin/com/kotlin/cloudtrail/CreateTrail.kt"
    snippet_name = "cloudtrail.kotlin.create_trail.main"

    # Fetch the Kotlin code from GitHub
    code_content = fetch_code_from_github(owner, repo, branch, file_path)

    if code_content:
        # Extract the required snippet
        snippet_code = extract_snippet(code_content, snippet_name)

        if snippet_code:
            print("\nExtracted Kotlin Code Snippet:\n")
            print(snippet_code)  # Print the snippet while preserving formatting
