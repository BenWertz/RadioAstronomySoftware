import numpy as np
import astropy
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.visualization import astropy_mpl_style, quantity_support
plt.style.use(astropy_mpl_style)
quantity_support()

class RadioSource:
    coords:SkyCoord
    altaz_coords:SkyCoord
    def __init__(self,name,coords:SkyCoord,frame:AltAz):
        self.name=name
        self.coords=coords
        self.altaz_coords=self.coords.transform_to(frame)
    def __repr__(self):
        return f"{self.name} (@{str(self.altaz_coords.alt)})"

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

a=cas_a.transform_to(AltAz(obstime=utcTime,location=hollis_nh,pressure=0))
print(f"A: {type(a)}")
for i,j in zip(list(a.__dict__.keys()),list(a.__dict__.keys())):
    print(f"\t{i}:{j} (={str(j)}); {str(a.__dict__[i])}")
print(a._sky_coord_frame.alt)


# sources=[
#     RadioSource("Cas A",cas_a,altaz_frame),
#     RadioSource("Cyg A",cyg_a,altaz_frame),
#     RadioSource("Tau A",tau_a,altaz_frame),
#     RadioSource("Vir A",vir_a,altaz_frame)
# ]

# for source in sources:
#     print(f"{type(source)}\t{str(source)}\n")