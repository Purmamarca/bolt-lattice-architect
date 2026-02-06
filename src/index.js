"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getData = getData;
exports.postData = postData;
const quantum_safe_1 = require("@security/quantum-safe");
async function getData() {
    const response = await (0, quantum_safe_1.latticeHandshake)({
        url: 'https://api.example.com/data',
        method: 'GET',
        encryption: 'ML-KEM-768'
    });
    return response;
}
async function postData(data) {
    const response = await (0, quantum_safe_1.latticeHandshake)({
        url: 'https://api.example.com/data',
        method: 'POST',
        body: data,
        encryption: 'ML-KEM-768'
    });
    return response;
}
