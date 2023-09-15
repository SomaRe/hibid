AuctionsByAuctioneerSearch = """query AuctionsByAuctioneerSearch($auctioneerId: Int, $status: AuctionLotStatus = null, $pageNumber: Int, $pageLength: Int) {
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

LiveCatalogLots = """
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
    
