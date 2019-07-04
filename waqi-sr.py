import os
import sys
import argparse
import json
import matplotlib.pyplot as plt
import matplotlib as mpl

# Set default figure parameters
mpl.rcParams['figure.figsize'] = [16, 10]
mpl.rcParams['figure.facecolor'] = 'w'

# English text dictionary
TEXT_EN = {
    'title': 'Air Quality Index of',
    'good': {
        'name': 'Good',
        'description': ('Air quality is considered satisfactory, and air '
                        'pollution poses little or no risk.')
    },
    'moderate': {
        'name': 'Moderate',
        'description': ('Air quality is acceptable; however, for some '
                        'pollutants there may be a moderate health concern '
                        'for a very small number of people who are unusually '
                        'sensitive to air pollution.')
    },
    'unhealthy_sg': {
        'name': 'Unhealthy for Sensitive Groups',
        'description': ('Members of sensitive groups may experience health '
                        'effects. The general public is not likely to be '
                        'affected.')
    },
    'unhealthy': {
        'name': 'Unhealthy',
        'description': ('Everyone may begin to experience health effects; '
                        'members of sensitive groups may experience more '
                        'serious health effects.')
    },
    'very_unhealthy': {
        'name': 'Very Unhealthy',
        'description': ('Health warnings of emergency conditions. The entire '
                        'population is likely to be affected.')
    },
    'hazardous': {
        'name': 'Hazardous',
        'description': ('Health alert: everyone may experience serious health '
                        'effects.')
    }
}

# Spanish text dictionary
TEXT_ES = {
    'title': 'Índice de la Calidad del Aire en',
    'good': {
        'name': 'Bueno',
        'description': ('La calidad del aire se considera satisfactoria y la '
                        'contaminación atmosférica presenta poco o ningún '
                        'riesgo.')
    },
    'moderate': {
        'name': 'Moderado',
        'description': ('La calidad del aire es aceptable; sin embargo, para '
                        'algunos contaminantes puede haber una preocupación '
                        'moderada de salud para un número muy pequeño de '
                        'personas que son inusualmente sensibles a la '
                        'contaminación del aire.')
    },
    'unhealthy_sg': {
        'name': 'Dañino para Grupos Sensitivos',
        'description': ('Los miembros de grupos sensibles pueden experimentar '
                        'efectos en su salud. No es probable que el público '
                        'general se vea afectado.')
    },
    'unhealthy': {
        'name': 'Dañino',
        'description': ('Todo el mundo puede comenzar a experimentar efectos '
                        'en su salud; los miembros de grupos sensibles pueden '
                        'experimentar efectos más graves.')
    },
    'very_unhealthy': {
        'name': 'Muy Dañino',
        'description': ('Advertencias sanitarias sobre situaciones de '
                        'emergencia. Es probable que toda la población se vea '
                        'afectada.')
    },
    'hazardous': {
        'name': 'Nocivo',
        'description': ('Alerta de salud: todo el mundo puede experimentar '
                        'efectos de salud graves.')
    }
}

def get_color(aqi):
    if (aqi >= 0 and aqi <= 50):
        return plt.cm.Greens(0.7)
    elif (aqi > 50 and aqi <= 100):
        return plt.cm.YlOrRd(0.2)
    elif (aqi > 100 and aqi <= 150):
        return plt.cm.YlOrRd(0.4)
    elif (aqi > 150 and aqi <= 200):
        return plt.cm.Reds(0.7)
    elif (aqi > 200 and aqi <= 300):
        return plt.cm.Purples(0.8)
    else:
        return plt.cm.PuRd(1.0)

def get_aqi_text(aqi, lang='en'):
    if lang == 'es':
        text = TEXT_ES
    else:
        text = TEXT_EN

    if (aqi >= 0 and aqi <= 50):
        return text['good']
    elif (aqi > 50 and aqi <= 100):
        return text['moderate']
    elif (aqi > 100 and aqi <= 150):
        return text['unhealthy_sg']
    elif (aqi > 150 and aqi <= 200):
        return text['unhealthy']
    elif (aqi > 200 and aqi <= 300):
        return text['very_unhealthy']
    else:
        return text['hazardous']

def get_pollutants(data):
    pollutants = []
    # Check if iaqi dict exists
    if ('data' in data and
            'iaqi' in data['data'] and
            data['data']['iaqi']):
        iaqi = data['data']['iaqi']

        if ('co' in iaqi and 'v' in iaqi['co'] and iaqi['co']['v']):
            pollutants.append({'name': 'CO', 'value': int(iaqi['co']['v'])})
        if ('no2' in iaqi and 'v' in iaqi['no2'] and iaqi['no2']['v']):
            pollutants.append({'name': 'NO2', 'value': int(iaqi['no2']['v'])})
        if ('o3' in iaqi and 'v' in iaqi['o3'] and iaqi['o3']['v']):
            pollutants.append({'name': 'O3', 'value': int(iaqi['o3']['v'])})
        if ('pm10' in iaqi and 'v' in iaqi['pm10'] and iaqi['pm10']['v']):
            pollutants.append({'name': 'PM10', 'value': int(iaqi['pm10']['v'])})
        if ('pm25' in iaqi and 'v' in iaqi['pm25'] and iaqi['pm25']['v']):
            pollutants.append({'name': 'PM2.5', 'value': int(iaqi['pm25']['v'])})
        if ('so2' in iaqi and 'v' in iaqi['so2'] and iaqi['so2']['v']):
            pollutants.append({'name': 'SO2', 'value': int(iaqi['so2']['v'])})

        return pollutants
    else:
        print('Incorrect file')
        sys.exit(1)


def plot_principal_aqi(aqi, date, lang='en'):
    if aqi > 300:
        value = 100
    else:
        value = aqi / 3
    group_size = [value, 100 - value]

    color = get_color(aqi)
    text = get_aqi_text(aqi, lang)

    # Ring
    ax = plt.subplot(AX[0:2, :])
    ax.axis('equal')
    mypie, _ = ax.pie(group_size, radius=1.3, colors=[color, plt.cm.Greys(0.0)], startangle=90, counterclock=False)
    plt.setp(mypie, width=0.3, edgecolor='white')
    # Title
    ax.set_title(date, pad=25, fontsize=14)
    # Number
    ax.text(0, 0, str(aqi), ha='center', size=72, fontweight='bold', va='center', color=color)
    # Text
    ax.text(1.5, 1, text['name'], size=24, fontweight='bold', color=color, ha='left', va='center')
    ax.text(1.5, 0.5, text['description'], size=14, ha='left', va='center', wrap=True)

def plot_secondary_aqi(aqi, name, position):
    if aqi > 300:
        value = 100
    else:
        value = aqi / 3
    group_size = [value, 100 - value]

    color = get_color(aqi)

    # Ring
    ax = plt.subplot(AX[2, position])
    ax.axis('equal')
    mypie, _ = ax.pie(group_size, radius=1.3, colors=[color, plt.cm.Greys(0.0)], startangle=90, counterclock=False)
    plt.setp(mypie, width=0.3, edgecolor='white')
    # Name
    ax.set_xlabel(name, fontsize=14)
    # Number
    ax.text(0, 0, str(aqi), ha='center', size=38, fontweight='bold', va='center', color=color)

def set_title(name, lang='en'):
    if lang == 'es':
        text = TEXT_ES
    else:
        text = TEXT_EN
    plt.suptitle(text.get('title') + ' ' + name, fontsize=18, fontweight='bold')


if __name__ == '__main__':

    # Parse the options
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE')
    parser.add_argument('-o', '--output', help='Save the result to a local file.')
    parser.add_argument('--lang', help='Language. Currently "es" and "en" are only available.', default='en')
    args = parser.parse_args()

    if (hasattr(args, 'output') and args.output):
        # Set matplotlib non-interactive backend to work in a container
        mpl.use('agg')

    with open(args.FILE, 'r') as f:
        json_data = f.read()
    data = json.loads(json_data)

    # Check if principal aqi exists
    if ('data' in data and
            'aqi' in data['data'] and
            data['data']['aqi']):
        principal_aqi = int(data['data']['aqi'])
    else:
        print('Incorrect file')
        sys.exit(1)

    # Check if time exists
    if ('data' in data and
            'time' in data['data'] and
            's' in data['data']['time'] and
            data['data']['time']['s']):
        date = data['data']['time']['s']
    else:
        print('Incorrect file')
        sys.exit(1)

    # Check if city name exists
    if ('data' in data and
            'city' in data['data'] and
            'name' in data['data']['city'] and
            data['data']['city']['name']):
        city_name = data['data']['city']['name']
    else:
        print('Incorrect file')
        sys.exit(1)

    pollutants = get_pollutants(data)

    # Create the grid spec
    AX = mpl.gridspec.GridSpec(3, len(pollutants))

    set_title(city_name, args.lang)

    plot_principal_aqi(principal_aqi, date, lang=args.lang)

    for i, pollutant in enumerate(pollutants):
        plot_secondary_aqi(pollutant['value'], pollutant['name'], i)

    if (hasattr(args, 'output') and args.output):
        plt.savefig(args.output)
    else:
        plt.show()
