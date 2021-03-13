select 
    FillId, 
    FillTime, 
    FillDayOfWeek 
from BerkeyFillLog 
where datetime(FillTime) >= datetime(date('now'), 'weekday 6', '-6 days')
    and datetime(FillTime) <= datetime(date('now'), 'weekday 6') 
order by datetime(FillTime) ASC;