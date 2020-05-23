import requests
import zipfile
import io
import pandas as pd


WIFI_IN_CULTURAL_MOSCOW_PLACES_URLS = [
    ['libraries', 'https://op.mos.ru/EHDWSREST/catalog/export/get?id=781683'],
    ['cinemas', 'https://op.mos.ru/EHDWSREST/catalog/export/get?id=781635'],
    ['cultural centers', 'https://op.mos.ru/EHDWSREST/catalog/export/get?id=781643'],
    ['parks', 'https://op.mos.ru/EHDWSREST/catalog/export/get?id=781691'],
    ]


def get_streets_and_amount_of_wifi_points(url: str):
    result = requests.get(url)
    wifi_points_zip = zipfile.ZipFile(io.BytesIO(result.content))
    wifi_points_zip.extractall()
    wifi_points_csv_path = wifi_points_zip.namelist()[0]
    df = pd.read_csv(wifi_points_csv_path, delimiter=';', encoding='CP1251')
    streets_and_amount_of_wifi_points = {}

    for index in df.index:
        if df.loc[index, 'FunctionFlag'] == 'действует' and (
            df.loc[index, 'AccessFlag'] == 'открытая сеть'
        ):
            if ('Address' in df.columns) and ('улица' in df.loc[index, 'Address']):
                street_name = df.loc[index, 'Address'].split(', ')[1]
            elif 'ParkName' in df.columns:
                street_name = df.loc[index, 'ParkName']
            else:
                continue

            if street_name not in streets_and_amount_of_wifi_points:
                streets_and_amount_of_wifi_points[street_name] = 0
            streets_and_amount_of_wifi_points[street_name] += 1

    return streets_and_amount_of_wifi_points


def get_top_five_streets_to_surf_the_internet(places_and_wifi_amounts: dict):
    return sorted(list(places_and_wifi_amounts.items()), key=lambda x: x[1])[-5:]


if __name__ == '__main__':
    for place, url in WIFI_IN_CULTURAL_MOSCOW_PLACES_URLS:
        wifi_points_of_cultural_places = get_streets_and_amount_of_wifi_points(url=url)

        if place == 'parks':
            top_five_parks_to_surf_the_internet = get_top_five_streets_to_surf_the_internet(wifi_points_of_cultural_places)
        else:
            joined_wifi_points_amount_all_over_the_capital = {}
            for street, wifi_amount in wifi_points_of_cultural_places.items():
                if street in joined_wifi_points_amount_all_over_the_capital:
                    joined_wifi_points_amount_all_over_the_capital[street] += wifi_amount
                else:
                    joined_wifi_points_amount_all_over_the_capital[street] = wifi_amount
            top_five_streets_to_surf_the_internet = get_top_five_streets_to_surf_the_internet(joined_wifi_points_amount_all_over_the_capital)

    print(f'top 5 parks to surf the Internet:')
    for street_and_wifi in top_five_parks_to_surf_the_internet:
        print('park:', street_and_wifi[0], ': wi-fi points amount:', street_and_wifi[1])

    print(f'top 5 streets to surf the Internet:')
    for street_and_wifi in top_five_streets_to_surf_the_internet:
        print('street:', street_and_wifi[0], ': wi-fi points amount:', street_and_wifi[1])
