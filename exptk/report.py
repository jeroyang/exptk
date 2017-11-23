#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from collections import defaultdict

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
        return syntax.format(r=r, p=p, f=f, t=self.title)

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
        tp_count = gold_number * recall
        positive_count = tp_count / precision
        fp_count = positive_count - tp_count
        fn_count = gold_number - tp_count
        scale_report = cls(['tp'] * int(tp_count),
                           ['fp'] * int(fp_count),
                           ['fn'] * int(fn_count),
                           title)
        return scale_report
