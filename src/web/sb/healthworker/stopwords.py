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
                              | dc
                              | Halmashauri ya Wilaya ya
                              | MC
                              | Halmashauri ya Manispaa ya
                              | TC
                              | Halmashauri ya Mji wa
                              )
                              \b
                              """, re.I | re.X | re.U)

facility_pattern = re.compile(ur"""
                          \b
                          (?:
                          dental clinic
                          |kliniki ya meno
                          |dispensary
                          |zahanati
                          |eye clinic
                          |kliniki ya macho
                          |health center
                          |health centre
                          |kituo cha afya
                          |hospital
                          |hospitali
                          |maternity home
                          |kituo cha uzazi
                          |surgical clinic
                          |klinini ya upasuaj
                          |clinic
                          |kliniki
                          |vct
                          |kituo cha kutoa ushauri nasaha
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

