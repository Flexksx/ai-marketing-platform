
-- 1. Add the column as TEXT (or VARCHAR to match your brands table)
ALTER TABLE posts ADD COLUMN brand_id text;

-- 2. Update the column 
-- We remove the ::uuid cast since both sides are now strings
UPDATE posts p 
SET brand_id = c.brand_id
FROM campaigns c 
WHERE p.campaign_id = c.id;

-- 3. Add the foreign key constraint
-- This will only work if brands.id is the primary key or has a unique constraint
ALTER TABLE posts 
ADD CONSTRAINT posts_brand_id_fkey 
FOREIGN KEY (brand_id) REFERENCES brands(id);
