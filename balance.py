import urllib, json

##Accesses DwarfPool stats page with given URL.
##Takes an Ethereum Wallet address without 0x.
##Returns a list of lines of the string of the DwarfPool stats page HTML
def retrieveHTML(address):
    f = urllib.urlopen("http://dwarfpool.com/eth/address?wallet="+address).read().splitlines()
    return f

##Scrapes ether amounts from DwarfPool HTML string
##Takes a list of lines of the string of the DwarfPool stats page HTML
##Returns the total Ether mined to an Ethereum Wallet Address
def findValues(lineList):
    currentBalance = 0
    confirmed = 0
    unconfirmed = 0
    for i in range(len(lineList)):
        if "Current balance" in lineList[i]:
            currentBalance = float(lineList[i-1][lineList[i-1].find(">")+1:lineList[i-1].find(" ETH")])
        if "Confirmed but still not on balance" in lineList[i]:
            confirmed = float(lineList[i-1][lineList[i-1].find(">")+1:lineList[i-1].find(" ETH")])
        if "Unconfirmed" in lineList[i]:
            unconfirmed = float(lineList[i-1][lineList[i-1].find(">")+1:lineList[i-1].find(" ETH")])
            
    return currentBalance+confirmed+unconfirmed

##Retrieves the current exchange rate USD/ETH
##Takes an ether amount
##Returns amount of dollars for the given amount of ether
def dollarConversion(eth):
    url = "https://api.coinbase.com/v2/exchange-rates?currency=ETH"
    resp = urllib.urlopen(url).read()
    data = json.loads(resp)
    return eth*float(data["data"]["rates"]["USD"])

##Runs the above functions,
##prompts the user for an Ethereum Wallet address,
##and prints current ether and dollar balances for the given Dwarfpool account
def main():
    address = raw_input("Enter your Ethereum Wallet address used with Dwarfpool (without \"0x\"): ")
    ethValue = findValues(retrieveHTML(address))
    dollars = dollarConversion(ethValue)
    print "You have mined " + str(ethValue) + " ETH, which is $" + str(dollars) + "."
    




main()

