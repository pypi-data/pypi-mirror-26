# -*- coding: utf-8 -*-

from aiida.orm.calculation.inline import make_inline,optional_inline
from aiida.orm import DataFactory,Node,CalculationFactory
from aiida.backends.djsite.db import models
import numpy as np
from aiida.workflows.user.epfl_theos.dbimporters.utils import objects_set,objects_are_equal


__copyright__ = u"Copyright (c), This file is part of the AiiDA-EPFL Pro platform. For further information please visit http://www.aiida.net/. All rights reserved"
__license__ = "Non-Commercial, End-User Software License Agreement, see LICENSE.txt file."
__version__ = "0.1.0"
__authors__ = "Nicolas Mounet, Gianluca Prandini, Antimo Marrazzo"


UpfData = DataFactory('upf')
ParameterData = DataFactory('parameter')

pseudo_families_libraries_dict = {'pslib.0.3.1_PBE_US': '031US',
                                  'pslib.0.3.1_PBE_PAW': '031PAW',
                                  'pslib.1.0.0_PBE_US': '100US',
                                  'pslib.1.0.0_PBE_PAW': '100PAW',
                                  'pslib.1.0.0_PBE_US_low_acc': '100US_low',
                                  'pslib.1.0.0_PBE_PAW_low_acc': '100PAW_low',
                                  'pslib.orig_PBE_PAW': 'psorigPAW',
                                  'pslib.orig_PBE_US': 'psorigUS',
                                  'GBRV_1.2': 'GBRV-1.2',
                                  'GBRV_1.4': 'GBRV-1.4',
                                  'GBRV_1.5': 'GBRV-1.5',
                                  'SG15': 'SG15',
                                  'SG15_1.1': 'SG15-1.1',
                                  'THEOS': 'THEOS',
                                  'THEOS_alternative': 'THEOS2',
                                  #'RE_100_PAW': '100PAW',
                                  #'RE_100_US': '100US',
                                  'RE_Wentz': 'Wentzcovitch',
                                  'RE_Vander': 'Vanderbilt',
                                  'Goedecker': 'Goedecker',
                                  'Dojo': 'Dojo',
                                  'All_Electrons': 'all_elec',
                                  'All_Electrons_denser': 'all_elec_denser',
                                  'PBE_US_BM': 'BM',
                                  'PBE_US_GIPAW': 'GIPAW',
                                  # Pseudo families for RE nitrides (with THEOS pseudo for N):
                                  'RE_Wentz_plus_nitrogen': 'Wentzcovitch',
                                  'RE_pslib.1.0.0_PBE_US_plus_nitrogen': '100US',
                                  'RE_pslib.1.0.0_PBE_PAW_plus_nitrogen': '100PAW',
                                  }

def get_closest_node(node,aiida_class=Node):
    """
    Function to get the closest node from a given node (in its parents).
    We are not using the transitive closure table here.
    :param node: the node you want to find the closest structure of
    :return: an AiiDA query set
    """
    node_type = aiida_class._query_type_string
    notfound = True
    q_inputs = models.DbNode.aiidaobjects.filter(outputs=node).distinct()
    depth = -1 # to be consistent with the DbPath depth (=0 for direct inputs)
    while notfound and q_inputs.count() > 0:
        depth += 1
        q = q_inputs.filter(type__startswith=node_type)
        notfound = (q.count() == 0)
        inputs = list(q_inputs)
        q_inputs = models.DbNode.aiidaobjects.filter(outputs__in=inputs).distinct()
    return q.distinct().order_by('ctime')

def get_all_children(nodes,*args,**kwargs):
    """
    Get all the children of given nodes
    :param nodes: one node or an iterable of nodes
    :param args & kwargs: additional query parameters
    :return: a list of aiida objects with all the children of the nodes
    """
    try:
        the_nodes = list(nodes)
    except TypeError:
        the_nodes = [nodes]
        
    children = models.DbNode.objects.none()
    q_outputs = models.DbNode.aiidaobjects.filter(inputs__in=the_nodes).distinct()
    while q_outputs.count() > 0:
        outputs = list(q_outputs)
        children = q_outputs | children.all()
        q_outputs = models.DbNode.aiidaobjects.filter(inputs__in=outputs).distinct()
        
    return children.filter(*args,**kwargs).distinct()

def get_kpoint_crystal_coordinates(kpoint_twopi_over_a,cell):
    """
    Transform k-point coordinates given in cartesian and 2pi/alat 
    coordinates, into crystal coordinates
    :param kpoint_twopi_over_a: 3-components vector or list, giving k-point
        in 2pi/a units (cartesian).
    :param cell: cell parameters (3x3 array or list), as coming from 
        structure.cell where structure is an AiiDA structure
    :return: k-point in crystal coordinates (i.e. given on basis of
        reciprocal lattice vectors)
    """
    KpointsData = DataFactory('array.kpoints')
    kpoints = KpointsData()
    kpoints.set_cell(cell)
    alat = np.linalg.norm(cell[0])
    kpoint_angstrom = 2.*np.pi/alat * np.array(kpoint_twopi_over_a)
    kpoints.set_kpoints([kpoint_angstrom], cartesian=True)
    
    return kpoints.get_kpoints()[0]

def birch_murnaghan(V,E0,V0,B0,B1):
    r = (V0/V)**(2./3.)
    return (E0 +
            9./16. * B0 * V0 * (r-1.)**2 * ( 2.+ (B1-4.)*(r-1.)))
    
def fit_birch_murnaghan_params(volumes, energies):
    from scipy.optimize import curve_fit
    
    x = np.array(volumes)
    y = np.array(energies)
    params, covariance = curve_fit(birch_murnaghan, 
                                   xdata=x,
                                   ydata=y,
                                   p0=(y.min(),    #E0
                                       x.mean(),   #V0
                                       0.1,        #B0
                                       3.,         #B1
                                   ),
                                   sigma=None,
                                   maxfev=10000)
    return params, covariance

def pressure_birch_murnaghan(V,V0,B0,B1):
    """
    Pressure from the Birch-Murnaghan equation of state, at a volume V
    """
    x = (V0/float(V))**(1./3.)
    return 3*B0/2. * (x**7-x**5)*(1+3/4.*(B1-4.)*(x**2-1.))
    
def get_volume_from_pressure_birch_murnaghan(P,V0,B0,B1):
    """
    Knowing the pressure P and the Birch-Murnaghan equation of state 
    parameters, gets the volume the closest to V0 (relatively) that is
    such that P_BirchMurnaghan(V)=P
    """
    
    # coefficients of the polynomial in x=(V0/V)^(1/3) (aside from the
    # constant multiplicative factor 3B0/2)
    polynomial = [3./4.*(B1-4.),0,1.-3./2.*(B1-4.),0,3./4.*(B1-4.)-1.,0,
                  0,0,0,-2*P/(3.*B0)]
    V = min([V0/(x.real**3) for x in np.roots(polynomial) 
             if abs(x.imag)<1e-8*abs(x.real)],key=lambda V: abs(V-V0)/float(V0))
    return V

def extract_and_validate_element(structure,error_message_prefix=""):
    """
    Extract the element tested from a structure, and check the 
    structure is correct.
    :param pw_calc: a pw calculation
    :param error_message_prefix: string to be prepended to the error
        message if it occurs.
    :return: the element.
    """
    elements = list(structure.get_symbols_set())
    if len(elements) == 1:
        element = elements[0]
    elif sorted(elements) == ['F','Si']:
        element = 'F'
    elif 'N' in elements and len(elements)==2:
        element = elements[1-elements.index('N')]
    else:
        raise ValueError("{}Incorrect structure; it should be either"
                         " a pure element, or a binary compound "
                         "either made of Si and F, or of N plus "
                         "another element".format(error_message_prefix))
    return element

@optional_inline
def prepare_structure_with_all_atoms_independent_inline(structure):
    """
    Prepare a new structure where all specie get a different kind name,
    e.g. a structure with formula Mo2Te4, with kinds 'Mo' and 'Te', will 
    become a structure with kinds 'Mo1', 'Mo2', 'Te1', 'Te2', 'Te3' and 'Te4'.
    :param structure: a StructureData object
    :return: a dictionary of the form:
        {'indpt_atoms_structure': the_structure}
    """
    the_structure = DataFactory('structure')(cell=structure.cell)
    for i,site in enumerate(structure.sites):
        symbol = structure.get_kind(site.kind_name).symbol
        the_structure.append_atom(position=site.position,symbols=symbol,
            name=symbol+str(1+len([structure.get_kind(_.kind_name).symbol
            for _ in structure.sites[:i]
            if structure.get_kind(_.kind_name).symbol==symbol])))

    return {'indpt_atoms_structure': the_structure}

@optional_inline
def compute_Delta_and_Birch_Murnaghan_EOS_inline(reference_EOS_file,
                                                 reference_structure,**kwargs):
    """
    Compute DeltaFactor (using the DeltaCodesDFT from Cottenier) between
    a reference calculation (typically an all-electron calculation) and
    a set of output_parameters from energy calculations at different 
    volumes (equation of state).
    It also outputs the Birch-Murnaghan fit parameters (bulk modulus,
    equilibrium volume, etc.) from the energy calculations.
    :param reference_EOS_file: SinglefileData with the reference file 
        containing the reference EOS (i.e. Birch-Murnaghan fit parameters),
        for each elemental structure. These will be used for the 
        comparison. Format should be the following:
            - some empty lines or lines beginning with '#'
            - then four columns with
            element     V0(eq. volume[ang^3/atom])  B0(bulk modulus[GPa])  B1(dimensionless)
    :param reference_structure: reference elemental structure
        (the one the reference calculation was computed on)
    :param parameters: (optional, inside kwargs): ParameterData with additional
        parameters, of the form
        {'element': name of the element tested (for compounds, e.g. 
                    rare-earth nitrides - by default the single element
                    of the structure is used)}
    :param kwargs: a dictionary with ParameterData objects as values,
        containing output parameters of pw calculations at various volumes
    
    :return: a dictionary of the form:
        {'output_parameters': ParameterData object with the dictionary:
                {'Birch_Murnaghan_fit_parameters': {
                        'E0': minimum energy, per atom,
                        'E0_units': 'eV/atom',
                        'V0': volume at minimum, per atom,
                        'V0_units': 'ang^3/atom',
                        'B0': bulk modulus,
                        'B0_units': 'GPa',
                        'B1': additional parameter for the fit (dimensionless),
                        },
                  'delta': delta factor,
                  'delta_units': 'eV',
                  'element': name of the element,
                  'number_of_atoms': number of atoms in the elemental structure,
                  'pseudo_md5': md5sum of the pseudo,
                  }
         }
    """
    from pymatgen.analysis.structure_matcher import StructureMatcher
    from calcDelta import calcDelta
    from itertools import chain
    from aiida.backends.djsite.db import models
    
    # 'exact' structure matcher, except for a possible scaling:
    sm = StructureMatcher(1e-8,1e-8,1e-8,scale=True)
    
    element = list(reference_structure.get_symbols_set())[0]
    try:
        element = kwargs.pop('parameters').get_dict()['element']
    except KeyError:
        if len(reference_structure.get_symbols_set())>1:
            raise ValueError("You need to pass 'parameters' with the name "
                             "of the element tested, for a compound")
       
    energies = []
    volumes = []
    ref_structure_pymat = reference_structure.get_pymatgen_structure()
    for k,calc_params in kwargs.iteritems():
        if not isinstance(calc_params,ParameterData):
            raise TypeError("Input with key {} should be of type "
                             "ParameterData".format(k))
        calc_output_dict = calc_params.get_dict()
        try:
            structure = calc_params.inp.output_parameters.out.output_structure
        except AttributeError:
            structure = calc_params.inp.output_parameters.inp.structure
            
        # compare structure with reference
        if not sm.fit(ref_structure_pymat,structure.get_pymatgen_structure()):
            raise ValueError("Cif and structure from the energy "
                              "calculation {} do not correspond"
                              "".format(calc_params.inp.output_parameters.pk))
        
        energies.append(calc_output_dict['energy'])
        volumes.append(calc_output_dict['volume'])
        # extract pseudo library
        pseudo_md5s_tmp = sorted(list(set([u.md5sum 
                        for u in calc_params.inp.output_parameters.get_inputs(
                                                        UpfData)])))
        pseudo_md5_element = [u.md5sum for u in calc_params.inp.output_parameters.get_inputs(
                                    UpfData) if u.element==element]
        if len(pseudo_md5_element) != 1:
            raise ValueError("Too few or too many pseudos used for element {}".format(element))
        if len(pseudo_md5s_tmp) != len(reference_structure.get_symbols_set()):
            raise ValueError("Too few or too many pseudo families used in "
                              "energy calculation {}"
                              "".format(calc_params.inp.output_parameters.pk))
        try:
            if (pseudo_md5s_tmp != pseudo_md5s):
                raise ValueError("The pseudo families used in energy "
                                  "calculations should all be the same")
        except NameError:
            pseudo_md5s = pseudo_md5s_tmp
        # extract number of atoms
        try:
            if calc_output_dict['number_of_atoms'] != natoms:
                raise ValueError("Structures in energy calculations "
                                  "should all have the same number of atoms")
        except NameError:
            natoms = calc_output_dict['number_of_atoms']
    
    volumes, energies = zip(*sorted(zip(volumes, energies)))
    fit_params, covariance = fit_birch_murnaghan_params(volumes, energies)
    E0 = fit_params[0]/natoms # eV/atom
    V0 = fit_params[1]/natoms # A^3/atom
    B0 = fit_params[2]*160.2176487 # GPa
    B1 = fit_params[3]
    
    output_dict = {'Birch_Murnaghan_fit_parameters': {
                        'E0': E0,
                        'E0_units': 'eV/atom',
                        'V0': V0,
                        'V0_units': 'ang^3/atom',
                        'B0': B0,
                        'B0_units': 'GPa',
                        'B1': B1,
                        },
                    'number_of_atoms': natoms,
                    'element': element,
                    'pseudo_md5': pseudo_md5_element[0],
                    }
    
    # now compute the Delta factor
    # calcDelta parameter
    useasymm = False
    # read reference file
    ref_file_path = reference_EOS_file.get_file_abs_path()
    try:
        data_ref = np.loadtxt(ref_file_path, 
            dtype={'names': ('element', 'V0', 'B0', 'BP'),
            'formats': ('S2', np.float, np.float, np.float)})
    except IOError as e:
        raise IOError("Cannot read the reference file {}: {}"
                       "".format(ref_file_path,e.message))
    # build array with the data to be compared to the reference
    data_tested = np.array([(element,V0,B0,B1)], dtype={
                        'names': ('element', 'V0', 'B0', 'BP'),
                        'formats': ('S2', np.float, np.float, np.float),
                        })
    eloverlap = list(set(data_tested['element']) & set(data_ref['element']))
    if not eloverlap:
        raise ValueError("Element {} is not present in the reference set"
                          "".format(element))
    # Delta computation
    Delta, Deltarel, Delta1 = calcDelta(data_tested, data_ref,
                                        eloverlap, useasymm)
    # Delta is in meV/atom here -> convert to eV/atom
    output_dict['delta'] = Delta[0]/1000.
    output_dict['delta_units'] = 'eV/atom'
    
    return {'output_parameters': ParameterData(dict=output_dict)}

def get_compute_Delta_and_Birch_Murnaghan_EOS_results(reference_EOS_file,
                                                      reference_structure,
                                                      store=True,**kwargs):
    """
    Get the results from the compute_Delta_and_Birch_Murnaghan_EOS_inline
    function:
    - if there exists already an inline calculation with the same input
    structure, the same input reference file, and the same pw output
    parameters, it does not relaunch it, it gets instead 
    the output dictionary of the previously launched function,
    - otherwise, launches the compute_Delta_and_Birch_Murnaghan_EOS_inline
    function and gets its result.
    """
    from aiida.orm.calculation.inline import InlineCalculation
    
    result_dict = None
    for ic in reference_structure.get_outputs(InlineCalculation):
        try:
            if ( ic.get_function_name() == 'compute_Delta_and_Birch_Murnaghan_EOS_inline'
                 and reference_EOS_file.uuid == ic.inp.reference_EOS_file.uuid
                 and all([any([objects_are_equal(p_ic.get_dict(),p.get_dict())
                               for p in kwargs.values()])
                          for p_ic in ic.get_inputs(ParameterData)])
                 and all([any([objects_are_equal(p_ic.get_dict(),p.get_dict())
                               for p_ic in ic.get_inputs(ParameterData)])
                          for p in kwargs.values()])
                 and 'output_parameters' in ic.get_outputs_dict() ):
                result_dict = ic.get_outputs_dict()
        except AttributeError:
            pass
    
    if result_dict is not None:
        print " compute_Delta_and_Birch_Murnaghan_EOS already run with "\
               "the same inputs -> we do not re-run"
    else:
        print "Launch compute_Delta_and_Birch_Murnaghan_EOS ... "
        result_dict = compute_Delta_and_Birch_Murnaghan_EOS_inline(
                    reference_EOS_file=reference_EOS_file,
                    reference_structure=reference_structure,
                    store=store,**kwargs)
    return result_dict

@optional_inline
def build_info_inline(**kwargs):
    """
    Inline function to build a ParameterData objection containing
    the most important information from the calculations on a given 
    element, with a given pseudo and certain cutoffs.
    This information can then easily be printed into a .info file (SSSP-like).
    .. note:: Not all the input parameters are required. If some are missing,
    the corresponding field are left with 'None'.
    :param parameters_delta: ParameterData object containing the delta info
        (output of prepare_structure_with_all_atoms_independent_inline)
    :param parameters_phonon_bulk: ParameterData object with the output
        parameters of a phonon calculation on the bulk
    :param parameters_energy_bulk: ParameterData object with the output
        parameters of an energy calculation on the bulk
    :param parameters_energy_gas_%d: (with %d an integer) ParameterData
        object(s) with the output parameters of energy calculation(s) on
        an isolated atom. There should be as many as the number of species
        in the bulk (to compute its cohesive energy)
    :param parameters_stress: ParameterData object with the output
        parameters of a stress calculation on the bulk
        (if not present it tries to find the stress inside 'parameters_energy_bulk')
    :return: a dictionary of the form
        {'output_parameters': ParameterData with the following dictionary:
            {'element': the element tested (i.e. in pure elemental bulk,
                    it's just the element, in SiF4, it's F, and in
                    rare-earths compounds with nitrogen, it's the rare-earth),
             'wfc_cutoff': wave-functions energy cutoff
             'wfc_cutoff_units': 'Ry',
             'dual': ratio between charge density and wave-function
                    energy cutoffs,
             'q-point': q-point where the phonon frequencies were evaluated,
             'q-point_units': 'crystal',
             'phonon_frequencies': phonon frequencies at this q-point,
             'phonon_frequencies_units': 'cm-1',
             'pressure': hydrostatic pressure computed from the trace of 
                         the stress tensor of the bulk computation,
             'pressure_units': 'GPa',
             'cohesive_energy': cohesive energy of the bulk w.r.t 
                                the isolated system(s),
             'cohesive_energy_units': 'meV/atom',
             'delta': delta factor w.r.t to Cottenier WIEN2k computations,
             'delta_units': 'meV/atom',
             'Z': number of valence electrons of the pseudo,
             'V0': equilibrium volume for the bulk,
             'V0_units': 'ang^3/atom',
             'B0': bulk modulus,
             'B0_units': 'GPa',
             'B1': B1 (or BP, or B01) fit parameters in the 
                   Birch-Murnaghan eq. of state of the bulk (dimensionless),
             'pseudo_md5': md5sum of the pseudo used for the element tested.
             }
         }
    """
    from aiida.common.constants import ry_to_ev,invcm_to_THz
    
    def extract_and_validate_pseudo(pw_calc,element,error_message_prefix=""):
        """
        Extract the pseudos for a given element, and check they are the
        same.
        :param pw_calc: a pw calculation
        :param element: the element name
        :param error_message_prefix: string to be prepended to the error
            message if it occurs.
        :return: the md5 of the pseudo file.
        """
        pseudos = pw_calc.get_inputs(UpfData)
        pseudo_md5s = set([u.md5sum for u in pseudos
                           if u.element==element])
        if len(pseudo_md5s) > 1:
            raise ValueError("{}Too many different pseudos "
                             "for element {} (there should be only one)"
                             "".format(error_message_prefix,element))
        return list(pseudo_md5s)[0]

    def extract_and_validate_cutoff_dual(pw_calc,error_message_prefix=""):
        """
        Extract the wave-function energy cutoff and the dual from a PW
        calculation, and check the units.
        :param pw_calc: a pw calculation
        :param error_message_prefix: string to be prepended to the error
            message if it occurs.
        :return: the element.
        """
        wfc_cutoff = pw_calc.res.wfc_cutoff
        rho_cutoff = pw_calc.res.rho_cutoff
        if pw_calc.res.wfc_cutoff_units == 'eV':
            wfc_cutoff /= ry_to_ev
        elif pw_calc.res.wfc_cutoff_units != 'Ry':
            raise ValueError("{}Improper units for wfc_cutoff (eV or Ry"
                              " are required)".format(error_message_prefix))
        if pw_calc.res.rho_cutoff_units == 'eV':
            rho_cutoff /= ry_to_ev
        elif pw_calc.res.rho_cutoff_units != 'Ry':
            raise ValueError("{}Improper units for rho_cutoff (eV or Ry"
                              " are required)".format(error_message_prefix))
        dual = rho_cutoff/wfc_cutoff
        return wfc_cutoff,dual
    
    
    keys = ['element','wfc_cutoff','dual','q-point','phonon_frequencies',
            'pressure','cohesive_energy','delta','Z','V0','B0','B1',
            'pseudo_md5']
    unit_keys = ['{}_units'.format(key) for key in keys 
                 if key not in ['element','dual','Z','B1','pseudo_md5']]
    unit_values = ['meV/atom' if key in ['delta_units','cohesive_energy_units']
                   else 'cm-1' if key=='phonon_frequencies_units'
                   else 'GPa' if key in ['pressure_units','B0_units']
                   else 'ang^3/atom' if key=='V0_units'
                   else 'Ry' if key=='wfc_cutoff_units'
                   else 'crystal'
                   for key in unit_keys]
    output_dict = dict([(unit_key,unit_value) for unit_key,unit_value
                        in zip(unit_keys,unit_values)])
    
    parameters_delta = kwargs.pop('parameters_delta',None)
    if parameters_delta:
        # extract info from the delta parameters
        delta_dict = parameters_delta.get_dict()
        output_dict['element'] = delta_dict['element']
        output_dict['pseudo_md5'] = delta_dict['pseudo_md5']
        
#        # Temporary fix (to be deleted!) 
#        inp_params_delta = parameters_delta.inp.output_parameters.get_inputs_dict()
#        for k,v in inp_params_delta.iteritems():
#            if type(v)==ParameterData:
#                pw_delta_calc = v.inp.output_parameters
#                break
#        output_dict['pseudo_md5']  = extract_and_validate_pseudo(pw_delta_calc,output_dict['element'],
#                                                                 error_message_prefix="Delta calc.: ")

        # extract delta
        output_dict['delta'] = delta_dict['delta']
        if delta_dict['delta_units'] == 'eV/atom':
            output_dict['delta'] *= 1000.
        elif delta_dict['delta_units'] != output_dict['delta_units']:
            raise ValueError("Delta parameters: Improper units for delta"
                              " (eV/atom or {} are required)"
                              "".format(output_dict['delta_units']))
        # extract volume
        output_dict['V0'] = delta_dict['Birch_Murnaghan_fit_parameters']['V0']
        if (delta_dict['Birch_Murnaghan_fit_parameters']['V0_units']
            != output_dict['V0_units']):
            raise ValueError("Delta parameters: Improper units for V0 "
                              "({} are required)".format(output_dict['V0_units']))
        # extract other Birch-Murnaghan fit parameters
        output_dict['B0'] = delta_dict['Birch_Murnaghan_fit_parameters']['B0']
        output_dict['B1'] = delta_dict['Birch_Murnaghan_fit_parameters']['B1']
        if (delta_dict['Birch_Murnaghan_fit_parameters']['B0_units']
            != output_dict['B0_units']):
            raise ValueError("Delta parameters: Improper units for B0 "
                              "({} are required)".format(output_dict['B0_units']))
        
    parameters_phonon_bulk = kwargs.pop('parameters_phonon_bulk',None)
    if parameters_phonon_bulk:
        # extract info from the phonon calculation output parameters
        phonon_dict = parameters_phonon_bulk.get_dict()
        dynmats = [v for k,v in phonon_dict.iteritems()
                   if k.startswith('dynamical_matrix')]
        if len(dynmats) != 1:
            raise ValueError("Phonon calc.: Too many or too few "
                              "dynamical matrices")
        dynmat_dict = dynmats[0]
        # extract q-point (in 2pi/a cartesian coordinates)
        qpoint_2piovera = dynmat_dict['q_point']
        if (phonon_dict.get('q_point_units','2pi/lattice_parameter')
            != '2pi/lattice_parameter'):
            raise ValueError("Phonon calc.: Improper units for q-point "
                              "(2pi/lattice_parameter are required)")
        # find pw calc and structure
        pw_calc = get_closest_node(parameters_phonon_bulk,
            aiida_class=CalculationFactory('quantumespresso.pw')).first()
        try:
            structure = pw_calc.out.output_structure
        except AttributeError:
            structure = pw_calc.inp.structure
        # translate q-point into crystal coordinates
        output_dict['q-point'] = get_kpoint_crystal_coordinates(
                                        qpoint_2piovera,structure.cell).tolist()
        # extract frequencies
        output_dict['phonon_frequencies'] = dynmat_dict['frequencies']
        
        if dynmat_dict.get('frequencies_units','cm-1') == 'THz':
            output_dict['phonon_frequencies'] /= invcm_to_THz
        elif dynmat_dict.get('frequencies_units','cm-1') != 'cm-1':
            raise ValueError("Phonon calc.: Improper units for "
                              "phonon freq. (THz or {} are required)"
                              "".format(output_dict['phonon_frequencies_units']))
        # find cutoffs
        output_dict['wfc_cutoff'],output_dict['dual'] = \
            extract_and_validate_cutoff_dual(pw_calc,
                                error_message_prefix="Phonon calc.: ")
        # find element
        element = extract_and_validate_element(structure,
                                error_message_prefix="Phonon calc.: ")
        try:
            if element != output_dict['element']:
                raise ValueError("The same element should be tested in "
                                 "the delta and phonon calculations")
        except KeyError:
            output_dict['element'] = element
        # find pseudo
        pseudo_md5 = extract_and_validate_pseudo(pw_calc,element,
                                error_message_prefix="Phonon calc.: ")
        try:
            if pseudo_md5 != output_dict['pseudo_md5']:
                raise ValueError("The same pseudo for element {} should"
                                 " be used in the delta and phonon "
                                 "calculations".format(element))
        except KeyError:
            output_dict['pseudo_md5'] = pseudo_md5
    
    parameters_stress = kwargs.pop('parameters_stress',None)
    if parameters_stress:
        # extract info from the bulk energy calculation output parameters
        pw_dict = parameters_stress.get_dict()
        pw_stress_calc = parameters_stress.inp.output_parameters
        try:
            structure_bulk = pw_stress_calc.out.output_structure
        except AttributeError:
            structure_bulk = pw_stress_calc.inp.structure
        # find cutoffs
        wfc_cutoff,dual = extract_and_validate_cutoff_dual(pw_stress_calc,
                            error_message_prefix="Energy bulk calc.: ")
        try:
            if (wfc_cutoff != output_dict['wfc_cutoff'] or
                dual != output_dict['dual']):
                raise ValueError("The same cutoff and dual should be "
                                 "tested in the phonon and energy calculations")
        except KeyError:
            output_dict['wfc_cutoff'] = wfc_cutoff
            output_dict['dual'] = dual
        # find tested element, and all the atoms
        element = extract_and_validate_element(structure_bulk,
                            error_message_prefix="Energy bulk calc.: ")
        bulk_atoms = [structure_bulk.get_kind(kind_name).symbols[0]
                      for kind_name in structure_bulk.get_site_kindnames()]
        try:
            if element != output_dict['element']:
                raise ValueError("The same element should be tested in "
                                 "the delta, phonon and energy calculations")
        except KeyError:
            output_dict['element'] = element
        # find tested pseudo
        pseudo_md5 = extract_and_validate_pseudo(pw_stress_calc,element,
                            error_message_prefix="Energy bulk calc.: ")
        try:
            if pseudo_md5 != output_dict['pseudo_md5']:
                raise ValueError("The same pseudo for element {} should"
                                 " be used in the delta, phonon, and energy"
                                 " calculations".format(element))
        except KeyError:
            output_dict['pseudo_md5'] = pseudo_md5
        # extract energy and pressure
        bulk_energy = pw_dict['energy']
        if pw_dict['energy_units'] != 'eV':
            raise ValueError("Energy bulk calc.: Improper units for the"
                             " the energy (eV required)")
        output_dict['pressure'] = np.trace(pw_dict['stress'])/3.
        if pw_dict['stress_units'] not in ['GPa','GPascal']:
            raise ValueError("Energy bulk calc.: Improper units for the"
                                  " the stress (GPa required)")
            
    parameters_energy_bulk = kwargs.pop('parameters_energy_bulk',None)
    if parameters_energy_bulk:
        # extract info from the bulk energy calculation output parameters
        pw_dict = parameters_energy_bulk.get_dict()
        pw_bulk_calc = parameters_energy_bulk.inp.output_parameters
        try:
            structure_bulk = pw_bulk_calc.out.output_structure
        except AttributeError:
            structure_bulk = pw_bulk_calc.inp.structure
        # find cutoffs
        wfc_cutoff,dual = extract_and_validate_cutoff_dual(pw_bulk_calc,
                            error_message_prefix="Energy bulk calc.: ")
        try:
            if (wfc_cutoff != output_dict['wfc_cutoff'] or
                dual != output_dict['dual']):
                raise ValueError("The same cutoff and dual should be "
                                 "tested in the phonon and energy calculations")
        except KeyError:
            output_dict['wfc_cutoff'] = wfc_cutoff
            output_dict['dual'] = dual
        # find tested element, and all the atoms
        element = extract_and_validate_element(structure_bulk,
                            error_message_prefix="Energy bulk calc.: ")
        bulk_atoms = [structure_bulk.get_kind(kind_name).symbols[0]
                      for kind_name in structure_bulk.get_site_kindnames()]
        try:
            if element != output_dict['element']:
                raise ValueError("The same element should be tested in "
                                 "the delta, phonon and energy calculations")
        except KeyError:
            output_dict['element'] = element
        # find tested pseudo
        pseudo_md5 = extract_and_validate_pseudo(pw_bulk_calc,element,
                            error_message_prefix="Energy bulk calc.: ")
        try:
            if pseudo_md5 != output_dict['pseudo_md5']:
                raise ValueError("The same pseudo for element {} should"
                                 " be used in the delta, phonon, and energy"
                                 " calculations".format(element))
        except KeyError:
            output_dict['pseudo_md5'] = pseudo_md5
        # extract energy and pressure
        bulk_energy = pw_dict['energy']
        if pw_dict['energy_units'] != 'eV':
            raise ValueError("Energy bulk calc.: Improper units for the"
                             " the energy (eV required)")
        if not parameters_stress and 'stress' in pw_dict:
            output_dict['pressure'] = np.trace(pw_dict['stress'])/3.
            if pw_dict['stress_units'] not in ['GPa','GPascal']:
                raise ValueError("Energy bulk calc.: Improper units for the"
                                  " the stress (GPa required)")
    
        # extract info from the gas energy calculation(s) output parameters
        # (if any)
        cohesive_energy = bulk_energy
        for parameters_key in [k for k in kwargs.keys()
                                if k.startswith('parameters_energy_gas_')]:
            parameters_energy_gas = kwargs.pop(parameters_key)
            pw_gas_calc = parameters_energy_gas.inp.output_parameters
            try:
                structure_gas = pw_gas_calc.out.output_structure
            except AttributeError:
                structure_gas = pw_gas_calc.inp.structure
            # find cutoffs
            wfc_cutoff,dual = extract_and_validate_cutoff_dual(pw_gas_calc,
                    error_message_prefix="Energy gas calc. {}: ".format(
                                                        parameters_key))
            if (wfc_cutoff != output_dict['wfc_cutoff'] or
                dual != output_dict['dual']):
                raise ValueError("The same cutoff and dual should be "
                                 "tested in all calculations")
            # check the structure
            if (len(structure_gas.sites)>1 
                or any([np.linalg.norm(v)<10. for v in structure_gas.cell])
                or structure_gas.kinds[0].symbols[0] not in bulk_atoms):
                raise ValueError("Energy gas calc. {}: incorrect structure"
                                  "".format(parameters_key))
            element = structure_gas.kinds[0].symbols[0]
            # find pseudo and compare with the corresponding bulk pseudo
            pseudo_md5 = extract_and_validate_pseudo(pw_gas_calc,element,
                            error_message_prefix="Energy gas calc. {}: "
                                                "".format(parameters_key))
            bulk_pseudo_md5 = extract_and_validate_pseudo(pw_bulk_calc,
                    element,error_message_prefix="Energy bulk calc. {}: ")
            if pseudo_md5 != bulk_pseudo_md5:
                raise ValueError("The same pseudo for element {} should"
                                 " be used in the bulk and gas calculations"
                                 "".format(element))
            # extract energy
            pw_dict = parameters_energy_gas.get_dict()
            gas_energy = pw_dict['energy']
            if pw_dict['energy_units'] != 'eV':
                raise ValueError("Energy gas calc. {}: Improper units for the"
                                 " the energy (eV required)".format(
                                 parameters_key))
            cohesive_energy -= gas_energy*bulk_atoms.count(element)
            for _ in range(bulk_atoms.count(element)):
                bulk_atoms.pop(bulk_atoms.index(element))
        
        # if there are some remaining atoms in the bulk, the cohesive 
        # energy cannot be computed
        if not bulk_atoms:
            output_dict['cohesive_energy'] = cohesive_energy*1000./float(len(structure_bulk.sites))
        
    if kwargs:
        raise ValueError("Too many input parameters")
    
    # extract the number of valence electrons from the pseudo
    pseudo = UpfData.query(dbattributes__in=models.DbAttribute.objects.filter(
                           key='md5',tval=output_dict['pseudo_md5'])).first()
    with open(pseudo.get_file_abs_path(),'r') as f:
        lines=f.readlines()
        for line in lines:
            if 'valence' in line:
                try:
                    output_dict['Z'] = int(float(line.split("z_valence=\""
                                            )[-1].split("\"")[0].strip()))
                except (ValueError, IndexError):
                    try:
                        output_dict['Z'] = int(float(line.split("Z"
                                                            )[0].strip()))
                    except (ValueError, IndexError):
                        pass
    
    output_dict.update(dict([(key,None) for key in keys
                             if output_dict.get(key,None) is None]))

    return {'output_parameters': ParameterData(dict=output_dict)}

def get_build_info_results(store=True,**kwargs):
    """
    Get the results from the build_info_inline function:
    - if there exists already an inline calculation with the same inputs,
    it does not relaunch it, it gets instead 
    the output dictionary of the previously launched function,
    - otherwise, launches the build_info_inline
    function and gets its result.
    """
    from aiida.orm.calculation.inline import InlineCalculation

    result_dict = None
    params = kwargs.values()[0]
    for ic in params.get_outputs(InlineCalculation):
        try:
            if ( ic.get_function_name() == 'build_info_inline'
                 and all([any([objects_are_equal(p_ic.get_dict(),p.get_dict())
                               for p in kwargs.values()])
                          for p_ic in ic.get_inputs(ParameterData)])
                 and all([any([objects_are_equal(p_ic.get_dict(),p.get_dict())
                               for p_ic in ic.get_inputs(ParameterData)])
                          for p in kwargs.values()])
                 and 'output_parameters' in ic.get_outputs_dict() ):
                result_dict = ic.get_outputs_dict()
        except AttributeError:
            pass
     
    if result_dict is not None:
        print "build_info already run with "\
               "the same inputs -> we do not re-run"
        created = False
    else:
        print "Launch build_info ... "
        result_dict = build_info_inline(store=store,**kwargs)
        created = True
    return result_dict,created

def write_info_file(filepath,parameters_info):
    """
    Write into a file all the info contained in the dictionary of
    parameters_info, plus its uuid in the header.
    :param filepath: full path of the file to write
    :param parameters_info: ParameterData object with a dictionary
        containing all the info
    """
    info_dict = parameters_info.get_dict()
    with open(filepath,'w') as f:
        f.write("### INFO from parameters with uuid {}\n".format(
                                            parameters_info.uuid))
        pseudo = UpfData.query(dbattributes__in=models.DbAttribute.objects.filter(
                               key='md5',tval=info_dict.pop('pseudo_md5'))).first()
        pseudo_library = pseudo_families_libraries_dict[pseudo.get_upf_family_names()[0]]
        for key in sorted([k for k in info_dict.keys()
                           if not k.endswith('_units')]):
            value = info_dict[key]
            if info_dict.get("{}_units".format(key),None):
                f.write("#{} [{}]\n".format(key.upper(),info_dict["{}_units".format(key)]))
            else:
                f.write("#{}\n".format(key.upper()))
            if isinstance(value,basestring):
                f.write("{}\n".format(value))
            else:
                try:
                    f.write("{}\n".format(" ".join([str(v) for v in value])))
                except TypeError:
                    f.write("{}\n".format(value))
        f.write("#PSEUDO_LIBRARY\n")
        f.write("{}\n".format(pseudo_library))
    
def read_info_file(filepath):
    """
    Read an info file and put all the data in a dictionary
    .. note:: The format of the file should be:
            ### possible header (ignored)
            # KEY1 [key1_units]
            value1
            # KEY2
            value2
        which becomes:
            {key1: value1,
             key1+'_units': key1_units,
             key2: value2}
    
    .. note:: all the keys are set to lower case in the return dictionary.

    :param ilepath: full path of the file to read.        
    :return: a dictionary with all the info.
    """
    info_dict = {}
    with open(filepath,'r') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            if i==0 and line.startswith('###'):
                # this is the header line -> ignored
                continue
            if line.startswith('#'):
                key = line.split('#')[-1].split()[0].lower()
                if key in ['b0','b1','v0','z']:
                    key = key.upper()
                try:
                    value_unit = line.split('[')[1].split(']')[0]
                except IndexError:
                    value_unit = None
                
                value = lines[i+1]
                try:
                    the_value = [int(v) for v in value.split()]
                except ValueError:
                    try:
                        the_value = [float(v) for v in value.split()]
                    except ValueError:
                        the_value = value.split()
                if len(the_value)==1:
                    the_value = the_value[0]
                if the_value=='None':
                    the_value = None
                info_dict[key] = the_value
                if value_unit:
                    info_dict["{}_units".format(key)] = value_unit
                    
    return info_dict

@optional_inline
def rescale_inline(parameters,structure):
    """
    Inline calculation to rescale a structure
    .. note:: in the case of the O / Cr and Mn structures, it also makes them 
    antiferromagnetic (each atom gets a different kind name)
    :param parameters: a ParameterData object with a dictionary of the form
        {'scaling_ratio': 1.02} (here for a 2% volume expansion)
    :param structure: an AiiDA structure to rescale
    :return: a dictionary of the form
        {'rescaled_structure': new_rescaled_structure}
    """

    scaling_ratio = (parameters.get_dict()['scaling_ratio'])**(1./3.)
    the_ase = structure.get_ase()
    positions = the_ase.get_positions()
    symbols = the_ase.get_chemical_symbols()
   
    if symbols[0] in ['O','Cr','Mn']:
        StructureData = DataFactory('structure')
        new_structure = StructureData(cell=the_ase.get_cell()*scaling_ratio)
        for i in range(len(symbols)):
            new_structure.append_atom(position=positions[i]*scaling_ratio,symbols=symbols[i],name=symbols[i]+str(i+1))
            
    else:
        new_ase = the_ase.copy()
        new_ase.set_cell(the_ase.get_cell()*scaling_ratio,scale_atoms=True)
        new_structure = DataFactory('structure')(ase=new_ase)

    return {'rescaled_structure': new_structure}

def get_rescale_results(parameters=None,structure=None, store=True):

    """
    Get the results from the rescale_inline function:
    - if there exists already an inline calculation with the same inputs,
    it does not relaunch it, it gets instead the output dictionary of the previously
    launched function,
    - otherwise, launches the rescale structure function
    and get its result.
    """
    from aiida.orm.calculation.inline import InlineCalculation
    from aiida.workflows.user.epfl_theos.dbimporters.utils import objects_are_equal

    result_dict = None
    for ic in InlineCalculation.query(inputs=structure).order_by('ctime'):
        try:
            if ( ic.get_function_name() == 'rescale_inline'
                 and objects_are_equal(ic.inp.parameters.get_dict(), parameters.get_dict())
                 and ic.inp.structure.pk == structure.pk
                 and 'rescaled_structure' in ic.get_outputs_dict()):
                result_dict = ic.get_outputs_dict()
        except AttributeError:
            pass

    if result_dict is not None:
        print " rescale_inline already run -> we do not re-run"
    else:
        print "Launch rescale_inline..."
        result_dict = rescale_inline(parameters=parameters,
                                    structure=structure,
                                    store=store)
    return result_dict

@optional_inline
def bands_distance_info_inline(**kwargs):
    """
    Inline function to build a ParameterData containing the bands distances between a reference
    cutoff and a list of cutoffs.
    :param bands_distance_parameters_%d: (with %d an integer) ParameterData
        object(s) with the output parameters of inline function 'bands_distance_inline'
    :return: a dictionary of the form
        {'output_parameters': ParameterData with the following dictionary:
            {'distance_%cutoff_%reference-cutoff_Ry': dictionaries with the results of the bands distance calculation
                         between two band structures with cutoffs %cutoff and %reference-cutoff (given in Rydberg)
            }
        }
    """
    
    output_dict = {}
    for parameters_key in [k for k in kwargs.keys()
                                if k.startswith('bands_distance_parameters_')]:

        results_bands_distance = kwargs.pop(parameters_key)
        cutoff = results_bands_distance.inp.output_parameters.inp.bandsdata1.inp.output_band.res.wfc_cutoff
        max_cutoff = results_bands_distance.inp.output_parameters.inp.bandsdata2.inp.output_band.res.wfc_cutoff
        cutoff = int( round( cutoff / 13.605698066) )
        max_cutoff = int( round( max_cutoff / 13.605698066) )
        output_dict['distance_{}_{}_Ry'.format(cutoff, max_cutoff)] = \
                    results_bands_distance.get_dict()['results']            
    return {'output_parameters': ParameterData(dict=output_dict)}

def get_bands_distance_info_results(store=True, **kwargs):

    """
    Get the results from the bands_distance_info_inline function:
    - if there exists already an inline calculation with the same inputs,
    it does not relaunch it, it gets instead the output dictionary of the previously
    launched function,
    - otherwise, launches the bands distance info function
    and get its result.
    """
    from aiida.orm.calculation.inline import InlineCalculation
    from aiida.workflows.user.epfl_theos.dbimporters.utils import objects_are_equal
    
    result_dict = None
    params = kwargs.values()[0]
    for ic in params.get_outputs(InlineCalculation):
        try:
            if ( ic.get_function_name() == 'bands_distance_info_inline'
                 and all([any([objects_are_equal(p_ic.get_dict(),p.get_dict())
                               for p in kwargs.values()])
                          for p_ic in ic.get_inputs(ParameterData)])
                 and all([any([objects_are_equal(p_ic.get_dict(),p.get_dict())
                               for p_ic in ic.get_inputs(ParameterData)])
                          for p in kwargs.values()])
                 and 'output_parameters' in ic.get_outputs_dict() ):
                result_dict = ic.get_outputs_dict()
        except AttributeError:
            pass
    
    if result_dict is not None:
        print "bands_distance_info already run with "\
               "the same inputs -> we do not re-run"
        created = False
    else:
        print "Launch bands distance info ... "
        result_dict = bands_distance_info_inline(store=store,**kwargs)
        created = True
    return result_dict,created

@optional_inline    
def bands_distance_inline(parameters,bandsdata1,bandsdata2):
    """
    Inline function to build a ParameterData objection containing
    the bands distance between two band structures calculated on an 
    uniform k-points mesh.
    
    To use this function run first the bash script 'efermi_f2py_make.sh' 
    in the folder where 'efermi.f' and 'efermi.pyf' are in order to create 
    the module efermi_module.
    
    :param parameters: ParameterData object containing the parameters of the
        bands distance calculation. It contains a dictionary of the form:
            {
              'smearing': smearing in Fermi-Dirac function used for the bands distance calculation [eV],
              'nspin': spin degeneracy: 2 or 1,
              'input_nelec': set to True if the number of electrons is specified by the user,
              'nelec': user-specified number of electrons,
            }
    :param bandsdata1: BandsData object with the band structure
        obtained on an uniform k-points mesh (no symmetries allowed)
    :param bandsdata2: BandsData object with the reference band structure
        obtained on an uniform k-points mesh (no symmetries allowed)
    :return a dictionary of the form
        {'output_parameters': ParameterData with the following dictionary:
           'warnings': list of warnings messages,
           'results':{
                      'eta_v': bands distance up to the Fermi energy [eV],
                      'eta_10': bands distance up to 10 eV above the Fermi energy [eV],
                      'max_v': maximum value of the eigenvalues difference in eta_v [eV],
                      'max_10': maximum value of the eigenvalues difference in eta_10 [eV],
                      'shift_v': energy shift for bands allignement in eta_v [eV],
                      'shift_10': energy shift for bands allignement in eta_10 [eV],
                      }
        }
    """
 
    import math
    import numpy as np
    from aiida.workflows.user.epfl_theos.quantumespresso.efermi_module import efermi
    from scipy.optimize import minimize
    from functools import partial
    
    warnings = []
    params = parameters.get_dict()
    
    try:
        smearing = params['smearing']
    except KeyError:
        smearing = 0.2721 # [eV] ==> 0.02 Ry
    try:
        nspin = params['nspin']
    except KeyError:
        nspin = 2
    try:
        input_nelec = params['input_nelec']
    except KeyError:
        input_nelec = False
    try:
        nelec = params['nelec']
    except KeyError:
        nelec = 0.0
    try:
        metal = params['metal']
    except KeyError:
        metal = True
        
    fermi_energy1 = bandsdata1.inp.output_band.res.fermi_energy
    fermi_energy2 = bandsdata2.inp.output_band.res.fermi_energy
    # Set the energy to be the SCF Fermi energy
    bands1 = bandsdata1.get_bands() - fermi_energy1
    bands2 = bandsdata2.get_bands() - fermi_energy2
    kpoints1 = bandsdata1.get_kpoints()
    kpoints2 = bandsdata2.get_kpoints()
 
    # Parameters to give to efermi
    num_electrons1 = int(bandsdata1.inp.output_band.res.number_of_electrons)
    num_electrons2 = int(bandsdata2.inp.output_band.res.number_of_electrons)
 
    if input_nelec==False:
        max_n=max(num_electrons1,num_electrons2)
        min_n=min(num_electrons1,num_electrons2)
        delta_n=(max_n-min_n)/nspin
    elif (input_nelec==True and nelec>0.0):
        min_n=nelec
    else:
        warnings.append("Error in finding the min number of electrons")
 
    num_bands1 = bandsdata1.inp.output_band.res.number_of_bands
    num_bands2 = bandsdata2.inp.output_band.res.number_of_bands
    nb1=0
    nb2=0
    if input_nelec==False:
        if num_electrons1>num_electrons2:
            bands1=bands1[:,delta_n:]
            nb1=num_bands1-delta_n
            nb2=num_bands2
        elif num_electrons1<num_electrons2:
            bands2=bands2[:,delta_n:]
            nb1=num_bands1
            nb2=num_bands2-delta_n
        elif num_electrons1==num_electrons2:
            nb1=num_bands1
            nb2=num_bands2
        else:
            warnings.append("Error in the semi-core states counting")
    elif (input_nelec==True and nelec>0.0):
        delta_n1=(num_electrons1-nelec)/nspin
        delta_n2=(num_electrons2-nelec)/nspin
        if (delta_n1<0 or delta_n2<0):
            warnings.append("nelec in input is greater than allowed")
        if delta_n1>0:
            bands1=bands1[:,delta_n1:]
            nb1=num_bands1-delta_n1
        else:
            nb1=num_bands1
        if delta_n2>0:
            bands2=bands2[:,delta_n2:]
            nb2=num_bands2-delta_n2
        else:
            nb2=num_bands2
    else:
        warnings.append("Error in the input number of electron")
    num_kpoints1 = len(kpoints1)
    num_kpoints2 = len(kpoints2)
    weight1 = np.ones(len(kpoints1))/num_kpoints1
    weight2 = np.ones(len(kpoints2))/num_kpoints2
    bands1_trans = np.transpose(bands1)
    bands2_trans = np.transpose(bands2)
    ismear = 2    # Fermi-Dirac
    ef = 0.0 # Fermi energy (It is 0.0 because it is already rescaled w.r.t. the SCF Fermi energy)
    
    def find_homo(num_elec,bands):
        band = bands[:,num_elec-1]
        homo = max(band)
        return homo
    
    # Calculate Fermi energy from efermi
    if metal:
        if nspin==1:
            res1 = efermi(2*min_n,nb1,smearing,num_kpoints1,weight1,ef,bands1_trans,ismear)
            res2 = efermi(2*min_n,nb2,smearing,num_kpoints2,weight2,ef,bands2_trans,ismear)
        else:
            res1 = efermi(min_n,nb1,smearing,num_kpoints1,weight1,ef,bands1_trans,ismear)
            res2 = efermi(min_n,nb2,smearing,num_kpoints2,weight2,ef,bands2_trans,ismear)
        e_fermi1 = res1[1]
        e_fermi2 = res2[1]
        smearing_v = smearing
        smearing_c = smearing
    else:
        if nspin==1:
            homo1 = find_homo(min_n,bands1)
            homo2 = find_homo(min_n,bands2)
        else:
            homo1 = find_homo(min_n/2,bands1)
            homo2 = find_homo(min_n/2,bands2)   
        e_fermi1 = homo1+1e-6
        e_fermi2 = homo2+1e-6
        smearing_v = 1e-8
        smearing_c = smearing

    #if abs(e_fermi1 - e_fermi2) > 0.1:
    #    warnings.append('efermi subroutine: the Fermi energy difference between the two set of bands is larger than 0.1 eV')
 
    # Check the element and the num of k-points are the same
    if len(kpoints1) != len(kpoints2):
        print len(kpoints1),len(kpoints2)
        warnings.append("The two sets of bands have different number of kpoints!")
  
    def compute_eta(bands1,bands2,e_fermi1,e_fermi2,smearing_v,smearing_c):
    #Wrapper to compute the eta function
    #Input: 2 bands structure as numpy arrays (band[k][n])
    #Output: eta_v,eta_10,x_v,x_10,max_v,max_10
    
        ## Function to calculate the Fermi-Dirac function    
        def fermi_dirac(band_energy, fermi_energy, smear):
            return 1.0 / ( np.exp( (band_energy - fermi_energy)/smear )  + 1.0 )

        tot_num_bands1 = len(bands1[0])
        tot_num_bands2 = len(bands2[0])
        def eta(shift=0.0, fermi_shift=0.0,smear=smearing_c):
            # Eta function to compute the distance between two bands structures
            sum_eta = 0.0
            normalization = 0.0
            occ=0.0
            for n in xrange(0,int(min(tot_num_bands1,tot_num_bands2))):
                for k in xrange(0, len(kpoints1)):
                    occ=np.sqrt(fermi_dirac(bands1[k][n],e_fermi1 +\
                    fermi_shift,smear)*fermi_dirac(bands2[k][n],e_fermi2 +\
                            fermi_shift,smear))
                    diff = occ*(bands1[k][n] - bands2[k][n] + shift)**2
                    sum_eta += diff
                    normalization += occ    
            eta = math.sqrt( sum_eta / ( normalization ) )
            return eta 
        def max_diff(shift=0.0, fermi_shift=0.0,smear=smearing_c):
            # function to compute the max eigenvalues distance
            max_diff=0.0
            occ=0.0
            for n in xrange(0,int(min(tot_num_bands1,tot_num_bands2))):
                for k in xrange(0, len(kpoints1)):
                    occ=np.sqrt(fermi_dirac(bands1[k][n],e_fermi1 +\
                    fermi_shift,smear)*fermi_dirac(bands2[k][n],e_fermi2 +\
                            fermi_shift,smear))
                    abs_diff = abs(bands1[k][n] - bands2[k][n] + shift)
                    if (abs_diff>max_diff) and (occ>0.5):
                        max_diff=abs_diff
            return max_diff
        def check_num_bands(shift=0.0, fermi_shift=0.0,smear=smearing_c):
            # function to check that the number of bands is enough to calculate the eta
            max_diff=0.0
            occ=0.0
            check_bands = True
            n=int(min(tot_num_bands1,tot_num_bands2)) - 1
            for k in xrange(0, len(kpoints1)):
                occ=np.sqrt(fermi_dirac(bands1[k][n],e_fermi1 +\
                fermi_shift,smear)*fermi_dirac(bands2[k][n],e_fermi2 +\
                        fermi_shift,smear))
                if occ>0.01:
                    check_bands=False
            return check_bands
        
        #Check that the number of bands included is enough
        check_bands=check_num_bands(shift=0.0, fermi_shift=10.0,smear=smearing_c)
 
        #Compute eta_v
        eta_val = partial(eta, fermi_shift=0.0,smear=smearing_v)
        result_val = minimize(eta_val, 0.0, method='Nelder-Mead')
        success_val = result_val.get('success')
        message_val = result_val.get('message')
        eta_val = result_val.get('fun')
        shift_val = result_val.get('x')[0]
        
        #Compute eta_10
        eta_cond = partial(eta, fermi_shift=10.0,smear=smearing_c)
        result_cond = minimize(eta_cond, 0.0, method='Nelder-Mead')
        success_cond = result_cond.get('success')
        message_cond = result_cond.get('message')
        eta_cond = result_cond.get('fun')
        shift_cond = result_cond.get('x')[0]
        
        #Compute max_v, max_10
        max_val=max_diff(shift=shift_val, fermi_shift=0.0,smear=smearing_v)
        max_cond=max_diff(shift=shift_cond, fermi_shift=10.0,smear=smearing_c)
                 
        return (eta_val,eta_cond,shift_val,shift_cond,max_val,max_cond,success_val,success_cond,check_bands,message_val,message_cond)
 
    (eta_val,eta_cond,shift_val,shift_cond,max_val,max_cond,success_val,success_cond,check_bands,message_val,message_cond) = \
    compute_eta(bands1,bands2,e_fermi1,e_fermi2,smearing_v,smearing_c)
    
    if not check_bands:
        warnings.append("The number of bands is too low!")
    if not success_val:
        warnings.append("The minimization of eta_v failed")
    if not success_cond:
        warnings.append("The minimization of eta_10 failed")
       
    output_dict = {
                   'warnings': warnings,
                   'results':{
                              'eta_v': eta_val,
                              'eta_10': eta_cond,
                              'max_v': max_val,
                              'max_10': max_cond,
                              'shift_v': shift_val,
                              'shift_10': shift_cond,
                              #'message_val': message_val,
                              #'message_cond': message_cond,
                              }
                   }
    
    return {'output_parameters': ParameterData(dict=output_dict)}

def get_bands_distance_results(parameters=None, bandsdata1=None, bandsdata2=None, store=True):

    """
    Get the results from the bands_distance_inline function:
    - if there exists already an inline calculation with the same inputs,
    it does not relaunch it, it gets instead the output dictionary of the previously
    launched function,
    - otherwise, launches the bands distance function
    and get its result.
    """
    from aiida.orm.calculation.inline import InlineCalculation
    from aiida.workflows.user.epfl_theos.dbimporters.utils import objects_are_equal

    result_dict = None
    for ic in bandsdata1.get_outputs(InlineCalculation):
        try:
            if ( ic.get_function_name() == 'bands_distance_inline'
                 and objects_are_equal(ic.inp.parameters.get_dict(), parameters.get_dict()) 
                 and objects_are_equal(ic.inp.bandsdata1.get_bands(), bandsdata1.get_bands(), epsilon=1e-7)
                 and objects_are_equal(ic.inp.bandsdata2.get_bands(), bandsdata2.get_bands(), epsilon=1e-7)
                 ) or ( ic.get_function_name() == 'bands_distance_inline'
                 and objects_are_equal(ic.inp.parameters.get_dict(), parameters.get_dict()) 
                 and objects_are_equal(ic.inp.bandsdata1.get_bands(), bandsdata2.get_bands(), epsilon=1e-7)
                 and objects_are_equal(ic.inp.bandsdata2.get_bands(), bandsdata1.get_bands(), epsilon=1e-7)
                 ):
                result_dict = ic.get_outputs_dict()
                warnings = ic.get_outputs_dict()['output_parameters'].get_dict()['warnings']
        except AttributeError:
            pass

    if result_dict is not None and not warnings:
        print "bands_distance_inline already run -> we do not re-run"
    else:
        print "Launch bands_distance_inline..."
        result_dict = bands_distance_inline(parameters=parameters,bandsdata1=bandsdata1,bandsdata2=bandsdata2,store=store)
    return result_dict



