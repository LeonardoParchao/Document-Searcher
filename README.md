# Web Document Search Tool

## Overview
The Web Document Search Tool is a Python-based application that allows users to search for documents on the web using customizable search criteria. It provides a graphical user interface (GUI) built with Tkinter, where users can enter search parameters such as query terms, domain names, date ranges, file types, languages, and more. The tool supports multiple search engines, including Google, Bing, DuckDuckGo, and Yandex.

## Features
- **Search Criteria Customization:** Search by domain, top-level domain (TLD), specific URL text, keywords, and more.
- **Date Filters:** Specify start and end dates to filter search results by date.
- **File Type Selection:** Search for specific document types such as PDF, DOC, DOCX, or all file types.
- **Language Filter:** Restrict search results to specific languages.
- **Multiple Search Engines:** Choose between Google, Bing, DuckDuckGo, and Yandex for your search.
- **Proxy Support:** Option to use a proxy server for the search requests.
- **Progress Tracking:** Real-time progress updates during the search.
- **Search Results:** Display and access search results directly from the GUI.

## Requirements
- Python 3.x
- Required libraries:
  - `requests`
  - `bs4` (BeautifulSoup)
  - `tkinter`
  - `threading`

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install the required Python libraries using pip:
   ```bash
   pip install requests beautifulsoup4
   ```
3. Download or clone the repository containing the script.

## Usage
1. Run the script:
   ```bash
   python script_name.py
   ```
2. The GUI will launch, allowing you to input your search criteria.

### Search Criteria
- **Top-Level Domain (TLD):** Specify a TLD (e.g., `com`, `org`) to restrict results to that domain extension.
- **Domain:** Enter a specific domain (e.g., `example.com`) to limit the search to that website.
- **Search Query:** Enter keywords or phrases to search for in the document content.
- **URL Text:** Specify text that must be present in the URL of the search results.
- **Date Filters:** Use `Start Date` and `End Date` to filter results by date.
- **File Type:** Choose a document type (e.g., PDF, DOC) or select `All` to search for any type.
- **Language:** Restrict results to documents in a specific language.
- **Search Engine:** Select the search engine to use for the query (Google, Bing, DuckDuckGo, or Yandex).
- **Proxy:** If needed, provide a proxy URL (e.g., `http://proxy.example.com:8080`).

### Search Process
1. After entering the desired search criteria, click the `Search` button.
2. The tool will perform the search and update the progress bar as results are retrieved.
3. Results will be displayed in the listbox on the right side of the GUI.
4. Double-click any result to open it in your default web browser.

### Clearing Fields
- To clear all input fields and reset the tool, click the `Clear` button.

## Error Handling
- **Input Errors:** If required fields are missing or incorrectly formatted (e.g., date format errors), the tool will display a warning message.
- **Network Issues:** If the tool encounters network issues or fails to retrieve search results, it will print an error message to the console.

## Example
To search for PDF documents containing the keyword "machine learning" on the domain `example.com` between 01-01-2020 and 31-12-2020 using Google:
- Enter `example.com` in the Domain field.
- Enter `machine learning` in the Search Query field.
- Select `PDF` from the File Type dropdown.
- Enter `01-01-2020` in the Start Date field.
- Enter `31-12-2020` in the End Date field.
- Select `Google` from the Search Engine dropdown.
- Click `Search`.

## License
This project is open-source and available under the MIT License.

## Contributions
Contributions to the project are welcome! Feel free to fork the repository and submit a pull request.

## Contact
For any inquiries or support, please contact the project maintainer at leonardo.parchao@gmail.com .
