---
title: AirQo PM2.5 Forecasts
emoji: 🌫️
colorFrom: green
colorTo: purple
sdk: static
pinned: false
short_description: August 2026 PM2.5 forecasts for 149 AirQo sensors
---

# AirQo PM2.5 Forecasts

A static page showing the PM2.5 forecasts produced by the AirQo PM2.5 model ([Kyalis/airqo-pm25-random-forest](https://huggingface.co/Kyalis/airqo-pm25-random-forest)) for 149 AirQo sensors in Uganda:

- daily forecasts for 1–14 August 2026, as an AQI-coloured calendar;
- hourly forecasts for 1 August 2026, as a bar chart with the AQI category boundaries.

The forecasts come from the current forecast model, a tuned SVR that predicts PM2.5 from temperature, humidity, time and sensor identity (no PM10). August weather was not known in advance, so each sensor's typical values for each hour were used.

The page has no backend: it reads `forecasts.json`, which holds the predictions the model made when the full pipeline was run. Server-side Spaces need a paid plan, so the page cannot run the model itself. To make new predictions, download the model from the model repository and run `pm25_inference.py`.

AQI categories (µg/m³): Good 0–9 · Moderate 9.1–35.49 · Unhealthy for Sensitive Groups 35.5–55.49 · Unhealthy 55.5–125.49 · Very Unhealthy 125.5–225.49 · Hazardous above 225.49.

Built for CSC3119 AI Deployment & Scalability, Assignment 4, Uganda Christian University.
