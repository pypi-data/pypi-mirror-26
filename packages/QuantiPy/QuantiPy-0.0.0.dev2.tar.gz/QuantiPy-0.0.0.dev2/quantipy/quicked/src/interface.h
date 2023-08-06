/*  @file interface.h
 *
 *  @author Alexander Wietek 
 *
 *  @brief Implementation of Python interface functions
 */
#ifndef __QUICKED_INTERFACE_H__
#define __QUICKED_INTERFACE_H__

#include <iostream>
#include <vector>
#include <math.h>

#include "HilbertSpace.h"
#include "SymmetryEngine.h"
#include "common.h"

namespace quicked { namespace interface
  {
    
    // Convert sz to n_upspins used in quantum number in Spin Hilbert spaces
    template <hilbert_t THilbertSpace>
    inline int sz_to_n_upspins(const uint32& n_sites, const int& sz);

    template <> inline int sz_to_n_upspins<HILBERTSPACE_SPINHALF_TYPE>
    (const uint32& n_sites, const int& sz)
    { return n_sites / 2 + sz; }
    template <> inline int sz_to_n_upspins<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
    (const uint32& n_sites, const int& sz)
    { return n_sites + sz; }
    template <> inline int sz_to_n_upspins<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
    (const uint32& n_sites, const int& sz)
    { return 3 * n_sites / 2 + sz; }
    template <> inline int sz_to_n_upspins<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
    (const uint32& n_sites, const int& sz)
    { return 2 * n_sites + sz; }
    template <> inline int sz_to_n_upspins<HILBERTSPACE_2_TYPE>
    (const uint32& n_sites, const int& sz)
    { return 0; }
    template <> inline int sz_to_n_upspins<HILBERTSPACE_3_TYPE>
    (const uint32& n_sites, const int& sz)
    { return 0; }
    template <> inline int sz_to_n_upspins<HILBERTSPACE_4_TYPE>
    (const uint32& n_sites, const int& sz)
    { return 0; }

    
    // max number up n_upspins
    template <hilbert_t THilbertSpace>
    inline int max_n_upspins(const uint32& n_sites);

    template <> inline int max_n_upspins<HILBERTSPACE_SPINHALF_TYPE>
    (const uint32& n_sites)
    { return n_sites; }
    template <> inline int max_n_upspins<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
    (const uint32& n_sites)
    { return 2 * n_sites; }
    template <> inline int max_n_upspins<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
    (const uint32& n_sites)
    { return 3 * n_sites; }
    template <> inline int max_n_upspins<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
    (const uint32& n_sites)
    { return 4 * n_sites; }
    template <> inline int max_n_upspins<HILBERTSPACE_2_TYPE>
    (const uint32& n_sites)
    { return 1; }
    template <> inline int max_n_upspins<HILBERTSPACE_3_TYPE>
    (const uint32& n_sites)
    { return 1; }
    template <> inline int max_n_upspins<HILBERTSPACE_4_TYPE>
    (const uint32& n_sites)
    { return 1; }
    

    // Get raw dimension of Hilbert spaces
    template <hilbert_t THilbertSpace>
    inline uint64 raw_dimension(const uint32& n_sites, const int& sz);

    template <> inline uint64 raw_dimension<HILBERTSPACE_SPINHALF_TYPE>
    (const uint32& n_sites, const int& sz)
    { return quicked::combinatorics::binomial(n_sites, n_sites / 2 + sz); }
    template <> inline uint64 raw_dimension<HILBERTSPACE_SPIN_ONE_GEN_TYPE>
    (const uint32& n_sites, const int& sz)
    { return quicked::combinatorics::bounded_partition(n_sites + sz, n_sites, 3); }
    template <> inline uint64 raw_dimension<HILBERTSPACE_SPIN_THREEHALF_GEN_TYPE>
    (const uint32& n_sites, const int& sz)
    { return quicked::combinatorics::bounded_partition(3 * n_sites / 2 + sz, n_sites, 4); }
    template <> inline uint64 raw_dimension<HILBERTSPACE_SPIN_TWO_GEN_TYPE>
    (const uint32& n_sites, const int& sz)
    { return quicked::combinatorics::bounded_partition(2 * n_sites + sz, n_sites, 5); }
    template <> inline uint64 raw_dimension<HILBERTSPACE_2_TYPE>
    (const uint32& n_sites, const int& sz)
    { return pow(2, n_sites); }
    template <> inline uint64 raw_dimension<HILBERTSPACE_3_TYPE>
    (const uint32& n_sites, const int& sz)
    { return pow(3, n_sites); }
    template <> inline uint64 raw_dimension<HILBERTSPACE_4_TYPE>
    (const uint32& n_sites, const int& sz)
    { return pow(4, n_sites);; }

    
    
    // Return all basis states (raw Hilbert space)
    template <hilbert_t THilbertSpace>
    void get_basis_states(const uint32& n_sites, const quantumnumber_t<THilbertSpace>& qn,
			  uint64 *n_basis_states, uint64 **basis_states)
    {
      std::vector<uint64> basis_state_vec;

      // Create all basis states
      HilbertSpace<THilbertSpace> hs(n_sites, qn);
      typedef typename HilbertSpace<THilbertSpace>::iterator iter_t;
      iter_t start = hs.begin();
      iter_t end = hs.end();
      for(iter_t state = hs.begin(); state != hs.end(); ++state)
	basis_state_vec.push_back(*state);

      // Fill C array from C++ vector
      *basis_states = new uint64[basis_state_vec.size()];
      std::copy(basis_state_vec.begin(), basis_state_vec.end(), *basis_states);
      *n_basis_states = basis_state_vec.size();
    }

    
    // Return all basis states and norms (of the symmetrized Hilbert space)
    template <hilbert_t THilbertSpace, template <hilbert_t> class TLocalSymmetry >
    void get_basis_states_symmetrized
    (const uint32& n_sites, const quantumnumber_t<THilbertSpace>& qn,
     const SymmetryEngine<THilbertSpace, TLocalSymmetry<THilbertSpace> >& symmetry_engine,
     uint64 *n_basis_states, uint64 **basis_states, double **norms)
    {
      // Create all basis states
      std::vector<uint64> basis_states_vec;
      std::vector<double> norms_vec;
      HilbertSpace<THilbertSpace> hs(n_sites, qn);
      typedef typename HilbertSpace<THilbertSpace>::iterator iter_t;
      iter_t start = hs.begin();
      iter_t end = hs.end();
      for(iter_t state = hs.begin(); state != hs.end(); ++state)
	{
	  // Find if state is representative
	  uint64 rep;
	  complex coeff;
	  symmetry_engine.find_representative(*state, &rep, &coeff);
	  if (*state==rep)
	    {
	      // Compute norm
	      complex amplitude = 0.0;
	      for (uint32 symcnt = 0; symcnt < symmetry_engine.n_symmetries(); ++symcnt)
		{
		  uint64 derivedstate;
		  complex coeff;
		  symmetry_engine.apply_symmetry(rep, symcnt, &derivedstate, &coeff);
		  if(derivedstate == rep)
		    amplitude += coeff;
		}
	      // Append if non-zero norm
	      if (std::abs(amplitude) > 1e-6)
		{
		  basis_states_vec.push_back(rep);
		  norms_vec.push_back(std::sqrt(std::abs(amplitude)));
		}     
	    } 
	}

      // Fill C arrays from C++ vectors
      *basis_states = new uint64[basis_states_vec.size()];
      std::copy(basis_states_vec.begin(), basis_states_vec.end(), *basis_states);
      *n_basis_states = basis_states_vec.size();
      basis_states_vec.clear();

      *norms = new double[norms_vec.size()];
      std::copy(norms_vec.begin(), norms_vec.end(), *norms);
      norms_vec.clear();      
    }


    template <hilbert_t THilbertSpace>
    void get_operator
    (const uint64& n_basis_states, const uint64* basis_states,
     const uint32& n_bonds, const uint32* n_sites_for_bonds,
     int** bond_sites, complex** bond_matrices,
     uint64* n_entries, uint64** rows, uint64** cols, complex** data)
    {
      const uint32 local_dim = local_dimension<THilbertSpace>();

      std::vector<uint64> rows_vec, cols_vec;
      std::vector<complex> data_vec;
      for (uint32 bond_idx = 0; bond_idx < n_bonds; ++bond_idx)
	{
	  const uint32 n_sites_for_bond = n_sites_for_bonds[bond_idx];
	  const complex* bond_matrix = bond_matrices[bond_idx];
	  const uint32 bond_matrix_dim = pow(local_dim, n_sites_for_bond);

	  uint32 local_vals[n_sites_for_bond];

	  for (uint64 state_idx = 0; state_idx < n_basis_states; ++ state_idx)
	    {
	      const uint64 state = basis_states[state_idx];

      	      // get index of current state in bond
      	      for (uint32 i = 0; i < n_sites_for_bond; ++i)
      		local_vals[i] = get_site_value<THilbertSpace>(state, bond_sites[bond_idx][i]);
      	      const uint32 index = quicked::utils::index_multisite(n_sites_for_bond, local_vals,
								   local_dim);
	      // std::cout << "local_vals: ";
	      // for (uint32 i = 0; i < n_sites_for_bond; ++i)
	      // 	std::cout << local_vals[i]<< " ";
	      // std::cout << std::endl;

      	      // Apply bond matrix
      	      for (uint32 new_index = 0; new_index < bond_matrix_dim; ++new_index)
      		if (std::abs(bond_matrix[index*bond_matrix_dim + new_index]) > 1e-12)
      		  {
		    // Diagonal bonds
		    if (new_index == index)
		      {
			rows_vec.push_back(state_idx);
			cols_vec.push_back(state_idx);
			data_vec.push_back(bond_matrix[index*bond_matrix_dim + new_index]);
		      }
		    
		    // Offdiagonal bonds
		    else
		      {
				
			// Create new_state
			uint32 new_local_vals[n_sites_for_bond];
			quicked::utils::localvals_multisite(new_index, n_sites_for_bond,
							    local_dim, new_local_vals);
			uint64 new_state = state;
			for (uint32 j =0; j < n_sites_for_bond; ++j)
			  set_site_value<THilbertSpace>(&new_state, bond_sites[bond_idx][j],
							new_local_vals[j]);
		
			// get index of representative using binary search
			uint32 new_state_idx =
			  std::lower_bound(basis_states, basis_states + n_basis_states, new_state)
			  - basis_states;

			// Check whether representative is present in basis states
			assert(basis_states[new_state_idx] == new_state);

			rows_vec.push_back(state_idx);
			cols_vec.push_back(new_state_idx);
			data_vec.push_back(bond_matrix[index*bond_matrix_dim + new_index]);
			
		      } // end: offdiagonal
		  } // end: loop over bondmatrix
      	    } // end: loop over states
      	} // end: loop over bonds


      // Fill C arrays from C++ vectors
      *n_entries = rows_vec.size();
      assert(rows_vec.size() == cols_vec.size());
      assert(cols_vec.size() == data_vec.size());
      
      *rows = new uint64[rows_vec.size()];
      std::copy(rows_vec.begin(), rows_vec.end(), *rows);
      rows_vec.clear();

      *cols = new uint64[cols_vec.size()];
      std::copy(cols_vec.begin(), cols_vec.end(), *cols);
      cols_vec.clear();

      *data = new complex[data_vec.size()];
      std::copy(data_vec.begin(), data_vec.end(), *data);
      data_vec.clear();
    }
    

    template <hilbert_t THilbertSpace, class TSymmetryEngine>
    void get_operator_symmetrized
    (const TSymmetryEngine& symmetry_engine,
     const uint64& n_basis_states, const uint64* basis_states, const double* norms,
     const uint32& n_bonds, const uint32* n_sites_for_bonds, int** bond_sites,
     complex** bond_matrices,
     uint64* n_entries, uint64** rows, uint64** cols, complex** data)
    {
      const uint32 local_dim = local_dimension<THilbertSpace>();

      std::vector<uint64> rows_vec, cols_vec;
      std::vector<complex> data_vec;
      for (uint32 bond_idx = 0; bond_idx < n_bonds; ++bond_idx)
	{
	  const uint32 n_sites_for_bond = n_sites_for_bonds[bond_idx];
	  const complex* bond_matrix = bond_matrices[bond_idx];
	  const uint32 bond_matrix_dim = pow(local_dim, n_sites_for_bond);
	  uint32 local_vals[n_sites_for_bond];
	  
	  for (uint64 state_idx = 0; state_idx < n_basis_states; ++ state_idx)
	    {
	      const uint64 state = basis_states[state_idx];

      	      // get index of current state in bond
      	      for (uint32 i = 0; i < n_sites_for_bond; ++i)
		local_vals[i] = get_site_value<THilbertSpace>(state, bond_sites[bond_idx][i]);
      	      const uint32 index = quicked::utils::index_multisite(n_sites_for_bond, local_vals,
								   local_dim);

      	      // Apply bond matrix
      	      for (uint32 new_index = 0; new_index < bond_matrix_dim; ++new_index)
      		if (std::abs(bond_matrix[index*bond_matrix_dim + new_index]) > 1e-12)
      		  {
		    
		    // Diagonal bonds
		    if (new_index == index)
		      {
			rows_vec.push_back(state_idx);
			cols_vec.push_back(state_idx);
			data_vec.push_back(bond_matrix[index*bond_matrix_dim + new_index]);
		      }
		    
		    // Offdiagonal bonds
		    else
		      {
				
			// Create new_state
			uint32 new_local_vals[n_sites_for_bond];
			quicked::utils::localvals_multisite(new_index, n_sites_for_bond,
							    local_dim, new_local_vals);
			uint64 new_state = state;
			for (uint32 j =0; j < n_sites_for_bond; ++j)
			  set_site_value<THilbertSpace>(&new_state, bond_sites[bond_idx][j],
							new_local_vals[j]);
			// get representative
			uint64 rep;
		    	complex bloch;
			symmetry_engine.find_representative(new_state,&rep, &bloch);

			// get index of representative using binary search
			uint32 rep_idx =
			  std::lower_bound(basis_states, basis_states + n_basis_states, rep)
			  - basis_states;
			
			// Check whether representative is present in basis states
			assert(basis_states[rep_idx] == rep);

			// // DEBUG
			// uint32 n_sites = symmetry_engine.n_sites();
			// std::cout << "state: "
			// 	  << quicked::state_string<THilbertSpace>(state, n_sites)
			// 	  << std::endl;
			// std::cout << "bond_sites[bond_idx]: ";
			// for (uint32 i = 0; i < n_sites_for_bond; ++i)
			//   std::cout << bond_sites[bond_idx][i]<< " ";
			// std::cout << std::endl;
			// std::cout << "index " << index << std::endl;
			// std::cout << "local_vals: ";
			// for (uint32 i = 0; i < n_sites_for_bond; ++i)
			//   std::cout << local_vals[i]<< " ";
			// std::cout << std::endl;
			// std::cout << "new_index " << new_index << std::endl;
			// std::cout << "new_local_vals: ";
			// for (uint32 i = 0; i < n_sites_for_bond; ++i)
			//   std::cout << new_local_vals[i]<< " ";
			// std::cout << std::endl;
			// std::cout << "new_state: "
			// 	  << quicked::state_string<THilbertSpace>(new_state, n_sites)
			// 	  << std::endl;
			// std::cout << "rep: "
			// 	  << quicked::state_string<THilbertSpace>(rep, n_sites)
			// 	  << std::endl;
			// std::cout << "bond_matrix[index*bond_matrix_dim + new_index] "
			// 	  << bond_matrix[index*bond_matrix_dim + new_index]
			// 	  << std::endl;
			// std::cout << "bloch " << bloch << std::endl;
			// std::cout << "norms[rep_idx] " << norms[rep_idx] << std::endl;
			// std::cout << "norms[state_idx] " << norms[state_idx] << std::endl;
			// exit(1);

			if (rep_idx != n_basis_states)
			  {
			    rows_vec.push_back(state_idx);
			    cols_vec.push_back(rep_idx);
			    data_vec.push_back(bond_matrix[index*bond_matrix_dim + new_index] *
					       bloch * norms[rep_idx] / norms[state_idx]);
			  }
			
		      } // end: offdiagonal
		  } // end: loop over bondmatrix
      	    } // end: loop over states
      	} // end: loop over bonds
      
      // Fill C arrays from C++ vectors
      *n_entries = rows_vec.size();
      assert(rows_vec.size() == cols_vec.size());
      assert(cols_vec.size() == data_vec.size());
      
      *rows = new uint64[rows_vec.size()];
      std::copy(rows_vec.begin(), rows_vec.end(), *rows);
      rows_vec.clear();

      *cols = new uint64[cols_vec.size()];
      std::copy(cols_vec.begin(), cols_vec.end(), *cols);
      cols_vec.clear();

      *data = new complex[data_vec.size()];
      std::copy(data_vec.begin(), data_vec.end(), *data);
      data_vec.clear();
    }
      
    
  } // namespace interface
} // namespace quicked

#endif
