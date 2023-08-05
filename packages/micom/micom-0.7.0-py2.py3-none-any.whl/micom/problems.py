"""Implements optimization and model problems."""

from micom.duality import fast_dual
from micom.solution import CommunitySolution
from micom.util import (_format_min_growth, _apply_min_growth,
                        check_modification)
from micom.logger import logger
from optlang.symbolics import Zero, One
from functools import partial
from itertools import chain


def add_pfba_objective(community):
    """Add pFBA objective.

    Add objective to minimize the summed flux of all reactions to the
    current objective. This one will work with any objective (even non-linear
    ones).

    See Also
    --------
    pfba

    Parameters
    ----------
    community : micom.Community
        The community to add the objective to.
    """
    # Fix all growth rates
    rates = {sp: community.constraints["objective_" + sp].primal
             for sp in community.species}
    rates["community"] = community.variables["community_objective"].primal
    for sp in community.species:
        const = community.constraints["objective_" + sp]
        const.lb = const.ub = rates[sp]
    community_obj = community.variables["community_objective"]
    community_obj.ub = community_obj.lb = rates["community"]

    if community.solver.objective.name == '_pfba_objective':
        raise ValueError('model already has pfba objective')
    reaction_variables = ((rxn.forward_variable, rxn.reverse_variable)
                          for rxn in community.reactions)
    variables = chain(*reaction_variables)
    community.objective = Zero
    community.objective.direction = "min"
    community.objective.set_linear_coefficients(dict.fromkeys(variables, 1.0))
    if community.modification is None:
        community.modification = "pFBA"
    else:
        community.modification += " and pFBA"


def solve(community, fluxes=True, pfba=True):
    """Get all fluxes stratified by species."""
    community.solver.optimize()
    if community.solver.status == "optimal":
        if fluxes and pfba:
            add_pfba_objective(community)
            community.solver.optimize()
        if fluxes:
            sol = CommunitySolution(community)
        else:
            sol = CommunitySolution(community, slim=True)
        return sol
    return None


def add_linear_optcom(community, min_growth=0.1):
    """Add a linear version of optcom.

    Adds constraints to the community such that each individual grows with
    at least its minimal growth rate.

    Arguments
    ---------
    community : micom.Community
        The community to modify.
    min_growth : positive float or array-like object.
        The minimum growth rate for each individual in the community. Either
        a single value applied to all individuals or one value for each.

    """
    check_modification(community)
    min_growth = _format_min_growth(min_growth, community.species)
    _apply_min_growth(community, min_growth)

    community.modification = "linear optcom"


def add_lagrangian(community, tradeoff, linear=False):
    """Add a Lagrangian optimization target to a linear OptCom model.

    Lagrangian forms in `micom` are usually objectives of the form
    (1 - tradeoff) * community_objective + tradeoff * cooperativity_cost.
    Here, cooperativity cost specifies the "sacrifice" in growth rate an
    individual has to make in order to maximize community growth. It is
    calculated as the sum of squared differences between the individuals
    current and maximal growth rate. In the linear case squares are substituted
    by absolute values (Manhattan distance).

    Arguments
    ---------
    community : micom.Community
        The community to modify.
    tradeoff : float in [0,1]
        The tradeoff between community growth and the individual "egoistic"
        growth target. 0 means optimize only community growth and 1 means
        optimize only the individuals own growth target.
    linear : boolean
        Whether to use a non-linear (sum of squares) or linear version of the
        cooperativity cost. If set to False requires a QP-capable solver.

    """
    logger.info("adding lagrangian objective to %s" % community.id)
    max_gcs = community.optimize_all(progress=False)
    com_expr = Zero
    cost_expr = Zero
    abundances = community.abundances
    logger.info("adding expressions for %d species" % len(community.species))
    for sp in community.species:
        species_obj = community.constraints["objective_" + sp]
        com_expr += abundances[sp] * species_obj.expression
        ex = max_gcs[sp] - species_obj.expression
        if not linear:
            ex = ex**2
        cost_expr += ex.expand()
    community.objective = (One - tradeoff) * com_expr - tradeoff * cost_expr
    if "with lagrangian" not in community.modification:
        community.modification += " with lagrangian"
    logger.info("finished adding lagrangian objective to %s" % community.id)


def add_dualized_optcom(community, min_growth):
    """Add dual Optcom variables and constraints to a community.

    Uses the original formulation of OptCom and solves the following
    multi-objective problem::

        maximize community_growth
        s.t. maximize growth_rate_i for all i
             s.t. Sv_i = 0
                  lb_i >= v_i >= ub_i

    Notes
    -----
    This method will only find one arbitrary solution from the Pareto front.
    There may exist several other optimal solutions.

    Arguments
    ---------
    community : micom.Community
        The community to modify.
    min_growth : positive float or array-like object.
        The minimum growth rate for each individual in the community. Either
        a single value applied to all individuals or one value for each.

    """
    logger.info("adding dual optcom to %s" % community.id)
    check_modification(community)
    min_growth = _format_min_growth(min_growth, community.species)

    prob = community.solver.interface

    # Temporarily subtitute objective with sum of individual objectives
    # for correct dual variables
    old_obj = community.objective
    community.objective = Zero
    for sp in community.species:
        species_obj = community.constraints["objective_" + sp]
        community.objective += species_obj.expression

    _apply_min_growth(community, min_growth)
    dual_coefs = fast_dual(community)

    logger.info("adding expressions for %d species" % len(community.species))
    for sp in community.species:
        primal_const = community.constraints["objective_" + sp]
        coefs = primal_const.get_linear_coefficients(primal_const.variables)
        coefs.update({dual_var: -coef for dual_var, coef in
                      dual_coefs.items() if sp in dual_var.name})
        obj_constraint = prob.Constraint(
            Zero, lb=0, ub=0, name="optcom_suboptimality_" + sp)
        community.add_cons_vars([obj_constraint])
        community.solver.update()
        obj_constraint.set_linear_coefficients(coefs)

    community.objective = old_obj
    community.modification = "dual optcom"
    logger.info("finished adding dual optcom to %s" % community.id)


def add_moma_optcom(community, min_growth, linear=False):
    """Add a dualized MOMA version of OptCom.

    Solves a MOMA (minimization of metabolic adjustment) formulation of OptCom
    given by::

        minimize cooperativity_cost
        s.t. maximize community_objective
             s.t. Sv = 0
                  lb >= v >= ub
        where community_cost = sum (growth_rate - max_growth)**2
              if linear=False or
              community_cost = sum |growth_rate - max_growth|
              if linear=True

    Arguments
    ---------
    community : micom.Community
        The community to modify.
    min_growth : positive float or array-like object.
        The minimum growth rate for each individual in the community. Either
        a single value applied to all individuals or one value for each.
    linear : boolean
        Whether to use a non-linear (sum of squares) or linear version of the
        cooperativity cost. If set to False requires a QP-capable solver.

    """
    logger.info("adding dual %s moma to %s" % (
        "linear" if linear else "quadratic", community.id))
    check_modification(community)
    min_growth = _format_min_growth(min_growth, community.species)

    prob = community.solver.interface
    old_obj = community.objective
    coefs = old_obj.get_linear_coefficients(old_obj.variables)

    # Get maximum individual growth rates
    max_gcs = community.optimize_all(progress=False)

    _apply_min_growth(community, min_growth)
    dual_coefs = fast_dual(community)
    coefs.update({
        v: -coef for v, coef in
        dual_coefs.items()})
    obj_constraint = prob.Constraint(
        Zero, lb=0, ub=0,
        name="optcom_suboptimality")
    community.add_cons_vars([obj_constraint])
    community.solver.update()
    obj_constraint.set_linear_coefficients(coefs)
    obj_expr = Zero
    logger.info("adding expressions for %d species" % len(community.species))
    for sp in community.species:
        v = prob.Variable("gc_constant_" + sp, lb=max_gcs[sp], ub=max_gcs[sp])
        community.add_cons_vars([v])
        species_obj = community.constraints["objective_" + sp]
        ex = v - species_obj.expression
        if not linear:
            ex = ex**2
        obj_expr += ex.expand()
    community.objective = prob.Objective(obj_expr, direction="min")
    community.modification = "moma optcom"
    logger.info("finished dual moma to %s" % community.id)


_methods = {"linear": [add_linear_optcom],
            "lagrangian": [add_linear_optcom, add_lagrangian],
            "linear lagrangian": [add_linear_optcom,
                                  partial(add_lagrangian, linear=True)],
            "original": [add_dualized_optcom],
            "moma": [add_moma_optcom],
            "lmoma": [partial(add_moma_optcom, linear=True)]}


def optcom(community, strategy, min_growth, tradeoff, fluxes, pfba):
    """Run OptCom for the community.

    OptCom methods are a group of optimization procedures to find community
    solutions that provide a tradeoff between the cooperative community
    growth and the egoistic growth of each individual [#p1]_. `micom`
    provides several strategies that can be used to find optimal solutions:

    - "linear": Applies a lower bound for the individual growth rates and
      finds the optimal community growth rate. This is the fastest methods
      but also ignores that individuals might strive to optimize their
      individual growth instead of community growth.
    - "lagrangian": Optimizes a joint objective containing the community
      objective (maximized) as well as a cooperativity cost which
      represents the  distance to the individuals "egoistic" maximum growth
      rate (minimized). Requires the `tradeoff` parameter. This method is
      still relatively fast and does require only few additional variables.
    - "linear lagrangian": The same as "lagrangian" only with a linear
      representation of the cooperativity cost (absolute value).
    - "moma": Minimization of metabolic adjustment. Simultaneously
      optimizes the community objective (maximize) and the cooperativity
      cost (minimize). This method finds an exact maximum but doubles the
      number of required variables, thus being slow.
    - "lmoma": The same as "moma" only with a linear
      representation of the cooperativity cost (absolute value).
    - "original": Solves the multi-objective problem described in [#p1]_.
      Here, the community growth rate is maximized simultanously with all
      individual growth rates. Note that there are usually many
      Pareto-optimal solutions to this problem and the method will only
      give one solution. This is also the slowest method.

    Parameters
    ----------
    community : micom.Community
        The community to optimize.
    strategy : str
        The strategy used to solve the OptCom formulation. Defaults to
        "lagrangian" which gives a decent tradeoff between speed and
        correctness.
    min_growth : float or array-like
        The minimal growth rate required for each individual. May be a
        single value or an array-like object with the same length as there
        are individuals.
    tradeoff : float in [0, 1]
        Only used for lagrangian strategies. Must be between 0 and 1 and
        describes the strength of the cooperativity cost / egoism. 1 means
        optimization will only minimize the cooperativity cost and zero
        means optimization will only maximize the community objective.
    fluxes : boolean
        Whether to return the fluxes as well.
    pfba : boolean
        Whether to obtain fluxes by parsimonious FBA rather than
        "classical" FBA.

    Returns
    -------
    micom.CommunitySolution
        The solution of the optimization. If fluxes==False will only contain
        the objective value, community growth rate and individual growth rates.

    References
    ----------
    .. [#p1] OptCom: a multi-level optimization framework for the metabolic
       modeling and analysis of microbial communities.
       Zomorrodi AR, Maranas CD. PLoS Comput Biol. 2012 Feb;8(2):e1002363.
       doi: 10.1371/journal.pcbi.1002363, PMID: 22319433

    """
    if strategy not in _methods:
        raise ValueError("strategy must be one of {}!".format(
                         ",".join(_methods)))
    funcs = _methods[strategy]

    with community as com:
        # Add needed variables etc.
        funcs[0](com, min_growth)
        if "lagrangian" in strategy:
            funcs[1](com, tradeoff)
        return solve(community, fluxes=fluxes, pfba=pfba)
