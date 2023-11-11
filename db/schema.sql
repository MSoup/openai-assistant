CREATE TABLE IF NOT EXISTS "users" (
    "first_name" TEXT,
    "last_name" TEXT,
    "username" TEXT,
    "profile_picture" TEXT
);

CREATE TABLE IF NOT EXISTS "usage" (
    "tokens_used" INTEGER,
    "username" TEXT,
    FOREIGN KEY("username") REFERENCES "users"("username")
);


