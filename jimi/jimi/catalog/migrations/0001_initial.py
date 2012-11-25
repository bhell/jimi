# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Variance'
        db.create_table('jimi_variance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('internal_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('catalog', ['Variance'])

        # Adding model 'Variant'
        db.create_table('jimi_variant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('internal_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('variance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Variance'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('catalog', ['Variant'])

        # Adding model 'Node'
        db.create_table('jimi_catalog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['catalog.Node'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
            ('teaser', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('_supplier', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='supplier', blank=True)),
            ('_price', self.gf('jimi.price.fields.MoneyField')(default=0.0, max_length=21, db_column='price')),
            ('_stock', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='stock')),
            ('_pending_customer', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='pending_customer')),
            ('_pending_supplier', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='pending_supplier')),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('catalog', ['Node'])

        # Adding M2M table for field variant on 'Node'
        db.create_table('jimi_productvariant', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('node', models.ForeignKey(orm['catalog.node'], null=False)),
            ('variant', models.ForeignKey(orm['catalog.variant'], null=False))
        ))
        db.create_unique('jimi_productvariant', ['node_id', 'variant_id'])


    def backwards(self, orm):
        # Deleting model 'Variance'
        db.delete_table('jimi_variance')

        # Deleting model 'Variant'
        db.delete_table('jimi_variant')

        # Deleting model 'Node'
        db.delete_table('jimi_catalog')

        # Removing M2M table for field variant on 'Node'
        db.delete_table('jimi_productvariant')


    models = {
        'catalog.node': {
            'Meta': {'object_name': 'Node', 'db_table': "'jimi_catalog'"},
            '_pending_customer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'pending_customer'"}),
            '_pending_supplier': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'pending_supplier'"}),
            '_price': ('jimi.price.fields.MoneyField', [], {'default': '0.0', 'max_length': '21', 'db_column': "'price'"}),
            '_stock': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'stock'"}),
            '_supplier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'supplier'", 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['catalog.Node']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'teaser': ('django.db.models.fields.TextField', [], {}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'variant': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.Variant']", 'symmetrical': 'False', 'db_table': "'jimi_productvariant'", 'blank': 'True'})
        },
        'catalog.variance': {
            'Meta': {'object_name': 'Variance', 'db_table': "'jimi_variance'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'catalog.variant': {
            'Meta': {'object_name': 'Variant', 'db_table': "'jimi_variant'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'variance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Variance']"})
        }
    }

    complete_apps = ['catalog']