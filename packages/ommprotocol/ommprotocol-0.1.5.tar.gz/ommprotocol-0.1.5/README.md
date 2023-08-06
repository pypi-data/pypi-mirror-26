ommprotocol
===========

[![DOI](https://zenodo.org/badge/50431234.svg)](https://zenodo.org/badge/latestdoi/50431234)

A command line application to launch MD protocols with OpenMM

*By Jaime Rodríguez-Guerra ([@jaimergp](https://github.com/jaimergp)). Contributors: Lur Alonso*

Some cool features
------------------

+ No coding required - just a YAML input file!
+ Smart support for different input file formats:
  + __Topology__: PDB/PDBx, Mol2, Amber's PRMTOP, Charmm's PSF, Gromacs' TOP, Desmond's DMS
  + __Positions__: PDB, COOR, INPCRD, CRD, GRO
  + __Velocities__: PDB, VEL
  + __Box vectors__: PDB, XSC, CSV, INPCRD, GRO
  + *A fallback method is implemented and will attempt to load verything else that might be supported by [ParmEd](http://parmed.github.io/ParmEd/html/index.html).*
+ Choose your preferred **trajectory** format (PDB, PDBx, DCD, HDF5, NETCDF, MDCRD) and **checkpoints** (Amber restart, OpenMM XML states, restart).
+ Live report of simulation progress, with estimated ETA and speed.
+ Checkpoint every *n* steps. Also, emergency rescue files are created if an error occurs.
+ Autochunk the trajectories for easy handling.

Installation
------------

1. Download and install [Miniconda](http://conda.pydata.org/miniconda.html), a tiny Python distribution with a cool package manager and installer. Check [its webpage](http://conda.pydata.org/docs/) for more info.

        wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
        bash Miniconda3*.sh

2. Restart terminal and add `omnia` and `insilichem` to the channels list.

        conda config --add channels omnia
        conda config --add channels insilichem

3. Install `ommprotocol`:

        conda install ommprotocol

    Optionally, you can use a separate environment called `openmm`, and then activate it when required.

        conda create -n openmm ommprotocol
        source activate openmm

4. If everything is OK, this sould run correctly.

        ommprotocol -h

Usage
-----

Quick launch:

    ommprotocol <inputfile.yaml>

All input configuration is done through YAML files. A couple of sample inputs are included in [`examples`](examples/) folder; parameters should be self-explaining.

There's two main parts in these files: 

* Top-level parameters: listed in next section, they are common for all stages
* `stages`: Contains a list with all the stages to be simulated in the requested order. Each stage can override one or more global parameter(s), if needed.


Available parameters
--------------------

The following keys are available for the input file. They are listed in different categories, but you can mix them up as you want. If an optional key is not provided, it will be set to the default value.

### Input options

- `topology`: Main input file. Should contain, at least, the topology, but it can also contain positions, velocities, PBC vectors, forcefields...
- `positions`: File with the initial coordinates of the system. Overrides those in topology, if needed.
- `velocities`: File containing the initial velocities of this stage. If not set, they will be set to the requested temperature. 
- `box_vectors`: File with replacement periodic box vectors, instead of those in the topology or positions file. Supported file types: XSC.
- `forcefield`: Which forcefields should be used, if not provided in topology. Needed for PDB topologies and CHARMM PSF.
- `checkpoint`: Restart simulation from this file. It can provide one or more of the options above. 

### Output options

- `project_name`: Name for this simulation.
- `outputpath`: Path to output folder. If relative, it'll be relative to input file. 
- `report`: True for live report of progress.
- `report_every`: Update interval of live progress reports.
- `trajectory`: Output format of trajectory file, if desired.
- `trajectory_every`: Write trajectory every n steps.
- `trajectory_new_every`: Create a new file for trajectory every n steps.
- `restart`: Output format for restart formats, if desired
- `restart_every`: Write restart format every n steps.
- `save_state_at_end`: Whether to save the state of the simulation at the end of every stage.
- `attempt_rescue`: Try to dump the simulation state into a file if an exception occurs.

### General conditions of simulation

- `minimization`: If *True*, minimize before simulating a MD stage.
- `steps`: Number of MD steps to simulate. If 0, no MD will take place.
- `timestep`: Integration timestep, in fs. Defaults to 1.0.
- `temperature`: In Kelvin. 300 by default.
- `barostat`: *True* for NPT, *False* for NVT.
- `pressure`: In bar. Only used if barostat is *True*.
- `barostat_interval`: Update interval of barostat, in steps.
- `restrained_atoms`, `constrained_atoms`: Parts of the system that should remain restrained (a force is applied to minimize movement) or constrained (no movement at all) during the simulation. Supports `mdtraj`'s [DSL queries](http://mdtraj.org/latest/atom_selection.html) or a list of 0-based atom indices.
- `restraint_strength`: If restraints are in use, the strength of the applied force in kJ/mol. Defaults to 5.0.
- `integrator`: Which integrator should be used. Langevin by default.
- `friction`: Friction coefficient for integrator, if needed. In 1/ps. Defaults to 1.0.
- `minimization_tolerance` : Threshold value minimization should converge to.
- `minimization_max_iterations` : Limit minimization iterations up to this value. If zero, don't limit.

### OpenMM simulation parameters

- `nonbondedMethod`: Choose between *NoCutoff*, *CutoffNonPeriodic*, *CutoffPeriodic*, *Ewald*, *PME*.
- `nonbondedCutoff`: In nm. Defaults to 1.0.   
- `constraints`: Choose between *null*, *HBonds*, *AllBonds*, *HAngles*.
- `rigidWater`: *True* or *False*.
- `removeCMMotion`: Whether to remove center of mass motion during simulation. Defaults to *True*.  
- `hydrogenMass`: The mass to use for hydrogen atoms bound to heavy atoms. Any mass added to a hydrogen is subtracted from the heavy atom to keep their total mass the same.
- `extra_system_options`: A sub-dict with additional keywords that might be supported by the `.createSystem` method of the topology in use. Check the [OpenMM docs](http://docs.openmm.org/7.1.0/api-python/app.html#loaders-and-setup) to know which ones to use.

### Hardware options

- `platform`: Which platform to use: *CPU*, *CUDA*, *OpenCL*. If not set, OpenMM will choose the fastest available.
- `platform_properties`: A sub-dict of keyworkds to configure the chosen platform. Check the [OpenMM docs](http://docs.openmm.org/7.1.0/api-python/generated/simtk.openmm.openmm.Platform.html#simtk.openmm.openmm.Platform) to know the supported values. Please notice all values must be strings, even booleans and ints; as a result, you should quote the values like this `'true'`.

### Stage-only parameters

- `name`: A name for this stage. 

## Get help

If you have problems running `ommprotocol`, feel free to [create an issue](https://github.com/insilichem/ommprotocol/issues)! Also, make sure to visit our main webpage at [www.insilichem.com](www.insilichem.com).

## Citation

[![DOI](https://zenodo.org/badge/50431234.svg)](https://zenodo.org/badge/latestdoi/50431234)

Ommprotocol is scientific software, funded by public research grants (Spanish MINECO's project ``CTQ2014-54071-P``, Generalitat de Catalunya's project ``2014SGR989`` and research grant ``2015FI_B00768``, COST Action ``CM1306``). If you make use of Ommprotocol in scientific publications, please cite it. It will help measure the impact of our research and future funding!

```
@misc{ommprotocol2017,
  author       = {Jaime Rodríguez-Guerra Pedregal and 
                  Daniel Soler and 
                  Lur Alonso-Cotchico and
                  Lorea Velasco and 
                  Jean-Didier Maréchal},
  title        = {Ommprotocol: A command line application to launch MD protocols with OpenMM},
  month        = apr,
  year         = 2017,
  doi          = {10.5281/zenodo.546882},
  url          = {https://doi.org/10.5281/zenodo.546882}
}
```