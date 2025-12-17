import flet as ft
import requests

AREA_JSON = "https://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"

area_data = requests.get(AREA_JSON).json()
prefectures = area_data["offices"]


def get_forecast(office_code: str):
    url = FORECAST_URL.format(code=office_code)
    return requests.get(url).json()


def main(page: ft.Page):
    page.title = "天気予報（気象庁API）"
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    # --- 表示エリア ---
    result = ft.Text("左から都道府県を選択してください", size=16)

    def on_select_code(office_code: str):
        office_name = prefectures[office_code]["name"]

        try:
            data = get_forecast(office_code)
            ts = data[0]["timeSeries"]

            areas = ts[0]["areas"][0]
            weathers = areas.get("weathers", [])
            dates = ts[0].get("timeDefines", [])

            lines = [f"{office_name} の天気"]
            for d, w in zip(dates[:2], weathers[:2]):
                lines.append(f"{d[:10]}: {w}")

            result.value = "\n".join(lines)
        except Exception as ex:
            result.value = f"取得エラー: {ex}"

        page.update()

    nav_list = ft.ListView(
        expand=True,
        spacing=0,
        controls=[
            ft.ListTile(
                title=ft.Text(prefectures[k]["name"]),
                leading=ft.Icon(ft.Icons.LOCATION_ON_OUTLINED),
                on_click=lambda e, code=k: on_select_code(code),
            )
            for k in prefectures.keys()
        ],
    )

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=nav_list,
                    width=220,
                ),
                ft.VerticalDivider(width=1),
                ft.Column(
                    [result],
                    expand=True,
                ),
            ],
            expand=True,
        )
    )


ft.app(main)
