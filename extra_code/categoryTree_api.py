import requests
import json

url = "https://hibid.com/graphql"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "site_subdomain": "hibid.com"
}

# Replace with your actual GraphQL query
graphql_query = """
query CategorySearch($auctionId: Int = null, $category: CategoryId = null, $searchText: String = null, $hideGoogle: Boolean = false, $zip: String = null, $miles: Int = null, $status: AuctionLotStatus = null, $filter: AuctionLotFilter = null, $isArchive: Boolean = false, $dateStart: DateTime, $dateEnd: DateTime, $returnEmptyCategories: Boolean = false) {
  categoryTree(
    input: {auctionId: $auctionId, category: $category, searchText: $searchText, hideGoogle: $hideGoogle, zip: $zip, miles: $miles, status: $status, filter: $filter, isArchive: $isArchive, dateStart: $dateStart, dateEnd: $dateEnd, returnEmptyCategories: $returnEmptyCategories}
  ) {
    id
    parentCategoryId
    baseCategoryId
    categoryName
    fullCategory
    hasChildren
    lotCount
    description
    uRLPath
    children {
      id
      parentCategoryId
      categoryName
      fullCategory
      hasChildren
      lotCount
      description
      uRLPath
      children {
        id
        parentCategoryId
        categoryName
        fullCategory
        hasChildren
        lotCount
        description
        uRLPath
        children {
          id
          parentCategoryId
          categoryName
          fullCategory
          hasChildren
          lotCount
          description
          uRLPath
          children {
            id
            parentCategoryId
            categoryName
            fullCategory
            hasChildren
            lotCount
            description
            uRLPath
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

data = {
    "operationName": "CategorySearch",
    "variables": {
        "auctionId": 478457,
        "category": None,
        "searchText": None,
        "hideGoogle": False,
        "zip": None,
        "miles": 50,
        "status": "OPEN",
        "filter": "ALL",
        "isArchive": False,
        "returnEmptyCategories": False,
        "dateStart": None,
        "dateEnd": None
    },
    "query": graphql_query
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    result_data = response.json()
    # save to json file
    with open('data.json', 'w') as outfile:
        json.dump(result_data, outfile)
    # Process the result_data as needed
else:
    print("Request failed with status code:", response.status_code)
    print("Response content:", response.content)
