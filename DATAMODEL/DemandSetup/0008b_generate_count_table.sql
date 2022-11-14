
DROP TABLE IF EXISTS demand."Counts" CASCADE;

CREATE TABLE "demand"."Counts" (
  gid INT GENERATED ALWAYS AS IDENTITY,
  "SurveyID" integer NOT NULL,
  "GeometryID" character varying(12) NOT NULL,

  "NrCars" integer,
  "NrLGVs" integer,
  "NrMCLs" integer,
  "NrTaxis" integer,
  "NrPCLs" integer,
  "NrEScooters" integer,
  "NrDocklessPCLs" integer,
  "NrOGVs" integer,
  "NrMiniBuses" integer,
  "NrBuses" integer,
  "NrSpaces" integer,
  "Notes" character varying(10000) COLLATE pg_catalog."default",

  "DoubleParkingDetails" character varying COLLATE pg_catalog."default",

  "NrCars_Suspended" integer,
  "NrLGVs_Suspended" integer,
  "NrMCLs_Suspended" integer,
  "NrTaxis_Suspended" integer,
  "NrPCLs_Suspended" integer,
  "NrEScooters_Suspended" integer,
  "NrDocklessPCLs_Suspended" integer,
  "NrOGVs_Suspended" integer,
  "NrMiniBuses_Suspended" integer,
  "NrBuses_Suspended" integer,

   UNIQUE ("SurveyID", "GeometryID")
)
WITH (
  OIDS=FALSE
);

ALTER TABLE demand."Counts"
  OWNER TO postgres;

-- and populate

INSERT INTO "demand"."Counts" ("SurveyID", "GeometryID")
SELECT "SurveyID", "GeometryID"
FROM mhtc_operations."Supply" r, demand."Surveys";


/***
UPDATE "demand"."Counts"
SET

ALTER TABLE "demand"."Counts" DROP CONSTRAINT "Counts_pkey";
ALTER TABLE "demand"."Counts" ADD PRIMARY KEY ("SurveyID", "GeometryID");
ALTER TABLE IF EXISTS demand."Counts" DROP COLUMN IF EXISTS "ID";
ALTER TABLE IF EXISTS demand."Counts" DROP COLUMN IF EXISTS "SectionID";

***/


/***
 For RBKC

ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrCarsWaiting" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrCarsIdling" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrCarsParkedIncorrectly" integer;

ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrLGVsWaiting" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrLGVsIdling" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrLGVsParkedIncorrectly" integer;

ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrMCLsWaiting" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrMCLsIdling" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrMCLsParkedIncorrectly" integer;

ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrTaxisWaiting" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrTaxisIdling" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrTaxisParkedIncorrectly" integer;

ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrOGVsWaiting" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrOGVsIdling" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrOGVsParkedIncorrectly" integer;

ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrMiniBusesWaiting" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrMiniBusesIdling" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrMiniBusesParkedIncorrectly" integer;	

ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrBusesWaiting" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrBusesIdling" integer;
ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrBusesParkedIncorrectly" integer;

ALTER TABLE IF EXISTS demand."Counts"
    ADD COLUMN "NrCarsWithDisabledBadgeParkedInPandD" integer;

 ***/
