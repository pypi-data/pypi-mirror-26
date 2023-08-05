import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'isotherms_json')

DATA = {
    'MCM-41': {
        'file': 'MCM-41 N2 77.355.json',
        'bet_area': 400.0,
        's_bet_area': 350.0,
        't_pore_volume': 0.28,
        't_area': 80.0,
    },
    'NaY': {
        'file': 'NaY N2 77.355.json',
        'bet_area': 700.0,
        't_pore_volume': 0.26,
        't_area': 120.0,
    },
    'SiO2': {
        'file': 'SiO2 N2 77.355.json',
        'bet_area': 200.0,
        't_pore_volume': 0.0,
        't_area': 280.0,
    },
    'Takeda 5A': {
        'file': 'Takeda 5A N2 77.355.json',
        'bet_area': 1075.0,
        't_pore_volume': 0.43,
        't_area': 130.0,
    },
    'UiO-66(Zr)': {
        'file': 'UiO-66(Zr) N2 77.355.json',
        'bet_area': 1250.0,
        't_pore_volume': 0.48,
        't_area': 20.0,
    },

}

DATA_IAST = {
    'CH4': {
        'file': 'MOF-5(Zn) - IAST - CH4.json',
    },
    'C2H6': {
        'file': 'MOF-5(Zn) - IAST - C2H6.json',
    },
}

DATA_ISOSTERIC = {
    't1': {
        'file': 'BAX 1500 - Isosteric Heat - 298.json',
    },
    't2': {
        'file': 'BAX 1500 - Isosteric Heat - 323.json',
    },
    't3': {
        'file': 'BAX 1500 - Isosteric Heat - 348.json',
    },
}
