# Fresh repository rebuild

This package is the replacement source for the Streamlit portfolio.

## Verified corrections

- Removed the explanatory paragraph under **Portfolio CV**.
- German proficiency is **A2**.
- The University of Ilorin instrument caption identifies a **computer-connected spectrophotometer**.
- Navigation uses **Project Explorer**, not Xylanase Explorer.
- The explorer includes all six project areas.
- Plotly charts use unique Streamlit keys.
- The Streamlit configuration is stored at `.streamlit/config.toml`.

## Required repository-root structure

```text
streamlit_app.py
portfolio.py
requirements.txt
pages/
data/
assets/
.streamlit/
```

Upload the contents of this folder to the root of a new GitHub repository. Do not upload the outer folder itself and do not rename `.streamlit` to `streamlit`.
