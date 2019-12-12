starter_variations = ["i am ", "i'm ", "im ", "i m "]


def prepare_response(text):
    text = text.lower()

    for starter in starter_variations:
        if text.startswith(starter):
            response = text[len(starter):]  # Anything after starter to end.
            response = "Hi, " + response
            return response

    return None


async def dadbot(message):
    response = prepare_response(message.content)

    if response is not None:
        await message.channel.send(response)
