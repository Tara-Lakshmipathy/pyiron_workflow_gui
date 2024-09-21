from pyiron_workflow import as_function_node
from typing import Optional

@as_function_node("plotter")
def plot_init_mesh_object(function_space):
    import pyvista
    from dolfinx.plot import vtk_mesh
    from dolfinx import mesh, fem, plot, io, default_scalar_type
    
    pyvista.start_xvfb()

    V = function_space
    plotter = pyvista.Plotter()
    topology, cell_types, geometry = plot.vtk_mesh(V)
    grid = pyvista.UnstructuredGrid(topology, cell_types, geometry)
    plotter.add_mesh(grid, show_edges=True)
    #return plotter.show(return_viewer=True)
    return plotter

@as_function_node("plotter")
def plot_one_d_deformed_mesh_object(function_space, solution_vector, factor: Optional[float | int]):
    import pyvista
    from dolfinx.plot import vtk_mesh
    from dolfinx import fem, default_scalar_type
    
    pyvista.start_xvfb()

    topology, cell_types, x = vtk_mesh(function_space)
    grid = pyvista.UnstructuredGrid(topology, cell_types, x)
    grid.point_data["u"] = solution_vector.x.array
    warped = grid.warp_by_scalar("u", factor=factor)
    plotter = pyvista.Plotter()
    plotter.add_mesh(warped, show_edges=True, show_scalar_bar=True, scalars="u")
    return plotter
    