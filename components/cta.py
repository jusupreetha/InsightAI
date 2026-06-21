import streamlit as st


def show_cta():

    left, center, right = st.columns([2.5, 1.5, 2.5])

    with center:

        if st.button(
            ":material/rocket_launch: Start Analysis",
            use_container_width=True,
            type="primary",
            key="landing_start_analysis"
        ):
            st.session_state.show_upload = True
            st.rerun()