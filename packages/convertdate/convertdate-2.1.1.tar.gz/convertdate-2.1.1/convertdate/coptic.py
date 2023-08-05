#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of convertdate.
# http:#github.com/fitnr/convertdate

# Licensed under the MIT license:
# http:#opensource.org/licenses/MIT
# Copyright (c) 2017, fitnr <fitnr@fakeisthenewreal>
from .utils import floor, jwday, monthcalendarhelper
from . import gregorian

EPOCH = 1825029.5
MONTH_NAMES = ["Thout", "Paopi", "Hathor", "Koiak", "Tobi", "Meshir",
               "Paremhat", "Paremoude", "Pashons", "Paoni", "Epip", "Mesori", "Pi Kogi Enavot"]
DAY_NAMES = ["Tkyriaka", "Pesnau", "Pshoment", "Peftoou", "Ptiou", "Psoou", "Psabbaton"]


def is_leap(year):
    "Determine whether this is a leap year."
    return year % 4 == 3 or year % 4 == -1


def to_jd(year, month, day):
    "Retrieve the Julian date equivalent for this date"
    return day + (month - 1) * 30 + (year - 1) * 365 + floor(year / 4) + EPOCH - 1


def from_jd(jdc):
    "Create a new date from a Julian date."
    cdc = floor(jdc) + 0.5 - EPOCH
    year = floor((cdc - floor((cdc + 366) / 1461)) / 365) + 1

    yday = jdc - to_jd(year, 1, 1)

    month = floor(yday / 30) + 1
    day = yday - (month - 1) * 30 + 1
    return year, month, day


def to_gregorian(year, month, day):
    return gregorian.from_jd(to_jd(year, month, day))


def from_gregorian(year, month, day):
    return from_jd(gregorian.to_jd(year, month, day))


def month_length(year, month):
    if month <= 12:
        return 30

    elif month == 13:
        if is_leap(year):
            return 6
        else:
            return 5
    else:
        raise ValueError("Invalid month")


def monthcalendar(year, month):
    start_weekday = jwday(to_jd(year, month, 1))
    monthlen = month_length(year, month)
    return monthcalendarhelper(start_weekday, monthlen)
