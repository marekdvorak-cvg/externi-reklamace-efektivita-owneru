# Dotazy pro data.json

Každý dotaz se spouští přes Salesforce (SOQL). Výsledné `records` (bez pole `attributes`) se uloží do `build/data.json` pod klíčem uvedeným v nadpisu. Názvy sloupců (aliasy) musí zůstat stejné.

## opened_daily

```sql
SELECT Owner.Name owner, DAY_ONLY(CreatedDate) day, COUNT(Id) cnt FROM Complaint__c WHERE Type__c = 'external' AND Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND CreatedDate >= 2026-09-01T00:00:00+02:00 GROUP BY Owner.Name, DAY_ONLY(CreatedDate) ORDER BY DAY_ONLY(CreatedDate)
```

## closed_daily

```sql
SELECT Owner.Name owner, DAY_ONLY(Closed_Date__c) day, COUNT(Id) cnt FROM Complaint__c WHERE Type__c = 'external' AND Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND Closed_Date__c >= 2026-09-01T00:00:00+02:00 AND (Done_Date__c >= 2026-09-01T00:00:00+02:00 OR Done_Date__c = null) GROUP BY Owner.Name, DAY_ONLY(Closed_Date__c) ORDER BY DAY_ONLY(Closed_Date__c)
```

## closed_stats

```sql
SELECT Owner.Name owner, COUNT(Id) cnt, AVG(Open_Days_Real__c) avgDays, MAX(Open_Days_Real__c) maxDays, SUM(Cost_EUR__c) cost FROM Complaint__c WHERE Type__c = 'external' AND Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND Closed_Date__c >= 2026-09-01T00:00:00+02:00 AND (Done_Date__c >= 2026-09-01T00:00:00+02:00 OR Done_Date__c = null) GROUP BY Owner.Name
```

## closed_30

```sql
SELECT Owner.Name owner, COUNT(Id) cnt FROM Complaint__c WHERE Type__c = 'external' AND Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND Closed_Date__c >= 2026-09-01T00:00:00+02:00 AND (Done_Date__c >= 2026-09-01T00:00:00+02:00 OR Done_Date__c = null) AND Open_Days_Effective__c <= 30 GROUP BY Owner.Name
```

## backlog

```sql
SELECT Owner.Name owner, COUNT(Id) cnt FROM Complaint__c WHERE Type__c = 'external' AND Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND Status__c NOT IN ('done','closed') GROUP BY Owner.Name
```

## backlog_30

```sql
SELECT Owner.Name owner, COUNT(Id) cnt FROM Complaint__c WHERE Type__c = 'external' AND Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND Status__c NOT IN ('done','closed') AND Open_Days_Effective__c > 30 GROUP BY Owner.Name
```

## done_open

```sql
SELECT Owner.Name owner, COUNT(Id) cnt FROM Complaint__c WHERE Type__c = 'external' AND Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND Status__c = 'done' AND Done_Date__c >= 2026-09-01T00:00:00+02:00 AND Closed_Date__c = null GROUP BY Owner.Name
```

## resolution

```sql
SELECT Complaint__r.Owner.Name owner, Status__c status, COUNT(Id) cnt FROM Complaint_Problem__c WHERE Complaint__r.Type__c = 'external' AND Complaint__r.Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND Complaint__r.Closed_Date__c >= 2026-09-01T00:00:00+02:00 AND (Complaint__r.Done_Date__c >= 2026-09-01T00:00:00+02:00 OR Complaint__r.Done_Date__c = null) AND Status__c != 'new' GROUP BY Complaint__r.Owner.Name, Status__c
```

## cost_source

```sql
SELECT Owner.Name owner, Problem_Source__c source, COUNT(Id) cnt, SUM(Cost_EUR__c) cost, SUM(Seller_Participation_Amount_EUR__c) seller FROM Complaint__c WHERE Type__c = 'external' AND Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND Closed_Date__c >= 2026-09-01T00:00:00+02:00 AND (Done_Date__c >= 2026-09-01T00:00:00+02:00 OR Done_Date__c = null) GROUP BY Owner.Name, Problem_Source__c
```

## extension

```sql
SELECT Owner.Name owner, Due_Date_Extension__c ext, COUNT(Id) cnt FROM Complaint__c WHERE Type__c = 'external' AND Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') AND Closed_Date__c >= 2026-09-01T00:00:00+02:00 AND (Done_Date__c >= 2026-09-01T00:00:00+02:00 OR Done_Date__c = null) GROUP BY Owner.Name, Due_Date_Extension__c
```

## cpc_types

```sql
SELECT Complaint__r.Owner.Name owner, Problem_Category__r.Type__c type, COUNT(Id) cnt FROM Complaint_Problem__c WHERE Complaint__r.Type__c = 'external' AND Complaint__r.CreatedDate >= 2026-09-01T00:00:00+02:00 AND Complaint__r.Owner.Name IN ('Pavel Tran Son','Marco Antonio Sinica','Kryštof Veber') GROUP BY Complaint__r.Owner.Name, Problem_Category__r.Type__c
```
