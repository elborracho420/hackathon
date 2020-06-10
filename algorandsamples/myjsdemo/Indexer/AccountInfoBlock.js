//AccountInfo.js
const algosdk = require('algosdk');
const indexer_token = "";
const indexer_server = "http://localhost";
const indexer_port = 8980;

// Instantiate the indexer client wrapper
let indexerClient = new algosdk.Indexer(indexer_token, indexer_server, indexer_port);

(async () => {
    let acct = "7WENHRCKEAZHD37QMB5T7I2KWU7IZGMCC3EVAO7TQADV7V5APXOKUBILCI";
    let round = 6127857;

    let accountInfo = await indexerClient.lookupAccountByID(acct)
        .round(round).do();
    console.log("Information for Account at block: " + JSON.stringify(accountInfo, undefined, 2));
})().catch(e => {
    console.log(e);
    console.trace();
});