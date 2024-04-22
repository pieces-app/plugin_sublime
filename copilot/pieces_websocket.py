import json
import asyncio
import pieces_os_client as pos_client
import websockets
from pieces import config 
import threading
import asyncio

TIMEOUT = 10 # Seconds

class WebSocketManager:
    def __init__(self):
        self.ws = None
        self.is_connected = False
        self.response_received = None
        self.model_id = ""
        self.query = ""
        self.loading = False
        self.final_answer = ""
        self.conversation = None

        # Create a new event loop
        self.loop = asyncio.new_event_loop()

        # Run the event loop in a new thread
        self.thread = threading.Thread(target=self.start_event_loop, args=(self.loop,))
        self.thread.start()

        # Schedule the creation of the Queue and the open_websocket coroutine to run on the new event loop
        asyncio.run_coroutine_threadsafe(self.setup(), self.loop)

    async def setup(self):
        self.message_queue = asyncio.Queue()
        await self.open_websocket()

    def start_event_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def open_websocket(self):
        """Opens a websocket connection"""
        self.ws = await websockets.connect(config.WEBSOCKET_URL)
        self.is_connected = True
        await self._start_ws()

    async def on_message(self, message):
        """Handle incoming websocket messages."""
        try:
            response = pos_client.QGPTStreamOutput.from_json(message)
            if response.question:
                answers = response.question.answers.iterable
                for answer in answers:
                    text = answer.text
                    if text:
                        self.final_answer += text
                        await self.message_queue.put(text)
                        #print(text, end='')

            if response.status == 'COMPLETED':
                self.conversation = response.conversation
                self.loading = False   # signal that the conversation is complete

        except Exception as e:
            print(f"Error processing message: {e}")

    async def _start_ws(self):
        """Start a new websocket connection."""
        try:
            async for message in self.ws:
                await self.on_message(message)
        except websockets.exceptions.ConnectionClosed:
            self.is_connected = False

    async def send_message(self):
        """Send a message over the websocket."""
        message = {
            "question": {
                "query": self.query,
                "relevant": {"iterable": []},
                "model": self.model_id
            },
            "conversation": self.conversation
        }
        json_message = json.dumps(message)

        if self.is_connected:
            try:
                await self.ws.send(json_message)
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Error sending message: {e}")
                self.is_connected = False
                await self.open_websocket()
                await self.send_message()

    async def close_websocket_connection(self):
        """Close the websocket connection."""
        if self.ws and self.is_connected:
            await self.ws.close()
            self.is_connected = False

    async def message_generator(self, model_id, query):
        """
        Stream messages from on message.
        This function is a generator that yields messages as they become available.
        """
        if self.loading:
            raise RuntimeError("Running already")
        # Set loading to True and initialize model_id and query
        self.loading = True
        self.model_id = model_id
        self.query = query
        self.final_answer = ''
        
        # Send the initial message
        await self.send_message()
        
        # While loading is True, try to get messages from the queue
        while self.loading:
            try:
                # If a message is available, yield it
                yield self.message_queue.get_nowait()

            except asyncio.QueueEmpty:
                # If the queue is empty, wait for a short period before trying again
                await asyncio.sleep(0.1)

        # Once loading is False, drain any remaining messages from the queue
        while not self.message_queue.empty():
            try:
                # If a message is available, yield it
                yield self.message_queue.get_nowait()
            except asyncio.QueueEmpty:
                # If the queue is empty, break the loop
                break

                