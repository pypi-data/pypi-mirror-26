from collections import OrderedDict

from .variable.base import (AbstractVariable, Variable, ForeignVariable,
                            VariableList, VariableGroup)
from .process import Process
from .utils import AttrMapping, ContextMixin
from .formatting import _calculate_col_width, pretty_print, maybe_truncate


def _set_process_names(processes):
    # type: Dict[str, Process]
    """Set process names using keys of the mapping."""
    for k, p in processes.items():
        p._name = k


def _set_group_vars(processes):
    """Assign variables that belong to variable groups."""
    for proc in processes.values():
        for var in proc._variables.values():
            if isinstance(var, VariableGroup):
                var._set_variables(processes)


def _get_foreign_vars(processes):
    # type: Dict[str, Process] -> Dict[str, List[ForeignVariable]]

    foreign_vars = {}

    for proc_name, proc in processes.items():
        foreign_vars[proc_name] = []

        for var in proc._variables.values():
            if isinstance(var, (tuple, list, VariableGroup)):
                foreign_vars[proc_name] += [
                    v for v in var if isinstance(v, ForeignVariable)
                ]
            elif isinstance(var, ForeignVariable):
                foreign_vars[proc_name].append(var)

    return foreign_vars


def _link_foreign_vars(processes):
    """Assign process instances to foreign variables."""
    proc_lookup = {v.__class__: v for v in processes.values()}

    for variables in _get_foreign_vars(processes).values():
        for var in variables:
            var._other_process_obj = proc_lookup[var._other_process_cls]


def _get_input_vars(processes):
    # type: Dict[str, Process] -> Dict[str, Dict[str, Variable]]

    input_vars = {}

    for proc_name, proc in processes.items():
        input_vars[proc_name] = {}

        for k, var in proc._variables.items():
            if isinstance(var, Variable) and not var.provided:
                input_vars[proc_name][k] = var

    # case of variables provided by other processes
    foreign_vars = _get_foreign_vars(processes)
    for variables in foreign_vars.values():
        for var in variables:
            if input_vars[var.ref_process.name].get(var.var_name, False):
                if var.provided:
                    del input_vars[var.ref_process.name][var.var_name]

    return {k: v for k, v in input_vars.items() if v}


def _get_process_dependencies(processes):
    # type: Dict[str, Process] -> Dict[str, List[Process]]

    dep_processes = {k: set() for k in processes}
    foreign_vars = _get_foreign_vars(processes)

    for proc_name, variables in foreign_vars.items():
        for var in variables:
            if var.provided:
                dep_processes[var.ref_process.name].add(proc_name)
            else:
                ref_var = var.ref_var
                if ref_var.provided or getattr(ref_var, 'optional', False):
                    dep_processes[proc_name].add(var.ref_process.name)

    return {k: list(v) for k, v in dep_processes.items()}


def _sort_processes(dep_processes):
    # type: Dict[str, List[Process]] -> List[str]
    """Stack-based depth-first search traversal.

    This is based on Tarjan's method for topological sorting.

    Part of the code below is copied and modified from:

    - dask 0.14.3 (Copyright (c) 2014-2015, Continuum Analytics, Inc.
      and contributors)
      Licensed under the BSD 3 License
      http://dask.pydata.org

    """
    ordered = []

    # Nodes whose descendents have been completely explored.
    # These nodes are guaranteed to not be part of a cycle.
    completed = set()

    # All nodes that have been visited in the current traversal.  Because
    # we are doing depth-first search, going "deeper" should never result
    # in visiting a node that has already been seen.  The `seen` and
    # `completed` sets are mutually exclusive; it is okay to visit a node
    # that has already been added to `completed`.
    seen = set()

    for key in dep_processes:
        if key in completed:
            continue
        nodes = [key]
        while nodes:
            # Keep current node on the stack until all descendants are visited
            cur = nodes[-1]
            if cur in completed:
                # Already fully traversed descendants of cur
                nodes.pop()
                continue
            seen.add(cur)

            # Add direct descendants of cur to nodes stack
            next_nodes = []
            for nxt in dep_processes[cur]:
                if nxt not in completed:
                    if nxt in seen:
                        # Cycle detected!
                        cycle = [nxt]
                        while nodes[-1] != nxt:
                            cycle.append(nodes.pop())
                        cycle.append(nodes.pop())
                        cycle.reverse()
                        cycle = '->'.join(cycle)
                        raise ValueError(
                            "cycle detected in process graph: %s" % cycle
                        )
                    next_nodes.append(nxt)

            if next_nodes:
                nodes.extend(next_nodes)
            else:
                # cur has no more descendants to explore, so we're done with it
                ordered.append(cur)
                completed.add(cur)
                seen.remove(cur)
                nodes.pop()
    return ordered


class Model(AttrMapping, ContextMixin):
    """An immutable collection (mapping) of process units that together
    form a computational model.

    This collection is ordered such that the computational flow is
    consistent with process inter-dependencies.

    Ordering doesn't need to be explicitly provided ; it is dynamically
    computed using the processes interfaces.

    Processes interfaces are also used for automatically retrieving
    the model inputs, i.e., all the variables which require setting a
    value before running the model.

    """
    def __init__(self, processes):
        """
        Parameters
        ----------
        processes : dict
            Dictionnary with process names as keys and subclasses of
            `Process` as values.

        """
        processes_obj = {}

        for k, cls in processes.items():
            if not issubclass(cls, Process) or cls is Process:
                raise TypeError("%s is not a subclass of Process" % cls)
            processes_obj[k] = cls()

        _set_process_names(processes_obj)
        _set_group_vars(processes_obj)
        _link_foreign_vars(processes_obj)

        self._input_vars = _get_input_vars(processes_obj)
        self._dep_processes = _get_process_dependencies(processes_obj)
        self._processes = OrderedDict(
            [(k, processes_obj[k])
             for k in _sort_processes(self._dep_processes)]
        )
        self._time_processes = OrderedDict(
            [(k, proc) for k, proc in self._processes.items()
             if proc.meta['time_dependent']]
        )

        super(Model, self).__init__(self._processes)
        self._initialized = True

    def _get_proc_var_name(self, variable):
        # type: AbstractVariable -> Union[tuple[str, str], None]
        for proc_name, variables in self._processes.items():
            for var_name, var in variables.items():
                if var is variable:
                    return proc_name, var_name
        return None, None

    @property
    def input_vars(self):
        """Returns all variables that require setting a
        value before running the model.

        These variables are grouped by process name (dict of dicts).

        """
        return self._input_vars

    def is_input(self, variable):
        """Test if a variable is an input of Model.

        Parameters
        ----------
        variable : object or tuple
            Either a Variable object or a (str, str) tuple
            corresponding to process name and variable name.

        Returns
        -------
        is_input : bool
            True if the variable is a input of Model (otherwise False).

        """
        if isinstance(variable, AbstractVariable):
            proc_name, var_name = self._get_proc_var_name(variable)
        elif isinstance(variable, (VariableList, VariableGroup)):
            proc_name, var_name = None, None   # prevent unpack iterable below
        else:
            proc_name, var_name = variable

        if self._input_vars.get(proc_name, {}).get(var_name, False):
            return True
        return False

    def visualize(self, show_only_variable=None, show_inputs=False,
                  show_variables=False):
        """Render the model as a graph using dot (require graphviz).

        Parameters
        ----------
        show_only_variable : object or tuple, optional
            Show only a variable (and all other linked variables) given either
            as a Variable object or a tuple corresponding to process name and
            variable name. Deactivated by default.
        show_inputs : bool, optional
            If True, show all input variables in the graph (default: False).
            Ignored if `show_only_variable` is not None.
        show_variables : bool, optional
            If True, show also the other variables (default: False).
            Ignored if `show_only_variable` is not None.

        See Also
        --------
        dot.dot_graph

        """
        from .dot import dot_graph
        return dot_graph(self, show_only_variable=show_only_variable,
                         show_inputs=show_inputs,
                         show_variables=show_variables)

    def initialize(self):
        """Run `.initialize()` for each processes in the model."""
        for proc in self._processes.values():
            proc.initialize()

    def run_step(self, step):
        """Run `.run_step()` for each time dependent processes in the model.
        """
        for proc in self._time_processes.values():
            proc.run_step(step)

    def finalize_step(self):
        """Run `.finalize_step()` for each time dependent processes
        in the model.
        """
        for proc in self._time_processes.values():
            proc.finalize_step()

    def finalize(self):
        """Run `.finalize()` for each processes in the model."""
        for proc in self._processes.values():
            proc.finalize()

    def clone(self):
        """Clone the Model.

        This is equivalent to a deep copy, except that variable data
        (i.e., `state`, `value`, `change` or `rate` properties) in all
        processes are not copied.
        """
        processes_cls = {k: type(obj) for k, obj in self._processes.items()}
        return type(self)(processes_cls)

    def update_processes(self, processes):
        """Add or replace processe(s) in this model.

        Parameters
        ----------
        processes : dict
            Dictionnary with process names as keys and subclasses of
            `Process` as values.

        Returns
        -------
        updated : Model
            New Model instance with updated processes.

        """
        processes_cls = {k: type(obj) for k, obj in self._processes.items()}
        processes_cls.update(processes)
        return type(self)(processes_cls)

    def drop_processes(self, keys):
        """Drop processe(s) from this model.

        Parameters
        ----------
        keys : str or list of str
            Name(s) of the processes to drop.

        Returns
        -------
        dropped : Model
            New Model instance with dropped processes.

        """
        if isinstance(keys, str):
            keys = [keys]

        processes_cls = {k: type(obj) for k, obj in self._processes.items()
                         if k not in keys}
        return type(self)(processes_cls)

    def __repr__(self):
        n_inputs = sum([len(v) for v in self._input_vars.values()])

        hdr = ("<xsimlab.Model (%d processes, %d inputs)>"
               % (len(self._processes), n_inputs))

        if not len(self._processes):
            return hdr

        max_line_length = 70
        col_width = max([_calculate_col_width(var)
                         for var in self._input_vars.values()])

        blocks = []
        for proc_name in self._processes:
            proc_str = "%s" % proc_name

            inputs = self._input_vars.get(proc_name, {})
            lines = []
            for name, var in inputs.items():
                line = pretty_print("    %s " % name, col_width)
                line += maybe_truncate("(in) %s" % var.description,
                                       max_line_length - col_width)
                lines.append(line)

            if lines:
                proc_str += '\n' + '\n'.join(lines)
            blocks.append(proc_str)

        return hdr + '\n' + '\n'.join(blocks)
