from pyiron_workflow import as_function_node, as_macro_node, as_dataclass_node
from typing import Optional
import matplotlib.pylab as plt

@as_function_node("animation")
def AnimateStructure(job):
    """
    job: pyiron_atomistics job
    """
    
    return job.animate_structures()

@as_function_node("plot")
def PlotTemperatureSteps(job):
    """
    job: pyiron_atomistics job
    """
    
    temperatures = job.output.temperature
    steps = job.output.steps
    plt.plot(steps, temperatures)
    plt.xlabel('MD step')
    plt.ylabel('Temperature [K]');
    
    return plt.show()

@as_function_node("plot")
def PlotVolumeSteps(job):
    """
    job: pyiron_atomistics job
    """
    
    volumes = job.output.volume
    steps = job.output.steps
    plt.plot(steps, volumes)
    plt.xlabel('MD step')
    plt.ylabel('Volume [A^3]');
    
    return plt.show()

@as_function_node("plot")
def PlotPotentialEnergySteps(job):
    """
    job: pyiron_atomistics job
    """
    
    energy_pot = job.output.energy_pot
    steps = job.output.steps
    plt.plot(steps, energy_pot)
    plt.xlabel('MD step')
    plt.ylabel('Potential energy [eV]');
    
    return plt.show()

@as_function_node("plot")
def PlotTotalEnergySteps(job):
    """
    job: pyiron_atomistics job
    """
    
    energy_tot = job.output.energy_tot
    steps = job.output.steps
    plt.plot(steps, energy_tot)
    plt.xlabel('MD step')
    plt.ylabel('Total energy [eV]');
    
    return plt.show()

@as_function_node("plot")
def PlotPressureSteps(job):
    """
    job: pyiron_atomistics job
    """
    
    press_xx = [tensor[0,0] for tensor in job.output.pressures]
    press_yy = [tensor[1,1] for tensor in job.output.pressures]
    press_zz = [tensor[2,2] for tensor in job.output.pressures]
    steps = job.output.steps
    plt.plot(steps, press_xx, label="pressure_xx")
    plt.plot(steps, press_yy, label="pressure_yy")
    plt.plot(steps, press_zz, label="pressure_zz")
    plt.xlabel('MD step')
    plt.ylabel('Pressure [bar]');
    plt.legend(loc='best')
    
    return plt.show()

@as_function_node("results")
def MurnaghanResults(murn):
    """
    murn: murnagha job
    """

    from IPython.display import display
    
    display(murn.plot())
    
    return murn.output_to_pandas()