.PHONY: all fetch analyze clean

all: analyze

fetch:
	@echo ">>> Starting fetch step..."
	./fetch_metars.sh
	@echo ">>> Finished fetch step. Data saved in raw_metars/"

analyze: fetch
	@echo ">>> Starting analysis step..."
	./analyze_data.sh
	@echo ">>> Finished analysis step. Results saved to weather_report.csv"
	@echo ">>> Pipeline completed successfully!"

clean:
	@echo ">>> Cleaning up generated files..."
	rm -rf raw_metars weather_report.csv
	@echo ">>> Cleanup complete."
