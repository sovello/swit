# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HealthWorker'
        db.create_table('healthworker_healthworker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.Facility'], null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('other_phone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('vodacom_phone', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('healthworker', ['HealthWorker'])

        # Adding M2M table for field specialties on 'HealthWorker'
        db.create_table('healthworker_healthworker_specialties', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('healthworker', models.ForeignKey(orm['healthworker.healthworker'], null=False)),
            ('specialty', models.ForeignKey(orm['healthworker.specialty'], null=False))
        ))
        db.create_unique('healthworker_healthworker_specialties', ['healthworker_id', 'specialty_id'])

        # Adding model 'RegionType'
        db.create_table('healthworker_regiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('healthworker', ['RegionType'])

        # Adding model 'Region'
        db.create_table('healthworker_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.RegionType'], null=True, blank=True)),
            ('parent_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.Region'], null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('healthworker', ['Region'])

        # Adding model 'FacilityType'
        db.create_table('healthworker_facilitytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('healthworker', ['FacilityType'])

        # Adding model 'Facility'
        db.create_table('healthworker_facility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.Region'], null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=128, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('ownership_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('place_type', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.FacilityType'], null=True)),
        ))
        db.send_create_signal('healthworker', ['Facility'])

        # Adding model 'Specialty'
        db.create_table('healthworker_specialty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=32, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('parent_specialty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.Specialty'], null=True, blank=True)),
        ))
        db.send_create_signal('healthworker', ['Specialty'])

        # Adding model 'MCTPayroll'
        db.create_table('healthworker_mctpayroll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('designation', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(max_length=255, null=True, blank=True)),
            ('check_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('health_worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.HealthWorker'], null=True, blank=True)),
            ('specialty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.Specialty'], null=True, blank=True)),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.Facility'], null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.Region'], null=True, blank=True)),
        ))
        db.send_create_signal('healthworker', ['MCTPayroll'])

        # Adding model 'MCTRegistration'
        db.create_table('healthworker_mctregistration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('cadre', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('current_employer', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('dates_of_registration_full', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('dates_of_registration_provisional', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('dates_of_registration_temporary', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('employer_during_internship', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.Facility'], null=True, blank=True)),
            ('file_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('health_worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['healthworker.HealthWorker'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('other_phone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('qualification_final', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('qualification_provisional', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('qualification_specialization_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('qualification_specialization_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('registration_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('registration_type', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('specialty', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('specialty_duration', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('healthworker', ['MCTRegistration'])

        # Adding M2M table for field specialties on 'MCTRegistration'
        db.create_table('healthworker_mctregistration_specialties', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mctregistration', models.ForeignKey(orm['healthworker.mctregistration'], null=False)),
            ('specialty', models.ForeignKey(orm['healthworker.specialty'], null=False))
        ))
        db.create_unique('healthworker_mctregistration_specialties', ['mctregistration_id', 'specialty_id'])


    def backwards(self, orm):
        # Deleting model 'HealthWorker'
        db.delete_table('healthworker_healthworker')

        # Removing M2M table for field specialties on 'HealthWorker'
        db.delete_table('healthworker_healthworker_specialties')

        # Deleting model 'RegionType'
        db.delete_table('healthworker_regiontype')

        # Deleting model 'Region'
        db.delete_table('healthworker_region')

        # Deleting model 'FacilityType'
        db.delete_table('healthworker_facilitytype')

        # Deleting model 'Facility'
        db.delete_table('healthworker_facility')

        # Deleting model 'Specialty'
        db.delete_table('healthworker_specialty')

        # Deleting model 'MCTPayroll'
        db.delete_table('healthworker_mctpayroll')

        # Deleting model 'MCTRegistration'
        db.delete_table('healthworker_mctregistration')

        # Removing M2M table for field specialties on 'MCTRegistration'
        db.delete_table('healthworker_mctregistration_specialties')


    models = {
        'healthworker.facility': {
            'Meta': {'object_name': 'Facility'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ownership_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'place_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.Region']", 'null': 'True', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.FacilityType']", 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'healthworker.facilitytype': {
            'Meta': {'object_name': 'FacilityType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'healthworker.healthworker': {
            'Meta': {'object_name': 'HealthWorker'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.Facility']", 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'other_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'specialties': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['healthworker.Specialty']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'vodacom_phone': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'healthworker.mctpayroll': {
            'Meta': {'object_name': 'MCTPayroll'},
            'birthdate': ('django.db.models.fields.DateField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'check_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'designation': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.Facility']", 'null': 'True', 'blank': 'True'}),
            'health_worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.HealthWorker']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.Region']", 'null': 'True', 'blank': 'True'}),
            'specialty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.Specialty']", 'null': 'True', 'blank': 'True'})
        },
        'healthworker.mctregistration': {
            'Meta': {'object_name': 'MCTRegistration'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cadre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_employer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dates_of_registration_full': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dates_of_registration_provisional': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dates_of_registration_temporary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'employer_during_internship': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.Facility']", 'null': 'True', 'blank': 'True'}),
            'file_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'health_worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.HealthWorker']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'other_phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'qualification_final': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'qualification_provisional': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'qualification_specialization_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'qualification_specialization_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'registration_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'registration_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'specialties': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['healthworker.Specialty']", 'symmetrical': 'False'}),
            'specialty': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'specialty_duration': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'healthworker.region': {
            'Meta': {'object_name': 'Region'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.Region']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.RegionType']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'healthworker.regiontype': {
            'Meta': {'object_name': 'RegionType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'healthworker.specialty': {
            'Meta': {'object_name': 'Specialty'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_specialty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['healthworker.Specialty']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['healthworker']