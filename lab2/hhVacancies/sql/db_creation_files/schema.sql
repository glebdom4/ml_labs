DROP TABLE IF EXISTS salary;
CREATE TABLE salary (
	id INTEGER PRIMARY KEY NOT NULL,
	from_ INT,
	to_ INT,
	currency VARCHAR,
	gross INT
);

DROP TABLE IF EXISTS area;
CREATE TABLE area (
	id INTEGER PRIMARY KEY NOT NULL,
	url VARCHAR,
	name VARCHAR NOT NULL
);

DROP TABLE IF EXISTS employer;
CREATE TABLE employer (
	id INTEGER PRIMARY KEY NOT NULL,
        reg_id INTEGER,
	name VARCHAR,
        url VARCHAR,
        alternate_url VARCHAR,
        trusted INT,
        blacklisted INT,
        CONSTRAINT name_unique UNIQUE (reg_id, name, url)
);

DROP TABLE IF EXISTS vacancy;
CREATE TABLE vacancy (
	id VARCHAR PRIMARY KEY NOT NULL,
 	description TEXT,
 	key_skills_id INT,
  	schedule_id INT,
  	accept_handicapped INT,
  	accept_kids INT,
  	experience_id INT,
        address_id INT,
        alternate_url VARCHAR,
        apply_alternate_url VARCHAR,
        code VARCHAR,
        department_id INT,
        employment_id INT,
        salary_id INT,
        archived INT,
        name VARCHAR,
        area_id INT,
        published_at VARCHAR,
        employer_id INT,
        response_letter_required INT,
        type_id INT,
        response_url TEXT,
        test_id INT,
        contacts_id INT,
        billing_type_id INT,
        allow_messages INT,
        premium INT,
        accept_incomplete_resumes INT,
	FOREIGN KEY (salary_id) REFERENCES salary(id)
	ON DELETE SET NULL,
	FOREIGN KEY (area_id) REFERENCES area(id)
	ON DELETE SET NULL
	FOREIGN KEY (employer_id) REFERENCES employer(id)
	ON DELETE SET NULL
);
