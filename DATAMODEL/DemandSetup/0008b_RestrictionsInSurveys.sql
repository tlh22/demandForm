/***
Setup details for demand
***/

DROP TABLE IF EXISTS demand."RestrictionsInSurveys" CASCADE;

CREATE TABLE demand."RestrictionsInSurveys"
(
    gid INT GENERATED ALWAYS AS IDENTITY,
    "SurveyID" integer NOT NULL,
    "GeometryID" character varying(12) COLLATE pg_catalog."default" NOT NULL,
    "DemandSurveyDateTime" timestamp without time zone,
    "Enumerator" character varying (100) COLLATE pg_catalog."default",
    "Done" boolean,
    "SuspensionReference" character varying (100) COLLATE pg_catalog."default",
    "SuspensionReason" character varying (255) COLLATE pg_catalog."default",
    "SuspensionLength" double precision,
    "NrBaysSuspended" integer,
    "SuspensionNotes" character varying (255) COLLATE pg_catalog."default",
    "Photos_01" character varying (255) COLLATE pg_catalog."default",
    "Photos_02" character varying (255) COLLATE pg_catalog."default",
    "Photos_03" character varying (255) COLLATE pg_catalog."default",
    "CaptureSource" character varying (255) COLLATE pg_catalog."default",
    geom geometry(LineString,27700) NOT NULL,
    UNIQUE ("SurveyID", "GeometryID")
)

TABLESPACE pg_default;

ALTER TABLE demand."RestrictionsInSurveys"
    OWNER to postgres;

/***

ALTER TABLE IF EXISTS demand."RestrictionsInSurveys"
    ADD COLUMN "CaptureSource" character varying(255);

INSERT INTO demand."RestrictionsInSurveys" ("SurveyID", "GeometryID", geom)
SELECT "SurveyID", gid::text AS "GeometryID", r.geom As geom
FROM mhtc_operations."RC_Sections_merged" r, demand."Surveys";
***/

-- OR

INSERT INTO demand."RestrictionsInSurveys" ("SurveyID", "GeometryID", geom)
SELECT "SurveyID", "GeometryID", r.geom As geom
FROM mhtc_operations."Supply" r, demand."Surveys";

/***
UPDATE demand."RestrictionsInSurveys"
SET "Done" = false
WHERE "Done" IS true;

INSERT INTO demand."RestrictionsInSurveys" ("SurveyID", "GeometryID", geom)
SELECT "SurveyID", "GeometryID", r.geom As geom
FROM mhtc_operations."Supply" r, demand."Surveys"
WHERE "GeometryID" NOT IN
(SELECT "GeometryID"
FROM demand."RestrictionsInSurveys")


**/