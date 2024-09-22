from flask import Flask, render_template, request

# Ініціалізація Flask-додатку
app = Flask(__name__)

def convert_to_cm(value, unit):
    """Конвертація одиниць довжини в сантиметри"""
    if unit == 'inch':
        return value
    elif unit == 'cm':
        return value  # Вже в сантиметрах
    else:
        raise ValueError(f"Unsupported unit: {unit}")

def convert_to_kg(value, unit):
    """Конвертація одиниць ваги в кілограми"""
    if unit == 'lb':
        return value * 0.453592  # Конвертуємо фунти в кілограми
    elif unit == 'kg':
        return value
    else:
        raise ValueError(f"Unsupported unit: {unit}")

@app.route('/', methods=['GET'])
def index():
    """Головна сторінка з формою введення даних"""
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    """Обробка форми та відображення результатів"""
    try:
        # Отримуємо дані про вантажівку
        truck_length = float(request.form['truck-length'])
        truck_length_unit = request.form['truck-length-unit']
        truck_width = float(request.form['truck-width'])
        truck_width_unit = request.form['truck-width-unit']
        truck_weight = float(request.form['truck-weight'])
        truck_weight_unit = request.form['truck-weight-unit']

        # Кількість палет
        pallet_count = int(request.form['pallet-count'])

        # Конвертація розмірів вантажівки в см
        truck_length_cm = convert_to_cm(truck_length, truck_length_unit)
        truck_width_cm = convert_to_cm(truck_width, truck_width_unit)
        truck_weight_kg = convert_to_kg(truck_weight, truck_weight_unit)

        pallets = []
        total_weight = 0

        # Проходимо по кожній палеті
        for i in range(1, pallet_count + 1):
            pallet_length = float(request.form[f'pallet-{i}-length'])
            pallet_width = float(request.form[f'pallet-{i}-width'])
            pallet_weight = float(request.form[f'pallet-{i}-weight'])
            pallet_length_unit = request.form[f'pallet-{i}-length-unit']
            pallet_width_unit = request.form[f'pallet-{i}-width-unit']
            pallet_weight_unit = request.form[f'pallet-{i}-weight-unit']

            # Конвертація розмірів палет в см
            pallet_length_cm = convert_to_cm(pallet_length, pallet_length_unit)
            pallet_width_cm = convert_to_cm(pallet_width, pallet_width_unit)
            pallet_weight_kg = convert_to_kg(pallet_weight, pallet_weight_unit)

            pallets.append({
                'length': pallet_length_cm,  # Перетворені в см розміри
                'width': pallet_width_cm,    # Перетворені в см розміри
                'weight': pallet_weight_kg,  # Вага в кг
                'length_unit': pallet_length_unit,
                'width_unit': pallet_width_unit,
                'weight_unit': pallet_weight_unit
            })
            total_weight += pallet_weight_kg

        return render_template('results.html', truck={
            'length': truck_length,
            'length_unit': truck_length_unit,
            'width': truck_width,
            'width_unit': truck_width_unit,
            'weight': truck_weight_kg,
        }, total_weight=total_weight, pallet_count=pallet_count, pallets=pallets)

    except ValueError as e:
        return render_template('results.html', error=str(e))
    except KeyError as e:
        return render_template('results.html', error=f'Missing form data: {str(e)}')
    except Exception as e:
        return render_template('results.html', error=f'An unexpected error occurred: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)