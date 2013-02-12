import re

import os
import os.path

_root = os.path.split(__file__)[0]
common_phrases_txt = os.path.join(_root, 'common-phrases.txt')
facility_common_phrases_txt = os.path.join(_root, 'facility-common-phrases.txt')
district_common_phrases_txt = os.path.join(_root, 'district-common-phrases.txt')

def get_pattern(files):
  phrase_terms = []
  for f in files:
    with open(f, "r") as a_file:
      for line in a_file:
        terms = line.decode('utf-8').strip().lower().split()
        if not terms:
          continue
        phrase_terms.append(terms)
  phrase_terms.sort(key=len)
  phrase_terms.reverse()
  pattern = (ur"\b(?:"
             + ur"|".join(ur"\s+".join(terms) for terms in phrase_terms)
             + ur")\b")
  pattern = re.compile(pattern, re.I | re.X | re.U)
  return pattern

_facility_pat = None

def get_facility_pattern():
  global _facility_pat
  if _facility_pat is None:
    _facility_pat = get_pattern([common_phrases_txt, facility_common_phrases_txt])
  return _facility_pat

_district_pat = None

def get_district_pattern():
  global _district_pat
  if _district_pat is None:
    _district_pat = get_pattern([common_phrases_txt, district_common_phrases_txt])
  return _district_pat

def fix_query(q, patterns):
  if q:
    if patterns:
      for p in patterns:
        replaced = p.sub(u' ', q)
        # avoid generating the empty string:
        if replaced.strip() == u'':
          replaced = q
        else:
          q = replaced
    # fix whitespace
    return u' '.join(q.split())
  else:
    return u''

def fix_facility_query(query):
  return fix_query(query, [get_facility_pattern()])

def fix_district_query(query):
  return fix_query(query, [get_district_pattern()])

