# Engineering Specification: YAML to SDK Code Injection Pipeline

## Overview
This document outlines the design and implementation details for a Python-based application that automates the process of extracting AWS SDK code snippets from YAML files stored in a GitHub repository and injecting them into corresponding HTML files. The application ensures seamless updates by committing the modified HTML files back to the repository.

## Functional Requirements
The system performs the following tasks:

1. **Read YAML Files from GitHub**
2. **Locate Corresponding Code Files**
3. **Extract Code Examples**
4. **Inject Code into HTML Files**
5. **Save or Commit Updated HTML Files**

## System Components
- **GitHub Repository**: Stores YAML, SDK, and HTML files.
- **Python Application**: Implements the process flow.
- **YAML Parser**: Extracts SDK snippet references.
- **Java Code Locator**: Identifies and extracts relevant SDK code.
- **HTML Updater**: Injects extracted snippets into HTML files.
- **GitHub Committer (Optional)**: Saves and commits changes.

## Process Flow

### 1. Read and Process YAML Files from GitHub
- Connect to the GitHub repository using the GitHub API.
- Retrieve all YAML files from the metadata directory, excluding cross_metadata.yaml.
- Allow the user to specify a programming language (e.g., Java, Kotlin, Python).
- Parse each YAML file to extract AWS service names, operations, GitHub paths, and snippet tags relevant to the selected language.
- Maintain an incremental index for each section processed.
- Display extracted service, operation, GitHub path, and snippet tags in a structured format.
- Compute and display the total number of snippet tags processed across all files.


### 2. Locate SDK Code Files
- Using extracted references, locate the corresponding SDK files in the repository.
- Read the SDK files and extract the relevant code snippets.
- Ensure extracted snippets maintain code integrity (e.g., preserving indentation and structure).

### 3. Extract Code Examples
- Match the extracted SDK snippets with the references in the YAML files.
- Store the extracted code snippets in a structured format (e.g., dictionary, JSON object) for further processing.
- Handle cases where referenced SDK snippets do not exist or have changed.

### 4. Inject Code into HTML Files
- Identify target HTML files where SDK snippets need to be inserted.
- Locate placeholders or predefined markers within the HTML files for seamless integration.
- Fetch and insert code snippets while preserving original formatting, indentation, and syntax.
- Ensure proper syntax highlighting by wrapping code blocks in appropriate HTML tags (e.g., <pre><code>).
- Maintain HTML structure by keeping surrounding elements intact.
- Support multiple programming languages, dynamically adjusting the injected code format based on the selected SDK language.
- Validate inserted snippets to prevent broken formatting or incorrect placements

### 5. Save or Commit Updated HTML Files
- Save the modified HTML files locally.
- If configured, commit the changes back to the GitHub repository:
  - Create a commit message summarizing the changes.
  - Push the updates to the specified branch.
  - Handle authentication securely (e.g., using GitHub tokens).

## Implementation Details

### Technologies
- **Python**: Primary language.
- **GitHub API**: Fetch and update repository content.
- **PyYAML**: Parse YAML files.
- **BeautifulSoup**: Modify HTML files.
- **GitPython**: Commit changes to the repository.

### Error Handling & Logging
- **Logging**: Maintain detailed logs for debugging and auditing.
- **Error Handling**: Handle missing files, API failures, and YAML parsing errors gracefully.

### Security Considerations
- Use secure authentication (e.g., GitHub PATs, OAuth tokens).
- Validate file paths to prevent unauthorized access.

## Future Enhancements
- **Web Interface**: Provide a UI for configuring repository and injection rules.
- **Automated CI/CD**: Integrate with GitHub Actions for automatic updates.
- **Support for Multiple Languages**: Extend support beyond Java.

## Conclusion
This application streamlines the process of maintaining code documentation by automating the extraction, injection, and update workflow, ensuring consistency and efficiency across repositories.
