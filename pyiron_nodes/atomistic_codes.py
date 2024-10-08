from ase import Atoms
from pyiron_workflow import as_macro_node

from pyiron_nodes.atomistic.engine.lammps import get_calculators
from pyiron_nodes.dev_tools import set_replacer


@as_macro_node("generic")
def Lammps(wf, structure=Atoms(), potential=None):
    from pyiron_contrib.tinybase.shell import ExecutablePathResolver

    wf.Potential = wf.create.atomistic.engine.lammps.Potential(
        structure=structure, name=potential
    )

    wf.ListPotentials = wf.create.atomistic.engine.lammps.ListPotentials(
        structure=structure
    )

    # wf.calc = wf.create.atomistic.engine.lammps.CalcStatic()
    # wf.calc_select = set_replacer(wf.calc, get_calculators())

    wf.InitLammps = wf.create.atomistic.engine.lammps.InitLammps(
        structure=structure,
        potential=wf.Potential,
        # calculator=wf.calc.outputs.calculator,
        calculator=calculator,
        # working_directory="test2",
    )
    wf.InitLammps.inputs.working_directory = (
        wf.InitLammps.working_directory.path.__str__()
    )
    wf.Shell = wf.create.atomistic.engine.lammps.Shell(
        command=ExecutablePathResolver(module="lammps", code="lammps").path(),
        working_directory=wf.InitLammps.outputs.path,
    )

    wf.ParseLogFile = wf.create.atomistic.engine.lammps.ParseLogFile(
        log_file=wf.Shell.outputs.log
    )
    wf.ParseDumpFile = wf.create.atomistic.engine.lammps.ParseDumpFile(
        dump_file=wf.Shell.outputs.dump
    )
    wf.Collect = wf.create.atomistic.engine.lammps.Collect(
        out_dump=wf.ParseDumpFile.outputs.dump,
        out_log=wf.ParseLogFile.outputs.log,
        calc_mode=calculator,  # wf.calc.mode,  # SVN gives output -> inject attribute getter node
    )

    return wf.Collect
