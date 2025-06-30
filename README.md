# 📍 Apartment/Society Geocoder

An interactive web application built with Streamlit to check, correct, and enrich location data (latitude and longitude) for a list of apartments, societies, or any other points of interest.

The app takes a CSV file as input, processes each address using a selected geocoding service, and provides a corrected CSV file for download, along with a map visualization of the results.


*(**Action Required:** Replace this with a real screenshot of your app!)*

---

## Features

-   **Interactive UI**: Easy-to-use web interface powered by Streamlit.
-   **CSV Upload**: Upload your data directly in the browser.
-   **Flexible Column Mapping**: Select which columns in your file contain the name and area information.
-   **Dual Geocoding Services**:
    -   **Nominatim (OpenStreetMap)**: A free, open-source geocoder. Good for general use but has rate limits.
    -   **Google Maps Geocoding API**: A highly accurate, robust service ideal for specific building names and addresses (requires a free or paid API key).
-   **Real-time Progress**: A progress bar and status updates show the geocoding progress.
-   **Data Visualization**: An interactive map displays the geocoded locations to help you visually inspect the results.
-   **Download Corrected Data**: Download the final, enriched dataset as a new CSV file.

## Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

-   Python 3.8 or higher
-   `pip` (Python package installer)
-   (Optional but Recommended) A Google Maps Geocoding API key. You can obtain one from the [Google Cloud Console](https://console.cloud.google.com/).

### Installation

1.  **Clone the repository (or download the files):**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment (recommended):**
    -   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the App

1.  Ensure you are in the project's root directory where `geocoder_app.py` is located.

2.  Run the following command in your terminal:
    ```bash
    streamlit run geocoder_app.py
    ```

3.  Your default web browser will automatically open with the application running at `http://localhost:8501`.

## How to Use the App

1.  **Upload a CSV file**: Click "Browse files" and select your CSV. The file must contain at least two columns: one for the entity name (e.g., apartment name) and one for its area (e.g., "Whitefield", "Koramangala, Bangalore").

2.  **Configure Settings (in the sidebar)**:
    -   **Choose Geocoding Service**: Select either "Nominatim" (free) or "Google Maps".
    -   If using Google Maps, enter your API key in the password field provided.
    -   **Select Columns**: From the dropdowns, map the "Apartment Name Column" and "Area/City Column" to the corresponding columns in your uploaded file.

3.  **Start Geocoding**: Click the "🚀 Start Geocoding" button.

4.  **Review and Download**:
    -   Watch the progress bar as the app processes each row.
    -   Once complete, review the geocoded points on the interactive map.
    -   Inspect the resulting data in the table.
    -   Click the "📥 Download Corrected CSV" button to save the file with the new `latitude` and `longitude` columns.

## Project Structure

```
.
├── geocoder_app.py        # The main Streamlit application script
├── requirements.txt       # Project dependencies
└── README.md              # This file
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to open an issue or submit a pull request.
