import streamlit as st
import pandas as pd

# Create a DataFrame to store the data
df = pd.DataFrame(columns=['Site Name', 'Contract Amount', 'Date', 'Category', 'Amount'])

# Initialize session state variables
if 'site_name' not in st.session_state:
    st.session_state.site_name = ''
if 'contract_amount' not in st.session_state:
    st.session_state.contract_amount = 0

# Function to save data to CSV file
def save_data():
    site_name = st.session_state.site_name
    df_site = df[df['Site Name'] == site_name]
    df_site.to_csv(f'{site_name}.csv', index=False)

# Function to get data for a selected site
def get_data():
    site_name = st.session_state.site_name
    df_site = df[df['Site Name'] == site_name]
    st.write(df_site)

# Function to display total amounts for each category
def display_totals():
    st.subheader('Total Amounts Till Now:')
    totals = df.groupby('Category')['Amount'].sum()
    st.write(totals)

# Streamlit app
def main():
    st.title('Construction Site Tracker')

    # Dropdown for selecting existing sites
    st.sidebar.header('Select Existing Site')
    existing_sites = df['Site Name'].unique()
    selected_site = st.sidebar.selectbox('Select Site', existing_sites, key='existing_site')

    # Set selected site in session state
    st.session_state.site_name = selected_site

    # Display selected site name on the right side
    st.text(f'Construction Site Tracker: {selected_site}')

    # Display contract amount if set previously
    if selected_site in df['Site Name'].values:
        contract_amount = df.loc[df['Site Name'] == selected_site, 'Contract Amount'].iloc[0]
        st.sidebar.text(f"Contract Amount: {contract_amount}")

    # Input for Site Name and Contract Amount
    st.sidebar.header('Input')
    new_site_name = st.sidebar.text_area('New Site Name', key='site_name', value=st.session_state.site_name)
    contract_amount = st.sidebar.number_input('Contract Amount', key='contract_amount', value=st.session_state.contract_amount)

    # Update session state with entered site name and contract amount
    st.session_state.site_name = new_site_name
    st.session_state.contract_amount = contract_amount

    # Date input
    st.sidebar.header('Date Input')
    date_input = st.sidebar.date_input('Select Date', pd.to_datetime('today'))

    # Sub-inputer for categories
    st.sidebar.header('Category Input')
    category = st.sidebar.text_input('Select Category', key='category', value='')
    amount = st.sidebar.number_input('Amount', key='amount', value=0)

    # Submit button to save data
    if st.sidebar.button('Submit') and new_site_name:
        df.loc[len(df)] = [new_site_name, contract_amount, date_input, category, amount]
        st.success('Data submitted successfully!')

    # Get Data button to display entries for a selected site
    if st.sidebar.button('Get Data'):
        get_data()

    # Save Data button to save data to CSV file
    if st.sidebar.button('Save Data'):
        save_data()

    # Display totals
    display_totals()

if __name__ == '__main__':
    main()
