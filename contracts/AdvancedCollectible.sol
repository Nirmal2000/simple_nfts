pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter; //check if erc721 variable
    bytes32 public keyHash;
    uint256 public fee;    
    enum Breed {PUB, SHIBA, ST_BERNARD}
    mapping(uint256 => Breed) public tokenIdtoBreed;
    mapping(bytes32 => address) public reqIdtoSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event BreedAssigned(uint256 indexed tokenId, Breed breed );

    constructor(address _VRFCoordinator, address _linkToken, bytes32 _keyHash, uint256 _fee) public 
    VRFConsumerBase(_VRFCoordinator, _linkToken)
    ERC721 ("Doggie", "DOG"){
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (uint256){
        bytes32 reqId = requestRandomness(keyHash, fee);
        reqIdtoSender[reqId] = msg.sender;
        emit requestedCollectible(reqId, msg.sender);
    }

    function fulfillRandomness(bytes32 _reqID, uint256 randomNumber) internal override {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdtoBreed[newTokenId] = breed;
        emit BreedAssigned(newTokenId, breed);
        address owner = reqIdtoSender[_reqID];        
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;

    }

    function setTokenURI(uint256 tokId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokId), "caller is not owner or caller");
        _setTokenURI(tokId, _tokenURI);
    }
}