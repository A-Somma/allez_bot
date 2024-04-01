import asyncio
import os
import signal
import discord
from gpiozero import Button, LED

class AllezBot(discord.Client):

    def __init__(self, *args, **kwargs):
        super(AllezBot, self).__init__(*args, **kwargs)
        self.led = LED(17)
        self.on_button = Button(36)
        self.off_button = Button(32)
        self.off_button.when_pressed = self.stop_blink
        self.on_button.when_pressed = self.start_blink

    def start_blink(self):
        self.led.blink()

    def stop_blink(self):
        self.led.off()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Call for aide from {message.author}')
        if('Squad' in message):
            self.start_blink()

def exit_bot():
    print("\nStopping bot...")
    os._exit(0)

async def start_bot():
    signal.signal(signal.SIGINT, lambda s, f: asyncio.create_task(exit_bot()))
    client = AllezBot(command_prefix='_Squad', intents=discord.Intents.default())
    async with client:
        print("Starting bot...")
        await client.start(os.environ['ALLEZ_TOKEN'])

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
