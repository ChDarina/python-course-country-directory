"""
Описание моделей данных (DTO).
"""
from datetime import datetime
from typing import Optional, List

from pydantic import Field, BaseModel


class HashableBaseModel(BaseModel):
    """
    Добавление хэшируемости для моделей.
    """

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))


class LocationDTO(HashableBaseModel):
    """
    Модель локации для получения сведений о погоде.

    .. code-block::

        LocationDTO(
            capital="Mariehamn",
            alpha2code="AX",
        )
    """

    capital: str
    alpha2code: str = Field(min_length=2, max_length=2)  # country alpha‑2 code


class CurrencyInfoDTO(HashableBaseModel):
    """
    Модель данных о валюте.

    .. code-block::

        CurrencyInfoDTO(
            code="EUR",
        )
    """

    code: str


class LanguagesInfoDTO(HashableBaseModel):
    """
    Модель данных о языке.

    .. code-block::

        LanguagesInfoDTO(
            name="Swedish",
            native_name="svenska"
        )
    """

    name: str
    native_name: str


class CountryDTO(BaseModel):
    """
    Модель данных о стране.

    .. code-block::

        CountryDTO(
            capital="Mariehamn",
            capital_latitude=10,
            capital_longitude=20,
            alpha2code="AX",
            alt_spellings=[
              "AX",
              "Aaland",
              "Aland",
              "Ahvenanmaa"
            ],
            currencies={
                CurrencyInfoDTO(
                    code="EUR",
                )
            },
            flag="http://assets.promptapi.com/flags/AX.svg",
            languages={
                LanguagesInfoDTO(
                    name="Swedish",
                    native_name="svenska"
                )
            },
            name="\u00c5land Islands",
            population=28875,
            area=17124442.0,
            subregion="Northern Europe",
            timezones=[
                "UTC+02:00",
            ],
        )
    """

    capital: str
    capital_latitude: Optional[float]
    capital_longitude: Optional[float]
    alpha2code: str
    alt_spellings: list[str]
    currencies: set[CurrencyInfoDTO]
    flag: str
    languages: set[LanguagesInfoDTO]
    name: str
    population: int
    area: Optional[float]
    subregion: str
    timezones: list[str]


class CurrencyRatesDTO(BaseModel):
    """
    Модель данных о курсах валют.

    .. code-block::

        CurrencyRatesDTO(
            base="RUB",
            date="2022-09-14",
            rates={
                "EUR": 0.016503,
            }
        )
    """

    base: str
    date: str
    rates: dict[str, float]


class WeatherInfoDTO(BaseModel):
    """
    Модель данных о погоде.

    .. code-block::

        WeatherInfoDTO(
            temp=13.92,
            pressure=1023,
            humidity=54,
            wind_speed=4.63,
            description="scattered clouds",
            visibility="10000.0",
            timezone=3
        )
    """

    temp: float
    pressure: int
    humidity: int
    wind_speed: float
    description: str
    visibility: float
    timezone: int


class NewsInfoDTO(BaseModel):
    """
    Модель данных о новости.

    .. code-block::

        NewsDTO(
            title="China: Top diplomat visits Moscow",
            description="China's top diplomat Wang Yi has arrived in Moscow and will meet with Russian Foreign Minister
                         Sergei Lavrov Wednesday, according to Russian state news agency TASS citing
                         the Russian foreign ministry.",
            source="CNN",
            url="https://edition.cnn.com/2023/02/21/china/china-wang-yi-russia-moscow-visit-intl-hnk/index.html",
            published_at="2023-02-21T12:56:51Z"
        )
    """

    title: str
    description: str
    source: str
    url: str
    published_at: datetime


class LocationInfoDTO(BaseModel):
    """
    Модель данных для представления общей информации о месте.

    .. code-block::

        LocationInfoDTO(
            location=CountryDTO(
                capital="Mariehamn",
                capital_latitude=10,
                capital_longitude=20,
                alpha2code="AX",
                alt_spellings=[
                  "AX",
                  "Aaland",
                  "Aland",
                  "Ahvenanmaa"
                ],
                currencies={
                    CurrencyInfoDTO(
                        code="EUR",
                    )
                },
                flag="http://assets.promptapi.com/flags/AX.svg",
                languages={
                    LanguagesInfoDTO(
                        name="Swedish",
                        native_name="svenska"
                    )
                },
                name="\u00c5land Islands",
                population=28875,
                area=17124442.0,
                subregion="Northern Europe",
                timezones=[
                    "UTC+02:00",
                ],
            ),
            weather=WeatherInfoDTO(
                temp=13.92,
                pressure=1023,
                humidity=54,
                wind_speed=4.63,
                description="scattered clouds",
                timezone=3
            ),
            currency_rates={
                "EUR": 0.016503,
            },
            news=[
                NewsDTO(
                    source="CNN",
                    title="The latest news about the coronavirus pandemic",
                    description="The latest news about the coronavirus pandemic",
                    url="https://www.cnn.com/world/live-news/coronavirus-pandemic-09-14-21-intl/index.html",
                    published_at="2021-09-14T20:00:00Z",
                    content="The latest news about the coronavirus pandemic",
                )
            ]
        )
    """

    location: CountryDTO
    weather: WeatherInfoDTO
    currency_rates: dict[str, float]
    news: Optional[List[NewsInfoDTO]]
