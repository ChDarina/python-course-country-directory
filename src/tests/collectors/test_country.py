"""
Тестирование функций сбора информации о странах.
"""

import pytest

from collectors.collector import CountryCollector


@pytest.mark.asyncio
class TestCollectorCountry:
    @pytest.fixture(autouse=True)
    def collector(self):
        return CountryCollector()

    @pytest.mark.asyncio
    async def test_read_countries(self, collector):
        """
        Тестирование чтения информации о стране.
        """
        assert len(await collector.read()) == 49

    @pytest.mark.asyncio
    async def test_collecting_countries(self, collector):
        """
        Тестирование получения информации о стране.
        """
        assert len(await collector.collect()) == 49
