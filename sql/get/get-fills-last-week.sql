select 
    FillId, 
    FillTime, 
    FillDayOfWeek 
from BerkeyFillLog 
where datetime(fillTime) >= datetime(date('now'), 'weekday 6', '-6 days', '-7 days') 
and datetime(FillTime) <= datetime(date('now'), 'weekday 6', '-6 days') 
order by datetime(FillTime) ASC;