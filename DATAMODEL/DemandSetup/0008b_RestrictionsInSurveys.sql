/***
Setup details for demand
***/

DROP TABLE IF EXISTS demand."RestrictionsInSurveys" CASCADE;

CREATE TABLE demand."RestrictionsInSurveys"
(
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
    geom geometry(LineString,27700) NOT NULL,
	CONSTRAINT "RestrictionsInSurveys_pkey" PRIMARY KEY ("SurveyID", "GeometryID")
)

TABLESPACE pg_default;

ALTER TABLE demand."RestrictionsInSurveys"
    OWNER to postgres;

CREATE UNIQUE INDEX "RiS_unique_idx"
ON demand."RestrictionsInSurveys"("SurveyID", "GeometryID");

INSERT INTO demand."RestrictionsInSurveys" ("SurveyID", "GeometryID", geom)
SELECT "SurveyID", gid::text AS "GeometryID", r.geom As geom
FROM mhtc_operations."RC_Sections_merged" r, demand."Surveys";

-- OR

INSERT INTO demand."RestrictionsInSurveys" ("SurveyID", "GeometryID", geom)
SELECT "SurveyID", "GeometryID", r.geom As geom
FROM mhtc_operations."Supply" r, demand."Surveys";

--- For Haringey

DROP TABLE IF EXISTS demand."RestrictionsInSurveys_ALL" CASCADE;

CREATE TABLE demand."RestrictionsInSurveys_ALL"
(
    "SurveyID" integer,
    "GeometryID" character varying(12) COLLATE pg_catalog."default",
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
    geom geometry(LineString,27700) NOT NULL,
	CONSTRAINT "RestrictionsInSurveys_ALL_pkey" PRIMARY KEY ("SurveyID", "GeometryID")
)

TABLESPACE pg_default;

ALTER TABLE demand."RestrictionsInSurveys_ALL"
    OWNER to postgres;

INSERT INTO demand."RestrictionsInSurveys_ALL"(
	   "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
	   "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
	   "Photos_01", "Photos_02", "Photos_03", geom)

SELECT "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
       "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
       "Photos_01", "Photos_02", "Photos_03", geom
	FROM demand."RestrictionsInSurveys_FP"

UNION

SELECT "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
       "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
       "Photos_01", "Photos_02", "Photos_03", geom
	FROM demand."RestrictionsInSurveys_FPB"

UNION

SELECT "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
       "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
       "Photos_01", "Photos_02", "Photos_03", geom
	FROM demand."RestrictionsInSurveys_FPC"

UNION

SELECT "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
       "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
       "Photos_01", "Photos_02", "Photos_03", geom
	FROM demand."RestrictionsInSurveys_HS"

UNION

SELECT "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
       "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
       "Photos_01", "Photos_02", "Photos_03", geom
	FROM demand."RestrictionsInSurveys_TN"

UNION

SELECT "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
       "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
       "Photos_01", "Photos_02", "Photos_03", geom
	FROM demand."RestrictionsInSurveys_THNED"

UNION

SELECT "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
       "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
       "Photos_01", "Photos_02", "Photos_03", geom
	FROM demand."RestrictionsInSurveys_7S"

UNION

SELECT "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
       "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
       "Photos_01", "Photos_02", "Photos_03", geom
	FROM demand."RestrictionsInSurveys_7SistersSouth"

UNION

SELECT "SurveyID", "GeometryID", "DemandSurveyDateTime", "Enumerator", "Done",
       "SuspensionReference", "SuspensionReason", "SuspensionLength", "NrBaysSuspended", "SuspensionNotes",
       "Photos_01", "Photos_02", "Photos_03", geom
	FROM demand."RestrictionsInSurveys_WHL"