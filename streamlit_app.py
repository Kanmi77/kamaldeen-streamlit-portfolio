from __future__ import annotations

import streamlit as st

from portfolio import footer, inject_css

st.set_page_config(
    page_title="Kamaldeen Olasunkanmi Bada | Scientific Portfolio",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": "Scientific and analytical portfolio of Kamaldeen Olasunkanmi Bada.",
        "Report a bug": "mailto:Sunkanmikamal.edu@gmail.com",
    },
)

inject_css()

pages = [
    st.Page("pages/home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/project_explorer.py", title="Project Explorer", icon="🗂️"),
    st.Page("pages/experience.py", title="Experience", icon="🧭"),
    st.Page("pages/skills.py", title="Skills", icon="🧰"),
    st.Page("pages/cv_contact.py", title="CV & Contact", icon="📄"),
]

navigation = st.navigation(pages, position="top")
navigation.run()
footer()
