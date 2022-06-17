
DROP TABLE IF EXISTS demand."VRMs" CASCADE;
CREATE TABLE demand."VRMs"
(
  "ID" SERIAL,
  "SurveyID" integer NOT NULL,
  "SectionID" integer,
  "GeometryID" character varying(12) NOT NULL,
  "PositionID" integer,
  "VRM" character varying(12),
  "VehicleTypeID" integer,
  "RestrictionTypeID" integer,
  "PermitTypeID" integer,
  "Notes" character varying(255),
  CONSTRAINT "VRMs_pkey" PRIMARY KEY ("ID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE demand."VRMs"
  OWNER TO postgres;

CREATE UNIQUE INDEX "VRMs_unique_idx"
ON demand."VRMs"("SurveyID", "GeometryID");