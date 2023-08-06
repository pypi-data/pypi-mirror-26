"""Information on a solver (:mod:`fluidsim.base.params`)
==============================================================

.. currentmodule:: fluidsim.base.params

Provides:

.. autoclass:: Parameters
   :members:
   :private-members:


"""

from __future__ import division, print_function

import os

from fluiddyn.util.paramcontainer import ParamContainer
from fluiddyn.util.util import import_class

from fluidsim.base.solvers.info_base import InfoSolverBase


class Parameters(ParamContainer):
    """Contain the parameters."""
    pass


def merge_params(*paramcontainers):
    """Merges missing parameters attributes and children."""
    if any([not isinstance(params, Parameters) for params in paramcontainers]):
        raise ValueError('Can only merge instances of Parameters')

    params_merged = paramcontainers[0]
    print(params_merged.init_fields.from_file.path)

    def merge_params_pair(params1, params2):
        """Merge `params1` --> `params2`."""
        try:
            diff_attribs = set(params2._key_attribs) - set(params1._key_attribs)
        except AttributeError:
            from warnings import warn
            warn('Kept for compatibility with fluiddyn==0.0.x', DeprecationWarning)
            diff_attribs = params2._attribs - params1._attribs

        for attrib in diff_attribs:
            print('Merge params attrib: ', attrib)
            params1._set_attrib(attrib, params2[attrib])

        diff_children = set(params2._tag_children) - set(params1._tag_children)

        for child in diff_children:
            print('Merge params child: ', child)
            params1._set_child(child, params2[child]._make_dict())

        for child in params2._tag_children:
            params1[child] = merge_params_pair(params1[child], params2[child])

        return params1

    for params in paramcontainers[1:]:
        params_merged = merge_params_pair(params_merged, params)

    return params_merged


def create_params(input_info_solver):
    """Create a Parameters instance from an InfoSolverBase instance."""
    if isinstance(input_info_solver, InfoSolverBase):
        info_solver = input_info_solver
    elif hasattr(input_info_solver, 'Simul'):
        info_solver = input_info_solver.Simul.create_default_params()
    else:
        raise ValueError('Can not create params from input input_info_solver.')

    params = Parameters(tag='params')
    dict_classes = info_solver.import_classes()

    dict_classes['Solver'] = import_class(
        info_solver.module_name, info_solver.class_name)

    for Class in list(dict_classes.values()):
        if hasattr(Class, '_complete_params_with_default'):
            try:
                Class._complete_params_with_default(params)
            except TypeError:
                try:
                    Class._complete_params_with_default(params, info_solver)
                except TypeError as e:
                    e.args += ('for class: ' + repr(Class),)
                    raise
    return params


def load_params_simul(path_dir=None):
    """Load the parameters and return a Parameters instance."""
    if path_dir is None:
        path_dir = os.getcwd()
    return Parameters(
        path_file=os.path.join(path_dir, 'params_simul.xml'))


def load_info_solver(path_dir=None):
    """Load the solver information, return an InfoSolverBase instance.

    """
    if path_dir is None:
        path_dir = os.getcwd()
    return InfoSolverBase(
        path_file=os.path.join(path_dir, 'info_solver.xml'))


# def load_info_simul(path_dir=None):
#     """Load the data and gather them in a ParamContainer instance."""

#     if path_dir is None:
#         path_dir = os.getcwd()
#     info_solver = load_info_solver(path_dir=path_dir)
#     params = load_params_simul(path_dir=path_dir)
#     info = ParamContainer(tag='info_simul')
#     info._set_as_child(info_solver)
#     info._set_as_child(params)
#     return info


if __name__ == '__main__':
    info_solver = InfoSolverBase(tag='solver')

    info_solver.complete_with_classes()

    params = create_params(info_solver)

    info = create_info_simul(info_solver, params)
