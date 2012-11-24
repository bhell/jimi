# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Node._supplier'
        db.add_column('jimi_catalog', '_supplier',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_column='supplier', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Node._supplier'
        db.delete_column('jimi_catalog', 'supplier')


    models = {
        'catalog.node': {
            'Meta': {'object_name': 'Node', 'db_table': "'jimi_catalog'"},
            '_supplier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'supplier'", 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fragment_in_stock': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fragment_pending_customer': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fragment_pending_supplier': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['catalog.Node']"}),
            'price_fragment': ('jimi.price.fields.MoneyField', [], {'default': '0.0', 'max_length': '21'}),
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