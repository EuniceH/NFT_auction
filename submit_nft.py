
import streamlit as st
import pandas as pd
from PIL import Image
from web3 import Web3
import os
from dotenv import load_dotenv
from pathlib import Path
import json
from datetime import datetime,timezone,timedelta

#EH: load env file
load_dotenv()


# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


# EH: Set streamlit layout as wide
st.set_page_config(page_title="NFT Submission",layout="wide")

#EH: define load contract function

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


#EH: Get seller information
st.header('NFT Submission for Auction Application')


username=st.text_input(label='Username')
public_key=st.text_input(label='Public Key')
asset_caption=st.text_input(label='Asset Name')
bid_start=st.number_input("Enter Desired Bid Start amount in Token",min_value=1000,step=1000)

close_date_request = st.date_input(
     "Please enter bid close date(UTC)",
     datetime.now()+timedelta(days=7),min_value=datetime.now() +timedelta(days=7))
st.write('Your close date (UTC) request is:', close_date_request)


def load_image(image_file):
	img = Image.open(image_file)
	return img


st.subheader("NFT Image")

#EH: upload nft file
image_file = st.file_uploader("Upload Images",
     type=["png","jpg","jpeg"])



if image_file is not None and (len(username) > 0) and (len(public_key)>0) and (len(asset_caption)>0):
          # TO See details
          file_details = {"filename":image_file.name, "filetype":image_file.type,
                    "fileslocation":image_file.size,"Owner Name":username,'Public Key':public_key,'Asset Name':asset_caption,'bid start amount':bid_start,"Bid close date":close_date_request.isoformat()}

          st.write("Please preview transaction detail before submission.")
          st.write(file_details)
          st.image(load_image(image_file), width=1000)
          
          #Saving upload
          with open(os.path.join("fileDir",image_file.name),"wb") as f:
               f.write((image_file).getbuffer())
          
          
          st.success("File Saved to local fileDir folder")

          #EH: Submit NFT for auction  
          submit=st.button("Submit Auction Request")
          st.write('By click this button, you agree and are subject to T&C of auction company.')

          if submit:
               
               trx_hash=contract.functions.nftRegistration(
                    public_key,#Owner address
                    asset_caption,#art name
                    username,#artist/owner name
                    int(bid_start),#initial appraisal value
                    str(image_file.size)#tokenURI

               ).transact({'from':public_key,'gas':1000000})

               receipt=w3.eth.waitForTransactionReceipt(trx_hash)

              #EH: provide trx hash and asset hash

               st.write("Transaction receipt mined:")
               st.write(dict(receipt))
               st.markdown("---")

               #EH: display transaction confirmation
               trx_df=pd.DataFrame(file_details,index=[0])
               st.dataframe(trx_df)



else:
     st.write("Please check inputs.") 

