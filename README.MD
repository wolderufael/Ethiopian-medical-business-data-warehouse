# Ethiopian Medical Business Data Warehouse

This repository contains the data pipeline and transformations for building a data warehouse aimed at analyzing Ethiopian medical businesses. The data collected from public sources, including Telegram channels, is transformed to provide meaningful insights for business analysis, including object detection and business monitoring.

## Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Data Pipeline](#data-pipeline)
- [YOLO Object Detection](#yolo-object-detection)
- [API with FastAPI](#api-with-fastapi)
- [Database Schema](#database-schema)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The **Ethiopian Medical Business Data Warehouse** collects, processes, and analyzes medical data sourced from public channels like Telegram. Object detection using YOLO models is applied to image data, and FastAPI is used to expose the collected data through an API.
## Project Structure
├── .github.<br>
│   └── workflow<br>
│       └── test.yaml<br>
├── .venv <br>
├── .vscode<br>
│   └── settings.json<br>
├── medical
├── notebook<br>
│   ├── Data_scrapping_and_transformation.ipynb<br>
│
├── script
│   ├── data_cleaning_and_transformation.py<br>
│   ├──script/telegram_scrapper.py<br>
│   
├── .gitignore<br>
├──  README.MD<br>
├──  requirements.txt <br>

### Key Features:
- Data scraping from Telegram channels
- Object detection using YOLOv5
- Data transformation and analysis
- FastAPI for exposing data and analysis results

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wolderufael/Ethiopian-medical-business-data-warehouse.git
   cd Ethiopian-medical-business-data-warehouse
2. **Set up Python environment**: Create a virtual environment and activate it:
   ```bash
    python -m venv .venv
    source .venv/bin/activate  # For Linux/macOS
    .venv\Scripts\activate  # For Windows

2. **Install the required packages**: Install the dependencies from the `requirements.txt` file:
   ```bash
    pip install -r requirements.txt

## Contributing
Contributions to improve this project are welcome. If you'd like to contribute, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
