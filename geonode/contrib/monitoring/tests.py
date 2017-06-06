# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
import os
from xml.etree.ElementTree import fromstring
import xmljson
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from geonode.contrib.monitoring.models import RequestEvent, Host, Service, ServiceType, populate, ExceptionEvent
from geonode.contrib.monitoring.collector import CollectorAPI
from geonode.base.populate_test_data import create_models
from geonode.layers.models import Layer
from geonode.layers.populate_layers_data import create_layer_data

req_xml = """<org.geoserver.monitor.RequestData>
<internalid>12681</internalid>
<id>12681</id>
<status>FINISHED</status>
<category>OWS</category>
<path>/wms</path>
<queryString>
<![CDATA[SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS=nurc:Arc_Sample&STYLES=&FORMAT=image/png&TRANSPARENT=true&HEIGHT=256&WIDTH=256&TILED=true&ZINDEX=9&SRS=EPSG:3857&CRS=EPSG:3857&BBOX=-5009377.085697311,10018754.171394618,0,15028131.257091932]]>
</queryString>
<body/>
<bodyContentLength>0</bodyContentLength>
<httpMethod>GET</httpMethod>
<startTime>2017-05-30 16:04:00.719 UTC</startTime>
<endTime>2017-05-30 16:04:00.809 UTC</endTime>
<totalTime>90</totalTime>
<remoteAddr>201.195.233.98</remoteAddr>
<remoteHost>201.195.233.98</remoteHost>
<remoteUser>anonymous</remoteUser>
<remoteUserAgent>
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393
</remoteUserAgent>
<remoteLat>0.0</remoteLat>
<remoteLon>0.0</remoteLon>
<host>demo.geo-solutions.it</host>
<internalHost>ks390295.kimsufi.com</internalHost>
<service>WMS</service>
<operation>GetMap</operation>
<owsVersion>1.3.0</owsVersion>
<resources>
<string>nurc:Arc_Sample</string>
</resources>
<responseLength>3622</responseLength>
<responseContentType>image/png</responseContentType>
<responseStatus>200</responseStatus>
<httpReferer>
http://dev.mapstore2.geo-solutions.it/mapstore/examples/api/?map=Prueba
</httpReferer>
<bbox class="org.geotools.geometry.jts.ReferencedEnvelope">
<minx>-45.00000000000001</minx>
<maxx>0.0</maxx>
<miny>66.51326044311185</miny>
<maxy>79.17133464081945</maxy>
<crs class="org.geotools.referencing.crs.DefaultGeographicCRS">
<name class="org.geotools.referencing.NamedIdentifier">
<code>WGS 84</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl">
<title class="org.geotools.util.SimpleInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.SimpleInternationalString>
<default/>
<string>European Petroleum Survey Group</string>
</org.geotools.util.SimpleInternationalString>
</title>
<alternateTitles class="org.geotools.resources.UnmodifiableArrayList">
<array>
<org.geotools.util.SimpleInternationalString serialization="custom">
<unserializable-parents/>
<org.geotools.util.SimpleInternationalString>
<default/>
<string>EPSG</string>
</org.geotools.util.SimpleInternationalString>
</org.geotools.util.SimpleInternationalString>
<org.geotools.util.SimpleInternationalString serialization="custom">
<unserializable-parents/>
<org.geotools.util.SimpleInternationalString>
<default/>
<string>
EPSG data base version 8.6 on HSQL Database Engine engine.
</string>
</org.geotools.util.SimpleInternationalString>
</org.geotools.util.SimpleInternationalString>
</array>
</alternateTitles>
<dates class="empty-set"/>
<edition class="org.geotools.util.SimpleInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.SimpleInternationalString>
<default/>
<string>8.6</string>
</org.geotools.util.SimpleInternationalString>
</edition>
<editionDate>1416524400000</editionDate>
<identifiers class="org.geotools.resources.UnmodifiableArrayList">
<array>
<org.geotools.metadata.iso.IdentifierImpl>
<code>EPSG</code>
</org.geotools.metadata.iso.IdentifierImpl>
</array>
</identifiers>
<citedResponsibleParties class="org.geotools.resources.UnmodifiableArrayList">
<array>
<org.geotools.metadata.iso.citation.ResponsiblePartyImpl>
<organisationName class="org.geotools.util.SimpleInternationalString" reference="../../../../title"/>
<contactInfo class="org.geotools.metadata.iso.citation.ContactImpl">
<onLineResource class="org.geotools.metadata.iso.citation.OnLineResourceImpl">
<function>
<name>INFORMATION</name>
</function>
<linkage>http://www.epsg.org</linkage>
</onLineResource>
</contactInfo>
<role>
<name>PRINCIPAL_INVESTIGATOR</name>
</role>
</org.geotools.metadata.iso.citation.ResponsiblePartyImpl>
</array>
</citedResponsibleParties>
<presentationForm class="org.geotools.resources.UnmodifiableArrayList">
<array>
<org.opengis.metadata.citation.PresentationForm>
<name>TABLE_DIGITAL</name>
</org.opengis.metadata.citation.PresentationForm>
</array>
</presentationForm>
</authority>
<name class="org.geotools.util.ScopedName">
<scope class="org.geotools.util.LocalName">
<name class="string">EPSG</name>
</scope>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">WGS 84</name>
</name>
</name>
</name>
<identifiers class="singleton-set">
<org.geotools.referencing.NamedIdentifier>
<code>4326</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../name/authority"/>
<version>8.6</version>
<name class="org.geotools.util.ScopedName">
<scope class="org.geotools.util.LocalName" reference="../../../../name/name/scope"/>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">4326</name>
</name>
</name>
</org.geotools.referencing.NamedIdentifier>
</identifiers>
<domainOfValidity class="org.geotools.metadata.iso.extent.ExtentImpl">
<description class="org.geotools.util.SimpleInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.SimpleInternationalString>
<default/>
<string>World.</string>
</org.geotools.util.SimpleInternationalString>
</description>
<geographicElements class="org.geotools.resources.UnmodifiableArrayList">
<array>
<org.geotools.metadata.iso.extent.GeographicBoundingBoxImpl>
<inclusion>true</inclusion>
<westBoundLongitude>-180.0</westBoundLongitude>
<eastBoundLongitude>180.0</eastBoundLongitude>
<southBoundLatitude>-90.0</southBoundLatitude>
<northBoundLatitude>90.0</northBoundLatitude>
</org.geotools.metadata.iso.extent.GeographicBoundingBoxImpl>
</array>
</geographicElements>
<temporalElements class="empty-set"/>
<verticalElements class="empty-set"/>
</domainOfValidity>
<scope class="org.geotools.util.GrowableInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.GrowableInternationalString>
<default>
<localMap class="singleton-map">
<entry>
<null/>
<string>
Horizontal component of 3D system. Used by the GPS satellite navigation system and for NATO military geodetic surveying.
</string>
</entry>
</localMap>
</default>
</org.geotools.util.GrowableInternationalString>
</scope>
<coordinateSystem class="org.geotools.referencing.cs.DefaultEllipsoidalCS">
<name class="org.geotools.referencing.NamedIdentifier">
<code>
Ellipsoidal 2D CS. Axes: latitude, longitude. Orientations: north, east. UoM: degree
</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../name/authority"/>
<name class="org.geotools.util.ScopedName">
<scope class="org.geotools.util.LocalName" reference="../../../../name/name/scope"/>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">
Ellipsoidal 2D CS. Axes: latitude, longitude. Orientations: north, east. UoM: degree
</name>
</name>
</name>
</name>
<alias class="singleton-set">
<org.geotools.util.ScopedName>
<scope class="org.geotools.util.LocalName">
<name class="string">EPSG abbreviation</name>
</scope>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">NAD83(2011) / CA 4 ftUS</name>
</name>
</org.geotools.util.ScopedName>
</alias>
<identifiers class="singleton-set">
<org.geotools.referencing.NamedIdentifier>
<code>6422</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../name/authority"/>
<version>8.6</version>
</org.geotools.referencing.NamedIdentifier>
</identifiers>
<remarks class="org.geotools.util.GrowableInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.GrowableInternationalString>
<default>
<localMap class="singleton-map">
<entry>
<null/>
<string>
Coordinates referenced to this CS are in degrees. Any degree representation (e.g. DMSH, decimal, etc.) may be used but that used must be declared for the user by the supplier of data. Used in geographic 2D coordinate reference systems.
</string>
</entry>
</localMap>
</default>
</org.geotools.util.GrowableInternationalString>
</remarks>
<axis>
<org.geotools.referencing.cs.DefaultCoordinateSystemAxis>
<name class="org.geotools.referencing.NamedIdentifier">
<code>Geodetic longitude</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../../name/authority"/>
<name class="org.geotools.util.ScopedName">
<scope class="org.geotools.util.LocalName" reference="../../../../../../name/name/scope"/>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">Geodetic longitude</name>
</name>
</name>
</name>
<identifiers class="singleton-set">
<org.geotools.referencing.NamedIdentifier>
<code>107</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../../../name/authority"/>
<version>8.6</version>
</org.geotools.referencing.NamedIdentifier>
</identifiers>
<remarks class="org.geotools.util.GrowableInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.GrowableInternationalString>
<default>
<localMap class="singleton-map">
<entry>
<null/>
<string>
Angle from the prime meridian plane to the meridian plane passing through the given point, eastwards usually treated as positive. Used in geographic 2D and geographic 3D coordinate reference systems.
</string>
</entry>
</localMap>
</default>
</org.geotools.util.GrowableInternationalString>
</remarks>
<abbreviation>Long</abbreviation>
<direction>
<name>EAST</name>
</direction>
<unit class="javax.measure.unit.TransformedUnit">
<__parentUnit class="javax.measure.unit.AlternateUnit">
<__symbol>rad</__symbol>
<__parent class="javax.measure.unit.ProductUnit">
<__elements/>
<__hashCode>0</__hashCode>
</__parent>
</__parentUnit>
<__toParentUnit class="javax.measure.converter.MultiplyConverter">
<__factor>0.017453292519943295</__factor>
</__toParentUnit>
</unit>
<minimum>-180.0</minimum>
<maximum>180.0</maximum>
<rangeMeaning>
<name>WRAPAROUND</name>
</rangeMeaning>
</org.geotools.referencing.cs.DefaultCoordinateSystemAxis>
<org.geotools.referencing.cs.DefaultCoordinateSystemAxis>
<name class="org.geotools.referencing.NamedIdentifier">
<code>Geodetic latitude</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../../name/authority"/>
<name class="org.geotools.util.ScopedName">
<scope class="org.geotools.util.LocalName" reference="../../../../../../name/name/scope"/>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">Geodetic latitude</name>
</name>
</name>
</name>
<identifiers class="singleton-set">
<org.geotools.referencing.NamedIdentifier>
<code>106</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../../../name/authority"/>
<version>8.6</version>
</org.geotools.referencing.NamedIdentifier>
</identifiers>
<remarks class="org.geotools.util.GrowableInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.GrowableInternationalString>
<default>
<localMap class="singleton-map">
<entry>
<null/>
<string>
Angle from the equatorial plane to the perpendicular to the ellipsoid through a given point, northwards usually treated as positive. Used in geographic 2D and geographic 3D coordinate reference systems.
</string>
</entry>
</localMap>
</default>
</org.geotools.util.GrowableInternationalString>
</remarks>
<abbreviation>Lat</abbreviation>
<direction>
<name>NORTH</name>
</direction>
<unit class="javax.measure.unit.TransformedUnit" reference="../../org.geotools.referencing.cs.DefaultCoordinateSystemAxis/unit"/>
<minimum>-90.0</minimum>
<maximum>90.0</maximum>
<rangeMeaning>
<name>EXACT</name>
</rangeMeaning>
</org.geotools.referencing.cs.DefaultCoordinateSystemAxis>
</axis>
</coordinateSystem>
<datum class="org.geotools.referencing.datum.DefaultGeodeticDatum">
<name class="org.geotools.referencing.NamedIdentifier">
<code>World Geodetic System 1984</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../name/authority"/>
<name class="org.geotools.util.ScopedName">
<scope class="org.geotools.util.LocalName" reference="../../../../name/name/scope"/>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">World Geodetic System 1984</name>
</name>
</name>
</name>
<alias class="java.util.Collections$UnmodifiableSet">
<c class="linked-hash-set">
<org.geotools.util.ScopedName>
<scope class="org.geotools.util.LocalName" reference="../../../../../coordinateSystem/alias/org.geotools.util.ScopedName/scope"/>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">WGS 84</name>
</name>
</org.geotools.util.ScopedName>
<org.geotools.util.ScopedName>
<scope class="org.geotools.util.LocalName">
<name class="string">EPSG</name>
</scope>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">World Geodetic System 1984</name>
</name>
</org.geotools.util.ScopedName>
<org.geotools.util.ScopedName>
<scope class="org.geotools.util.LocalName">
<name class="string">OGR</name>
</scope>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">World_Geodetic_System_1984</name>
</name>
</org.geotools.util.ScopedName>
<org.geotools.util.ScopedName>
<scope class="org.geotools.util.LocalName">
<name class="string">ESRI</name>
</scope>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">D_WGS_1984</name>
</name>
</org.geotools.util.ScopedName>
<org.geotools.util.ScopedName>
<scope class="org.geotools.util.LocalName">
<name class="string">Oracle</name>
</scope>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">WGS 84</name>
</name>
</org.geotools.util.ScopedName>
<org.geotools.util.ScopedName>
<scope class="org.geotools.util.LocalName">
<name class="string">OGC</name>
</scope>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">WGS84</name>
</name>
</org.geotools.util.ScopedName>
<org.geotools.util.LocalName>
<name class="string">WGS_84</name>
</org.geotools.util.LocalName>
<org.geotools.util.LocalName>
<name class="string">WGS_1984</name>
</org.geotools.util.LocalName>
</c>
</alias>
<identifiers class="singleton-set">
<org.geotools.referencing.NamedIdentifier>
<code>6326</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../name/authority"/>
<version>8.6</version>
</org.geotools.referencing.NamedIdentifier>
</identifiers>
<remarks class="org.geotools.util.GrowableInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.GrowableInternationalString>
<default>
<localMap class="singleton-map">
<entry>
<null/>
<string>
EPSG::6326 has been the then current realisation. No distinction is made between the original and subsequent (G730, G873, G1150, G1674 and G1762) WGS 84 frames. Since 1997, WGS 84 has been maintained within 10cm of the then current ITRF.
</string>
</entry>
</localMap>
</default>
</org.geotools.util.GrowableInternationalString>
</remarks>
<anchorPoint class="org.geotools.util.GrowableInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.GrowableInternationalString>
<default>
<localMap class="singleton-map">
<entry>
<null/>
<string>
Defined through a consistent set of station coordinates. These have changed with time: by 0.7m on 1994-06-29 (G730), a further 0.2m on 1997-01-29 (G873), 0.06m on 2002-01-20 (G1150), 0.2m on 2012-02-08 (G1674) and 0.02m on 2013-10-16 (G1762).
</string>
</entry>
</localMap>
</default>
</org.geotools.util.GrowableInternationalString>
</anchorPoint>
<realizationEpoch>-9223372036854775808</realizationEpoch>
<domainOfValidity class="org.geotools.metadata.iso.extent.ExtentImpl" reference="../../domainOfValidity"/>
<scope class="org.geotools.util.GrowableInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.GrowableInternationalString>
<default>
<localMap class="singleton-map">
<entry>
<null/>
<string>Satellite navigation.</string>
</entry>
</localMap>
</default>
</org.geotools.util.GrowableInternationalString>
</scope>
<ellipsoid class="org.geotools.referencing.datum.DefaultEllipsoid">
<name class="org.geotools.referencing.NamedIdentifier">
<code>WGS 84</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../name/authority"/>
<name class="org.geotools.util.ScopedName">
<scope class="org.geotools.util.LocalName" reference="../../../../../name/name/scope"/>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">WGS 84</name>
</name>
</name>
</name>
<alias class="java.util.Collections$UnmodifiableSet">
<c class="linked-hash-set">
<org.geotools.util.ScopedName>
<scope class="org.geotools.util.LocalName">
<name class="string">EPSG alias</name>
</scope>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">WGS84</name>
</name>
</org.geotools.util.ScopedName>
<org.geotools.util.ScopedName reference="../../../../alias/c/org.geotools.util.ScopedName[2]"/>
<org.geotools.util.ScopedName reference="../../../../alias/c/org.geotools.util.ScopedName[3]"/>
<org.geotools.util.ScopedName reference="../../../../alias/c/org.geotools.util.ScopedName[4]"/>
<org.geotools.util.ScopedName reference="../../../../alias/c/org.geotools.util.ScopedName[5]"/>
<org.geotools.util.ScopedName reference="../../../../alias/c/org.geotools.util.ScopedName[6]"/>
<org.geotools.util.LocalName reference="../../../../alias/c/org.geotools.util.LocalName"/>
<org.geotools.util.LocalName reference="../../../../alias/c/org.geotools.util.LocalName[2]"/>
</c>
</alias>
<identifiers class="singleton-set">
<org.geotools.referencing.NamedIdentifier>
<code>7030</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../../name/authority"/>
<version>8.6</version>
</org.geotools.referencing.NamedIdentifier>
</identifiers>
<remarks class="org.geotools.util.GrowableInternationalString" serialization="custom">
<unserializable-parents/>
<org.geotools.util.GrowableInternationalString>
<default>
<localMap class="singleton-map">
<entry>
<null/>
<string>
Inverse flattening derived from four defining parameters (semi-major axis; C20 = -484.16685*10e-6; earth's angular velocity w = 7292115e11 rad/sec; gravitational constant GM = 3986005e8 m*m*m/s/s).
</string>
</entry>
</localMap>
</default>
</org.geotools.util.GrowableInternationalString>
</remarks>
<semiMajorAxis>6378137.0</semiMajorAxis>
<semiMinorAxis>6356752.314245179</semiMinorAxis>
<inverseFlattening>298.257223563</inverseFlattening>
<ivfDefinitive>true</ivfDefinitive>
<unit class="javax.measure.unit.BaseUnit">
<__symbol>m</__symbol>
</unit>
</ellipsoid>
<primeMeridian class="org.geotools.referencing.datum.DefaultPrimeMeridian">
<name class="org.geotools.referencing.NamedIdentifier">
<code>Greenwich</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../name/authority"/>
<name class="org.geotools.util.ScopedName">
<scope class="org.geotools.util.LocalName" reference="../../../../../name/name/scope"/>
<separator>:</separator>
<name class="org.geotools.util.LocalName">
<asScopedName class="org.geotools.util.ScopedName" reference="../.."/>
<name class="string">Greenwich</name>
</name>
</name>
</name>
<identifiers class="singleton-set">
<org.geotools.referencing.NamedIdentifier>
<code>8901</code>
<codespace>EPSG</codespace>
<authority class="org.geotools.metadata.iso.citation.CitationImpl" reference="../../../../../name/authority"/>
<version>8.6</version>
</org.geotools.referencing.NamedIdentifier>
</identifiers>
<greenwichLongitude>0.0</greenwichLongitude>
<angularUnit class="javax.measure.unit.TransformedUnit" reference="../../../coordinateSystem/axis/org.geotools.referencing.cs.DefaultCoordinateSystemAxis/unit"/>
</primeMeridian>
</datum>
</crs>
</bbox>
</org.geoserver.monitor.RequestData>"""

req_big = xmljson.yahoo.data(fromstring(req_xml))

class RequestsTestCase(TestCase):

    fixtures = ['initial_data.json', 'bobby']

    def setUp(self):
        
        create_models('layer')

        self.user = 'admin'
        self.passwd = 'admin'
        self.u, _ = get_user_model().objects.get_or_create(username=self.user)
        self.u.is_active = True
        self.u.email = 'test@email.com'
        self.u.set_password(self.passwd)
        self.u.save()
        self.ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.47 Safari/537.36" 
        populate()

        self.host = Host.objects.create(name='localhost', ip='127.0.0.1')
        self.service_type = ServiceType.objects.get(name=ServiceType.TYPE_GEONODE)
        self.service = Service.objects.create(name='geonode', host=self.host, service_type=self.service_type)

    def test_gs_req(self):
        rq = RequestEvent.from_geoserver(self.service, req_big)
        self.assertTrue(rq)

    def test_gn_request(self):

        l = Layer.objects.all().first()
        self.client.login(username=self.user, password=self.passwd)
        self.client.get(reverse('layer_detail', args=(l.typename,)), **{"HTTP_USER_AGENT": self.ua})

        self.assertEqual(RequestEvent.objects.all().count(), 1)
        rq = RequestEvent.objects.get()
        self.assertTrue(rq.response_time > 0)
        self.assertEqual(list(rq.resources.all().values_list('name', 'type')), [(l.typename, u'layer',)])
        self.assertEqual(rq.request_method, 'GET')

    def test_gn_error(self):
        l = Layer.objects.all().first()
        self.client.login(username=self.user, password=self.passwd)
        resp = self.client.get(reverse('layer_detail', args=('nonex',)), **{"HTTP_USER_AGENT": self.ua})

        self.assertEqual(RequestEvent.objects.all().count(), 1)
        rq = RequestEvent.objects.get()
        self.assertEqual(ExceptionEvent.objects.all().count(), 1)
        eq = ExceptionEvent.objects.get()
        self.assertEqual('django.http.response.Http404', eq.error_type)


    def test_service_handlers(self):
        self.client.login(username=self.user, password=self.passwd)
        for idx, l in enumerate(Layer.objects.all()):
            for inum in range(0, idx+1):
                self.client.get(reverse('layer_detail', args=(l.typename,)), **{"HTTP_USER_AGENT": self.ua})
        requests = RequestEvent.objects.all()

        c = CollectorAPI()
        q = requests.order_by('created')
        c.process_requests(self.service, requests, q.last().created, q.first().created)
