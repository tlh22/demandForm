/***
Setup details for demand
***/

INSERT INTO demand."RestrictionsInSurveys" ("SurveyID", "GeometryID", geom)
SELECT "SurveyID", gid::text AS "GeometryID", r.geom As geom
FROM mhtc_operations."RC_Sections_merged" r, demand."Surveys";

-- OR

INSERT INTO demand."RestrictionsInSurveys" ("SurveyID", "GeometryID", geom)
SELECT "SurveyID", "GeometryID", r.geom As geom
FROM mhtc_operations."Supply" r, demand."Surveys";

---
/***

--- Haringey ...

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

***/
