#!python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2017 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr

"""
Evaluation

Usage:
  pyannote-metrics.py detection [--subset=<subset> --collar=<seconds> --skip-overlap] <database.task.protocol> <hypothesis.mdtm>
  pyannote-metrics.py segmentation [--subset=<subset> --tolerance=<seconds>] <database.task.protocol> <hypothesis.mdtm>
  pyannote-metrics.py diarization [--subset=<subset> --greedy --collar=<seconds> --skip-overlap] <database.task.protocol> <hypothesis.mdtm>
  pyannote-metrics.py identification [--subset=<subset> --collar=<seconds> --skip-overlap] <database.task.protocol> <hypothesis.mdtm>
  pyannote-metrics.py spotting [--subset=<subset>] <database.task.protocol> <hypothesis.json>
  pyannote-metrics.py -h | --help
  pyannote-metrics.py --version

Options:
  <database.task.protocol>   Set evaluation protocol (e.g. "Etape.SpeakerDiarization.TV")
  --subset=<subset>          Evaluated subset (train|developement|test) [default: test]
  --collar=<seconds>         Collar, in seconds [default: 0.0].
  --skip-overlap             Do not evaluate overlap regions.
  --tolerance=<seconds>      Tolerance, in seconds [default: 0.5].
  --greedy                   Use greedy diarization error rate.
  -h --help                  Show this screen.
  --version                  Show version.

All modes but "spotting" expect hypothesis using the MDTM file format.
MDTM files contain one line per speech turn, using the following convention:

<uri> 1 <start_time> <duration> speaker <confidence> <gender> <speaker_id>

    * uri: file identifier (as given by pyannote.database protocols)
    * start_time: speech turn start time in seconds
    * duration: speech turn duration in seconds
    * confidence: confidence score (can be anything, not used for now)
    * gender: speaker gender (can be anything, not used for now)
    * speaker_id: speaker identifier

"spotting" mode expects hypothesis using the following JSON file format.
It should contain a list of trial hypothesis, using the same trial order as
pyannote.database speaker spotting protocols (e.g. protocol.test_trial())

[
    {'uri': '<uri>', 'model_id': '<model_id>', 'scores': [[<t1>, <v1>], [<t2>, <v2>], ... [<tn>, <vn>]]},
    {'uri': '<uri>', 'model_id': '<model_id>', 'scores': [[<t1>, <v1>], [<t2>, <v2>], ... [<tn>, <vn>]]},
    {'uri': '<uri>', 'model_id': '<model_id>', 'scores': [[<t1>, <v1>], [<t2>, <v2>], ... [<tn>, <vn>]]},
    ...
    {'uri': '<uri>', 'model_id': '<model_id>', 'scores': [[<t1>, <v1>], [<t2>, <v2>], ... [<tn>, <vn>]]},
]

    * uri: file identifier (as given by pyannote.database protocols)
    * model_id: target identifier (as given by pyannote.database protocols)
    * [ti, vi]: [time, value] pair indicating that the system has output the
                score vi at time ti (e.g. [10.2, 0.2] means that the system
                gave a score of 0.2 at time 10.2s).

Calling "spotting" mode will create a bunch of files.
* <hypothesis.det.txt> contains DET curve using the following raw file format:
    <threshold> <fpr> <fnr>
* <hypothesis.lcy.txt> contains latency curves using this format:
    <threshold> <fpr> <fnr> <speaker_latency> <absolute_latency>

"""


# command line parsing
from docopt import docopt

import sys
import json
import warnings
import functools
import numpy as np
import pandas as pd
from tabulate import tabulate
import multiprocessing as mp

# use for parsing hypothesis file
from pyannote.parser import MagicParser

# evaluation protocols
from pyannote.database import get_protocol
from pyannote.database.util import get_annotated

from pyannote.metrics.detection import DetectionErrorRate
from pyannote.metrics.detection import DetectionAccuracy
from pyannote.metrics.detection import DetectionRecall
from pyannote.metrics.detection import DetectionPrecision

from pyannote.metrics.segmentation import SegmentationPurity
from pyannote.metrics.segmentation import SegmentationCoverage
from pyannote.metrics.segmentation import SegmentationPrecision
from pyannote.metrics.segmentation import SegmentationRecall

from pyannote.metrics.diarization import GreedyDiarizationErrorRate
from pyannote.metrics.diarization import DiarizationErrorRate
from pyannote.metrics.diarization import DiarizationPurity
from pyannote.metrics.diarization import DiarizationCoverage

from pyannote.metrics.identification import IdentificationErrorRate
from pyannote.metrics.identification import IdentificationPrecision
from pyannote.metrics.identification import IdentificationRecall

from pyannote.metrics.spotting import LowLatencySpeakerSpotting

showwarning_orig = warnings.showwarning

def showwarning(message, category, *args, **kwargs):
    import sys
    print(category.__name__ + ':', str(message))

warnings.showwarning = showwarning

def get_hypothesis(hypotheses, item):

    uri = item['uri']

    if uri in hypotheses.uris:
        hypothesis = hypotheses(uri=uri)
    else:
        # if the exact 'uri' is not available in hypothesis,
        # look for matching substring
        tmp_uri = [u for u in hypotheses.uris if u in uri]
        if len(tmp_uri) == 0:
            msg = 'Could not find hypothesis for file "{uri}".'
            raise ValueError(msg.format(uri=uri))
        elif len(tmp_uri) > 1:
            msg = 'Found too many hypotheses matching file "{uri}" ({uris}).'
            raise ValueError(msg.format(uri=uri, uris=tmp_uri))
        else:
            tmp_uri = tmp_uri[0]
            msg = 'Could not find hypothesis for file "{uri}"; using "{tmp_uri}" instead.'
            warnings.warn(msg.format(tmp_uri=tmp_uri, uri=uri))

        hypothesis = hypotheses(uri=tmp_uri)
        hypothesis.uri = uri

    return hypothesis

def process_one(item, hypotheses=None, metrics=None):
    reference = item['annotation']
    hypothesis = get_hypothesis(hypotheses, item)
    uem = get_annotated(item)
    return {key: metric(reference, hypothesis, uem=uem)
            for key, metric in metrics.items()}

def get_reports(protocol, subset, hypotheses, metrics):

    process = functools.partial(process_one,
                                hypotheses=hypotheses,
                                metrics=metrics)

    # get items and their number
    progress = protocol.progress
    protocol.progress = False
    items = list(getattr(protocol, subset)())
    protocol.progress = progress
    n_items = len(items)

    # heuristic to estimate the optimal number of processes
    chunksize = 20
    processes = max(1, min(mp.cpu_count(), n_items // chunksize))

    pool = mp.Pool(processes)
    _ = pool.map(process, items, chunksize=chunksize)

    return {key: metric.report(display=False)
            for key, metric in metrics.items()}

def reindex(report, protocol, subset):
    progress = protocol.progress
    protocol.progress = False
    new_index = [item['uri'] for item in getattr(protocol, subset)()] + \
                ['TOTAL']
    protocol.progress = progress
    return report.reindex(new_index)

def detection(protocol, subset, hypotheses, collar=0.0, skip_overlap=False):

    metrics = {
        'error': DetectionErrorRate(collar=collar, skip_overlap=skip_overlap),
        'accuracy': DetectionAccuracy(collar=collar,
                                      skip_overlap=skip_overlap),
        'precision': DetectionPrecision(collar=collar,
                                        skip_overlap=skip_overlap),
        'recall': DetectionRecall(collar=collar, skip_overlap=skip_overlap)}

    reports = get_reports(protocol, subset, hypotheses, metrics)

    report = metrics['error'].report(display=False)
    accuracy = metrics['accuracy'].report(display=False)
    precision = metrics['precision'].report(display=False)
    recall = metrics['recall'].report(display=False)

    report['accuracy', '%'] = accuracy[metrics['accuracy'].name, '%']
    report['precision', '%'] = precision[metrics['precision'].name, '%']
    report['recall', '%'] = recall[metrics['recall'].name, '%']

    report = reindex(report, protocol, subset)

    columns = list(report.columns)
    report = report[[columns[0]] + columns[-3:] + columns[1:-3]]

    summary = 'Detection (collar = {0:g} ms{1})'.format(
        1000*collar, ', no overlap' if skip_overlap else '')

    headers = [summary] + \
              [report.columns[i][0] for i in range(4)] + \
              ['%' if c[1] == '%' else c[0] for c in report.columns[4:]]

    print(tabulate(report, headers=headers, tablefmt="simple",
                   floatfmt=".2f", numalign="decimal", stralign="left",
                   missingval="", showindex="default", disable_numparse=False))

def segmentation(protocol, subset, hypotheses, tolerance=0.5):

    metrics = {'coverage': SegmentationCoverage(tolerance=tolerance),
               'purity': SegmentationPurity(tolerance=tolerance),
               'precision': SegmentationPrecision(tolerance=tolerance),
               'recall': SegmentationRecall(tolerance=tolerance)}

    reports = get_reports(protocol, subset, hypotheses, metrics)

    coverage = metrics['coverage'].report(display=False)
    purity = metrics['purity'].report(display=False)
    precision = metrics['precision'].report(display=False)
    recall = metrics['recall'].report(display=False)

    coverage = coverage[metrics['coverage'].name]
    purity = purity[metrics['purity'].name]
    precision = precision[metrics['precision'].name]
    recall = recall[metrics['recall'].name]

    report = pd.concat([coverage, purity, precision, recall], axis=1)
    report = reindex(report, protocol, subset)

    headers = ['Segmentation (tolerance = {0:g} ms)'.format(1000*tolerance),
               'coverage', 'purity', 'precision', 'recall']
    print(tabulate(report, headers=headers, tablefmt="simple",
                   floatfmt=".2f", numalign="decimal", stralign="left",
                   missingval="", showindex="default", disable_numparse=False))

def diarization(protocol, subset, hypotheses, greedy=False,
                collar=0.0, skip_overlap=False):

    metrics = {
        'purity': DiarizationPurity(collar=collar, skip_overlap=skip_overlap),
        'coverage': DiarizationCoverage(collar=collar,
                                        skip_overlap=skip_overlap)}

    if greedy:
        metrics['error'] = GreedyDiarizationErrorRate(
            collar=collar, skip_overlap=skip_overlap)
    else:
        metrics['error'] = DiarizationErrorRate(
            collar=collar, skip_overlap=skip_overlap)

    reports = get_reports(protocol, subset, hypotheses, metrics)

    report = metrics['error'].report(display=False)
    purity = metrics['purity'].report(display=False)
    coverage = metrics['coverage'].report(display=False)

    report['purity', '%'] = purity[metrics['purity'].name, '%']
    report['coverage', '%'] = coverage[metrics['coverage'].name, '%']

    columns = list(report.columns)
    report = report[[columns[0]] + columns[-2:] + columns[1:-2]]

    report = reindex(report, protocol, subset)

    summary = 'Diarization ({0:s}collar = {1:g} ms{2})'.format(
                'greedy, ' if greedy else '',
                1000 * collar,
                ', no overlap' if skip_overlap else '')

    headers = [summary] + \
              [report.columns[i][0] for i in range(3)] + \
              ['%' if c[1] == '%' else c[0] for c in report.columns[3:]]

    print(tabulate(report, headers=headers, tablefmt="simple",
                   floatfmt=".2f", numalign="decimal", stralign="left",
                   missingval="", showindex="default", disable_numparse=False))

def identification(protocol, subset, hypotheses,
                   collar=0.0, skip_overlap=False):

    metrics = {
        'error': IdentificationErrorRate(collar=collar,
                                         skip_overlap=skip_overlap),
        'precision': IdentificationPrecision(collar=collar,
                                             skip_overlap=skip_overlap),
        'recall': IdentificationRecall(collar=collar,
                                       skip_overlap=skip_overlap)}

    reports = get_reports(protocol, subset, hypotheses, metrics)

    report = metrics['error'].report(display=False)
    precision = metrics['precision'].report(display=False)
    recall = metrics['recall'].report(display=False)

    report['precision', '%'] = precision[metrics['precision'].name, '%']
    report['recall', '%'] = recall[metrics['recall'].name, '%']

    columns = list(report.columns)
    report = report[[columns[0]] + columns[-2:] + columns[1:-2]]

    report = reindex(report, protocol, subset)

    summary = 'Identification (collar = {1:g} ms{2})'.format(
                1000 * collar,
                ', no overlap' if skip_overlap else '')

    headers = [summary] + \
              [report.columns[i][0] for i in range(3)] + \
              ['%' if c[1] == '%' else c[0] for c in report.columns[3:]]

    print(tabulate(report, headers=headers, tablefmt="simple",
                   floatfmt=".2f", numalign="decimal", stralign="left",
                   missingval="", showindex="default", disable_numparse=False))

def spotting(protocol, subset, hypotheses, output_prefix):

    Scores = []
    trials = getattr(protocol, '{subset}_trial'.format(subset=subset))()
    for i, (current_trial, hypothesis) in enumerate(zip(trials, hypotheses)):

        # check trial/hypothesis target consistency
        try:
            assert current_trial['model_id'] == hypothesis['model_id']
        except AssertionError as e:
            msg = ('target mismatch in trial #{i} '
                   '(found: {found}, should be: {should_be})')
            raise ValueError(
                msg.format(i=i, found=hypothesis['model_id'],
                           should_be=current_trial['model_id']))

        # check trial/hypothesis file consistency
        try:
            assert current_trial['uri'] == hypothesis['uri']
        except AssertionError as e:
            msg = ('file mismatch in trial #{i} '
                   '(found: {found}, should be: {should_be})')
            raise ValueError(
                msg.format(i=i, found=hypothesis['uri'],
                           should_be=current_trial['uri']))

        # check at least one score is provided
        try:
            assert len(hypothesis['scores']) > 0
        except AssertionError as e:
            msg = ('empty list of scores in trial #{i}.')
            raise ValueError(msg.format(i=i))

        timestamps, scores = zip(*hypothesis['scores'])
        Scores.append(scores)

        # check trial/hypothesis timerange consistency
        try_with = current_trial['try_with']
        try:
            assert min(timestamps) >= try_with.start
        except AssertionError as e:
            msg = ('incorrect timestamp in trial #{i} '
                   '(found: {found:g}, should be: >= {should_be:g})')
            raise ValueError(
                msg.format(i=i,
                found=min(timestamps),
                should_be=try_with.start))

    # estimate best set of thresholds
    scores = np.concatenate(Scores)
    epsilons = np.array(
        [n * 10**(-e) for e in range(4, 1, -1) for n in range(1, 10)])
    percentile = np.concatenate([epsilons, np.arange(0.1, 100., 0.1), 100 - epsilons[::-1]])
    thresholds = np.percentile(scores, percentile)

    metric = LowLatencySpeakerSpotting(thresholds=thresholds)
    trials = getattr(protocol, '{subset}_trial'.format(subset=subset))()
    for i, (current_trial, hypothesis) in enumerate(zip(trials, hypotheses)):
        reference = current_trial['reference']
        metric(reference, hypothesis['scores'])

    thresholds, fpr, fnr, eer, _ = metric.det_curve(return_latency=False)

    print('EER = {eer:.2f}%'.format(eer=100 * eer))

    # save DET curve to hypothesis.det.txt
    det_path = '{output_prefix}.det.txt'.format(output_prefix=output_prefix)
    det_tmpl = '{t:.9f} {p:.9f} {n:.9f}\n'
    with open(det_path, mode='w') as fp:
        fp.write('# threshold false_positive_rate false_negative_rate\n')
        for t, p, n in zip(thresholds, fpr, fnr):
            line = det_tmpl.format(t=t, p=p, n=n)
            fp.write(line)

    print('DET curve saved to {det_path}'.format(det_path=det_path))

    thresholds, fpr, fnr, _, _, speaker_lcy, absolute_lcy = \
        metric.det_curve(return_latency=True)

    # save DET curve to hypothesis.det.txt
    lcy_path = '{output_prefix}.lcy.txt'.format(output_prefix=output_prefix)
    lcy_tmpl = '{t:.9f} {p:.9f} {n:.9f} {s:.6f} {a:.6f}\n'
    with open(lcy_path, mode='w') as fp:
        fp.write('# threshold false_positive_rate false_negative_rate speaker_latency absolute_latency\n')
        for t, p, n, s, a in zip(thresholds, fpr, fnr, speaker_lcy, absolute_lcy):
            if p == 1:
                continue
            if np.isnan(s):
                continue
            line = lcy_tmpl.format(t=t, p=p, n=n, s=s, a=a)
            fp.write(line)

    print('Latency curve saved to {lcy_path}'.format(lcy_path=lcy_path))

if __name__ == '__main__':

    arguments = docopt(__doc__, version='Evaluation')

    # protocol
    protocol_name = arguments['<database.task.protocol>']
    protocol = get_protocol(protocol_name, progress=True)

    # subset (train, development, or test)
    subset = arguments['--subset']

    collar = float(arguments['--collar'])
    skip_overlap = arguments['--skip-overlap']
    tolerance = float(arguments['--tolerance'])

    if arguments['spotting']:

        hypothesis_json = arguments['<hypothesis.json>']
        with open(hypothesis_json, mode='r') as fp:
            hypotheses = json.load(fp)

        output_prefix = hypothesis_json[:-5]

        spotting(protocol, subset, hypotheses, output_prefix)
        sys.exit(0)

    # hypothesis
    hypothesis_mdtm = arguments['<hypothesis.mdtm>']
    hypotheses = MagicParser().read(hypothesis_mdtm, modality='speaker')

    if arguments['detection']:
        detection(protocol, subset, hypotheses,
                  collar=collar, skip_overlap=skip_overlap)

    if arguments['segmentation']:
        segmentation(protocol, subset, hypotheses, tolerance=tolerance)

    if arguments['diarization']:
        greedy = arguments['--greedy']
        diarization(protocol, subset, hypotheses, greedy=greedy,
                    collar=collar, skip_overlap=skip_overlap)

    if arguments['identification']:
        identification(protocol, subset, hypotheses,
                       collar=collar, skip_overlap=skip_overlap)
