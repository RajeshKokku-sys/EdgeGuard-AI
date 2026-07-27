import streamlit as st
import pandas as pd
import os

from PIL import Image


# -----------------------------------------
# Add project root to Python path
# -----------------------------------------

import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from database.db_manager import DatabaseManager


# -----------------------------------------
# Streamlit Configuration
# -----------------------------------------

st.set_page_config(
    page_title="EdgeGuard AI",
    layout="wide"
)


st.title("🚨 EdgeGuard AI - Security Dashboard")


# -----------------------------------------
# Load Database
# -----------------------------------------

try:

    db = DatabaseManager()

    events = db.get_events()


except Exception as e:

    st.error(
        f"Database Error: {e}"
    )

    st.stop()



# -----------------------------------------
# Check Events
# -----------------------------------------

if len(events) == 0:

    st.warning(
        "No security events found in database"
    )

    st.stop()



# -----------------------------------------
# Convert Events to DataFrame
# -----------------------------------------

columns = [

    "ID",

    "Camera",

    "Track ID",

    "Event Type",

    "Zone",

    "Confidence",

    "Timestamp"

]


df = pd.DataFrame(
    events,
    columns=columns
)



# -----------------------------------------
# Dashboard Metrics
# -----------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Events",
        len(df)
    )


with col2:

    st.metric(
        "Tracked Persons",
        df["Track ID"].nunique()
    )


with col3:

    st.metric(
        "Restricted Zones",
        df["Zone"].nunique()
    )



st.divider()



# -----------------------------------------
# Event History
# -----------------------------------------

st.subheader(
    "Security Event History"
)


st.dataframe(
    df,
    use_container_width=True
)



st.divider()



# -----------------------------------------
# Evidence Viewer
# -----------------------------------------

st.subheader(
    "Captured Evidence"
)


image_folder = "evidence/images"


if not os.path.exists(image_folder):

    st.warning(
        "Evidence folder not found"
    )

else:

    images = os.listdir(
        image_folder
    )


    if len(images) == 0:

        st.warning(
            "No evidence images available"
        )


    else:

        for image_name in images[::-1]:

            image_path = os.path.join(
                image_folder,
                image_name
            )


            st.write(
                f"Evidence: {image_name}"
            )


            image = Image.open(
                image_path
            )


            st.image(
                image,
                width=600
            )


            st.divider()