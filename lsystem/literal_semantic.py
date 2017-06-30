class RotateTerminal:

    def __init__(self, rotation = None):
        if rotation is None:
            rotation = 90
        self.rotation = rotation


class MoveTerminal:

    def __init__(self, distance = None):
        if distance is None:
            distance = 1
        self.distance = distance


class PushTerminal:
    pass


class PopTerminal:
    pass


class NonTerminal:

    def __init__(self):
        self.transition = []
        self.final_transition = []

    def append_trans(self, trans):
        assert trans is RotateTerminal \
            or trans is MoveTerminal \
            or trans is PushTerminal \
            or trans is PopTerminal \
            or trans is NonTerminal
        self.transition.append(trans)

    def append_final_trans(self, trans):
        assert trans is RotateTerminal \
            or trans is MoveTerminal \
            or trans is PushTerminal \
            or trans is PopTerminal
        self.final_transition.append(trans)

    def iterate(self, level: int):
        if level < 0:
            raise ValueError("Level cannot be below 0")

        if level == 0:
            return self.final_transition

        if level > 0:
            for literal in self.transition:
                if literal is NonTerminal:
                    for l2literal in literal.iterate(level -1):
                        yield l2literal
                else:
                    yield literal 
            return