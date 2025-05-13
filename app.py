import streamlit as st
import pandas as pd

st.set_page_config(page_title="CreditOcean V2", layout="centered")

# Styling colors
primary = "#0077b6"
accent = "#90e0ef"
success = "#2a9d8f"

# Header UI
st.markdown(f"""
    <div style='text-align:center;'>
        <h1 style='color:{primary};margin-bottom:0;'>🌊 CreditOcean V2</h1>
        <h3 style='color:#555;font-weight:normal;'>Upload your Excel and calculate real credit usage</h3>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload Excel file", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.markdown("---")
        st.subheader("📋 Preview of Uploaded Data")
        st.dataframe(df.head(), use_container_width=True)

        credit_rules = {
            "domain": 3,
            "company": 1,
            "contact": 2,
            "email": 3,
            "phone": 6,
            "linkedin": 2
        }

        seen_domains = set()
        seen_companies = set()
        total_credits = 0
        credit_details = []

        for _, row in df.iterrows():
            entry = {k: 0 for k in credit_rules}

            domain = str(row.get("Domain", "")).strip().lower()
            if domain and domain not in seen_domains:
                entry["domain"] = 1
                seen_domains.add(domain)

            company = str(row.get("Company Name", "")).strip().lower()
            if company and company not in seen_companies:
                entry["company"] = 1
                seen_companies.add(company)

            title = str(row.get("Contact Title", "")).strip()
            name = str(row.get("Contact Name", "")).strip()
            if title and name:
                entry["contact"] = 1

            email = str(row.get("Company Email", "")).strip().lower()
            if email and '@' in email and not email.startswith(("info@", "kontakt@", "sales@", "support@")):
                entry["email"] = 1

            phone = str(row.get("Mobile", "") or row.get("Direct Number", "")).strip()
            if phone:
                entry["phone"] = 1

            linkedin = str(row.get("LinkedIn URL", "")).strip()
            if "/in/" in linkedin:
                entry["linkedin"] = 1

            credits = sum(entry[k] * credit_rules[k] for k in entry)
            entry["credits"] = credits
            total_credits += credits
            credit_details.append(entry)

        st.markdown("---")
        st.subheader("📊 Credit Summary")
        st.success(f"Total Rows Analyzed: {len(credit_details)}")
        st.success(f"Total Credits Used: {total_credits}")

        with st.expander("🔍 Show Detailed Credit Breakdown"):
            st.dataframe(pd.DataFrame(credit_details), use_container_width=True)

    except Exception as e:
        st.error(f"❌ Could not process file: {str(e)}")
else:
    st.info("👈 Upload your Excel file to begin calculating credits.")
update app.py with design + credit logic
