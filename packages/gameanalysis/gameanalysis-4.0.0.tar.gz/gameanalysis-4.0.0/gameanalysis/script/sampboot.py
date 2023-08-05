"""calculate bootstrap bounds from deviation samples"""
import argparse
import json
import sys

import numpy as np

from gameanalysis import bootstrap
from gameanalysis import gamereader
from gameanalysis import rsgame


def add_parser(subparsers):
    parser = subparsers.add_parser(
        'sampboot', help="""Bootstrap on sample payoffs from a mixture""",
        description="""Compute bootstrap statistics using samples from a
        mixture. Return type is a dictionary that maps percentiles to
        values.""")
    parser.add_argument(
        '--input', '-i', metavar='<input-file>', default=sys.stdin,
        type=argparse.FileType('r'), help="""Input data to run bootstrap on.
        Input should be a json list of surpluses drawn from the distribution of
        interest. (default: stdin)""")
    parser.add_argument(
        '--output', '-o', metavar='<output-file>', default=sys.stdout,
        type=argparse.FileType('w'), help="""Output file for script. (default:
        stdout)""")
    parser.add_argument(
        '--regret', '-r', nargs=2, metavar=('<game-file>', '<mix-file>'),
        type=argparse.FileType('r'), help="""Compute bootstrap regret from
        deviations instead of raw surplus values. This input should be a list
        of objects with role, strategy, and payoff indicating the payoff to
        deviating. The two arguments to this parameter must be a file with a
        game specification, and a file with the mixture the deviation samples
        were drawn from.""")
    parser.add_argument(
        '--dev-surplus', '-d', nargs=2, metavar=('<game-file>', '<mix-file>'),
        type=argparse.FileType('r'), help="""Compute bootstrap surplus from
        deviations instead of raw surplus values.  The arguments and inputs
        must look the same as regret, but this will bootstrap over surplus
        instead.""")
    parser.add_argument(
        '--percentiles', '-p', metavar='percentile', type=float, nargs='+',
        help="""Percentiles to return in [0, 100]. By default all bootstrap
        values will be returned sorted.""")
    parser.add_argument(
        '--num-bootstraps', '-n', metavar='num-bootstraps', default=101,
        type=int, help="""The number of bootstrap samples to acquire. More
        samples takes longer, but in general the percentiles requested should
        be a multiple of this number minus 1, otherwise there will be some
        error due to linear interpolation between points.  (default:
        %(default)s)""")
    parser.add_argument(
        '--mean', '-m', action='store_true', help="""In addition to bootstrap
        confidence intervals, also return the mean value.  This is in the
        dictionary with key 'mean'.""")
    return parser


def _unpack_datum(role, strategy, payoff, **_):
    return role, strategy, payoff


def load_devs(game, data):
    devs = np.empty((len(data) // game.num_strats, game.num_strats))
    inds = np.zeros(game.num_strats, int)
    for datum in data:
        role, strat, pay = _unpack_datum(**datum)
        sind = game.role_strat_index(role, strat)
        devs[inds[sind], sind] = pay
        inds[sind] += 1
    return devs


def main(args):
    data = json.load(args.input)
    if args.regret is not None:
        game = gamereader.read(json.load(args.regret[0]))
        game = rsgame.emptygame_copy(game)  # gc any extra data
        mix = game.from_mix_json(json.load(args.regret[1]))
        devs = load_devs(game, data)
        expect = np.add.reduceat(devs * mix, game.role_starts, 1)
        result = bootstrap.sample_regret(game, expect, devs,
                                         args.num_bootstraps,
                                         percentiles=args.percentiles)
        if args.mean:
            mdevs = devs.mean(0)
            mexpect = np.add.reduceat(
                mdevs * mix, game.role_starts).repeat(game.num_role_strats)
            mean = np.max(mdevs - mexpect)

    elif args.dev_surplus is not None:
        game = gamereader.read(json.load(args.dev_surplus[0]))
        game = rsgame.emptygame_copy(game)  # gc any extra data
        mix = game.from_mix_json(json.load(args.dev_surplus[1]))
        devs = load_devs(game, data)
        surpluses = np.sum(
            devs * mix * game.num_role_players.repeat(game.num_role_strats), 1)
        result = bootstrap.mean(surpluses, args.num_bootstraps,
                                percentiles=args.percentiles)
        if args.mean:
            mean = surpluses.mean()

    else:
        data = np.asarray(data, float)
        result = bootstrap.mean(data, args.num_bootstraps,
                                percentiles=args.percentiles)
        if args.mean:
            mean = data.mean()

    if args.percentiles is None:
        args.percentiles = np.linspace(0, 100, args.num_bootstraps)
    jresult = {str(p).rstrip('0').rstrip('.'): v.item()
               for p, v in zip(args.percentiles, result)}
    if args.mean:
        jresult['mean'] = mean

    json.dump(jresult, args.output)
    args.output.write('\n')
