import streamlit as st

import pandas as pd

from PIL import Image

import os

import sys
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Add project root to Python path
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from database.db_manager import DatabaseManager



st.set_page_config(

    page_title="EdgeGuard AI",

    layout="wide"

)



st.title(
    "🚨 EdgeGuard AI Evidence Dashboard"
)



db = DatabaseManager()



events = (
    db.get_events_with_evidence()
)



if not events:

    st.warning(
        "No events available"
    )

    st.stop()



columns = [

"ID",

"Camera",

"Track ID",

"Zone",

"Event",

"Confidence",

"Timestamp",

"Image",

"Video"

]



df = pd.DataFrame(

    events,

    columns=columns

)



# -----------------------------
# Metrics
# -----------------------------


c1,c2,c3 = st.columns(3)


c1.metric(

"Total Events",

len(df)

)


c2.metric(

"Unique Persons",

df["Track ID"].nunique()

)


c3.metric(

"Zones",

df["Zone"].nunique()

)



st.divider()



st.subheader(
    "Security Events"
)



st.dataframe(
    df,
    use_container_width=True
)



st.divider()



st.subheader(
    "Evidence Viewer"
)



for _,row in df.iterrows():


    st.write(
        f"""
        ## Event {row['ID']}

        Camera:
        {row['Camera']}

        Person ID:
        {row['Track ID']}

        Zone:
        {row['Zone']}

        Time:
        {row['Timestamp']}
        """
    )



    # Image

    if row["Image"] and os.path.exists(
        row["Image"]
    ):


        image = Image.open(
            row["Image"]
        )


        st.image(
            image,
            width=500
        )



    # Video

    if row["Video"] and os.path.exists(
        row["Video"]
    ):


        video_file = open(
            row["Video"],
            "rb"
        )


        st.video(
            video_file
        )



    st.divider()