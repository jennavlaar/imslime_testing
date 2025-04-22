import os
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

def parse_filename(filename):
    pattern = r"result_(\d+)_percent_registered_users(\d+)_ramp(true|false)_(full|login)\.json"
    match = re.match(pattern, filename)
    if match:
        return {
            "registered_pct": int(match.group(1)),
            "user_count": int(match.group(2)),
            "ramp": match.group(3) == "true",
            "scenario": match.group(4)
        }
    return {}

def extract_key_metrics(data):
    metrics = data.get("metrics", {})
    return {
        "http_req_duration_avg": metrics.get("http_req_duration", {}).get("avg"),
        "http_req_duration_p90": metrics.get("http_req_duration", {}).get("p(90)"),
        "http_req_duration_p95": metrics.get("http_req_duration", {}).get("p(95)"),
        "login_duration_avg": metrics.get("login_duration", {}).get("avg"),
        "login_duration_p90": metrics.get("login_duration", {}).get("p(90)"),
        "login_duration_p95": metrics.get("login_duration", {}).get("p(95)"),
        "play_duration_avg": metrics.get("play_duration", {}).get("avg"),
        "play_duration_p90": metrics.get("play_duration", {}).get("p(90)"),
        "play_duration_p95": metrics.get("play_duration", {}).get("p(95)"),
        "iteration_duration_avg": metrics.get("iteration_duration", {}).get("avg"),
        "http_req_failed_value": metrics.get("http_req_failed", {}).get("value"),
        "checks_passes": metrics.get("checks", {}).get("passes"),
        "checks_fails": metrics.get("checks", {}).get("fails"),
        "vus_max": metrics.get("vus_max", {}).get("value"),
    }

def compile_important_metrics(folder_path):
    records = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename)) as f:
                data = json.load(f)
            meta = parse_filename(filename)
            metrics = extract_key_metrics(data)
            record = {**meta, **metrics, "filename": filename}
            records.append(record)
    return pd.DataFrame(records)

def generate_visuals(df, output_folder="."):
    sns.set(style="whitegrid")
    user_levels = [10, 25, 35, 50]

    # 1. Login Duration vs User Count 
    g = sns.lmplot(
        data=df,
        x="user_count",
        y="login_duration_avg",
        hue="scenario",
        col="ramp", 
        markers=["o", "s"],
        ci=None,
        height=6,
        aspect=1.2,
        scatter_kws={"s": 100},
    )
    g.set_titles(col_template="Ramp: {col_name}")
    g.set_axis_labels("Concurrent Users", "Avg Login Duration (ms)")
    for ax in g.axes.flat:
        ax.set_xticks(user_levels)
    plt.suptitle("Login Duration vs User Count (Split by Ramp)", y=1.05)
    login_plot_path = os.path.join(output_folder, "login_duration_vs_users.png")
    plt.savefig(login_plot_path, bbox_inches='tight')
    print(f"[✓] Saved: {login_plot_path}")
    plt.close()

    # 2. Play Duration vs User Count (full scenarios only)
    df_full = df[df["scenario"] == "full"]
    if not df_full.empty:
        g2 = sns.lmplot(
            data=df_full,
            x="user_count",
            y="play_duration_avg",
            hue="ramp",
            col="ramp", 
            markers=["o", "s"],
            ci=None,
            height=6,
            aspect=1.2,
            scatter_kws={"s": 100},
        )
        g2.set_titles(col_template="Ramp: {col_name}")
        g2.set_axis_labels("Concurrent Users", "Avg Play Duration (ms)")
        for ax in g2.axes.flat:
            ax.set_xticks(user_levels)
        plt.suptitle("Play Duration vs User Count (Full Scenarios)", y=1.05)
        play_plot_path = os.path.join(output_folder, "play_duration_vs_users.png")
        plt.savefig(play_plot_path, bbox_inches='tight')
        print(f"[✓] Saved: {play_plot_path}")
        plt.close()

    # 3. Failed HTTP Requests (if there are any)
    df_fails = df[df["http_req_failed_value"] > 0]
    if not df_fails.empty:
        plt.figure(figsize=(10, 5))
        sns.barplot(data=df_fails, x="filename", y="http_req_failed_value", palette="Reds_d")
        plt.title("Failed HTTP Requests per Test")
        plt.ylabel("Failures")
        fail_plot_path = os.path.join(output_folder, "http_failures.png")
        plt.savefig(fail_plot_path)
        print(f"[✓] Saved: {fail_plot_path}")
        plt.close()

if __name__ == "__main__":
    folder_path = "./load_testing/results" 
    df = compile_important_metrics(folder_path)
    df.to_csv("important_metrics_compiled.csv", index=False)
    print("[✓] CSV exported: important_metrics_compiled.csv")

    generate_visuals(df, ".")

# [✓] Cute checks :)
