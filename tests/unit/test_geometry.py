from alzak.core.geometry import RectF


def test_aabb_overlap_and_touching_edge() -> None:
    base = RectF(0.0, 0.0, 10.0, 10.0)
    assert base.intersects(RectF(9.0, 5.0, 4.0, 4.0))
    assert not base.intersects(RectF(10.0, 0.0, 4.0, 4.0))
