-- Roles
INSERT IGNORE INTO Role (Role_ID, Role_Name) VALUES
(1, 'Regular'),
(2, 'Color Guard'),
(3, 'Percussion'),
(4, 'Drum Major');

-- Instrument Types (sequential IDs, no gap)
INSERT IGNORE INTO Instrument_Types (Instr_Type_ID, Instr_Type_Name) VALUES
(1,  'Trumpet'),
(2,  'French Horn'),
(3,  'Snare Drum'),
(4,  'Oboe'),
(5,  'Clarinet'),
(6,  'Trombone'),
(7,  'Tuba'),
(8,  'Flute'),
(9,  'Piccolo'),
(10, 'Violin'),
(11, 'Viola'),
(12, 'Cello'),
(13, 'Double Bass'),
(14, 'Alto Saxophone'),
(15, 'Tenor Saxophone'),
(16, 'Baritone Saxophone');

-- Guardians
INSERT INTO Guardian (Guardian_FName, Guardian_LName, Guardian_Phone) VALUES
('Dean', 'Chamra',  '555-0101'),
('Jane',   'Dietrich',  '555-0102'),
('Kelli',    'Foskic',  '555-0103'),
('Laura',    'Kroger',   '555-0104'),
('Christopher',  'Kobus',     '555-0105');

-- Students
INSERT INTO Student (Stud_FName, Stud_LName, Stud_Phone, Year_ID, Stud_Gender, Stud_Email) VALUES
('Kaeden',    'Bryer',  '1234567890', 1, 'Male', 'kaedenbryer@oakland.edu'),
('Pablo',     'Avila',  '1234567890', 2, 'Male',   'avila@oakland.edu'),
('Nate',   'Oberdier',  '1234567890', 3, 'Male', 'noberdier@oakland.edu'),
('Nicholas',  'Sakowski',   '1234567890', 4, 'Male',   'nsakowski@oakland.edu'),
('Julia',      'Schoen',     '1234567890', 1, 'Female', 'jtschoen@oakland.edu'),
('Grant',  'Kerry',    '1234567890', 2, 'Male',   'gkerry@oakland.edu'),
('Charlie',   'Hayes',     '1234567890', 3, 'Female', 'hayes@oakland.edu'),
('Alec',    'Barnes',     '1234567890', 4, 'Male',   'barnsey@oakland.edu'),
('Avery', 'Schepke',  '1234567890', 1, 'Female', 'aschepke@oakland.edu'),
('Sen',   'Jutsu',    '1234567890', 2, 'Male',   'sen@oakland.edu');

-- Student-Guardian relationships
INSERT INTO Student_Guardian (Stud_ID, Guardian_ID) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5,  5),
(6, 1), (7, 3), (8, 2), (9, 4), (10, 5);

-- Instruments (20 total: 8 Trumpet, 2 French Horn, 1 Snare Drum, 2 Clarinet,
--              1 Trombone, 1 Tuba, 2 Flute, 1 Violin, 2 Alto Saxophone)
INSERT INTO Instrument (Instrument_Type) VALUES
(1), (1), (1), (1), (1), (1), (1), (1),
(2), (2),
(3),
(5), (5),
(6),
(7),
(8), (8),
(10),
(14), (14);

-- Uniforms (30 total)
-- Regular (20): 3 XS, 5 S, 6 M, 4 L, 2 XL
-- Color Guard (3): 1 S, 1 M, 1 L
-- Percussion (5): 1 S, 1 M, 2 L, 1 XL
-- Drum Major (2): 1 L, 1 XL
-- Columns: Role_ID, Chest, Arms, Hips, Waist, Inseam, Gloves

-- Regular XS (IDs 1-3)
INSERT INTO Uniform (Role_ID, Uniform_Chest, Uniform_Arms, Uniform_Hips, Uniform_Waist, Uniform_Inseam, Uniform_Gloves) VALUES
(1, 31.50, 28.00, 32.50, 24.50, 27.50, 'XS'),
(1, 32.00, 28.50, 33.00, 25.00, 28.00, 'XS'),
(1, 32.50, 29.00, 33.50, 25.50, 28.50, 'XS'),

-- Regular S (IDs 4-8)
(1, 35.00, 30.00, 35.00, 27.00, 29.00, 'S'),
(1, 35.50, 30.00, 35.50, 27.50, 29.50, 'S'),
(1, 36.00, 30.50, 36.00, 28.00, 30.00, 'S'),
(1, 36.50, 31.00, 36.50, 28.50, 30.50, 'S'),
(1, 37.00, 31.50, 37.00, 29.00, 30.00, 'S'),

-- Regular M (IDs 9-14)
(1, 38.50, 32.00, 39.00, 30.00, 30.00, 'M'),
(1, 39.50, 32.00, 39.50, 30.50, 30.50, 'M'),
(1, 40.00, 32.50, 40.00, 31.00, 31.00, 'M'),
(1, 40.50, 33.00, 40.50, 31.50, 31.50, 'M'),
(1, 41.00, 33.50, 41.00, 32.00, 31.00, 'M'),
(1, 41.50, 33.50, 41.50, 32.50, 32.00, 'M'),

-- Regular L (IDs 15-18)
(1, 43.50, 34.00, 42.50, 33.50, 31.50, 'L'),
(1, 44.00, 34.50, 43.00, 34.00, 32.00, 'L'),
(1, 44.50, 35.00, 43.50, 34.50, 32.50, 'L'),
(1, 45.00, 35.50, 44.00, 35.00, 32.00, 'L'),

-- Regular XL (IDs 19-20)
(1, 47.50, 36.00, 46.50, 37.50, 32.50, 'XL'),
(1, 48.00, 36.50, 47.00, 38.00, 33.00, 'XL'),

-- Color Guard S (ID 21), M (ID 22), L (ID 23)
(2, 36.00, 30.50, 36.00, 28.00, 30.00, 'S'),
(2, 40.00, 32.50, 40.00, 31.00, 31.00, 'M'),
(2, 44.00, 34.50, 43.00, 34.00, 32.00, 'L'),

-- Percussion S (ID 24), M (ID 25), L (IDs 26-27), XL (ID 28)
(3, 36.50, 31.00, 36.50, 28.50, 30.50, 'S'),
(3, 40.50, 33.00, 40.50, 31.50, 31.50, 'M'),
(3, 44.50, 35.00, 43.50, 34.50, 32.50, 'L'),
(3, 45.50, 35.50, 44.50, 35.00, 32.00, 'L'),
(3, 48.50, 37.00, 47.50, 38.50, 33.50, 'XL'),

-- Drum Major L (ID 29), XL (ID 30)
(4, 44.00, 35.00, 43.50, 34.00, 32.50, 'L'),
(4, 48.00, 37.00, 47.00, 38.00, 33.00, 'XL');

-- Student Uniform Rentals (4 active — no end date or end condition)
INSERT INTO Student_Uniform_Rentals (Stud_ID, Uniform_ID, Unif_Rental_Start_Date, Unif_Rental_End_Date, Unif_Start_Condition, Unif_End_Condition) VALUES
(1,  4, '2025-08-15', NULL, 'Good',      NULL),
(3, 11, '2025-08-22', NULL, 'Excellent', NULL),
(5, 17, '2025-09-03', NULL, 'Good',      NULL),
(7, 22, '2025-09-08', NULL, 'Good',      NULL);

-- Student Instrument Rentals (4 active — no end date or end condition)
INSERT INTO Student_Instrument_Rentals (Stud_ID, Instrument_ID, Instr_Rental_Start_Date, Instr_Rental_End_Date, Instr_Start_Condition, Instr_End_Condition) VALUES
(2,  1, '2025-08-15', NULL, 'Good',      NULL),
(4,  9, '2025-08-22', NULL, 'Excellent', NULL),
(6, 12, '2025-09-03', NULL, 'Good',      NULL),
(8, 16, '2025-09-08', NULL, 'Good',      NULL);
