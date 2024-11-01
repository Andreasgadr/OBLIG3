import pandas as pd
import numpy as np
import altair as alt

# Les inn Excel-fil
kgdata = pd.read_excel("ssb-barnehager-2015-2023-alder-1-2-aar.xlsm", sheet_name="KOSandel120000",
                       header=3,
                       names=['kom','y15','y16','y17','y18','y19','y20','y21','y22','y23'],
                       na_values=['.', '..'])

# Renser dataen ved å maskere ubetydelige verdier
for coln in ['y15','y16','y17','y18','y19','y20','y21','y22','y23']:
    mask_over_100 = (kgdata[coln] > 100)
    kgdata.loc[mask_over_100, coln] = float("nan")

# Fjerner data i kolonne 724 - 779 én gang (utenfor løkken)
kgdata.loc[724:779, 'kom'] = "NaN"

# Manipulerer innholdet i `kom`-kolonnen én gang (utenfor løkken)
kgdata["kom"] = kgdata['kom'].str.split(" ").apply(lambda x: x[1] if len(x) > 1 else "")

# Sletter metadata-rader én gang (utenfor løkken)
kgdata_no_meta = kgdata.drop(kgdata.index[724:])

# Funksjon for å skrive DataFrame til Excel
def write_pandas_dataframe_to_excel_worksheet_with_nan(pandas_df, file_name, wsh_name):
    with pd.ExcelWriter(file_name, mode='a') as writer:
        pandas_df.to_excel(writer, sheet_name=wsh_name, na_rep='nan')

print(kgdata_no_meta)

# Funksjon for å finne høyeste verdier
def get_top_percentage(df, column, n=1, ascending=False):
    sorted_df = df.sort_values(by=column, ascending=ascending)
    top_n = sorted_df.head(n)
    return top_n[['kom', column]]

# A. Høyeste prosentandel i 2023
highest_2023 = get_top_percentage(kgdata_no_meta, 'y23')
print("\nA. Høyeste prosentandel i 2023:")
for index, row in highest_2023.iterrows():
    print(f"{row['kom']}: {row['y23']:.1f}%")


# B. Laveste prosentandel i 2023
lowest_2023 = get_top_percentage(kgdata_no_meta, 'y23', ascending=True)
print("\nB. Laveste prosentandel i 2023:")
for index, row in lowest_2023.iterrows():
    print(f"{row['kom']}: {row['y23']:.1f}%")


# Definer årskolonner og beregn avrundet gjennomsnitt for 2015-2023
year_columns = [f'y{year}' for year in range(15, 24)]
kgdata_no_meta['mean_2015_2023_rounded'] = kgdata_no_meta[year_columns].mean(axis=1).round(1)

# Hent høyeste eller laveste verdier basert på gjennomsnitt
def get_top_values(df, column, n=3, top=True):
    top_value = df[column].max() if top else df[column].min()
    return df[df[column] == top_value][['kom', column]].head(n)

# Funksjon for å skrive ut kommuner med høyeste eller laveste gjennomsnittlig prosent
def print_top_values(df, column, top=True, n=3):
    label = "C. Høyeste" if top else "D. Laveste"
    top_values = get_top_values(df, column, top=top, n=n)
    print(f"\n{label} gjennomsnittlige prosent (2015-2023):")
    for _, row in top_values.iterrows():
        print(f"{row['kom']}: {row[column]:.1f}%")

# C. Høyeste gjennomsnittlige prosent (2015-2023)
print_top_values(kgdata_no_meta, 'mean_2015_2023_rounded', top=True)

# D. Laveste gjennomsnittlige prosent (2015-2023)
print_top_values(kgdata_no_meta, 'mean_2015_2023_rounded', top=False)


def plot_single_kommune(df, kommune):
    # Filtrer data for valgt kommune
    kommune_data = df[df['kom'] == kommune][year_columns].melt(
        var_name='Year', value_name='Percentage'
    )
    
    # Bytt årskolonnenavnene til faktiske årstall for lettere lesing
    kommune_data['Year'] = kommune_data['Year'].str.replace('y', '20').astype(int)
    
    # Plotter diagrammet
    chart = alt.Chart(kommune_data).mark_line(point=True).encode(
        x=alt.X('Year:O', title='År'),
        y=alt.Y('Percentage', title='Prosent', scale=alt.Scale(domain=[0, 100])),
        tooltip=['Year', 'Percentage']
    ).properties(
        title=f'Prosent av barn (1-2 år) i barnehage for {kommune} (2015-2023)',
        width=600,
        height=400
    )
    
    return chart

# Eksempel på bruk: plot_single_kommune(kgdata_no_meta, "Oslo")



import pandas as pd
import altair as alt

# G. Funksjon for å lage diagram for valgt kommune
def create_childcare_percentage_chart(dataframe, municipality_name):
    # Årskolonner og filtrer data for valgt kommune
    years = [f'y{year}' for year in range(15, 24)]
    filtered_data = dataframe[dataframe['kom'] == municipality_name].melt(
        id_vars='kom',
        value_vars=years,
        var_name='year_column',
        value_name='percentage_value'
    )
    
    # Konverter årstall til lesbart format
    filtered_data['year_column'] = filtered_data['year_column'].str.replace('y', '20').astype(int)
    
    # Lag diagrammet
    childcare_chart = alt.Chart(filtered_data).mark_line(point=True).encode(
        x=alt.X('year_column:O', title='År'),
        y=alt.Y('percentage_value:Q', title='Prosent', scale=alt.Scale(zero=False)),
        tooltip=['year_column', 'percentage_value']
    ).properties(
        title=f'Prosent av barn 1-2 år i barnehage i {municipality_name} (2015-2023)',
        width=1000,
        height=600
    )
    
    return childcare_chart

# Velg kommune og lagre diagram
chosen_municipality = "Oslo"  # Endre til ønsket kommune
childcare_chart = create_childcare_percentage_chart(kgdata_no_meta, chosen_municipality)

# Lagre diagrammet som en HTML-fil
childcare_chart.save(f'{chosen_municipality}_barnehage_prosent_2015_2023.html')
print(f"G. Diagram for {chosen_municipality} er lagret som en HTML-fil.")

