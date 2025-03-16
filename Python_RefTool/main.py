import requests
import yaml
import re
from typing import List, Tuple

# Define structured data type for extracted snippets
SnippetData = Tuple[str, str, str, str]  # (Service, Operation, GitHub Path, Snippet Tag)

# GitHub repository details
OWNER = "awsdocs"
REPO = "aws-doc-sdk-examples"
BRANCH = "main"
METADATA_DIR = "https://api.github.com/repos/awsdocs/aws-doc-sdk-examples/contents/.doc_gen/metadata"

# Exclude cross_metadata.yaml
EXCLUDED_FILE = "cross_metadata.yaml"

# GitHub raw content URL formats
GITHUB_RAW_METADATA_URL = "https://raw.githubusercontent.com/awsdocs/aws-doc-sdk-examples/main/.doc_gen/metadata/{}"
GITHUB_RAW_CODE_URL = "https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"


class ClassExtract:
    """Handles fetching and extracting metadata from GitHub"""

    @staticmethod
    def get_yaml_file_list() -> List[str]:
        """Fetches the list of YAML files in the GitHub metadata directory, excluding 'cross_metadata.yaml'."""
        response = requests.get(METADATA_DIR)
        if response.status_code == 200:
            files = response.json()
            return [file["name"] for file in files if file["name"].endswith(".yaml") and file["name"] != EXCLUDED_FILE]
        else:
            print(f"Failed to fetch file list from GitHub. Status Code: {response.status_code}")
            return []

    @staticmethod
    def fetch_yaml_from_github(file_name: str) -> dict:
        """Fetches and parses a YAML file from GitHub."""
        url = GITHUB_RAW_METADATA_URL.format(file_name)
        response = requests.get(url)

        if response.status_code == 200:
            try:
                return yaml.safe_load(response.text)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML ({file_name}): {e}")
                return {}
        else:
            print(f"Failed to fetch YAML file: {file_name} (Status Code: {response.status_code})")
            return {}

    @staticmethod
    def extract_snippet_data(yaml_content: dict, language: str) -> List[SnippetData]:
        """Extracts snippet data (service, operation, GitHub path, and snippet tags) for the given language."""
        extracted_data = []

        for section_name, section_data in yaml_content.items():
            if not isinstance(section_data, dict):
                continue  # Skip invalid sections

            # Extract service and operation from section name (e.g., comprehend_DetectSentiment)
            parts = section_name.split("_", 1)
            if len(parts) != 2:
                continue  # Skip if the section name is not in the expected format
            service, operation = parts

            languages = section_data.get('languages', {})
            lang_data = languages.get(language, {})

            for version_info in lang_data.get('versions', []):
                github_path = version_info.get('github', 'Unknown')

                for excerpt in version_info.get('excerpts', []):
                    snippet_tags = excerpt.get('snippet_tags', [])

                    for tag in snippet_tags:
                        extracted_data.append((service, operation, github_path, tag))

        return extracted_data

    @staticmethod
    def fetch_code_from_github(file_path: str) -> str:

        """Fetches a raw code file from GitHub."""
        url = GITHUB_RAW_CODE_URL.format(owner=OWNER, repo=REPO, branch=BRANCH, file_path=file_path)
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch code file: {url} (Status Code: {response.status_code})")
            return ""

    @staticmethod
    def extract_snippet(code_content: str, snippet_name: str) -> str:
        """Extracts a code snippet from the fetched file content."""
        pattern = rf"// snippet-start:\[{re.escape(snippet_name)}\](.*?)// snippet-end:\[{re.escape(snippet_name)}\]"
        match = re.search(pattern, code_content, re.DOTALL)

        if match:
            return match.group(1).strip()  # Extract and return the snippet with preserved formatting
        else:
            print(f"Snippet '{snippet_name}' not found in the file.")
            return ""


class ClassWrite:
    """Handles writing extracted snippet data to the console."""

    @staticmethod
    def print_snippet(index: int, service: str, operation: str, github_path: str, tag: str):
        """Prints the extracted snippet metadata."""
        print(f"[{index}] Service: {service} | Operation: {operation} | GitHub Path: {github_path} | Snippet Tag: {tag}")

    @staticmethod
    def print_code_snippet(snippet_code: str):
        """Prints the formatted code snippet."""
        print("\nExtracted Kotlin Code Snippet:\n")
        print(snippet_code)


class ClassController:
    """Controls the flow of the program."""

    def __init__(self):
        self.extractor = ClassExtract()
        self.writer = ClassWrite()

    def run(self):
        """Main execution flow."""
        language = input("Enter the programming language (e.g., Java, Kotlin, Python): ").strip()

        # A collection that stores YAML files read from Github.
        yaml_files = self.extractor.get_yaml_file_list()

        total_snippet_count = 0
        index = 0  # Incremental index for sections processed

        if not yaml_files:
            print("No YAML files found.")
            return

        for file_name in yaml_files:
            yaml_content = self.extractor.fetch_yaml_from_github(file_name)

            if yaml_content:
                snippets = self.extractor.extract_snippet_data(yaml_content, language)

                for service, operation, github_path, tag in snippets:
                    index += 1  # Increment section index
                    self.writer.print_snippet(index, service, operation, github_path, tag)

                    """
                    # Fetch and extract the code snippet from the actual file
                    code_content = self.extractor.fetch_code_from_github(github_path)

                    if code_content:
                        snippet_code = self.extractor.extract_snippet(code_content, tag)
                        if snippet_code:
                            self.writer.print_code_snippet(snippet_code)
                    """

                total_snippet_count += len(snippets)

        print(f"\nTotal snippet tags read: {total_snippet_count}")


if __name__ == "__main__":
    controller = ClassController()
    controller.run()
