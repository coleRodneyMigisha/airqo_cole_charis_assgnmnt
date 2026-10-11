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

The page has no backend: it reads `forecasts.json`, which holds the predictions the model made when the full pipeline was run. To make new predictions, download the model from the model repository and run `pm25_inference.py`.

AQI categories (µg/m³): Good 0–9 · Moderate 9.1–35.49 · Unhealthy for Sensitive Groups 35.5–55.49 · Unhealthy 55.5–125.49 · Very Unhealthy 125.5–225.49 · Hazardous above 225.49.

Built for CSC3119 AI Deployment & Scalability, Assignment 4, Uganda Christian University.
