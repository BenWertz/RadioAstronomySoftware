from astroplan import Observer, FixedTarget
from astropy.coordinates import EarthLocation,SkyCoord,get_sun
from astropy.time import Time
import astropy.units as u
import datetime
from dateutil import tz

def text_spacing(entries,spacing):
    out=""
    for i in range(len(entries)):
        out+=entries[i]
        out+=" "*(spacing*(i+1)-len(out))
    return out

target_sources=[
    FixedTarget.from_name("Cassiopeia A"),
    FixedTarget.from_name("Cygnus  A"),
    FixedTarget.from_name("M 1"),
    FixedTarget.from_name("Virgo  A"),
]

hollis_nh=EarthLocation(
    lat=42.75291*u.deg,
    lon=-71.60056*u.deg,
    height=129*u.m
)

observer=Observer(location=hollis_nh,timezone="US/Eastern")

days=[]
meridian_times=[]

# Let's hope this is when we can start.
# To be honest, we both know we should have been here a long time ago.
first_day=Time("2021-04-28 00:00:00")

numDays=30+(31-7)

#Generate time objects for each day.
for i in range(numDays):
    current_day=first_day+i*u.day
    day_meridians=[]
    for source in target_sources:
        mer=observer.target_meridian_transit_time(
            current_day,source,'next'
        )
        mer.format="iso"
        day_meridians.append(mer)
    days.append(current_day)
    meridian_times.append(day_meridians)

# Open thank-you to https://www.geeksforgeeks.org/formatting-dates-in-python/ for explaining time formatting
# (seriously, it's so useful and solves like half of my problems)

observation_window=2*u.hour
spacing=15
header="Day"
header+=" "*(15-len(header))
header+=text_spacing(["Cassiopeia A","Cygnus A","Taurus A","Virgo A"],spacing)
header+="Sun transit"
print(header)
for i in range(len(days)):
    line=days[i].to_datetime().strftime("%a, %b %d")
    line+=" "*(15-len(line))
    l0=len(line)
    for j in range(len(meridian_times[i])):
        midTime=observer.astropy_time_to_datetime(meridian_times[i][j])
        startTime=observer.astropy_time_to_datetime(meridian_times[i][j]-0.5*observation_window)
        endTime=observer.astropy_time_to_datetime(meridian_times[i][j]+0.5*observation_window)
        line+=f"{midTime.strftime('%I:%M:%S %p')}"
#        line+=f"{startTime.strftime('%I:%M:%S %p')}-{endTime.strftime('%I:%M:%S %p')}"
        #if j!=len(meridian_times[i])-1:
        line+=" "*(spacing*(j+1)+l0-len(line))
    current_sun=get_sun(days[i])
    sun_time=observer.target_meridian_transit_time(days[i],current_sun)
    line+=f" {observer.astropy_time_to_datetime(sun_time).strftime('%I:%M:%S %p')}: {repr(observer.altaz(sun_time,current_sun).alt)}"
    print(line+"\n")
print()
for j in range(len(meridian_times[0])):
    print(["Cas A","Cyg A","Tau A","Vir A"][j]+":"+repr(observer.altaz(meridian_times[0][j],target_sources[j]).alt))
