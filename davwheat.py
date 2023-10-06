import requests

async def crs_command(ctx, *args):
    """Looks up a CRS code for a requested train station using David Wheatley's API"""

    search_term = ' '.join(args)

    url = f"https://national-rail-api.davwheat.dev/crs/{search_term}"

    response = requests.get(url)

    if response.status_code != 200:
        await ctx.send(f"The request failed: \n{response.text}")
        return

    data = response.json()

    if len(data) == 0:
        await ctx.send("No stations found.")
        return

    # If we made it this far chances are there are some stations to be found :)
    reply_text = ""

    for station in data:
        reply_text += f"\n`{station['crsCode']}: {station['stationName']}`"

    await ctx.send(reply_text)
