-- survey areas
--DROP TABLE IF EXISTS mhtc_operations."SurveyAreas";
CREATE TABLE mhtc_operations."SurveyAreas"
(
    id SERIAL,
    name character varying(32) COLLATE pg_catalog."default",
    geom geometry(MultiPolygon,27700),
    CONSTRAINT "SurveyAreas_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE mhtc_operations."SurveyAreas"
    OWNER to postgres;

ALTER TABLE "mhtc_operations"."RC_Sections_merged"
    ADD COLUMN "SurveyArea" integer;


--

UPDATE "mhtc_operations"."RC_Sections_merged" AS s
SET "SurveyArea" = a."Code"
FROM mhtc_operations."SurveyAreas" a
WHERE ST_WITHIN (s.geom, a.geom);

--
-- Calculate length of section within area

SELECT a."SurveyAreaName", SUM(s."SectionLength")
FROM mhtc_operations."RC_Sections_merged" s, mhtc_operations."SurveyAreas" a
WHERE ST_WITHIN (s.geom, a.geom)
GROUP BY a."SurveyAreaName"
ORDER BY a."SurveyAreaName";

-- OR

UPDATE "mhtc_operations"."Supply" AS s
SET "SurveyAreaID" = a."Code"
FROM mhtc_operations."SurveyAreas" a
WHERE ST_WITHIN (s.geom, a.geom);

SELECT a."SurveyAreaName", SUM(s."RestrictionLength"), SUM("Capacity")
FROM mhtc_operations."Supply" s, mhtc_operations."SurveyAreas" a
WHERE a."Code" = s."SurveyAreaID"
GROUP BY a."SurveyAreaName"
ORDER BY a."SurveyAreaName";