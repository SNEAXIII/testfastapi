ignoreError=|| exit /b 0
start_docker_desktop:
	$(shell python manage_docker_state.py start)
stop_wsl:
	$(shell python manage_docker_state.py stop)
create_ssl_keys:
	php $(api_console_path) lexik:jwt:generate-keypair
build:
	make start_docker_desktop
	docker compose build
up:
	make start_docker_desktop
	docker compose up
buildup:
	make build
	make up
stop:
	docker compose stop
down:
	docker compose down --remove-orphans
rm:
	docker rm -f $(shell docker ps -aq) $(ignoreError)
prune:
	make rm
	docker system prune -af
portainer:
	docker run -d -p 80:80 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
	cmd /c start "https://localhost:9443"
end:
	make stop
	make stop_wsl
kill:
	make end
	make rm
myadmin:
	cmd /c start "http://localhost:8080/"
docs:
	cmd /c start "http://localhost:8000/docs"
dump:
	docker exec mysql /tools/dump.sh
populate:
	curl --location --request POST 'http://localhost:8000/populate_db'