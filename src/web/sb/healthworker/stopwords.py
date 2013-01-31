import re

district_pattern = re.compile(ur"""
                              \b
                              (?:
                              rural
                              | vijijini
                              | urban
                              | mjini
                              | fbo
                              | kidini
                              | private
                              | binafsi
                              | public
                              | uma
                              | city
                              | jiji la
                              | district\s+council
                              | dc
                              | Halmashauri\s+ya\s+Wilaya\s+ya
                              | Municipal\s+Council
                              | mc
                              | Halmashauri\s+ya\s+Manispaa\s+ya
                              | Town\s+Council
                              | tc
                              | Halmashauri\s+ya\s+Mji\s+wa
                              | city
                              | Jiji\s+la
                              | municipal
                              | Manispaa
                              | town
                              | Mji
                              | district
                              )
                              \b
                              """, re.I | re.X | re.U)

facility_pattern = re.compile(ur"""
                          \b
                          (?:
                          dental\s+clinic
                          | kliniki\s+ya\s+meno
                          | dispensary
                          | zahanati
                          | eye\s+clinic
                          | kliniki\s+ya\s+macho
                          | health\s+center
                          | health\s+centre
                          | kituo\s+cha\s+afya
                          | hospital
                          | hospitali
                          | maternity\s+home
                          | kituo\scha\s+uzazi
                          | surgical\s+clinic
                          | klinini\s+ya\s+upasuaj
                          | clinic
                          | kliniki
                          | vct
                          | kituo\s+cha\s+kutoa\s+ushauri\s+nasaha
                          | district\s+council
                          | dc
                          | Halmashauri\s+ya\s+Wilaya\s+ya
                          | Municipal\s+Council
                          | mc
                          | Halmashauri\s+ya\s+Manispaa\s+ya
                          | Town\s+Council
                          | tc
                          | Halmashauri\s+ya\s+Mji\s+wa
                          | city
                          | Jiji\s+la
                          | municipal
                          | Manispaa
                          | town
                          | Mji
                          | district
                          )
                          \b
                          """, re.X | re.I | re.UNICODE)

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
  return fix_query(query, [facility_pattern])

def fix_district_query(query):
  return fix_query(query, [district_pattern])

