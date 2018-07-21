CREATE TABLE IF NOT EXISTS researchSLR (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	date_Time DATETIME,
	repository VARCHAR(10)
);
CREATE TABLE IF NOT EXISTS searchSLR (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	idResearch INTEGER,
	date_Time DATETIME,
	searchString VARCHAR(255),
	searchIn VARCHAR(10),
	urlSearchAPI VARCHAR(255),
	nGrams INTEGER,
	amountFeatures INTEGER,
	amountResults INTEGER,
	amountPerPage INTEGER,
	amountNone INTEGER,
	amountInclude INTEGER,
	amountExclude INTEGER,
	tfIdfNone VARCHAR(255),
	tfIdfInclude VARCHAR(255),
	tfIdfExclude VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS documentInSearchSLR (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	idSearch INTEGER,
	idDocument INTEGER,
	title VARCHAR(255),
	abstract VARCHAR,
	rankDoc INTEGER,
	classification VARCHAR(1) NOT NULL,
	tfIDF VARCHAR(255),
	keywords VARCHAR(255)
);
