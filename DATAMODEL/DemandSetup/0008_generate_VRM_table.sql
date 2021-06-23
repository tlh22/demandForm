
DROP TABLE IF EXISTS demand."VRMs" CASCADE;
CREATE TABLE demand."VRMs"
(
  "ID" SERIAL,
  "SurveyID" integer,
  "SectionID" integer,
  "GeometryID" character varying(12),
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
