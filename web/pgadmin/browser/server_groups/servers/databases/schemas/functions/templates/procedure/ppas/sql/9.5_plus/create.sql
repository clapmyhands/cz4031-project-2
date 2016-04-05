{% import 'macros/functions/security.macros' as SECLABEL %}
{% import 'macros/functions/privilege.macros' as PRIVILEGE %}
{% import 'macros/functions/variable.macros' as VARIABLE %}
{% set is_columns = [] %}
{% if data %}
CREATE OR REPLACE PROCEDURE {{ conn|qtIdent(data.pronamespace, data.name) }}{% if data.arguments %}
({% for p in data.arguments %}{% if p.argmode %}{{p.argmode}} {% endif %}{% if p.argname %}{{ conn|qtIdent(p.argname)}} {% endif %}{% if p.argtype %}{{p.argtype}}{% endif %}{% if p.argdefval %} DEFAULT {{p.argdefval}}{% endif %}
{% if not loop.last %}, {% endif %}
{% endfor -%}){% endif %}

    {{ data.provolatile }}{% if data.proleakproof %} LEAKPROOF {% elif not data.proleakproof %} NOT LEAKPROOF {% endif %}
{% if data.proisstrict %}STRICT {% endif %}
{% if data.prosecdef %}SECURITY DEFINER {% endif %}{% if data.procost %}

    COST {{data.procost}}{% endif %}{% if data.prorows %}

    ROWS {{data.prorows}}{% endif -%}{% if data.variables %}{% for v in data.variables %}

    SET {{ conn|qtIdent(v.name) }}={{ v.value|qtLiteral }}{% endfor -%}
{% endif %}

AS
{{ data.prosrc }};
{% if data.acl and not is_sql %}
{% for p in data.acl %}

{{ PRIVILEGE.SET(conn, "PROCEDURE", p.grantee, data.name, p.without_grant, p.with_grant, data.pronamespace, data.func_args)}}
{% endfor %}{% endif %}
{% if data.description %}

COMMENT ON PROCEDURE {{ conn|qtIdent(data.pronamespace, data.name) }}
    IS '{{ data.description }}';
{% endif -%}
{% if data.seclabels %}
{% for r in data.seclabels %}
{% if r.security_label and r.provider %}

{{ SECLABEL.SET(conn, 'PROCEDURE', data.name, r.provider, r.security_label, data.pronamespace, data.func_args) }}
{% endif %}
{% endfor %}
{% endif -%}

{% endif %}
