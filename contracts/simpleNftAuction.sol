// SPDX-License-Identifier: GPL-3.0-
// from https://github.com/darubiomunoz/smartcontract-simpleauction/blob/master/5-SimpleAuction.sol
pragma solidity >=0.7.0 <0.9.0;

contract SimpleNftAuction {
    // Parameters of the auction.
    // Times are either absolute unix timestamp (seconds since 1970-01-01) or 
    // use https://www.unixtimestamp.com/ to help conversion or
    // enter time periods in seconds in _biddingtime field 
    address payable public beneficiary;
    uint public auctionEndTime; 

    // Current state of the auction.
    address public highestBidder;
    uint public highestBid;

    // Allowed withdrawls of previous bids.
    mapping(address => uint) pendingReturns;

    // Set to true at the end, disallows any changes.
    // By default initialized to "false".
    bool ended;

    // Events that will be emitted on changes.
    event HighestBidIncreased(address bidder, uint amount);
    event AuctionEnded(address winner, uint amount);

    // The following is a so-called natspec comment, recognizable by the three slashes.
    // It will be shown when the user is asked to confirm the transaction.

    /// Create a simple auction with "_biddingTime" seconds bidding 
    /// time on behalf of the beneficiary address "_beneficiary"
    constructor(uint _biddingTime, address payable _beneficiary) {
        beneficiary = _beneficiary;
        auctionEndTime = block.timestamp + _biddingTime;
    }

    /// Bid on the auction with the value sent together with this transaction.
    /// The value will only be refunded if the auction is not won.
    function bid() public payable {
        // No arguments are necessary, all information is already part of the transaction.
        // The keyword payable is required for the function to be able to receive Ether.

        // Revert the call if the bidding period is over.
        require(block.timestamp <= auctionEndTime, "The auction has already ended.");

        // If the bid is not higher, send the money back
        // (the failing require will revert all changes in this function execution including it having received the money).
        require(msg.value >= highestBid, "There's already a higher bid. Try bidding higher!");

        if(highestBid != 0) {
            // Sending back the money by simply using highestBidder.send(highestBid) is a security risk because it could execute an untrusted contract.
            // It is always safer to let the receipients withdraw their money themselves.
            pendingReturns[highestBidder] += highestBid;
        }

        highestBidder = msg.sender;
        highestBid = msg.value;

        emit HighestBidIncreased(msg.sender, msg.value);
    }
    /// @TODO: (Next step) 
    /// Withdraw a bid that was overbid.
    // function withdraw() public returns(bool) {
        // uint amount = pendingReturns[msg.sender];

        // if(amount > 0) {
            // It is important to set this to zero because the recipient can call this function again as part of the receiving call before "send" returns.
            // pendingReturns[msg.sender] = 0;

            // if(!payable(msg.sender).send(amount)) {
                // No need to call throw here, just reset the amount owing.
                // pendingReturns[msg.sender] = amount;
                // return false;
            // }
        // }

        // return true;
    // }

    /// End the auction and send the highest bid to the beneficiary. 
    function auctionEnd() public {
        // It is a good guideline to structure functions that interact with other contracts 
        // (i.e. they call functions or send Ether) into three phases:
        // 1. Checking conditions.
        // 2. Performing actions (potentially changing conditions).
        // 3. Interacting with other contracts.
        // If these phases are mixed up, the other contract could call back into the current contract and modify the state or cause effects (ether payout) to be performed multiple times.
        // If functions called internally include interaction with external contracts, they also have to be considered interaction with external contracts.

        // Conditions
        require(block.timestamp >= auctionEndTime, "The auction hasn't ended yet.");
        require(!ended, "auctionEnd has already been called.");

        // Effects
        ended = true;
        emit AuctionEnded(highestBidder, highestBid);

        // Interaction
        beneficiary.transfer(highestBid);
    }
}

contract nft_sale_approval {
    string _tokenURI;
    uint _highestBid;
    bool _inspected=false;
    address payable public owner=msg.sender; 

    mapping(address => uint256) pay_stamp;
    // mapping(address => uint) offers;

    constructor(string memory tokenURI, address payable beneficiary) {
        _tokenURI=tokenURI;
        beneficiary=owner;
    }

    function get_address() view public returns(string memory) {
        return _tokenURI;
    }

    function inspect() public {
        _inspected=true;
    }

    function get_inspect_status() view public returns(bool) {
        return _inspected;
    }

    function transfer_property(address payable buyer) public {
        require(_inspected==true);
        owner=buyer;
    }

    function pay_property(address payable buyer) public payable {
        require(_inspected==true);
        owner=buyer;
        msg.sender.transfer(_highestBid);
        pay_stamp[msg.sender]=block.timestamp;
    }

    function lender_approve(address payable approved) public payable { //verify AuctionEnded, confirm buyer funds, and transfer
        require(_inspected==true);
        require(pay_stamp[approved]>0);
        require(msg.value>_highestBid);
        // lender approves credit

        // calculate overpayment
        uint overpayment=msg.value-_highestBid;
        owner.transfer(_highestBid);
        msg.sender.transfer(overpayment);

        owner=approved;
    }

    function get_pay_date(address buyer) view public returns(uint256) {
        return pay_stamp[buyer];
    }
}