The purpose of this assignment is to extract textual data from the articles provided in the given URLs and perform text analysis to compute several variables as defined in the project requirements.

## Project Overview

This project involves:
1. **Data Extraction**: Extract article titles and article text from the URLs listed in the `Input.xlsx` file.
   - Save the extracted text in a `.txt` file named with the corresponding `URL_ID`.
   - Ensure only the article title and text are extracted, excluding website headers, footers, or other irrelevant elements.

2. **Text Analysis**: Perform textual analysis on the extracted content to compute the following variables:
   - POSITIVE SCORE
   - NEGATIVE SCORE
   - POLARITY SCORE
   - SUBJECTIVITY SCORE
   - AVG SENTENCE LENGTH
   - PERCENTAGE OF COMPLEX WORDS
   - FOG INDEX
   - AVG NUMBER OF WORDS PER SENTENCE
   - COMPLEX WORD COUNT
   - WORD COUNT
   - SYLLABLES PER WORD
   - PERSONAL PRONOUNS
   - AVG WORD LENGTH

3. **Output Format**: Save the results in the exact format specified in the `Output Data Structure.xlsx` file.


## Tools and Libraries Used
- **Python**
  - Libraries: `BeautifulSoup`, `Selenium`, `Scrapy` (or any other library for web scraping)
  - Libraries for text analysis: `NLTK`, `TextBlob`, `re`
- **Excel Manipulation**: `pandas`

## Project Structure

|-- Input.xlsx  # Input file containing URLs and URL_IDs
|-- Output Data Structure.xlsx  # Defines output format
|-- Text Analysis.docx  # Describes variables for text analysis
|-- scripts
    |-- data_extraction.py  # Python script for extracting data
    |-- text_analysis.py  # Python script for performing text analysis
|-- outputs
    |-- Extracted Texts/  # Folder containing extracted .txt files
    |-- Results.xlsx  # Final output file

## How to Run the Project

1. **Setup Environment**:
   - Install Python (version 3.6 or later).
   - Install required dependencies using:
     ```
     pip install -r requirements.txt
     ```

2. **Data Extraction**:
   - Run the `data_extraction.py` script to extract articles from URLs listed in `Input.xlsx`.
   - Extracted articles will be saved as `.txt` files in the `Extracted Texts/` folder.

     ```
     python scripts/data_extraction.py
     ```

3. **Text Analysis**:
   - Run the `text_analysis.py` script to perform textual analysis on the extracted content.
   - The results will be saved in `Results.xlsx`.

     ```
     python scripts/text_analysis.py
     ```

4. **Output**:
   - Review the final output in `Results.xlsx` for computed variables in the required format.
