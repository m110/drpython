
class Brick(object):
    """Single brick consists of two blocks."""

    def __init__(self, blocks):
        self._blocks = blocks

    def set_blocks(self, block_a, block_b):
        self._blocks = (block_a, block_b)

    @property
    def blocks(self):
        return self._blocks

    def is_horizontal(self):
        return self.blocks[0].y == self.blocks[1].y
