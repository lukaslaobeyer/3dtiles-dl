import numpy as np


class OrientedBoundingBox:
    def __init__(self, vertices):
        assert vertices.shape == (8, 3)
        self.vertices = vertices

    @staticmethod
    def from_tilespec(spec, eps=1e-2):
        assert "box" in spec
        center = np.array(spec["box"][:3])
        halfx = np.array(spec["box"][3:6])
        halfy = np.array(spec["box"][6:9])
        halfz = np.array(spec["box"][9:12])

        return OrientedBoundingBox(np.stack((
            center - halfx - halfy - halfz,
            center + halfx - halfy - halfz,
            center + halfx + halfy - halfz,
            center - halfx + halfy - halfz,
            center - halfx - halfy + halfz,
            center + halfx - halfy + halfz,
            center + halfx + halfy + halfz,
            center - halfx + halfy + halfz,
        )))


class Sphere:
    def __init__(self, center, r):
        self.center = np.array(center)
        self.r = r

    def test(self, other):
        """Returns true when `other` contains this Sphere's `center`, or when this Sphere
        completely contains `other`"""

        if not isinstance(other, OrientedBoundingBox):
            raise TypeError("unsupported type")

        P0, P1, P2, P3 =\
            other.vertices[0], other.vertices[1], other.vertices[3], other.vertices[4]
        u = P1 - P0
        v = P2 - P0
        w = P3 - P0

        is_center_inside_box = (
            u.dot(P0) <= u.dot(self.center) <= u.dot(P1) and
            v.dot(P0) <= v.dot(self.center) <= v.dot(P2) and
            w.dot(P0) <= w.dot(self.center) <= w.dot(P3)
        )

        return is_center_inside_box or (
            np.linalg.norm((other.vertices - self.center), axis=-1) < self.r
        ).all()
