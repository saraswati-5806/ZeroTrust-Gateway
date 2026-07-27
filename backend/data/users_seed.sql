CREATE TABLE users (

    id SERIAL PRIMARY KEY,

    username VARCHAR(50),

    role VARCHAR(30),

    home_country VARCHAR(50),

    allowed_start_hour INT,

    allowed_end_hour INT

);

INSERT INTO users
(username, role, home_country, allowed_start_hour, allowed_end_hour)

VALUES

('alice','Admin','India',8,20),

('bob','Developer','India',9,18),

('john','Manager','Singapore',8,22);



CREATE TABLE devices (

    device_id VARCHAR(50) PRIMARY KEY,

    username VARCHAR(50),

    healthy BOOLEAN,

    encrypted BOOLEAN,

    antivirus BOOLEAN

);

INSERT INTO devices VALUES

('DEV001','alice',TRUE,TRUE,TRUE),

('DEV002','bob',TRUE,TRUE,TRUE),

('DEV003','john',TRUE,FALSE,TRUE);