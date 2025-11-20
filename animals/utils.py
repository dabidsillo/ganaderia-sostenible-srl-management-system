import httpx  # Cambiado de requests a httpx
import openai
from bs4 import BeautifulSoup
from typing import Dict
from .models import Animal
from datetime import date, timedelta

def get_weather_data(city):
    """Obtiene el clima actual de una ciudad desde wttr.in y procesa la respuesta."""
    url = f"https://wttr.in/{city}?format=%C+%t"  # %C: Condiciones, %t: Temperatura
    try:
        response = httpx.get(url)
        response.raise_for_status()
        raw_data = response.text.strip()  # Ejemplo: "Parcialmente nublado +30°C"
        # Separar la descripción del clima y la temperatura
        description, temperature = raw_data.split(" +")
        temperature = temperature.replace("°C", "")  # Limpiar el símbolo de grados
        return {
            "main": {"temp": float(temperature)},
            "weather": [{"description": description}]
        }
    except Exception as e:
        print(f"Error al obtener datos del clima: {e}")
        return {
            "main": {"temp": 0},
            "weather": [{"description": "Desconocido"}],
        }


def prepare_animal_data(animal, weather_data):
    """Prepara los datos para calcular el consumo del animal."""
    temperature = weather_data.get("main", {}).get("temp", 0)
    weather_conditions = weather_data.get("weather", [{}])[0].get("description", "Desconocido")
    
    return {
        "name": animal.name,
        "breed": animal.breed,
        "age": animal.calculate_age(),
        "is_pregnant": animal.is_pregnant,
        "temperature": temperature,
        "weather_conditions": weather_conditions,
    }
import openai
from typing import Dict

import openai
import json

def get_consumption_from_ai(api_key, animal_data):
    """Consulta a la IA para calcular el consumo de comida y agua."""
    openai.api_key = api_key

    # Estructura de mensajes para la nueva API
    messages = [
        {
            "role": "system",
            "content": "Eres un experto en ganadería y nutrición animal. Proporciona el consumo diario de comida y agua para un animal en formato JSON.",
        },
        {
            "role": "user",
            "content": (
                f"Proporciona el consumo diario de comida (en kg) y agua (en litros) para el siguiente animal:\n"
                f"{{\n"
                f"  \"nombre\": \"{animal_data['name']}\",\n"
                f"  \"raza\": \"{animal_data['breed']}\",\n"
                f"  \"edad\": {animal_data['age']},\n"
                f"  \"gestacion\": {str(animal_data['is_pregnant']).lower()},\n"
                f"  \"temperatura\": {animal_data['temperature']},\n"
                f"  \"condiciones_climaticas\": \"{animal_data['weather_conditions']}\"\n"
                f"}}\n"
                f"Por favor, responde únicamente en este formato:\n"
                f"{{\n"
                f"  \"comida_kg\": 15.0,\n"
                f"  \"agua_litros\": 30.0\n"
                f"}}"
            ),
        },
    ]

    try:
        # Usar `ChatCompletion` con el modelo `gpt-3.5-turbo`
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Cambiar a "gpt-4" si tienes acceso
            messages=messages,
            max_tokens=150,
        )
        
        response_text = response['choices'][0]['message']['content'].strip()
        print(f"Respuesta de la IA: {response_text}")

        # Convertir la respuesta en JSON
        response_data = json.loads(response_text)
        food_amount = response_data.get("comida_kg", 0)
        water_amount = response_data.get("agua_litros", 0)
        return food_amount, water_amount
    except Exception as e:
        print(f"Error al procesar la respuesta de la IA: {e}")
        return 0, 0



def get_weekly_weather_data(latitude, longitude):
    """
    Obtiene el clima proyectado para los próximos 7 días desde la API de Open-Meteo.
    Parámetros:
        - latitude: Latitud de la ubicación.
        - longitude: Longitud de la ubicación.
    Retorna:
        - Lista de diccionarios con datos de temperatura y condiciones climáticas por día.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        data = response.json()

        # Extraer las fechas, temperaturas y precipitación
        daily_data = []
        for i in range(len(data["daily"]["time"])):
            daily_data.append({
                "date": data["daily"]["time"][i],
                "temp_max": data["daily"]["temperature_2m_max"][i],
                "temp_min": data["daily"]["temperature_2m_min"][i],
                "precipitation": data["daily"]["precipitation_sum"][i],
            })

        return daily_data
    except Exception as e:
        print(f"Error al obtener datos climáticos semanales: {e}")
        return []


import random
from animals.utils import get_weekly_weather_data, get_consumption_from_ai, prepare_animal_data

def predict_weekly_feed(latitude, longitude):
    """
    Predice el consumo de comida y agua para los próximos 7 días considerando el clima y variaciones.
    """
    # Obtener datos climáticos de la semana
    weekly_weather = get_weekly_weather_data(latitude, longitude)

    # Preparar predicciones diarias
    predictions = []
    animals = Animal.objects.all()

    for day_data in weekly_weather:
        daily_food = 0
        daily_water = 0

        for animal in animals:
            # Preparar datos del animal con el clima de ese día
            animal_data = {
                "name": animal.name,
                "breed": animal.breed,
                "age": animal.calculate_age(),
                "is_pregnant": animal.is_pregnant,
                "temperature": (day_data["temp_max"] + day_data["temp_min"]) / 2,  # Promedio de temp
                "weather_conditions": f"Lluvia: {day_data['precipitation']} mm"
            }

            # Obtener la predicción del AI
            food, water = get_consumption_from_ai("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", animal_data)

            # Ajustar el consumo según las condiciones climáticas
            if day_data["precipitation"] > 5:  # Días lluviosos
                water *= 0.85  # Reducir el consumo de agua en un 15%
            if day_data["temp_max"] > 30:  # Días cálidos
                water *= 1.1  # Aumentar el consumo de agua en un 10%
                food *= 1.05  # Aumentar ligeramente el consumo de comida
            elif day_data["temp_max"] < 15:  # Días fríos
                food *= 0.9  # Reducir el consumo de comida en un 10%

            # Agregar variación aleatoria adicional (±5%)
            food *= random.uniform(0.95, 1.05)
            water *= random.uniform(0.95, 1.05)

            daily_food += food
            daily_water += water

        predictions.append({
            "date": day_data["date"],
            "food": round(daily_food, 2),
            "water": round(daily_water, 2),
        })

    return predictions
