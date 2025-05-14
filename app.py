import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="CreditOcean V2", layout="centered")

# Styling
primary = "#0077b6"
success = "#2a9d8f"

st.markdown(f"""
    <div style='text-align:center;'>
        <h1 style='color:{primary};'>🌊 CreditOcean V2</h1>
        <h3 style='color:#444;'>Upload Excel to calculate credits and download results</h3>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.markdown("### 📋 Data Preview")
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
        credit_rows = []

        for _, row in df.iterrows():
            entry = {k: 0 for k in credit_rules}

            domain = str(row.get("Domain", row.get("Domæne", ""))).strip().lower()
            if domain and domain not in seen_domains:
                entry["domain"] = 1
                seen_domains.add(domain)

            company = str(row.get("Company Name", row.get("Virksomhed", ""))).strip().lower()
            if company and company not in seen_companies:
                entry["company"] = 1
                seen_companies.add(company)

            title = str(row.get("Contact Title", row.get("Stilling", ""))).strip()
            name = str(row.get("Contact Name", row.get("Navn", ""))).strip()
            if title and name:
                entry["contact"] = 1

            email = str(row.get("Company Email", row.get("E-mail", ""))).strip().lower()
            if email and '@' in email and not email.startswith(("info@", "kontakt@", "support@", "sales@")):
                entry["email"] = 1

            phone = str(row.get("Mobile", row.get("Direct Number", row.get("Telefon", "")))).strip()
            if phone:
                entry["phone"] = 1

            linkedin = str(row.get("LinkedIn URL", row.get("LinkedIn", ""))).strip()
            if "/in/" in linkedin:
                entry["linkedin"] = 1

            credits = sum(entry[k] * credit_rules[k] for k in credit_rules)
            entry["credits"] = credits
            total_credits += credits

            entry["name"] = name
            entry["title"] = title
            entry["email_raw"] = email
            entry["mobile_raw"] = phone
            entry["company"] = company
            credit_rows.append(entry)

        st.markdown("---")
        st.subheader("📊 Credit Summary")
        st.success(f"Total contacts analyzed: {len(credit_rows)}")
        st.success(f"Total credits used: {total_credits}")
        st.success(f"Total price: {total_credits * 3} DKK")

        result_df = pd.DataFrame(credit_rows)

        with st.expander("🔍 Show credit breakdown"):
            st.dataframe(result_df, use_container_width=True)

        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='CreditData')
            return output.getvalue()

        excel_data = to_excel(result_df)
        st.download_button("⬇️ Download Excel result", data=excel_data, file_name="credit_results.xlsx")

    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

else:
    st.info("👈 Please upload an Excel file to begin.")
