import requests
import time
import json
import sys
import os


def countdown(total_seconds):
    while total_seconds:
        # Calculate days, hours, minutes, and seconds
        days, remainder1 = divmod(total_seconds, 86400)  # 1 day = 86400 seconds
        hours, remainder2 = divmod(remainder1, 3600)     # 1 hour = 3600 seconds
        minutes, seconds = divmod(remainder2, 60)        # 1 minute = 60 seconds
        
        # Format the time remaining and display it conditionally
        time_str_parts = []
        if days:
            time_str_parts.append(f"{days} days")
        if hours:
            time_str_parts.append(f"{hours:02} hours")
        time_str_parts.append(f"{minutes:02} minutes")
        time_str_parts.append(f"{seconds:02} seconds")

        time_remaining = ", ".join(time_str_parts) + " remaining"
        
        # Use '\r' to return to the beginning of the line, 
        # so the new time overwrites the old time (clearing the terminal line)
        print(time_remaining, end='\r')
        
        # Wait for 1 second before updating the display
        time.sleep(1)
        total_seconds -= 1
    print(" " * len(time_remaining), end = "\r")
    print("Countdown completed!")


def get_lots_from_live_auction(lot_id, get_time_left=False):
    graphql_url = "https://hibid.com/graphql" 

    query = """
        query LiveCatalogLots($auctionId: Int!) {
            liveCatalogLots(id: $auctionId) {
                auction {
                    ...auction
                    __typename
                }
                liveLots {
                    ...lotOnly
                    __typename
                }
                upcomingLots {
                    ...lotOnly
                    __typename
                }
                __typename
            }
        }

        fragment auction on Auction {
            id
            altBiddingUrl
            altBiddingUrlCaption
            amexAccepted
            discoverAccepted
            mastercardAccepted
            visaAccepted
            regType
            holdAmount
            termsAndConditions
            auctioneer {
                ...auctioneer
                __typename
            }
            auctionNotice
            auctionOptions {
                bidding
                altBidding
                catalog
                liveCatalog
                shippingType
                preview
                registration
                webcast
                useLotNumber
                useSaleOrder
                __typename
            }
            auctionState {
                auctionStatus
                bidCardNumber
                isRegistered
                openLotCount
                timeToOpen
                __typename
            }
            bidAmountType
            biddingNotice
            bidIncrements {
                minBidIncrement
                upToAmount
                __typename
            }
            bidType
            buyerPremium
            buyerPremiumRate
            checkoutDateInfo
            previewDateInfo
            currencyAbbreviation
            description
            eventAddress
            eventCity
            eventDateBegin
            eventDateEnd
            eventDateInfo
            eventName
            eventState
            eventZip
            featuredPicture {
                description
                fullSizeLocation
                height
                thumbnailLocation
                width
                __typename
            }
            links {
                description
                id
                type
                url
                videoId
                __typename
            }
            lotCount
            showBuyerPremium
            audioVideoChatInfo {
                aVCEnabled
                blockChat
                __typename
            }
            shippingAndPickupInfo
            paymentInfo
            hidden
            sourceType
            __typename
        }

        fragment auctioneer on Auctioneer {
            address
            bidIncrementDisclaimer
            buyerRegNotesCaption
            city
            countryId
            country
            cRMID
            currencyExpressUrl
            email
            fax
            id
            internetAddress
            missingThumbnail
            name
            noMinimumCaption
            phone
            state
            postalCode
            __typename
        }

        fragment lotOnly on Lot {
            bidAmount
            bidList
            bidQuantity
            description
            estimate
            featuredPicture {
                description
                fullSizeLocation
                height
                thumbnailLocation
                width
                __typename
            }
            forceLiveCatalog
            fr8StarUrl
            hideLeadWithDescription
            id
            itemId
            lead
            links {
                description
                id
                type
                url
                videoId
                __typename
            }
            linkTypes
            lotNavigator {
                lotCount
                lotPosition
                nextId
                previousId
                __typename
            }
            lotNumber
            lotState {
                ...lotState
                __typename
            }
            pictureCount
            pictures {
                description
                fullSizeLocation
                height
                thumbnailLocation
                width
                __typename
            }
            quantity
            ringNumber
            rv
            category {
                baseCategoryId
                categoryName
                description
                fullCategory
                header
                id
                parentCategoryId
                uRLPath
                __typename
            }
            shippingOffered
            simulcastStatus
            site {
                currencyExpressUrl
                domain
                fr8StarUrl
                isDomainRequest
                isExtraWWWRequest
                siteType
                subdomain
                __typename
            }
            saleOrder
            __typename
        }

        fragment lotState on LotState {
            bidCount
            biddingExtended
            bidMax
            bidMaxTotal
            buyerBidStatus
            buyerHighBid
            buyerHighBidTotal
            buyNow
            choiceType
            highBid
            highBuyerId
            isArchived
            isClosed
            isHidden
            isLive
            isNotYetLive
            isOnLiveCatalog
            isPosted
            isPublicHidden
            isRegistered
            isWatching
            linkedSoftClose
            mayHaveWonStatus
            minBid
            priceRealized
            priceRealizedMessage
            priceRealizedPerEach
            productStatus
            productUrl
            quantitySold
            reserveSatisfied
            sealed
            showBidStatus
            showReserveStatus
            softCloseMinutes
            softCloseSeconds
            status
            timeLeft
            timeLeftLead
            timeLeftSeconds
            timeLeftTitle
            timeLeftWithLimboSeconds
            timeLeftWithLimboSeconds
            watchNotes
            __typename
        }
    """
    
    payload = {
        "operationName": "LiveCatalogLots",
        "query": query,
        "variables": {
            "auctionId": lot_id
        }
    }

    response = requests.post(graphql_url, json=payload)
    if response.status_code == 200:
        result = response.json()
        if get_time_left:
            lot = result["data"]["liveCatalogLots"]["liveLots"]
            min_time = min([i["lotState"]["timeLeftSeconds"] for i in lot if i["lotState"]["timeLeftSeconds"] > 0 ])
            return int(min_time)
        return result
    else:
        print("Error:", response.status_code)
        return None

def track_and_update_data(lot_id, file_name, sleep_time=60):
    num_tries = 0
    file_path = "auctions/" + file_name
    
    # If the file already exists, load its content
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            d = json.load(f)
    else:
        d = {
            "auction" : {},
            "lots":[]
        }

    while True:
        data = get_lots_from_live_auction(lot_id)
        if data:
            d["auction"] = data["data"]["liveCatalogLots"]["auction"]
            live_lots = data["data"]["liveCatalogLots"]["liveLots"]
            for lot in live_lots:
                if lot['itemId'] not in [i['itemId'] for i in d["lots"]]:
                    d["lots"].append(lot)
        elif num_tries > 5:
            break
        else:
            num_tries += 1
            print(f"Number of tries: {num_tries}")
            

        # save to json file
        try:
            with open(file_path, "w") as f:
                json.dump(d, f, indent=4, sort_keys=True)
        except Exception as e:
            print(f"Error saving to file: {e}")
        
        countdown(60)



def get_scheduled_auctions(auctioneer_id, closest_auction_only=True):
  
  graphql_url = "https://hibid.com/graphql" 
  query = """query AuctionsByAuctioneerSearch($auctioneerId: Int, $status: AuctionLotStatus = null, $pageNumber: Int, $pageLength: Int) {
  auctionSearch(
    input: {auctioneerId: $auctioneerId, status: $status}
    pageNumber: $pageNumber
    pageLength: $pageLength
  ) {
    pagedResults {
      pageLength
      pageNumber
      totalCount
      filteredCount
      results {
        matchinglotcount
        matchingCategoryCounts {
          category
          count
          featuredPicture {
            fullSizeLocation
            thumbnailLocation
            description
            width
            height
            __typename
          }
          __typename
        }
        auction {
          ...AuctionHeader
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  }

  fragment AuctionHeader on Auction {
  id
  altBiddingUrl
  altBiddingUrlCaption
  auctioneer {
    id
    name
    missingThumbnail
    __typename
  }
  auctionOptions {
    bidding
    altBidding
    catalog
    liveCatalog
    shippingType
    preview
    registration
    webcast
    useLotNumber
    useSaleOrder
    __typename
  }
  auctionState {
    auctionStatus
    isRegistered
    openLotCount
    timeToOpen
    __typename
  }
  description
  eventName
  eventAddress
  eventCity
  eventState
  eventZip
  eventDateBegin
  eventDateEnd
  eventDateInfo
  bidType
  biddingNotice
  auctionNotice
  links {
    description
    id
    type
    url
    videoId
    __typename
  }
  lotCount
  showBuyerPremium
  sourceType
  featuredPicture {
    description
    fullSizeLocation
    height
    thumbnailLocation
    width
    __typename
  }
  __typename
  }"""

  payload = {
    "operationName": "AuctionsByAuctioneerSearch",
    "query": query,
    "variables": {
      "auctioneerId": auctioneer_id,
      "pageLength": 25,
      "pageNumber": 1,
      "status": "OPEN"
    }
  }

  response = requests.post(graphql_url, json=payload)
  if response.status_code == 200:
    result = response.json()
    if closest_auction_only:
      auc_id = result["data"]["auctionSearch"]["pagedResults"]["results"][0]["auction"]["id"]
      aucioneer_name = result["data"]["auctionSearch"]["pagedResults"]["results"][0]["auction"]["auctioneer"]["name"]
      return auc_id, aucioneer_name
    else:
      return result
  else:
    print("Error:", response.status_code)
    return None
  


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 1:
        aucioneer_id = int(args[0])
        while True:
            try:
                auc_id, aucioneer_name = get_scheduled_auctions(aucioneer_id, closest_auction_only=True)
                aucioneer_name = aucioneer_name.replace(" ", "_")
                time_to_auction = get_lots_from_live_auction(auc_id, get_time_left=True)
                file_name = f"{aucioneer_name}_{auc_id}.json"
                print(f"Tracking auction {auc_id} from {aucioneer_name} in:")
                countdown(int(time_to_auction) - 60 if time_to_auction > 60 else time_to_auction)
                track_and_update_data(auc_id, file_name, sleep_time=60)
            except Exception as e:
                print(e)
                time.sleep(60)


