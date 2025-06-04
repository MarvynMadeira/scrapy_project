# scrapy_project

personal project of a future website that consists of a crawler that searches for data from Amazon and stores it in an SQL database.

## Technologies

- Python 3.9+
- Scrapy
- PostgreSQL

## Structure

scrapy_project/
├── book_data_analysis/ # Project root
│ ├── init.py # Init file for module
│ ├── items.py # Item definitions for Scrapy
│ ├── middlewares.py # Custom middleware (if any)
│ ├── pipelines.py # Pipelines for processing scraped data
│ ├── settings.py # Scrapy settings
│ └── spiders/ # Spider definitions
│ ├── init.py
│ └── amazonLink_spider.py # Main spider for Amazon book links
├── scrapy.cfg # Scrapy config file
├── requirements.txt # Python dependencies
└── README.md # This file

## Installation

```bash
git clone https://github.com/MarvynMadeira/scrapy_project.git
cd scrapy_project
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

## Running the Spider

scrapy crawl amazonLink_spider -a url=""

## Data Analysis
Use the scripts inside the book_data_analysis/spiders/ folder (e.g., amazonLink_spider.py) to define how the spider extracts data from Amazon.

📬 Contact
https://github.com/MarvynMadeira
