/*
 *  QuickED Extension module
 */


#include <Python.h>
#include <numpy/arrayobject.h>

#include <iostream>
#include <vector>

#include "interface.h"
#include "SymmetryEngine.h"
#include "LocalSymmetryVoid.h"

extern "C"
{
  // Definition of all functions interfaced by Python
  static PyObject * raw_dimension(PyObject *self, PyObject *args);
  static PyObject * basis_state_string(PyObject *self, PyObject *args);
  static PyObject * get_basis_states(PyObject *self, PyObject *args);
  static PyObject * get_basis_states_symmetrized(PyObject *self, PyObject *args);
  static PyObject * get_operator(PyObject *self, PyObject *args);
  static PyObject * get_operator_symmetrized(PyObject *self, PyObject *args);
  
  // Table of all functions interfaced by Python
  static PyMethodDef functions[] = 
    {
      {"_raw_dimension", raw_dimension, METH_VARARGS,
       "raw dimension of Hilbert space"},
      {"_basis_state_string", basis_state_string, METH_VARARGS,
       "String of a basis state"},
      {"_get_basis_states", get_basis_states, METH_VARARGS,
       "Get the array of raw basis states"},
      {"_get_basis_states_symmetrized", get_basis_states_symmetrized, METH_VARARGS,
       "Get the array of symmetrized basis states"},
      {"_get_operator", get_operator, METH_VARARGS,
       "Get Operator in raw basis"},
      {"_get_operator_symmetrized", get_operator_symmetrized, METH_VARARGS,
       "Get Operator in symmetrized basis"},
      { NULL, NULL, 0, NULL}
    };

  // Error Handling
  struct module_state {
    PyObject *error;
  };

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
  static struct module_state _state;
#endif

  static PyObject *
  error_out(PyObject *m) {
    struct module_state *st = GETSTATE(m);
    PyErr_SetString(st->error, "Unknown error in QuickED extension");
    return NULL;
  }


  // Module Initialization function
#if PY_MAJOR_VERSION >= 3

  static int _quicked_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
  }

  static int _quicked_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
  }


  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_quicked",
    NULL,
    sizeof(struct module_state),
    functions,
    NULL,
    _quicked_traverse,
    _quicked_clear,
    NULL
  };

#define INITERROR return NULL

  PyMODINIT_FUNC PyInit__quicked(void)

#else
#define INITERROR return

    void init_quicked(void)
#endif
  {
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
    import_array();
    return module;
#else
    (void) Py_InitModule("_quicked", functions);
    import_array();
#endif
    
  }

}// end: extern "C"


// Wrappers and template dispatchers
static PyObject * raw_dimension(PyObject *self, PyObject *args)
{
  int n_sites, sz;
  const char *type;
  if (!PyArg_ParseTuple(args, "isi", &n_sites, &type, &sz)) return NULL;
  
  uint64 dimension=0;
  using quicked::interface::raw_dimension;
  if(strcmp(type, "spinhalf") == 0) 
    dimension = raw_dimension<HILBERTSPACE_SPINHALF_TYPE>(n_sites, sz);
  else if (strcmp(type, "spinone") == 0)
    dimension = raw_dimension<HILBERTSPACE_SPIN_ONE_GEN_TYPE>(n_sites, sz);
  else if (strcmp(type, "spinthreehalf") == 0)
    dimension = raw_dimension<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>(n_sites, sz);
  else if (strcmp(type, "spintwo") == 0)
    dimension = raw_dimension<HILBERTSPACE_SPIN_TWO_GEN_TYPE>(n_sites, sz);
  else if (strcmp(type, "u2") == 0)
    dimension = raw_dimension<HILBERTSPACE_2_TYPE>(n_sites, sz);
  else if (strcmp(type, "u3") == 0)
    dimension = raw_dimension<HILBERTSPACE_3_TYPE>(n_sites, sz);
  else if (strcmp(type, "u4") == 0)
    dimension = raw_dimension<HILBERTSPACE_4_TYPE>(n_sites, sz);


  return Py_BuildValue("L", dimension);
}


static PyObject * basis_state_string(PyObject *self, PyObject *args)
{
  const char *type;
  uint64 state;
  int n_sites;
  if (!PyArg_ParseTuple(args, "Lis", &state, &n_sites, &type)) return NULL;
  
  std::string str;

  using quicked::state_string;
  if(strcmp(type, "spinhalf") == 0) 
    str = state_string<HILBERTSPACE_SPINHALF_TYPE>(state, n_sites);
  else if (strcmp(type, "spinone") == 0)
    str = state_string<HILBERTSPACE_SPIN_ONE_GEN_TYPE>(state, n_sites);
  else if (strcmp(type, "spinthreehalf") == 0)
    str = state_string<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>(state, n_sites);
  else if (strcmp(type, "spintwo") == 0)
    str = state_string<HILBERTSPACE_SPIN_TWO_GEN_TYPE>(state, n_sites);
  else if (strcmp(type, "u2") == 0)
    str = state_string<HILBERTSPACE_2_TYPE>(state, n_sites);
  else if (strcmp(type, "u3") == 0)
    str = state_string<HILBERTSPACE_3_TYPE>(state, n_sites);
  else if (strcmp(type, "u4") == 0)
    str = state_string<HILBERTSPACE_4_TYPE>(state, n_sites); 
  return Py_BuildValue("s", str.c_str());
}


template <hilbert_t THilbertSpace>
void dispatch_get_basis_states
(const uint32& n_sites, const uint32& sz,
 uint64 *n_basis_states, uint64 **basis_states)
{
  using quicked::interface::sz_to_n_upspins;
  using quicked::interface::get_basis_states;
  using quicked::quantumnumber_t;
  uint32 n_upspins = sz_to_n_upspins<THilbertSpace>(n_sites, sz);
  assert(n_upspins < max_n_upspins<THilbertSpace>(n_sites));
  quantumnumber_t<THilbertSpace> qn = {n_upspins};
  get_basis_states<THilbertSpace>(n_sites, qn, n_basis_states, basis_states);
}

static PyObject * get_basis_states(PyObject *self, PyObject *args)
{
  const char *type;
  int n_sites, sz;
  if (!PyArg_ParseTuple(args, "isi", &n_sites, &type, &sz)) return NULL;
  std::cout << type << " " << n_sites << " " << sz << std::endl;

  // Create vector containing all basis states
  uint64 n_basis_states;
  uint64* basis_states;
  
  using quicked::interface::sz_to_n_upspins;
  using quicked::interface::get_basis_states;
  using quicked::quantumnumber_t;
  if(strcmp(type, "spinhalf") == 0)
    dispatch_get_basis_states<HILBERTSPACE_SPINHALF_TYPE>
      (n_sites, sz, &n_basis_states, &basis_states);
  else if (strcmp(type, "spinone") == 0)
    dispatch_get_basis_states<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
      (n_sites, sz, &n_basis_states, &basis_states);    
  else if (strcmp(type, "spinthreehalf") == 0)
    dispatch_get_basis_states<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
      (n_sites, sz, &n_basis_states, &basis_states);    
  else if (strcmp(type, "spintwo") == 0)
    dispatch_get_basis_states<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
      (n_sites, sz, &n_basis_states, &basis_states);
  else if (strcmp(type, "u2") == 0)
    dispatch_get_basis_states<HILBERTSPACE_2_TYPE>
      (n_sites, sz, &n_basis_states, &basis_states);
  else if (strcmp(type, "u3") == 0)
    dispatch_get_basis_states<HILBERTSPACE_3_TYPE>
      (n_sites, sz, &n_basis_states, &basis_states);
  else if (strcmp(type, "u4") == 0)
    dispatch_get_basis_states<HILBERTSPACE_4_TYPE>
      (n_sites, sz, &n_basis_states, &basis_states);

  
  // create numpy array
  npy_intp dims[1] = {(npy_intp)n_basis_states};
  PyObject* vec_np = PyArray_SimpleNewFromData(1, dims, NPY_ULONGLONG, basis_states);
  Py_INCREF(vec_np);

  return Py_BuildValue("O", vec_np);
}


template <hilbert_t THilbertSpace>
void dispatch_get_basis_states_symmetrized
(const uint32& n_sites, const uint32& sz,
 const std::vector<std::vector<uint32> >& permutations_vec,
 const std::vector<complex>& blochfactors_vec,
 uint64 *n_basis_states, uint64 **basis_states, double **norms)
{
  using quicked::interface::sz_to_n_upspins;
  using quicked::interface::get_basis_states_symmetrized;
  using quicked::quantumnumber_t;
  using quicked::SymmetryEngine;
  using quicked::LocalSymmetryVoid;
  
  LocalSymmetryVoid<THilbertSpace> local_sym;
  uint32 n_upspins = sz_to_n_upspins<THilbertSpace>(n_sites, sz);
  assert(n_upspins < max_n_upspins<THilbertSpace>(n_sites));
  quantumnumber_t<THilbertSpace> qn = {n_upspins};
  SymmetryEngine<THilbertSpace, LocalSymmetryVoid<THilbertSpace> > symmetry_engine
    (permutations_vec, blochfactors_vec, local_sym);
  get_basis_states_symmetrized<THilbertSpace, LocalSymmetryVoid>
    (n_sites, qn, symmetry_engine, n_basis_states, basis_states, norms);
}

static PyObject * get_basis_states_symmetrized(PyObject *self, PyObject *args)
{
  int n_sites, sz;
  PyArrayObject *permutations;
  PyArrayObject *blochfactors;
  const char *type;

  if (!PyArg_ParseTuple(args, "iO!O!si", &n_sites, &PyArray_Type, &permutations,
			&PyArray_Type, &blochfactors, &type, &sz))
    return NULL;
  
  if (permutations == NULL) return NULL;
  if (blochfactors == NULL) return NULL;

  
  int *perms_arr = reinterpret_cast<int*>(permutations->data);
  complex *blochs_arr = reinterpret_cast<complex*>(blochfactors->data);
  
  // Create input in proper format for calling interface
  assert(permutations->nd==2);
  assert(blochfactors->nd==1);

  npy_intp *shape_perms = permutations->dimensions;
  npy_intp *shape_blochs = blochfactors->dimensions;

  std::vector<complex> blochfactors_vec;
  for (uint32 i = 0; i < shape_blochs[0]; ++i)
    {
      // std::cout << blochs_arr[i] << std::endl;
      blochfactors_vec.push_back(blochs_arr[i]);
    }
  
  // std::cout << "shape_perms " << shape_perms[0] << " " << shape_perms[1]
  // 	    << std::endl << std::flush;
  std::vector<std::vector<uint32> > permutations_vec;
  for (uint32 i = 0; i < shape_perms[0]; ++i)
    {
      std::vector<uint32> sym;
      for (uint32 j = 0; j < shape_perms[1]; ++j)
	{
	  // std::cout << perms_arr[i*shape_perms[1] + j] <<" ";
	  int p = perms_arr[i*shape_perms[1] + j];
	  assert(p >= 0);
	  sym.push_back(p);
	}
      // std::cout << std::endl;
      permutations_vec.push_back(sym);

    }
 
  // Create vector containing all basis states
  uint64 n_basis_states;
  uint64* basis_states;
  double* norms;
  
  if(strcmp(type, "spinhalf") == 0)
    dispatch_get_basis_states_symmetrized<HILBERTSPACE_SPINHALF_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       &n_basis_states, &basis_states, &norms);
  else if (strcmp(type, "spinone") == 0)
    dispatch_get_basis_states_symmetrized<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       &n_basis_states, &basis_states, &norms);
  else if (strcmp(type, "spinthreehalf") == 0)
    dispatch_get_basis_states_symmetrized<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       &n_basis_states, &basis_states, &norms);
  else if (strcmp(type, "spintwo") == 0)
    dispatch_get_basis_states_symmetrized<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       &n_basis_states, &basis_states, &norms);
  else if (strcmp(type, "u2") == 0)
    dispatch_get_basis_states_symmetrized<HILBERTSPACE_2_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       &n_basis_states, &basis_states, &norms);
  else if (strcmp(type, "u3") == 0)
    dispatch_get_basis_states_symmetrized<HILBERTSPACE_3_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       &n_basis_states, &basis_states, &norms);
  else if (strcmp(type, "u4") == 0)
    dispatch_get_basis_states_symmetrized<HILBERTSPACE_4_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       &n_basis_states, &basis_states, &norms);
  
  // create numpy arrays
  npy_intp dims[1] = {(npy_intp)n_basis_states};
  PyObject* npy_basis_states = PyArray_SimpleNewFromData(1, dims, NPY_ULONGLONG, basis_states);
  Py_INCREF(npy_basis_states);

  PyObject* npy_norms = PyArray_SimpleNewFromData(1, dims, NPY_DOUBLE, norms);
  Py_INCREF(npy_norms);

  PyObject *rslt = PyTuple_New(2);
  PyTuple_SetItem(rslt, 0, npy_basis_states);
  PyTuple_SetItem(rslt, 1, npy_norms);
  
  return rslt;
}


template <hilbert_t THilbertSpace>
void dispatch_get_operator
(const uint32& n_sites, const uint32& sz,
 const uint32& n_bonds, const uint32* n_sites_for_bonds,
 int** bond_sites, complex **bond_matrices,
 uint64 *n_basis_states, uint64 **basis_states,
 uint64 *n_entries, uint64 **rows, uint64 **cols, complex **data)
{
  using quicked::interface::sz_to_n_upspins;
  using quicked::interface::get_basis_states;
  using quicked::interface::get_operator;
  using quicked::quantumnumber_t;
  
  uint32 n_upspins = sz_to_n_upspins<THilbertSpace>(n_sites, sz);
  assert(n_upspins < max_n_upspins<THilbertSpace>(n_sites));
  quantumnumber_t<THilbertSpace> qn = {n_upspins};

  bool delete_basis = false;
  if (*basis_states == NULL)
    {
      get_basis_states<THilbertSpace>
	(n_sites, qn, n_basis_states, basis_states);
      delete_basis = true;
    }

  get_operator<THilbertSpace>
    (*n_basis_states, *basis_states, n_bonds, n_sites_for_bonds,
     bond_sites, bond_matrices, n_entries, rows, cols, data);
  
  if (delete_basis)
    {
      delete [] *basis_states;
      *n_basis_states = 0;
      *basis_states = NULL;
    }
}


static PyObject * get_operator(PyObject *self, PyObject *args)
{
  int n_sites, sz;
  const char *type;

  PyArrayObject *bond_sites;
  PyArrayObject *bond_matrices;
  PyArrayObject *basis_states;

  if (!PyArg_ParseTuple(args, "isiO!O!O!", &n_sites,&type, &sz, &PyArray_Type,
			&bond_sites, &PyArray_Type, &bond_matrices,
			&PyArray_Type, &basis_states))
    return NULL;

  // Get dimensions and shapes of input arrays
  if (bond_sites == NULL) return NULL;
  if (bond_matrices == NULL) return NULL;
  
  int *bond_sites_arr = reinterpret_cast<int*>(bond_sites->data);
  complex *bond_matrices_arr = reinterpret_cast<complex*>(bond_matrices->data);
  uint64* basis_states_arr = NULL;
  uint64 n_basis_states = 0;
  assert(basis_states->nd==1);
  if (basis_states->dimensions[0] > 0)
    {
      basis_states_arr = reinterpret_cast<uint64*>(basis_states->data);
      n_basis_states = (uint64)basis_states->dimensions[0];
    }

  assert(bond_sites->nd==2);
  assert(bond_matrices->nd==1);  
  
  npy_intp *shape_bond_sites = bond_sites->dimensions;
  // npy_intp *shape_bond_matrices = bond_matrices->dimensions;

  // Get bond_matrices in proper format
  uint32 local_dim=0;
  if (strcmp(type, "spinhalf") == 0) local_dim = 2;
  else if (strcmp(type, "spinone") == 0) local_dim = 3;
  else if (strcmp(type, "spinthreehalf") == 0) local_dim = 4;
  else if (strcmp(type, "spintwo") == 0) local_dim = 5;
  else if (strcmp(type, "u2") == 0) local_dim = 2;
  else if (strcmp(type, "u3") == 0) local_dim = 3;
  else if (strcmp(type, "u4") == 0) local_dim = 4;
  
  uint32 n_bonds = shape_bond_sites[0];
  uint32* n_sites_for_bond = new uint32[n_bonds];
  int** bond_sites_final = new int*[n_bonds];
  complex** bond_matrices_final = new complex*[n_bonds];

  uint32 bond_offset = shape_bond_sites[1];
  uint32 bond_matrix_offset = 0;
  for (uint32 i = 0; i < n_bonds; ++i)
    {
      n_sites_for_bond[i] = 0;
      while(bond_sites_arr[i*bond_offset + n_sites_for_bond[i]] != -1)
	++n_sites_for_bond[i];
      
      bond_sites_final[i] = bond_sites_arr + i*bond_offset;
      bond_matrices_final[i] = bond_matrices_arr + bond_matrix_offset;
      bond_matrix_offset += pow(local_dim, 2*n_sites_for_bond[i]);
    }
  assert(bond_matrix_offset == shape_bond_matrices[0]);


  // Dispatch get_operator
  uint64 n_entries;
  uint64 *rows, *cols;
  complex *data;
  
  if(strcmp(type, "spinhalf") == 0)
    dispatch_get_operator<HILBERTSPACE_SPINHALF_TYPE>
      (n_sites, sz, n_bonds, n_sites_for_bond, bond_sites_final,
       bond_matrices_final, &n_basis_states, &basis_states_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "spinone") == 0)
    dispatch_get_operator<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
      (n_sites, sz, n_bonds, n_sites_for_bond, bond_sites_final,
       bond_matrices_final, &n_basis_states, &basis_states_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "spinthreehalf") == 0)
    dispatch_get_operator<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
      (n_sites, sz, n_bonds, n_sites_for_bond, bond_sites_final,
       bond_matrices_final, &n_basis_states, &basis_states_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "spintwo") == 0)
    dispatch_get_operator<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
      (n_sites, sz, n_bonds, n_sites_for_bond, bond_sites_final,
       bond_matrices_final, &n_basis_states, &basis_states_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "u2") == 0)
    dispatch_get_operator<HILBERTSPACE_2_TYPE>
      (n_sites, sz, n_bonds, n_sites_for_bond, bond_sites_final,
       bond_matrices_final, &n_basis_states, &basis_states_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "u3") == 0)
    dispatch_get_operator<HILBERTSPACE_3_TYPE>
      (n_sites, sz, n_bonds, n_sites_for_bond, bond_sites_final,
       bond_matrices_final, &n_basis_states, &basis_states_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "u4") == 0)
    dispatch_get_operator<HILBERTSPACE_4_TYPE>
      (n_sites, sz, n_bonds, n_sites_for_bond, bond_sites_final,
       bond_matrices_final, &n_basis_states, &basis_states_arr,
       &n_entries, &rows, &cols, &data);
 
 
  // Free bond_matrices
  delete [] bond_sites_final;
  delete [] bond_matrices_final;
  delete [] n_sites_for_bond;
  
  // create numpy arrays
  npy_intp dims[1] = {(npy_intp)n_entries};
  PyObject* npy_rows = PyArray_SimpleNewFromData(1, dims, NPY_ULONGLONG, rows);
  Py_INCREF(npy_rows);
  PyObject* npy_cols = PyArray_SimpleNewFromData(1, dims, NPY_ULONGLONG, cols);
  Py_INCREF(npy_cols);
  PyObject* npy_data = PyArray_SimpleNewFromData(1, dims, NPY_COMPLEX128, data);
  Py_INCREF(npy_data);

  PyObject *rslt = PyTuple_New(3);
  PyTuple_SetItem(rslt, 0, npy_rows);
  PyTuple_SetItem(rslt, 1, npy_cols);
  PyTuple_SetItem(rslt, 2, npy_data);
  
  return rslt;
}


template <hilbert_t THilbertSpace>
void dispatch_get_operator_symmetrized
(const uint32& n_sites, const uint32& sz,
 const std::vector<std::vector<uint32> >& permutations_vec,
 const std::vector<complex>& blochfactors_vec,
 const uint32& n_bonds, const uint32* n_sites_for_bonds,
 int** bond_sites, complex** bond_matrices,
 uint64 *n_basis_states, uint64 **basis_states, double **norms,
 uint64* n_entries, uint64** rows, uint64** cols, complex** data)
{
  using quicked::interface::sz_to_n_upspins;
  using quicked::interface::get_basis_states_symmetrized;
  using quicked::interface::get_operator_symmetrized;
  using quicked::quantumnumber_t;
  using quicked::SymmetryEngine;
  using quicked::LocalSymmetryVoid;

  LocalSymmetryVoid<THilbertSpace> local_sym;
  uint32 n_upspins = sz_to_n_upspins<THilbertSpace>(n_sites, sz);
  assert(n_upspins < max_n_upspins<THilbertSpace>(n_sites));
  quantumnumber_t<THilbertSpace> qn = {n_upspins};
  SymmetryEngine<THilbertSpace, LocalSymmetryVoid<THilbertSpace> > symmetry_engine
    (permutations_vec, blochfactors_vec, local_sym);

  bool delete_basis = false;
  if ((*basis_states == NULL) || (*norms == NULL))
    {
      get_basis_states_symmetrized<THilbertSpace, LocalSymmetryVoid>
	(n_sites, qn, symmetry_engine, n_basis_states, basis_states, norms);
      delete_basis = true;
    }
  
  get_operator_symmetrized<THilbertSpace,
			   SymmetryEngine<THilbertSpace, LocalSymmetryVoid<THilbertSpace> > >
    (symmetry_engine, *n_basis_states, *basis_states, *norms,
     n_bonds, n_sites_for_bonds, bond_sites, bond_matrices,
     n_entries, rows, cols, data);

  if (delete_basis)
    {
      delete [] *basis_states;
      delete [] *norms;
      *n_basis_states = 0;
      *basis_states = NULL;
      *norms = NULL;
    }
  
  
}


static PyObject * get_operator_symmetrized(PyObject *self, PyObject *args)
{
  int n_sites, sz;
  PyArrayObject *permutations;
  PyArrayObject *blochfactors;
  const char *type;

  PyArrayObject *bond_sites;
  PyArrayObject *bond_matrices;
  PyArrayObject *basis_states;
  PyArrayObject *norms;
  if (!PyArg_ParseTuple(args, "iO!O!siO!O!O!O!", &n_sites, &PyArray_Type, &permutations,
			&PyArray_Type, &blochfactors, &type, &sz, &PyArray_Type,
			&bond_sites, &PyArray_Type, &bond_matrices,
			&PyArray_Type, &basis_states, &PyArray_Type, &norms))
    return NULL;

  // Get dimensions and shapes of input arrays
  if (permutations == NULL) return NULL;
  if (blochfactors == NULL) return NULL;
  if (bond_sites == NULL) return NULL;
  if (bond_matrices == NULL) return NULL;
  
  int *perms_arr = reinterpret_cast<int*>(permutations->data);
  complex *blochs_arr = reinterpret_cast<complex*>(blochfactors->data);
  int *bond_sites_arr = reinterpret_cast<int*>(bond_sites->data);
  complex *bond_matrices_arr = reinterpret_cast<complex*>(bond_matrices->data);
  
  assert(permutations->nd==2);
  assert(blochfactors->nd==1);
  assert(bond_sites->nd==2);
  assert(bond_matrices->nd==1);

  uint64* basis_states_arr = NULL;
  double* norms_arr = NULL;
  uint64 n_basis_states = 0;
  assert(basis_states->nd==1);
  assert(norms->nd==1);
  if ((basis_states->dimensions[0] > 0) && (norms->dimensions[0] > 0))
    {
      basis_states_arr = reinterpret_cast<uint64*>(basis_states->data);
      norms_arr = reinterpret_cast<double*>(norms->data);
      n_basis_states = (uint64)basis_states->dimensions[0];
      assert(n_basis_states == (uint64)norms->dimensions[0]);
    }
  
  npy_intp *shape_perms = permutations->dimensions;
  npy_intp *shape_blochs = blochfactors->dimensions;
  npy_intp *shape_bond_sites = bond_sites->dimensions;
  // npy_intp *shape_bond_matrices = bond_matrices->dimensions;

  // Get permutations and blochfactors in proper format
  std::vector<complex> blochfactors_vec;
  for (uint32 i = 0; i < shape_blochs[0]; ++i)
    blochfactors_vec.push_back(blochs_arr[i]);
  
  std::vector<std::vector<uint32> > permutations_vec;
  for (uint32 i = 0; i < shape_perms[0]; ++i)
    {
      std::vector<uint32> sym;
      for (uint32 j = 0; j < shape_perms[1]; ++j)
	{
	  int p = perms_arr[i*shape_perms[1] + j];
	  assert(p >= 0);
	  sym.push_back(p);
	}
      permutations_vec.push_back(sym);
    }
  

  // Get bond_matrices in proper format
  uint32 local_dim=0;
  if (strcmp(type, "spinhalf") == 0) local_dim = 2;
  else if (strcmp(type, "spinone") == 0) local_dim = 3;
  else if (strcmp(type, "spinthreehalf") == 0) local_dim = 4;
  else if (strcmp(type, "spintwo") == 0) local_dim = 5;
  else if (strcmp(type, "u2") == 0) local_dim = 2;
  else if (strcmp(type, "u3") == 0) local_dim = 3;
  else if (strcmp(type, "u4") == 0) local_dim = 4;

  uint32 n_bonds = shape_bond_sites[0];
  uint32* n_sites_for_bond = new uint32[n_bonds];
  int** bond_sites_final = new int*[n_bonds];
  complex** bond_matrices_final = new complex*[n_bonds];

  uint32 bond_offset = shape_bond_sites[1];
  uint32 bond_matrix_offset = 0;
  for (uint32 i = 0; i < n_bonds; ++i)
    {
      n_sites_for_bond[i] = 0;
      while(bond_sites_arr[i*bond_offset + n_sites_for_bond[i]] != -1)
	++n_sites_for_bond[i];
      
      bond_sites_final[i] = bond_sites_arr + i*bond_offset;
      bond_matrices_final[i] = bond_matrices_arr + bond_matrix_offset;
      bond_matrix_offset += pow(local_dim, 2*n_sites_for_bond[i]);
    }
  assert(bond_matrix_offset == shape_bond_matrices[0]);
  
  // Dispatch get_operator
  uint64 n_entries;
  uint64 *rows, *cols;
  complex *data;
  if(strcmp(type, "spinhalf") == 0)
    dispatch_get_operator_symmetrized<HILBERTSPACE_SPINHALF_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       n_bonds, n_sites_for_bond, bond_sites_final, bond_matrices_final,
       &n_basis_states, &basis_states_arr, &norms_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "spinone") == 0)
    dispatch_get_operator_symmetrized<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       n_bonds, n_sites_for_bond, bond_sites_final, bond_matrices_final,
       &n_basis_states, &basis_states_arr, &norms_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "spinthreehalf") == 0)
    dispatch_get_operator_symmetrized<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       n_bonds, n_sites_for_bond, bond_sites_final, bond_matrices_final,
       &n_basis_states, &basis_states_arr, &norms_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "spintwo") == 0)
    dispatch_get_operator_symmetrized<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       n_bonds, n_sites_for_bond, bond_sites_final, bond_matrices_final,
       &n_basis_states, &basis_states_arr, &norms_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "u2") == 0)
    dispatch_get_operator_symmetrized<HILBERTSPACE_2_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       n_bonds, n_sites_for_bond, bond_sites_final, bond_matrices_final,
       &n_basis_states, &basis_states_arr, &norms_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "u3") == 0)
    dispatch_get_operator_symmetrized<HILBERTSPACE_3_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       n_bonds, n_sites_for_bond, bond_sites_final, bond_matrices_final,
       &n_basis_states, &basis_states_arr, &norms_arr,
       &n_entries, &rows, &cols, &data);
  else if (strcmp(type, "u4") == 0)
    dispatch_get_operator_symmetrized<HILBERTSPACE_4_TYPE>
      (n_sites, sz, permutations_vec, blochfactors_vec,
       n_bonds, n_sites_for_bond, bond_sites_final, bond_matrices_final,
       &n_basis_states, &basis_states_arr, &norms_arr,
       &n_entries, &rows, &cols, &data);
  
  // Free bond_matrices
  delete [] bond_sites_final;
  delete [] bond_matrices_final;
  delete [] n_sites_for_bond;

  // create numpy arrays
  npy_intp dims[1] = {(npy_intp)n_entries};
  PyObject* npy_rows = PyArray_SimpleNewFromData(1, dims, NPY_ULONGLONG, rows);
  Py_INCREF(npy_rows);
  PyObject* npy_cols = PyArray_SimpleNewFromData(1, dims, NPY_ULONGLONG, cols);
  Py_INCREF(npy_cols);
  PyObject* npy_data = PyArray_SimpleNewFromData(1, dims, NPY_COMPLEX128, data);
  Py_INCREF(npy_data);

  PyObject *rslt = PyTuple_New(3);
  PyTuple_SetItem(rslt, 0, npy_rows);
  PyTuple_SetItem(rslt, 1, npy_cols);
  PyTuple_SetItem(rslt, 2, npy_data);
  
  return rslt;
}

