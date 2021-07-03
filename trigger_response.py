import re
from on_message_commands import OnMessageCommands
from random import randrange


class TriggerResponse(OnMessageCommands):
    @classmethod
    def init(cls):
        pass

    @classmethod
    def exec_check(cls, message) -> bool:
        return True

    @classmethod
    def respond(cls, message):
        pass


class Trigger():
    # match "ok" and sender UID and random 10 and (channel ID or channel ID2)
    # "ok" match UID sender 10 random ID channel ID2 channel or and and and

    def __init__(self, rpn) -> None:
        self.rpn = rpn
        self.selector_root = self._root_from_rpn(rpn)

    def _root_from_rpn(self, rpn):
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


class Selector:
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
    num_args = 1

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.pattern = re.compile(args[0])

    def execute(self, message) -> bool:
        return bool(self.pattern.match(message.content))


class Sender(Selector):
    num_args = 1

    def execute(self, message) -> bool:
        return message.author.id == self._get_arg(0)


class Random(Selector):
    num_args = 1

    def execute(self, message) -> bool:
        return randrange(self._get_arg(0)) == 0


class And(Selector):
    num_args = 2

    def execute(self, message) -> bool:
        return self._get_arg(0, message) and self._get_arg(1, message)


class Or(Selector):
    num_args = 2

    def execute(self, message) -> bool:
        return self._get_arg(0, message) or self._get_arg(1, message)


class InvalidRpnError(Exception):
    """Provided rpn string is invalid."""
