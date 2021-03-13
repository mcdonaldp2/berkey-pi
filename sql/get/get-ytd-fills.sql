select COUNT(*) from BerkeyFillLog 
where datetime(FillTime) >= datetime('now', 'start of year') 
    and datetime(FillTime) < datetime('now', 'start of year', '+12 month');