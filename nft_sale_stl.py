#EH: import library

import streamlit as st
import json
import pandas as pd
from datetime import datetime,timezone
import os
from web3 import Web3
from dotenv import load_dotenv
from pathlib import Path

w3 = Web3(Web3.HTTPProvider('HTTP:#127.0.0.1:7545'))


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


#EH: set trx count
trx_count=w3.eth.get_transaction_count(public_key1)
#st.write('trx_count:',trx_count)


#EH:  inspection approval section
with st.expander('************Inspection Section***************'):
    st.write('Inspector Account Balance:', acct_bal)
    inspector_private_key=st.text_input(label="Inspector private key")
    inspect_result=st.button(label='Inspection Appoval')

    #EH: inspection apprval condition
    if inspect_result and len(inspector_private_key)>0:
        
        #EH: set payload
        payload={'from': public_key1, 'nonce': trx_count}

        #EH: build raw trx from smart contract inspect function
        raw_inspect_txn=contract.functions.inspect().buildTransaction(payload)

        #EH: sign trx
        signed_txn=w3.eth.account.signTransaction(raw_inspect_txn, private_key=inspector_private_key)

        #EH: send/sign transaction
        inspect_trx=w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        
        #EH: display approval confirmation
        st.write('inspection approval confirmation:', inspect_trx)

        #EH: display asset name
        st.write('asset address:',contract.functions.get_nft().call())


#EH:  display inspectation status
if contract.functions.get_inspect_status().call() == True:
    inspect_status="Pass"
else:
    inspect_status="Fail"
st.write('NFT authetication inspection status:',inspect_status)


#EH:  Bidder Payment submission section

#EH: set asset owner variable 

asset_owner=contract.functions.owner().call()  
   

with st.expander('************Buyer trx Section***************'):
    #EH: get buyer private key
    buyer_private_key=st.text_input(label="buyer private key",placeholder=0*32)

    #EH: check buyer account balance
    payer_acct_bal=w3.eth.get_balance(public_key1)
    st.write('Payer Account Balance:', acct_bal)

    #EH: set payment submission button
    buyer_pay=st.button(label='Payer submits Payment')

    if buyer_pay:

        #EH: set payload
        payload={'from': public_key1,'nonce': trx_count, 'value':(nft_bid_df['Bid amount'].iloc[0]).astype(int).item()}

        #EH: build raw trx from pay nft function
        raw_pay_txn=contract.functions.pay_nft(public_key1).buildTransaction(payload)

        #EH: sign trx
        signed_txn=w3.eth.account.signTransaction(raw_pay_txn, private_key=buyer_private_key)

        #EH: send trx
        pay_trx=w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        #EH: display confirmation
        st.write('Payer payment confirmation:', pay_trx)

#EH: display payment date
pay_date=datetime.fromtimestamp(contract.functions.get_pay_date(public_key1).call())
st.write('Payment date:',pay_date)



# st.write(contract.all_functions()[0])
st.write('contract address')
st.write(contract.address)
# st.write ('contract functions')
#st.write(list(contract.functions))

#get nft
if st.button(list(contract.functions)[1]):  st.write(contract.functions.get_nft().call())

#owner
if st.button(list(contract.functions)[2]):
    
    st.write(asset_owner)   
    st.write(f'balance:{w3.eth.get_balance(asset_owner)}') 

#get inspection status
if st.button(list(contract.functions)[4]):  st.write(contract.functions.get_inspect_status().call()) 


#get pay date
if st.button(list(contract.functions)[7]):  st.write(datetime.fromtimestamp(contract.functions.get_pay_date(public_key1).call()))

#transfer asset
final_private_key=st.text_input(label="nft receiver private key",placeholder=0*32)

#EH: set transfer nft function
if st.button(list(contract.functions)[3]):

    #set  payload
    payload={'from': public_key1, 'nonce': trx_count}

    #EH: build trx
    raw_inspect_txn=contract.functions.transfer_nft(public_key1).buildTransaction(payload)
    #EH: sign trx
    signed_txn=w3.eth.account.signTransaction(raw_inspect_txn, private_key=final_private_key)
    #EH: send trx
    transfer_trx=w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    #EH: display confirmation number
    st.write('nft transfer confirmation:', transfer_trx)









