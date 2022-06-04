
import streamlit as st
import pandas as pd
from PIL import Image
import os
from datetime import datetime,timezone,timedelta
# EH: Set layout as wide
st.set_page_config(page_title="NFT Submission",layout="wide")
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
                    "filesize":image_file.size,"Owner Name":username,'Public Key':public_key,'Asset Name':asset_caption,'bid start amount':bid_start,"Bid close date":close_date_request.isoformat()}

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

              #EH: provide trx hash and asset hash
              #EH: Need to write more exception syntax on this part
               st.write('transaction hash#')
               st.write('Asset hash#')

               #EH: display transaction confirmation
               trx_df=pd.DataFrame(file_details,index=[0])
               st.dataframe(trx_df)



else:
     st.write("Please check inputs.") 

