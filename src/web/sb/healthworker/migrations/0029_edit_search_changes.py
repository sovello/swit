# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

drop_fn_sql = r"""drop function if exists edit_search(needle text, haystack text, max_edits integer)"""

create_fn_sql = r"""
create or replace function is_similar(needle text, haystack text, max_distance real default 0.3) returns boolean as $$
declare
  needle_tokens text[];
  haystack_tokens text[];
  haystack_token text;
  needle_token text;
  needle_found boolean;
  any_needles_not_found boolean;
  any_needles_found boolean;
begin
  haystack_tokens = regexp_split_to_array(lower(haystack), E'\\s+');
  needle_tokens = regexp_split_to_array(lower(needle), E'\\s+');
  any_needles_not_found = false;
  any_needles_found = false;
  if array_length(needle_tokens, 1) = 0 and array_length(haystack_tokens, 1) = 0 then
    return true;
  end if;
  foreach needle_token in array needle_tokens loop
    exit when any_needles_not_found;
    needle_found = false;
    foreach haystack_token in array haystack_tokens loop
      exit when needle_found;
      needle_found = similarity(needle_token, haystack_token) >= (1-max_distance);
      --if dmetaphone_alt(needle_token) = dmetaphone_alt(haystack_token) then
      --  needle_found = true;
      --end if;
    end loop;
    any_needles_not_found = any_needles_not_found or (not needle_found);
    any_needles_found = any_needles_found or needle_found;
  end loop;
  -- there is a match if there weren't any needles found
  return (not any_needles_not_found) and any_needles_found;
end;
$$ language plpgsql;
"""

class Migration(SchemaMigration):
  def forwards(self, orm):
    db.execute(drop_fn_sql)
    db.execute(create_fn_sql)

  def backwards(self, orm):
    db.execute(drop_fn_sql)

