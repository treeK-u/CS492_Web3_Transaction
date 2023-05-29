pragma solidity ^0.7.0;

contract UserHistory {
    struct UserSessionHistory {
        uint id;
        string sessionId;
        address userAddress;
        uint visitCount;

        string firstLoginTimestamp;
        string lastLoginTimestamp;
    }

    uint public userCount = 0;
    mapping(uint => string) public idSidTable;
    mapping(string => UserSessionHistory) public historyList;

    // Events
    event historyCreated(
        string sessionId,
        address userAddress,
        string firstLoginTimestamp
    );

    event historyUpdated(
        string sessionId,
        address userAddress,
        string lastLoginTimestamp
    );

    function createHistory(string memory sessionId, address userAddress, string memory firstTimestamp) public {
        userCount++;
        historyList[sessionId] = UserSessionHistory(userCount, sessionId, userAddress, 1, firstTimestamp, firstTimestamp);

        idSidTable[userCount] = sessionId;
        emit historyCreated(sessionId, userAddress, firstTimestamp);
    }

    function updateHistory(string memory sessionId, address userAddress, string memory timestamp) public {
        UserSessionHistory memory _history = historyList[sessionId];

        _history.userAddress = userAddress;
        _history.lastLoginTimestamp = timestamp;
        _history.visitCount++;

        historyList[sessionId] = _history;

        emit historyUpdated(sessionId, _history.userAddress, timestamp);
    }
}
