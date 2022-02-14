import numpy as np
import astropy
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from time import sleep
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from math import *
from astropy.visualization import astropy_mpl_style, quantity_support
plt.style.use(astropy_mpl_style)
quantity_support()

class RadioSource:
    coords:SkyCoord
    altaz_coords:SkyCoord
    def __init__(self,name,coords:SkyCoord,frame:AltAz):
        self.name=name
        self.coords=coords
        self.update(frame)
    def update(self,frame):
        self.altaz_coords=self.coords.transform_to(frame)
    def __repr__(self):
        return f"{self.name} (Azimuth: {self.altaz_coords.az}, Altitude: {self.altaz_coords.alt})"

cas_a=SkyCoord.from_name("Cassiopeia A")
cyg_a=SkyCoord.from_name("Cygnus A")
tau_a=SkyCoord.from_name("M1")
vir_a=SkyCoord.from_name("Virgo A")

edt_offset=-5*u.hour
#utcTime=Time("2022-02-11 12:00:00")-utcOffset
utcTime=Time.now()

hollis_nh=EarthLocation(
    lat=42.75284*u.deg,
    lon=-71.60044*u.deg,
    height=129*u.m
)

altaz_frame=AltAz(obstime=utcTime,location=hollis_nh,pressure=0)

midnight = Time('2022-03-01 05:00:00')
delta_midnight = np.linspace(0, 24, 1000)*u.hour
time_range = midnight + delta_midnight
frame_range = AltAz(obstime=time_range, location=hollis_nh)
casa_r=cas_a.transform_to(frame_range)

sources=[
    RadioSource("Cas A",cas_a,altaz_frame),
    RadioSource("Cyg A",cyg_a,altaz_frame),
    RadioSource("Tau A",tau_a,altaz_frame),
    RadioSource("Vir A",vir_a,altaz_frame)
]

for i in range(len(sources)):
    source=sources[i]
    plt.plot(
        delta_midnight,
        -source.coords.transform_to(frame_range).alt.degree,
        label=source.name
    )
    t=(source.coords.ra-midnight.sidereal_time("apparent",hollis_nh.lon))%(360*u.degree)
    print(f"{source.name}: Culmination at {t.hms}")
    plt.axvline(x=(t.hour%24),color=["blue","purple","red","green"][i])
plt.legend(loc='upper left')

plt.show()