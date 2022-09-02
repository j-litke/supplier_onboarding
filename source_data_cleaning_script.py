# Import libraries.
import pandas as pd

# Import json file to a Pandas DataFrame.
df = pd.read_json('supplier_car.json', lines=True)

# Unstack the DataFrame to match granularity of target data.
df_unstacked = df.pivot(index=["ID", "MakeText", "TypeName", "TypeNameFull", "ModelText",
                               "ModelTypeText"],
                        columns=["Attribute Names"],
                        values=["Attribute Values", "entity_id"])
df_unstacked = df_unstacked.reset_index().set_index(["ID"])

# Create dictionaries for German/English translations
colour_dict = {
"anthrazit":"anthracite",
"anthrazit mét.":"anthracite met.",
"beige mét.":"beige met.",
"blau":"blue",
"blau mét.":"blue met.",
"bordeaux":"burgundy",
"bordeaux mét.":"burgundy met.",
"braun":"brown",
"braun mét.":"brown met.",
"gelb":"yellow",
"gelb mét.":"yellow met.",
"gold mét.":"gold met.",
"grau":"grey",
"grau mét.":"gray met.",
"grün":"green",
"grün mét.":"green met.",
"orange mét.":"orange met.",
"rot":"red",
"rot mét.":"red met.",
"schwarz":"black",
"schwarz mét.":"black met.",
"silber":"silver",
"silber mét.":"silver met.",
"violett mét.":"purple met.",
"weiss":"white",
"weiss mét.":"white met."}
condition_dict = {
"Oldtimer":"Old Timer",
"Neu":"New",
"Vorführmodell":"Demonstration Model"
}
cartype_dict = {
"Limousine": "Other",
"Kombi": "Station Wagon",
"SUV / Geländewagen": "SUV",
"Cabriolet": "Convertible / Roadster",
"Wohnkabine": "Other",
"Kleinwagen": "Single seater",
"Kompaktvan / Minivan": "Other",
"Sattelschlepper": "Other",
"Pick-up": "Other"
}

# Create dictionary for Brand Name normalisation
brand_dict = {"FORD (USA)": "Ford"}


# Make the translations/replacements
df_normalized = df_unstacked.copy(deep=True)
df_normalized.loc[:, ("Attribute Values", "BodyColorText")].replace(colour_dict, inplace=True)
df_normalized.loc[:, ("Attribute Values", "ConditionTypeText")].replace(condition_dict, inplace=True)
df_normalized.loc[:, ("Attribute Values", "BodyTypeText")].replace(cartype_dict, inplace=True)
df_normalized.loc[:, ("MakeText", "")].replace(brand_dict, inplace=True)

# Create an empty DataFrame to fill with the normalized data
target_cols = [
"carType",
"color",
"condition",
"currency",
"drive",
"city",
"country",
"make",
"manufacture_year",
"mileage",
"mileage_unit",
"model",
"model_variant",
"price_on_request",
"type",
"zip",
"manufacture_month",
"fuel_consumption_unit"
]
df_integration = pd.DataFrame(columns=target_cols)

# Fill empty DataFrame with corresponding columns from source data
df_integration["carType"] = df_normalized.loc[:, ("Attribute Values", "BodyTypeText")]
df_integration["color"] = df_normalized.loc[:, ("Attribute Values", "BodyColorText")]
df_integration["condition"] = df_normalized.loc[:, ("Attribute Values", "ConditionTypeText")]
df_integration["city"] = df_normalized.loc[:, ("Attribute Values", "City")]
df_integration["make"] = df_normalized.loc[:, ("MakeText", "")]
df_integration["mileage"] = df_normalized.loc[:, ("Attribute Values", "Km")]
df_integration["mileage_unit"] = "kilometer"
df_integration["model"] = df_normalized.loc[:, ("ModelText", "")]
df_integration["model_variant"] = df_normalized.loc[:, ("TypeName", "")]


# Export to Excel
with pd.ExcelWriter('integrated_supplier_data.xlsx') as writer:
    df_unstacked.to_excel(writer, sheet_name='step_1')
    df_normalized.to_excel(writer, sheet_name='step_2')
    df_integration.to_excel(writer, sheet_name='step_3', index=False)