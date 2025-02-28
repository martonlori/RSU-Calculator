# RSU Tax Calculator

## Overview
This project is a **command-line application** that calculates the tax liability for vested RSUs (Restricted Stock Units). The tax calculation is based on exchange rates retrieved from the **official MNB (Magyar Nemzeti Bank) website**.

The program dynamically queries the exchange rate for a given date and calculates the tax amounts based on Hungarian tax laws. It supports both **web scraping (BeautifulSoup)** and **SOAP API requests** to fetch exchange rates.

---

## Features

### ✅ Dynamic Exchange Rate Retrieval
- Scrapes data from the **MNB official site**
- Uses **BeautifulSoup** for web scraping
- Uses **MNB's SOAP API** as a primary source, with web scraping as a fallback

### ✅ Tax Calculation Logic
- Takes **two user inputs**:
  - 🟢 **Number of stocks vested**
  - 🟢 **Date of vesting**
- Queries the **exchange rate for that date**
- Calculates **taxable income** and applies tax formulas
- Returns **two final tax values**:
  - 💰 **SZJA (Personal Income Tax)**
  - 💰 **SZOCHO (Social Contribution Tax)**

### ✅ Structured and Testable Design
- Functions are modular and **easily testable**
- Unit tests implemented with **pytest**
- Code follows **PEP8 style guide**


### ✅ Portability & Ease of Use
- 🏗️ **Docker support** will be implemented later for easier installation and to prevent dependency issues
- Works as a **standalone CLI tool** with minimal setup

---

## Development Roadmap

### 📌 Planned Features & Enhancements
- ✅ Compare **SOAP API vs Web Scraping**
  - If SOAP API is **stable**, make it the primary source
  - If it fails, fallback to web scraping
- ✅ Test for **legacy data** (Excel & ShareWorks history vs actual transfers)

### 📌 Technical Goals
- 🏗️ **Improve Python skills**: Regular Expressions (RE), Web Scraping, API calls
- 🏗️ **Practice software design**: Structuring code for better readability & testability
- 🏗️ **Learn Docker**: Ensure easy deployment & prevent dependency conflicts

---

## Testing & Quality Assurance

- ✅ Write **unit tests** for key functions (get_vested_stocks, get_date, get_current_rate, calculate_tax, get_release_price)
- ✅ Perform **manual validation** by comparing results with real historical data
- ✅ Use **pytest** to ensure code correctness
- ✅ Check code style & design before finalizing

---

## Installation & Usage

### 🔹 Option 1: Run it Locally
```bash
git clone https://github.com/your-repo/rsu-tax-calculator.git
cd rsu-tax-calculator
pip install -r requirements.txt
python project.py
