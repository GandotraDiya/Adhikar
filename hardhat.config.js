require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
  paths: {
    sources: "./blockchain/contracts", // This allows you to keep contracts in this subfolder
    artifacts: "./artifacts",
    cache: "./cache",
    tests: "./test"
  }
};
