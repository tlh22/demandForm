-- bayline type demand details


-- vehicle types

INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (1, 'Car', 1.0);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (2, 'LGV', 1.0);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (3, 'MCL', 0.4);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (4, 'OGV', 1.5);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (5, 'Bus', 2.0);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (6, 'PCL', 0.2);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (7, 'Taxi', 1.0);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (8, 'Other', 1.0);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (9, NULL, 1.0);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (10, 'Obstruction', 0.0);
INSERT INTO "demand_lookups"."VehicleTypes" ("Code", "Description", "PCU") VALUES (11, 'Minbus', 1.0);

-- permit types

INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (0, NULL);
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (1, 'Resident (Zone)');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (2, 'Resident (Other)');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (3, 'Visitor voucher');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (4, 'Disabled (Blue badge)');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (5, 'Essential Service Permit (ESP)');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (6, 'Business permit');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (7, 'Companion');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (8, 'Carer''s permit');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (9, 'No visible permit');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (10, 'Boroughwide and Utility Permit');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (11, 'Car Club permit');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (12, 'Doctor''s Permit');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (13, 'Monthly Resident');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (14, 'Visitor Voucher concessionary');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (15, 'Trader''s permit');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (16, 'Other (inc. Coronavirus Permit)');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (17, 'No permit required (MCL)');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (18, 'No permit required (Non Resident MCL)');
INSERT INTO "demand_lookups"."PermitTypes" ("Code", "Description") VALUES (19, 'Homes for Haringey');

-- User types

INSERT INTO "demand_lookups"."UserTypes" ("Code", "Description") VALUES (1, 'Resident');
INSERT INTO "demand_lookups"."UserTypes" ("Code", "Description") VALUES (2, 'Commuter');
INSERT INTO "demand_lookups"."UserTypes" ("Code", "Description") VALUES (3, 'Visitor');