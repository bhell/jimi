# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table('price_country', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('price', ['Country'])

        # Adding model 'Tax'
        db.create_table('price_tax', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal('price', ['Tax'])

        # Adding M2M table for field region on 'Tax'
        db.create_table('price_tax_valid_in_country', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tax', models.ForeignKey(orm['price.tax'], null=False)),
            ('country', models.ForeignKey(orm['price.country'], null=False))
        ))
        db.create_unique('price_tax_valid_in_country', ['tax_id', 'country_id'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table('price_country')

        # Deleting model 'Tax'
        db.delete_table('price_tax')

        # Removing M2M table for field region on 'Tax'
        db.delete_table('price_tax_valid_in_country')


    models = {
        'price.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'price.tax': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tax'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'region': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['price.Country']", 'db_table': "'price_tax_valid_in_country'", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['price']