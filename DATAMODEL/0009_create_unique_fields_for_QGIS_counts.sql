/***
 * Create unique GeometryID/SurveyID field so that join can be made in QGIS
 ***/

ALTER TABLE demand."RestrictionsInSurveys"
    ADD COLUMN "GeometryID_SurveyID" character varying(100) COLLATE pg_catalog."default";

ALTER TABLE demand."Counts"
    ADD COLUMN "GeometryID_SurveyID" character varying(100) COLLATE pg_catalog."default";

-- Populate

UPDATE demand."RestrictionsInSurveys"
SET "GeometryID_SurveyID" = CONCAT("GeometryID", '_', "SurveyID"::text);

UPDATE demand."Counts" c
SET "GeometryID_SurveyID" = RiS."GeometryID_SurveyID"
FROM demand."RestrictionsInSurveys" RiS
WHERE c."SurveyID" = RiS."SurveyID"
AND c."GeometryID" = RiS."GeometryID"
;

-- Set up indexes

CREATE UNIQUE INDEX geometryid_surveyid_ris_idx ON demand."RestrictionsInSurveys" ("GeometryID_SurveyID");

CREATE UNIQUE INDEX geometryid_surveyid_counts_idx ON demand."Counts" ("GeometryID_SurveyID");