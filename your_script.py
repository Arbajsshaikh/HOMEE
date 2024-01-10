import streamlit as st
import pandas as pd

def save_to_csv(data, site_name):
    df = pd.DataFrame(data)
    df.to_csv(f"{site_name}.csv", index=False)

def main():
    st.title("Construction Site Data Entry App")

    site_name = st.text_input("Enter Site Name:")
    contract_amount = st.number_input("Enter Site Contract Amount:")

    if st.button("Show Site Info"):
        st.write(f"Site Name: {site_name}")
        st.write(f"Site Contract Amount: {contract_amount}")

    date = st.date_input("Select Date:")

    categories = ['Bricks', 'Plumber', 'Murum', 'Sand', 'Aggregate', 'Steel', 'Electrical material',
                  'Plumbing material', 'Flooring material', 'Labor payment', 'Ducting', 'Rcc labor',
                  'Brick work and plaster work', 'Electric labor', 'Plumbing labor', 'Flooring labor', 'IPS labor']

    data = {}
    for category in categories:
        data[category] = st.number_input(f"Enter {category} Amount:", key=category)

    if st.button("Submit"):
        save_to_csv(data, site_name)
        st.success("Data saved successfully!")

    if st.button("Get Data"):
        get_site_name = st.text_input("Enter Site Name to retrieve data:")
        try:
            df = pd.read_csv(f"{get_site_name}.csv")
            st.write(df)
        except FileNotFoundError:
            st.error(f"No data found for Site Name: {get_site_name}")

    st.subheader("All Subcategories Titles:")
    st.write(", ".join(categories))

if _name_ == "_main_":
    main()
