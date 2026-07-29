import sys
import os
import warnings


warnings.filterwarnings(
    "ignore",
    category=FutureWarning
)


# ==================================================
# Add Project Root
# ==================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


sys.path.append(PROJECT_ROOT)



import streamlit as st



from camera.camera_registry import CameraRegistry

from camera.multi_camera_manager import MultiCameraManager


from ai_pipeline.processor import FrameProcessor


from camera_view import show_camera_frame




# ==================================================
# Streamlit Configuration
# ==================================================

st.set_page_config(

    page_title="EdgeGuard AI",

    layout="wide"

)



st.title(
    "🚨 EdgeGuard AI Security Dashboard"
)




# ==================================================
# Initialize Cameras
# ==================================================

@st.cache_resource
def initialize_camera_manager():


    config_path = os.path.join(

        PROJECT_ROOT,

        "camera",

        "cameras.json"

    )


    registry = CameraRegistry(

        config_path

    )


    manager = MultiCameraManager(

        registry.get_active_cameras()

    )


    manager.start()


    return manager




camera_manager = initialize_camera_manager()




# ==================================================
# Initialize AI Pipeline
# ==================================================

@st.cache_resource
def initialize_ai_processor():


    return FrameProcessor()




processor = initialize_ai_processor()




# ==================================================
# Get Frames
# ==================================================

frames = camera_manager.get_frames()


camera_status = camera_manager.get_status()




# ==================================================
# AI Processing
#
# Frame
#   |
#   ▼
# AI Pipeline
#   |
#   ▼
# ByteTrack + Face Recognition
#
# ==================================================


processed_frames = {}



for camera_name, frame in frames.items():


    if frame is not None:


        result = processor.process_camera_frame(

            camera_name,

            frame

        )


        processed_frames[camera_name] = result




# ==================================================
# Display Cameras
# ==================================================

st.subheader(
    "📹 Live AI Monitoring"
)



camera_names = list(
    processed_frames.keys()
)



columns = st.columns(2)



for index, camera_name in enumerate(camera_names):


    with columns[index % 2]:


        data = processed_frames[camera_name]


        show_camera_frame(

            camera_name,

            data["frame"],

            camera_status[camera_name],

            data["people"]

        )



# ==================================================
# Security Summary
# ==================================================

st.divider()


st.subheader(
    "🛡️ Security Summary"
)



total_people = 0

unknown_people = 0

authorized_people = 0



for camera_name,data in processed_frames.items():


    for person in data["people"]:


        total_people += 1


        identity = person["identity"]


        if identity["authorized"]:

            authorized_people += 1

        else:

            unknown_people += 1




col1,col2,col3 = st.columns(3)



with col1:

    st.metric(

        "Total People",

        total_people

    )


with col2:

    st.metric(

        "Authorized",

        authorized_people

    )


with col3:

    st.metric(

        "Unknown",

        unknown_people

    )



# ==================================================
# Refresh
# ==================================================

st.rerun()