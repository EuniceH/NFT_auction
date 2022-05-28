import streamlit as st
import pandas as pd
from datetime import datetime,timezone
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))


# #EH: create function for bid entry dataframe
# def bid_entry(name, key, bid_amt):
#     bid_df=pd.DataFrame()
#     bid_df['name']=name
#     bid_df['Etherium_public_key']=key
#     bid_df['Bid amount in Token']=bid_amt
    

#     return bid_df


    
#EH: add cache decorator for streamlit
#@st.cache(allow_output_mutation=True)


# EH: Set layout as wide
st.set_page_config(page_title="NFT Auction",layout="wide")
# EH: set max screen width.
st.markdown(
        f"""<style>.main .block-container{{ max-width: 1600px }} </style> """,
        unsafe_allow_html=True,
)

#st.title('NFT Auction')


#EH:  create dictionary for NFT
nft_database = {
    "Laker_NFT1": ["Laker", 4000, datetime(2022, 6, 18, 0, 0, tzinfo=timezone.utc).isoformat(), "Images/image1.png"],
    "1990_NFT2": ["1990", 5000, datetime(2022, 6, 1, 0, 0, tzinfo=timezone.utc).isoformat(),"Images/image2.png"],
    "AllStar_NFT3": ["AllStar",7000, datetime(2022, 6, 8, 0, 0, tzinfo=timezone.utc).isoformat(),"Images/image3.png"]
}



# "st.session_state object:",st.session_state

# if 'prev_bid' not in st.session_state:
#     st.session_state['prev_bid']=''





#EH: Sidebar section
#with st.sidebar:

#EH: select auction item
st.sidebar.header('Auction Item Selection')
nft_option = st.sidebar.selectbox(
 'Please select auction NFT item.',
 (nft_database.keys()))

st.sidebar.write('You selected:', nft_option)

st.sidebar.write('**********************')





#EH: Get bidder's information
st.sidebar.subheader('Auction Entry Form')
prev_bid=[nft_database[nft_option][1]]

username=st.sidebar.text_input(label='Username')
public_key=st.sidebar.text_input(label='Public Key')

#EH:  Chris, Please take a look this portion
bid_amount=st.sidebar.number_input("Enter Bid amount in Token",min_value=prev_bid[-1]+5,step=5)

if(st.sidebar.button("Bid Submission")==True):
    latest_bid=pd.DataFrame({"Name":username,"Public Key":public_key,"Highest Bid":bid_amount},index=[0])

    #EH: Display register dataframe
    st.sidebar.subheader('Auction highest bid')
    st.sidebar.dataframe(latest_bid)
    #st.sidebar.write("Current highest Bid Amount in Token: ",latest_bid["Highest Bid"][0])
    
    prev_bid.append(bid_amount)


#counter of bids
#dataframe for history (username, nft, bid counts,token amount, sort by the highest bid counts)
#timer (Chris)

            





    
    


    #EH: highest bidder pays token

if(st.sidebar.button("Pay with Token")==True):
    st.sidebar.write("hash trx","##########")
    st.sidebar.balloons()


#EH: Main section

st.image(f'Images/image{nft_option[-1]}.png',width=1200)
st.write("NFT: ", nft_database[nft_option][0])
st.write("Close Date: ", nft_database[nft_option][2])
st.write("Current highest Bid Amount in Token: ",prev_bid[-1])

st.text(" \n")

col1, col2, col3, col4 = st.columns([0.1, 3, 1,2])




#EH: Display Bidding transactions
#st.dataframe(my_dataframe)


