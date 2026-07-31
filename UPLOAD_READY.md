# Upload-ready analytical portfolio

This package replaces the previous version.

Key changes:

- Featured Afelele and breast-cancer views now use interactive analytical visualisations rather than simple bar-chart previews.
- The Home page includes interactive xylanase, Afelele, breast-cancer and RNA-seq evidence.
- The Project Explorer represents all six project areas equally and opens no project by default.
- Xylanase now includes a candidate landscape, multi-evidence parallel coordinates and molecular-dynamics heatmap.
- Afelele now includes a connected community-shift analysis, genus heatmap, heavy-metal uncertainty panels and physicochemical explorer.
- Breast-cancer analysis now includes PCA, selectable feature distributions, correlations and a relationship explorer.
- German proficiency remains A2.

Upload every item inside this extracted folder to the root of:

`Kanmi77/kamaldeen-streamlit-portfolio`

Then open Streamlit Community Cloud, choose **Manage app**, and reboot the app.
## V3.1 corrective update

- Corrected the University of Ilorin image caption to identify the instrument as a **computer-connected spectrophotometer**.
- Assigned an explicit unique `key` to every `st.plotly_chart` element. This prevents the duplicate element-ID error when the same analytical figure is displayed in the Overview and detailed analysis tabs.

