from on_message_commands import OnMessageCommands


class Calculator(OnMessageCommands):
    """If message starts with '>calc', perform the operations and respond
    with the result."""
    _VALID_CHARS_LIST = []
    _OPERATIONS_LIST = []
    _PREFIX = ">calc "

    @classmethod
    def init(cls):
        cls._OPERATIONS_LIST = ["+", "-", "/", "*"]
        cls._VALID_CHARS_LIST = [str(num) for num in range(10)]
        cls._VALID_CHARS_LIST += cls._OPERATIONS_LIST
        cls._VALID_CHARS_LIST.append(".")

    @classmethod
    def exec_check(cls, message):
        if message.content.lower().startswith(cls._PREFIX):
            return True
        else:
            return False

    @classmethod
    def _calculate(cls, operation: str) -> float:
        op = ""
        for char in operation:
            if char in cls._OPERATIONS_LIST:
                op = char
                break
        numbers = list(map(float, operation.split(op)))

        if op == "+":
            return numbers[0] + numbers[1]
        elif op == "-":
            return numbers[0] - numbers[1]
        elif op == "*":
            return numbers[0] * numbers[1]
        elif op == "/":
            return numbers[0] / numbers[1]

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)

        operation = message.content.lower()[len(cls._PREFIX):]

        for char in operation:
            if char not in cls._VALID_CHARS_LIST:
                response = "I am not smart enough for your bullshit, "
                response += message.author.name
                await message.channel.send(response)
                return

        num_ops = 0

        for char in operation:
            if char in cls._OPERATIONS_LIST:
                num_ops += 1

        if num_ops > 1:
            await message.channel.send("That's too many operations.")
            return
        elif num_ops == 0:
            await message.channel.send("Nigga that's no math.")
            return

        try:
            response = f"The result is {cls._calculate(operation)}. "
            response += f"Was that too hard for you, {message.author.name}?"
        except ZeroDivisionError:
            await message.channel.send("Stop trying to crash me you fuckturd.")
            return

        await message.channel.send(response)
