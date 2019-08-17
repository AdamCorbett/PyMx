
class ActivityArea:
    def __init__(self, area):
        self.camera = 0
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.poly = []
        self.parse(area)

    def parse(self, area):
        values = area.split(',')
        self.camera = values[0]
        if values[1].startswith("poly"):
            points = values[1].split('=')[1]
            for point in points.split('/'):
                x, y = point.split('x')
                self.poly.append((x, y))
        else:
            self.x = values[1]
            self.y = values[2]
            self.width = values[3]
            self.height = values[4]

    def __repr__(self):
        if len(self.poly) == 0:
            return "{0}: ({1}, {2}), ({3}, {4})".format(self.camera, self.x, self.y, self.width, self.height)
        else:
            points = []
            for point in self.poly:
                points.append("({0}, {1})".format(point[0], point[1]))
            return "{0}: [{1}]".format(self.camera, "-".join(points))