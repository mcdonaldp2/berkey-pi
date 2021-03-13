CREATE TABLE IF NOT EXISTS "BerkeyConfig" (
    FilterConfigId integer primary key, 
    ModelId integer, 
    NumberOfFilterElements integer, 
    CreatedOn text DEFAULT (DATE()));

