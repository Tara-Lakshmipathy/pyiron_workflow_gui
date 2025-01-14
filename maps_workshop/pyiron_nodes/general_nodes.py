from pyiron_workflow import as_function_node, as_macro_node, as_dataclass_node


@as_function_node
def CreateProject(pr_name: str):
    """
    pr: name of project
    """
    
    from pyiron_atomistics import Project
    
    pr = Project(pr_name)
    print("Project name: \"" + pr_name + "\"")
    
    return pr