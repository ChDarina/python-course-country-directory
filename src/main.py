"""
Запуск приложения.
"""

import asyncclick as click

from reader import Reader
from renderer import Renderer


def print_table(title: str, table: str) -> None:
    """
    Вывод информации о сущности в консоль.

    :param title: Название таблицы.
    :param table: Таблица.
    """
    click.secho(title, fg="white")
    click.secho(table, fg="green")


@click.command()
@click.option(
    "--location",
    "-l",
    "location",
    type=str,
    help="Страна и/или город",
    prompt="Страна и/или город",
)
async def process_input(location: str) -> None:
    """
    Поиск и вывод информации о стране, погоде и курсах валют.

    :param str location: Страна и/или город
    """

    location_info = await Reader().find(location)
    if location_info:
        print_table(
            "Данные о стране:", await Renderer(location_info).tabulate_country()
        )
        print_table(
            "Данные о погоде:", await Renderer(location_info).tabulate_weather()
        )
        print_table("Данные о новостях:", await Renderer(location_info).tabulate_news())
    else:
        click.secho("Информация отсутствует.", fg="yellow")


if __name__ == "__main__":
    # запуск обработки входного файла
    # pylint: disable=E1120
    process_input(_anyio_backend="asyncio")
