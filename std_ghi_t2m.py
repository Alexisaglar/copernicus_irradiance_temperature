import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.cm import get_cmap

temperature_file = "processed_data/temperature.csv"
irradiance_file = "processed_data/irradiance.csv"

def get_csv_data(temperature_file, irradiance_file):
    irradiance = pd.read_csv(irradiance_file)
    irradiance["index_date"] = pd.to_datetime(irradiance["index_date"], errors='coerce')
    irradiance.set_index(irradiance["index_date"], inplace=True)
    irradiance.drop(columns=["index_date"], inplace=True)

    temperature = pd.read_csv(temperature_file)
    temperature["valid_time"] = pd.to_datetime(temperature["valid_time"], errors='coerce')
    temperature.set_index(temperature["valid_time"], inplace=True)
    temperature.drop(columns=["valid_time"], inplace=True)

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

def compute_seasonal_time_stats(df):
    df = df.reset_index()
    print(df)
    grouped = df.groupby(["season", "time"])
    mean_df = grouped.mean()
    std_df = grouped.std()
    print(std_df)
    return mean_df, std_df

def compute_seasonal_time_averages(df):
    df["year"] = df.index.year  # Extract year
    df = df.reset_index()
    return df.groupby(["year", "season", "time"]).mean()

def plot_combined_seasonal_profiles(avg_irradiance, avg_temperature,
                                    mean_irradiance, std_irradiance,
                                    mean_temperature, std_temperature, seasons):
    fig, axs = plt.subplots(len(seasons), 1, figsize=(12, 12), sharex=True)
    cmap = get_cmap("tab10")  # Use a colormap for unique colors

    for i, season in enumerate(seasons):
        season_data_irr = avg_irradiance.loc[avg_irradiance.index.get_level_values("season") == season]
        season_data_temp = avg_temperature.loc[avg_temperature.index.get_level_values("season") == season]

        season_mean_irr = mean_irradiance.loc[season]
        season_std_irr = std_irradiance.loc[season]
        season_mean_temp = mean_temperature.loc[season]
        season_std_temp = std_temperature.loc[season]

        temp_min = season_mean_temp["t2m"].min() - 7 
        temp_max = season_mean_temp["t2m"].max() + 7
        norm_factor = season_mean_irr["GHI"].max()

        ax2 = axs[i].twinx()

        lines = []
        labels = []

        # Plot individual years
        for j, year in enumerate(season_data_irr.index.get_level_values("year").unique()):
            year_irradiance = season_data_irr.loc[season_data_irr.index.get_level_values("year") == year]
            year_temperature = season_data_temp.loc[season_data_temp.index.get_level_values("year") == year]

            color = cmap(j % 10)  # Ensure the color index doesn't exceed colormap range

            # Convert "time" to datetime for plotting
            times = pd.to_datetime(year_irradiance.index.get_level_values("time"), format="%H:%M")

            # Plot irradiance for each year
            line1, = axs[i].plot(
                times,
                year_irradiance["GHI"],
                label=f"GHI ({year})",
                color=color,
                linewidth=1,
                alpha=0.5,
            )
            lines.append(line1)
            labels.append(f"GHI ({year})")

            # Normalize temperature for plotting
            normalized_temp = (year_temperature["t2m"] - temp_min) / (temp_max - temp_min) * norm_factor

            # Plot temperature for each year
            line2, = ax2.plot(
                times,
                normalized_temp,
                label=f"Temperature ({year})",
                color=color,
                linewidth=1,
                linestyle="--",
                alpha=0.5,
            )
            lines.append(line2)
            labels.append(f"Temperature ({year})")

        # Plot mean irradiance with standard deviation shading
        times_mean = pd.to_datetime(season_mean_irr.index.get_level_values("time"), format="%H:%M")
        axs[i].plot(times_mean, season_mean_irr["GHI"], color="black", linewidth=2, label="Mean GHI")
        axs[i].fill_between(times_mean,
                            season_mean_irr["GHI"] - season_std_irr["GHI"],
                            season_mean_irr["GHI"] + season_std_irr["GHI"],
                            color="blue", alpha=0.2)

        # Plot mean temperature with standard deviation shading
        normalized_mean_temp = (season_mean_temp["t2m"] - temp_min) / (temp_max - temp_min) * norm_factor
        temp_std_scaled = season_std_temp["t2m"] / (temp_max - temp_min) * norm_factor

        ax2.plot(times_mean, normalized_mean_temp, color="darkred", linewidth=2, linestyle="--", label="Mean Temperature")
        ax2.fill_between(times_mean,
                         normalized_mean_temp - temp_std_scaled,
                         normalized_mean_temp + temp_std_scaled,
                         color="red", alpha=0.2)

        # Set y-limits and labels
        axs[i].set_title(f"{season.capitalize()} Combined Profile")
        axs[i].set_ylabel("Irradiance (W/m²)")
        ax2.set_ylabel("Temperature (°C)")
        ax2.set_ylim(0, norm_factor)
        temp_ticks = np.linspace(temp_min, temp_max, 5)
        normalized_ticks = (temp_ticks - temp_min) / (temp_max - temp_min) * norm_factor
        ax2.set_yticks(normalized_ticks)
        ax2.set_yticklabels([f"{tick:.1f}" for tick in temp_ticks])

        # Add legends
        axs[i].legend(loc="upper left", fontsize=8)
        ax2.legend(loc="upper right", fontsize=8)

    axs[-1].set_xlabel("Time of Day")
    axs[-1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    irradiance, temperature = get_csv_data(temperature_file, irradiance_file)

    irradiance["season"] = irradiance.index.month.map(assign_season)
    temperature["season"] = temperature.index.month.map(assign_season)

    # Adjust the time resolution to include only hour and minute
    irradiance["time"] = irradiance.index.strftime("%H:%M")  # Use only hour and minute
    temperature["time"] = temperature.index.strftime("%H:%M")

    seasons = ["winter", "spring", "summer", "autumn"]
    irradiance["season"] = pd.Categorical(irradiance["season"], categories=seasons, ordered=True)
    temperature["season"] = pd.Categorical(temperature["season"], categories=seasons, ordered=True)

    # Compute seasonal time averages per year
    avg_irradiance = compute_seasonal_time_averages(irradiance)
    avg_temperature = compute_seasonal_time_averages(temperature)

    # Compute mean and standard deviation per season and time
    avg_irradiance_mean, avg_irradiance_std = compute_seasonal_time_stats(irradiance)
    avg_temperature_mean, avg_temperature_std = compute_seasonal_time_stats(temperature)

    # Plot the combined seasonal profiles
    plot_combined_seasonal_profiles(avg_irradiance, avg_temperature,
                                    avg_irradiance_mean, avg_irradiance_std,
                                    avg_temperature_mean, avg_temperature_std, seasons)
