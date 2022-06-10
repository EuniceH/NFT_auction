import streamlit as st
import json
import pandas as pd
from datetime import datetime,timezone
import os
from web3 import Web3
from dotenv import load_dotenv
from pathlib import Path
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))


#EH: load env file
load_dotenv()


# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


# EH: Set streamlit layout as wide
st.set_page_config(page_title="NFT Approvals",layout="wide")



#EH: define load contract function

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/nft_sale_approval_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("NFT_SALE_APPROVAL_ADDRESS")

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
st.header('NFT Transfer Approval')

#EH: display highest bid record
nft=st.selectbox(label="NFT Selection",options={'Laker_NFT1','1990_NFT2','AllStar_NFT3'})
nft_bid_df=pd.read_csv(Path(f'./bid_history/{nft}_bid_history.csv'),header=0,index_col=0)
nft_bid_df=nft_bid_df.iloc[[-1]]
st.subheader('Highest Bid')
st.dataframe(nft_bid_df)


#EH:  account public key selection
username=st.text_input(label='Transactor')
accounts = w3.eth.accounts
public_key1=st.selectbox("Select Account", options=accounts)

#EH:  check buyer account balance

acct_bal=w3.eth.get_balance(public_key1)


trx_count=w3.eth.get_transaction_count(public_key1)
#st.write('trx_count:',trx_count)


#EH:  inspection approval
with st.expander('************Inspection Section***************'):
    st.write('Inspector Account Balance:', acct_bal)
    inspector_private_key=st.text_input(label="Inspector private key")
    inspect_result=st.button(label='Inspection Appoval')
    if inspect_result and len(inspector_private_key)>0:
        
        
        payload={'from': public_key1, 'nonce': trx_count}

        raw_inspect_txn=contract.functions.inspect().buildTransaction(payload)
        signed_txn=w3.eth.account.signTransaction(raw_inspect_txn, private_key=inspector_private_key)
        inspect_trx=w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        
        st.write('inspection approval confirmation:', inspect_trx)
        #st.write('NFT authetication inspection status:',inspect_status)
        st.write('asset address:',contract.functions.get_address().call())

if contract.functions.get_inspect_status().call() == True:
    inspect_status="Pass"
else:
    inspect_status="Fail"
st.write('NFT authetication inspection status:',inspect_status)
        

#EH:  Final Bidder Payment submission 

seller_public_key="0xb8eF5cbB02657b79A5B9F98Abf44B119f218e9aC"   

with st.expander('************Buyer trx Section***************'):
    # if st.button('Payer submits Payment'): 
        #if contract.functions.get_inspect_status().call()==True:
            # public_key2=st.selectbox("Select Account", options=accounts)
    buyer_private_key=st.text_input(label="buyer private key",placeholder=0*32)


    payer_acct_bal=w3.eth.get_balance(public_key1)
    st.write('Payer Account Balance:', acct_bal)

    buyer_pay=st.button(label='Payer submits Payment')

    if buyer_pay:
        payload={'from': public_key1, 'nonce': trx_count, 'value':(nft_bid_df['Bid amount'].iloc[0]).astype(int).item()}

        raw_pay_txn=contract.functions.pay_property(public_key1).buildTransaction(payload)
        signed_txn=w3.eth.account.signTransaction(raw_pay_txn, private_key=buyer_private_key)
        pay_trx=w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        st.write('Payer payment confirmation:', pay_trx)
pay_date=datetime.fromtimestamp(contract.functions.get_pay_date(public_key1).call())
st.write('Payment date:',pay_date)

#EH: auction service approval


# with st.expander('************Auction Service Approval***************'):

#     service_private_key=st.text_input(label="auction service private key")
#     service_acct_bal=w3.eth.get_balance(public_key1)
#     st.write('Auction service Account Balance:', acct_bal)
    
#     if len(pay_trx)>0:    
                
#         if st.button(label="Final Approval by auction service company"):     
                
#             payload={'from': public_key1, 'nonce': trx_count, 'value': 1001}

#             Buyer_public_key=st.text_input(label="Enter Buyer public key",placeholder=0*32)


#             raw_final_approve_txn=contract.functions.lender_approve(Buyer_public_key).buildTransaction(payload)
#             signed_txn=w3.eth.account.signTransaction(raw_final_approve_txn, private_key=service_private_key)
#             service_approval_trx=w3.eth.sendRawTransaction(signed_txn.rawTransaction)
# st.write('Final Approval by auction service confirmation:',service_approval_trx)









