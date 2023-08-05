# Ways and relations used in this test.
#https://www.openstreetmap.org/way/358445798
#https://www.openstreetmap.org/relation/1228099
#https://www.openstreetmap.org/way/362327591
#https://www.openstreetmap.org/relation/4795362
#https://www.openstreetmap.org/way/200068201
#https://www.openstreetmap.org/way/358445798
#https://www.openstreetmap.org/relation/1228099
#https://www.openstreetmap.org/way/362327591
#https://www.openstreetmap.org/relation/4795362
#https://www.openstreetmap.org/relation/4795362
#https://www.openstreetmap.org/way/200068201
#https://www.openstreetmap.org/way/220084069
#https://www.openstreetmap.org/way/242899474

# expect these features in _both_ the landuse and POIs layers.
for layer in ['pois', 'landuse']:

    # tourism whitelist
    tourism_values = [
        (16, 17645, 24242, 358445798, 'artwork'), # City Sculpture, Detroit
        (13, 2240, 3421, -1228099, 'theme_park'), # Walt Disney World Resort
        (13, 2351, 3181, 362327591, 'theme_park'), # Busch Gardens Williamsburg
        (14, 2825, 6555, -4795362, 'resort'), # Disneyland Resort
        (14, 2812, 6557, 200068201, 'aquarium') # Aquarium of the Pacific
    ]

    for z, x, y, osm_id, tourism in tourism_values:
        test.assert_has_feature(
            z, x, y, layer,
            { 'id': osm_id,
              'kind': tourism })

# these are POIs, but also a buildings, so they won't show up in the landuse
# layer.
# Wendy Thompson Hut, BC
test.assert_has_feature(
    15, 5236, 11051, 'pois',
    { 'id': 220084069,
      'kind': 'wilderness_hut' })
# Scharffenberger Winery
test.assert_has_feature(
    16, 10296, 25030, 'pois',
    { 'id': 242899474,
      'kind': 'winery' })

# this is a POI, but also a point, so as it has no area, it won't show up
# in the landuse layer.
# http://www.openstreetmap.org/node/3095286850
test.assert_has_feature(
    16, 34893, 21123, 'pois',
    { 'id': 3095286850,
      'kind': 'trail_riding_station' })
