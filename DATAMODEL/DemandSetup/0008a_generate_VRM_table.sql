
DROP TABLE IF EXISTS demand."VRMs" CASCADE;
CREATE TABLE demand."VRMs"
(
  "ID" SERIAL,
  "SurveyID" integer NOT NULL,
  "SectionID" integer,
  "GeometryID" character varying(12) NOT NULL,
  "PositionID" integer,
  "VRM" character varying(12),
  "InternationalCodeID" integer,
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


/***
ALTER TABLE demand."VRMs" ALTER "Foreign" TYPE INTEGER USING CASE WHEN false THEN 0 ELSE 1 END;
ALTER TABLE demand."VRMs" RENAME COLUMN "Foreign" TO "InternationalCodeID";
***/