import requests
from bs4 import BeautifulSoup
import pandas as pd
data = []

def get_cell_value(data, class_name ):
    cell = data.find(class_=class_name)
    return cell.get_text(strip=True) if cell else None
    


for i in range(1, 24):
    url = f"https://www.scrapethissite.com/pages/forms/?page_num={i}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    text = r.text
    soup = BeautifulSoup(text, "html.parser")


    table = soup.find('table')
    all_rows = table.find_all('tr', class_="team")


    for row in all_rows:
        row_data = {
            "name": get_cell_value(row, "name"),
            "year":get_cell_value(row, "year"),
            "wins": get_cell_value(row, "wins"),
            "losses": get_cell_value(row, "losses"),
            "ot_losses": get_cell_value(row, "ot-losses"),
            "win_pct": get_cell_value(row, "pct"),
            "gf": get_cell_value(row, "gf"),
            "ga": get_cell_value(row, "ga"),
            "diff": get_cell_value(row, "diff")
        }
        data.append(row_data)

df = pd.DataFrame(data)
df = df.replace("", pd.NA)
df["year"] = df["year"].astype("Int64")
df["wins"] = df["wins"].astype("Int64")
df["losses"] = df["losses"].astype("Int64")
df["ot_losses"] = df["ot_losses"].astype("Int64")
df["win_pct"] = df["win_pct"].astype("float")
df["gf"] = df["gf"].astype("Int64")
df["ga"] = df["ga"].astype("Int64")
df["diff"] = df["diff"].astype("Int64")
df.info()
print(df.isnull().sum())
print(df.duplicated().sum())
df.to_csv("data/processed/nhl_data.csv", index=False)