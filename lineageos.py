import requests

LINEAGEOS_ENDPOINT = 'https://download.lineageos.org/api/v2/'

async def codename_command(ctx, *args):
    message_args = ctx.message.content.split(' ')

    try:
        codename = args[0]
    except:
        await ctx.send("Please specify a codename.")
        return

    response = requests.get(LINEAGEOS_ENDPOINT + f'devices/{codename}')

    if response.status_code == 404:
        await ctx.send(f"The device with codename '{codename}' is not supported by LineageOS.")
        return

    data = response.json()
    device_name = data['name']
    device_oem = data['oem']

    await ctx.send(f"{device_oem} {device_name}")