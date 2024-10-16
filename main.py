import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imageio
import matplotlib.patches as patches
import matplotlib.cbook as cbook
from matplotlib.pyplot import figure
import os

for file_in in os.listdir():
    if 'interno_v005' in file_in:
        file = file_in
        break

#file = 'interno_v005_20190916_1242.txt'
Interno = pd.read_csv(file, skiprows=23, encoding='windows-1252',
                      #sep='\s+',
                      delim_whitespace=True,
                      #usecols=['Elapsed', 'time', 'P', 'HeightMSL', 'Temp', 'RH', 'Dewp', 'Speed', 'Dir', 'O3',
                      #         'BoxTemperature', 'O3Current', 'IntegratedOzone', 'ResidualOzone', 'TotalOzone',
                      #         'O3PumpCurrent', 'KeyFlags']
                    )
##############################################################################
with open(file) as fl:
    lineas = fl.readlines()
for i in range(0, len(lineas)):
    if 'Balloon release date' in( lineas[i]):
        fecha = pd.to_datetime(lineas[i][-12:].split(), format='%d/%m/%y')[0]
        nameFileImage = fecha.strftime('%Y/%m/ozone_%Y%m%d.jpg')
###############################################################################

for file_in in os.listdir():
    if 'us' in file_in:
        us = file_in
#us = 'us190916.txt'
with open(us) as us_aux:
    lineas = us_aux.readlines()
for i in range(0, len(lineas)):
    if 'Ushuaia' in ( lineas[i]):
        for j in lineas[i+2].replace('  ', ' ').split(' '):
            print(j)
        Dobson = lineas[i+2].replace('  ', ' ').split(' ')[11]
        ECC = lineas[i+2].replace('  ', ' ').split(' ')[10]


aux = Interno.columns.tolist()[1:]
aux.append('ZZZ')
Interno.drop(index=0, inplace=True)
Interno.columns = aux
Interno.loc[:,Interno.columns[:-2]]= Interno.loc[:,Interno.columns[:-2]].apply(pd.to_numeric, errors='coerce')

Interno.KeyFlags = Interno.KeyFlags.fillna('')+Interno.ZZZ.fillna('')
fig, ax = plt.subplots()
fig.set_size_inches(6.9, 9)
#fig.set_dpi(500)
ax.axis()
##https://stackoverflow.com/questions/41453902/is-it-possible-to-patch-an-image-in-matplotlib
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from urllib import request
from skimage import io
##############################################################################3
ax.annotate('Ozonosondeo Ushuaia ' + fecha.strftime('%d-%m-%Y'),
            xy=(0.5, .95), xycoords='axes fraction',
            xytext=(-20, 20), textcoords='offset pixels',
            horizontalalignment='center',
            verticalalignment='top',fontsize=18)

##############################################################################33

f = 'https://d1qb6yzwaaq4he.cloudfront.net/protocols/o3field/gome2b/' + nameFileImage

im = io.imread(f)
oi = OffsetImage(im, zoom = .35)
box = AnnotationBbox(oi, (32, 23200), frameon=False )
ax.add_artist(box)
##########################################################
from matplotlib.text import OffsetFrom
offset_from = OffsetFrom(box, (0.5, 1))
##########################################################33
ax.text(32,29000,s="Ozonosonda ECC:" + ECC + "UD\n"+
                     "Dobson N°131:    " + Dobson + "UD",
        horizontalalignment='center',
        backgroundcolor='white',
                    zorder=10)
#############################################################
offset_from_leg = OffsetFrom(box, (0.5, 0))
legends = 'https://www.temis.nl/protocols/o3hole/img/legend_o3_0.jpg'
im_leg = io.imread(legends)
oi_leg = OffsetImage(im_leg, zoom = .437)
box_leg = AnnotationBbox(oi_leg, (32, 16500), frameon=False,
                         #boxcoords=offset_from_leg
                         )
ax.add_artist(box_leg)
##########################################################33
ColorTropo = 'lightblue'
ColorEstra = 'skyblue'
ColorPres = 'purple'
ax.plot(Interno.O3, Interno.HeightMSL, color=ColorPres, linewidth=3)#, alpha=.3, marker='.', linestyle=''

ax.axes.set_xlim(0, 40)
ax.axes.set_ylim(0, 40000)
#ax.set_xlabel(r'$P\ [mPa]$')
ax.xaxis.label.set_color(ColorPres)
ax.tick_params(axis='x', colors=ColorPres)
ax.spines['bottom'].set_color(ColorPres)
#############################################3
from matplotlib.ticker import EngFormatter
formatter0 = EngFormatter(unit='mPa')
ax.xaxis.set_major_formatter(formatter0)
formatter2 = EngFormatter(unit='m')
ax.yaxis.set_major_formatter(formatter2)
################################################

Tropopausa = Interno.HeightMSL.loc[Interno.KeyFlags.str.contains('Tr', regex=True, na=False)].head(1).values[0]
Temp = Interno.Temp.loc[Interno.HeightMSL==Tropopausa].head(1).values[0]
ax.add_patch(plt.Rectangle((0, 0), 40, Tropopausa, color=ColorTropo))
ax.add_patch(plt.Rectangle((0, Tropopausa), 40, 40000, color=ColorEstra))

bbox = dict(boxstyle="round", fc="0.8")
arrowprops = dict(
    arrowstyle="->",
#    connectionstyle="angle,angleA=010,angleB=180,rad=10"
)

ColorTemp = 'blue'
ax2=ax.twiny()
ax2.get_xaxis().set_visible(False)
ax2.spines['bottom'].set_color(ColorPres)

ax_2 = ax2.secondary_xaxis(-0.06)
ax_2.set_color(ColorTemp)
#ax_2.set_xlabel(r'$T\ [^oC]$')# ax.twiny()
ax_2.xaxis.label.set_color(ColorTemp)

#ax2.axis['bottom'] = ax2.new_fixed_axis(loc="bottom", offset=(0,10))
ax2.plot(Interno.Temp, Interno.HeightMSL, color=ColorTemp,linewidth=3)#, alpha=.3, marker='.', linestyle=''
ax2.set_xlim(-120, 20)
formatter1 = EngFormatter(unit=r'$^oC$')
ax_2.xaxis.set_major_formatter(formatter1)

ax2.annotate(
    f'Tropopausa a los {Tropopausa:.1f}m con {Temp:.1f}°C',
    xy=(Temp, Tropopausa),
    xytext=(0.2*72, -90), textcoords='offset points',
    bbox=bbox, arrowprops=arrowprops)


################################################################33
nameOut= 'Perfil_' + fecha.strftime('%d-%m-%Y') +'.jpg'
fig.savefig(nameOut, dpi=500)
###ADD LOGOS
import agregarlogo as logo

logo.crearGeneral(fig,ax, nameOut)


#################################################################33

plt.show()