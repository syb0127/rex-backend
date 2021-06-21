CREATE TABLE UserInfo (
    Username VARCHAR(20) NOT NULL,
    UserID VARCHAR(20) NOT NULL,
    Salted_Password VARCHAR(30),
    Email VARCHAR(50) NOT NULL
)
GO

SELECT * FROM UserInfo
GO

INSERT INTO UserInfo
VALUES
    ('username', 'userid', 'salted password', 'email@gmail.com')
GO

SELECT * FROM UserInfo
GO