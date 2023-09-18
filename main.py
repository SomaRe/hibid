from graphql_queries import AuctionsByAuctioneerSearch, LiveCatalogLots, GetLotDetails
import requests
import logging
import logging
import time
import json
import sys
import os

logging.basicConfig(filename='app.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_lot_description(lot_id):
    """
    Retrieves the description of a lot from a live auction using GraphQL.

    Args:
        lot_id (str or int): The ID of the auction lot to retrieve description for.

    Returns:
        str or "Error fetching lot description.": The description of the lot if the request was successful.

    """
    graphql_url = "https://hibid.com/graphql"

    query = GetLotDetails
    payload = {
        "operationName": "GetLotDetails",
        "query": query,
        "variables": {
            "lotId": lot_id
        }
    }

    response = requests.post(graphql_url, json=payload)

    if response.status_code == 200:
        result = response.json()
        description = result["data"]["lot"]["lot"]["description"]
        return description
    else:
        # Print an error message and return None in case of an error
        logging.error(f"Error fetching lot description. Status code: {response.status_code}")
        return "Error fetching lot description."


def countdown(total_seconds):

    """
    Countdown timer that displays the remaining time in days, hours, minutes, and seconds.

    Args:
        total_seconds (int): The total number of seconds for the countdown timer.

    Returns:
        None
    """
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
    # Clear the timer display line
    print(" " * len(time_remaining), end="\r")


def get_lots_from_live_auction(lot_id, get_time_left=False):

    """
    Retrieves lots from a live auction using GraphQL.

    Args:
        lot_id (str): The ID of the auction to retrieve lots from.
        get_time_left (bool, optional): Whether to fetch and return the minimum time left for lots. Default is False.

    Returns:
        dict or int or None: If `get_time_left` is False, returns the GraphQL response as a dictionary.
        If `get_time_left` is True, returns the minimum time left in seconds as an integer.
        Returns None if there was an error in the request.

    """
    graphql_url = "https://hibid.com/graphql"

    query = LiveCatalogLots
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
            # Extract the relevant data from the GraphQL response
            lot = result["data"]["liveCatalogLots"]["liveLots"]
            # Find the minimum time left among lots that have positive time left
            min_time = min([i["lotState"]["timeLeftSeconds"] for i in lot if i["lotState"]["timeLeftSeconds"] > 0])
            return int(min_time)

        # print open lots
        open_lots = result["data"]["liveCatalogLots"]["auction"]["auctionState"]["openLotCount"]
        print(f"Open lots: {open_lots}")
        # Return the entire GraphQL response
        return result
    else:
        # Print an error message and return None in case of an error
        logging.error(f"Error fetching lots from live auction. Status code: {response.status_code}")
        return None


def get_scheduled_auctions(auctioneer_id, closest_auction_only=True):
    """
    Retrieves scheduled auctions for a given auctioneer using GraphQL.

    Args:
        auctioneer_id (str): The ID of the auctioneer to retrieve auctions for.
        closest_auction_only (bool, optional): Whether to return information about the closest auction only.
            If True, returns a tuple containing the ID and name of the closest auctioneer.
            If False, returns the entire GraphQL response. Default is True.

    Returns:
        tuple or dict or None: If `closest_auction_only` is True, returns a tuple (auc_id, auctioneer_name).
        If `closest_auction_only` is False, returns the GraphQL response as a dictionary.
        Returns None if there was an error in the request.

    """
    graphql_url = "https://hibid.com/graphql"

    # Replace "<>" with your actual GraphQL query
    query = AuctionsByAuctioneerSearch
    
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
    """
    Retrieves scheduled auctions for a given auctioneer using GraphQL.

    Args:
        auctioneer_id (str): The ID of the auctioneer to retrieve auctions for.
        closest_auction_only (bool, optional): Whether to return information about the closest auction only.
            If True, returns a tuple containing the ID and name of the closest auctioneer.
            If False, returns the entire GraphQL response. Default is True.

    Returns:
        tuple or dict or None: If `closest_auction_only` is True, returns a tuple (auc_id, auctioneer_name).
        If `closest_auction_only` is False, returns the GraphQL response as a dictionary.
        Returns None if there was an error in the request.

    """
    graphql_url = "https://hibid.com/graphql"

    # Replace "<>" with your actual GraphQL query
    query = AuctionsByAuctioneerSearch
    
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
            # Extract information about the closest auction
            closest_auction = result["data"]["auctionSearch"]["pagedResults"]["results"][0]["auction"]
            auc_id = closest_auction["id"]
            auctioneer_name = closest_auction["auctioneer"]["name"]
            return auc_id, auctioneer_name
        else:
            # Return the entire GraphQL response
            return result
    else:
        # Print an error message and return None in case of an error
        logging.error(f"Error fetching scheduled auctions. Status code: {response.status_code}")
        return None
    response = requests.post(graphql_url, json=payload)

    if response.status_code == 200:
        result = response.json()

        if closest_auction_only:
            # Extract information about the closest auction
            closest_auction = result["data"]["auctionSearch"]["pagedResults"]["results"][0]["auction"]
            auc_id = closest_auction["id"]
            auctioneer_name = closest_auction["auctioneer"]["name"]
            return auc_id, auctioneer_name
        else:
            # Return the entire GraphQL response
            return result
    else:
        # Print an error message and return None in case of an error
        logging.error(f"Error fetching scheduled auctions. Status code: {response.status_code}")
        return None
  

def update_auction_data(lot_id, auction_data, item_ids):
    """
    Updates the provided auction data based on live lots fetched from a live auction.
    
    Args:
        lot_id (str or int): The ID of the auction lot to fetch data for.
        auction_data (dict): The existing auction data to be updated. Should have keys "auction" and "lots".
        item_ids (set): A set containing the IDs of items already recorded in auction_data. This set will be updated with new item IDs if they are found.
    
    Returns:
        bool: True if live auction data was successfully fetched and processed, False otherwise.
    
    Notes:
        - The function fetches the live auction data using the `get_lots_from_live_auction` function.
        - New lots are added to the auction_data's "lots" dictionary and their IDs are added to the item_ids set.
        - For lots already present in auction_data, their high bid information is updated if it has changed.
        - If there's a new high bid for a lot, a message will be printed to the console.
    """
    data = get_lots_from_live_auction(lot_id)
    
    if not data:
        return False

    auction_data["auction"] = data["data"]["liveCatalogLots"]["auction"]
    live_lots = data["data"]["liveCatalogLots"]["liveLots"]

    for lot in live_lots:
        lot_id = lot["itemId"]
        if lot_id not in item_ids:
            auction_data["lots"][lot_id] = lot
            item_ids.add(lot_id)
        else:
            stored_lot = auction_data["lots"][lot_id]
            if stored_lot["lotState"]["highBid"] != lot["lotState"]["highBid"]:
                stored_lot["lotState"] = lot["lotState"]
                logging.info(f"Lot {lot_id} has a new high bid: {lot['lotState']['highBid']}")

    return True


def track_and_update_data(lot_id, file_name, sleep_time=60, max_retries=3):
    """
    Continuously tracks and updates auction data, saving to a JSON file.
    
    Args:
        lot_id (str or int): ID of the auction lot to track and fetch data for.
        file_name (str): Name of the file to which the auction data will be saved.
        sleep_time (int, optional): Time interval (in seconds) between successive data fetches. Defaults to 60 seconds.
        max_retries (int, optional): Maximum number of consecutive failed data fetch attempts before stopping. Defaults to 3.

    Notes:
        - The function fetches live auction data using the `update_auction_data` function.
        - If data fetching fails, the function will retry up to max_retries times before stopping.
        - After each data update, the function will pause for the duration specified by sleep_time.
        - The function logs any errors encountered during data fetching or file saving.
    """
    num_tries = 0
    file_path = os.path.join("auctions", file_name)

    # Load existing data if file exists, else initialize
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            auction_data = json.load(f)
    else:
        auction_data = {
            "auction": {},
            "lots": {}
        }

    while True:
        item_ids = set(auction_data["lots"].keys())
        try:
            success = update_auction_data(lot_id, auction_data, item_ids)
            if not success:
                num_tries += 1
                logging.warning(f"Failed to fetch data. Retry {num_tries} of {max_retries}")
                if num_tries > max_retries:
                    break
        except Exception as e:
            logging.error(f"Error fetching data: {e}")

        # Save to json file
        try:
            with open(file_path, "w") as f:
                json.dump(auction_data, f, indent=4, sort_keys=True)
        except Exception as e:
            logging.error(f"Error saving to file: {e}")
        
        countdown(sleep_time)


def main(auctioneer_id):
    """
    Main entry point for the auction tracking application. Continuously tracks scheduled auctions based on an auctioneer ID.
    
    Args:
        auctioneer_id (str or int): ID of the auctioneer whose auctions are to be tracked.
    
    Notes:
        - Uses the `get_scheduled_auctions` function to fetch details of the next scheduled auction.
        - Waits until the start of the auction, then begins tracking and updating data using `track_and_update_data`.
        - If any errors are encountered, logs the error and pauses for 60 seconds before retrying.
    """
    while True:
        try:
            auc_id, auctioneer_name = get_scheduled_auctions(auctioneer_id, closest_auction_only=True)
            auctioneer_name = auctioneer_name.replace(" ", "_")
            time_to_auction = get_lots_from_live_auction(auc_id, get_time_left=True)
            file_name = f"{auctioneer_name}_{auc_id}.json"
            logging.info(f"Tracking auction {auc_id} from {auctioneer_name} in:")
            countdown(int(time_to_auction) - 60 if time_to_auction > 60 else time_to_auction)
            track_and_update_data(auc_id, file_name, sleep_time=60)
        except Exception as e:
            logging.error(e)
            time.sleep(60)
 

  
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        logging.error("Usage: python script_name.py <auctioneer_id>")
        sys.exit(1)

    try:
        auctioneer_id = int(args[0])
        main(auctioneer_id)
    except ValueError:
        logging.error("Please provide a valid integer for the auctioneer_id.")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting...")
        sys.exit(0)


