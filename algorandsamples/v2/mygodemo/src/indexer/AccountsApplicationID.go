package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/algorand/go-algorand-sdk/client/v2/indexer"
)

// indexer host

const indexerAddress = "http://localhost:59998"
const indexerToken = ""

// query parameters
var applicationID uint64 = 70

func main() {
	// Create an indexer client
	indexerClient, err := indexer.MakeClient(indexerAddress, indexerToken)
	if err != nil {
		return
	}
	// Lookup application
	 result, err := indexerClient.SearchAccounts().ApplicationId(applicationID).Do(context.Background())
	// Print the results
	JSON, err := json.MarshalIndent(result, "", "\t")
	fmt.Printf(string(JSON) + "\n")
}
