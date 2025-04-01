# iOS Appium Path Extractor

## Overview

The **iOS Appium Path Extractor** is a macOS-based Python tool designed to rapidly extract UI element paths from iOS Appium page sources. By automating the extraction process, it streamlines the development of automation scripts and supports security assessments, reverse engineering, and red team operations. This tool dramatically reduces manual effort, saving valuable time for developers and security professionals alike.

## Purpose and Use Cases

In dynamic testing and security research, quickly mapping an app's UI is crucial. This tool was developed to:
- **Accelerate Automation:** Automatically parse and extract element paths from Appium source pages, enabling rapid integration into automated test scripts.
- **Enhance Security Assessments:** Provide detailed UI mappings to support red team exercises and vulnerability research in iOS applications.
- **Facilitate Reverse Engineering:** Help analysts understand app interfaces by archiving page sources and extracting precise UI element identifiers.

These capabilities make it an essential asset for teams that need to evaluate iOS apps efficiently—whether for quality assurance, penetration testing, or continuous security monitoring.

## Features

- **Rapid UI Path Extraction:**  
  The main script (`extract_paths.py`) processes Appium-generated HTML source files to automatically extract UI element paths (e.g., XPath expressions). This eliminates the tedious, manual work of identifying UI components.

- **Page Source Archiving:**  
  The companion script (`Page Source Appium Saver/save_app_pages.py`) captures and saves complete page sources from active Appium sessions, ensuring that the data is preserved for later analysis and debugging.

- **Efficiency for Developers:**  
  By automating both the capture and extraction processes, the tool significantly reduces the time required to build and update automation scripts. This efficiency allows developers to focus on higher-level analysis and strategy.

- **Modular and Extensible:**  
  The tool's modular design allows for easy integration into larger automation frameworks and red team toolkits. It can be adapted to different testing environments and extended to support additional functionalities.

## Technical Architecture

The project is organized into several key modules:

1. **Content Extraction:**
   - **`extract_paths.py`**  
     Parses HTML page sources from Appium sessions, extracting relevant UI element paths using libraries such as BeautifulSoup and lxml.
   
2. **Page Source Archiving:**
   - **`save_app_pages.py`**  
     Connects to an active Appium session, captures the current page source, and saves it locally for subsequent processing.

3. **Utilities and Shared Functions:**
   - **`shared_functions.py`**  
     Contains reusable functions that support both extraction and archiving tasks, ensuring maintainability and ease of extension.

4. **Progress Monitoring:**
   - Scripts provide real-time feedback during the extraction process, keeping users informed of the operation’s status.

## Setup Requirements

### Prerequisites

- **macOS Only:**  
  This tool is designed specifically for macOS due to dependencies on macOS-specific configurations.
- **Python 3.x:**  
  Ensure Python 3 is installed on your system.
- **Appium Environment:**  
  The tool assumes you are already capturing page sources from an Appium session on an iOS device.

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Neverlow512/iOS-Appium-Path-Extractor.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd iOS-Appium-Path-Extractor
   ```
3. **(Optional) Set Up a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Use `venv\Scripts\activate` on Windows (Note: this tool is macOS-only)
   ```
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   _The `requirements.txt` includes:_
   - `appium-python-client==2.12.1`
   - `selenium==4.9.0`
   - `beautifulsoup4==4.11.1`
   - `lxml==4.9.2`
   - `requests==2.28.1`

## Usage

### 1. Capture Appium Page Sources

Before extracting UI element paths, run the page source saver to capture the current Appium session:
```bash
python "Page Source Appium Saver/save_app_pages.py"
```
This script connects to an active Appium session and saves the HTML source of the app’s current state to disk.

### 2. Extract UI Element Paths

Once the page sources are saved, run the extraction script:
```bash
python extract_paths.py
```
This script parses the saved HTML files, extracts the UI element paths (e.g., XPath expressions), and outputs them in a structured format for easy integration into your automation workflows.

### 3. Integration and Application

- **Automated Testing:**  
  Integrate the extracted UI paths into your test scripts to dynamically interact with app elements.
- **Cybersecurity Assessments:**  
  Use the detailed UI mappings during red team exercises to simulate attacker techniques and identify potential vulnerabilities.
- **Reverse Engineering:**  
  Leverage the extracted data to better understand app interfaces and behaviors for vulnerability research.

## Benefits for Developers and Security Professionals

- **Saves Time:**  
  Automates the manual process of UI mapping, reducing development and testing time.
- **Improves Efficiency:**  
  Provides a reliable, repeatable method for extracting UI paths, ensuring consistent data for automation and security analysis.
- **Facilitates Rapid Prototyping:**  
  Quickly generate and update automation scripts by integrating the tool into your continuous integration pipelines.
- **Supports Security Operations:**  
  Enhances red team and vulnerability research efforts by providing precise UI mappings that can be used to simulate attacks or test defenses.

## Security & Ethical Considerations

This tool is intended for ethical and legal use only. It is designed for:
- **Automated Testing:**  
  To support quality assurance and automated UI testing in controlled environments.
- **Security Research:**  
  To assist in ethical vulnerability assessments and red team operations.
  
**Important:** Do not use this tool to compromise or attack production systems. Always follow responsible disclosure practices when identifying vulnerabilities.

## License

This project is licensed under the [MIT License](LICENSE).  
© 2024-2025 Neverlow512

```
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## Contact

For inquiries, collaborations, or further information, please contact:  
**Email:** [neverlow512@proton.me](mailto:neverlow512@proton.me)  
**GitHub:** [github.com/Neverlow512](https://github.com/Neverlow512)
