import requests

import daisySecrets

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
    
    url = f"https://api.rtt.io/api/v1/json/search/{origin}/to/{destination}"
    response = requests.get(url, auth=(daisySecrets.rttuser, daisySecrets.rttpass))
    data = response.json()

    try:
        services = data['services']
    except:
        await ctx.send("Something went wrong, you probably have requested a non-existent station")
        return

    if not services:
        await ctx.send("No trains available.")
        return

    reply_text = ""

    for service in services[:5]:
        time = service['locationDetail']['gbttBookedDeparture']
        operator = service['atocCode']
        dest = service['locationDetail']["destination"][0]['description']

        try:
            real_time = service['locationDetail']['realtimeDeparture']
        except:
            real_time = service['locationDetail']['gbttBookedDeparture']
        
        try:
            if service["serviceType"] == "train":
                platform = "Plt " + service['locationDetail']["platform"]

                if len(platform) == 5:
                    platform += " "
                
                if mode == "V":
                    try:
                        if service['locationDetail']["serviceLocation"] == "AT_PLAT":
                            platform += " (at)"
                        elif service['locationDetail']["serviceLocation"] == "APPR_PLAT":
                            platform += " (appr)"
                        elif service['locationDetail']["serviceLocation"] == "APPR_STAT":
                            platform += " (appr)"
                        elif service['locationDetail']["serviceLocation"] == "DEP_PREP":
                            platform += " (dep)"
                        elif service['locationDetail']["serviceLocation"] == "DEP_READY":
                            platform += " (dep)"
                        else:
                            platform += " (" + service['locationDetail']["serviceLocation"] + ")"
                    except:
                        if service['locationDetail']['platformConfirmed']:
                            platform += " (conf)"
                        else:
                            platform += " (ind)"

            elif service["serviceType"] == "bus":
                platform = "Bus"
            elif service["serviceType"] == "ship":
                platform = "Ship"
            else:
                platform = "Plt UNK"
        
        except:
            print('failed to find platform')
            platform = "Plt UNK"
        
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