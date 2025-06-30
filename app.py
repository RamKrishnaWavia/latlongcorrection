import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim, GoogleV3
from geopy.extra.rate_limiter import RateLimiter
import time
from io import StringIO

# --- Helper function to convert DataFrame to CSV for download ---
# Using the cache decorator is important for performance
@st.cache_data
def convert_df_to_csv(df):
    """Converts a DataFrame to a UTF-8 encoded CSV file for download."""
    return df.to_csv(index=False).encode('utf-8')

# --- App Configuration ---
st.set_page_config(layout="wide", page_title="Apartment Geocoder")

# --- App Title and Description ---
st.title("📍 Apartment/Society Geocoder")
st.markdown("""
This app helps you check and correct the latitude and longitude of apartment complexes or other points of interest.
**Instructions:**
1.  **(Optional)** Download the CSV template to see the required format.
2.  **Upload your own CSV file** with your apartment data.
3.  **Select the columns** that contain the apartment name and area/city.
4.  **Choose a geocoding service** and provide an API key if needed.
5.  **Run the geocoder** and download your corrected file.
""")

# --- [NEW] Template Download Section ---
st.subheader("Get Started with a Template")

# Create a template dataframe
template_data = {
    'name': ['Prestige Shantiniketan', 'Sobha Dream Acres', 'Brigade Gateway'],
    'area': ['Whitefield', 'Panathur', 'Malleshwaram']
}
template_df = pd.DataFrame(template_data)

# Convert the template dataframe to a CSV file in memory
template_csv = convert_df_to_csv(template_df)

st.download_button(
   label="📥 Download Template CSV",
   data=template_csv,
   file_name='apartment_template.csv',
   mime='text/csv',
   help="Click to download a sample CSV file with the correct 'name' and 'area' columns."
)
st.markdown("---") # Visual separator

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("⚙️ Configuration")

    uploaded_file = st.file_uploader("1. Upload your CSV file", type=["csv"])

    geocoder_option = st.radio(
        "2. Choose Geocoding Service",
        ('Nominatim (Free, Slower)', 'Google Maps (API Key Required)'),
        help="Google is more accurate for specific building names but requires an API key. Nominatim is free but may not find all addresses and has rate limits."
    )

    google_api_key = None
    if geocoder_option == 'Google Maps (API Key Required)':
        google_api_key = st.text_input("Enter your Google Maps API Key", type="password")

    # These will be populated once a file is uploaded
    name_col = None
    area_col = None
    df = None

    if uploaded_file is not None:
        try:
            # Read the uploaded file into a pandas DataFrame
            df = pd.read_csv(uploaded_file)
            
            st.subheader("3. Select Columns")
            all_columns = df.columns.tolist()
            # Try to pre-select columns if they match the template names
            name_col_index = all_columns.index('name') if 'name' in all_columns else 0
            area_col_index = all_columns.index('area') if 'area' in all_columns else min(1, len(all_columns)-1)

            name_col = st.selectbox("Select Apartment Name Column", all_columns, index=name_col_index)
            area_col = st.selectbox("Select Area/City Column", all_columns, index=area_col_index)

        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
            df = None # Ensure df is None if reading fails
            
    run_button = st.button("🚀 Start Geocoding", disabled=(df is None or not name_col or not area_col))


# --- Main Panel for Displaying Results ---
if run_button:
    if geocoder_option == 'Google Maps (API Key Required)' and not google_api_key:
        st.error("Please enter a Google Maps API Key to proceed.")
    else:
        with st.spinner('Geocoding in progress... This may take a while.'):
            # --- Prepare DataFrame ---
            df['full_address'] = df[name_col].astype(str) + ', ' + df[area_col].astype(str) + ', Bangalore, Karnataka'
            df['latitude'] = None
            df['longitude'] = None
            df['geocoding_status'] = 'Pending'


            # --- Initialize Geocoder ---
            if geocoder_option == 'Google Maps (API Key Required)':
                geolocator = GoogleV3(api_key=google_api_key)
                geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)
            else: # Nominatim
                geolocator = Nominatim(user_agent="streamlit_geocoder_app_v1")
                geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.1)

            # --- Process the data ---
            progress_bar = st.progress(0)
            status_text = st.empty()
            total_rows = len(df)
            success_count = 0

            for i, row in df.iterrows():
                address = row['full_address']
                try:
                    location = geocode(address, timeout=10)
                    if location:
                        df.at[i, 'latitude'] = location.latitude
                        df.at[i, 'longitude'] = location.longitude
                        df.at[i, 'geocoding_status'] = 'Success'
                        success_count += 1
                        status_text.text(f"✅ Success: {address}")
                    else:
                        df.at[i, 'geocoding_status'] = 'Failed'
                        status_text.text(f"⚠️ Failed: Could not find location for {address}")

                except Exception as e:
                    df.at[i, 'geocoding_status'] = f'Error: {e}'
                    status_text.text(f"❌ Error for {address}: {e}")
                
                # Update progress bar
                progress_bar.progress((i + 1) / total_rows)

            st.success(f"Geocoding complete! Successfully found {success_count} out of {total_rows} locations.")
            
            # --- Display Results ---
            results_df = df.copy()
            map_df = results_df.dropna(subset=['latitude', 'longitude'])

            st.subheader("🗺️ Map of Geocoded Locations")
            if not map_df.empty:
                st.map(map_df)
            else:
                st.warning("No locations were successfully geocoded to display on the map.")

            st.subheader("📊 Corrected Data")
            st.dataframe(results_df)

            # --- Download Button ---
            csv_to_download = convert_df_to_csv(results_df)
            st.download_button(
                label="📥 Download Corrected CSV",
                data=csv_to_download,
                file_name='bangalore_apartments_corrected.csv',
                mime='text/csv',
            )
else:
    if df is not None:
        st.subheader("File Preview")
        st.dataframe(df.head())
        st.info("Configure settings in the sidebar and click 'Start Geocoding'.")
    else:
        # This message shows on first load
        st.info("Awaiting CSV file upload...")
