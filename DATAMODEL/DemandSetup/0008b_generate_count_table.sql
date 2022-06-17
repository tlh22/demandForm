
DROP TABLE IF EXISTS demand."Count" CASCADE;

CREATE TABLE "demand"."Counts" (
  "ID" SERIAL,
  "SurveyID" integer NOT NULL,
  "SectionID" integer,
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
  "Notes" character varying(250) COLLATE pg_catalog."default",

  "SuspensionReference" character varying(100) COLLATE pg_catalog."default",
  "NrBaysSuspended" integer,
  "ReasonForSuspension" character varying(100) COLLATE pg_catalog."default",
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


  CONSTRAINT "Count_pkey" PRIMARY KEY ("ID")
)
WITH (
  OIDS=FALSE
);

ALTER TABLE demand."Count"
  OWNER TO postgres;

CREATE UNIQUE INDEX "Count_unique_idx"
ON demand."Counts"("SurveyID", "GeometryID");

-- and populate

INSERT INTO "demand"."Count" ("SurveyID", "GeometryID")
SELECT "SurveyID", "GeometryID"
FROM mhtc_operations."Supply" r, demand."Surveys";



