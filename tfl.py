from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import daisySecrets

import datetime, requests, time

async def tflstatus_command(update: Update, context: ContextTypes.DEFAULT_TYPE, mode="tfl") -> None:
    """Send the status of transit using TfL APIs."""

    # TfL line to get the status for
    message_args = update.message.text.split(' ')
    if (len(message_args) == 1) or (message_args[1] == "nr"):
        try:
            if message_args[1] == "nr":
                service = "nr"
                all_lines_status_url = 'https://api.tfl.gov.uk/line/mode/overground,elizabeth-line,national-rail/status'
        except:
            service = "tfl"
            all_lines_status_url = 'https://api.tfl.gov.uk/line/mode/tube,overground,elizabeth-line,dlr,tram/status'

        # Make a request to the TfL API to get the status of all lines
        response = requests.get(all_lines_status_url)

        # Check if the request was successful
        if response.status_code == requests.codes.ok:
            # Parse the response as JSON
            all_lines_status = response.json()
            # Iterate over each line and display the current status
            if service == "nr":
                status_output = "<b>Current status on all National Rail services</b>"
            else:
                status_output = "<b>Current status on all TfL services</b>"

            for line in all_lines_status:
                disruptions = line['lineStatuses']
                if disruptions:
                    lineName = fixLineName(line['name'])

                    status = disruptions[0]['statusSeverityDescription']
                    status_output += "\n" + lineName + ": " + status

            await update.message.reply_html(f"{status_output}")
        else:
            await update.message.reply_text(f"Error retrieving line status: {response.status_code}")

    else:
        # TfL API endpoint for getting the line status
        line_status_url = 'https://api.tfl.gov.uk/line/{line}/status'
        line_id = message_args[1]

        if line_id == "overground":
            line_id = "london-overground"
        elif line_id == "gwr":
            line_id = "great-western-railway"
        elif line_id == "trams":
            line_id = "tram"
        elif line_id == "swr":
            line_id = "south-western-railway"

        # Make a request to the TfL API to get the line status
        response = requests.get(line_status_url.format(line=line_id))

        # Check if the request was successful
        if response.status_code == requests.codes.ok:
            # Parse the response as JSON
            line_status = response.json()[0]['lineStatuses'][0]
            line_status_summary = line_status['statusSeverityDescription']

            replyText = "Currently "

            isTube = (response.json()[0]["modeName"] == "tube")

            if isTube or response.json()[0]["modeName"] == "elizabeth-line" or response.json()[0]["modeName"] == "tram":  # Thanks Boris for this terrible name
                replyText += "the "

            lineName = fixLineName(response.json()[0]['name'])
            replyText += lineName

            if isTube:
                replyText += " line"
            
            if line_status_summary == "Good Service":
                replyText += " has a good service."
            elif line_status_summary == "Part Suspended":
                replyText += " is partially suspended."
            elif line_status_summary == "Part Closure":
                replyText += " is partially closed."
            elif line_status_summary == "Planned Closure":
                replyText += " is closed."
            else:
                replyText += f" has {line_status_summary}."

            if 'reason' in line_status:
                replyText = replyText + "\n\n" + line_status["reason"]

            await update.message.reply_text(replyText)
        else:
            await update.message.reply_text(f"Error retrieving line status: {response.status_code}")

def fixLineName(name):
    if name == "Tram":
        name = "Trams"

    return name

async def tflbus_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_args = update.message.text.split(' ')

    # Replace 'STOP_CODE' with the 5-digit bus stop code you want to retrieve data for
    try:
        stop_code = int(message_args[1])
    except:
        await update.message.reply_text("Failed to read stop code")
        return

    # Base URL for the TFL Unified API
    base_url = 'https://api.tfl.gov.uk'

    # Endpoint for the Search API to resolve the stop code to Naptan ID
    search_url = f'{base_url}/StopPoint/Search?query={stop_code}'

    # Make the API request to resolve the stop code to Naptan ID
    response = requests.get(search_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        stop_points = response.json()
        
        # Extract the first stop point (assuming exact match)
        if len(stop_points) > 0:
            stop_point = stop_points['matches'][0]
            naptan_id = stop_point['id']
            
            # Endpoint for the StopPoint API with the resolved Naptan ID
            stoppoint_url = f'{base_url}/StopPoint/{naptan_id}/Arrivals'
            
            # Make the API request to retrieve bus times
            response = requests.get(stoppoint_url)

            if response.status_code == 200:
                # Parse the JSON response
                bus_times = response.json()
                
                if len(bus_times) == 0:
                    await update.message.reply_text(f"No bus times available for {stop_point['name']}")
                    return
                
                replyText = f"Next buses for {stop_point['name']}"

                # Extract relevant information
                for bus in bus_times:
                    bus_id = bus['vehicleId']
                    destination = bus['destinationName']
                    line = bus['lineName']
                    try:
                        expected_arrival = time.strftime('%M', time.gmtime(bus['timeToStation']))
                        expected_arrival += " minutes"
                    except:
                        try:
                            arrival_time = datetime.fromisoformat(bus['expectedArrival'])
                            current_time = datetime.utcnow()
                            expected_arrival = (arrival_time - current_time).total_seconds() / 60
                        except:
                            expected_arrival = "unknown"
                    
                    replyText += f"\n{line} {destination}, Expected Arrival: {expected_arrival}"
                
                await update.message.reply_text(replyText)
                return
            else:
                await update.message.reply_text('Error occurred while retrieving bus times.')
                return
        else:
            await update.message.reply_text('No stop point found for the specified stop code.')
            return
    else:
        await update.message.reply_text('Error occurred while resolving the stop code to Naptan ID.')
        return
