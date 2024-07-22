# LinkedIn Scraping

🌐 Python script to scrape LinkedIn job listings after login.

---

## Overview

This repository contains Python code to scrape job listings from LinkedIn's job page, specifically designed to work after a successful login session. LinkedIn's job page has different styles for logged-in and non-logged-in users; this script is compatible with the logged-in style.

---

## Usage

ℹ️ Before running the script, ensure you have set up a valid LinkedIn login session. The script uses Selenium for web scraping, allowing it to interact with the dynamic content of the LinkedIn job listings page.

### Prerequisites

- Python 3.x
- Selenium
- WebDriver (ChromeDriver, GeckoDriver, etc.)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ahmddbilall/Scraping_with_selenium.git
   cd Scraping_with_selenium

2. Install dependencies:
    
    ```bash
    pip install -r requirements.txt


3. Add your linkdin details in Linkdin/constant.py

4. Open main.ipynb and run all the cells



### Notes
📅 Last Tested: July 22, 2024

The script's functionality was validated up to this date. Any changes to LinkedIn's page structure or authentication mechanisms may require updates to the script for continued functionality.


### Disclaimer
⚠️ Legal Notice: Scraping LinkedIn's website may violate their terms of service. Ensure compliance with LinkedIn's terms and conditions and respect their policies regarding automated data retrieval.