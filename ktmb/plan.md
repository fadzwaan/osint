1. use Instant Data Scraper and have this 



```excel

point-parent	point-parent href	point	point 2	point 3

Perlis	https://www.ktmb.com.my/StationInfo.html#collapse1	Padang Besar Station	Bukit Keteri Station	Arau Station

Kedah	https://www.ktmb.com.my/StationInfo.html#collapse2	Kodiang Station	Anak Bukit Station	Alor Setar Station

Penang	https://www.ktmb.com.my/StationInfo.html#collapse3	Tasek Gelugor Station	Butterworth Station	Bukit Mertajam Station

Perak	https://www.ktmb.com.my/StationInfo.html#collapse4	Parit Buntar Station	Bagan Serai Station	Kamunting Station

```



and clean with this 



```python
import pandas as pd

# Load CSV
df = pd.read_csv("ktmb.csv")

# Rename column
df = df.rename(columns={"point-parent": "state"})

# Identify station columns (point, point 2, point 3, ...)
point_cols = [col for col in df.columns if col.startswith("point") and col != "point-parent"]

# Combine all points into one column
df["point"] = (
    df[point_cols]
    .apply(lambda row: ", ".join(row.dropna().astype(str)), axis=1)
)

# Count total points per state
df["total_point"] = df[point_cols].notna().sum(axis=1)

# Keep only required columns
final_df = df[["state", "total_point", "point"]]

print(final_df)

final_df.to_excel("ktmb_cleaned.xlsx", index=False)


```



2\. download https://www.ktmb.com.my/assets/pdf/2023/Jadual-Komuter-Utara-16-Sept-2023.pdf use https://www.ilovepdf.com/pdf\_to\_excel

