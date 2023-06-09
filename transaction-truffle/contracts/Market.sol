pragma solidity ^0.7.0;

contract Market {
    // Struct
    struct Commodity {
        uint id;
        string name;
        uint price;

        string category;
        string imgPath;
        string description;
        address sellerAddress;

        uint soldCount;
        bool isDeleted;
    }

    struct PurchaseHistory {
        uint id;
        uint commodityId;
        address buyerAddress;
        string purchaseTimestamp;
    }

    // Globals
    uint public commodityCount = 0;
    mapping(uint => Commodity) public commodityList;
    uint public purchaseCount = 0;
    PurchaseHistory[] public purchaseHistoryList;

    // Events
    event CommodityCreated(
        uint id,
        string name
    );

    event CommoditySold(
        uint id
    );


    function createCommodity(
        string memory _name,
        uint _price,
        string memory _category,
        string memory _imgPath,
        string memory description,
        address sellerAddress
    ) public {
        commodityCount++;

        commodityList[commodityCount] = Commodity(
            commodityCount,
            _name,
            _price,
            _category,
            _imgPath,
            description,
            sellerAddress,
            0,
            false
        );

        emit CommodityCreated(commodityCount, _name);
    }

    function soldCommodity(uint _id, address buyerAddress, string memory timestamp) public {
        Commodity memory _commodity = commodityList[_id];
        _commodity.soldCount++;

        commodityList[_id] = _commodity;

        purchaseCount++;
        purchaseHistoryList.push(PurchaseHistory(
            purchaseCount,
            _id,
            buyerAddress,
            timestamp
        ));
        emit CommoditySold(_id);
    }

    function deleteCommodity(uint _id) public {
        Commodity memory _commodity = commodityList[_id];
        _commodity.isDeleted = true;

        commodityList[_id] = _commodity;
    }
}