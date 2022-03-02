import numpy as np
import astropy
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from dateutil import tz
from time import sleep
import datetime
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from math import *
from astropy.visualization import astropy_mpl_style, quantity_support
from matplotlib.ticker import MultipleLocator,AutoMinorLocator

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
#vir_a=SkyCoord.from_name("Virgo A")

est_offset=4*u.hour
#utcTime=Time("2022-02-11 12:00:00")-utcOffset
utcTime=Time.now()

hollis_nh=EarthLocation(
    lat=42.75291*u.deg,
    lon=-71.60056*u.deg,
    height=129*u.m
)

altaz_frame=AltAz(obstime=utcTime,location=hollis_nh,pressure=0)

abc = tz.gettz('US/Pacific')
dat = datetime.datetime(2010, 9, 25, 10, 36)

midnight = Time('2022-03-01 00:00:00')+est_offset
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


fig, ax = plt.subplots()

#plt.xlabel('Time (hours)')
#ax.ylabel('Elevation angle (degrees)')


ax.set_xlim(0,24)
ax.set_ylim(0,90)
ax.set_title(f"Altitude of radio source targets over 24 hours (day:{midnight})",fontsize=12)
ax.set_xlabel(xlabel="Time (hours)",fontsize=10)
ax.set_ylabel(ylabel="Altitude angle (degrees)",fontsize=10)

ax.xaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_major_formatter('{x:.0f}')
ax.xaxis.set_minor_locator(AutoMinorLocator(2))

ax.yaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_major_formatter('{x:.0f}')
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.tick_params(which='major', length=6)
ax.tick_params(which='minor', length=3)

# ax.yaxis.set_major_locator(MultipleLocator(10))
# ax.yaxis.set_major_formatter('{x:.0f}')
# ax.yaxis.set_minor_locator(MultipleLocator(5))

for i in range(len(sources)):
    source=sources[i]
    ax.plot(
        delta_midnight,
        source.coords.transform_to(frame_range).alt.degree,
        label=source.name
    )
    t=(source.coords.ra-midnight.sidereal_time("apparent",hollis_nh.lon))
    print(f"{source.name}: Culmination at {(t%(360*u.degree)).hms}")
    ax.axvline(x=(t.hour%24),color=["blue","purple","red","green"][i])
ax.legend(loc='upper left')

plt.show()