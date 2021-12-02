-- Step 0: Tidy fields
UPDATE demand."Demand_Merged"
SET ncars = NULL
WHERE ncars = '';

UPDATE demand."Demand_Merged"
SET nlgvs = NULL
WHERE nlgvs = '';

UPDATE demand."Demand_Merged"
SET nmcls = NULL
WHERE nmcls = '';

UPDATE demand."Demand_Merged"
SET nogvs = NULL
WHERE nogvs = '';

UPDATE demand."Demand_Merged"
SET nogvs2 = NULL
WHERE nogvs2 = '';

UPDATE demand."Demand_Merged"
SET nbuses = NULL
WHERE nbuses = '';

UPDATE demand."Demand_Merged"
SET nminib = NULL
WHERE nminib = '';

UPDATE demand."Demand_Merged"
SET ntaxis = NULL
WHERE ntaxis = '';

UPDATE demand."Demand_Merged"
SET nspaces = NULL
WHERE nspaces = '';

UPDATE demand."Demand_Merged"
SET sbays = NULL
WHERE sbays = '';

-- Check
SELECT "SurveyID",
    SUM(COALESCE("ncars"::float, 0.0) +
	COALESCE("nlgvs"::float, 0.0) +
    COALESCE("nmcls"::float, 0.0)*0.33 +
    (COALESCE("nogvs"::float, 0) + COALESCE("nogvs2"::float, 0) + COALESCE("nminib"::float, 0) + COALESCE("nbuses"::float, 0))*1.5 +
    COALESCE("ntaxis"::float, 0))
FROM demand."Demand_Merged"
GROUP BY "SurveyID"
ORDER BY "SurveyID";

-- Step 1: Add new fields

ALTER TABLE demand."Demand_Merged"
    ADD COLUMN "Demand" double precision;
ALTER TABLE demand."Demand_Merged"
    ADD COLUMN "Stress" double precision;

-- Step 2: calculate demand values using trigger

-- set up trigger for demand and stress

CREATE OR REPLACE FUNCTION "demand"."update_demand"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    AS $$
DECLARE
	 vehicleLength real := 0.0;
	 vehicleWidth real := 0.0;
	 motorcycleWidth real := 0.0;
	 restrictionLength real := 0.0;
BEGIN

    IF vehicleLength IS NULL OR vehicleWidth IS NULL OR motorcycleWidth IS NULL THEN
        RAISE EXCEPTION 'Capacity parameters not available ...';
        RETURN OLD;
    END IF;

    NEW."Demand" = COALESCE(NEW."ncars"::float, 0.0) + COALESCE(NEW."nlgvs"::float, 0.0)
                    + COALESCE(NEW."nmcls"::float, 0.0)*0.33
                    + (COALESCE(NEW."nogvs"::float, 0) + COALESCE(NEW."nogvs2"::float, 0) + COALESCE(NEW."nminib"::float, 0) + COALESCE(NEW."nbuses"::float, 0))*1.5
                    + COALESCE(NEW."ntaxis"::float, 0);

    /* What to do about suspensions */

    CASE
        WHEN NEW."Capacity" = 0 THEN
            CASE
                WHEN NEW."Demand" > 0.0 THEN NEW."Stress" = 100.0;
                ELSE NEW."Stress" = 0.0;
            END CASE;
        ELSE
            CASE
                WHEN NEW."Capacity"::float - COALESCE(NEW."sbays"::float, 0.0) > 0.0 THEN
                    NEW."Stress" = NEW."Demand" / (NEW."Capacity"::float - COALESCE(NEW."sbays"::float, 0.0)) * 100.0;
                ELSE
                    CASE
                        WHEN NEW."Demand" > 0.0 THEN NEW."Stress" = 100.0;
                        ELSE NEW."Stress" = 0.0;
                    END CASE;
            END CASE;
    END CASE;

	RETURN NEW;

END;
$$;

-- create trigger

CREATE TRIGGER "update_demand" BEFORE INSERT OR UPDATE ON "demand"."Demand_Merged" FOR EACH ROW EXECUTE FUNCTION "demand"."update_demand"();

-- trigger trigger

UPDATE "demand"."Demand_Merged" SET "RestrictionLength" = "RestrictionLength";

-- Step 3: output demand

SELECT
d."SurveyID", s."SurveyDay" As "Survey Day", s."BeatStartTime" || '-' || s."BeatEndTime" As "Survey Time", d."GeometryID",
       (COALESCE("ncars"::float, 0)+COALESCE("ntaxis"::float, 0)) As "Nr Cars", COALESCE("nlgvs"::float, 0) As "Nr LGVs",
       COALESCE("nmcls"::float, 0) AS "Nr MCLs", COALESCE("nogvs"::float, 0) AS "Nr OGVs", COALESCE("nbuses"::float, 0) AS "Nr Buses",
       COALESCE("nspaces"::float, 0) AS "Nr Spaces",
       COALESCE(d."sbays"::integer, 0) AS "Bays Suspended", d."snotes" AS "Suspension Notes", "Demand" As "Demand",
             d."nnotes" AS "Surveyor Notes",
        su."RestrictionTypeID", su."Capacity"

FROM --"SYL_AllowableTimePeriods" syls,
      demand."Demand_Merged" d, demand."Surveys" s, mhtc_operations."Supply" su  -- include Supply to ensure that only current supply elements are included
WHERE s."SurveyID" = d."SurveyID"
AND d."GeometryID" = su."GeometryID"
ORDER BY  "GeometryID", d."SurveyID"

