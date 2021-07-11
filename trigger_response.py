# import json
import re
import random
from datetime import datetime as dt, timedelta as td, timezone as tz
from database import db
from on_message_commands import OnMessageCommands


class TriggerResponse(OnMessageCommands):
    """If a message contains a trigger then reply with a randomly selected
    response for that trigger."""

    _triggers = []
    _cache = {}

    @classmethod
    def init(cls):
        # Load triggers from database.
        for trigger, responses in db.get_triggers().items():
            cls._triggers.append(Trigger(trigger, responses))

    @classmethod
    def exec_check(cls, message) -> bool:
        for t in cls._triggers:
            if t.match(message):
                cls._cache[message] = t
                return True
        return False

    @classmethod
    async def respond(cls, message):
        cls.on_call(message)

        # Prevent triggers from recalculating unless necessary.
        if message in cls._cache:
            print(cls._cache[message].rpn)

            await cls._cache[message].respond(message)
            del cls._cache[message]
            return

        for t in cls._triggers:
            if t.match(message):
                print(t.rpn)
                await t.respond(message)


class Trigger():
    """Represents a trigger."""

    # match "ok" and sender UID and random 10 and (channel ID or channel ID2)
    # "ok" match UID sender 10 random ID channel ID2 channel or and and and

    responses = []

    _substitution_map = {
        'sender_ping': lambda x: x.author.mention,
        'time': lambda *x: dt.now(tz(td(
                   hours=int(x[1]) if len(x) > 1 else None
               ))).strftime('%I:%M %p, %Z' if len(x) < 3 else x[2]),
        'sender_name': lambda x: x.author.name
    }

    def __init__(self, rpn: str, responses) -> None:
        self.rpn = rpn
        self.selector_root = self._root_from_rpn(rpn)
        self.responses = responses

    def _root_from_rpn(self, rpn):
        """Generate binary tree root from rpn expression."""

        selectors = {
            'match': Match,
            'sender': Sender,
            'random': Random,
            'and': And,
            'or': Or
        }

        stack = []
        for term in rpn.split('~'):
            if term not in selectors.keys():
                stack.append(term)
            else:
                args = []
                for i in range(selectors[term].num_args):
                    args.append(stack.pop())
                stack.append(selectors[term](*args))

        if len(stack) != 1 or not issubclass(type(stack[0]), Selector):
            raise InvalidRpnError

        return stack[0]

    def match(self, message) -> bool:
        return self.selector_root.execute(message)

    async def respond(self, message):
        weighted = []
        for r in self.responses:
            for i in range(r['bias']):
                weighted.append(r)

        response = random.choice(weighted)

        subbed = response['response']
        for s in re.findall(r'(?<=<<).+?(?=>>)', subbed):
            t = s.strip().split()
            if t[0] in self._substitution_map.keys():
                if len(t) == 1:
                    subbed = self._substitution_map[t[0]](message).join(
                        subbed.split('<<'+s+'>>')
                    )

                else:
                    subbed = (self._substitution_map[t[0]](message, *t[1:])
                              .join(subbed.split('<<'+s+'>>')))

        await message.channel.send(
            subbed, reference=message if response['as_reply'] else None
        )


class Selector:
    """Base class for selectors."""

    num_args = 0
    _args = []

    def __init__(self, *args) -> None:
        self._args = args

    def _get_arg(self, index, message=''):
        a = self._args[index]
        return a.execute(message) if issubclass(type(a), Selector) else a

    def execute(self, message) -> bool:
        raise NotImplementedError


class Match(Selector):
    """Matches regex."""

    num_args = 1

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.pattern = re.compile(args[0])

    def execute(self, message) -> bool:
        return bool(self.pattern.match(message.content.lower()))


class Sender(Selector):
    """Checks who the sender of a message is."""

    num_args = 1

    def execute(self, message) -> bool:
        return message.author.id == int(self._get_arg(0))


class Random(Selector):
    """Random chance."""

    num_args = 1

    def execute(self, message) -> bool:
        return random.randrange(int(self._get_arg(0))) == 0


class And(Selector):
    """Boolean 'and'."""

    num_args = 2

    def execute(self, message) -> bool:
        return self._get_arg(0, message) and self._get_arg(1, message)


class Or(Selector):
    """Boolean 'or'."""
    num_args = 2

    def execute(self, message) -> bool:
        return self._get_arg(0, message) or self._get_arg(1, message)


class InvalidRpnError(Exception):
    """Provided rpn string is invalid."""
