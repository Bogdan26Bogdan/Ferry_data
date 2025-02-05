DROP TABLE IF EXISTS "Main Table";
DROP TABLE IF EXISTS "Route Data";

CREATE TABLE IF NOT EXISTS "Main Table" (
	"Route Code"	TEXT NOT NULL,
	"Ferry Run Date"	TEXT NOT NULL,
	"From Terminal"	TEXT,
	"To Terminal"	TEXT,
	"Actual Arrival Time"	TEXT,
	"Scheduled Departure Time"	TEXT NOT NULL,
	"Actual Departure Time"	TEXT,
	"Current Sailing Status"	TEXT,
	"Vessel Name"	TEXT,
	"Sailing Duration" TEXT, 
	"Other Data"	TEXT,
	PRIMARY KEY("Route Code","Ferry Run Date", "Scheduled Departure Time")
);

CREATE TABLE IF NOT EXISTS "Route Data" (
	"Route Code"	TEXT NOT NULL,
	"Ferry Run Date"	TEXT NOT NULL,
	"Scheduled Departure Time" TEXT NOT NULL,
	"Sample Time"	TEXT NOT NULL,
	"Departure Time"	TEXT,
	"Arrival Time"	TEXT,
	"Sailing Status"	TEXT,
	"Total Fill"	INTEGER,
	"All Size Fill"	INTEGER,
	"7ft Under Fill"	INTEGER,
	PRIMARY KEY("Route Code","Ferry Run Date","Scheduled Departure Time","Sample Time")
);


-- Trigger for updating the state in the main table.
CREATE TRIGGER IF NOT EXISTS main_table_updates
	AFTER INSERT
	ON "Route Data"
BEGIN
	-- Sailing Status
	UPDATE "Main Table" 
	SET "Current Sailing Status" = NEW."Sailing Status" 
	WHERE 
		"Route Code"=NEW."Route Code" 
		AND 
		"Ferry Run Date"=NEW."Ferry Run Date"
		AND
		"Scheduled Departure Time" = NEW."Scheduled Departure Time"
		AND 
		NEW."Sample Time" = ( 
			SELECT max("Sample Time") FROM "Route Data" 
			WHERE 
				"Route Code"=NEW."Route Code" 
				AND 
				"Ferry Run Date"=NEW."Ferry Run Date"
				AND 
				NEW."Sailing Status" IS NOT NULL
				AND
				NEW."Sailing Status" != ""
		); 

		
	-- Actual Arrival and Departure Time: Newest time with past as status
	UPDATE "Main Table" 
	SET 
		"Actual Departure Time" = NEW."Departure Time", 
		"Actual Arrival Time" = NEW."Arrival Time"
	WHERE 
		"Route Code"=NEW."Route Code" 
		AND 
		"Ferry Run Date"=NEW."Ferry Run Date"
		AND 
		"Scheduled Departure Time" = NEW."Scheduled Departure Time"
		AND 
		NEW."Sample Time" = ( 
			SELECT max("Sample Time") FROM "Route Data" 
			WHERE 
				"Route Code"=NEW."Route Code" 
				AND 
				"Ferry Run Date"=NEW."Ferry Run Date"
				AND 
				NEW."Departure Time" IS NOT NULL 
				AND 
				NEW."Departure Time" != ""
				AND 
				NEW."Arrival Time" IS NOT NULL 
				AND 
				NEW."Arrival Time" != ""
				AND 
				NEW."Sailing Status" = "past"
		);
END;