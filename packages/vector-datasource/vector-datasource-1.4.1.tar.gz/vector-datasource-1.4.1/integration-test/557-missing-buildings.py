# Best Tile
#https://www.openstreetmap.org/way/103383621
test.assert_has_feature(
    16, 10484, 25339, 'buildings',
    {'id': 103383621})

# Miraloma School
#https://www.openstreetmap.org/way/338881092
test.assert_has_feature(
    16, 10476, 25339, 'buildings',
    {'id': 338881092})

# Tiny individual building (way_area = 5.4 sq.m.)
#https://www.openstreetmap.org/way/278410540
test.assert_has_feature(
    16, 10474, 25343, 'buildings',
    {'id': 278410540, 'min_zoom': 17})
