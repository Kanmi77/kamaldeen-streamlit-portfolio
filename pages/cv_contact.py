from __future__ import annotations

from pathlib import Path

import streamlit as st

from portfolio import DOCS, EMAIL, GITHUB, LINKEDIN, header

header(
    "Professional documents",
    "CV and contact",
    "Download the multidisciplinary portfolio CV or contact me regarding scientific, analytical, laboratory and technical-commercial opportunities.",
)

pdf_path = DOCS / "Kamaldeen_Olasunkanmi_Bada_Portfolio_CV.pdf"
docx_path = DOCS / "Kamaldeen_Olasunkanmi_Bada_Portfolio_CV.docx"

left, right = st.columns([1.15, 0.85], gap="large")
with left:
    st.markdown("## Portfolio CV")
    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "Download CV · PDF",
            data=pdf_path.read_bytes(),
            file_name=pdf_path.name,
            mime="application/pdf",
            icon="⬇️",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "Download editable CV · DOCX",
            data=docx_path.read_bytes(),
            file_name=docx_path.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            icon="⬇️",
            use_container_width=True,
        )

    st.markdown("## Professional focus")
    st.markdown(
        "I am targeting opportunities across scientific research, data-driven decision support and technical commercial functions. These include bioinformatics, microbiology and molecular biology, data science, financial analytics, QC/QA and technical sales roles where scientific understanding, analytical judgement and clear communication are valued."
    )

with right:
    st.markdown("## Contact")
    st.markdown(f"**Email**  \n{EMAIL}")
    st.markdown("**Location**  \nBavaria, Germany")
    st.markdown("**Work preferences**  \nOn-site · Hybrid · Remote · Open to relocation")
    st.link_button("Email", f"mailto:{EMAIL}", icon="✉️", use_container_width=True)
    st.link_button("LinkedIn", LINKEDIN, icon="↗", use_container_width=True)
    st.link_button("GitHub", GITHUB, icon="↗", use_container_width=True)

st.divider()
st.markdown("## Enquiry form")
st.caption("Submitting the form prepares a structured email in your default email application; no personal data is stored by this app.")
with st.form("contact_form", clear_on_submit=False):
    name = st.text_input("Name")
    organisation = st.text_input("Organisation")
    enquiry_type = st.selectbox(
        "Enquiry type",
        ["Employment opportunity", "Research collaboration", "Technical project", "Teaching or speaking", "General enquiry"],
    )
    message = st.text_area("Message", height=160)
    submitted = st.form_submit_button("Prepare email", use_container_width=True)

if submitted:
    if not name.strip() or not message.strip():
        st.warning("Please enter your name and a message.")
    else:
        import urllib.parse

        subject = urllib.parse.quote(f"Portfolio enquiry: {enquiry_type}")
        body = urllib.parse.quote(
            f"Hello Kamaldeen,\n\nMy name is {name}.\nOrganisation: {organisation or 'Not provided'}\nEnquiry type: {enquiry_type}\n\n{message}\n"
        )
        mailto = f"mailto:{EMAIL}?subject={subject}&body={body}"
        st.success("Your email is ready. Use the button below to open it in your email application.")
        st.link_button("Open prepared email", mailto, icon="✉️", use_container_width=True)
