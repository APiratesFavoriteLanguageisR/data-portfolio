import time
import logging

def run_stage( stage_name: str, stage_function: callable, *args, **kwargs):
    """
    Utility function to run a pipeline stage with standardized logging and error handling.

    Parameters
    ----------
    stage_name : str
        Name of the pipeline stage (e.g., "Extract", "Transform", "Load").
    stage_function : callable
        Function that implements the logic for the stage. It should accept the provided args and kwargs.
    *args
        Positional arguments to pass to the stage function.
    **kwargs
        Keyword arguments to pass to the stage function.

    Returns
    -------
    Any
        The output of the stage function, if it completes successfully.

    Raises
    ------
    Exception
        If any error occurs during the execution of the stage function, it will be logged and re-raised.
    """
    
    logging.info(f"Starting stage: {stage_name}")
    
    start_time = time.perf_counter()
    
    try:
        result = stage_function(*args, **kwargs)
        end_time = time.perf_counter()
        logging.info(f"Completed stage: {stage_name} in {end_time - start_time:.2f} seconds")
        return result
    except Exception as e:
        logging.error(f"Error in stage {stage_name}: {str(e)}")
        raise