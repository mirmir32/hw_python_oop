from typing import ClassVar, Dict
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    # С передачей словаря (asdict) в функцию так и не разобрался.
    # Структура, вроде бы, в целом ясна, но никак не
    # получается переварить правильный синтаксис,
    # так еще и в итоге округлить всё надо до трех знаков
    # после запятой.

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM: ClassVar[int] = 1000
    M_IN_H: ClassVar[int] = 60
    LEN_STEP: ClassVar[float] = 0.65
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Не определен метод get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEF_CAL_RUN_1: ClassVar[int] = 18
    COEF_CAL_RUN_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return (((self.COEF_CAL_RUN_1 * self.get_mean_speed()
                - self.COEF_CAL_RUN_2))
                * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_CAL_SWALKING_1: ClassVar[float] = 0.035
    COEF_CAL_SWALKING_2: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        return ((self.COEF_CAL_SWALKING_1 + self.COEF_CAL_SWALKING_2
                * (self.get_mean_speed() ** 2 // self.height))
                * self.weight * self.duration * self.M_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    COEF_CAL_SWIMMING_1: ClassVar[float] = 1.1
    COEF_CAL_SWIMMING_2: ClassVar[float] = 2
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_CAL_SWIMMING_1)
                * self.COEF_CAL_SWIMMING_2 * self.weight)

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / self.M_IN_KM)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    WORKOUT_TYPE_LIST: Dict[str, Training] = {'RUN': Running,
                                              'WLK': SportsWalking,
                                              'SWM': Swimming
                                              }
    if workout_type not in WORKOUT_TYPE_LIST:
        raise TypeError(f'Тип тренировки {workout_type} не поддерживается')
    return WORKOUT_TYPE_LIST[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
