# -*- coding: utf-8 -*-
"""
Spglib interface for Quantipy
"""

import _spglib as _spg
import numpy as np
from scipy import linalg


def get_symmetry(unitcell, basiscoordinates, symprec=1e-5, angle_tolerance=-1.0):
    """
    Return symmetry operations as hash.
    Hash key 'rotations' gives the numpy integer array
    of the rotation matrices for scaled positions
    Hash key 'translations' gives the numpy double array
    of the translation vectors in scaled positions
    """

    # Atomic positions have to be specified by scaled positions for spglib.
    lattice = np.array(unitcell, dtype='double', order='C')
    positions = np.array(linalg.solve(lattice, basiscoordinates.T).T, dtype='double', order='C')
    numbers = np.zeros(len(positions), dtype='intc', order='C')

    # Get number of symmetry operations and allocate symmetry operations
    # multi = _spg.multiplicity(cell, positions, numbers, symprec)
    multi = 48 * len(positions)
    rotation = np.zeros((multi, 3, 3), dtype='intc')
    translation = np.zeros((multi, 3), dtype='double')

    num_sym = _spg.symmetry(rotation,
                            translation,
                            lattice,
                            positions,
                            numbers,
                            symprec,
                            angle_tolerance)

    return {'rotations': np.array(rotation[:num_sym], dtype='intc', order='C'),
            'translations': np.array(translation[:num_sym], dtype='double', order='C'),
            'names': [None]*num_sym}

def get_symmetry_dataset(unitcell, basiscoordinates, symprec=1e-5, angle_tolerance=-1.0):
    """
    number: International space group number
    international: International symbol
    hall: Hall symbol
    transformation_matrix:
      Transformation matrix from lattice of input cell to Bravais lattice
      L^bravais = L^original * Tmat
    origin shift: Origin shift in the setting of 'Bravais lattice'
    rotations, translations:
      Rotation matrices and translation vectors
      Space group operations are obtained by
        [(r,t) for r, t in zip(rotations, translations)]
    wyckoffs:
      Wyckoff letters
    """
   
    # Atomic positions have to be specified by scaled positions for spglib.
    lattice = np.array(unitcell, dtype='double', order='C')
    positions = np.array(linalg.solve(lattice, basiscoordinates.T).T, dtype='double', order='C')
    numbers = np.zeros(len(positions), dtype='intc', order='C')


    
    keys = ('number',
            'hall_number',
            'international',
            'hall',
            'transformation_matrix',
            'origin_shift',
            'rotations',
            'translations',
            'wyckoffs',
            'equivalent_atoms',
            'brv_lattice',
            'brv_types',
            'brv_positions')
    dataset = {}
    for key, data in zip(keys, _spg.dataset(lattice,
                                           positions,
                                           numbers,
                                           symprec,
                                           angle_tolerance)):
        dataset[key] = data

    dataset['international'] = dataset['international'].strip()
    dataset['hall'] = dataset['hall'].strip()
    dataset['transformation_matrix'] = np.array(
        dataset['transformation_matrix'], dtype='double', order='C')
    dataset['origin_shift'] = np.array(dataset['origin_shift'], dtype='double')
    dataset['rotations'] = np.array(dataset['rotations'],
                                    dtype='intc', order='C')
    dataset['translations'] = np.array(dataset['translations'],
                                       dtype='double', order='C')
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    dataset['wyckoffs'] = [letters[x] for x in dataset['wyckoffs']]
    dataset['equivalent_atoms'] = np.array(dataset['equivalent_atoms'],
                                           dtype='intc')
    dataset['brv_lattice'] = np.array(np.transpose(dataset['brv_lattice']),
                                      dtype='double', order='C')
    dataset['brv_types'] = np.array(dataset['brv_types'], dtype='intc')
    dataset['brv_positions'] = np.array(dataset['brv_positions'],
                                        dtype='double', order='C')

    return dataset

def get_spacegroup(unitcell, basiscoordinates, symprec=1e-5, angle_tolerance=-1.0, symbol_type=0):
    """
    Return space group in international table symbol and number
    as a string.
    """

    dataset = get_symmetry_dataset(unitcell, basiscoordinates,
                                   symprec=symprec,
                                   angle_tolerance=angle_tolerance)
    symbols = _spg.spacegroup_type(dataset['hall_number'])
    if symbol_type == 1:
        return "%s (%d)" % (symbols[0], dataset['number'])
    else:
        return "%s (%d)" % (symbols[4], dataset['number'])

def get_pointgroup(rotations):
    """
    Return point group in international table symbol and number.
    The symbols are mapped to the numbers as follows:
    1   "1    "
    2   "-1   "
    3   "2    "
    4   "m    "
    5   "2/m  "
    6   "222  "
    7   "mm2  "
    8   "mmm  "
    9   "4    "
    10  "-4   "
    11  "4/m  "
    12  "422  "
    13  "4mm  "
    14  "-42m "
    15  "4/mmm"
    16  "3    "
    17  "-3   "
    18  "32   "
    19  "3m   "
    20  "-3m  "
    21  "6    "
    22  "-6   "
    23  "6/m  "
    24  "622  "
    25  "6mm  "
    26  "-62m "
    27  "6/mmm"
    28  "23   "
    29  "m-3  "
    30  "432  "
    31  "-43m "
    32  "m-3m "
    """
    schoenfliess = {1:u'C1', 2:u'Ci', 3:u'C2', 4:u'Cs', 5:u'C2h', 6:u'D2', 7:u'C2v', 8:u'D2h',
            9:u'C4', 10:u'S4', 11:u'C4h', 12:u'D4', 13:u'C4v', 14:u'D2d', 15:u'D4h', 16:u'C3',
            17:u'S6', 18:u'D3', 19:u'C3v', 20:u'D3d', 21:u'C6', 22:u'C3h', 23:u'C6h', 24:u'D6',
            25:u'C6v', 26:u'D3h', 27:u'D6h', 28:u'T', 29:u'Th', 30:u'O', 31:u'Td', 32:u'Oh'}
            
    # (symbol, pointgroup_number, transformation_matrix)
    pginfo = _spg.pointgroup(np.array(rotations, dtype='intc', order='C'))

    # (symbol, schoenfliess, pointgroup_number, transformation_matrix)
    pginfo.insert(1,schoenfliess[pginfo[1]])
    return pginfo

def refine_cell(bulk, symprec=1e-5, angle_tolerance=-1.0):
    """
    Return refined cell
    """
    # Atomic positions have to be specified by scaled positions for spglib.
    num_atom = bulk.get_number_of_atoms()
    lattice = np.array(bulk.get_cell().T, dtype='double', order='C')
    pos = np.zeros((num_atom * 4, 3), dtype='double')
    pos[:num_atom] = bulk.get_scaled_positions()

    numbers = np.zeros(num_atom * 4, dtype='intc')
    numbers[:num_atom] = np.array(bulk.get_atomic_numbers(), dtype='intc')
    num_atom_bravais = _spg.refine_cell(lattice,
                                       pos,
                                       numbers,
                                       num_atom,
                                       symprec,
                                       angle_tolerance)

    return (np.array(lattice.T, dtype='double', order='C'),
            np.array(pos[:num_atom_bravais], dtype='double', order='C'),
            np.array(numbers[:num_atom_bravais], dtype='intc'))


def find_primitive(cell, coordinates, symprec=1e-5, angle_tolerance=-1.0):
    """
    A primitive cell in the input cell is searched and returned
    If no primitive cell is found, (None, None, None) is returned.
    """
    
    # Atomic positions have to be specified by scaled positions for spglib.
    lattice = np.array(cell, dtype='double', order='C')
    positions = np.array(linalg.solve(lattice, coordinates.T).T, dtype='double', order='C')
    numbers = np.zeros(len(positions), dtype='intc', order='C')

    # lattice is transposed with respect to the definition of Atoms class
    num_atom_prim = _spg.primitive(lattice,
                                  positions,
                                  numbers,
                                  symprec,
                                  angle_tolerance)
    if num_atom_prim > 0:
        return (np.array(lattice.T, dtype='double', order='C'),
                np.array(positions[:num_atom_prim], dtype='double', order='C'),
                np.array(numbers[:num_atom_prim], dtype='intc'))
    else:
        return None, None, None


        
############
# k-points #
############
def get_grid_point_from_address(grid_address,
                                mesh,
                                is_shift=np.zeros(3, dtype='intc')):
    """
    Return grid point index by tranlating grid address
    """

    return _spg.grid_point_from_address(np.array(grid_address, dtype='intc'),
                                       np.array(mesh, dtype='intc'),
                                       np.array(is_shift, dtype='inct'))
    

def get_ir_reciprocal_mesh(mesh,
                           bulk,
                           is_shift=np.zeros(3, dtype='intc'),
                           is_time_reversal=True,
                           symprec=1e-5):
    """
    Return k-points mesh and k-point map to the irreducible k-points
    The symmetry is serched from the input cell.
    is_shift=[0, 0, 0] gives Gamma center mesh.
    """

    mapping = np.zeros(np.prod(mesh), dtype='intc')
    mesh_points = np.zeros((np.prod(mesh), 3), dtype='intc')
    _spg.ir_reciprocal_mesh(
        mesh_points,
        mapping,
        np.array(mesh, dtype='intc'),
        np.array(is_shift, dtype='intc'),
        is_time_reversal * 1,
        np.array(bulk.get_cell().T, dtype='double', order='C'),
        np.array(bulk.get_scaled_positions(), dtype='double', order='C'),
        np.array(bulk.get_atomic_numbers(), dtype='intc'),
        symprec)
  
    return mapping, mesh_points

def get_grid_points_by_rotations(address_orig,
                                 reciprocal_rotations,
                                 mesh,
                                 is_shift=np.zeros(3, dtype='intc')):
    """
    Rotation operations in reciprocal space ``reciprocal_rotations`` are applied
    to a grid point ``grid_point`` and resulting grid points are returned.
    """
    
    rot_grid_points = np.zeros(len(reciprocal_rotations), dtype='intc')
    _spg.grid_points_by_rotations(
        rot_grid_points,
        np.array(address_orig, dtype='intc'),
        np.array(reciprocal_rotations, dtype='intc', order='C'),
        np.array(mesh, dtype='intc'),
        np.array(is_shift, dtype='intc'))
    
    return rot_grid_points

def get_BZ_grid_points_by_rotations(address_orig,
                                    reciprocal_rotations,
                                    mesh,
                                    bz_map,
                                    is_shift=np.zeros(3, dtype='intc')):
    """
    Rotation operations in reciprocal space ``reciprocal_rotations`` are applied
    to a grid point ``grid_point`` and resulting grid points are returned.
    """
    
    rot_grid_points = np.zeros(len(reciprocal_rotations), dtype='intc')
    _spg.BZ_grid_points_by_rotations(
        rot_grid_points,
        np.array(address_orig, dtype='intc'),
        np.array(reciprocal_rotations, dtype='intc', order='C'),
        np.array(mesh, dtype='intc'),
        np.array(is_shift, dtype='intc'),
        bz_map)
    
    return rot_grid_points
    
def relocate_BZ_grid_address(grid_address,
                             mesh,
                             reciprocal_lattice, # column vectors
                             is_shift=np.zeros(3, dtype='intc')):
    """
    Grid addresses are relocated inside Brillouin zone. 
    Number of ir-grid-points inside Brillouin zone is returned. 
    It is assumed that the following arrays have the shapes of 
      bz_grid_address[prod(mesh + 1)][3] 
      bz_map[prod(mesh * 2)] 
    where grid_address[prod(mesh)][3]. 
    Each element of grid_address is mapped to each element of 
    bz_grid_address with keeping element order. bz_grid_address has 
    larger memory space to represent BZ surface even if some points 
    on a surface are translationally equivalent to the other points 
    on the other surface. Those equivalent points are added successively 
    as grid point numbers to bz_grid_address. Those added grid points 
    are stored after the address of end point of grid_address, i.e. 
                                                                          
    |-----------------array size of bz_grid_address---------------------| 
    |--grid addresses similar to grid_address--|--newly added ones--|xxx| 
                                                                          
    where xxx means the memory space that may not be used. Number of grid 
    points stored in bz_grid_address is returned. 
    bz_map is used to recover grid point index expanded to include BZ 
    surface from grid address. The grid point indices are mapped to 
    (mesh[0] * 2) x (mesh[1] * 2) x (mesh[2] * 2) space (bz_map).
    """
    
    bz_grid_address = np.zeros(
        ((mesh[0] + 1) * (mesh[1] + 1) * (mesh[2] + 1), 3), dtype='intc')
    bz_map = np.zeros(
        (2 * mesh[0]) * (2 * mesh[1]) * (2 * mesh[2]), dtype='intc')
    num_bz_ir = _spg.BZ_grid_address(
        bz_grid_address,
        bz_map,
        grid_address,
        np.array(mesh, dtype='intc'),
        np.array(reciprocal_lattice, dtype='double', order='C'),
        np.array(is_shift, dtype='intc'))

    return bz_grid_address[:num_bz_ir], bz_map
  
def get_stabilized_reciprocal_mesh(mesh,
                                   rotations,
                                   is_shift=np.zeros(3, dtype='intc'),
                                   is_time_reversal=True,
                                   qpoints=np.array([], dtype='double')):
    """
    Return k-point map to the irreducible k-points and k-point grid points .

    The symmetry is searched from the input rotation matrices in real space.
    
    is_shift=[0, 0, 0] gives Gamma center mesh and the values 1 give
    half mesh distance shifts.
    """
    
    mapping = np.zeros(np.prod(mesh), dtype='intc')
    mesh_points = np.zeros((np.prod(mesh), 3), dtype='intc')
    qpoints = np.array(qpoints, dtype='double', order='C')
    if qpoints.shape == (3,):
        qpoints = np.array([qpoints], dtype='double', order='C')
    if qpoints.shape == (0,):
        qpoints = np.array([[0, 0, 0]], dtype='double', order='C')

    _spg.stabilized_reciprocal_mesh(
        mesh_points,
        mapping,
        np.array(mesh, dtype='intc'),
        np.array(is_shift, dtype='intc'),
        is_time_reversal * 1,
        np.array(rotations, dtype='intc', order='C'),
        qpoints)
    
    return mapping, mesh_points

def get_triplets_reciprocal_mesh_at_q(fixed_grid_number,
                                      mesh,
                                      rotations,
                                      is_time_reversal=True):

    map_triplets = np.zeros(np.prod(mesh), dtype='intc')
    map_q = np.zeros(np.prod(mesh), dtype='intc')
    mesh_points = np.zeros((np.prod(mesh), 3), dtype='intc')

    _spg.triplets_reciprocal_mesh_at_q(
        map_triplets,
        map_q,
        mesh_points,
        fixed_grid_number,
        np.array(mesh, dtype='intc'),
        is_time_reversal * 1,
        np.array(rotations, dtype='intc', order='C'))

    return map_triplets, map_q, mesh_points
        
def get_BZ_triplets_at_q(grid_point,
                         bz_grid_address,
                         bz_map,
                         map_triplets,
                         mesh):
    """grid_address is overwritten."""
    weights = np.zeros_like(map_triplets)
    for g in map_triplets:
        weights[g] += 1
    ir_weights = np.extract(weights > 0, weights)
    triplets = np.zeros((len(ir_weights), 3), dtype='intc')
    num_ir_ret = _spg.BZ_triplets_at_q(triplets,
                                      grid_point,
                                      bz_grid_address,
                                      bz_map,
                                      map_triplets,
                                      np.array(mesh, dtype='intc'))
    
    return triplets, ir_weights

def get_neighboring_grid_points(grid_point,
                                relative_grid_address,
                                mesh,
                                bz_grid_address,
                                bz_map):
    relative_grid_points = np.zeros(len(relative_grid_address), dtype='intc')
    _spg.neighboring_grid_points(relative_grid_points,
                                grid_point,
                                relative_grid_address,
                                mesh,
                                bz_grid_address,
                                bz_map)
    return relative_grid_points
    

    
######################
# Tetrahedron method #
######################
def get_triplets_tetrahedra_vertices(relative_grid_address,
                                     mesh,
                                     triplets,
                                     bz_grid_address,
                                     bz_map):
    num_tripltes = len(triplets)
    vertices = np.zeros((num_tripltes, 2, 24, 4), dtype='intc')
    for i, tp in enumerate(triplets):
        vertices_at_tp = np.zeros((2, 24, 4), dtype='intc')
        _spg.triplet_tetrahedra_vertices(
            vertices_at_tp,
            relative_grid_address,
            np.array(mesh, dtype='intc'),
            tp,
            bz_grid_address,
            bz_map)
        vertices[i] = vertices_at_tp

    return vertices

def get_tetrahedra_relative_grid_address(microzone_lattice):
    """
    reciprocal_lattice:
      column vectors of parallel piped microzone lattice
      which can be obtained by:
      microzone_lattice = np.linalg.inv(bulk.get_cell()) / mesh
    """
    
    relative_grid_address = np.zeros((24, 4, 3), dtype='intc')
    _spg.tetrahedra_relative_grid_address(
        relative_grid_address,
        np.array(microzone_lattice, dtype='double', order='C'))
    
    return relative_grid_address

def get_all_tetrahedra_relative_grid_address():
    relative_grid_address = np.zeros((4, 24, 4, 3), dtype='intc')
    _spg.all_tetrahedra_relative_grid_address(relative_grid_address)
    
    return relative_grid_address
    
def get_tetrahedra_integration_weight(omegas,
                                      tetrahedra_omegas,
                                      function='I'):
    if isinstance(omegas, float):
        return _spg.tetrahedra_integration_weight(
            omegas,
            np.array(tetrahedra_omegas, dtype='double', order='C'),
            function)
    else:
        integration_weights = np.zeros(len(omegas), dtype='double')
        _spg.tetrahedra_integration_weight_at_omegas(
            integration_weights,
            np.array(omegas, dtype='double'),
            np.array(tetrahedra_omegas, dtype='double', order='C'),
            function)
        return integration_weights

                                      
                                               
