import streamlit as st
import pandas as pd

st.set_page_config(page_title="CreditOcean V2", layout="centered")

primary_color = "#0077b6"
header_color = "#023e8a"
success_color = "#2a9d8f"

st.markdown(f"<h1 style='color: {header_color};'>🌊 CreditOcean V2 – Credit Calculator</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #444;'>Upload an Excel file with contact data and get a detailed credit breakdown based on actual datapoints.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload Excel (.xlsx or .xls)", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.markdown("### 📋 Preview of Uploaded Data")
        st.dataframe(df.head(), height=200)

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

        st.markdown(f"<h3 style='color:{success_color};'>📊 Credit Summary</h3>", unsafe_allow_html=True)
        st.success(f"**Total Entries:** {len(credit_details)}")
        st.success(f"**Total Credits:** {total_credits} credits")

        st.markdown("### 📄 Detailed Credit Breakdown")
        breakdown_df = pd.DataFrame(credit_details)
        st.dataframe(breakdown_df)

    except Exception as e:
        st.error(f"❌ Error reading Excel file: {str(e)}")
