include .env

build:
	@ docker compose up -d

run_bot_locally:
	@ python3 main.py

run_llama:
	@ docker run -it -p 7860:7860 --platform=linux/amd64 -e HUGGING_FACE_HUB_TOKEN=${HUGGING_FACE_HUB_TOKEN} \
		registry.hf.space/harsh-manvar-llama-2-7b-chat-test:latest python app.py