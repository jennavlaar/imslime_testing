@echo off
setlocal enabledelayedexpansion

:: Define your options
set USER_DATA_FILES=0_percent_registered.json 25_percent_registered.json 50_percent_registered.json 75_percent_registered.json 100_percent_registered.json
set USER_COUNTS=10 25 35 50
set RAMP_UPS=true false
set SCENARIOS=login full

:: Create results directory if it doesn't exist
if not exist results (
    mkdir results
)

:: Loop through all combinations
for %%F in (%USER_DATA_FILES%) do (
    for %%C in (%USER_COUNTS%) do (
        for %%R in (%RAMP_UPS%) do (
            for %%S in (%SCENARIOS%) do (
                set FILE_NAME=%%~nF
                set OUTPUT_FILE=results\result_!FILE_NAME!_users%%C_ramp%%R_%%S.json
                echo Running: %%F %%C %%R %%S > !OUTPUT_FILE!
                k6 run load_test.js --env USER_DATA_FILE=%%F --env USER_COUNT=%%C --env RAMP_UP=%%R --env SCENARIO=%%S --summary-export=!OUTPUT_FILE!
            )
        )
    )
)

echo Done running all tests.
pause
