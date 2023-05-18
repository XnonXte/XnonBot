import interactions

bot = interactions.Client()


@interactions.listen()
async def on_startup():
    print("Just a test!")

bot.start("MTEwMzM2MjUwNzA5NzI0Mzc0OQ.GnjNGa.oTwY_-MWdFFhFS0U1suYiQKbNMtyOsMhTUg9Hk")
