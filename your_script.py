import streamlit as st
import pandas as pd
import os

# Initialize DataFrames outside the main function
sites_df = pd.DataFrame(columns=["Site Name"])
df = pd.DataFrame(columns=["Site Name", "Date", "Category", "Amount"])

# Function to save data to CSV file
def save_to_csv(site_name, data):
    filename = f"{site_name}.csv"
    data_pivoted = data.pivot(index="Date", columns="Category", values="Amount")
    data_pivoted.to_csv(filename)
    return filename

# Function to get data from CSV file
def get_data(site_name):
    filename = f"{site_name}.csv"
    try:
        df = pd.read_csv(filename, index_col="Date")
        return df
    except FileNotFoundError:
        return None

# Main Streamlit app
def main():
    global sites_df, df  # Declare sites_df and df as global

    st.title("Construction Site Tracker")

    # Add Site input with dropdown selector
    add_site_name = st.text_input("Add Site Name:")
    if add_site_name:
        sites_df = pd.concat([sites_df, pd.DataFrame([{"Site Name": add_site_name}])], ignore_index=True)

    # Site Name dropdown
    selected_site_name = st.selectbox("Select Site Name:", sites_df["Site Name"].tolist())

    # Date input
    date = st.date_input("Enter Date:")
        # Sub-categories and their inputs
    categories = [
            'Bricks', 'Plumber', 'Murum', 'Sand', 'Aggregate', 'Steel',
            'Electrical material', 'Plumbing material', 'Flooring material',
            'Labor payment', 'Ducting', 'Rcc labor', 'Brick work and plaster work',
            'Electric labor', 'Plumbing labor', 'Flooring labor', 'IPS labor' ]

        selected_category = st.selectbox("Select Category:", categories)
        category_amount = st.number_input(f"Enter Amount for {selected_category}:", min_value=0.0)    
    # Save data to the global DataFrame
    if st.button("Submit"):
        new_data = {"Site Name": selected_site_name, "Date": date, "Category": selected_category, "Amount": category_amount}
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    # Save data to CSV and display it
    if st.button("Save to CSV"):
        filename = save_to_csv(selected_site_name, df)
        st.success(f"Data saved to {filename}")

    # Get data for a specific site
    if st.button("Get Data"):
        retrieved_data = get_data(selected_site_name)
        if retrieved_data is not None:
            st.write("Retrieved Data:")
            st.write(retrieved_data)
        else:
            st.warning("Data not found for the specified site.")

    # Display total for each sub-category
    st.title("Total Expenditure by Sub-Category:")
    for category in df["Category"].unique():
        total_amount = df[(df["Site Name"] == selected_site_name) & (df["Category"] == category)]["Amount"].sum()
        st.write(f"{category}: ${total_amount:,.2f}")

    # Download button for CSV
    if st.button("Download CSV"):
        csv_file = save_to_csv(selected_site_name, df)
        st.download_button(label="Download CSV", data=open(csv_file, "rb").read(), key="download_csv", file_name=os.path.basename(csv_file))

if __name__ == "__main__":
    main()
