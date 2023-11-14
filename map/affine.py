# 2153689

class Affine:
    def __init__(self, left, right, LEFT, RIGHT) -> None:
        self.left = left
        self.right = right
        self.LEFT = LEFT
        self.RIGHT = RIGHT
    
    def Forward(self, co):
        left = self.left
        right = self.right
        LEFT = self.LEFT
        RIGHT = self.RIGHT
        CO = (co - left) / (right - left) * (RIGHT - LEFT) + LEFT
        return CO
    
    def Reverse(self, CO):
        left = self.left
        right = self.right
        LEFT = self.LEFT
        RIGHT = self.RIGHT
        co = (CO - LEFT) * (right - left) / (RIGHT - LEFT) + left
        return co
    