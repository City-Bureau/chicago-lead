import sys

filename = sys.argv[1]

vrt = '''<OGRVRTDataSource>
    <OGRVRTLayer name="%s">
        <SrcDataSource>%s.csv</SrcDataSource>
        <GeometryType>wkbPoint</GeometryType>
        <LayerSRS>WGS84</LayerSRS>
        <GeometryField encoding="PointFromColumns" x="long" y="lat"/>
    </OGRVRTLayer>
</OGRVRTDataSource>''' % (filename, filename)

with sys.stdout as f:
	f.write(vrt)
