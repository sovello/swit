# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

old_fn_sql = r"""
create or replace function is_similar(needle text, haystack text, max_distance real default 0.3) returns boolean as $$
declare
  needle_tokens text[];
  haystack_tokens text[];
  found_tokens text[];
  haystack_token text;
  needle_token text;
  needle_found boolean;
begin
  haystack_tokens := regexp_split_to_array(lower(haystack), E'\\s+');
  needle_tokens := regexp_split_to_array(lower(needle), E'\\s+');
  if array_length(needle_tokens, 1) = 0 and array_length(haystack_tokens, 1) = 0 then
    return true;
  end if;

  foreach needle_token in array needle_tokens loop
    needle_found := false;
    foreach haystack_token in array haystack_tokens loop
      exit when needle_found;
      continue when ARRAY[haystack_token] <@ found_tokens; -- don't reuse haystack tokens
      needle_found := similarity(needle_token, haystack_token) >= (1-max_distance);
      if needle_found then
        found_tokens := found_tokens || haystack_token;
      end if;
    end loop;

    -- If any needles are not found, it's not a match
    if not needle_found then
      return false;
    end if;
  end loop;

  -- There is a match as long as one needle was found
  return array_length(found_tokens, 1) > 0;
end;
$$ language plpgsql;
"""

new_fn_sql = r"""
create or replace function is_similar(needle text, haystack text, max_distance real default 0.5) returns boolean as $$
declare
  needle_tokens text[];
  haystack_tokens text[];
  found_tokens text[];
  haystack_token text;
  needle_token text;
  needle_found boolean;
begin
  haystack_tokens := regexp_split_to_array(lower(haystack), E'\\s+');
  needle_tokens := regexp_split_to_array(lower(needle), E'\\s+');
  if array_length(needle_tokens, 1) = 0 and array_length(haystack_tokens, 1) = 0 then
    return true;
  end if;

  foreach needle_token in array needle_tokens loop
    needle_found := false;
    foreach haystack_token in array haystack_tokens loop
      exit when needle_found;
      continue when ARRAY[haystack_token] <@ found_tokens; -- don't reuse haystack tokens
      needle_found := char_length(needle_token) > 1 and char_length(haystack_token) > 1 and similarity(needle_token, haystack_token) >= (1-max_distance);
      if needle_found then
        found_tokens := found_tokens || haystack_token;
      end if;
    end loop;

    -- If any needles are not found, it's not a match
    if not needle_found then
      return false;
    end if;
  end loop;

  -- There is a match as long as one needle was found
  return array_length(found_tokens, 1) > 0;
end;
$$ language plpgsql;
"""

class Migration(SchemaMigration):
  def forwards(self, orm):
    db.execute(new_fn_sql)

  def backwards(self, orm):
    db.execute(old_fn_sql)

