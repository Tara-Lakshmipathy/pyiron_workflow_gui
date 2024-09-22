from pyiron_workflow import as_function_node
from typing import Optional

from ase import Atoms


@as_function_node("plot")
def Plot3d(structure: Atoms, particle_size: Optional[int|float] = 1):
    return structure.plot3d(particle_size=particle_size)
