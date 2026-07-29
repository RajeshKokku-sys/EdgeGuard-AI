import streamlit as st
import cv2



def show_camera_frame(
        camera_name,
        frame,
        status,
        people=None
):

    """
    Display AI processed camera frame
    with person information.
    """

    st.subheader(
        f"📷 {camera_name}"
    )


    # -----------------------------
    # Camera Status
    # -----------------------------

    if status:

        st.success(
            "🟢 Camera Connected"
        )

    else:

        st.error(
            "🔴 Camera Disconnected"
        )



    # -----------------------------
    # Display Frame
    # -----------------------------

    if frame is not None:


        frame_rgb = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2RGB

        )


        st.image(

            frame_rgb,

            channels="RGB",

            use_container_width=True

        )


    else:

        st.warning(
            "Waiting for frame..."
        )



    # -----------------------------
    # AI Person Information
    # -----------------------------

    if people:


        st.markdown(
            "### 👥 Detected People"
        )


        for person in people:


            identity = person.get(
                "identity",
                {}
            )


            name = identity.get(
                "name",
                "Unknown"
            )


            authorized = identity.get(
                "authorized",
                False
            )


            score = identity.get(
                "score",
                0.0
            )



            if authorized:

                status_text = (
                    "✅ AUTHORIZED"
                )

            else:

                status_text = (
                    "🚨 UNKNOWN"
                )



            st.write(

                f"""
                **Person ID:**
                {person['track_id']}


                **Detection Confidence:**
                {person['confidence']:.2f}


                **Name:**
                {name}


                **Face Match Score:**
                {score:.2f}


                **Status:**
                {status_text}

                ---
                """

            )