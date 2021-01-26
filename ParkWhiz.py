import requests
import sys
import boto3
import time

# get SNS client
client = boto3.client("sns")
# Get a specific date's availability
def getSpecificDate(dateAvailability, location):
    # set default location id
    locationID = ''
    if location == "Copper Mountain":
        locationID = '448854'
    url = "https://api.parkwhiz.com/v4/venues/" + locationID + "/events/?&pretty=true&fields=venue::default,event::default,event:availability,site_url"
    #response = requests.get("https://api.parkwhiz.com/v4/venues/448854/events/?&pretty=true&fields=venue::default,event::default,event:availability,site_url")
    response = requests.get(url)
    # print(response.json())
    copperAvailabilityJSON = response.json()
    for dateWanted in copperAvailabilityJSON:
        if dateWanted['name'] == dateAvailability:
            #print(dateWanted['site_url'])
            #print(dateWanted['availability'])
            return (dateWanted)

#isAvailable = getSpecificDate('Feb 7 2021 Daily Parking', 'Copper Moiuntain')

# Run like this:
# python ParkWhiz.py "Feb 16 2021 Daily Parking" "Copper Mountain" "+14844333269"

if __name__ == '__main__':
    date = str(sys.argv[1])
    location = str(sys.argv[2])
    if len(sys.argv) > 3:
        phoneNumber = str(sys.argv[3])
    checkOut = False
    checkoutTries = 1
    if len(sys.argv) > 3:
        if str(sys.argv[3]) == "-e":
            expiration = int(sys.argv[4])
    else:
        expiration = 3600
    
    while not checkOut:
        isAvailable = getSpecificDate(date, location)
        if isAvailable['availability']['available'] > 0:
            # add logic here to send text message
            bookUrl = "https://www.parkwhiz.com" + isAvailable['site_url']
            dateAvailable = str(isAvailable['start_time'])[0:10]
            #client.publish(
            #    PhoneNumber=phoneNumber,
            #    Message= dateAvailable + '\n' + str(isAvailable['availability']) + '\n' + bookUrl
            #    )
            topic_arn = 'arn:aws:sns:us-east-1:001178231653:ParkingCopper'
            theMessage= dateAvailable + '\n' + str(isAvailable['availability']) + '\n' + bookUrl
            client.publish(Message=theMessage, TopicArn=topic_arn)
            print(isAvailable['site_url'])
            print(isAvailable['availability'])
            print("found a spot for " + date + ' after ' + str(checkoutTries) + ' times')
            # Kill the loop
            checkOut = True
        # wait one minute
        if not checkOut:
            print("tried to find spot for " + date + ' ' + str(checkoutTries) + ' times')
            checkoutTries += 1
            time.sleep(60)