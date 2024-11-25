import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.cm import get_cmap

temperature_file = "processed_data/temperature.csv"
irradiance_file = "processed_data/irradiance.csv"

def plot_seasonal_profiles(avg_irradiance, avg_temperature, seasons):
    fig, axs = plt.subplots(len(seasons), 1, figsize=(12, 12), sharex=True)
    cmap = get_cmap("tab10")  # Use a colormap for unique colors

    for i, season in enumerate(seasons):
        season_data_irr = avg_irradiance.loc[avg_irradiance.index.get_level_values("season") == season]
        season_data_temp = avg_temperature.loc[avg_temperature.index.get_level_values("season") == season]

        temp_min = season_data_temp["t2m"].min() - 2
        temp_max = season_data_temp["t2m"].max() + 2
        norm_factor = season_data_irr["GHI"].max()  

        ax2 = axs[i].twinx()  # Create twin axis for temperature
        lines = []  # Collect line objects for legend
        labels = []  # Collect labels for legend

        for j, year in enumerate(season_data_irr.index.get_level_values("year").unique()):
            year_irradiance = season_data_irr.loc[season_data_irr.index.get_level_values("year") == year]
            year_temperature = season_data_temp.loc[season_data_temp.index.get_level_values("year") == year]

            color = cmap(j)

            # Plot irradiance
            line1, = axs[i].plot(
                pd.to_datetime(year_irradiance.index.get_level_values("time")),
                year_irradiance["GHI"],
                label=f"GHI ({year})",
                color=color,
                linewidth=2,
            )
            lines.append(line1)
            labels.append(f"GHI ({year})")

            normalized_temp = (year_temperature["t2m"] - temp_min) / (temp_max - temp_min) * norm_factor

            # Plot normalized temperature
            line2, = ax2.plot(
                pd.to_datetime(year_temperature.index.get_level_values("time")),
                normalized_temp,
                label=f"Temperature ({year})",
                color=color,
                linewidth=2,
                linestyle="--",
            )
            lines.append(line2)
            labels.append(f"Temperature ({year})")

            ax2.set_ylim(0, norm_factor)
            temp_ticks = np.linspace(temp_min, temp_max, 5)
            normalized_ticks = (temp_ticks - temp_min) / (temp_max - temp_min) * norm_factor
            ax2.set_yticks(normalized_ticks)
            ax2.set_yticklabels([f"{tick:.1f}" for tick in temp_ticks])

        axs[i].set_title(f"{season.capitalize()} Average Profile")
        axs[i].set_ylabel("Irradiance (W/m²)")
        ax2.set_ylabel("Temperature (°C)", color="black")

        # Add a combined legend for both axes
        axs[i].legend(lines, labels, loc="upper left", fontsize=8)

    axs[-1].set_xlabel("Time of Day")
    axs[-1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    plt.tight_layout()
    plt.show()

def get_csv_data(temperature_file, irradiance_file):
    irradiance = pd.read_csv(irradiance_file)
    irradiance["index_date"] = pd.to_datetime(irradiance["index_date"], errors='coerce')
    irradiance.set_index(irradiance["index_date"], inplace=True)

    temperature = pd.read_csv(temperature_file)
    temperature["valid_time"] = pd.to_datetime(temperature["valid_time"], errors='coerce')
    temperature.set_index(temperature["valid_time"], inplace=True)

    return irradiance, temperature

def assign_season(month):
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "autumn"
    else:
        return None  # Handle edge cases gracefully

def compute_total_year_time_averages(df):
    return df.groupby(["season", "time"]).mean()

def compute_seasonal_time_averages(df):
    df["year"] = df.index.year  # Extract year
    return df.groupby(["year", "season", "time"]).mean()

irradiance, temperature = get_csv_data(temperature_file, irradiance_file)

irradiance["season"] = irradiance.index.month.map(assign_season)
temperature["season"] = temperature.index.month.map(assign_season)


# Ensure correct date format for "time" column
irradiance["time"] = irradiance.index.strftime("%H:%M:%S")  # Use only time formatting
temperature["time"] = temperature.index.strftime("%H:%M:%S")

print(irradiance)

seasons = ["winter", "spring", "summer", "autumn"]
irradiance["season"] = pd.Categorical(irradiance["season"], categories=seasons, ordered=True)
temperature["season"] = pd.Categorical(temperature["season"], categories=seasons, ordered=True)

avg_irradiance = compute_seasonal_time_averages(irradiance)
avg_temperature = compute_seasonal_time_averages(temperature)

avg_irradiance.to_csv("irradiance_seasons.csv")
avg_temperature.to_csv("temperature_seasons.csv")

total_year_irradiance_avg = compute_total_year_time_averages(irradiance)
total_year_temperature_avg = compute_total_year_time_averages(temperature)
total_year_irradiance_avg.to_csv("processed_data/total_irradiance_4_years.csv")
total_year_temperature_avg.to_csv("processed_data/total_temperature_4_years.csv")
print(total_year_irradiance_avg['GHI'])

# plot_seasonal_profiles(total_year_irradiance_avg, total_year_temperature_avg, seasons)

# avg_irradiance = avg_irradiance.groupby(["season"]).mean()
# avg_temperature = avg_temperature.groupby(["season"]).mean()
# plot_seasonal_profiles(avg_irradiance, avg_temperature, seasons)
plot_seasonal_profiles(avg_irradiance, avg_temperature, seasons)

