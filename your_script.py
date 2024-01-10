import streamlit as st
import pandas as pd

# Initialize DataFrame outside the main function
df = pd.DataFrame(columns=["Site Name", "Date", "Category", "Amount"])

# Function to save data to CSV file
def save_to_csv(site_name, data):
    filename = f"{site_name}.csv"
    data.to_csv(filename, index=False)
    return filename

# Function to get data from CSV file
def get_data(site_name):
    filename = f"{site_name}.csv"
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        return None

# Main Streamlit app
def main():
    global df  # Make sure to use the global DataFrame

    st.title("Construction Site Tracker")

    # Input fields for site name and contract amount
    site_name = st.text_input("Enter Site Name:")
    contract_amount = st.number_input("Enter Site Contract Amount:", min_value=0.0)

    # Display site name and contract amount
    if site_name and contract_amount:
        st.sidebar.write(f"Site Name: {site_name}")
        st.sidebar.write(f"Contract Amount: ${contract_amount:,.2f}")

        # Date input
        date = st.date_input("Enter Date:")

        # Sub-categories and their inputs
        categories = [
            'Bricks', 'Plumber', 'Murum', 'Sand', 'Aggregate', 'Steel',
            'Electrical material', 'Plumbing material', 'Flooring material',
            'Labor payment', 'Ducting', 'Rcc labor', 'Brick work and plaster work',
            'Electric labor', 'Plumbing labor', 'Flooring labor', 'IPS labor'
        ]

        selected_category = st.selectbox("Select Category:", categories)
        category_amount = st.number_input(f"Enter Amount for {selected_category}:", min_value=0.0)

        # Save data to the global DataFrame
        if st.button("Submit"):
            new_data = {"Site Name": site_name, "Date": date, "Category": selected_category, "Amount": category_amount}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

        # Save data to CSV and display it
        if st.button("Save to CSV"):
            filename = save_to_csv(site_name, df)
            st.success(f"Data saved to {filename}")

        # Get data for a specific site
        if st.button("Get Data"):
            selected_site = st.text_input("Enter Site Name to Retrieve Data:")
            retrieved_data = get_data(selected_site)
            if retrieved_data is not None:
                st.write("Retrieved Data:")
                st.write(retrieved_data)
            else:
                st.warning("Data not found for the specified site.")

        # Display total for each sub-category
        st.title("Total Expenditure by Sub-Category:")
        for category in categories:
            total_amount = df[df["Category"] == category]["Amount"].sum()
            st.write(f"{category}: ${total_amount:,.2f}")

if __name__ == "__main__":
    main()
