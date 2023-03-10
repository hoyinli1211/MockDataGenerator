import streamlit as st
from faker import Faker
import pandas as pd
import random
from datetime import datetime 

#Sidebar
st.sidebar.title("Instructions:")
st.sidebar.markdown("1. Select the data type from the dropdown menu")
st.sidebar.markdown("2. Enter the number of records to generate")
st.sidebar.markdown("3. Click the 'Generate Data' checkbox to generate the mock-up data")
st.sidebar.markdown("4. Download the generated synthetic data")

def faker_introduction():
  st.title("Faker Introduction")
  st.markdown("Faker is a Python package that generates synthetic data for various purposes such as testing and data analysis. It can be used to generate fake names, addresses, email addresses, etc.")
  st.markdown("Generating synthetic data can be useful for testing and data analysis purposes, as it allows you to work with a large dataset without compromising on the privacy of real users.")

# Create a dictionary to map data types to their corresponding methods in the Faker class
fake = Faker()
data_type_mapping = {
  #customer profile related
  "name": fake.name,
  "first_name": fake.first_name,
  "last_name": fake.last_name,
  "prefix": fake.prefix,
  "suffix": fake.suffix,
  "job": fake.job,
  "address": fake.address,
  "email": fake.email,
  "phone_number": fake.phone_number,
  "date_of_birth": fake.date_of_birth,
  "gender": lambda: fake.random_element(elements=("male", "female")),
  "ssn": fake.ssn,
  "username": fake.user_name,
  "password": fake.password,
  "url": fake.url,
  "company_suffix": fake.company_suffix,
  "company": fake.company,
  #transaction related
  "tran_date": fake.date_this_decade,
  "tran_datetime": fake.date_time,
  "tran_amount": lambda: random.randint(1, 100000),
  "tran_CD": lambda:fake.random_element(elements=("debit", "credit")),
  "tran_status": lambda: fake.random_element(elements=("approved", "declined", "pending")),
  "tran_type": lambda:fake.random_element(elements=("ATM", "FPS", "CHATs", "SWIFT", "CHEQUE", "Others")),
  "tran_channel": lambda:fake.random_element(elements=("Internet Banking","Mobile Banking","Branch/ATM")),
  "ctp_name": fake.name
}  

customer_profile = {
  "name": fake.name,
  "first_name": fake.first_name,
  "last_name": fake.last_name,
  "prefix": fake.prefix,
  "suffix": fake.suffix,
  "job": fake.job,
  "address": fake.address,
  "email": fake.email,
  "phone_number": fake.phone_number,
  "date_of_birth": fake.date_of_birth,
  "gender": lambda: fake.random_element(elements=("male", "female")),
  "ssn": fake.ssn,
  "company_suffix": fake.company_suffix,
  "company": fake.company,
}

transactional = {
  "tran_date": lambda: fake.date_between_dates(date_start=datetime(2023,1,1), date_end=datetime(2023,1,30)),
  "tran_datetime": lambda: fake.date_time_between_dates(datetime_start=datetime(2023,1,1), datetime_end=datetime(2023,1,30)),
  "tran_amount": lambda: random.randint(1, 100000),
  "tran_CD": lambda:fake.random_element(elements=("debit", "credit")),
  "tran_status": lambda: fake.random_element(elements=("approved", "declined", "pending")),
  "tran_type": lambda:fake.random_element(elements=("ATM", "FPS", "CHATs", "SWIFT", "CHEQUE", "Others")),
  "tran_channel": lambda:fake.random_element(elements=("Internet Banking","Mobile Banking","Branch/ATM")),
  "ctp_name": fake.name,
  "credit_card_number": fake.credit_card_number,
  "currency_code": fake.currency_code,
  "currency_name": fake.currency_name,
  "cryptocurrency_code": fake.cryptocurrency_code,
  "merchant_id": lambda: "AA-{:05d}".format(fake.random_number(digits=5))
}

digital_footprint = {
  "event_datetime": lambda: fake.date_time_between_dates(datetime_start=datetime(2023,1,1), datetime_end=datetime(2023,1,30)),
  "username": fake.user_name,
  "ipv4": fake.ipv4,
  "ipv6": fake.ipv6,
  "mac_address": fake.mac_address,
  "uuid": fake.uuid4,
  "user_agent": fake.user_agent,
  "domain_name": fake.domain_name,
  "tld": fake.tld,
  "url": fake.url,
  "slug": fake.slug,
  "ipv4_network_class": fake.ipv4_network_class,
  "ipv4_private": fake.ipv4_private,
  "ascii_company_email":fake.ascii_company_email,
  "ascii_safe_email":fake.ascii_safe_email
}

data_type_mapping = {**customer_profile, **transactional, **digital_footprint}

def create_data(data_mapping, choice, n):

  #type = data_type_mapping
  # Create an empty dataframe
  data = {}

  # Iterate through the selected data types
  for data_type in choice:
      method = data_mapping[data_type]
      data[data_type] = [method() for _ in range(n)]
  df = pd.DataFrame(data)
  return df

#Main Page
st.title("Mock Data Generator")
tabs = st.tabs(["Note","Configuration & Mock Data Generation"])

tab_note = tabs[0]

with tab_note:
    faker_introduction()

tab_main = tabs[1]

with tab_main:

  fake = Faker()
  # Get the list of providers for the selected locale
  
  customer_profile_choice = list(customer_profile.keys())
  transactional_choice = list(transactional.keys())
  digital_footprint_choice = list(digital_footprint.keys())
      
  # Ask the user to select data types
  data_type_pick = []
  #customer_profile_pick = st.multiselect("Customer Profile", customer_profile_choice)
  #transactional_pick = st.multiselect("Transactional", transactional_choice)
  #digital_footprint_pick = st.multiselect("Digital Footprint", digital_footprint_choice)
  data_type_pick.extend(st.multiselect("Customer Profile", customer_profile_choice))
  data_type_pick.extend(st.multiselect("Transactional", transactional_choice))
  data_type_pick.extend(st.multiselect("Digital Footprint", digital_footprint_choice))
  
  # Use the `number_input` widget to gather the user's desired number of records
  num_records = st.number_input("Enter the number of records to generate", value=1000, min_value=1)
  
  if st.button("Generate Data"):
    df=create_data(data_type_mapping, data_type_pick, num_records)
    st.write('Mock Data',df)
    st.download_button("Download Mock data",df.to_csv(index=False), "mock_data.csv")
