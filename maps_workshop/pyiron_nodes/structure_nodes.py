from pyiron_workflow import as_function_node, as_macro_node, as_dataclass_node
from typing import Optional

@as_function_node
def CreateStructure(pr, element:str, bravais_lattice: Optional[str], a: Optional[float|int], c: Optional[float|int] = None, cubic:bool = False):
    """
    pr: pyiron_atomistics project
    bravais_lattice: e.g., "bcc" or "fcc" or "hcp"
    a: lattice constant in Angstrom
    c: height of hexagonal prism in Angstrom
    cubic: returns conventional unit cell instead of primitive for cubic structures (not to be used for non-cubic)
    """

    from pyiron_atomistics import Project
    
    pr = pr
    if bravais_lattice != 'hcp' and c == None:
        structure = pr.create.structure.bulk(element, crystalstructure=bravais_lattice, cubic=cubic, a=a)
    elif bravais_lattice == 'hcp' and c == None:
        structure = pr.create.structure.bulk(element, crystalstructure=bravais_lattice, cubic=cubic, a=a)
    else:
        structure = pr.create.structure.bulk(element, crystalstructure=bravais_lattice, cubic=cubic, a=a, c=c)
    
    return structure

@as_function_node("repeated_structre")
def RepeatStructure(structure, repetition_x: int, repetition_y: int, repetition_z: int):
    """
    structure: ase object from pyiron_atomistics
    """

    return structure.repeat([repetition_x, repetition_y, repetition_z])

@as_function_node("view")
def VisualizeStructure(structure):
    """
    structure: ase object from pyiron_atomistics
    """
    
    return structure.plot3d()