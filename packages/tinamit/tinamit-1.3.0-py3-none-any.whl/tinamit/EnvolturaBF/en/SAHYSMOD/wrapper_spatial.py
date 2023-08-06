import os
import re
from warnings import warn

from subprocess import run
import numpy as np

from tinamit.BF import ModeloImpaciente
from tinamit.EnvolturaBF.en.SAHYSMOD.sahysmodIO import read_into_param_dic, write_from_param_dic


class ModeloSAHYSMOD(ModeloImpaciente):
    """
    This is the wrapper for SAHYSMOD. At the moment, it only works for one polygon (no spatial models).
    """

    def __init__(self, sayhsmod_exe, initial_data):
        """
        Inicialises the SAHYSMOD wrapper. You must have SAHYSMOD already installed on your computer.

        :param sayhsmod_exe: The path to the SAHYSMOD executable.
        :type sayhsmod_exe: str

        :param initial_data: The path to the initial data file. Create a SAHYSMOD input file set to run for one year
        according to the initial conditions for your model. As of now, Tinamit (and this wrapper) do not have spatial
        functionality, so make sure your model has only 1 internal polygon. If you'd like to contribute to adding
        spatial variability, we'd be forever grateful and will add your name to the credits. Get in touch!
        (julien.malard@mail.mcgill.ca)
        :type initial_data: str

        """

        # Inicialise as the super class.
        super().__init__()

        # The following attributes are specific to the SAHYSMOD wrapper

        # Create some useful model attributes
        self.n_poly = None  # Number of (internal) polygons in the model

        # Set the path from which to read input data.
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.input = os.path.join(current_dir, 'SAHYSMOD.inp')
        self.dic_input = {}

        # Set the working directory to write model output, and remember where the initial data is stored.
        self.working_dir, self.initial_data = os.path.split(initial_data)
        self.output = 'SAHYSMOD.out'

        # Prepare the command to the SAHYSMOD executable
        args = dict(SAHYSMOD=sayhsmod_exe, input=self.input, output=self.output)
        self.command = '{SAHYSMOD} {input} {output}'.format(**args)

        # Read input values from .inp file. This also takes care of setting appropriate dims for each variable.
        self._read_input_vals()

    def inic_vars(self):

        # DON'T change the names of the dictionary keys here. Bad things will happen if you do, because they are
        # specific to Tinamit's model wrapper class.
        self.variables.clear()

        for name, dic in vars_SAHYSMOD.items():
            self.variables[name] = {'val': None,
                                    'unidades': dic['units'],
                                    'ingreso': dic['inp'],
                                    'egreso': dic['out'],
                                    'dims': (1, )  # This will be changed later for multidimensional variables.
                                    }

    def iniciar_modelo(self, **kwargs):
        pass  # Nothing specific to do. Variables have already been read in .inic_vars()

    def avanzar_modelo(self, n_años):
        """

        :param n_años:
        :type n_años: int
        """

        # Create the appropriate input file:
        self._write_inp(n_year=n_años)

        # Run the command prompt command
        run(self.command, cwd=self.working_dir)

    def cerrar_modelo(self):
        pass  # Ne specific closing actions necessary.

    # Some internal functions specific to this SAHYSMOD wrapper
    def _write_inp(self, n_year):
        """
        This function writes a SAHYSMOD input file according to the model's current internal state (so that the
        simulation based on the input file will start with initial values corresponding to the model's present state).

        :param n_year: The number of years for which SAHYSMOD will be run.
        :type n_year: int

        """

        # Set the number of run years
        self.dic_input['NY'] = n_year

        for var_code in SAHYSMOD_output_vars:

            key = var_code.replace('#', '').upper()
            var_name = codes_to_vars[var_code]

            if var_code[-1] == '#':
                self.dic_input[key] = self.datos_internos[var_name]
            else:
                self.dic_input[key] = self.variables[var_name]['val']

        # Make sure we have no missing areas
        for k in ["A", "B"]:
            vec = self.dic_input[k]
            vec[vec == -1] = 0

        # And finally write the input file
        write_from_param_dic(param_dictionary=self.dic_input, to_fn=self.input)

    def leer_egr(self, n_year):
        """
        This function reads the last year of a SAHYSMOD output file.

        """

        dic_out = read_output_file(file_path=self.output, n_s=self.n_estaciones, n_p=self.n_poly, n_y=n_year)

        for cr in ['CrA', 'CrB', 'CrU', 'Cr4', 'A#', 'B#', 'U']:
            if dic_out[cr] == -1:
                dic_out[cr] = 0

        # Ajust for soil salinity of different crops
        kr = self.variables[codes_to_vars['Kr']]['val']
        if kr == 0:
            soil_sal = dic_out['A#'] * dic_out['CrA'] + dic_out['B#'] * dic_out['CrB'] + dic_out['U'] * dic_out['CrU']
            to_fill = ['Cr4']
        elif kr == 1:
            soil_sal = dic_out['CrU'] * dic_out['U'] + dic_out['C1*'] * (1 - dic_out['U'])
            to_fill = ['CrA', 'CrB', 'Cr4']
        elif kr == 2:
            soil_sal = dic_out['CrA'] * dic_out['A#'] + dic_out['C2*'] * (1 - dic_out['A#'])
            to_fill = ['CrB', 'CrU', 'Cr4']
        elif kr == 3:
            soil_sal = dic_out['CrB'] * dic_out['B#'] + dic_out['C3*'] * (1 - dic_out['B#'])
            to_fill = ['CrA', 'CrU', 'Cr4']
        elif kr == 4:
            soil_sal = dic_out['Cr4']
            to_fill = ['CrA', 'CrB', 'CrU']
        else:
            raise ValueError('There is a big mistake with your SAHYSMOD model. Sorry, we can\'t help.')

        for cr in to_fill:
            dic_out[cr][:] = soil_sal

        for var_code in SAHYSMOD_output_vars:

            var_name = codes_to_vars[var_code]

            if var_code[-1] == '#':
                # For seasonal variables...

                self.datos_internos[var_name]['val'][:] = dic_out[var_code]
                # Note: dynamic link with self.variables has already been created in self._read_input_vals()

            else:
                # For nonseasonal variables...

                self.variables[var_name]['val'][:] = dic_out[var_code]

    def _read_input_vals(self):
        """
        This function will read the initial values for the model from a SAHYSMOD input (.inp) file and save the
        relavant information to this model class's internal variables.

        """

        # Read the input file
        dic_input = read_into_param_dic(from_fn=self.initial_data)
        self.dic_input.clear()
        self.dic_input.update(dic_input)

        # Save the number of seasons and length of each season
        self.n_estaciones = int(dic_input['NS'])
        self.dur_estaciones = [int(float(x)) for x in dic_input['TS']]
        self.n_poly = n_poly = int(dic_input['NN_IN'])

        if dic_input['NY'] != 1:
            warn('More than 1 year specified in SAHYSMOD input file. Switching to 1 year of simulation.')
            dic_input['NY'] = 1

        # Make sure the number of season lengths equals the number of seasons.
        if self.n_estaciones != len(self.dur_estaciones):
            raise ValueError('Error in the SAHYSMOD input file: the number of season lengths specified is not equal '
                             'to the number of seasons (lines 3 and 4).')

        for var_name in vars_SAHYSMOD:
            self.variables[var_name]['val'] = np.zeros(n_poly, dtype=float)
            self.variables[var_name]['dims'] = (n_poly,)

            var_code = vars_SAHYSMOD[var_name]['code']
            if var_code[-1] == '#':
                self.datos_internos[var_name] = np.zeros((self.n_estaciones, n_poly), dtype=float)

        for var_code in SAHYSMOD_input_vars:

            key = var_code.replace('#', '').upper()

            var_name = codes_to_vars[var_code]

            data = np.array(dic_input[key], dtype=float)

            if var_code[-1] == '#':
                self.datos_internos[var_name][:] = data
                self.variables[var_name]['val'] = data[0]  # Create a dynamic link.
            else:
                self.variables[var_name]['val'][:] = data


# A dictionary of SAHYSMOD variables. See the SAHYSMOD documentation for more details.
vars_SAHYSMOD = {'Pp - Rainfall': {'code': 'Pp#', 'units': 'm3/season/m2', 'inp': True, 'out': False},
                 'Ci - Incoming canal salinity': {'code': 'Ci#', 'units': 'dS/m', 'inp': True, 'out': True},
                 'Cinf - Aquifer inflow salinity': {'code': 'Cinf', 'units': 'dS/m', 'inp': True, 'out': False},
                 'Dc - Capillary rise critical depth': {'code': 'Dc', 'units': 'm', 'inp': True, 'out': False},
                 'Dd - Subsurface drain depth': {'code': 'Dd', 'units': 'm', 'inp': True, 'out': False},
                 'Dr - Root zone thickness': {'code': 'Dr', 'units': 'm', 'inp': True, 'out': False},
                 'Dx - Transition zone thickness': {'code': 'Dx', 'units': 'm', 'inp': True, 'out': False},
                 'EpA - Potential ET crop A': {'code': 'EpA#', 'units': 'm3/season/m2', 'inp': True, 'out': False},
                 'EpB - Potential ET crop B': {'code': 'EpB#', 'units': 'm3/season/m2', 'inp': True, 'out': False},
                 'EpU - Potential ET non-irrigated': {'code': 'EpU#', 'units': 'm3/season/m2', 'inp': True,
                                                      'out': False},
                 'Flq - Aquifer leaching efficienty': {'code': 'Flq', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Flr - Root zone leaching efficiency': {'code': 'Flr', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Flx - Transition zone leaching efficiency': {'code': 'Flx', 'units': 'Dmnl', 'inp': True,
                                                               'out': False},
                 'Frd - Drainage function reduction factor': {'code': 'Frd#', 'units': 'Dmnl', 'inp': True,
                                                              'out': False},
                 'FsA - Water storage efficiency crop A': {'code': 'FsA#', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'FsB - Water storage efficiency crop B': {'code': 'FsB#', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'FsU - Water storage efficiency non-irrigated': {'code': 'FsU#', 'units': 'Dmnl',
                                                                  'inp': True, 'out': False},
                 'Fw - Fraction well water to irrigation': {'code': 'Fw#', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Gu - Subsurface drainage for irrigation': {'code': 'Gu#', 'units': 'm3/season/m2',
                                                             'inp': True, 'out': False},
                 'Gw - Groundwater extraction': {'code': 'Gw#', 'units': 'm3/season/m2', 'inp': True, 'out': True},
                 'Hp - Initial water level semi-confined': {'code': 'Hc', 'units': 'm', 'inp': True, 'out': False},
                 'IaA - Crop A field irrigation': {'code': 'IaA#', 'units': 'm3/season/m2', 'inp': True, 'out': True},
                 'IaB - Crop B field irrigation': {'code': 'IaB#', 'units': 'm3/season/m2', 'inp': True, 'out': True},
                 'Rice A - Crop A paddy?': {'code': 'KcA#', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Rice B - Crop B paddy?': {'code': 'KcB#', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Kd - Subsurface drainage?': {'code': 'Kd', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Kf - Farmers\'s responses?': {'code': 'Kf', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Kaq1 - Horizontal hydraulic conductivity 1': {'code': 'Kaq1', 'units': 'm/day', 'inp': True,
                                                                'out': False},
                 'Kaq2 - Horizontal hydraulic conductivity 2': {'code': 'Kaq2', 'units': 'm/day', 'inp': True,
                                                                'out': False},
                 'Kaq3 - Horizontal hydraulic conductivity 3': {'code': 'Kaq3', 'units': 'm/day', 'inp': True,
                                                                'out': False},
                 'Kaq4 - Horizontal hydraulic conductivity 4': {'code': 'Kaq4', 'units': 'm/day', 'inp': True,
                                                                'out': False},
                 'Ksc1 - Semi-confined aquifer 1?': {'code': 'Ksc1', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Ksc2 - Semi-confined aquifer 2?': {'code': 'Ksc2', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Ksc3 - Semi-confined aquifer 3?': {'code': 'Ksc3', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Ksc4 - Semi-confined aquifer 4?': {'code': 'Ksc4', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Kr - Land use key': {'code': 'Kr', 'units': 'Dmnl', 'inp': True, 'out': True},
                 'Kvert - Vertical hydraulic conductivity semi-confined': {'code': 'Kvert', 'units': 'm/day',
                                                                           'inp': True, 'out': False},
                 'Lc - Canal percolation': {'code': 'Lc#', 'units': 'm3/season/m2', 'inp': True, 'out': False},
                 'Peq - Aquifer effective porosity': {'code': 'Peq', 'units': 'm/m', 'inp': True, 'out': False},
                 'Per - Root zone effective porosity': {'code': 'Per', 'units': 'm/m', 'inp': True, 'out': False},
                 'Pex - Transition zone effective porosity': {'code': 'Pex', 'units': 'm/m', 'inp': True, 'out': False},
                 'Psq - Semi-confined aquifer storativity': {'code': 'Psq', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'Ptq - Aquifer total pore space': {'code': 'Ptq', 'units': 'm/m', 'inp': True, 'out': False},
                 'Ptr - Root zone total pore space': {'code': 'Ptr', 'units': 'm/m', 'inp': True, 'out': False},
                 'Ptx - Transition zone total pore space': {'code': 'Ptx', 'units': 'm/m', 'inp': True, 'out': False},
                 'QH1 - Drain discharge to water table height ratio': {'code': 'QH1#', 'units': 'm/day/m',
                                                                       'inp': True, 'out': False},
                 'QH2 - Drain discharge to sq. water table height ratio': {'code': 'QH2#', 'units': 'm/day/m2',
                                                                           'inp': True, 'out': False},
                 'Qinf - Aquifer inflow': {'code': 'Qinf', 'units': 'm3/season/m2', 'inp': True, 'out': False},
                 'Qout - Aquifer outflow': {'code': 'Qout', 'units': 'm3/season/m2', 'inp': True, 'out': False},
                 'Scale': {'code': 'Scale', 'units': 'Dmnl', 'inp': True, 'out': False},
                 'SL - Soil surface level': {'code': 'SL', 'units': 'm', 'inp': True, 'out': False},
                 'SiU - Surface inflow to non-irrigated': {'code': 'SiU#', 'units': 'm3/season/m2',
                                                           'inp': True, 'out': False},
                 'SdA - Surface outflow crop A': {'code': 'SoA#', 'units': 'm3/season/m2', 'inp': True, 'out': False},
                 'SdB - Surface outflow crop B': {'code': 'SoB#', 'units': 'm3/season/m2', 'inp': True, 'out': False},
                 'SoU - Surface outflow non-irrigated': {'code': 'SoU#', 'units': 'm3/season/m2',
                                                         'inp': True, 'out': False},
                 'It - Total irrigation': {'code': 'It', 'units': 'm3/season/m2', 'inp': False, 'out': True},
                 'Is - Canal irrigation': {'code': 'Is', 'units': 'm3/season/m2', 'inp': False, 'out': True},

                 'FfA - Irrigation efficiency crop A': {'code': 'FfA', 'units': 'Dmnl', 'inp': False, 'out': True},
                 'FfB - Irrigation efficiency crop B': {'code': 'FfB', 'units': 'Dmnl', 'inp': False, 'out': True},
                 'FfT - Total irrigation efficiency': {'code': 'FfT', 'units': 'Dmnl', 'inp': False, 'out': True},
                 'Io - Water leaving by canal': {'code': 'Io', 'units': 'm3/season/m2', 'inp': False, 'out': True},
                 'JsA - Irrigation sufficiency crop A': {'code': 'JsA', 'units': 'Dmnl', 'inp': False, 'out': True},
                 'JsB - Irrigation sufficiency crop B': {'code': 'JsB', 'units': 'Dmnl', 'inp': False, 'out': True},
                 'EaU - Actual evapotranspiration nonirrigated': {'code': 'EaU', 'units': 'm3/season/m2',
                                                                  'inp': False, 'out': True},
                 'LrA - Root zone percolation crop A': {'code': 'LrA', 'units': 'm3/season/m2',
                                                        'inp': False, 'out': True},
                 'LrB - Root zone percolation crop B': {'code': 'LrB', 'units': 'm3/season/m2',
                                                        'inp': False, 'out': True},
                 'LrU - Root zone percolation nonirrigated': {'code': 'LrU', 'units': 'm3/season/m2',
                                                              'inp': False, 'out': True},
                 'LrT - Total root zone percolation': {'code': 'LrT', 'units': 'm3/season/m2', 'inp': False,
                                                       'out': True},
                 'RrA - Capillary rise crop A': {'code': 'RrA', 'units': 'm3/season/m2', 'inp': False, 'out': True},
                 'RrB - Capillary rise crop B': {'code': 'RrB', 'units': 'm3/season/m2', 'inp': False, 'out': True},
                 'RrU - Capillary rise non-irrigated': {'code': 'RrU', 'units': 'm3/season/m2', 'inp': False,
                                                        'out': True},
                 'RrT - Total capillary rise': {'code': 'RrT', 'units': 'm3/season/m2', 'inp': False, 'out': True},
                 'Gti - Trans zone horizontal incoming groundwater': {'code': 'Gti', 'units': 'm3/season/m2',
                                                                      'inp': False, 'out': True},
                 'Gto - Trans zone horizontal outgoing groundwater': {'code': 'Gto', 'units': 'm3/season/m2',
                                                                      'inp': False, 'out': True},
                 'Qv - Net vertical water table recharge': {'code': 'Qv', 'units': 'm', 'inp': False, 'out': True},
                 'Gqi - Aquifer horizontal incoming groundwater': {'code': 'Gqi', 'units': 'm3/season/m2',
                                                                   'inp': False, 'out': True},
                 'Gqo - Aquifer horizontal outgoing groundwater': {'code': 'Gqo', 'units': 'm3/season/m2',
                                                                   'inp': False, 'out': True},
                 'Gaq - Net aquifer horizontal flow': {'code': 'Gaq', 'units': 'm3/season/m2',
                                                       'inp': False, 'out': True},
                 'Gnt - Net horizontal groundwater flow': {'code': 'Gnt', 'units': 'm3/season/m2',
                                                           'inp': False, 'out': True},
                 'Gd - Total subsurface drainage': {'code': 'Gd', 'units': 'm3/season/m2',
                                                    'inp': False, 'out': True},
                 'Ga - Subsurface drainage above drains': {'code': 'Ga', 'units': 'm3/season/m2',
                                                           'inp': False, 'out': True},
                 'Gb - Subsurface drainage below drains': {'code': 'Gb', 'units': 'm3/season/m2',
                                                           'inp': False, 'out': True},
                 'Dw - Groundwater depth': {'code': 'Dw', 'units': 'm', 'inp': False, 'out': True},
                 'Hw - Water table elevation': {'code': 'Hw', 'units': 'm', 'inp': True, 'out': True},
                 'Hq - Subsoil hydraulic head': {'code': 'Hq', 'units': 'm', 'inp': False, 'out': True},
                 'Sto - Water table storage': {'code': 'Sto', 'units': 'm', 'inp': False, 'out': True},
                 'Zs - Surface water salt': {'code': 'Zs', 'units': 'm*dS/m', 'inp': False, 'out': True},
                 'Area A - Seasonal fraction area crop A': {'code': 'A#', 'units': 'Dmnl', 'inp': True, 'out': True},
                 'Area B - Seasonal fraction area crop B': {'code': 'B#', 'units': 'Dmnl', 'inp': True, 'out': True},
                 'Area U - Seasonal fraction area nonirrigated': {'code': 'U', 'units': 'Dmnl', 'inp': False,
                                                                  'out': True},
                 'Uc - Fraction permanently non-irrigated': {'code': 'Uc', 'units': 'Dmnl', 'inp': False, 'out': True},
                 'CrA - Root zone salinity crop A': {'code': 'CrA', 'units': 'dS / m', 'inp': True, 'out': True},
                 'CrB - Root zone salinity crop B': {'code': 'CrB', 'units': 'dS / m', 'inp': True, 'out': True},
                 'CrU - Root zone salinity non-irrigated': {'code': 'CrU', 'units': 'dS / m', 'inp': True, 'out': True},
                 'Cr4 - Fully rotated land irrigated root zone salinity': {'code': 'Cr4', 'units': 'dS / m',
                                                                           'inp': False, 'out': True},
                 'C1 - Key 1 non-permanently irrigated root zone salinity': {'code': 'C1*', 'units': 'dS / m',
                                                                             'inp': False, 'out': True},
                 'C2 - Key 2 non-permanently irrigated root zone salinity': {'code': 'C2*', 'units': 'dS / m',
                                                                             'inp': False, 'out': True},
                 'C3 - Key 3 non-permanently irrigated root zone salinity': {'code': 'C3*', 'units': 'dS / m',
                                                                             'inp': False, 'out': True},
                 'Cxf - Transition zone salinity': {'code': 'Cxf', 'units': 'dS / m', 'inp': True, 'out': True},
                 'Cxa - Transition zone above-drain salinity': {'code': 'Cxa', 'units': 'dS / m', 'inp': True,
                                                                'out': True},
                 'Cxb - Transition zone below-drain salinity': {'code': 'Cxb', 'units': 'dS / m', 'inp': True,
                                                                'out': True},
                 'Cti - Transition zone incoming salinity': {'code': 'Cti', 'units': 'dS / m', 'inp': False,
                                                             'out': True},
                 'Cqf - Aquifer salinity': {'code': 'Cqf', 'units': 'dS / m', 'inp': True, 'out': True},
                 'Cd - Drainage salinity': {'code': 'Cd', 'units': 'ds / m', 'inp': False, 'out': True},
                 'Cw - Well water salinity': {'code': 'Cw', 'units': 'ds / m', 'inp': False, 'out': True},
                 }

# A dictionary to get the variable name from its SAHYSMOD code.
codes_to_vars = dict([(v['code'], k) for (k, v) in vars_SAHYSMOD.items()])

# A list containing only SAHYSMOD input variable codes
SAHYSMOD_input_vars = [v['code'] for v in vars_SAHYSMOD.values() if v['inp']]

# A list containing only SAHYSMOD output variable codes
SAHYSMOD_output_vars = [v['code'] for v in vars_SAHYSMOD.values() if v['out']]


def read_output_file(file_path, n_s, n_p, n_y):
    """

    :param n_y:
    :param file_path:
    :type file_path: str
    :param n_s: Number of seasons per year.
    :type n_s: int
    :param n_p: Number of INTERNAL polygons in the SAHYSMOD model.
    :type n_p: int
    :return:
    :rtype: dict
    """

    dic_data = dict([(k, np.empty((n_s, n_p))) for k in SAHYSMOD_output_vars])

    with open(file_path, 'r') as d:
        l = ''
        while 'YEAR:      %i' % n_y not in l:
            l = d.readline()
        for season in range(n_s):
            for season_poly in range(n_p):  # Read output for the last year's seasons from the output file
                season_poly_output = []  # To hold the output file lines with the desired season
                if n_p == 1 and n_s == 1:
                    poly = [next(d) for _ in range(23)]
                else:
                    poly = [next(d) for _ in range(24)]
                season_poly_output.append(poly)

                for cod in SAHYSMOD_output_vars:
                    var_out = cod.replace('#', '').replace('*', '\*')

                    for line in poly:

                        line += ' '
                        m = re.search(' %s += +([^ ]*)' % var_out, line)

                        if m:
                            val = m.groups()[0]
                            if val == '-':
                                val = -1
                            else:
                                try:
                                    val = float(val)
                                except ValueError:
                                    raise ValueError('The variable "%s" was not read from the SAHYSMOD output.'
                                                     % var_out)
                            dic_data[cod][(season, season_poly)] = val
                            break
    return dic_data


if __name__ == '__main__':
    from pprint import pprint
    pprint(read_output_file(
        'C:\\Users\\jmalar1\\PycharmProjects\\Tinamit\\tinamit\\Ejemplos\\en\\Ejemplo_SAHYSMOD\\test.out',
        n_s=2, n_p=214, n_y=5))
