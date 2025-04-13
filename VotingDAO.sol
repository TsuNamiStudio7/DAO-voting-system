// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingDAO {
    struct Proposal {
        string description;
        uint voteCount;
    }

    address public chairperson;
    mapping(address => bool) public hasVoted;
    Proposal[] public proposals;

    constructor() {
        chairperson = msg.sender;
    }

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            voteCount: 0
        }));
    }

    function vote(uint proposalId) public {
        require(!hasVoted[msg.sender], "You have already voted.");
        require(proposalId < proposals.length, "Invalid proposal.");

        proposals[proposalId].voteCount += 1;
        hasVoted[msg.sender] = true;
    }

    function getProposal(uint proposalId) public view returns (string memory desc, uint count) {
        Proposal storage p = proposals[proposalId];
        return (p.description, p.voteCount);
    }

    function totalProposals() public view returns (uint) {
        return proposals.length;
    }
}
