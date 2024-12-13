# backend/config.py
class SchedulerSettings:
    cooling_delta_low = 0.333
    cooling_delta_medium = 0.5
    cooling_delta_high = 1.0
    default_delta = 0.5
    temp_regression_rate = 0.5
    cost_rate: float = 1.0
scheduler_settings = SchedulerSettings()
