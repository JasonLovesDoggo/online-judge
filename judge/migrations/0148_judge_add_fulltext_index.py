# Generated by Django 3.2.25 on 2024-10-01 06:08

from django.db import migrations


def execute_mysql_command(apps, schema_editor, sql, error_msg):
    if schema_editor.connection.vendor != 'mysql':
        return

    Problem = apps.get_model('judge', 'Problem')
    formatted_sql = sql.format(Problem._meta.db_table)

    with schema_editor.connection.cursor() as cursor:
        try:
            cursor.execute(formatted_sql)
        except Exception as e:
            if error_msg in str(e):
                print(f'Info: {error_msg}')
            else:
                raise


def add_fulltext_index(apps, schema_editor):
    execute_mysql_command(
        apps,
        schema_editor,
        'ALTER TABLE {} ADD FULLTEXT(code, name, description)',
        'Duplicate key name',
    )


def remove_fulltext_index(apps, schema_editor):
    execute_mysql_command(
        apps,
        schema_editor,
        'ALTER TABLE {} DROP INDEX code',
        'check that column/key exists',
    )


class Migration(migrations.Migration):
    dependencies = [
        ('judge', '0147_judge_add_tiers'),
    ]

    operations = [
        migrations.RunPython(add_fulltext_index, remove_fulltext_index),
    ]
