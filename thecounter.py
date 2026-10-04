"""The Counter"""
import os, time

async def counter_command(ctx, *args):
    message_args = ctx.message.content.split(' ')

    try:
        with open("counter.txt", "r") as text_file:
            ts = text_file.read()
            print(ts)
            await ctx.send(f"Time since *The Counter* <t:{ts}:R>")
            return
    except:
        await ctx.send("Issue reading *The Counter*")
        return


async def resetcounter_command(ctx, *args):
    message_args = ctx.message.content.split(' ')

    ts = time.time()
    print(ts)

    ts = int(ts)
    print(ts)

    try:
        with open("counter.txt", "w") as text_file:
            text_file.write(str(ts))
        await ctx.send(f"# *The Counter* has been reset! \nTime since *The Counter* <t:{ts}:R>")
        return
    except:
        await ctx.send(f"*The Counter* reset failed")
        return