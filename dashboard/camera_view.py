import cv2
import streamlit as st


def show_camera_frame(
    camera_name,
    frame,
    status,
    people=None
):
    """
    Display live AI processed camera frame with:
    - Camera Status
    - Face Recognition
    - ByteTrack IDs
    - Zone Intelligence
    - Intrusion Alerts
    """

    # ======================================================
    # Camera Title
    # ======================================================

    st.subheader(f"📷 {camera_name}")

    # ======================================================
    # Camera Status
    # ======================================================

    if status:
        st.success("🟢 Camera Connected")
    else:
        st.error("🔴 Camera Disconnected")

    # ======================================================
    # Live Frame
    # ======================================================

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

        st.warning("Waiting for camera frame...")
        return

    # ======================================================
    # AI Intelligence Panel
    # ======================================================

    st.markdown("---")
    st.subheader("🧠 AI Intelligence")

    if not people:

        st.info("No people detected.")
        return

    # ======================================================
    # Person Details
    # ======================================================

    for person in people:

        identity = person.get("identity", {})

        name = identity.get("name", "Unknown")

        authorized = identity.get(
            "authorized",
            False
        )

        department = identity.get(
            "department",
            "-"
        )

        designation = identity.get(
            "designation",
            "-"
        )

        score = identity.get(
            "score",
            0.0
        )

        zone = person.get(
            "zone",
            "Outside Zone"
        )

        intrusion = person.get(
            "intrusion",
            False
        )

        # --------------------------------------------------

        if authorized:
            auth_status = "✅ AUTHORIZED"
        else:
            auth_status = "❌ UNKNOWN"

        if intrusion:
            intrusion_status = "🚨 INTRUSION DETECTED"
        else:
            intrusion_status = "✅ SAFE"

        # --------------------------------------------------

        if intrusion:

            st.error(
                f"""
### 🚨 Security Alert

**Person ID:** {person['track_id']}

**Detection Confidence:** {person['confidence']:.2f}

**Name:** {name}

**Authorization:** {auth_status}

**Zone:** {zone}

**Status:** {intrusion_status}

**Department:** {department}

**Designation:** {designation}

**Face Match Score:** {score:.2f}
"""
            )

        else:

            st.success(
                f"""
### 👤 Person Information

**Person ID:** {person['track_id']}

**Detection Confidence:** {person['confidence']:.2f}

**Name:** {name}

**Authorization:** {auth_status}

**Zone:** {zone}

**Status:** {intrusion_status}

**Department:** {department}

**Designation:** {designation}

**Face Match Score:** {score:.2f}
"""
            )

        # --------------------------------------------------
        # Bounding Box Information
        # --------------------------------------------------

        if "bbox" in person:

            x1, y1, x2, y2 = person["bbox"]

            st.caption(
                f"Bounding Box: ({x1}, {y1}) → ({x2}, {y2})"
            )

        st.markdown("---")

    # ======================================================
    # Summary
    # ======================================================

    total_people = len(people)

    authorized_count = sum(
        1 for p in people
        if p.get("identity", {}).get("authorized", False)
    )

    unknown_count = total_people - authorized_count

    intrusion_count = sum(
        1 for p in people
        if p.get("intrusion", False)
    )

    st.subheader("📊 Camera Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "People",
            total_people
        )

    with col2:
        st.metric(
            "Authorized",
            authorized_count
        )

    with col3:
        st.metric(
            "Unknown",
            unknown_count
        )

    with col4:
        st.metric(
            "Intrusions",
            intrusion_count
        )