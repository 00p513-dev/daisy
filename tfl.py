import requests
import datetime
import time

# Define the command to get TfL status
async def tflstatus_command(ctx, mode="tfl"):
    message_args = ctx.message.content.split(' ')
    if (len(message_args) == 1) or (message_args[1] == "nr") or (message_args[1] == "mainline") or (message_args[1] == "trains"):
        try:
            if message_args[1] == "nr":
                service = "nr"
                all_lines_status_url = 'https://api.tfl.gov.uk/line/mode/overground,elizabeth-line,national-rail/status'
        except:
            service = "tfl"
            all_lines_status_url = 'https://api.tfl.gov.uk/line/mode/tube,overground,elizabeth-line,dlr,tram/status'

        response = requests.get(all_lines_status_url)

        if response.status_code == requests.codes.ok:
            all_lines_status = response.json()

            if service == "nr":
                status_output = "Current status on all National Rail services"
            else:
                status_output = "Current status on all TfL services"

            for line in all_lines_status:
                disruptions = line['lineStatuses']
                if disruptions:
                    lineName = fixLineName(line['name'])

                    status = disruptions[0]['statusSeverityDescription']
                    status_output += "\n" + lineName + ": " + status

            await ctx.send(status_output)
        else:
            await ctx.send(f"Error retrieving line status: {response.status_code}")

    else:
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

        response = requests.get(line_status_url.format(line=line_id))

        if response.status_code == requests.codes.ok:
            line_status = response.json()[0]['lineStatuses'][0]
            line_status_summary = line_status['statusSeverityDescription']

            replyText = "Currently "

            isTube = (response.json()[0]["modeName"] == "tube")

            if isTube or response.json()[0]["modeName"] == "elizabeth-line" or response.json()[0]["modeName"] == "tram" or response.json()[0]["modeName"] == "dlr":
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

            await ctx.send(replyText)
        else:
            await ctx.send(f"Error retrieving line status: {response.status_code}")

# Helper function to fix line names
def fixLineName(name):
    if name == "Tram":
        name = "Trams"

    return name

# Define the command to get TFL bus times
async def tflbus_command(ctx):
    message_args = ctx.message.content.split(' ')

    try:
        stop_code = int(message_args[1])
    except:
        await ctx.send("Failed to read stop code")
        return
    
    try:
        mode = message_args[2]
        mode = mode.lower()
        if mode == "-v" or mode == "v":
            mode = "v"
    except:
        mode = "n"

    base_url = 'https://api.tfl.gov.uk'
    search_url = f'{base_url}/StopPoint/Search?query={stop_code}'

    response = requests.get(search_url)

    if response.status_code == 200:
        stop_points = response.json()
        
        if len(stop_points) > 0:
            stop_point = stop_points['matches'][0]
            naptan_id = stop_point['id']
            stoppoint_url = f'{base_url}/StopPoint/{naptan_id}/Arrivals'
            response = requests.get(stoppoint_url)

            if response.status_code == 200:
                bus_times = response.json()
                
                if len(bus_times) == 0:
                    await ctx.send(f"No bus times available for {stop_point['name']}")
                    return
                
                replyText = f"Next buses for {stop_point['name']}"
                try:
                    replyText += f" Stop {stop_point['stopLetter']} \n"
                except:
                    replyText += "\n"

                sortedBus = {}

                for bus in bus_times:
                    bus_id = bus['vehicleId']
                    destination = bus['destinationName']
                    line = bus['lineName']
                    try:
                        expected_arrival = int(time.strftime('%M', time.gmtime(bus['timeToStation'])))     
                    except:
                        try:
                            arrival_time = datetime.fromisoformat(bus['expectedArrival'])
                            current_time = datetime.utcnow()
                            expected_arrival = int((arrival_time - current_time).total_seconds() / 60)
                        except:
                            expected_arrival = 0
                    
                    sortedBus[bus_id] = {"arrival": expected_arrival, "destination": destination, "line": line}
                
                sortedBus = dict(sorted(sortedBus.items(), key=lambda item: item[1]["arrival"]))

                for bus in sortedBus:
                    if mode == "v":
                        replyText += f"{sortedBus[bus]['arrival']} minutes {sortedBus[bus]['line']} {sortedBus[bus]['destination']} ({bus})\n"
                    else:
                        replyText += f"{sortedBus[bus]['arrival']} minutes {sortedBus[bus]['line']} {sortedBus[bus]['destination']}\n"
                await ctx.send(replyText)
                return
            else:
                await ctx.send('Error occurred while retrieving bus times.')
                return
        else:
            await ctx.send('No stop point found for the specified stop code.')
            return
    else:
        await ctx.send('Error occurred while resolving the stop code to Naptan ID.')
        return
