import ast

def stringlist_to_list(v: str) -> list | str:
    """
    In case a list in pd.Series is turned into a string representation of a list
    This function turns it back to a list   
    """ 
    if isinstance(v, str) and v.startswith('[') and v.endswith(']'):
        return ast.literal_eval(v)
    else:
        return v
