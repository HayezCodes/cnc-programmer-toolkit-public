import streamlit as st
import pandas as pd
from datetime import datetime

st.title("CNC Programming Checklist")

st.caption("Checklist Mode: Export Only (No Saving)")

# -----------------------
# JOB INFO
# -----------------------
st.subheader("Job Information")

customer = st.text_input("Customer")
job_number = st.text_input("Job Number")
drawing_number = st.text_input("Drawing Number")
revision = st.text_input("Revision")
machine = st.text_input("Machine")
material = st.text_input("Material")
programmer = st.text_input("Programmer")

notes = st.text_area("Notes")

# -----------------------
# CHECKLIST ITEMS
# -----------------------
st.subheader("Checklist")

checklist_items = {
    "SolidWorks Model Created / Verified": False,
    "Drawing Dimensions Verified": False,
    "Material Confirmed": False,
    "Correct Machine Selected": False,
    "Workholding Verified": False,
    "Tooling Selected": False,
    "Speeds and Feeds Applied": False,
    "Mastercam Program Complete": False,
    "Toolpaths Verified": False,
    "Simulation Checked": False,
    "Post Processed": False,
    "Program Verified in CIMCO": False,
    "Program Sent to Machine (Predator)": False,
}

checked_items = {}

for item in checklist_items:
    checked_items[item] = st.checkbox(item)

# -----------------------
# EXPORT LOGIC
# -----------------------
st.divider()
st.subheader("Export Checklist")

if st.button("Generate Export"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "Timestamp": timestamp,
        "Customer": customer,
        "Job Number": job_number,
        "Drawing Number": drawing_number,
        "Revision": revision,
        "Machine": machine,
        "Material": material,
        "Programmer": programmer,
        "Notes": notes,
    }

    # Add checklist results
    for item, value in checked_items.items():
        data[item] = "YES" if value else "NO"

    df = pd.DataFrame([data])

    # CSV Download
    csv = df.to_csv(index=False).encode("utf-8")

    filename = f"{job_number}_{timestamp.replace(':','-').replace(' ','_')}.csv"

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

    # TXT Summary
    txt_lines = [f"{k}: {v}" for k, v in data.items()]
    txt_content = "\n".join(txt_lines)

    st.download_button(
        label="Download TXT Summary",
        data=txt_content,
        file_name=filename.replace(".csv", ".txt"),
        mime="text/plain"
    )

    st.success("Checklist ready for download.")