class Rectangle:
    def __init__(self, length: int, width: int):
        """Initialize the rectangle with length and width."""
        self.length = length
        self.width = width

    def __iter__(self):
        """Return an iterator that yields the length and width in the specified format."""
        yield {'length': self.length}
        yield {'width': self.width}

# Example usage
if __name__ == "__main__":
    rect = Rectangle(5, 10)

    # Iterating over the rectangle instance
    for dimension in rect:
        print(dimension)
