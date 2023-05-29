pragma solidity ^0.7.0;

contract Market {
    // Struct
    struct Commodity {
        uint id;
        string name;
        uint price;
        bool isSold;

        string category;
        string imgPath;
        string description;
        address sellerAddress;
    }

    // Globals
    uint public commodityCount = 0;
    mapping(uint => Commodity) public commodityList;

    // Events
    event CommodityCreated(
        uint id,
        bool isSold
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
            false,
            _category,
            _imgPath,
            description,
            sellerAddress
        );

        emit CommodityCreated(commodityCount, false);
    }

    function soldCommodity(uint _id) public {
        Commodity memory _commodity = commodityList[_id];
        _commodity.isSold = !_commodity.isSold;
        commodityList[_id] = _commodity;
        emit CommoditySold(_id);
    }
}