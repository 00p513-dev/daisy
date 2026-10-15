import requests

BASE_URL = "http://84.8.144.158:8080"

async def train_command(ctx, *args):
    try:
        origin = args[0].upper()
    except:
        await ctx.send("Please specify a departure station")
        return
    
    try:
        destination = args[1].upper()
    except:
        await ctx.send("Please specify a destination station")
        return

    try:
        mode = args[2].upper()
        if mode == "-V":
            mode = "V"
        elif mode != "V":
            mode = "N"
    except:
        mode = "N"
    
    try:
        departures = requests.get(f"{BASE_URL}/api/departures", params={"crs": origin, "window": 180}).json()['services']
        arrivals = requests.get(f"{BASE_URL}/api/arrivals", params={"crs": destination, "window": 480}).json()['services']
    except:
        await ctx.send("Something went wrong, you probably have requested a non-existent station")
        return

    # Keep departures that also arrive at the destination later (same UID on both boards)
    arrival_times = {s['uid']: s['scheduledArrival'] or s['scheduledTime'] for s in arrivals}
    services = []
    for s in departures:
        dep = s['scheduledDeparture'] or s['scheduledTime']
        arr = arrival_times.get(s['uid'])
        if arr and (int(arr[:2]) * 60 + int(arr[3:]) - int(dep[:2]) * 60 - int(dep[3:])) % 1440 < 720:
            services.append(s)

    if not services:
        await ctx.send("No trains available.")
        return

    reply_text = ""

    for service in services[:5]:
        time = service['scheduledDeparture'] or service['scheduledTime']
        operator = service['atocCode']
        dest = service['destName'] or service['destCrs']

        if service['isCancelled']:
            real_time = "Canc"
        else:
            real_time = service['actualTime'] or time

        platform = "Plt " + service['platform'] if service['platform'] else "Plt -"

        if len(platform) == 5:
            platform += " "

        if mode == "V":
            platform += " (conf)" if service['platformConfirmed'] else " (ind)"

        if mode == "V":
            length = 13
        else:
            length = 5
        
        for i in range(length - len(platform)):
            platform += " "

        if mode == "N":
            reply_text += f"`{time} {platform} {dest}`\n"
        if mode == "V":
            reply_text += f"`{time} ({real_time}) {platform} [{operator}] {dest}`\n"

    await ctx.send(reply_text)
