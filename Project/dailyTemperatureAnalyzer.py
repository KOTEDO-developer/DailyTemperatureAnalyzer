import logging
import os
from datetime import time

import pandas as pd


""" Настройка логгера """

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("dailyTemperatureAnalyzer.log"),
        logging.StreamHandler()
    ]
)


"""Класс-обработчик ошибок и логов"""

class dailyTemperatureAnalyzerErrorHandler:
    @staticmethod
    def handle_error(context: str, exception: Exception):
        logging.error(f"[{context}] Ошибка: {exception}")

    @staticmethod
    def warn(message: str):
        logging.warning(message)

    @staticmethod
    def info(message: str):
        logging.info(message)


"""Основная бизнес-логика проекта"""


class dailyTemperatureAnalyzer:
    def __init__(self, source_file: str, export_file: str):
        self.source_file = source_file
        self.export_file = export_file
        self.dataset = None
        self.summary = None
        self.logger = dailyTemperatureAnalyzerErrorHandler

    def run(self):
        self.logger.info("=== Запуск анализа погодных данных ===")
        self.load_data()
        if self.dataset is not None and not self.dataset.empty:
            self.preprocess()
            if self.dataset is not None and not self.dataset.empty:
                self.filter_daytime_observations()
                if self.dataset is not None and not self.dataset.empty:
                    self.aggregate_temperatures()
                    if self.summary is not None and not self.summary.empty:
                        self.save_results()
                        self.display_statistics()
                    else:
                        self.logger.warn("Нет итогов для сохранения или отображения.")
                else:
                    self.logger.warn("Нет записей после фильтрации по времени.")
            else:
                self.logger.warn("Нет данных после предобработки.")
        else:
            self.logger.warn("Данные не загружены или пусты.")
        self.logger.info("=== Завершение работы ===")

    def load_data(self):
        self.logger.info(f"Загрузка файла: {self.source_file}")
        try:
            df = pd.read_excel(self.source_file, header=6)
            if df.empty:
                raise ValueError("Файл прочитан, но он пустой.")
            self.dataset = df
            self.logger.info("Файл успешно загружен.")
        except Exception as e:
            self.logger.handle_error("Загрузка данных", e)
            self.dataset = None

    def preprocess(self):
        self.logger.info("Предобработка данных.")
        try:
            self.dataset.rename(columns={
                'Местное время в Москве (ВДНХ)': 'timestamp',
                'T': 'temp_c'
            }, inplace=True)

            self.dataset['timestamp'] = pd.to_datetime(
                self.dataset['timestamp'], errors='coerce', dayfirst=True
            )
            self.dataset.dropna(subset=['timestamp'], inplace=True)

            if self.dataset['temp_c'].isnull().all():
                raise ValueError("Все значения температуры отсутствуют.")

            self.dataset['temp_c'] = (
                self.dataset['temp_c']
                .astype(str)
                .str.replace(',', '.', regex=False)
                .str.replace('−', '-', regex=False)
                .str.extract(r'([-+]?\d*\.?\d+)')[0]
                .astype(float)
            )

            self.dataset.dropna(subset=['temp_c'], inplace=True)

            self.dataset['clock'] = self.dataset['timestamp'].dt.time

            if self.dataset.empty:
                raise ValueError("Нет валидных записей после предобработки.")

            self.logger.info("Предобработка завершена.")
        except Exception as e:
            self.logger.handle_error("Предобработка", e)
            self.dataset = None

    def filter_daytime_observations(self):
        self.logger.info("Фильтрация по времени суток.")
        try:
            if 'clock' not in self.dataset.columns:
                raise ValueError("Временные данные отсутствуют.")
            target_times = {time(9), time(12), time(15), time(18)}
            self.dataset = self.dataset[self.dataset['clock'].isin(target_times)].copy()

            if self.dataset.empty:
                raise ValueError("Нет записей в целевое дневное время.")

            self.logger.info(f"Фильтрация завершена. Осталось записей: {len(self.dataset)}")
        except Exception as e:
            self.logger.handle_error("Фильтрация времени", e)
            self.dataset = None

    def aggregate_temperatures(self):
        self.logger.info("Агрегация температур.")
        try:
            self.dataset['date_only'] = self.dataset['timestamp'].dt.date
            self.dataset['year_only'] = self.dataset['timestamp'].dt.year

            result = (
                self.dataset
                .groupby(['year_only', 'date_only'])['temp_c']
                .mean()
                .round(1)
                .reset_index()
                .rename(columns={'temp_c': 'mean_temp'})
            )

            if result.empty:
                raise ValueError("После группировки не получено ни одной записи.")

            self.summary = result.sort_values(by='date_only')
            self.logger.info("Агрегация завершена.")
        except Exception as e:
            self.logger.handle_error("Агрегация температур", e)
            self.summary = None

    def save_results(self):
        self.logger.info("Сохранение результатов.")
        try:
            os.makedirs(os.path.dirname(self.export_file), exist_ok=True)
            self.summary.to_excel(self.export_file, index=False)
            self.logger.info(f"Результаты сохранены в: {self.export_file}")
        except Exception as e:
            self.logger.handle_error("Сохранение файла", e)

    def display_statistics(self):
        self.logger.info("Вывод сводной статистики.")
        try:
            stats = self.summary.groupby('year_only')['mean_temp'].agg(['mean', 'min', 'max']).round(1)
            self.logger.info("\nГодовая статистика:\n" + str(stats))
            self.logger.info(f"Общее число дней в итогах: {len(self.summary)}")
        except Exception as e:
            self.logger.handle_error("Статистика", e)


def main():
    source_path = r'C:\Users\Иван\PycharmProjects\PythonProject\Project\resources\27612.01.05.2010.01.05.2025.1.0.0.ru.utf8.00000000.xls'
    export_path = r'C:\Users\Иван\PycharmProjects\PythonProject\Project\resources\result.xlsx'

    analyzer = dailyTemperatureAnalyzer(source_path, export_path)
    analyzer.run()

if __name__ == "__main__":
    main()