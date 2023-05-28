var Market = artifacts.require("./Market.sol");
var UserHistory = artifacts.require("./UserHistory.sol");

module.exports = function(deployer) {
  deployer.deploy(Market);
  deployer.deploy(UserHistory);
};
