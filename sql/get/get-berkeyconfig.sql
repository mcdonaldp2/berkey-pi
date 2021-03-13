select 
    FilterConfigId,
    b.ModelId, 
    ModelName,
    NumberOfFilterElements, 
    CreatedOn 
    from BerkeyConfig b
    inner join BerkeyModel bm on bm.ModelId = b.ModelId
    where FilterConfigId = (select max(FilterConfigId) from BerkeyConfig);