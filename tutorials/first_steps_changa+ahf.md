Tangos Tutorial – Changa + AHF
==============================

Initial set up
--------------

Make sure you have followed the [initial set up instructions](../README.md). Then download the
[raw simulation data](http://star.ucl.ac.uk/~app/tangos/tutorial_changa.tar.gz) required for this tutorial.
Unpack the tar file either in your home folder or the folder that you pointed the `TANGOS_SIMULATION_FOLDER` environment
variable to.

Import the simulation
---------------------

At the unix command line type:

```
tangos_manager add tutorial_changa
```

The process should take about a minute on a standard modern computer, during which you'll see a bunch of log messages 
scroll up the screen.
 
 Let's pick this command apart
 
  * `tangos_manager` is the command-line tool to administrate your tangos database
  * `add` is a subcommand to add a new simulation
  * `tutorial_changa` identifies the simulation we're adding
 
Note that all _tangos_ command-line tools provide help. For example `tangos_manager --help` will show you all subcommands, and `tangos_manager add --help` will tell you more about the possible options for adding a simulation.
  
At this point, the database knows about the existence of timesteps and their halos in our simulation, but nothing about the properties of those halos or groups. We need to add more information before the database is useful.


Import some AHF-defined properties
----------------------------------

At the unix command line type:

```
tangos_import_from_ahf Mvir Rvir --sims tutorial_changa
```

The process should take less than a minute on a standard modern computer, during which you'll see a bunch of log messages scroll up the screen.

The example command line lists two properties, `Mvir` and `Rvir` to import from the stat files. The added directive 
`--sims pioneer50h128.1536gst1.bwK1` specifies which simulation you want to apply this operation to. It's not strictly
necessary to add this if you only have one simulation in your database.

Generate the merger trees
-------------------------

The merger trees are most simply generated using pynbody's bridge function to do this, type

```
tangos_timelink --sims tutorial_changa
```

which builds the merger tree for the halos. Again, the `--sims tutorial_changa` may be omitted if it's the
only simulation in your tangos database. Note that in this tutorial, only a few timesteps are provided. This makes the merger
trees a little boring (see the Ramses and Gadget tutorial datasets for more interesting merger trees).

The construction of each merger tree should take a few minutes,  and again you'll see a log scroll up the screen while it happens.

If you want to speed up this process, it can be [MPI parallelised](mpi.md).

Add the first property
----------------------
 
Next, we will add some properties to the halos so that we can start to do some science. Because this is a _zoom_ simulation,
we only want to do science on the highest resolution regions. The first thing to calculate is therefore which halos fall
in that region. From your shell type:
```bash
tangos_writer contamination_fraction --sims tutorial_changa
```

Here,
 * `tangos_writer` is the main script for adding properties to a tangos database;
 * `contamination_fraction` is the name of a built-in property which returns the fraction of dark matter particles
   which come from outside the high resolution region.
   
If you want to speed up this process, it can be [MPI parallelised](mpi.md).

If you want to see how your database is looking, you can skip ahead to [data exploration](#explore-whats-possible), 
though so far there's not a huge amount of interest to see. 

Add some more interesting properties
------------------------------------

Let's finally do some science. We'll add density profiles and thumbnail images; 
from your shell type:
 
```bash
tangos_writer dm_density_profile gas_density_profile uvi_image --with-prerequisites --include-only="contamination_fraction<0.01 & NDM()>5000" --sims tutorial_changa  
```

Here,
 * `tangos_writer` is the same script you called above to add properties to the database
 * `dm_density_profile` is an array representing the dark matter density profile; to see all available properties
   you can call `tangos_manager list-possible-haloproperties`
 * `--with-prerequisites` automatically includes  any underlying properties that are required to perform the calculation. In this case,
   the `dm_density_profile` calculation actually needs to know an accurate center for the halo (known as `shrink_center`),
   so that calculation will be automatically performed and stored
 * `--include-only` allows an arbitrary filter to be applied, specifying which halos the properties should be calculated
   for. In the present case, we use that to insist that only "high resolution" halos are included (specifically, those
   with a fraction of low-res particles smaller than 1%) – and, more than that, there must be 5000 dark matter particles
   in a halo before we calculate these properties (otherwise it's too small for us to care). 
   
   
This is the slowest process in all the _tangos_ tutorials; there is a 
[specific example](mpi.md#tangos_writer_example) in the [MPI parallelisation document](mpi.md) showing how to make
best use of a multi-core system to speed things up.
   
Tangos error handling
---------------------

While running this case the log may contain some errors such as 
`Number of smoothing particles exceeds number of particles in tree`. Don't panic, this is normal! You're seeing
the effect of attempting to smooth over a very small number of star or gas particles in some tiny halos. 

If keen, one can alter the `--include-only` clause to prevent any such errors occuring but it's not really necessary: 
_tangos_ isolates errors that occur in individual halo calculations; it reports them and then moves onto the next
calculation or halo. 


Explore what's possible
-----------------------
 
Now that you have a minimal functioning _tangos_ database, proceed to the data exploration tutorial, either with the
[web server](data_exploration_python.md) or [python interface](data_exploration_python.md).