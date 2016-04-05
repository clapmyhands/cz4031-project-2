SELECT
    pr.oid, pr.proname || '(' || COALESCE(pg_catalog.pg_get_function_identity_arguments(pr.oid), '') || ')' as name,
    lanname, pg_get_userbyid(proowner) as funcowner, description
FROM
    pg_proc pr
JOIN
    pg_type typ ON typ.oid=prorettype
JOIN
    pg_language lng ON lng.oid=prolang
LEFT OUTER JOIN
    pg_description des ON (des.objoid=pr.oid AND des.classoid='pg_proc'::regclass)
WHERE
    proisagg = FALSE
    AND pronamespace = {{scid}}::oid
    AND typname NOT IN ('trigger', 'event_trigger')
ORDER BY
    proname;
