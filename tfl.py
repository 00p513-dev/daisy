from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import daisySecrets

import requests


async def tflbus_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the status of a TfL bus route."""

    try:
        message_args = update.message.text.split(' ')
        route_number = message_args[1]

        # TfL API endpoint for getting the status of a bus route
        bus_route_status_url = f'https://api.tfl.gov.uk/Line/{route_number}/Status'

        # Make a request to the TfL API to get the status of the bus route
        response = requests.get(bus_route_status_url)

        # Check if the request was successful
        if response.status_code == requests.codes.ok:
            # Parse the response as JSON
            bus_route_status = response.json()
            # Get the status severity description of the bus route
            bus_line_status = bus_route_status[0]['lineStatuses'][0]
            status = bus_line_status['statusSeverityDescription']
            if 'reason' in bus_line_status:
                status = status + " - " + bus_line_status['reason']
            # Return the status of the bus route
            await update.message.reply_text(status)
        else:
            # Return an error message if the request was not successful
            await update.message.reply_text(f"Error retrieving bus route status: {response.status_code}")
    except Exception as e:
        print(e)
        await update.message.reply_text("Oh n-nyo t-that d-didn't wowk! Sowwy Wowwy")


async def tflstatus_command(update: Update, context: ContextTypes.DEFAULT_TYPE, mode="tfl") -> None:
    """Send the status of transit using TfL APIs."""

    # TfL line to get the status for
    message_args = update.message.text.split(' ')
    if (len(message_args) == 1) or (message_args[1] == "nr"):
        if message_args[1] == "nr":
            all_lines_status_url = 'https://api.tfl.gov.uk/line/mode/overground,elizabeth-line,national-rail/status'
        else:
            all_lines_status_url = 'https://api.tfl.gov.uk/line/mode/tube,overground,elizabeth-line,dlr,tram/status'

        # Make a request to the TfL API to get the status of all lines
        response = requests.get(all_lines_status_url)

        # Check if the request was successful
        if response.status_code == requests.codes.ok:
            # Parse the response as JSON
            all_lines_status = response.json()
            # Iterate over each line and display the current status
            if message_args[1] == "nr":
                status_output = "<b>Current status on all National Rail services</b>"
            else:
                status_output = "<b>Current status on all TfL services</b>"

            for line in all_lines_status:
                disruptions = line['lineStatuses']
                if disruptions:
                    if line['name'] == "Tram":
                        line['name'] = "Trams"

                    status = disruptions[0]['statusSeverityDescription']
                    status_output += "\n" + line['name'] + ": " + status

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

            isTube = not (response.json()[0]["modeName"] == "national-rail" or
                          response.json()[0]["modeName"] == "elizabeth-line" or
                          response.json()[0]["modeName"] == "overground")

            if isTube or (response.json()[0]["modeName"] == "elizabeth-line"):  # Thanks Boris for this terrible name
                replyText += "the "

            replyText += response.json()[0]['name']

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
