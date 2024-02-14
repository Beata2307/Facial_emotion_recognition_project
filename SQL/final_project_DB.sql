
CREATE DATABASE IF NOT EXISTS final_project;
USE final_project;

-- =========================================================================================
-- Define relationships between tables using primary and foreign keys --
ALTER TABLE data_sources
ADD PRIMARY KEY (id);

ALTER TABLE emotions_ids
ADD PRIMARY KEY (id);

-- Define realtion between emotions_ids and action unit tables --
SHOW COLUMNS FROM facs_emotions_units LIKE 'emotion';
SHOW COLUMNS FROM facs_emotions_units LIKE 'action_units';
SHOW COLUMNS FROM emotions_ids LIKE 'id';

ALTER TABLE facs_emotions_units MODIFY emotion BIGINT;

ALTER TABLE facs_emotions_units
ADD FOREIGN KEY (emotion) REFERENCES emotions_ids(id);

ALTER TABLE facs_emotions_units
ADD FOREIGN KEY (action_units) REFERENCES facs_single_units(action_unit);

ALTER TABLE facs_single_units
ADD PRIMARY KEY (action_unit);

-- Images from PIXABAY --
ALTER TABLE images_pixabay
CHANGE COLUMN `index` `id` INT PRIMARY KEY;

ALTER TABLE images_pixabay
ADD FOREIGN KEY (source_id) REFERENCES data_sources(id);

ALTER TABLE images_pixabay
ADD FOREIGN KEY (emotion_id) REFERENCES emotions_ids(id);

-- Images from DuckDuckGo (ddg) --- 
ALTER TABLE images_ddg
CHANGE COLUMN `index` `id` INT PRIMARY KEY;

ALTER TABLE images_ddg
ADD FOREIGN KEY (source_id) REFERENCES data_sources(id);

ALTER TABLE images_ddg
ADD FOREIGN KEY (emotion_id) REFERENCES emotions_ids(id);

-- Images from Kaggle --
ALTER TABLE images_kaggle
CHANGE COLUMN `index` `id` INT PRIMARY KEY;

ALTER TABLE images_kaggle
ADD FOREIGN KEY (source_id) REFERENCES data_sources(id);

ALTER TABLE images_kaggle
ADD FOREIGN KEY (emotion_id) REFERENCES emotions_ids(id);

-- Images from FER2013 --
ALTER TABLE images_fer2013
CHANGE COLUMN `index` `id` INT PRIMARY KEY;

ALTER TABLE images_fer2013
ADD FOREIGN KEY (source_id) REFERENCES data_sources(id);

ALTER TABLE images_fer2013
ADD FOREIGN KEY (emotion_id) REFERENCES emotions_ids(id);

-- ================================================================================
-- QUERIES  
-- Create table with all images - but without reseting index for the moment 
DROP TABLE all_images;

CREATE TABLE all_images AS 
	SELECT * 
	FROM images_pixabay
		UNION ALL
	SELECT * 
	FROM images_ddg
		UNION ALL
	SELECT * 
	FROM images_kaggle
		UNION ALL
	SELECT * FROM images_fer2013;
    
select * from all_images; 

-- SELECT PICTURES FROM GIVEN SOURCE ----
SELECT 
	ds.source,
	ds.url_link,
	ei.emotion,
	height,
	width,
	aspect_ratio,
	image_format,
	color_space,
	file_size_MB,
	pixels
FROM images_pixabay pb
JOIN emotions_ids ei
	ON pb.emotion_id = ei.id
JOIN data_sources ds
	ON pb.source_id = ds.id;
    
-- SELECT PICTURES BASED ON EMOTION ----		
SELECT 
	ds.source,
	ds.url_link,
	ei.emotion,
	height,
	width,
	aspect_ratio,
	image_format,
	color_space,
	file_size_MB,
	pixels
FROM all_images ai
JOIN data_sources ds
	ON ai.source_id = ds.id
JOIN emotions_ids ei
	ON ai.emotion_id = ei.id
WHERE ei.emotion ='Anger';        

SELECT COUNT(*) as total_rows
FROM all_images ai
JOIN emotions_ids ei 
	ON ai.emotion_id = ei.id
WHERE ei.emotion = 'Anger';

-- ----------------------------------------------------------------------------

SELECT COUNT(*) AS total
FROM all_images
WHERE emotion_id = 0;

select * from all_images
where height = 48;

select * from all_images
where color_space = 'Grayscale'; 

-- use CTE to reset index in table with all images and then chose one image based on id
WITH numbered_images AS (
	SELECT
		ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS pic_nr,
		ei.emotion,
		ds.source,
		ds.url_link,
		height,
		width,
		aspect_ratio,
		image_format,
		color_space,
		file_size_MB,
		pixels
	FROM all_images ai
	JOIN data_sources ds ON ai.source_id = ds.id
	JOIN emotions_ids ei ON ai.emotion_id = ei.id
)
SELECT *
FROM numbered_images
WHERE pic_nr = 5;
 
-- use subquery to  select facial action units associated with particular emotion 
SELECT 
    id,
    ei.emotion,
    action_unit,
    fs.description,
    facial_muscle,
    example
FROM (SELECT * FROM emotions_ids WHERE emotion = 'Anger') as ei
JOIN facs_emotions_units feu
	ON ei.id = feu.emotion
JOIN facs_single_units fs
	ON feu.action_units = fs.action_unit;

-- count images with different width and height
SELECT 
    height,
    width,
    COUNT(*) AS image_count
FROM all_images
GROUP BY height, width
ORDER BY height ASC, width ASC;

SELECT 
ei.emotion,
COUNT(*) as images_per_emotion
FROM all_images ai
JOIN emotions_ids ei 
	ON ai.emotion_id = ei.id
GROUP BY ei.emotion
ORDER BY images_per_emotion DESC;

SELECT 
ei.emotion,
count(*) AS nr_of_facial_units
FROM facs_emotions_units feu
JOIN facs_single_units fs
	ON feu.action_units = fs.action_unit
JOIN emotions_ids ei
	ON ei.id = feu.emotion
GROUP BY ei.emotion
ORDER BY nr_of_facial_units DESC
LIMIT 1;
 
 SELECT
    id,
    ei.emotion,
    action_unit,
    fs.description,
    facial_muscle,
    example
FROM (SELECT * FROM emotions_ids WHERE emotion = 'Anger') as ei
JOIN facs_emotions_units feu
	ON ei.id = feu.emotion
JOIN facs_single_units fs
	ON feu.action_units = fs.action_unit;
    
SELECT 
suited_for_ML,
COUNT(*) as total_number
FROM 
(SELECT *,
    CASE
        WHEN aspect_ratio = 1 THEN 'should_be_fine'
        ELSE 'possible_distortions'
    END as suited_for_ML
FROM all_images) as ml
GROUP BY suited_for_ML;

-- CREATE TABLE WITH 

CREATE TABLE all_data AS
	SELECT
		ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS pic_nr,
        ei.id as emotion_id,
		ei.emotion,
        fs.action_unit,
        fs.description,
        fs.facial_muscle,
        fs.example,
		ds.source,
		ds.url_link,
		height,
		width,
		aspect_ratio,
		image_format,
		color_space,
		file_size_MB
	FROM all_images ai
	JOIN data_sources ds ON ai.source_id = ds.id
	JOIN emotions_ids ei ON ai.emotion_id = ei.id
    JOIN facs_emotions_units feu ON feu.emotion = ai.emotion_id
    JOIN facs_single_units fs ON feu.action_units = fs.action_unit ;
    
select * from all_data;

-- select count(*) from all_images;
--     
-- SELECT count(*) FROM images_pixabay;
-- SELECT count(*) FROM images_ddg;

-- SELECT count(*) FROM images_kaggle;
-- SELECT count(*) FROM images_fer2013;

-- DROP TABLE  images_pixabay;
-- DROP TABLE  images_ddg;
-- DROP TABLE  images_kaggle;
-- DROP TABLE  data_sources;

-- Concatenating and restarting the "id" column
-- CREATE TEMPORARY TABLE all_images (
-- 	SELECT
-- 	ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS pic_nr,
-- 	ei.emotion,
-- 	ds.source,
-- 	ds.url_link,
-- 	height,
-- 	width,
-- 	aspect_ratio,
-- 	image_format,
-- 	color_space,
-- 	file_size_MB,
-- 	pixels
-- 	FROM (
-- 		SELECT * FROM images_pixabay pb
-- 		UNION ALL
-- 		SELECT * FROM images_ddg ddg
-- 		UNION ALL
-- 		SELECT * FROM images_kaggle k
-- 		UNION ALL
-- 		SELECT * FROM images_fer2013 f
-- 	) AS ai
-- 	JOIN data_sources ds
-- 		ON ai.source_id = ds.id
-- 	JOIN emotions_ids ei
-- 		ON ai.emotion_id = ei.id
-- 	ORDER BY pic_nr DESC;
-- -- );


SELECT COUNT(*) AS total_rows
FROM all_images;
