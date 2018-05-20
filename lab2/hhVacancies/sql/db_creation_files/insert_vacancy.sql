INSERT OR IGNORE INTO area (id, url, name) VALUES (?, ?, ?);
INSERT INTO salary (from_, to_, currency, gross) VALUES (?, ?, ?, ?);
SELECT * FROM salary ORDER BY id DESC LIMIT 1;
INSERT OR IGNORE INTO employer (reg_id, name, url, alternate_url, trusted, blacklisted) VALUES (?, ?, ?, ?, ?, ?);
SELECT * FROM salary ORDER BY id DESC LIMIT 1;
INSERT INTO vacancy (id, name, description, published_at, area_id, salary_id, employer_id) VALUES (?, ?, ?, ?, ?, ?, ?);

