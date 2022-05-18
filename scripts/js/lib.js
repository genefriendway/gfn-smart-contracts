const fs = require('fs');


const readFromJSON = (jsonFile) => {
    let rawdata = fs.readFileSync(jsonFile);
    if(Object.entries(rawdata).length === 0) {
        rawdata = '{}';
    }
    return JSON.parse(rawdata);
}

const writeToJSON = (jsonData, output) => {
    let data = JSON.stringify(jsonData);
    fs.writeFileSync(output, data);
}

module.exports = {
    readFromJSON: readFromJSON,
    writeToJSON: writeToJSON
};