import ast
import astor
import copy
import inspect
import sys
import tempfile
import textwrap
import traceback
import warnings

from miniutils.opt_decorator import optional_argument_decorator

# Astor tries to get fancy by failing nicely, but in doing so they fail when traversing non-AST type node properties.
#  By deleting this custom handler, it'll fall back to the default ast visit pattern, which skips these missing
# properties. Everything else seems to be implemented, so this will fail silently if it hits an AST node that isn't
# supported but should be.
del astor.node_util.ExplicitNodeVisitor.visit


class DictStack:
    """
    Creates a stack of dictionaries to roughly emulate closures and variable environments
    """

    def __init__(self, *base):
        import builtins
        self.dicts = [dict(builtins.__dict__)] + [dict(d) for d in base]
        self.constants = [True] + [False] * len(base)

    def __setitem__(self, key, value):
        self.dicts[-1][key] = value

    def __getitem__(self, item):
        for dct in self.dicts[::-1]:
            if item in dct:
                if dct[item] is None:
                    raise KeyError("Found '{}', but it was set to an unknown value".format(item))
                return dct[item]
        raise KeyError("Can't find '{}' anywhere in the function's context".format(item))

    def __delitem__(self, item):
        for dct in self.dicts[::-1]:
            if item in dct:
                del dct[item]
                return
        raise KeyError()

    def __contains__(self, item):
        try:
            self[item]
            return True
        except KeyError:
            return False

    def items(self):
        items = []
        for dct in self.dicts[::-1]:
            for k, v in dct.items():
                if k not in items:
                    items.append((k, v))
        return items

    def keys(self):
        return set().union(*[dct.keys() for dct in self.dicts])

    def push(self, dct=None, is_constant=False):
        self.dicts.append(dct or {})
        self.constants.append(is_constant)

    def pop(self):
        self.constants.pop()
        return self.dicts.pop()


def _function_ast(f):
    """Returns ast for the given function. Gives a tuple of (ast_module, function_body, function_file"""
    assert callable(f)

    try:
        f_file = sys.modules[f.__module__].__file__
    except (KeyError, AttributeError):
        f_file = ''

    root = ast.parse(textwrap.dedent(inspect.getsource(f)), f_file)
    return root, root.body[0].body, f_file


def can_have_side_effect(node, ctxt):
    if isinstance(node, ast.AST):
        # print("Can {} have side effects?".format(node))
        if isinstance(node, ast.Call):
            # print("  Yes!")
            return True
        else:
            for field, old_value in ast.iter_fields(node):
                if isinstance(old_value, list):
                    return any(can_have_side_effect(n, ctxt) for n in old_value if isinstance(n, ast.AST))
                elif isinstance(old_value, ast.AST):
                    return can_have_side_effect(old_value, ctxt)
                else:
                    # print("  No!")
                    return False
    else:
        return False


def _constant_iterable(node, ctxt, avoid_side_effects=True):
    """If the given node is a known iterable of some sort, return the list of its elements."""
    # TODO: Support zipping
    # TODO: Support sets/dicts?
    # TODO: Support for reversed, enumerate, etc.
    # TODO: Support len, in, etc.
    # Check for range(*constants)
    def wrap(return_node, name, idx):
        if not avoid_side_effects:
            return return_node
        if can_have_side_effect(return_node, ctxt):
            return ast.Subscript(name, ast.Index(idx))
        return _make_ast_from_literal(return_node)

    if isinstance(node, ast.Call):
        if _resolve_name_or_attribute(node.func, ctxt) == range:
            args = [_collapse_literal(arg, ctxt) for arg in node.args]
            if all(isinstance(arg, ast.Num) for arg in args):
                return [ast.Num(n) for n in range(*[arg.n for arg in args])]

        return None
    elif isinstance(node, (ast.List, ast.Tuple)):
        return [_collapse_literal(e, ctxt) for e in node.elts]
        #return [_resolve_name_or_attribute(e, ctxt) for e in node.elts]
    # Can't yet support sets and lists, since you need to compute what the unique values would be
    # elif isinstance(node, ast.Dict):
    #     return node.keys
    elif isinstance(node, (ast.Name, ast.Attribute, ast.NameConstant)):
        res = _resolve_name_or_attribute(node, ctxt)
        #print("Trying to resolve '{}' as list, got {}".format(astor.to_source(node), res))
        if isinstance(res, ast.AST) and not isinstance(res, (ast.Name, ast.Attribute, ast.NameConstant)):
            res = _constant_iterable(res, ctxt)
        if not isinstance(res, ast.AST):
            try:
                if hasattr(res, 'items'):
                    return dict([(k, wrap(_make_ast_from_literal(v), node, k)) for k, v in res.items()])
                else:
                    return [wrap(_make_ast_from_literal(res_node), node, i) for i, res_node in enumerate(res)]
            except TypeError:
                pass
    return None


def _resolve_name_or_attribute(node, ctxt_or_obj):
    """If the given name of attribute is defined in the current context, return its value. Else, returns the node"""
    if isinstance(node, ast.Name):
        if isinstance(ctxt_or_obj, DictStack):
            if node.id in ctxt_or_obj:
                #print("Resolved '{}' to {}".format(node.id, ctxt_or_obj[node.id]))
                return ctxt_or_obj[node.id]
            else:
                return node
        else:
            return getattr(ctxt_or_obj, node.id, node)
    elif isinstance(node, ast.NameConstant):
        return node.value
    elif isinstance(node, ast.Attribute):
        base_obj = _resolve_name_or_attribute(node.value, ctxt_or_obj)
        if not isinstance(base_obj, ast.AST):
            return getattr(base_obj, node.attr, node)
        else:
            return node
    else:
        return node


_collapse_map = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,

    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
    ast.LShift: lambda a, b: a << b,
    ast.RShift: lambda a, b: a >> b,
    ast.MatMult: lambda a, b: a @ b,

    ast.BitAnd: lambda a, b: a & b,
    ast.BitOr: lambda a, b: a | b,
    ast.BitXor: lambda a, b: a ^ b,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
    ast.Invert: lambda a: ~a,
    ast.Not: lambda a: not a,

    ast.UAdd: lambda a: a,
    ast.USub: lambda a: -a,

    ast.Eq: lambda a, b: a == b,
    ast.NotEq: lambda a, b: a != b,
    ast.Lt: lambda a, b: a < b,
    ast.LtE: lambda a, b: a <= b,
    ast.Gt: lambda a, b: a > b,
    ast.GtE: lambda a, b: a >= b,
}


def _make_ast_from_literal(lit):
    """Converts literals into their AST equivalent"""
    if isinstance(lit, (list, tuple)):
        res = [_make_ast_from_literal(e) for e in lit]
        tp = ast.List if isinstance(lit, list) else ast.Tuple
        return tp(elts=res)
    elif isinstance(lit, (int, float)):
        return ast.Num(lit)
    elif isinstance(lit, str):
        return ast.Str(lit)
    elif isinstance(lit, bool):
        return ast.NameConstant(lit)
    else:
        return lit


def __collapse_literal(node, ctxt):
    """Collapses literal expressions. Returns literals if they're available, AST nodes otherwise"""
    if isinstance(node, (ast.Name, ast.Attribute, ast.NameConstant)):
        res = _resolve_name_or_attribute(node, ctxt)
        if isinstance(res, ast.AST) and not isinstance(res, (ast.Name, ast.Attribute, ast.NameConstant)):
            res = __collapse_literal(res, ctxt)
        return res
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.Index):
        return __collapse_literal(node.value, ctxt)
    elif isinstance(node, (ast.Slice, ast.ExtSlice)):
        raise NotImplemented()
    elif isinstance(node, ast.Subscript):
        # print("Attempting to subscript {}".format(astor.to_source(node)))
        lst = _constant_iterable(node.value, ctxt)
        # print("Can I subscript {}?".format(lst))
        if lst is None:
            return node
        slc = __collapse_literal(node.slice, ctxt)
        # print("Getting subscript at {}".format(slc))
        if isinstance(slc, ast.AST):
            return node
        # print("Value at {}[{}] = {}".format(lst, slc, lst[slc]))
        return lst[slc]
    elif isinstance(node, (ast.UnaryOp, ast.BinOp, ast.BoolOp)):
        if isinstance(node, ast.UnaryOp):
            operands = [__collapse_literal(node.operand, ctxt)]
        else:
            operands = [__collapse_literal(o, ctxt) for o in [node.left, node.right]]
        #print("({} {})".format(repr(node.op), ", ".join(repr(o) for o in operands)))
        is_literal = [not isinstance(opr, ast.AST) for opr in operands]
        if all(is_literal):
            try:
                val = _collapse_map[type(node.op)](*operands)
                return val
            except:
                warnings.warn("Literal collapse failed. Collapsing skipped, but executing this function will likely fail."
                              " Error was:\n{}".format(traceback.format_exc()))
                return node
        else:
            if isinstance(node, ast.UnaryOp):
                return ast.UnaryOp(operand=_make_ast_from_literal(operands[0]), op=node.op)
            else:
                return type(node)(left=_make_ast_from_literal(operands[0]),
                                  right=_make_ast_from_literal(operands[1]),
                                  op=node.op)
    elif isinstance(node, ast.Compare):
        operands = [__collapse_literal(o, ctxt) for o in [node.left] + node.comparators]
        if all(not isinstance(opr, ast.AST) for opr in operands):
            return all(_collapse_map[type(cmp_func)](operands[i-1], operands[i])
                       for i, cmp_func in zip(range(1, len(operands)), node.ops))
        else:
            return node
    else:
        return node


def _collapse_literal(node, ctxt):
    """Collapse literal expressions in the given node. Returns the node with the collapsed literals"""
    return _make_ast_from_literal(__collapse_literal(node, ctxt))


def _assign_names(node):
    """Gets names from a assign-to tuple in flat form, just to know what's affected
    "x=3" -> "x"
    "a,b=4,5" -> ["a", "b"]
    "(x,(y,z)),(a,) = something" -> ["x", "y", "z", "a"]
    """
    if isinstance(node, ast.Name):
        yield node.id
    elif isinstance(node, ast.Tuple):
        for e in node.elts:
            yield from _assign_names(e)


# noinspection PyPep8Naming
class TrackedContextTransformer(ast.NodeTransformer):
    def __init__(self, ctxt=None):
        self.ctxt = ctxt or DictStack()
        super().__init__()

    # def visit(self, node):
    #     orig_node = copy.deepcopy(node)
    #     new_node = super().visit(node)
    #
    #     orig_node_code = astor.to_source(orig_node).strip()
    #     try:
    #         if new_node is None:
    #             print("Deleted >>> {} <<<".format(orig_node_code))
    #         elif isinstance(new_node, ast.AST):
    #             print("Converted >>> {} <<< to >>> {} <<<".format(orig_node_code, astor.to_source(new_node).strip()))
    #         elif isinstance(new_node, list):
    #             print("Converted >>> {} <<< to [[[ {} ]]]".format(orig_node_code, ", ".join(astor.to_source(n).strip() for n in new_node)))
    #     except AssertionError as ex:
    #         raise AssertionError("Failed on {} >>> {}".format(orig_node_code, astor.dump_tree(new_node))) from ex
    #
    #     return new_node

    def visit_Assign(self, node):
        node.value = self.visit(node.value)
        #print(node.value)
        # TODO: Support tuple assignments
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var = node.targets[0].id
            val = _constant_iterable(node.value, self.ctxt)
            if val is not None:
                #print("Setting {} = {}".format(var, val))
                self.ctxt[var] = val
            else:
                val = _collapse_literal(node.value, self.ctxt)
                #print("Setting {} = {}".format(var, val))
                self.ctxt[var] = val
        else:
            for targ in node.targets:
                for assgn in _assign_names(targ):
                    self.ctxt[assgn] = None
        return node


# noinspection PyPep8Naming
class UnrollTransformer(TrackedContextTransformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_vars = set()

    def visit_For(self, node):
        result = [node]
        iterable = _constant_iterable(node.iter, self.ctxt)
        if iterable is not None:
            result = []
            loop_var = node.target.id
            orig_loop_vars = self.loop_vars
            # print("Unrolling 'for {} in {}'".format(loop_var, list(iterable)))
            for val in iterable:
                self.ctxt.push({loop_var: val})
                self.loop_vars = orig_loop_vars | {loop_var}
                for body_node in copy.deepcopy(node.body):
                    res = self.visit(body_node)
                    if isinstance(res, list):
                        result.extend(res)
                    elif res is None:
                        continue
                    else:
                        result.append(res)
                # result.extend([self.visit(body_node) for body_node in copy.deepcopy(node.body)])
                self.ctxt.pop()
            self.loop_vars = orig_loop_vars
        return result

    def visit_Name(self, node):
        if node.id in self.loop_vars:
            if node.id in self.ctxt:
                return self.ctxt[node.id]
            raise NameError("'{}' not defined in context".format(node.id))
        return node


# noinspection PyPep8Naming
class CollapseTransformer(TrackedContextTransformer):
    def visit_BinOp(self, node):
        return _collapse_literal(node, self.ctxt)

    def visit_UnaryOp(self, node):
        return _collapse_literal(node, self.ctxt)

    def visit_BoolOp(self, node):
        return _collapse_literal(node, self.ctxt)

    def visit_Compare(self, node):
        return _collapse_literal(node, self.ctxt)

    def visit_Subscript(self, node):
        return _collapse_literal(node, self.ctxt)


def _make_function_transformer(transformer_type, name, description):
    @optional_argument_decorator
    def transform(return_source=False, save_source=True, function_globals=None, **kwargs):
        """
        :param return_source: Returns the unrolled function's source code instead of compiling it
        :param save_source: Saves the function source code to a tempfile to make it inspectable
        :param kwargs: Any other environmental variables to provide during unrolling
        :return: The unrolled function, or its source code if requested
        """

        def inner(f):
            f_mod, f_body, f_file = _function_ast(f)
            # Grab function globals
            glbls = f.__globals__
            # Grab function closure variables
            if isinstance(f.__closure__, tuple):
                glbls.update({k: v.cell_contents for k, v in zip(f.__code__.co_freevars, f.__closure__)})
            # Apply manual globals override
            if function_globals is not None:
                glbls.update(function_globals)
            # print({k: v for k, v in glbls.items() if k not in globals()})
            trans = transformer_type(DictStack(glbls, kwargs))
            f_mod.body[0].decorator_list = []
            f_mod = trans.visit(f_mod)
            # print(astor.dump_tree(f_mod))
            if return_source or save_source:
                try:
                    source = astor.to_source(f_mod)
                except ImportError:  # pragma: nocover
                    raise ImportError("miniutils.pragma.{name} requires 'astor' to be installed to obtain source code"
                                      .format(name=name))
            else:
                source = None

            if return_source:
                return source
            else:
                # func_source = astor.to_source(f_mod)
                f_mod = ast.fix_missing_locations(f_mod)
                if save_source:
                    temp = tempfile.NamedTemporaryFile('w', delete=True)
                    f_file = temp.name
                exec(compile(f_mod, f_file, 'exec'), glbls)
                func = glbls[f_mod.body[0].name]
                if save_source:
                    func.__tempfile__ = temp
                    temp.write(source)
                    temp.flush()
                return func

        return inner
    transform.__name__ = name
    transform.__doc__ = '\n'.join([description, transform.__doc__])
    return transform


# Unroll literal loops
unroll = _make_function_transformer(UnrollTransformer, 'unroll', "Unrolls constant loops in the decorated function")

# Collapse defined literal values, and operations thereof, where possible
collapse_literals = _make_function_transformer(CollapseTransformer, 'collapse_literals',
                                               "Collapses literal expressions in the decorated function into single literals")

# Directly reference elements of constant list, removing literal indexing into that list within a function
def deindex(iterable, iterable_name, *args, **kwargs):
    """
    :param iterable: The list to deindex in the target function
    :param iterable_name: The list's name (must be unique if deindexing multiple lists)
    :param return_source: Returns the unrolled function's source code instead of compiling it
    :param save_source: Saves the function source code to a tempfile to make it inspectable
    :param kwargs: Any other environmental variables to provide during unrolling
    :return: The unrolled function, or its source code if requested
    """

    if hasattr(iterable, 'items'):  # Support dicts and the like
        internal_iterable = {k: '{}_{}'.format(iterable_name, k) for k, val in iterable.items()}
        mapping = {internal_iterable[k]: val for k, val in iterable.items()}
    else:  # Support lists, tuples, and the like
        internal_iterable = {i: '{}_{}'.format(iterable_name, i) for i, val in enumerate(iterable)}
        mapping = {internal_iterable[i]: val for i, val in enumerate(iterable)}

    kwargs[iterable_name] = {k: ast.Name(id=name, ctx=ast.Load()) for k, name in internal_iterable.items()}

    return collapse_literals(*args, function_globals=mapping, **kwargs)

# Inline functions?

