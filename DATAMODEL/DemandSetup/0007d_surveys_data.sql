-- surveys

--INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (1, 'Monday', '0030', '0300');
--INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (2, 'Tuesday', '0030', '0300');


INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (1, 'Wednesday', '0500', '0700');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (2, 'Wednesday', '0700', '0800');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (3, 'Wednesday', '0900', '1000');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (4, 'Wednesday', '1100', '1200');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (5, 'Wednesday', '1300', '1400');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (6, 'Wednesday', '1500', '1600');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (7, 'Wednesday', '1700', '1800');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (8, 'Wednesday', '1900', '2000');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (9, 'Wednesday', '2100', '2200');

INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (10, 'Saturday', '0500', '0600');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (11, 'Saturday', '0700', '0800');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (12, 'Saturday', '0900', '1000');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (13, 'Saturday', '1100', '1200');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (14, 'Saturday', '1300', '1400');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (15, 'Saturday', '1500', '1600');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (16, 'Saturday', '1700', '1800');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (17, 'Saturday', '1900', '2000');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (18, 'Saturday', '2100', '2200');

INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (19, 'Sunday', '0500', '0600');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (20, 'Sunday', '0700', '0800');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (21, 'Sunday', '0900', '1000');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (22, 'Sunday', '1100', '1200');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (23, 'Sunday', '1300', '1400');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (24, 'Sunday', '1500', '1600');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (25, 'Sunday', '1700', '1800');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (26, 'Sunday', '1900', '2000');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (27, 'Sunday', '2100', '2200');

UPDATE demand."Surveys"
SET "BeatTitle" = LPAD("SurveyID"::text, 3, '0') || '_' || "SurveyDay" || '_' || "BeatStartTime" || '_' || "BeatEndTime";


INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (31, 'Wednesday', '0500', '0600');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (32, 'Wednesday', '0700', '0800');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (33, 'Wednesday', '0900', '1000');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (34, 'Wednesday', '1100', '1200');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (35, 'Wednesday', '1400', '1500');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (36, 'Wednesday', '1600', '1700');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (37, 'Wednesday', '1800', '1900');

INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (38, 'Saturday', '0500', '0600');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (39, 'Saturday', '0700', '0800');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (40, 'Saturday', '0900', '1000');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (41, 'Saturday', '1100', '1200');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (42, 'Saturday', '1400', '1500');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (43, 'Saturday', '1600', '1700');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (44, 'Saturday', '1800', '1900');

INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (45, 'Sunday', '0500', '0600');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (46, 'Sunday', '0700', '0800');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (47, 'Sunday', '0900', '1000');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (48, 'Sunday', '1100', '1200');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (49, 'Sunday', '1400', '1500');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (50, 'Sunday', '1600', '1700');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (51, 'Sunday', '1800', '1900');

UPDATE demand."Surveys"
SET "BeatTitle" = LPAD("SurveyID"::text, 3, '0') || '_' || "SurveyDay" || '_' || "BeatStartTime" || '_' || "BeatEndTime";

INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (61, 'Sunday (TN)', '0830', '0930');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (62, 'Sunday (TN)', '0930', '1030');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (63, 'Sunday (TN)', '1030', '1130');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (64, 'Sunday (TN)', '1130', '1230');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (65, 'Sunday (TN)', '1230', '1330');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (66, 'Sunday (TN)', '1330', '1430');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (67, 'Sunday (TN)', '1430', '1530');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (68, 'Sunday (TN)', '1530', '1630');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (69, 'Sunday (TN)', '1630', '1730');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (70, 'Sunday (TN)', '1730', '1830');


INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (1, 'Thursday (TN)', '0830', '0930');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (2, 'Thursday (TN)', '0930', '1030');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (3, 'Thursday (TN)', '1030', '1130');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (4, 'Thursday (TN)', '1130', '1230');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (5, 'Thursday (TN)', '1230', '1330');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (6, 'Thursday (TN)', '1330', '1430');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (7, 'Thursday (TN)', '1430', '1530');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (8, 'Thursday (TN)', '1530', '1630');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (9, 'Thursday (TN)', '1630', '1730');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (10, 'Thursday (TN)', '1730', '1830');

INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (11, 'Sunday (TN)', '0830', '0930');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (12, 'Sunday (TN)', '0930', '1030');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (13, 'Sunday (TN)', '1030', '1130');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (14, 'Sunday (TN)', '1130', '1230');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (15, 'Sunday (TN)', '1230', '1330');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (16, 'Sunday (TN)', '1330', '1430');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (17, 'Sunday (TN)', '1430', '1530');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (18, 'Sunday (TN)', '1530', '1630');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (19, 'Sunday (TN)', '1630', '1730');
INSERT INTO demand."Surveys"("SurveyID", "SurveyDay", "BeatStartTime", "BeatEndTime") VALUES (20, 'Sunday (TN)', '1730', '1830');

UPDATE demand."Surveys"
SET "BeatTitle" = LPAD("SurveyID"::text, 3, '0') || '_' || "SurveyDay" || '_' || "BeatStartTime" || '_' || "BeatEndTime"
WHERE "BeatTitle" IS NULL;