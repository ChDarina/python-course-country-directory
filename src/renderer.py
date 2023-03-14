"""
Функции для формирования выходной информации.
"""
import datetime
from decimal import ROUND_HALF_UP, Decimal

from tabulate import tabulate

from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    @staticmethod
    def tabulate_data(data: list, headers: list[str]) -> str:
        """
        Представление данных в виде таблицы.

        :param data: Данные о сущности.
        :param headers: Список столбцов.

        :return:
        """
        return tabulate(data, headers=headers)

    async def tabulate_country(self) -> str:
        """
        Представление данных о стране в виде таблицы..

        :return:
        """
        location = self.location_info.location
        data = [
            [
                location.name,
                location.capital,
                location.capital_latitude,
                location.capital_longitude,
                location.subregion,
                location.area if location.area else "Нет информации",
                await self._format_languages(),
                await self._format_population(),
                await self._format_currency_rates(),
            ]
        ]
        return self.tabulate_data(
            data,
            [
                "Страна",
                "Столица",
                "Широта столицы",
                "Долгота столицы",
                "Регион",
                "Площадь",
                "Языки",
                "Население страны",
                "Курсы валют",
            ],
        )

    async def tabulate_news(self) -> str:
        """
        Представление данных о новостях в виде таблицы..

        :return:
        """
        location = self.location_info.news
        data = []
        for news in location:
            data.append(
                [news.source, news.title, news.url, news.published_at, news.description]
            )
        return self.tabulate_data(
            data, ["Источник", "Новость", "Ссылка", "Дата", "Описание"]
        )

    async def tabulate_weather(self) -> str:
        """
        Представление данных о погоде в виде таблицы.

        :return:
        """
        weather = self.location_info.weather
        data = [
            [
                weather.description,
                weather.temp,
                weather.wind_speed,
                weather.visibility,
                await self._format_timezone(),
            ]
        ]
        return self.tabulate_data(
            data,
            [
                "Описание",
                "Температура (°C)",
                "Скорость ветра (м/с)",
                "Видимость (м)",
                "Часовой пояс",
            ],
        )

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_timezone(self) -> str:
        """
        Форматирование информации о часовом поясе.

        :return:
        """
        number_timezone = self.location_info.weather.timezone
        # Вычисление часа из числового часового пояса
        hours = datetime.timedelta(hours=int(abs(number_timezone)))
        # Вычисление минут из числового часового пояса
        minutes = datetime.timedelta(
            minutes=int((abs(number_timezone) - int(abs(number_timezone))) * 60)
        )
        total = hours + minutes

        timezone = f"{total.seconds // 3600:02d}:{(total.seconds // 60) % 60:02d} UTC"
        if number_timezone < 0:
            timezone = "-" + timezone
        else:
            timezone = "+" + timezone

        return timezone

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )
