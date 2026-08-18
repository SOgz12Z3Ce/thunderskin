class InlineAspect:
    def __init__(self, _id: str):
        self.id = _id

    def symbol(self):
        return f"elements/{self.id}"
    
    def __eq__(self, other):
        if not isinstance(other, InlineAspect):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
