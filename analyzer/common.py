#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re


def match_regex(regex, string):
    '''
    extract the 1st matching regex from a string
    regex:  regex to be matched
    string: raw string to be matched
    '''
    match = re.findall(regex, string)

    if (len(match) < 1):
        match = None
    else:
        match = match[0]

    return match


def locate_keyword_from_lines(keyword, lines):
    '''
    Return position index of lines, if cannot find
    the keyword, return None
    '''
    flag = False
    pos = 0
    for line in lines:
        if (keyword in line):
            flag = True
            break
        pos += 1

    if (flag):
        return(pos)
    else:
        return(None)


def match_re_in_lines(re, lines, st=0, ed=None):
    '''
    Search a certain regular expression in lines [st, ed)
    If there is any match, return the 1st matching result,
    otherwise return None
    '''
    if (ed is None):
        ed = len(lines)

    for i in range(st, ed):
        match = match_regex(re, lines[i])
        if match is not None:
            return match

    return None