def temperature(I: float) -> tuple[float | None, str]:
    """

    Формула пересчёта сигнал-значение:
        PV = (I - i_min) * (PV_max - PV_min) / (i_max - i_min) + PV_min

    PV     – текущее значение температуры, °C;
    I      – значение выходного сигнала датчика, мА;
    PV_min – минимальное значение диапазона (0 °C);
    PV_max – максимальное значение диапазона (75 °C);
    i_min, i_max – токи, соответствующие PV_min и PV_max (4 и 20 мА).

    Диагностика:
        I == 0               – датчик отключён;
        0 < I < 3.9          – датчик неисправен;
        3.9 <= I <= 20.1     – всё ок (значение достоверно);
        I > 20.1             – датчик неисправен.

    Возвращает кортеж (температура, состояние):
        (float, "все ок")        – датчик исправен, значение достоверно;
        (None,  "датчик отключён");
        (None,  "датчик неисправен");
        (None,  "текст ошибки") – неверный тип или значение аргумента.

    """
    PV_min, PV_max = 0.0, 75.0
    i_min, i_max = 4.0, 20.0
    i_ok_low, i_ok_high = 3.9, 20.1

    try:
        # 1. Тип входа: bool отсекаем отдельно, он подкласс int
        if type(I) not in (int, float):
            raise TypeError(f"'I' должен быть числом")

        # 2. Значение
        if I < 0:
            raise ValueError(f"отрицательный ток: {I}")

        # 3. Диагностика
        if I == 0:
            return None, "датчик отключён"
        if not i_ok_low <= I <= i_ok_high:
            return None, "датчик неисправен"

        # 4. Вычесления
        PV = (I - i_min) * (PV_max - PV_min) / (i_max - i_min) + PV_min

        # 5. Диапазон
        PV = float(min(max(PV, PV_min), PV_max))

        return PV, "все ок"

    except (TypeError, ValueError) as error:
        return None, str(error)

for i in range(-2, 50):
        print(temperature(i / 2))
