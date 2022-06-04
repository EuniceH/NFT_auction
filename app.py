
import streamlit as st
import pandas as pd
from datetime import datetime,timezone
import time
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))


st.set_page_config(page_title="NFT Auction",layout="wide")
st.markdown(
"""
<style>
[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
width: 600px;
}
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
width: 500px;
margin-left: -600px;
}
</style>
""",
unsafe_allow_html=True
)
# #EH: add cache decorator for streamlit
# @st.cache(allow_output_mutation=True)


#EH: append bid records
def bid_join(df1,df2):
    join_df=pd.concat([df1,df2],ignore_index=True)

    return join_df

#EH: reset session state
def delete_ss():
    del st.session_state['prev_bid']
    del st.session_state['counter']
    del st.session_state['current_bid']
    del st.session_state['bid_history']

st.title('NFT Auction')


#EH:  create dictionary for NFT
nft_database = {
    "Laker_NFT1": ["Laker", 4000, datetime(2022, 6, 18, 0, 0, tzinfo=timezone.utc).isoformat(), "Images/image1.png"],
    "1990_NFT2": ["1990", 5000, datetime(2022, 6, 1, 0, 0, tzinfo=timezone.utc).isoformat(),"Images/image2.png"],
    "AllStar_NFT3": ["AllStar",7000, datetime(2022, 6, 8, 0, 0, tzinfo=timezone.utc).isoformat(),"Images/image3.png"]
}


#EH: select auction item
st.sidebar.header('Auction Item Selection')
nft_option = st.sidebar.selectbox(
 'Please select auction NFT item.',
 (nft_database.keys()),on_change=(delete_ss))

# "st.session_state object:",st.session_state

if 'prev_bid' not in st.session_state:
    st.session_state['prev_bid']=nft_database[nft_option][1]

if 'counter' not in st.session_state:
    st.session_state['counter']=0

if 'current_bid' not in st.session_state:
    st.session_state['current_bid']=nft_database[nft_option][1]

if 'bid_history' not in st.session_state:
    st.session_state['bid_history']=pd.DataFrame(columns=["Asset Name","Name","Bid amount","Public Key","hash confirmation"],index=[1])


#EH: set session state
def session_setup():
        st.session_state['prev_bid']=st.session_state['prev_bid']
        st.session_state['counter']=st.session_state['counter']
        st.session_state['current_bid']=st.session_state['current_bid']
    






#EH: Sidebar section



st.sidebar.write('You selected:', nft_option)

st.sidebar.write('**********************')





#EH: Get bidder's information
st.sidebar.subheader('Auction Entry Form')


username=st.sidebar.text_input(label='Username',on_change=session_setup)
public_key=st.sidebar.text_input(label='Public Key')

#EH: Set bid value floor
def min_set(x,y):
    if x>y:
        x
    else:
        x=y
    
    return x
    

#EH:  get bid amount input
bid_amount=st.sidebar.number_input("Enter Bid amount in Token",min_value=min_set(st.session_state['current_bid'],nft_database[nft_option][1]+5),step=5)

bid_entry={"Asset Name":nft_database[nft_option][0],"Name":username,"Bid amount":bid_amount,"Public Key":public_key}

asset_list=list(nft_database.keys())



#EH: Bid submission button and criteria
if st.sidebar.button("Bid Submission"):

    #EH: criteria of higher than current bid amount, validating username and public key
    if bid_amount > st.session_state['prev_bid'] and (len(username) > 0) and (len(public_key)>0):
        
        #EH: Log bid entry
        single_entry_df=pd.DataFrame(bid_entry,index=[st.session_state['counter']+1])
        single_entry_df['hash confirmation']="placeholder"

        st.sidebar.subheader("Bid Transaction Confirmation:")

        st.sidebar.dataframe(single_entry_df)

        #EH: add bid entry to bid history dataframe
        st.session_state['bid_history']=bid_join(st.session_state['bid_history'],single_entry_df)   

        #EH: update session state info
        st.session_state['prev_bid']=st.session_state['current_bid']
        st.session_state['current_bid']=bid_amount
        st.session_state['counter']+=1

    #EH: error message
    else:
        st.sidebar.write('Error! Please check your input!')

#EH: display bid history
st.sidebar.subheader("Bid Rank")

st.sidebar.dataframe((st.session_state['bid_history'].iloc[1:,:-2]).sort_values(by=['Bid amount'], ascending=False).style.highlight_max(['Bid amount'],axis=0))





#EH: Main section
#EH: Display asset and bid information
st.image(f'Images/image{nft_option[-1]}.png',width=700)
st.write("NFT: ", nft_database[nft_option][0])
st.write("Close Date: ", nft_database[nft_option][2])
st.write("Start Bid Amount in Token: ",nft_database[nft_option][1])


#EH: transadation data for user preview
st.write("Please preview bid transaction detail before submission.")
st.write(bid_entry)



#EH: Set Time Counter

curr_date=datetime.now(timezone.utc)
closing_date=datetime.fromisoformat(nft_database[nft_option][2])
delta=int((closing_date-curr_date).total_seconds())

ph = st.empty()

for secs in range(delta,0,-1):
    dd=secs//86400
    hh=secs//3600-dd*24
    mm, ss =(secs//60-(secs//3600)*60), secs%60
    ph.metric("Countdown", f"{dd:02d}Days:{hh:02d}Hours:{mm:02d}Mins:{ss:02d}")
    time.sleep(1)




