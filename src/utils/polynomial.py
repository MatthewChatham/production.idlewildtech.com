colnames = ['Wavelength (nm)', 'Local DewPoint (F) ', 'Reactor Temp (C)', 'Ar (SLPM)', 'CO2 (SLPM)', 'H2 (SLPM)', 'Water (%) fuel ', 'Time since initital precusor Turn-on (min)']
plotnames = ['Wavelength (nm)', 'Local DewPoint (F) ', 'Reactor Temp (C)', 'Ar (SLPM)', 'CO2 (SLPM)', 'H2 (SLPM)', 'Water (%) fuel ', 'Time since initial<br>precursor Turn-on (min)']
argnames = ['wavelength', 'dewpoint', 'temp', 'ar', 'co2', 'h2', 'water', 'precursor']
def predict_polynomial(**kwargs):
    return 228.70377 - \
        0.016383 * kwargs['wavelength'] + \
        0.3250432 * kwargs['dewpoint'] - \
        0.081015 * kwargs['temp'] + \
        11.174133 * kwargs['ar'] + \
        146.74183 * kwargs['co2'] - \
        20.51894 * kwargs['h2'] - \
        2.474501 * kwargs['water'] + \
        0.0142118 * (kwargs['dewpoint'] - 41.8245) * (kwargs['dewpoint'] - 41.8245) + \
        0.0002391 * (kwargs['temp'] - 858.557) * (kwargs['temp'] - 858.557) - \
        0.083145 * (kwargs['wavelength'] - 686.453) * (kwargs['ar'] - 0.44482) - \
        282.5678 * (kwargs['co2'] - 0.10459) * (kwargs['co2'] - 0.10459) - \
        49.81929 * (kwargs['ar'] - 0.44482) * (kwargs['h2'] - 0.14547) - \
        126.5609 * (kwargs['co2'] - 0.10459) * (kwargs['h2'] - 0.14547) + \
        0.0037736 * (kwargs['wavelength'] - 686.453) * (kwargs['water'] - 5.41055) + \
        0.019309 * (kwargs['dewpoint'] - 41.8245) * (kwargs['water'] - 5.41055) + \
        0.0050497 * (kwargs['temp'] - 858.557) * (kwargs['water'] - 5.41055) + \
        0.1577076 * (kwargs['water'] - 5.41055) * (kwargs['water'] - 5.41055) + \
        0.0190479 * kwargs['precursor']  # -\
    # 5.604298*(var_lookup['Standardized data or preliminary data[Preliminary]']) -\
    # 1.948717*(var_lookup['Standardized data or preliminary data[Standard]'])
