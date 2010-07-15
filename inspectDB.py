#!/usr/bin/env python

# django init for standalone scripts
from django.core.management import setup_environ
import settings
setup_environ(settings)

# rest of imports
import sys
import django
import re

try:
    set
except NameError:
    from sets import Set as set   # Python 2.3 fallback


def loadSqlOrder(scriptfile):
    """Loads a SQL create table script, and returns a list with the
    tables created in the same order as in the script"""

    searchingFor = "CREATE TABLE"
    try:
        fp = open( scriptfile, 'r')
    except IOError:
        return None;

    #get all the CREATE TABLE lines of the script
    pattern = re.compile(searchingFor, re.IGNORECASE)
    tables = filter(pattern.search, fp.readlines())
    fp.close()

    #removes the CREATE TABLE part, and strips the string 
    f = lambda s : s[ s.find(searchingFor) + len(searchingFor) : len(s)-2 ].strip() 
    
    return map(f, tables)


def sortListByList(list, listOrd):    
    """Applies the order of the listOrd (ordered) elements, 
    into list elements."""
    return listOrd \
            + [item for item in list if not listOrd.__contains__(item)]


def inspectdb(tableOrder=[]):
    "Generator that introspects the tables in the given database name and returns a Django model, one line at a time."
    from django.db import connection, get_introspection_module
    import keyword

    introspection_module = get_introspection_module()

    #table2model = lambda table_name: table_name.title().replace('_', '')
    table2model = lambda table_name: table_name

    cursor = connection.cursor()
    yield "# This is an auto-generated customized Django model module for the IRAM-30m Archive"
    yield "# If you provide an SQL script, the models' order should be OK"
    yield "# In other case, please rearrange models' order!"
    yield "#"
    yield "# Also Many to Many tables ('*_has_*' or '*_usedin_*') are ignored and replaced with ManyToManyField. Please check it!"
    yield "#"
    yield "# You'll have to do the following manually to clean this up:"
    yield "#    * Replace any reference to model User to use django.user (e.g %s/DjangoUsers/User/g)"
    yield "#    * Fix CharField max_length: 60->20 ; 135 -> 45 ; 765 -> 255 "
    yield "#    * Replace IntegerField with BooleanField when needed "
    yield "# Feel free to rename the models, but don't rename db_table values or field names."
    yield "#"
    yield "# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'"
    yield "# into your database."
    yield ''
    yield 'from django.db import models'
    yield 'from django.contrib.auth.models import User'
    yield ''

    tablesList = sortListByList( introspection_module.get_table_list(cursor), tableOrder ) 

    pattern = re.compile("_(has|usedin)_", re.IGNORECASE)    
    #remove the many2many table
    for table_name in filter( lambda i: not pattern.search(i), tablesList ):
        yield 'class %s(models.Model):' % table2model(table_name)
        try:
            relations = introspection_module.get_relations(cursor, table_name)
        except NotImplementedError:
            relations = {}
        try:
            indexes = introspection_module.get_indexes(cursor, table_name)
        except NotImplementedError:
            indexes = {}
        for i, row in enumerate(introspection_module.get_table_description(cursor, table_name)):
            att_name = row[0].lower()
            comment_notes = [] # Holds Field notes, to be displayed in a Python comment.
            extra_params = {}  # Holds Field parameters such as 'db_column'.

            if ' ' in att_name:
                extra_params['db_column'] = att_name
                att_name = att_name.replace(' ', '')
                comment_notes.append('Field renamed to remove spaces.')
            if keyword.iskeyword(att_name):
                extra_params['db_column'] = att_name
                att_name += '_field'
                comment_notes.append('Field renamed because it was a Python reserved word.')

            if i in relations:
                rel_to = relations[i][1] == table_name and "'self'" or table2model(relations[i][1])
                field_type = 'ForeignKey(%s' % rel_to
                if att_name.endswith('_id'):
                    att_name = att_name[:-3]
                else:
                    extra_params['db_column'] = att_name
            else:
                try:
                    field_type = introspection_module.DATA_TYPES_REVERSE[row[1]]
                except KeyError:
                    field_type = 'TextField'
                    comment_notes.append('This field type is a guess.')

                # This is a hook for DATA_TYPES_REVERSE to return a tuple of
                # (field_type, extra_params_dict).
                if type(field_type) is tuple:
                    field_type, new_params = field_type
                    extra_params.update(new_params)

                # Add maxlength for all CharFields.
                if field_type == 'CharField' and row[3]:
                    extra_params['max_length'] = row[3]

                if field_type == 'DecimalField':
                    extra_params['max_digits'] = row[4]
                    extra_params['decimal_places'] = row[5]

                # Add primary_key and unique, if necessary.
                column_name = extra_params.get('db_column', att_name)
                if column_name in indexes:
                    if indexes[column_name]['primary_key']:
                        extra_params['primary_key'] = True
                    elif indexes[column_name]['unique']:
                        extra_params['unique'] = True

                field_type += '('

            # Don't output 'id = meta.AutoField(primary_key=True)', because
            # that's assumed if it doesn't exist.
            if att_name == 'id' and field_type == 'AutoField(' and extra_params == {'primary_key': True}:
                continue
            
            if att_name == 'id' and field_type == 'IntegerField(' and extra_params == {'primary_key': True}:
                continue

            # Add 'null' and 'blank', if the 'null_ok' flag was present in the
            # table description.
            if row[6]: # If it's NULL...
                extra_params['blank'] = True
                if not field_type in ('TextField(', 'CharField('):
                    extra_params['null'] = True

            field_desc = '%s = models.%s' % (att_name, field_type)
            if extra_params:
                if not field_desc.endswith('('):
                    field_desc += ', '
                field_desc += ', '.join(['%s=%r' % (k, v) for k, v in extra_params.items()])
            field_desc += ')'
            if comment_notes:
                field_desc += ' # ' + ' '.join(comment_notes)
            yield '    %s' % field_desc

        pattern = re.compile( table_name + "_has_(.+)|(.+)_usedin_"+table_name ,re.IGNORECASE )        
        # filter gets all the table with many2many names
        tablesRelatedTo = filter(pattern.search, tablesList)

        if tablesRelatedTo:            
            # and map transforms that list to a list with matches
            matchesRelatedTo = map(pattern.findall, tablesRelatedTo)
            for table,i in zip(matchesRelatedTo, range(len(matchesRelatedTo))):
                comment = "Automatically generated!"
                yield '    %s = models.ManyToManyField(db_table = "%s") # %s' % (table[0][0].lower() or table[0][1].lower(), tablesRelatedTo[i], comment)

        yield '    class Meta:'
        yield '        db_table = %r' % table_name
        yield ''

#main method
def main(argv=sys.argv):
    if len(sys.argv) != 2:
        print "One parameter is missing: SQL filename not specified"
        print argv[0] + " SQLfilename"
        print
        return
    
    tableOrder = loadSqlOrder(argv[1])

    for line in inspectdb(tableOrder):
        print line

if __name__ == "__main__":
    main()
