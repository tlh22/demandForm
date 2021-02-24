/***
Setup details for demand
***/

DROP TABLE IF EXISTS demand."RestrictionsInSurveys" CASCADE;

CREATE TABLE demand."RestrictionsInSurveys"
(
    "SurveyID" integer,
    "GeometryID" character varying(12) COLLATE pg_catalog."default",
    "DemandSurveyDateTime" timestamp without time zone,
    "Done" boolean,
    "SuspensionReference" character varying (100) COLLATE pg_catalog."default",
    "SuspensionReason" character varying (255) COLLATE pg_catalog."default",
    "SuspensionLength" double precision,
    "NrBaysSuspended" integer,
    "SuspensionNotes" character varying (255) COLLATE pg_catalog."default",
    "Photos_01" character varying (255) COLLATE pg_catalog."default",
    "Photos_02" character varying (255) COLLATE pg_catalog."default",
    "Photos_03" character varying (255) COLLATE pg_catalog."default",
	CONSTRAINT "RestrictionsInSurveys_pkey" PRIMARY KEY ("SurveyID", "GeometryID")
)

TABLESPACE pg_default;

ALTER TABLE demand."RestrictionsInSurveys"
    OWNER to postgres;

INSERT INTO demand."RestrictionsInSurveys" ("SurveyID", "GeometryID")
SELECT "SurveyID", gid::text AS "GeometryID"
FROM mhtc_operations."RC_Sections_merged", demand."Surveys";