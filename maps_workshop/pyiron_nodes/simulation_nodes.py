from pyiron_workflow import as_function_node, as_macro_node, as_dataclass_node
from typing import Optional

@as_function_node
def LammpsCalcMinimize(pr, structure, job_name:str, pot_list_index:int, f_tol: Optional[float|int], min_style:str, del_ex_job:bool = False):
    """
    pr: pyiron_atomistics project
    structure: ase object from pyiron_atomistics
    pot_list_index: chosen potential from list
    f_tol: force tolerance for convergence
    min_style: minimization algorithm e.g., "fire", "cg", "quickmin" etc.
    del_ex_job: delete existing job?
    """
    
    pr = pr
    structure = structure
    job = pr.create.job.Lammps(job_name=job_name, delete_existing_job=del_ex_job)
    job.structure = structure.copy()
    job.potential = job.list_potentials()[pot_list_index]
    job.calc_minimize(ionic_force_tolerance=f_tol)
    print("Job name: \"" + job_name + "\"")
    print("Chosen potential: " + job.list_potentials()[pot_list_index])
    
    return job

@as_function_node
def LammpsMD(pr, structure, job_name:str, pot_list_index:int, temperature: Optional[float|int], pressure:Optional[float|int], n_ionic_steps: int, del_ex_job:bool = False):
    """
    pr: pyiron_atomistics project
    structure: ase object from pyiron_atomistics
    pot_list_index: chosen potential from list
    temperature: target temperature of MD simulation
    pressure: target pressure of MD simulation
    n_ionic_steps: total number of md steps to be simulated
    del_ex_job: delete existing job?
    """
    
    pr = pr
    structure = structure
    job = pr.create.job.Lammps(job_name=job_name, delete_existing_job=del_ex_job)
    job.structure = structure.copy()
    job.potential = job.list_potentials()[pot_list_index]
    job.calc_md(temperature=temperature, pressure=pressure, n_ionic_steps=n_ionic_steps)
    print("Job name: \"" + job_name + "\"")
    print("Chosen potential: " + job.list_potentials()[pot_list_index])

    return job

@as_function_node("potential_list")
def LammpsPotList(job):
    """
    job: pyiron_atomistics job
    """
    
    return job.list_potentials()

@as_function_node("completed_job")
def LammpsJobRun(job):
    """
    job: pyiron_atomistics job
    """

    job.run()
    return job

@as_function_node
def MurnaghanJob(pr, job, murn_job_name:str, n_sample_points:int, equation_of_state:str, fit_order:int, volume_range:float|int, 
                 del_ex_job:bool = False):
    """
    pr: pyiron_atomistics project
    job: pyiron_atomistics job
    n_sample_points: number of iterations
    equation_of_state: "murnaghan", "birchmurnaghan", "polynomial", "birch", "vinet"
    fit_order: order of fit if polynomial
    volume_range: volumetric strain range for iterations
    """
    
    pr = pr
    murn = job.create_job(job_type=pr.job_type.Murnaghan, job_name=murn_job_name, delete_existing_job=del_ex_job)
    murn.input['fit_type'] = equation_of_state
    murn.input['num_points'] = n_sample_points
    murn.input['fit_order'] = fit_order
    murn.input['vol_range'] = volume_range
    murn.run()
    
    return murn

@as_dataclass_node
class MurnaghanParameters():
    murn_job_name: Optional[str] = 'murn'
    n_sample_points: Optional[int] = 7
    equation_of_state: Optional[str] = 'birchmurnaghan'
    fit_order: Optional[int] = 3
    volume_range: Optional[float|int] = 0.05
    job_name: Optional[str] = 'el_str'
    pot_list_index: Optional[int] = 0
    f_tol: Optional[float|int] = 1e-6
    min_style: Optional[str] = 'cg'

@as_macro_node("murn")
def MurnaghanLammpsMacro(self, pr, structure, parameters: Optional[MurnaghanParameters.dataclass] = MurnaghanParameters.dataclass(), del_ex_job:bool = False):
    """
    pr: pyiron_atomistics project
    structure: ase object from pyiron_atomistics
    parameters: MunaghanParameters dataclass
    del_ex_job: delete existing job?
    """
    
    self.engine = LammpsCalcMinimize(pr, structure, parameters.job_name, parameters.pot_list_index, parameters.f_tol, parameters.min_style, del_ex_job)
    
    self.murn = MurnaghanJob(pr, self.engine, parameters.murn_job_name, parameters.n_sample_points, parameters.equation_of_state, parameters.fit_order, parameters.volume_range, del_ex_job)
    
    return self.murn