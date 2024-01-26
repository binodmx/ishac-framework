// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Oracle {
    struct Request {
        uint id;
        bytes32 attributeName;
        mapping(address => bytes32) attributeValues;
    }
    event RequestEvent(uint id, bytes32 name);
    event ResponseEvent(uint id, bytes32 value);
    event DebugEvent(string message);
    mapping(uint => Request) public requests;
    address[] public oracleNodes;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function addOracleNode(address _oracleNode) public {
        emit DebugEvent("[DEBUG] addOracleNode() called");
        require(msg.sender == owner, "Only the owner can add oracle nodes");
        oracleNodes.push(_oracleNode);
        emit DebugEvent("[DEBUG] oracle node added");
    }

    function removeOracleNode(address _oracleNode) public {
        emit DebugEvent("[DEBUG] removeOracleNode() called");
        require(msg.sender == owner, "Only the owner can remove oracle nodes");
        for (uint i = 0; i < oracleNodes.length; i++) {
            if (oracleNodes[i] == _oracleNode) {
                delete oracleNodes[i];
                break;
            }
        }
        emit DebugEvent("[DEBUG] oracle node removed");
    }
    
    function createRequest(uint _id, bytes32 _attributeName) public {
        emit DebugEvent("[DEBUG] createRequest() called");
        Request storage request = requests[_id];
        request.id = _id;
        request.attributeName = _attributeName;
        emit RequestEvent(_id, _attributeName);
    }

    function updateRequest(uint _id, bytes32 _valueRetrieved) public {
        emit DebugEvent("[DEBUG] updateRequest() called");
        for (uint i = 0; i < oracleNodes.length; i++) {
            if (oracleNodes[i] == msg.sender) {
                requests[_id].attributeValues[msg.sender] = _valueRetrieved;
                emit DebugEvent("[DEBUG] request updated");
                createResponse(_id);
                break;
            }
        }
    }

    function createResponse(uint _id) private {
        emit DebugEvent("[DEBUG] createResponse() called");
        bytes32[] memory values = new bytes32[](oracleNodes.length);
        for (uint i = 0; i < oracleNodes.length; i++) {
            if (requests[_id].attributeValues[oracleNodes[i]] != 0) {
                values[i] = requests[_id].attributeValues[oracleNodes[i]];
            }
        }
        
        bytes32 mode;
        uint absMode;
        uint maxCount;
        for (uint i = 0; i < values.length; i++) {
            uint count = 0;
            for (uint j = 0; j < values.length; j++) {
                if (values[i] == values[j]) {
                    count++;
                }
            }
            if (count > maxCount) {
                maxCount = count;
                absMode = 1;
                mode = values[i];
            } else if (count != 0 && count == maxCount && mode != values[i]) {
                absMode++;
            }
        }

        uint quorum = (oracleNodes.length - 1) / 2 + 1;
        if (maxCount >= quorum && absMode == 1) {
            emit ResponseEvent(_id, mode);
        }
    }
}
