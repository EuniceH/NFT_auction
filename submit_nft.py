#EH: import libraries
import streamlit as st
import pandas as pd
from PIL import Image
from web3 import Web3
import os
from datetime import datetime,timezone,timedelta
import sqlalchemy
from dotenv import load_dotenv
from pathlib import Path
import json




#EH: load env file
load_dotenv()


# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# EH: Set layout as wide
st.set_page_config(page_title="NFT Submission",layout="wide")


#EH:  set streamlit cache for smart contract load
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/nftRegistry_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

#EH: Load the contract
contract = load_contract()





# EH: set max screen width.
st.markdown(
        f"""<style>.main .block-container{{ max-width: 1600px }} </style> """,
        unsafe_allow_html=True,
)

# Create the connection string for your SQLite database
database_connection_string = 'sqlite:///'

# Pass the connection string to the SQLAlchemy create_engine function
engine = sqlalchemy.create_engine(database_connection_string, echo=True)

create_nft_table = """
CREATE TABLE nft_info (
    "filename"             VARCHAR(50),
    "filetype"             VARCHAR(50),
    "filesize"             INT,
    "Owner_Name"           VARCHAR(50),
    "Public_Key"           VARCHAR(200),
    "Asset_name"           VARCHAR(50),
    "bid_start_amount"     INT,
    "Bid_close_date"       VARCHAR(50)
  );
 """

engine.execute(create_nft_table)



#EH: Get seller information
st.header('NFT Submission for Auction Application')


username=st.text_input(label='Username')
accounts = w3.eth.accounts
public_key=st.selectbox("Select Account", options=accounts)
asset_caption=st.text_input(label='Asset Name')
bid_start=st.number_input("Enter Desired Bid initial amount",min_value=1000,step=1000)

close_date_request = st.date_input(
     "Please enter bid close date(UTC)",
     datetime.now()+timedelta(days=7),min_value=datetime.now() +timedelta(days=7))
st.write('Your close date (UTC) request is:', close_date_request)

#EH: define load/open image function
def load_image(image_file):
	img = Image.open(image_file)
	return img

def insert_data(nft_df):
    for index, row in nft_df.iterrows():
         engine.execute("INSERT INTO nft_info(filename, filetype, filesize, Owner_Name, Public_Key, Asset_name, bid_start_amount, Bid_close_date) values(?,?,?,?,?,?,?,?)", row.filename, row.filetype,                                                  row.filesize,row.Owner_Name, row.Public_Key, row.Asset_name, row.bid_start_amount, row.Bid_close_date)
    
    sql_nft_info_df = pd.read_sql_table('nft_info', con=engine)
    
    st.write(sql_nft_info_df)
    
def select_data():
##    query_info=f"""
##    SELECT '{select_what}'
##    FROM '{from_table}'
##    WHERE '{where_condition}'
##    """
    
    sql_nft_info_df = pd.read_sql_table('nft_info', con=engine)
    st.write(sql_nft_info_df)
    
def update_data(Public_Key):
    update_data = """
    UPDATE nft_info
    SET 'filename' = '{nft_df.filename}',
        'filetype' = '{nft_df.filetype}',
        'filesize' = '{nft_df.filesize}',
        'Owner_Name' = '{nft_df.Owner_Name}',
        'Asset_name' = '{nft_df.Asset_name}',
        'bid_start_amount' = '{nft_df.bid_start_amount}',
        'Bid_close_date' = '{nft_df.Bid_close_date}'
    WHERE 'Public_Key' = '{nft_df.Public_Key}'
    """
    
    engine.execute(update_data)
    read_all_data = """
    SELECT * FROM nft_info
    """
    engine.execute(read_all_data)
    sql_nft_info_df = pd.read_sql_table('nft_info', con=engine)
    st.write(sql_nft_info_df)    
##    list(results)
    
st.subheader("NFT Image")

#EH: upload nft file
image_file = st.file_uploader("Upload Images",
     type=["png","jpg","jpeg"])
#EH: load file condition and display
if image_file is not None and (len(username) > 0) and (len(public_key)>0) and (len(asset_caption)>0):
          # TO See details
          file_details = {"filename":image_file.name, "filepath":image_file.type,
                    "filesize":image_file.size,"Owner_Name":username,'Public_Key':public_key,'Asset_name':asset_caption,'bid_start_amount':bid_start,"Bid_close_date":close_date_request.isoformat()}

          st.write("Please preview transaction detail before submission.")
          st.write(file_details)
          st.image(load_image(image_file), width=1000)
          
          #Saving upload
          with open(os.path.join("fileDir",image_file.name),"wb") as f:
               f.write((image_file).getbuffer())
          
          
          st.success("File Saved to local fileDir folder")

          #EH: Submit NFT for auction  
          submit=st.button("Register NFT for Auction Request")
          st.write('By click this button, you agree and are subject to T&C of auction company.')

          if submit:
               
               #EH: register nft and mint token from smart contract
               nft_register=contract.functions.nftRegistration(
                    public_key,#Owner address
                    asset_caption,#art name
                    username,#artist/owner name
                    int(bid_start),#initial appraisal value
                    str(image_file.size)#tokenURI

               ).transact({'from':public_key,'gas':1000000})

               receipt=w3.eth.waitForTransactionReceipt(nft_register)

              #EH: provide trx hash

               st.write("Transaction receipt mined:")
               st.write(dict(receipt))
               st.markdown("---")

               #EH: display transaction confirmation
               trx_df=pd.DataFrame(file_details,index=[0])
               st.dataframe(trx_df)



else:
     st.write("Please check inputs.") 
