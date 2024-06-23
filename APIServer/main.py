import uvicorn
import sys
import time

if __name__ == "__main__":

	init_without_error = True
	next_try_delay = 5
	try:
		while init_without_error:
			try:
				print('Try to connect to PostgreSQL')
				sys.argv.append("--reload-ignore=venv")
				uvicorn.run("APIServer:app", host="0.0.0.0", port=9001, reload=True, log_level="info")
				init_without_error = False
			except Exception as e:
				print(f'PostgreSQL connect error, pause for next try {next_try_delay} secons\nError {e}')
				time.sleep(next_try_delay)
	except KeyboardInterrupt:
		print("Execution stopped by user (Ctrl+C)")
		exit()


