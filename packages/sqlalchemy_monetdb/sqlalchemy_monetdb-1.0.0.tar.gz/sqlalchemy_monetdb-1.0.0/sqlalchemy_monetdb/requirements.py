from sqlalchemy.testing.requirements import SuiteRequirements, exclusions


class Requirements(SuiteRequirements):
    @property
    def schemas(self):
        return exclusions.open()

    @property
    def sequences(self):
        return exclusions.open()

    @property
    def reflects_pk_names(self):
        return exclusions.open()

    @property
    def unicode_ddl(self):
        return exclusions.open()

    @property
    def datetime_microseconds(self):
        """monetdb doesn't support microsecond resolution"""
        return exclusions.closed()
    time_microseconds = datetime_microseconds

    @property
    def datetime_historic(self):
        return exclusions.open()

    @property
    def date_historic(self):
        return exclusions.open()

    @property
    def precision_numerics_enotation_small(self):
        return exclusions.open()

    @property
    def precision_numerics_enotation_large(self):
        """We don't support Numeric > 18"""
        return exclusions.closed()

    @property
    def view_reflection(self):
        return exclusions.open()

    @property
    def dbapi_lastrowid(self):
        return exclusions.open()

    @property
    def precision_numerics_retains_significant_digits(self):
        return exclusions.open()

    @property
    def sequences_optional(self):
        return exclusions.open()

    @property
    def independent_connections(self):
        return exclusions.open()

    @property
    def temp_table_names(self):
        """target dialect supports listing of temporary table names"""
        return exclusions.open()

    @property
    def temporary_tables(self):
        """target database supports temporary tables"""
        return exclusions.open()

    @property
    def temporary_views(self):
        """
        MonetDB doesn't have temporary views, but does support views of temporary tables.

        TODO: disabled for now, but maybe we can enable this?
        """
        return exclusions.closed()


    @property
    def foreign_key_constraint_option_reflection(self):
        """TODO: PostgreSQL, MonetDB and sqlite support this, so probably MoentDB also"""
        return exclusions.closed()

    @property
    def views(self):
        """Target database must support VIEWs."""

        return exclusions.open()

    @property
    def temp_table_reflection(self):
        return exclusions.open()

    @property
    def bound_limit_offset(self):
        """target database can render LIMIT and/or OFFSET using a bound
        parameter

        open by default, but closed since raises:

        sqlalchemy.exc.CompileError: This SELECT structure does not use a simple integer value for offset
        """
        return exclusions.closed()

    @property
    def parens_in_union_contained_select_w_limit_offset(self):
        """Target database must support parenthesized SELECT in UNION
        when LIMIT/OFFSET is specifically present.

        E.g. (SELECT ...) UNION (SELECT ..)

        This is known to fail on SQLite.

        This is also unsupported by MonetDB

        https://www.monetdb.org/bugzilla/show_bug.cgi?id=6434

        """
        return exclusions.closed()

    @property
    def parens_in_union_contained_select_wo_limit_offset(self):
        """Target database must support parenthesized SELECT in UNION
        when OFFSET/LIMIT is specifically not present.

        E.g. (SELECT ... LIMIT ..) UNION (SELECT .. OFFSET ..)

        This is known to fail on SQLite.  It also fails on Oracle
        because without LIMIT/OFFSET, there is currently no step that
        creates an additional subquery.

        This is also unsupported by MonetDB

        https://www.monetdb.org/bugzilla/show_bug.cgi?id=6434

        """
        return exclusions.closed()

    @property
    def order_by_col_from_union(self):
        """target database supports ordering by a column from a SELECT
        inside of a UNION
        E.g.  (SELECT id, ...) UNION (SELECT id, ...) ORDER BY id
        Fails on SQL Server

        This is also unsupported by MonetDB
        """
        return exclusions.closed()

    @property
    def broken_cx_oracle6_numerics(config):
        return exclusions.closed()

    @property
    def implicitly_named_constraints(self):
        """target database must apply names to unnamed constraints."""
        return exclusions.open()

    @property
    def unique_constraint_reflection(self):
        """target dialect supports reflection of unique constraints"""
        return exclusions.closed()