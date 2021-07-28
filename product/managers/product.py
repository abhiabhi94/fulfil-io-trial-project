from itertools import repeat

from django.db import connections
from django.db import models
from django.db import transaction


class ProductManager(models.Manager):

    @staticmethod
    def _model_fields(model):
        return [f for f in model._meta.fields if not isinstance(f, models.AutoField)]

    @staticmethod
    def _prep_values(fields, obj, con):
        return tuple(f.get_db_prep_save(f.pre_save(obj, True), connection=con)
                     for f in fields)

    def bulk_upsert(self, objects, keys=None, skip_for_update=None, skip_entirely=None):
        if not objects:
            return
        skip_for_update = skip_for_update or []
        skip_entirely = skip_entirely or []

        keys = keys or [self.model._meta.pk.name]
        con = connections[self.db]

        table = self.model._meta.db_table

        all_fields = [f for f in self._model_fields(self.model) if f.name not in skip_entirely]

        # these are the fields that will be INSERTed on a failed UPDATE
        all_field_names = [f.name for f in all_fields]
        all_col_names = ",".join(con.ops.quote_name(f.column) for f in all_fields)

        # key fields are those used for WHERE in the UPDATE
        key_fields = [f for f in self.model._meta.fields if f.name in keys and f.name in all_field_names]
        key_col_names = ",".join(con.ops.quote_name(f.column) for f in key_fields)

        # Select key tuples from the database to find out which ones need to be
        # updated and which ones need to be inserted.
        assert key_fields, "Empty key fields"

        # update fields are those whose values are updated
        update_fields = [
            f for f in self.model._meta.fields
            if f.name not in keys and f.name not in skip_for_update and f.name in all_field_names
        ]
        update_col_names = ",".join(con.ops.quote_name(f.column) for f in update_fields)

        # repeat tuple values
        tuple_placeholder = "(%s)" % ",".join("%%s::%s" % f.db_type(con) for f in all_fields)
        placeholders = ",".join(repeat(tuple_placeholder, len(objects)))

        parameters = [self._prep_values(all_fields, o, con) for o in objects]
        parameters = [field for row in parameters for field in row]

        assignments = ",".join("%(f)s=nv.%(f)s" % {
            'f': con.ops.quote_name(f.column)
        } for f in update_fields)

        where_keys = " AND ".join("m.%(f)s=nv.%(f)s" % {
            'f': con.ops.quote_name(f.column)
        } for f in key_fields)

        up_where_keys = " AND ".join("up.%(f)s=new_values.%(f)s" % {
            'f': con.ops.quote_name(f.column)
        } for f in key_fields)

        sql_replacements = {
            'keys': keys,
            'table': table,
            'all_fields': all_fields,
            'all_col_names': all_col_names,
            'key_fields': key_fields,
            'key_col_names': key_col_names,
            'update_fields': update_fields,
            'update_col_names': update_col_names,
            'tuple_placeholder': tuple_placeholder,
            'placeholders': placeholders,
            'parameters': parameters,
            'assignments': assignments,
            'where_keys': where_keys,
            'up_where_keys': up_where_keys,
        }

        sql = """
            WITH new_values (%(all_col_names)s) AS (
              VALUES
                %(placeholders)s
            ),
            upsert AS
            (
                UPDATE %(table)s m
                    SET %(assignments)s
                FROM new_values nv
                WHERE %(where_keys)s
                RETURNING m.*
            )
            INSERT INTO %(table)s (%(all_col_names)s)
            SELECT %(all_col_names)s
            FROM new_values
            WHERE NOT EXISTS (SELECT 1
                              FROM %(table)s up
                              WHERE %(up_where_keys)s)
        """ % sql_replacements

        with transaction.atomic(using=self.db, savepoint=False):
            cursor = con.cursor()
            cursor.execute(sql, parameters)

    def delete_all(self):
        con = connections[self.db]
        sql = f'TRUNCATE {self.model._meta.db_table}'
        with transaction.atomic(using=self.db, savepoint=False):
            cursor = con.cursor()
            cursor.execute(sql)
