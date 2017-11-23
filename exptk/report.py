#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from collections import defaultdict
from fractions import Fraction

def get_numerator(ratio, max_denominator):
    fraction = Fraction.from_float(ratio).limit_denominator(max_denominator)
    return int(fraction.numerator * max_denominator / fraction.denominator)

def get_denominator(ratio, max_numerator):
    return get_numerator(1/ratio, max_numerator)

class Report:
    """
    Holding the results of experiment, presenting the precision, recall,
    f1 score of the experiment.
    """
    def __init__(self, tp=[], fp=[], fn=[], title=None):
        """
        tp: the ture positive items
        fp: the false positive items
        fn: the false negative items
        title: the title of this report
        """
        self.tp = list(zip(tp, [title]*len(tp)))
        self.fp = list(zip(fp, [title]*len(fp)))
        self.fn = list(zip(fn, [title]*len(fn)))
        self.title = title

    def precision(self):
        try:
            return float(len(self.tp)) / (len(self.tp) + len(self.fp))
        except ZeroDivisionError:
            return 0.0

    def recall(self):
        try:
            return float(len(self.tp)) / (len(self.tp) + len(self.fn))
        except ZeroDivisionError:
            return 0.0

    def f1(self):
        r = self.recall()
        p = self.precision()
        try:
            return float(2 * r * p) / (r + p)
        except ZeroDivisionError:
            return 0.0

    def __repr__(self):
        r = self.recall()
        p = self.precision()
        f = self.f1()
        syntax = 'Report<P{p:.3f} R{r:.3f} F{f:.3f} {t!r}>'
        return syntax.format(p=p, r=r, f=f, t=self.title)

    @classmethod
    def from_reports(cls, reports, title):
        meta_report = cls([], [], [], title)
        for report in reports:
            meta_report.tp.extend(list(zip(report.tp, [title]*len(report.tp))))
            meta_report.fp.extend(list(zip(report.fp, [title]*len(report.fp))))
            meta_report.fn.extend(list(zip(report.fn, [title]*len(report.fn))))
        return meta_report

    def split(self):
        title2report = defaultdict(Report)
        for (content, title), _ in self.tp:
            title2report[title].tp.append(content)
        for (content, title), _ in self.fp:
            title2report[title].fp.append(content)
        for (content, title), _ in self.fn:
            title2report[title].fn.append(content)
        for title, report in title2report.items():
            report.title = title
        return list(title2report.values())

    @classmethod
    def from_scale(cls, gold_number, precision, recall, title):
        tp_count = get_numerator(recall, gold_number)
        positive_count = get_denominator(precision, tp_count)
        fp_count = positive_count - tp_count
        fn_count = gold_number - tp_count
        scale_report = cls(['tp'] * tp_count,
                           ['fp'] * fp_count,
                           ['fn'] * fn_count,
                           title)
        syntax = 'P{p:.3f} R{r:.3f}'
        wanted_title_part = syntax.format(p=precision, r=recall)
        if wanted_title_part == str(scale_report)[7:20]:
            return scale_report
        raise AssertionError('The precision and/or recall has error.\n',
                wanted_title_part, '!=', str(scale_report)[7:21])
